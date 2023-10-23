import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog, QSizePolicy


class FullScreenApp(QMainWindow):
    def __init__(self, hide_button):
        super().__init__()

        self.setWindowTitle("FullScreenApp")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        video_widget = QWidget(central_widget)
        video_widget.setStyleSheet("background-color: black;")
        video_layout = QGridLayout()
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_widget.setLayout(video_layout)

        central_layout = QGridLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(video_widget, 2, 0, 7, 14)

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

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "",
                                              "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file:
            print(f"Selected file: {file}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Check for the --test-vid option
    hide_button = "--test-video" not in sys.argv

    window = FullScreenApp(hide_button)
    window.showFullScreen()
    sys.exit(app.exec_())
