from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from gui.screen_location import LocationHelpScreen


class WelcomeScreen(QWidget):
    """
    Klasa przedstawia sobą definicję widżetu z ekranem powitalnym,
    który pokazuje wykryty nr rejestracyny, typ pojazdu oraz daje
    możliwość zapoznania się ze schematem parkingu.

    Zawiera odpowiednie funkcje do generowania widżetu.
    """
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
    def get_icon_n_text_layout(text: str, text_size: int, icon_path: str, icon_size: int) -> QHBoxLayout:
        """
        Funkcja zwraca poziomy układ z obrazkiem po lewej stronie i tekstem po prawej

        Args:
            text(str): Tekst
            text_size(int): Rozmiar tekstu
            icon_path(str): Ścieżka z plikiem obrazku
            icon_size(int): Rozmiar wszystkich stron obrazku

        Returns:
            QHBoxLayout

        """
        original_icon = QIcon(icon_path)
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(icon_size, icon_size))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(20, 20, 20, 20)

        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", text_size, QFont.Bold))
        text_label.setText(text)
        text_label.setContentsMargins(20, 20, 20, 20)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(icon_label)
        horizontal_layout.addWidget(text_label)
        horizontal_layout.setAlignment(Qt.AlignCenter)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        return horizontal_layout

    def get_vehicle_type_layout(self) -> QHBoxLayout:
        """
            Funkcja zwraca poziomy układ z obrazkiem pokazującym typ pojazdu po lewej stronie
            oraz odpowiednim tekstem po prawej stronie.

            Returns:
                QHBoxLayout

        """
        vehicle_type = self.get_vehicle_type_text(self.vehicle_class)
        icon_path = f'resources/images/{self.vehicle_class}.png'
        return self.get_icon_n_text_layout(
            vehicle_type, 65, icon_path, 200
        )

    def get_parking_sector_layout(self) -> QHBoxLayout:
        """
        Funkcja zwraca poziomy układ z obrazkiem ilustrującym po lewej stronie
        oraz tekstem z nazwą sektora po prawej stronie.

        Returns:
            QHBoxLayout

        """
        text = f"Miejsce do parkowania: Sektor {self.sector_name}"
        icon_path = f'resources/images/location.png'
        return self.get_icon_n_text_layout(
            text, 45, icon_path, 150
        )

    @staticmethod
    def generate_horizontal_button(text: str, img_path: str) -> QPushButton:
        """
            Funkcja generuje przycisk z odpowiednim obrazkiem po lewej stronie i tekstem po prawej.

            Args:
                text(str): Tekst przycisku
                img_path(str): Ścieżka pliku obrazku

            Returns:
                QPushButton

        """
        original_icon = QIcon(img_path)
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(100, 100))
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        icon_label.setContentsMargins(5, 5, 5, 5)

        text_label = QLabel()
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        text_label.setFont(QFont("Arial", 35, QFont.Bold))
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

    def show_sector_location_help(self) -> None:
        """
        Pokazuje (dodaje na góre głownego stosu widżetów i aktywuje) widżet ze schematem parkingu.

        Returns:
            None

        """
        location_help_screen = LocationHelpScreen(self.sector_name, parent=self)

        self.parent().addWidget(location_help_screen)
        self.parent().setCurrentIndex(self.parent().currentIndex() + 1)

    def __init__(self, parent, vehicle_class: str,
                 license_plate: str, sector_name: str):
        """
        Funckja inizcalizuje ekran powitalny za pomocą wartości
        uzyskanych od modelu YOLOv7.

        Args:
            parent: Widżet rodzicielski
            vehicle_class(str): Klasa pojazdu YOLOv7 (car/motorcycle/truck)
            license_plate(str): Numer rejestracyjny
            sector_name(str): Pobrana z bazy danych nazwa sektoru do parkowania pojazdu
        """
        super().__init__(parent)

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

        data_widget = QWidget()
        data_layout = QVBoxLayout(data_widget)

        ## -- NR REJESTRACYJNY
        license_plate_label = self.get_license_plate_label()
        main_layout.addWidget(license_plate_label, 0, 0, 1, 16)

        ## -- TYP POJAZDU
        vehicle_type_layout = self.get_vehicle_type_layout()
        data_layout.addLayout(vehicle_type_layout)

        ## -- MIEJSCE PARKINGU
        parking_sector_layout = self.get_parking_sector_layout()
        data_layout.addLayout(parking_sector_layout)

        ## -- PRZYCISK "POKAŻ SCHEMAT"
        show_location_button = self.generate_horizontal_button(
            "Pokaż miejsce na schemacie",
            'resources/images/location_help.png'
        )
        show_location_button.clicked.connect(self.show_sector_location_help)
        data_layout.addWidget(show_location_button)

        data_widget.setLayout(data_layout)
        data_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        data_widget.setStyleSheet("background-color: white;")
        main_layout.addWidget(data_widget, 1, 0, 8, 16)

        self.setLayout(main_layout)
