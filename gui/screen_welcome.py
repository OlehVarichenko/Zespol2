from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from gui.screen_location import LocationHelpScreen


class WelcomeScreen(QWidget):
    def get_license_plate_label(self):
        license_plate_label = QLabel(f"Witaj, {self.license_plate}!")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))

        return license_plate_label

    @staticmethod
    def get_vehicle_type_text(class_name: str) -> str:
        vehicle_type_text = None

        if class_name == 'car':
            vehicle_type_text = 'Samochód'
        elif class_name == 'truck':
            vehicle_type_text = 'Ciężarówka'
        elif class_name == 'motorcycle':
            vehicle_type_text = 'Motocykl'

        return vehicle_type_text

    @staticmethod
    def get_sector_text(class_name: str) -> str:
        sector_text = None

        if class_name == 'car':
            sector_text = 'A'
        elif class_name == 'truck':
            sector_text = 'B'
        elif class_name == 'motorcycle':
            sector_text = 'C'

        return sector_text

    def get_vehicle_type_layout(self):
        vehicle_type_label = QLabel()
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setFont(QFont("Arial", 65, QFont.Bold))
        vehicle_type_label.setText(self.get_vehicle_type_text(self.vehicle_class))
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon(f'gui/resources/images/{self.vehicle_class}_2.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(250, 250))
        vehicle_icon_label.setAlignment(Qt.AlignCenter)
        vehicle_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        vehicle_type_layout = QHBoxLayout()
        vehicle_type_layout.addWidget(vehicle_icon_label)
        vehicle_type_layout.addWidget(vehicle_type_label)
        vehicle_type_layout.setAlignment(Qt.AlignCenter)
        vehicle_type_layout.setContentsMargins(0, 0, 0, 0)

        return vehicle_type_layout

    def get_parking_sector_layout(self):
        location_label = QLabel()
        location_label.setAlignment(Qt.AlignCenter)
        location_label.setFont(QFont("Arial", 45, QFont.Bold))
        location_label.setText(f"Miejsce do parkowania: Sektor {self.sector_name}")
        location_label.setContentsMargins(20, 20, 20, 20)

        location_original_icon = QIcon('gui/resources/images/location.png')
        location_icon_label = QLabel()
        location_icon_label.setPixmap(location_original_icon.pixmap(100, 100))
        location_icon_label.setAlignment(Qt.AlignCenter)
        location_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        location_layout = QHBoxLayout()
        location_layout.addWidget(location_icon_label)
        location_layout.addWidget(location_label)
        location_layout.setAlignment(Qt.AlignCenter)
        location_layout.setContentsMargins(0, 0, 0, 0)

        return location_layout

    def get_horizontal_button(self, text: str, icon_path: str):
        original_icon = QIcon(icon_path)
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(65, 65))
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        icon_label.setContentsMargins(5, 5, 5, 5)

        text_label = QLabel()
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        text_label.setFont(QFont("Arial", 30, QFont.Bold))
        text_label.setText(text)
        text_label.setContentsMargins(5, 5, 5, 5)

        button_layout = QHBoxLayout()
        button_layout.addWidget(icon_label)
        button_layout.addWidget(text_label)
        button_layout.setAlignment(Qt.AlignCenter)

        button = QPushButton()
        button.setStyleSheet(
            "background-color: black; color: white; border-radius: 20px;"
        )
        button.setLayout(button_layout)
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        return button

    def show_sector_location_help(self):
        location_help_screen = LocationHelpScreen(2, parent=self)

        self.parent().addWidget(location_help_screen)
        self.parent().setCurrentIndex(self.parent().currentIndex() + 1)

    def __init__(self, parent, vehicle_class: str,
                 license_plate: str, sector_name: str):
        super().__init__(parent)
        self.setWindowTitle("WJAZD")

        self.vehicle_class: str = vehicle_class
        self.license_plate: str = license_plate
        self.sector_name: str = sector_name

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
        license_plate_label = self.get_license_plate_label()
        main_layout.addWidget(license_plate_label, 0, 0, 1, 16)

        ## -- TYP POJAZDU
        vehicle_type_layout = self.get_vehicle_type_layout()
        main_layout.addLayout(vehicle_type_layout, 1, 5, 1, 6)

        ## -- MIEJSCE PARKINGU
        parking_sector_layout = self.get_parking_sector_layout()
        main_layout.addLayout(parking_sector_layout, 2, 4, 1, 8)

        ## -- PRZYCISK "POKAŻ SCHEMAT"
        show_location_button = self.get_horizontal_button(
            "Pokaż miejsce na schemacie",
            'gui/resources/images/location_help.png'
        )
        show_location_button.clicked.connect(self.show_sector_location_help)
        main_layout.addWidget(show_location_button, 5, 5, 2, 6)

        self.setLayout(main_layout)
