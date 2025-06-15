"""Main UI module."""

from datetime import datetime
from pathlib import Path
from random import randint
from typing import Self, override

from pandas import DataFrame
from PySide6.QtWidgets import (
    QComboBox,
    QPushButton,
    QWidget,
)

from library.functional import model_predict
from library.ui.date_selector import DateSelector
from library.ui.layout import Layout
from library.ui.prediction import PredictionDialog
from library.ui.time_selector import TimeSelector


class App(QWidget):
    """Main widget."""

    @override
    def __init__(self: Self) -> None:
        super().__init__()
        self.setWindowTitle("Energy consumption time series")

        self.start_date = DateSelector(self.check_datetime_validity)
        self.end_date = DateSelector(self.check_datetime_validity)

        self.start_time = TimeSelector(self.check_datetime_validity)
        self.end_time = TimeSelector(self.check_datetime_validity)

        self.companies = self.get_companies()

        self.predict_button = QPushButton("Предсказать потребление")
        self.predict_button.clicked.connect(self.show_predict_result)

        self.setLayout(
            Layout(
                start_date=self.start_date,
                start_time=self.start_time,
                end_date=self.end_date,
                end_time=self.end_time,
                companies=self.companies,
                predict_button=self.predict_button,
            ),
        )

        self.check_datetime_validity()

    @staticmethod
    def get_companies() -> QComboBox:
        """Generate menu of companies."""
        companies = QComboBox()
        file_ending_length = 11
        companies.addItems(
            [
                company.name[:-file_ending_length]
                for company in Path("./data/").iterdir()
            ],
        )
        return companies

    def get_start_datetime(self: Self) -> datetime:
        """Get selected start date and time in `datetime` format."""
        return datetime.combine(
            date=self.start_date.date().toPython(),
            time=self.start_time.time().toPython(),
        )

    def get_end_datetime(self: Self) -> datetime:
        """Get selected end date and time in `datetime` format."""
        return datetime.combine(
            date=self.end_date.date().toPython(),
            time=self.end_time.time().toPython(),
        )

    def check_datetime_validity(self: Self) -> None:
        """Check that start datetime is less than end datetime."""
        if self.get_start_datetime() > self.get_end_datetime():
            self.predict_button.setEnabled(False)
            self.predict_button.setToolTip(
                "Время начала не может быть больше времени окончания",
            )
        else:
            self.predict_button.setEnabled(True)
            self.predict_button.setToolTip("")

    def show_predict_result(self) -> None:
        """Show predict result."""
        data_frame = model_predict(
            self.companies.currentText(),
            self.get_start_datetime(),
            self.get_end_datetime(),
        )
        # data_frame = DataFrame({
        #     "A": [randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        #     "B": [randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        #     "C": [randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        #     "D": [randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)],
        # })
        PredictionDialog(parent=self, data_frame=data_frame).exec()
