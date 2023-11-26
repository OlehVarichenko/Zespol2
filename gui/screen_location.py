from PyQt5.QtWidgets import QWidget, QGridLayout, \
    QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class LocationHelpScreen(QWidget):
    def __init__(self, highlight_sector_id, parent=None):
        super().__init__(parent)
        self.highlight_sector_id = highlight_sector_id
        self.sectors_data = self.parent().parent().parent().db_communicator.get_sectors_data()
        self.init_ui()

    @staticmethod
    def generate_button(text: str, img_path: str):
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

    def close_screen(self):
        curr_index = self.parent().currentIndex()
        self.parent().setCurrentIndex(curr_index - 1)
        self.parent().removeWidget(self)
        self.setParent(None)

    def init_ui(self):
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

            vehicle_original_icon = QIcon(f'gui/resources/images/{sector.vehicle_type_name}.png')
            vehicle_icon_label = QLabel()
            vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(120, 120))
            vehicle_icon_label.setAlignment(Qt.AlignCenter)
            vehicle_icon_label.setContentsMargins(5, 5, 5, 5)
            vehicle_icon_label.setStyleSheet("border-width: 0px;")

            sector_name_label = QLabel(sector.name)
            sector_name_label.setFont(QFont("Arial", 40, QFont.Bold))
            sector_name_label.setStyleSheet("border-width: 0px;")

            sector_layout.addWidget(vehicle_icon_label)
            sector_layout.addWidget(sector_name_label)

            sector_widget.setStyleSheet("border: 5px solid black;")

            if sector.id == self.highlight_sector_id:
                sector_widget.setStyleSheet("border: 5px solid black;background-color: yellow;")

            parking_scheme_layout.addWidget(
                sector_widget,
                sector.row, sector.col,
                sector.row_span, sector.col_span
            )

        parking_scheme_widget = QWidget(self)
        parking_scheme_widget.setLayout(parking_scheme_layout)
        main_layout.addWidget(parking_scheme_widget, 0, 4, 9, 12)

        back_button = self.generate_button('Powrót', 'gui/resources/images/back.png')
        back_button.clicked.connect(self.close_screen)
        main_layout.addWidget(back_button, 3, 0, 3, 4)
