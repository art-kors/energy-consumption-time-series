"""Main UI module."""

from datetime import datetime
from pathlib import Path
from typing import Self

from PySide6.QtWidgets import (
    QComboBox,
    QPushButton,
    QWidget,
)

from library.functional import model_predict
from library.ui.date_selector import DateSelector
from library.ui.layout import Layout
from library.ui.result import ResultDialog
from library.ui.time_selector import TimeSelector


class App(QWidget):
    def __init__(self: Self) -> None:
        super().__init__()
        self.setWindowTitle("Выбор даты, времени и города")

        self.start_date = DateSelector(self.check_datetime_validity)
        self.end_date = DateSelector(self.check_datetime_validity)

        self.start_time = TimeSelector(self.check_datetime_validity)
        self.end_time = TimeSelector(self.check_datetime_validity)

        self.companies = self.get_companies()

        self.btn_show = QPushButton("Показать выбор")
        self.btn_show.clicked.connect(self.show_selection)

        self.setLayout(
            Layout(
                self.start_date,
                self.start_time,
                self.end_date,
                self.end_time,
                self.companies,
                self.btn_show,
            ),
        )

        self.check_datetime_validity()

    @staticmethod
    def get_companies() -> QComboBox:
        companies = QComboBox()
        file_ending_length = 11
        companies.addItems(
            [
                company.name[:-file_ending_length]
                for company in Path("./data/").iterdir()
            ],
        )
        return companies

    def get_start_datetime(self):
        date = self.start_date.date().toPython()
        time = self.start_time.time().toPython()
        return datetime.combine(date=date, time=time)

    def get_end_datetime(self):
        date = self.end_date.date().toPython()
        time = self.end_time.time().toPython()
        return datetime.combine(date=date, time=time)

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
        data_frame = model_predict(
            self.companies.currentText(),
            self.get_start_datetime(),
            self.get_end_datetime(),
        )
        ResultDialog(parent=self, data_frame=data_frame).exec()
