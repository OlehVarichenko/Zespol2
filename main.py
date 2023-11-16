import sys
from enum import IntEnum
from typing import Optional

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

from db.db_communicator import PostrgesDatabaseCommunicator

# Inicjalizacja detektora
yolov7 = YOLOv7()
ocr_classes = ['tablica', 'truck', 'motorcycle', 'car']
yolov7.set(ocr_classes=ocr_classes, conf_thres=0.7)  # Ustaw progi pewności na 0.7
# wybór cpu/gpu
device = 'cuda' if cuda.is_available() else 'cpu'
yolov7.load('best.weights', classes='classes.yaml', device=device)


def sanitize_license_plate(license_plate: str) -> str:
    license_plate = license_plate.replace(' ', '')
    license_plate = license_plate.replace('-', '')
    license_plate = license_plate.replace('/', '')
    return license_plate


def recognize_vehicle(frame):
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

    def __init__(self, show_load_video_button: bool):
        super().__init__()

        self.welcome_screen = None
        self.message_screen = None
        self.exit_screen = None

        self.db_communicator = PostrgesDatabaseCommunicator(
            "parking", "Q1234567",
            "127.0.0.1", 5432, "ParkingDB"
        )

        self.setWindowTitle("PARKING AUTOMATYCZNY")

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.main_window_widget = QWidget(self)

        self.video_widget = QLabel()  # Use a QLabel to display the video
        self.video_widget.setStyleSheet("background-color: black")

        main_window_layout = QGridLayout()
        main_window_layout.setSpacing(5)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.addWidget(self.video_widget, 1, 0, 8, 16)

        header_label = QLabel("PARKING AUTOMATYCZNY")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("background-color: black; color: white;")
        header_label.setFont(QFont("Arial", 75, QFont.Bold))  # Change the font and size

        main_window_layout.addWidget(header_label, 0, 0, 1, 16)

        self.playing_video = False  # Flag to track video playback
        self.vehicle_already_detected = False

        if show_load_video_button:
            self.load_video_button = QPushButton('Przetestuj video')
            self.load_video_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.load_video_button.clicked.connect(self.open_file_dialog)
            main_window_layout.addWidget(self.load_video_button, 5, 5, 1, 6)
            self.cap = None  # Initialize the video capture object as None
        else:
            self.cap = cv2.VideoCapture(0)  # 0 for the default camera

        self.main_window_widget.setLayout(main_window_layout)

        self.stacked_widget.addWidget(self.main_window_widget)

        # Create a timer to update the video frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)  # Update every 10 milliseconds

        self.frames_without_detection: int = 0
        self.previous_license_plate: Optional[str] = None
        self.previous_vehicle_type: Optional[str] = None
        self.frames_with_same_detection: int = 0

    def on_vehicle_detection(self, vehicle_type: str, license_plate: str):
        with self.db_communicator as comm:
            bill = comm.get_bill(license_plate)
            if bill is None:
                self.open_welcome_screen(vehicle_type, license_plate)
            else:
                self.message_screen = MessageScreen(self.stacked_widget, Messages.GENERAL_ERROR)
                self.stacked_widget.addWidget(self.message_screen)
                self.stacked_widget.setCurrentIndex(1)

    def open_welcome_screen(self, vehicle_type: str, license_plate: str):
        if self.stacked_widget.currentIndex() == 0:

            result = self.db_communicator.new_stay(vehicle_type, license_plate)

            if result is True:
                self.welcome_screen = WelcomeScreen(self.stacked_widget, vehicle_type, license_plate)
                self.stacked_widget.addWidget(self.welcome_screen)
                self.stacked_widget.setCurrentIndex(1)
            else:
                self.message_screen = MessageScreen(self.stacked_widget, Messages.GENERAL_ERROR)
                self.stacked_widget.addWidget(self.message_screen)
                self.stacked_widget.setCurrentIndex(1)

    def open_message_screen(self, message_enum: IntEnum):
        self.close_all_screens()

        if self.stacked_widget.currentIndex() == 0:
            self.message_screen = MessageScreen(self.stacked_widget,
                                                message_enum)

            self.stacked_widget.addWidget(self.message_screen)
            self.stacked_widget.setCurrentIndex(1)

    def open_exit_screen(self, vehicle_type: str, license_plate: str):
        if self.stacked_widget.currentIndex() == 0:
            self.exit_screen = ExitScreen(self.stacked_widget, vehicle_type, license_plate)

            self.stacked_widget.addWidget(self.exit_screen)
            self.stacked_widget.setCurrentIndex(1)

    def close_all_screens(self):
        if self.stacked_widget.currentIndex() != 0:
            self.stacked_widget.setCurrentIndex(0)
            for i in range(self.stacked_widget.count() - 1, 0, -1):
                widget = self.stacked_widget.widget(i)
                self.stacked_widget.removeWidget(widget)
                widget.setParent(None)

    @staticmethod
    def get_resized_pixmap_from_frame(frame, width: int, height: int):
        frame_resized = cv2.resize(frame, (width, height))
        frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        height, width, channel = frame_resized.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame_resized.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)

        return pixmap

    def update_frame(self):
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

                    if self.frames_with_same_detection > 5:
                        # self.open_welcome_screen(vehicle_type, license_plate)
                        # self.open_message_screen(Messages.DETECTION_ERROR)
                        # self.open_exit_screen(license_plate, vehicle_type)
                        if not self.vehicle_already_detected:
                            self.on_vehicle_detection(vehicle_type, license_plate)
                        self.vehicle_already_detected = True

                    self.previous_license_plate = license_plate
                    self.previous_vehicle_type = vehicle_type
                    self.frames_without_detection = 0
                else:

                    self.frames_without_detection += 1
                    if self.frames_without_detection > 60:
                        self.vehicle_already_detected = False
                        self.close_all_screens()

            else:
                self.playing_video = False
                self.close_all_screens()
                self.frames_without_detection = 0
                self.video_widget.setStyleSheet("background-color: black")
                if hasattr(self, 'load_video_button'):
                    self.load_video_button.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                              "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file:
            if self.cap is not None:
                self.cap.release()

            # Open the selected video file
            self.cap = cv2.VideoCapture(file)

            if self.cap.isOpened():
                print(f"Selected file: {file}")
            else:
                print(f"Failed to open the video file: {file}")


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
