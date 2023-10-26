import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer


class SecondScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Screen")

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel()
        label.setStyleSheet("background-color: white;")
        layout.addWidget(label, 0, 0, 9, 16)

        info_label1 = QLabel("SC 12345")
        info_label1.setAlignment(Qt.AlignCenter)
        info_label1.setStyleSheet("background-color: white; color: black;")
        info_label1.setFont(QFont("Arial", 75, QFont.Bold))  # Change the font and size
        layout.addWidget(info_label1, 0, 0, 1, 16)

        ##

        # Create a label
        horizontal_label = QLabel()
        horizontal_label.setAlignment(Qt.AlignCenter)

        # Create a font with Arial 75px
        horizontal_label.setFont(QFont("Arial", 75, QFont.Bold))  # Change the font and size

        # Set the text for the label
        horizontal_label.setText("Your Text")

        original_icon = QIcon('car.png')
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(400, 400))

        # Create a horizontal layout for the icon and text
        h_layout = QHBoxLayout()
        h_layout.addWidget(icon_label)
        h_layout.addWidget(horizontal_label)

        # Add some margin to the icon and text
        h_layout.setContentsMargins(20, 20, 20, 20)

        # Add the horizontal layout to the grid layout
        layout.addLayout(h_layout, 1, 2, 1, 14)

        ##

        self.setLayout(layout)


class FullScreenApp(QMainWindow):

    def __init__(self, hide_button):
        super().__init__()

        self.second_screen = SecondScreen()

        self.setWindowTitle("FullScreenApp")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.video_widget = QLabel()  # Use a QLabel to display the video
        self.video_widget.setStyleSheet("background-color: black;")

        central_layout = QGridLayout()
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
