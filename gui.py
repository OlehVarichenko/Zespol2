import sys

from PyQt5 import QtCore

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer

from lpr.algorithm.object_detector import YOLOv7
from lpr.utils.detections import draw


# Inicjalizacja detektora
yolov7 = YOLOv7()
ocr_classes = ['tablica']
yolov7.set(ocr_classes=ocr_classes)
yolov7.load('best.weights', classes='classes.yaml', device='cpu')  # use 'gpu' for CUDA GPU inference


def recognize_license_plate(frame):
    texts = {}

    # Wykrywanie obiektów w klatce
    detections = yolov7.detect(frame, track=True)

    # Sprawdzenie i zapisywanie tekstu o ile został wykryty
    for detection in detections:
        if detection['class'] in ocr_classes:
            detection_id = detection['id']
            text = detection['text']
            if len(text) > 0:
                if detection_id not in texts:
                    texts[detection_id] = {
                        'most_frequent': {
                            'value': '',
                            'count': 0
                        },
                        'all': {}
                    }

                if text not in texts[detection_id]['all']:
                    texts[detection_id]['all'][text] = 0

                texts[detection_id]['all'][text] += 1

                if texts[detection_id]['all'][text] > texts[detection_id]['most_frequent']['count']:
                    texts[detection_id]['most_frequent']['value'] = text
                    texts[detection_id]['most_frequent']['count'] = texts[detection_id]['all'][text]

                if detection_id in texts:
                    detection['text'] = texts[detection_id]['most_frequent']['value']

                # Zapisujemy tekst do pliku
                with open('logs/output.txt', 'a') as file:
                    file.write(f'Detected license plate: {text}\n')

    detected_frame = draw(frame, detections)
    return detected_frame


class SecondScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ekran wjazdowy")

        # dodanie czarnego tłą dla spacingu
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        main_layout = QGridLayout()
        main_layout.setSpacing(5)

        main_layout.setContentsMargins(0, 0, 0, 0)

        white_fullscreen_label = QLabel()
        white_fullscreen_label.setStyleSheet("background-color: white;")
        main_layout.addWidget(white_fullscreen_label, 1, 0, 8, 16)

        ## -- NR REJESTRACYJNY

        license_plate_label = QLabel("SC 12345")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))
        main_layout.addWidget(license_plate_label, 0, 0, 1, 16)

        ## -- TYP POJAZDU

        vehicle_type_label = QLabel()
        vehicle_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        vehicle_type_label.setFont(QFont("Arial", 65, QFont.Bold))
        vehicle_type_label.setText("Samochód")
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon('resources/images/car.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(200, 200))
        vehicle_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        vehicle_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        vehicle_type_layout = QHBoxLayout()
        vehicle_type_layout.addWidget(vehicle_icon_label)
        vehicle_type_layout.addWidget(vehicle_type_label)
        vehicle_type_layout.setAlignment(Qt.AlignCenter)
        vehicle_type_layout.setContentsMargins(0, 0, 0, 0)

        # Add the horizontal layout to the grid layout
        main_layout.addLayout(vehicle_type_layout, 1, 5, 1, 6)

        ## -- MIEJSCE PARKINGU

        location_label = QLabel()
        location_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        location_label.setFont(QFont("Arial", 45, QFont.Bold))
        location_label.setText("Miejsce parkingu: Sektor C")
        location_label.setContentsMargins(20, 20, 20, 20)

        location_original_icon = QIcon('resources/images/location.png')
        location_icon_label = QLabel()
        location_icon_label.setPixmap(location_original_icon.pixmap(100, 100))
        location_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        location_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        location_layout = QHBoxLayout()
        location_layout.addWidget(location_icon_label)
        location_layout.addWidget(location_label)
        location_layout.setAlignment(Qt.AlignCenter)
        location_layout.setContentsMargins(0, 0, 0, 0)

        # Add the horizontal layout to the grid layout
        main_layout.addLayout(location_layout, 2, 5, 1, 6)

        ## -- PRZYCISK "POKAŻ MAPĘ"

        map_original_icon = QIcon('resources/images/location_help.png')
        show_location_icon = QLabel()
        show_location_icon.setPixmap(map_original_icon.pixmap(75, 75))
        show_location_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        show_location_icon.setContentsMargins(5, 5, 5, 5)

        show_location_label = QLabel()
        show_location_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        show_location_label.setFont(QFont("Arial", 30, QFont.Bold))
        show_location_label.setText("Pokaż miejsce na schemacie")
        show_location_label.setContentsMargins(5, 5, 5, 5)

        show_location_button_layout = QHBoxLayout()
        show_location_button_layout.addWidget(show_location_icon)
        show_location_button_layout.addWidget(show_location_label)
        show_location_button_layout.setAlignment(Qt.AlignCenter)

        show_location_button = QPushButton()
        show_location_button.setStyleSheet(
            "background-color: black; color: white; border-radius: 15px;"
        )
        show_location_button.setLayout(show_location_button_layout)
        show_location_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(show_location_button, 5, 5, 1, 6)

        self.setLayout(main_layout)


class FullScreenApp(QMainWindow):

    def __init__(self, hide_button):
        super().__init__()

        self.second_screen = SecondScreen()

        self.setWindowTitle("FullScreenApp")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.video_widget = QLabel()  # Use a QLabel to display the video
        self.video_widget.setStyleSheet("background-color: black")

        central_layout = QGridLayout()
        central_layout.setSpacing(5)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.video_widget, 1, 0, 8, 16)

        info_label1 = QLabel("PARKING AUTOMATYCZNY")
        info_label1.setAlignment(Qt.AlignCenter)
        info_label1.setStyleSheet("background-color: black; color: white;")
        info_label1.setFont(QFont("Arial", 75, QFont.Bold))  # Change the font and size

        central_layout.addWidget(info_label1, 0, 0, 1, 16)

        self.playing_video = False  # Flag to track video playback

        if not hide_button:
            self.button = QPushButton('Przetestuj video')
            self.button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.button.clicked.connect(self.open_file_dialog)
            central_layout.addWidget(self.button, 5, 6, 1, 4)

        central_widget.setLayout(central_layout)

        # Initialize video capture if the --test-video option is not used
        if hide_button:
            self.cap = cv2.VideoCapture(0)  # 0 for the default camera
        else:
            self.cap = None  # Initialize the video capture object as None

        # Create a timer to update the video frame
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(30)  # Update every 30 milliseconds

        self.open_second_screen()

    def open_second_screen(self):
        self.setCentralWidget(self.second_screen)

    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                if not self.playing_video:
                    self.playing_video = True
                    self.video_widget.setStyleSheet("background-color: black;")
                    if hide_button is not True:
                        self.button.hide()  # Hide the button during video playback

                widget_width = self.video_widget.width()
                widget_height = self.video_widget.height()

                frame = cv2.resize(frame, (widget_width, widget_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                height, width, channel = frame.shape
                bytesPerLine = 3 * width
                qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImg)
                self.video_widget.setPixmap(pixmap)  # Update the QLabel with the new frame
            else:
                if self.playing_video:
                    self.playing_video = False
                    self.video_widget.setStyleSheet("background-color: black")
                    self.button.show()  # Show the button after video playback

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
    hide_button = "--test-video" not in sys.argv

    if "--fullhd-window" in sys.argv:
        window = FullScreenApp(hide_button)
        window.setGeometry(100, 100, 1920, 1080)  # Set window size to 1920x1080
        window.show()
    else:
        window = FullScreenApp(hide_button)
        window.showFullScreen()

    sys.exit(app.exec())
