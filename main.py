import sys
from decimal import Decimal
from enum import IntEnum
from typing import Optional, Tuple

import cv2
from torch import cuda
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy, QStackedWidget
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

from algorithm.object_detector import YOLOv7

from gui.screen_exit import ExitScreen
from gui.screen_welcome import WelcomeScreen
from gui.screen_message import MessageScreen, Messages

from db.db_communicator import PostgresDatabaseCommunicator

# Inicjalizacja detektora
yolov7 = YOLOv7()
ocr_classes = ['tablica', 'truck', 'motorcycle', 'car']
yolov7.set(ocr_classes=ocr_classes, conf_thres=0.7)  # Ustawienie progów pewności
# Wybór cpu/gpu
device = 'cuda' if cuda.is_available() else 'cpu'
yolov7.load('best.weights', classes='classes.yaml', device=device)


def sanitize_license_plate(license_plate: str) -> str:
    """
    Funkcja usuwa niepożądane znaki z wykrytych numerów rejestracyjnych

    Args:
        license_plate(str): Numer rejestracyjny

    Returns:
        str: Oczyszczony numer rejestracyjny

    """
    license_plate = license_plate.replace(' ', '')
    license_plate = license_plate.replace('-', '')
    license_plate = license_plate.replace('/', '')
    return license_plate


def recognize_vehicle(frame) -> Tuple[Optional[str], Optional[str]]:
    """
    Funkcja przekazuje klatkę YOLOv7 i dostaje wynik

    Args:
        frame:

    Returns:
        Tuple[Optional[str], Optional[str]]: Numer rejestracyjny, typ pojazdu

    """
    # Wykrywanie obiektów na klatce
    detections = yolov7.detect(frame, track=True)

    vehicle_type: Optional[str] = None
    license_plate: Optional[str] = None

    # Sprawdzanie i zapisywanie tekstu, jeśli istnieje
    for detection in detections:
        if detection['class'] == 'tablica':
            license_plate = detection.get('text', '')
        elif detection['class'] == 'car':
            vehicle_type = 'car'
        elif detection['class'] == 'truck':
            vehicle_type = 'truck'
        elif detection['class'] == 'motorcycle':
            vehicle_type = 'motorcycle'

    return license_plate, vehicle_type


