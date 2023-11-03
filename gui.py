import sys

from PyQt5 import QtCore

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer


class SecondScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ekran wjazdowy")

        # dodanie czarnego tłą dla spacingu
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        layout = QGridLayout()
        layout.setSpacing(5)

        layout.setContentsMargins(0, 0, 0, 0)

        info_label = QLabel()
        info_label.setStyleSheet("background-color: white;")
        layout.addWidget(info_label, 1, 0, 8, 16)

        license_plate_label = QLabel("SC 12345")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))
        layout.addWidget(license_plate_label, 0, 0, 1, 16)

        ##

        vehicle_type_label = QLabel()
        vehicle_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        vehicle_type_label.setFont(QFont("Arial", 65, QFont.Bold))
        vehicle_type_label.setText("Motocykl")
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon('resources/images/motorbike.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(250, 250))
        vehicle_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        vehicle_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        h_layout = QHBoxLayout()
        h_layout.addWidget(vehicle_icon_label)
        h_layout.addWidget(vehicle_type_label)
        h_layout.setAlignment(Qt.AlignCenter)

        # Add the horizontal layout to the grid layout
        layout.addLayout(h_layout, 1, 4, 1, 7)

        ##
        button_h_layout = QHBoxLayout()

        map_original_icon = QIcon('resources/images/location_help.png')
        map_icon_label = QLabel()
        map_icon_label.setPixmap(map_original_icon.pixmap(50, 50))
        map_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        map_icon_label.setContentsMargins(5, 5, 5, 5)

        button_label = QLabel()
        button_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        button_label.setFont(QFont("Arial", 20, QFont.Bold))
        button_label.setText("Pokaż miejsce na schemacie")
        button_label.setContentsMargins(5, 5, 5, 5)

        button_h_layout.addWidget(map_icon_label)
        button_h_layout.addWidget(button_label)
        button_h_layout.setAlignment(Qt.AlignCenter)

        button = QPushButton()
        button.setStyleSheet(
            "background-color: black; color: white; border-radius: 15px;"
        )
        button.setLayout(button_h_layout)
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        layout.addWidget(button, 5, 6, 1, 4)

        self.setLayout(layout)


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
