from decimal import Decimal
from math import floor

import psycopg2
from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from gui.screen_message import Messages


class ExitScreen(QWidget):
    @staticmethod
    def generate_button(text: str, img_path: str):
        """
            Funkcja generuje przycisk z odpowiednim obrazkiem na górze i tekstem na dole.

            Args:
                text(str): Tekst przycisku
                img_path(str): Ścieżka pliku obrazku

            Returns:
                QPushButton

        """
        original_icon = QIcon(img_path)
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(75, 75))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(5, 5, 5, 5)

        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", 30, QFont.Bold))
        text_label.setText(text)
        text_label.setContentsMargins(5, 5, 5, 5)

        button_layout = QVBoxLayout()
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

    def get_license_plate_label(self) -> QLabel:
        """
        Funkcja zwraza QLabel z numerem rejestracyjnym pojazdu

        Returns:
            QLabel

        """
        license_plate_label = QLabel(f"{self.license_plate}: opłaty")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))

        return license_plate_label

    def get_vehicle_tariff_layout(self) -> QHBoxLayout:
        """
        Funkcja zwraca poziomy układ z obrazkiem pokazującym typ pojazdu po lewej stronie
        oraz tekst z odpowiednią taryfą za godzinę po prawej stronie

        Returns:
            QHBoxLayout

        """
        icon_path = f'gui/resources/images/{self.vehicle_type}.png'
        return self.get_icon_n_text_layout(
            f'Taryfa: {round(self.tariff, 2)} zł/h', 50, icon_path,120
        )

    def get_parking_time_layout(self) -> QHBoxLayout:
        """
        Funkcja zwraza poziomy układ z ilustrującym obrazkiem + czasem postoju pojazdu

        Returns:
            QHBoxLayout

        """
        icon_path = f'gui/resources/images/clock.png'
        parking_time_string = ''

        days = floor(self.parking_time / 60 / 60 / 24)
        if days == 1:
            parking_time_string += f'{days} dzień '
        elif days >= 2:
            parking_time_string += f'{days} dni '

        hours = floor(self.parking_time / 60 / 60 - days * 24)
        if hours == 1:
            parking_time_string += f'{hours} godzina '
        elif 2 <= hours % 10 <= 4 and not 12 <= hours <= 14:
            parking_time_string += f'{hours} godziny '
        elif hours >= 5:
            parking_time_string += f'{hours} godzin '

        minutes = floor(self.parking_time / 60 - hours * 60 - days * 24 * 60)
        if minutes == 1:
            parking_time_string += f'{floor(minutes)} minuta'
        elif 2 <= minutes % 10 <= 4 and not 12 <= minutes <= 14:
            parking_time_string += f'{floor(minutes)} minuty'
        elif minutes >= 5:
            parking_time_string += f'{floor(minutes)} minut'
        elif days == 0 and hours == 0 and minutes == 0:
            seconds = self.parking_time
            if seconds == 1:
                parking_time_string += f'{seconds} sekunda'
            elif 2 <= seconds % 10 <= 4 and not 12 <= seconds <= 14:
                parking_time_string += f'{seconds} sekundy'
            elif seconds >= 5:
                parking_time_string += f'{seconds} sekund'

        return self.get_icon_n_text_layout(
            f'Czas postoju: {parking_time_string}', 50, icon_path, 120
        )

    def get_total_layout(self) -> QHBoxLayout:
        """
        Funkcja zwraca poziomy układ z ilustrującym obrazkiem + łączną kwotą do zapłaty

        Returns:
            QHBoxLayout

        """
        icon_path = f'gui/resources/images/wallet.png'
        return self.get_icon_n_text_layout(
            f'Do zapłaty: {self.total} zł', 50, icon_path, 120
        )

    def on_voucher_button_click(self) -> None:
        """
        Funkcja podpina się pod przycisk przejazdu testowego i imituje pomyślne dokonanie płatności

        Returns:
            None

        """
        try:
            self.parent().parent().db_communicator.finish_stay(self.stay_id,
                                                               self.parking_time, self.total)
            self.parent().parent().open_message_screen(Messages.PAYMENT_SUCCESSFUL)
        except psycopg2.Error:
            self.parent().parent().open_message_screen(Messages.PAYMENT_UNSUCCESSFUL)

    def __init__(self, parent, stay_id: int, vehicle_type: str,
                 license_plate: str, tariff: Decimal, stay_duration: int):
        """
        Funkcja przyjmuje niezbędne wartości do funkcjonowania tego widżetu
        oraz dodaje elementy do wyświetlenia na widżecie

        Args:
            parent: Obiekt rodzicielski
            stay_id(int): ID postoju
            vehicle_type(str): Typ pojazdu
            license_plate(str): Numer rejestracyjny
            tariff(Decimal): Taryfa za godzinę
            stay_duration(int): Czas postoju w sekundach
        """
        super().__init__(parent)

        self.vehicle_type: str = vehicle_type
        self.license_plate: str = license_plate
        self.stay_id = stay_id

        self.tariff: Decimal = tariff
        self.parking_time: int = stay_duration

        self.total = round(self.tariff * self.parking_time / 60 / 60, 2)

        # dodanie czarnego tła dla spacingu
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

        ## -- TARYFA DLA TYPU POJAZDU
        vehicle_type_layout = self.get_vehicle_tariff_layout()
        data_layout.addLayout(vehicle_type_layout)

        ## -- CZAS POSTOJU
        parking_sector_layout = self.get_parking_time_layout()
        data_layout.addLayout(parking_sector_layout)

        ## -- PODSUMOWANIE
        total_sum_layout = self.get_total_layout()
        data_layout.addLayout(total_sum_layout)

        buttons_layout = QHBoxLayout(data_widget)

        ## -- PRZYCISK BLIK
        blik_button = self.generate_button(
            "Zapłać\nBLIKiem", 'gui/resources/images/blik.png'
        )
        buttons_layout.addWidget(blik_button)

        ## -- PRZYCISK KARTA
        card_button = self.generate_button(
            "Zapłać\nkartą", 'gui/resources/images/credit_card.png'
        )
        buttons_layout.addWidget(card_button)

        ## -- PRZYCISK KOD
        test_ride_button = self.generate_button(
            "Testowy\nprzejazd", 'gui/resources/images/coupon.png'
        )
        test_ride_button.clicked.connect(self.on_voucher_button_click)
        buttons_layout.addWidget(test_ride_button)

        data_layout.addLayout(buttons_layout)

        data_widget.setLayout(data_layout)
        data_widget.setSizePolicy(QSizePolicy.MinimumExpanding,
                                  QSizePolicy.MinimumExpanding)
        data_widget.setStyleSheet("background-color: white;")
        main_layout.addWidget(data_widget, 1, 0, 8, 16)

        self.setLayout(main_layout)
