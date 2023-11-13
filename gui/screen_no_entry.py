from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class NoEntryScreen(QWidget):
    def get_vehicle_type_layout(self):
        vehicle_type_label = QLabel()
        # vehicle_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setFont(QFont("Arial", 90, QFont.Bold))
        vehicle_type_label.setText('BRAK\nWOLNYCH\nMIEJSC')
        vehicle_type_label.setStyleSheet("color: white;")
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon(f'gui/resources/images/no_entry.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(500, 500))
        # vehicle_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        vehicle_icon_label.setAlignment(Qt.AlignCenter)
        vehicle_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        vehicle_type_layout = QVBoxLayout()
        vehicle_type_layout.addWidget(vehicle_icon_label)
        vehicle_type_layout.addWidget(vehicle_type_label)
        vehicle_type_layout.setAlignment(Qt.AlignCenter)
        vehicle_type_layout.setContentsMargins(0, 0, 0, 0)

        return vehicle_type_layout

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("WJAZD")

        main_layout = QGridLayout()
        main_layout.setSpacing(5)

        main_layout.setContentsMargins(0, 0, 0, 0)

        black_fullscreen_label = QLabel()
        black_fullscreen_label.setStyleSheet("background-color: black;")
        main_layout.addWidget(black_fullscreen_label, 0, 0, 9, 16)

        ## -- TYP POJAZDU
        vehicle_type_layout = self.get_vehicle_type_layout()
        main_layout.addLayout(vehicle_type_layout, 2, 3, 5, 10)

        self.setLayout(main_layout)
