from typing import Dict, Tuple
from enum import IntEnum

from PyQt5.QtWidgets import QWidget, \
    QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class Messages(IntEnum):
    """
    Klasa zawiera kody błędów, dla których utworzono słownik z komunikatami i obrazkami.
    Dziedziczenie po IntEnum pozwala na tworzenie obiektu enum po przekazanym numerze.
    """
    DETECTION_ERROR = -2
    GENERAL_ERROR = -1
    NO_FREE_PARKING_LOTS = 1
    NO_FREE_PARKING_LOTS_SOME_TYPE = 2
    PAYMENT_SUCCESSFUL = 3
    PAYMENT_UNSUCCESSFUL = 4


class MessageScreen(QWidget):
    """
    Klasa przedstawia sobą definicję widżetu z komunikatem
    (zawiera odpowiednie dane oraz funkcje do generowania widżetu).
    """

    messages_dict: Dict[IntEnum, Tuple[str, str]] = {
        Messages.GENERAL_ERROR: ("WYSTĄPIŁ BŁĄD SYSTEMU\nPROSIMY O ZWRÓCENIE SIĘ DO OBSŁUGI",
                                 "resources/images/error.png"),
        Messages.DETECTION_ERROR: ("WYSTĄPIŁ BŁĄD DETEKCJI\nPROSIMY O ZWRÓCENIE SIĘ DO OBSŁUGI",
                                   "resources/images/error.png"),
        Messages.NO_FREE_PARKING_LOTS: ("BRAK MIEJSC PARKINGOWYCH",
                                        "resources/images/no_entry.png"),
        Messages.NO_FREE_PARKING_LOTS_SOME_TYPE: ("BRAK MIEJSC PARKINGOWYCH\nDLA DANEGO TYPU POJAZDU",
                                                  "resources/images/no_entry.png"),
        Messages.PAYMENT_SUCCESSFUL: ("PŁATNOŚĆ DOKONANA POMYŚLNIE\nMIŁEGO DNIA!",
                                      "resources/images/ok.png"),
        Messages.PAYMENT_UNSUCCESSFUL: ("WYSTĄPIŁ PROBLEM Z PŁATNOŚCIĄ\nPROSIMY SPRÓBOWAĆ PONOWNIE",
                                        "resources/images/error.png")
    }

    @staticmethod
    def get_message_layout(text: str,
                           icon_path: str,
                           text_size: int,
                           icon_size: int) -> QVBoxLayout:
        """
        Funkcja zwraca pionowy układ z obrazkiem na górze + komunikatem na dole

        Args:
            text(str): Tekst komunikatu
            icon_path(str): Ścieżka z plikiem obrazku
            text_size(int): Rozmiar czcionki
            icon_size(int): Rozmiar obrazku

        Returns:
            QVBoxLayout

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
        """
        Funkcja inicjalizuje widżet z komunikatem.

        Args:
            parent: Widżet rodzicielski
            message_code(int): Kod powiadomienia do wyboru komunikatu ze słownika
            text_size(Optional[int]): Rozmiar czcionki
            icon_size(Optional[int]): Rozmiar obrazku
        """
        super().__init__(parent)
        self.setWindowTitle("WJAZD")

        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        black_fullscreen_label = QLabel()
        black_fullscreen_label.setStyleSheet("background-color: black;")
        main_layout.addWidget(black_fullscreen_label, 0, 0, 9, 16)

        ## -- KOMUNIKAT
        message_attribs = self.messages_dict[Messages(message_code)]
        vehicle_type_layout = self.get_message_layout(
            message_attribs[0],
            message_attribs[1],
            text_size if len(message_attribs) < 3 else message_attribs[2],
            icon_size if len(message_attribs) < 4 else message_attribs[3],
        )
        main_layout.addLayout(vehicle_type_layout, 2, 3, 5, 10)

        self.setLayout(main_layout)
