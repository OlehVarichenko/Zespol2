import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QPen, QIcon
from PyQt5.QtCore import Qt

# Assuming you have fetched data using psycopg2 from the 'Sectors' table
# Sample data for demonstration purposes
sectors_data = [
    {'sector_id': 1, 'sector_name': 'Sector A', 'row': 0, 'col': 0, 'row_span': 150, 'column_span': 200},
    {'sector_id': 2, 'sector_name': 'Sector B', 'row': 750, 'col': 900, 'row_span': 150, 'column_span': 300},
    # Add more sector data here...
]


class LocationHelpScreen(QWidget):
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

    def __init__(self, highlight_sector_id, parent=None):
        super().__init__(parent)
        self.highlight_sector_id = highlight_sector_id
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout()

        white_fullscreen_label = QLabel()
        white_fullscreen_label.setStyleSheet("background-color: white;")
        main_layout.addWidget(white_fullscreen_label, 0, 0, 9, 16)

        self.setLayout(main_layout)

        parking_scheme_layout = QGridLayout(self)
        parking_scheme_layout.addWidget(white_fullscreen_label, 0, 0, 900, 1200)
        parking_scheme_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed

        # Add sectors dynamically based on fetched data
        for sector in sectors_data:
            sector_widget = QWidget()
            sector_layout = QVBoxLayout(sector_widget)
            sector_layout.setAlignment(Qt.AlignCenter)

            vehicle_original_icon = QIcon(f'gui/resources/images/car_2.png')
            vehicle_icon_label = QLabel()
            vehicle_icon_label.setPixmap(vehicle_original_icon.pixmap(100, 100))
            vehicle_icon_label.setAlignment(Qt.AlignCenter)
            vehicle_icon_label.setContentsMargins(5, 5, 5, 5)
            vehicle_icon_label.setStyleSheet("border-width: 0px;")

            sector_name_label = QLabel(sector['sector_name'])
            sector_name_label.setFont(QFont("Arial", 30, QFont.Bold))
            sector_name_label.setStyleSheet("border-width: 0px;")

            sector_layout.addWidget(vehicle_icon_label)
            sector_layout.addWidget(sector_name_label)

            sector_widget.setStyleSheet("border: 5px solid black;")

            # Highlight the specified sector
            if sector['sector_id'] == self.highlight_sector_id:
                sector_widget.setStyleSheet("border: 5px solid black;background-color: yellow;")

            parking_scheme_layout.addWidget(sector_widget, sector['row'],
                                            sector['col'], sector['row_span'], sector['column_span'])

        parking_scheme_widget = QWidget(self)
        parking_scheme_widget.setLayout(parking_scheme_layout)
        main_layout.addWidget(parking_scheme_widget, 0, 4, 9, 12)

        # back_button = QPushButton('Back')
        back_button = self.generate_button('Powrót', 'gui/resources/images/back.png')
        # back_button.setStyleSheet("background-color: black; color: white;")
        # back_button.setFont(QFont("Arial", 10, QFont.Bold))
        # back_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        main_layout.addWidget(back_button, 3, 0, 3, 4)  # Row 2 with row_span 2
