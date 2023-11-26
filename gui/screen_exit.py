from decimal import Decimal
from math import floor

from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from gui.screen_message import Messages


class ExitScreen(QWidget):
    @staticmethod
    def generate_button(text: str, img_path: str):
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
    def get_icon_n_text_layout(text: str, text_size: int, icon_path: str, icon_size: int):
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

        # Create a horizontal layout for the icon and text
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(icon_label)
        horizontal_layout.addWidget(text_label)
        horizontal_layout.setAlignment(Qt.AlignCenter)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        return horizontal_layout

    def get_license_plate_label(self):
        license_plate_label = QLabel(f"{self.license_plate}: opłaty")
        license_plate_label.setAlignment(Qt.AlignCenter)
        license_plate_label.setStyleSheet("background-color: white; color: black;")
        license_plate_label.setFont(QFont("Arial", 75, QFont.Bold))

        return license_plate_label

    def get_vehicle_tariff_layout(self):
        icon_path = f'gui/resources/images/{self.vehicle_type}.png'
        return self.get_icon_n_text_layout(
            f'Taryfa: {round(self.tariff, 2)} zł/h', 50, icon_path,120
        )

    def get_parking_time_layout(self):
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
            parking_time_string += f' {floor(minutes)} minuta'
        elif 2 <= minutes % 10 <= 4 and not 12 <= minutes <= 14:
            parking_time_string += f' {floor(minutes)} minuty'
        elif minutes >= 5:
            parking_time_string += f' {floor(minutes)} minut'

        return self.get_icon_n_text_layout(
            f'Czas postoju: {parking_time_string}', 50, icon_path, 120
        )

    def get_total_layout(self):
        icon_path = f'gui/resources/images/wallet.png'
        return self.get_icon_n_text_layout(
            f'Do zapłaty: {self.total} zł', 50, icon_path, 120
        )

    def on_voucher_button_click(self):
        self.parent().parent().db_communicator.finish_stay(self.stay_id,
                                                           self.parking_time, self.total)
        self.parent().parent().open_message_screen(Messages.PAYMENT_SUCCESSFUL)

    def __init__(self, parent, stay_id: int, vehicle_type: str,
                 license_plate: str, tariff: Decimal, stay_duration: int):
        super().__init__(parent)
        self.setWindowTitle("WYJAZD")

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

        white_fullscreen_label = QLabel()
        white_fullscreen_label.setStyleSheet("background-color: white;")
        main_layout.addWidget(white_fullscreen_label, 1, 0, 8, 16)

        ## -- NR REJESTRACYJNY
        license_plate_label = self.get_license_plate_label()
        main_layout.addWidget(license_plate_label, 0, 0, 1, 16)

        ## -- TARYFA DLA TYPU POJAZDU
        vehicle_type_layout = self.get_vehicle_tariff_layout()
        main_layout.addLayout(vehicle_type_layout, 1, 6, 1, 4)

        ## -- CZAS POSTOJU
        parking_sector_layout = self.get_parking_time_layout()
        main_layout.addLayout(parking_sector_layout, 2, 5, 1, 6)

        ## -- PODSUMOWANIE
        total_sum_layout = self.get_total_layout()
        main_layout.addLayout(total_sum_layout, 3, 5, 1, 6)

        ## -- PRZYCISK BLIK
        blik_button = self.generate_button(
            "Zapłać\nBLIKiem", 'gui/resources/images/blik.png'
        )
        main_layout.addWidget(blik_button, 5, 1, 3, 4)

        ### PRZYCISK KARTA
        card_button = self.generate_button(
            "Zapłać\nkartą", 'gui/resources/images/credit_card.png'
        )
        main_layout.addWidget(card_button, 5, 6, 3, 4)

        # PRZYCISK KOD
        voucher_button = self.generate_button(
            "Zapłać\nkodem", 'gui/resources/images/coupon.png'
        )
        voucher_button.clicked.connect(self.on_voucher_button_click)
        main_layout.addWidget(voucher_button, 5, 11, 3, 4)

        self.setLayout(main_layout)
