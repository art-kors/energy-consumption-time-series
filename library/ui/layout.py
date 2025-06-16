"""Main layout module."""

from typing import Self, override

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from library.ui.date_selector import DateSelector
from library.ui.time_selector import TimeSelector


class Layout(QVBoxLayout):
    """Main window layout."""

    @override
    def __init__(
        self: Self,
        settings_button: QPushButton,
        start_date: DateSelector,
        start_time: TimeSelector,
        end_date: DateSelector,
        end_time: TimeSelector,
        companies: QComboBox,
        predict_button: QPushButton,
    ) -> None:
        super().__init__()

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(QLabel("Дата начала:"))
        start_date_layout.addWidget(start_date)

        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(QLabel("Время начала:"))
        start_time_layout.addWidget(start_time)

        end_date_layout = QHBoxLayout()
        end_date_layout.addWidget(QLabel("Дата окончания:"))
        end_date_layout.addWidget(end_date)

        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(QLabel("Время окончания:"))
        end_time_layout.addWidget(end_time)

        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("Компания:"))
        city_layout.addWidget(companies)

        self.addWidget(settings_button)
        self.addLayout(start_date_layout)
        self.addLayout(start_time_layout)
        self.addLayout(end_date_layout)
        self.addLayout(end_time_layout)
        self.addLayout(city_layout)
        self.addWidget(predict_button)
