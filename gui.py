# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
#
#
# class FullScreenApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("FullScreenApp")
#         # self.setGeometry(100, 100, 800, 600)
#
#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#
#         video_widget = QWidget(central_widget)
#         video_widget.setStyleSheet("background-color: black;")
#         video_layout = QGridLayout()
#         video_widget.setLayout(video_layout)
#
#         central_layout = QGridLayout()
#         central_layout.addWidget(video_widget, 2, 0, 13, 13)
#
#         info_label1 = QLabel("Info 1")
#         info_label2 = QLabel("Info 2")
#
#         central_layout.addWidget(info_label1, 0, 0, 2, 13)
#         central_layout.addWidget(info_label2, 0, 13, 15, 2)
#
#         central_widget.setLayout(central_layout)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = FullScreenApp()
#     window.showFullScreen()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QFileDialog


class FullScreenApp(QMainWindow):
    def __init__(self):
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

        button = QPushButton('Przetestuj video')
        button.clicked.connect(self.openFileDialog)  # Connect the button click event to the file dialog

        central_layout.addWidget(button, 5, 5, 1, 4)  # Add the button at row=5, col=5, 1 row, 4 cols

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
    window = FullScreenApp()
    window.showFullScreen()
    sys.exit(app.exec_())
