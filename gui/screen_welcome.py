from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class WelcomeScreen(QWidget):
    def init_ui(self):
        pass

    def get_license_plate_label(self):
        license_plate_label = QLabel(f"Witaj, {self.license_plate}!")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))

        return license_plate_label

    def get_vehicle_type_layout(self):
        vehicle_type_label = QLabel()
        # vehicle_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setFont(QFont("Arial", 65, QFont.Bold))
        vehicle_type_label.setText('Ciężarówka')
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon(f'gui/resources/images/{self.vehicle_type}.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(250, 250))
        # vehicle_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
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
        # location_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        location_label.setAlignment(Qt.AlignCenter)
        location_label.setFont(QFont("Arial", 45, QFont.Bold))
        location_label.setText("Miejsce do parkowania: Sektor C")
        location_label.setContentsMargins(20, 20, 20, 20)

        location_original_icon = QIcon('gui/resources/images/location.png')
        location_icon_label = QLabel()
        location_icon_label.setPixmap(location_original_icon.pixmap(100, 100))
        # location_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        location_icon_label.setAlignment(Qt.AlignCenter)
        location_icon_label.setContentsMargins(20, 20, 20, 20)

        # Create a horizontal layout for the icon and text
        location_layout = QHBoxLayout()
        location_layout.addWidget(location_icon_label)
        location_layout.addWidget(location_label)
        location_layout.setAlignment(Qt.AlignCenter)
        location_layout.setContentsMargins(0, 0, 0, 0)

        return location_layout

    def __init__(self, vehicle_type: str = 'car', license_plate: str = 'SC 12345'):
        super().__init__()
        self.setWindowTitle("WJAZD")

        self.vehicle_type: str = vehicle_type
        self.license_plate: str = license_plate

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

        ## -- PRZYCISK "POKAŻ MAPĘ"

        map_original_icon = QIcon('gui/resources/images/location_help.png')
        show_location_icon = QLabel()
        show_location_icon.setPixmap(map_original_icon.pixmap(50, 50))
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
            "background-color: black; color: white; border-radius: 20px;"
        )
        show_location_button.setLayout(show_location_button_layout)
        show_location_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(show_location_button, 5, 5, 1, 6)

        self.setLayout(main_layout)