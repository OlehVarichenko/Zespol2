from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class ExitScreen(QWidget):
    def init_ui(self):
        pass

    def get_license_plate_label(self):
        license_plate_label = QLabel(f"{self.license_plate}: opłaty")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))

        return license_plate_label

    def get_vehicle_type_text(self, class_name: str) -> str:
        vehicle_type_text = None

        if class_name == 'car':
            vehicle_type_text = 'Samochód'
        elif class_name == 'truck':
            vehicle_type_text = 'Ciężarówka'
        elif class_name == 'motorcycle':
            vehicle_type_text = 'Motocykl'

        return vehicle_type_text

    def get_vehicle_type_layout(self):
        vehicle_type_label = QLabel()
        # vehicle_type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        vehicle_type_label.setAlignment(Qt.AlignCenter)
        vehicle_type_label.setFont(QFont("Arial", 50, QFont.Bold))
        vehicle_type_label.setText('Taryfa: 2zł/s')
        vehicle_type_label.setContentsMargins(20, 20, 20, 20)

        vehicle_original_icon = QIcon(f'gui/resources/images/{self.vehicle_type}_2.png')
        vehicle_icon_label = QLabel()
        vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(120, 120))
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
        location_label.setFont(QFont("Arial", 50, QFont.Bold))
        location_label.setText("Czas postoju: 19 min")
        location_label.setContentsMargins(20, 20, 20, 20)

        location_original_icon = QIcon('gui/resources/images/clock.png')
        location_icon_label = QLabel()
        location_icon_label.setPixmap(location_original_icon.pixmap(120, 120))
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

    def get_total_layout(self):
        location_label = QLabel()
        # location_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        location_label.setAlignment(Qt.AlignCenter)
        location_label.setFont(QFont("Arial", 50, QFont.Bold))
        location_label.setText("Do zapłaty: 122 zł")
        location_label.setContentsMargins(20, 20, 20, 20)

        location_original_icon = QIcon('gui/resources/images/wallet.png')
        location_icon_label = QLabel()
        location_icon_label.setPixmap(location_original_icon.pixmap(120, 120))
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

    def __init__(self, parent, license_plate: str = 'SC 12345', vehicle_type: str = 'car'):
        super().__init__(parent)
        self.setWindowTitle("WYJAZD")

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
        main_layout.addLayout(vehicle_type_layout, 1, 6, 1, 4)

        ## -- MIEJSCE PARKINGU
        parking_sector_layout = self.get_parking_sector_layout()
        main_layout.addLayout(parking_sector_layout, 2, 5, 1, 6)

        ## -- MIEJSCE PARKINGU 2
        parking_sector_layout_2 = self.get_total_layout()
        main_layout.addLayout(parking_sector_layout_2, 3, 5, 1, 6)

        ## -- PRZYCISK "POKAŻ MAPĘ"

        map_original_icon = QIcon('gui/resources/images/blik.png')
        show_location_icon = QLabel()
        show_location_icon.setPixmap(map_original_icon.pixmap(75, 75))
        show_location_icon.setAlignment(Qt.AlignCenter)
        show_location_icon.setContentsMargins(5, 5, 5, 5)

        show_location_label = QLabel()
        show_location_label.setAlignment(Qt.AlignCenter)
        show_location_label.setFont(QFont("Arial", 30, QFont.Bold))
        show_location_label.setText("Zapłać\nBLIKiem")
        show_location_label.setContentsMargins(5, 5, 5, 5)

        show_location_button_layout = QVBoxLayout()
        show_location_button_layout.addWidget(show_location_icon)
        show_location_button_layout.addWidget(show_location_label)
        show_location_button_layout.setAlignment(Qt.AlignCenter)

        show_location_button = QPushButton()
        show_location_button.setStyleSheet(
            "background-color: black; color: white; border-radius: 20px;"
        )
        show_location_button.setLayout(show_location_button_layout)
        show_location_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(show_location_button, 5, 1, 3, 4)

        ### PRZYCISK 2

        ## -- PRZYCISK "POKAŻ MAPĘ"

        map_original_icon = QIcon('gui/resources/images/credit_card.png')
        show_location_icon = QLabel()
        show_location_icon.setPixmap(map_original_icon.pixmap(75, 75))
        show_location_icon.setAlignment(Qt.AlignCenter)
        show_location_icon.setContentsMargins(5, 5, 5, 5)

        show_location_label = QLabel()
        show_location_label.setAlignment(Qt.AlignCenter)
        show_location_label.setFont(QFont("Arial", 30, QFont.Bold))
        show_location_label.setText("Zapłać\nkartą")
        show_location_label.setContentsMargins(5, 5, 5, 5)

        show_location_button_layout = QVBoxLayout()
        show_location_button_layout.addWidget(show_location_icon)
        show_location_button_layout.addWidget(show_location_label)
        show_location_button_layout.setAlignment(Qt.AlignCenter)

        show_location_button = QPushButton()
        show_location_button.setStyleSheet(
            "background-color: black; color: white; border-radius: 20px;"
        )
        show_location_button.setLayout(show_location_button_layout)
        show_location_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(show_location_button, 5, 6, 3, 4)


        # PRZYCISK 3
        ## -- PRZYCISK "POKAŻ MAPĘ"

        map_original_icon = QIcon('gui/resources/images/coupon.png')
        show_location_icon = QLabel()
        show_location_icon.setPixmap(map_original_icon.pixmap(75, 75))
        show_location_icon.setAlignment(Qt.AlignCenter)
        show_location_icon.setContentsMargins(5, 5, 5, 5)

        show_location_label = QLabel()
        show_location_label.setAlignment(Qt.AlignCenter)
        show_location_label.setFont(QFont("Arial", 30, QFont.Bold))
        show_location_label.setText("Zapłać\nkuponem")
        show_location_label.setContentsMargins(5, 5, 5, 5)

        show_location_button_layout = QVBoxLayout()
        show_location_button_layout.addWidget(show_location_icon)
        show_location_button_layout.addWidget(show_location_label)
        show_location_button_layout.setAlignment(Qt.AlignCenter)

        show_location_button = QPushButton()
        show_location_button.setStyleSheet(
            "background-color: black; color: white; border-radius: 20px;"
        )
        show_location_button.setLayout(show_location_button_layout)
        show_location_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(show_location_button, 5, 11, 3, 4)

        self.setLayout(main_layout)
