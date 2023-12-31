from PyQt5.QtWidgets import QWidget, QGridLayout, \
    QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class LocationHelpScreen(QWidget):
    def __init__(self, highlight_sector_name: str, parent=None):
        """
        Funkcja przyjmuje nazwę sektoru do podświetlenia na schemacie,
        a także opcjonalnie widżet rodzicielski całego ekranu.

        Args:
            highlight_sector_name(str): Nazwa sektoru do podświetlenia na schemacie
            parent:
        """
        super().__init__(parent)
        self.highlight_sector_name: str = highlight_sector_name
        self.sectors_data = self.parent().parent().parent().db_communicator.get_sectors_data()
        self.init_ui()

    @staticmethod
    def generate_button(text: str, img_path: str) -> QPushButton:
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
        icon_label.setPixmap(original_icon.pixmap(125, 125))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setContentsMargins(5, 5, 5, 5)

        text_label = QLabel()
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", 50, QFont.Bold))
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

    def close_screen(self) -> None:
        """
        Funkcja zamyka wszystkie ekrany/komunikaty i dzięki temu wraca do ekranu głównego
        odtwarzającego video z kamerki.

        Returns:
            None
        """
        curr_index = self.parent().currentIndex()
        self.parent().setCurrentIndex(curr_index - 1)
        self.parent().removeWidget(self)
        self.setParent(None)

    def init_ui(self) -> None:
        """
        Funkcja zajmuje się dodaniem wszystkich elementów do ekranu.
        Głównymi elementami są przycisk powrotu oraz schemat w postaci
        QGridLayoutu ilustrujący położenie sektorów parkingu.

        Returns:
            None

        """
        main_layout = QGridLayout()

        white_fullscreen_label = QLabel()
        white_fullscreen_label.setStyleSheet("background-color: white;")
        main_layout.addWidget(white_fullscreen_label, 0, 0, 9, 16)

        self.setLayout(main_layout)

        parking_scheme_layout = QGridLayout(self)
        parking_scheme_layout.addWidget(white_fullscreen_label, 0, 0, 900, 1200)
        parking_scheme_layout.setContentsMargins(10, 10, 10, 10)

        for sector in self.sectors_data:
            sector_widget = QWidget()
            sector_layout = QVBoxLayout(sector_widget)
            sector_layout.setAlignment(Qt.AlignCenter)

            vehicle_original_icon = QIcon(f'resources/images/{sector.vehicle_type_name}.png')
            vehicle_icon_label = QLabel()
            vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(120, 120))
            vehicle_icon_label.setAlignment(Qt.AlignCenter)
            vehicle_icon_label.setContentsMargins(5, 5, 5, 5)
            vehicle_icon_label.setStyleSheet("border-width: 0px;")

            sector_name_label = QLabel(f"Sektor {sector.name}")
            sector_name_label.setFont(QFont("Arial", 40, QFont.Bold))
            sector_name_label.setAlignment(Qt.AlignCenter)
            sector_name_label.setStyleSheet("border-width: 0px;")

            sector_layout.addWidget(vehicle_icon_label)
            sector_layout.addWidget(sector_name_label)

            sector_widget.setStyleSheet("border: 5px solid black;")

            if sector.name.lower() == self.highlight_sector_name.lower():
                sector_widget.setStyleSheet("border: 5px solid black;background-color: yellow;")

            parking_scheme_layout.addWidget(
                sector_widget,
                sector.row, sector.col,
                sector.row_span, sector.col_span
            )

        parking_scheme_widget = QWidget(self)
        parking_scheme_widget.setLayout(parking_scheme_layout)
        main_layout.addWidget(parking_scheme_widget, 0, 4, 9, 12)

        back_button = self.generate_button('Powrót', 'resources/images/back.png')
        back_button.clicked.connect(self.close_screen)
        main_layout.addWidget(back_button, 3, 0, 3, 4)
