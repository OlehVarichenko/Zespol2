import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import numpy as np


class FullScreenApp(QMainWindow):

    def __init__(self, hide_button):
        super().__init__()

        self.setWindowTitle("FullScreenApp")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.video_widget = QLabel()  # Use a QLabel to display the video
        self.video_widget.setStyleSheet("background-color: black;")
        video_layout = QGridLayout()
        video_layout.setContentsMargins(0, 0, 0, 0)
        self.video_widget.setLayout(video_layout)

        central_layout = QGridLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.video_widget, 2, 0, 7, 14)

        info_label1 = QLabel("Info 1")
        info_label2 = QLabel("Info 2")

        central_layout.addWidget(info_label1, 0, 0, 2, 16)
        central_layout.addWidget(info_label2, 2, 14, 7, 2)

        if not hide_button:
            button = QPushButton('Przetestuj video')
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            button.clicked.connect(self.openFileDialog)
            central_layout.addWidget(button, 5, 5, 1, 4)

        central_widget.setLayout(central_layout)

        # Initialize video capture if the --test-video option is not used
        if hide_button:
            self.cap = cv2.VideoCapture(0)  # 0 for default camera

            # Create a timer to update the video frame
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # Update every 30 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.video_widget.setPixmap(pixmap)  # Update the QLabel with the new frame

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                              "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file:
            print(f"Selected file: {file}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Check for the --test-video option
    hide_button = "--test-video" not in sys.argv

    window = FullScreenApp(hide_button)
    window.showFullScreen()
    sys.exit(app.exec_())
