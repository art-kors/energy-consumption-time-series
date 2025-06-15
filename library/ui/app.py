"""Main UI module."""

from datetime import datetime, time

import pandas as pd
from PySide6.QtWidgets import (
    QComboBox,
    QPushButton,
    QWidget,
)

from library.ui.date_selector import DateSelector
from library.ui.layout import Layout
from library.ui.result import ResultDialog
from library.ui.time_selector import TimeSelector


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор даты, времени и города")

        self.start_date = DateSelector(self.check_datetime_validity)
        self.end_date = DateSelector(self.check_datetime_validity)

        self.start_time = TimeSelector(self.check_datetime_validity)
        self.end_time = TimeSelector(self.check_datetime_validity)

        self.city_combo = QComboBox()
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
        self.city_combo.addItems(cities)

        self.btn_show = QPushButton("Показать выбор")
        self.btn_show.clicked.connect(self.show_selection)

        self.setLayout(Layout(
            self.start_date,
            self.start_time,
            self.end_date,
            self.end_time,
            self.city_combo,
            self.btn_show,
        ))

        self.check_datetime_validity()

    def get_start_datetime(self):
        start_dt = self.start_date.date().toPython()
        start_tm = self.start_time.time().toPython()
        return datetime.combine(start_dt, time(start_tm.hour, start_tm.minute))

    def get_end_datetime(self):
        end_dt = self.end_date.date().toPython()
        end_tm = self.end_time.time().toPython()
        return datetime.combine(end_dt, time(end_tm.hour, end_tm.minute))

    def check_datetime_validity(self):
        start = self.get_start_datetime()
        end = self.get_end_datetime()

        if start > end:
            self.btn_show.setEnabled(False)
            self.btn_show.setToolTip(
                "Время начала не может быть больше времени окончания",
            )
        else:
            self.btn_show.setEnabled(True)
            self.btn_show.setToolTip("")

    def show_selection(self):
        dataframe = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [28, 34, 45],
            'Occupation': ['Engineer', 'Doctor', 'Artist'],
            'result': [123, 456, 789],
        })
        ResultDialog(self, dataframe).exec()
        city = self.city_combo.currentText()
