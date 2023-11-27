from typing import Dict, Tuple
from enum import IntEnum

from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class Messages(IntEnum):
    DETECTION_ERROR = -2
    GENERAL_ERROR = -1
    NO_FREE_PARKING_LOTS = 1
    NO_FREE_PARKING_LOTS_SOME_TYPE = 2
    PAYMENT_SUCCESSFUL = 3
    PAYMENT_UNSUCCESSFUL = 4


messages_dict: Dict[IntEnum, Tuple[str, str]] = {
    Messages.GENERAL_ERROR: ("WYSTĄPIŁ BŁĄD SYSTEMU\nPROSIMY O ZWRÓCENIE SIĘ DO OBSŁUGI",
                             "gui/resources/images/error.png"),
    Messages.DETECTION_ERROR: ("WYSTĄPIŁ BŁĄD DETEKCJI\nPROSIMY O ZWRÓCENIE SIĘ DO OBSŁUGI",
                               "gui/resources/images/error.png"),
    Messages.NO_FREE_PARKING_LOTS: ("BRAK\nMIEJSC\nPARKINGOWYCH",
                                    "gui/resources/images/no_entry.png"),
    Messages.NO_FREE_PARKING_LOTS_SOME_TYPE: ("BRAK MIEJSC PARKINGOWYCH\nDLA DANEGO TYPU POJAZDU",
                                              "gui/resources/images/no_entry.png"),
    Messages.PAYMENT_SUCCESSFUL: ("PŁATNOŚĆ DOKONANA POMYŚLNIE\n\nMIŁEGO DNIA!",
                                  "gui/resources/images/ok.png"),
    Messages.PAYMENT_UNSUCCESSFUL: ("WYSTĄPIŁ PROBLEM Z PŁATNOŚCIĄ\n\nPROSIMY SPRÓBOWAĆ PONOWNIE",
                                    "gui/resources/images/error.png")
}


class MessageScreen(QWidget):
    @staticmethod
    def get_message_layout(text: str,
                           icon_path: str,
                           text_size: int,
                           icon_size: int):
        original_icon = QIcon(icon_path)
        icon_label = QLabel()
        icon_label.setPixmap(original_icon.pixmap(icon_size, icon_size))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(20, 20, 20, 20)

        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", text_size, QFont.Bold))
        text_label.setText(text)
        text_label.setStyleSheet("color: white;")
        text_label.setContentsMargins(20, 20, 20, 20)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(icon_label)
        vertical_layout.addWidget(text_label)
        vertical_layout.setAlignment(Qt.AlignCenter)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        return vertical_layout

    def __init__(self, parent, message_code: int,
                 text_size: int = 55, icon_size: int = 470):
        super().__init__(parent)
        self.setWindowTitle("WJAZD")

        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        black_fullscreen_label = QLabel()
        black_fullscreen_label.setStyleSheet("background-color: black;")
        main_layout.addWidget(black_fullscreen_label, 0, 0, 9, 16)

        ## -- KOMUNIKAT
        message_attribs = messages_dict[Messages(message_code)]
        vehicle_type_layout = self.get_message_layout(
            message_attribs[0],
            message_attribs[1],
            text_size if len(message_attribs) < 3 else message_attribs[2],
            icon_size if len(message_attribs) < 4 else message_attribs[3],
        )
        main_layout.addLayout(vehicle_type_layout, 2, 3, 5, 10)

        self.setLayout(main_layout)
