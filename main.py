import sys

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy, QHBoxLayout, QFrame, QStackedWidget
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation

from algorithm.object_detector import YOLOv7
from utils.detections import draw

from gui.screen_welcome import WelcomeScreen
from gui.screen_no_entry import NoEntryScreen


# Inicjalizacja detektora
yolov7 = YOLOv7()
ocr_classes = ['tablica', 'truck', 'motorcycle', 'car']
yolov7.set(ocr_classes=ocr_classes, conf_thres=0.7) # Ustaw progi pewności na 0.7
yolov7.load('best.weights', classes='classes.yaml', device='cpu')  # use 'gpu' for CUDA GPU inference


def recognize_license_plate(frame):
    # detected_plates = set()

    # Wykrywanie obiektów na klatce
    detections = yolov7.detect(frame, track=True)

    vehicle_type: str = None
    license_plate: str = None

    # Sprawdzanie i zapisywanie tekstu, jeśli istnieje
    for detection in detections:
        # if detection['class'] in ocr_classes:
        #     detection_id = detection['id']
        #     text = detection.get('text', '')  # Użyj get(), aby uniknąć KeyError
        #
        #     if text and detection_id not in detected_plates:
        #         detected_plates.add(text)

        if detection['class'] == 'tablica':
            license_plate = detection.get('text', '')
        elif detection['class'] == 'car':
            vehicle_type = 'car'
        elif detection['class'] == 'truck':
            vehicle_type = 'truck'
        elif detection['class'] == 'motorcycle':
            vehicle_type = 'motorcycle'

    # detected_frame = draw(frame, detections)
    return license_plate, vehicle_type


class ParkingApp(QMainWindow):

    def __init__(self, show_load_video_button: bool):
        super().__init__()

        self.welcome_screen = None

        self.setWindowTitle("PARKING AUTOMATYCZNY")

        self.stacked_widget = QStackedWidget(self)
        self.no_entry_screen = None

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

        self.frames_without_license_plate: int = 0

    def open_welcome_screen(self, license_plate: str, vehicle_type: str):
        if self.stacked_widget.currentIndex() == 0:
            self.welcome_screen = WelcomeScreen(self.stacked_widget, license_plate, vehicle_type)

            # self.setCentralWidget(self.welcome_screen)
            self.stacked_widget.addWidget(self.welcome_screen)
            self.stacked_widget.setCurrentIndex(1)

    def open_no_entry_screen(self):
        self.close_all_screens()

        if self.stacked_widget.currentIndex() == 0:
            self.no_entry_screen = NoEntryScreen(self.stacked_widget)

            # self.setCentralWidget(self.welcome_screen)
            self.stacked_widget.addWidget(self.no_entry_screen)
            self.stacked_widget.setCurrentIndex(1)

    # def close_welcome_screen(self):
    #     if self.stacked_widget.currentIndex() != 0:
    #         self.stacked_widget.setCurrentIndex(0)
    #         self.stacked_widget.removeWidget(self.welcome_screen)
    #         self.welcome_screen.setParent(None)
    #         self.welcome_screen = None

    def close_all_screens(self):
        if self.stacked_widget.currentIndex() != 0:
            self.stacked_widget.setCurrentIndex(0)
            for i in range(self.stacked_widget.count() - 1, 0, -1):
                widget = self.stacked_widget.widget(i)
                self.stacked_widget.removeWidget(widget)
                widget.setParent(None)

    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                if not self.playing_video:
                    self.playing_video = True
                    if hasattr(self, 'load_video_button'):
                        self.load_video_button.hide()  # Hide the button during video playback

                if self.stacked_widget.currentIndex() == 0:

                    widget_width = self.video_widget.width()
                    widget_height = self.video_widget.height()

                    frame_resized = cv2.resize(frame, (widget_width, widget_height))
                    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                    height, width, channel = frame_resized.shape
                    bytesPerLine = 3 * width
                    qImg = QImage(frame_resized.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qImg)
                    self.video_widget.setPixmap(pixmap)  # Update the QLabel with the new frame

                license_plate, vehicle_type = recognize_license_plate(frame)
                if license_plate is not None and vehicle_type is not None:
                    # self.open_welcome_screen(license_plate, vehicle_type)
                    self.open_no_entry_screen()
                    self.frames_without_license_plate = 0
                else:
                    self.frames_without_license_plate += 1
                    if self.frames_without_license_plate > 60:
                        self.close_all_screens()

            else:
                self.close_all_screens()
                self.frames_without_license_plate = 0
                self.video_widget.setStyleSheet("background-color: black")
                if hasattr(self, 'load_video_button'):
                    self.load_video_button.show()  # Show the button after video playback

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                              "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file:
            # Release the existing video capture object
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

    # Check for the --test-video option
    show_test_video_button = "--test-video" in sys.argv

    if "--fullhd-window" in sys.argv:
        window = ParkingApp(show_test_video_button)
        window.setGeometry(100, 100, 1920, 1080)  # Set window size to 1920x1080
        window.show()
    else:
        window = ParkingApp(show_test_video_button)
        window.showFullScreen()

    sys.exit(app.exec())