class ParkingApp(QMainWindow):
    """
    Klasa główna aplikacji. Zawiera w sobie kod zarządzający.
    """

    def __init__(self, show_load_video_button: bool):
        """
        Funkcja inicjalizuje aplikację. Pozwala na wybór źródła video pomiędzy kamerką a plikami video.

        Args:
            show_load_video_button(bool): Czy ignorować kamerkę i zamiast tego wyświetlić przycisk z możliwością ładowania video?
        """
        super().__init__()

        self.welcome_screen = None
        self.message_screen = None
        self.exit_screen = None

        self.db_communicator = PostgresDatabaseCommunicator(
            "parking", "Q1234567",
            "127.0.0.1", 5432, "ParkingDB"
        )

        self.setWindowTitle("PARKING AUTOMATYCZNY")

        # Główny (centralny) widżet stosowy do którego można dodawać/usuwać widżety,
        # używany podczas całego działania aplikacji
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.main_window_widget = QWidget(self)

        self.video_widget = QLabel()
        self.video_widget.setStyleSheet("background-color: black")

        main_window_layout = QGridLayout()
        main_window_layout.setSpacing(5)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.addWidget(self.video_widget, 1, 0, 8, 16)

        header_label = QLabel("PARKING AUTOMATYCZNY")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("background-color: black; color: white;")
        header_label.setFont(QFont("Arial", 75, QFont.Bold))

        main_window_layout.addWidget(header_label, 0, 0, 1, 16)

        # Jeśli plik zamiast kamerki
        if show_load_video_button:
            self.load_video_button = QPushButton('Przetestuj video')
            self.load_video_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.load_video_button.clicked.connect(self.open_file_dialog)
            main_window_layout.addWidget(self.load_video_button, 5, 5, 1, 6)
            self.cap = None
        else:
            self.cap = cv2.VideoCapture(0)

        self.main_window_widget.setLayout(main_window_layout)

        self.stacked_widget.addWidget(self.main_window_widget)

        # Zegar sondujący kamerkę/plik video
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

        # Flagi używane w celu uniemożliwienia zduplikowanych/nietrafnych wykryć
        # oraz w celu zamknięcia widżetów po odjeździe pojazdu
        self.frames_without_detection: int = 0
        self.previous_license_plate: Optional[str] = None
        self.previous_vehicle_type: Optional[str] = None
        self.frames_with_same_detection: int = 0
        self.playing_video = False
        self.vehicle_already_detected = False

    def on_vehicle_detection(self, vehicle_type: str, license_plate: str) -> None:
        """
        Funkcja próbująca pobrać rachunek za postój i wyświetlić ekran z opłatami.
        W razie braku postoju (bill is None) wyświetla ekran powitalny + dodaje postój do bazy.

        W razie wyjątku wyświetla komunikat z błędem.

        Args:
            vehicle_type(str): Typ pojazdu (car/motorcycle/truck)
            license_plate(str): Numer rejestracyjny

        Returns:
            None

        """
        try:
            bill = self.db_communicator.get_bill(license_plate)
            if bill is None:
                self.open_welcome_screen(vehicle_type, license_plate)
            else:
                self.open_exit_screen(bill.stay_id, vehicle_type,
                                      license_plate, bill.tariff, bill.stay_duration)
        except:
            self.open_message_screen(Messages.GENERAL_ERROR)

    def open_welcome_screen(self, vehicle_type: str, license_plate: str) -> None:
        """
        Funkcja dodaje do bazy danych nowy postój i wyświetla ekran powitalny.

        W razie wyjątku wyświetla komunikat z błędem.

        Args:
            vehicle_type(str): Typ pojazdu (car/motorcycle/truck)
            license_plate(str): Numer rejestracyjny

        Returns:
            None

        """
        if self.stacked_widget.currentIndex() == 0:
            try:
                sector_name = self.db_communicator.new_stay(vehicle_type, license_plate)
                if sector_name is None:
                    self.open_message_screen(Messages.NO_FREE_PARKING_LOTS_SOME_TYPE)
                    return

                self.welcome_screen = WelcomeScreen(self.stacked_widget, vehicle_type,
                                                    license_plate, sector_name)
                self.stacked_widget.addWidget(self.welcome_screen)
                self.stacked_widget.setCurrentIndex(1)
            except:
                self.open_message_screen(Messages.GENERAL_ERROR)

    def open_message_screen(self, message_enum: IntEnum) -> None:
        """
        Funkcja usuwa wszystkie widżety ze stosu, dodaje komunikat na stos i wyswietla go.

        Args:
            message_enum(IntEnum): Enum z typem komunikatu

        Returns:
            None

        """
        self.close_all_screens()

        if self.stacked_widget.currentIndex() == 0:
            self.message_screen = MessageScreen(self.stacked_widget,
                                                message_enum)

            self.stacked_widget.addWidget(self.message_screen)
            self.stacked_widget.setCurrentIndex(1)

    def open_exit_screen(self, stay_id: int, vehicle_type: str, license_plate: str,
                         tariff: Decimal, stay_duration: int) -> None:
        """
        Funkcja wyświetla ekran z opłatami.

        W razie wyjątku wyświetla komunikat z błędem.

        Args:
            stay_id(int): ID postoju
            vehicle_type(str): Typ pojazdu
            license_plate(str): Numer rejestracyjny
            tariff(Decimal): Taryfa za godzinę
            stay_duration(int): Czas postoju w sekundach

        Returns:
            None

        """
        if self.stacked_widget.currentIndex() == 0:
            try:
                self.exit_screen = ExitScreen(self.stacked_widget, stay_id, vehicle_type,
                                              license_plate, tariff, stay_duration)

                self.stacked_widget.addWidget(self.exit_screen)
                self.stacked_widget.setCurrentIndex(1)
            except:
                self.open_message_screen(Messages.GENERAL_ERROR)

    def close_all_screens(self) -> None:
        """
        Usuwa wszystkie widżety ze stosu i wraca do ekranu z odtwarzaniem strumienia video.

        Returns:
            None

        """
        if self.stacked_widget.currentIndex() != 0 and self.stacked_widget.count() > 0:
            self.stacked_widget.setCurrentIndex(0)
            for i in range(self.stacked_widget.count() - 1, 0, -1):
                widget = self.stacked_widget.widget(i)
                self.stacked_widget.removeWidget(widget)
                widget.setParent(None)

    @staticmethod
    def get_resized_pixmap_from_frame(frame, width: int, height: int) -> QPixmap:
        """
        Funkcja zwraca pixmap o odpowiedniej wielkości na podstawie klatki video.

        Args:
            frame: Klatka video
            width: Żądana szerokość
            height: Żądana wysokość

        Returns:
            QPixmap

        """
        frame_resized = cv2.resize(frame, (width, height))
        frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_resized.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame_resized.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)

        return pixmap

    def update_frame(self) -> None:
        """
        Funkcja uruchamia się przez QTimera i sprawdza obecność nowych klatek w strumieniu video,
        uzyskuje dane od modelu i podejmuje działania po uzyskaniu danych.

        Returns:
            None

        """
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                if not self.playing_video:
                    self.playing_video = True
                    if hasattr(self, 'load_video_button'):
                        self.load_video_button.hide()

                if self.stacked_widget.currentIndex() == 0:
                    pixmap = self.get_resized_pixmap_from_frame(
                        frame,
                        self.video_widget.width(),
                        self.video_widget.height()
                    )
                    self.video_widget.setPixmap(pixmap)

                license_plate, vehicle_type = recognize_vehicle(frame)

                if license_plate is not None and vehicle_type is not None:
                    license_plate = sanitize_license_plate(license_plate)

                    if license_plate == self.previous_license_plate \
                            and vehicle_type == self.previous_vehicle_type:
                        self.frames_with_same_detection += 1
                    else:
                        self.frames_with_same_detection = 0

                    # Przeciwdziałamy złej detekcji, przyjmyjemy tylko stabilnie wykrywane dane
                    if self.frames_with_same_detection > 5:
                        # Przeciwdziałamy powtórnej detekcji
                        if not self.vehicle_already_detected:
                            self.on_vehicle_detection(vehicle_type, license_plate)
                        self.vehicle_already_detected = True

                    self.previous_license_plate = license_plate
                    self.previous_vehicle_type = vehicle_type
                    self.frames_without_detection = 0
                # W razie niewykrycia pojazdu
                else:
                    self.frames_without_detection += 1
                    if self.frames_without_detection > 60:
                        self.vehicle_already_detected = False
                        self.close_all_screens()
            # W razie braku klatek
            else:
                self.playing_video = False
                self.vehicle_already_detected = False
                self.close_all_screens()
                self.frames_without_detection = 0
                self.video_widget.setStyleSheet("background-color: black")
                if hasattr(self, 'load_video_button'):
                    self.load_video_button.show()

    def open_file_dialog(self):
        """
        Funkcja otwiera dialog z wyborem pliku video po naciśnięciu odpowiedniego przycisku.
        W razie wyboru odpowiedniego pliku zamyka strumień video o ile jest obecny
        i ustawia odpowiednio źródło strumienia video.

        Returns:
            None

        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                              "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file:
            if self.cap is not None:
                self.cap.release()

            self.cap = cv2.VideoCapture(file)

            if self.cap.isOpened():
                print(f"Wybrano plik: {file}")
            else:
                print(f"Nie udało się otworzyć pliku: {file}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    show_test_video_button = "--test-video" in sys.argv

    if "--fullhd-window" in sys.argv:
        window = ParkingApp(show_test_video_button)
        window.setGeometry(100, 100, 1920, 1080)
        window.show()
    else:
        window = ParkingApp(show_test_video_button)
        window.showFullScreen()

    sys.exit(app.exec())
