"""Main UI module."""

from datetime import datetime, time

import pandas as pd
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QHeaderView,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from library.ui.date_selector import DateSelector
from library.ui.layout import Layout
from library.ui.plot import Plot
from library.ui.table import PandasModel
from library.ui.time_selector import TimeSelector


class CheckboxDialog(QDialog):
    def __init__(self, parent, data_frame):
        super().__init__(parent)
        self.data_frame = data_frame
        self.setWindowTitle("Выберите варианты")
        self.checkboxes = []
        layout = QVBoxLayout()

        self.table = QTableView()
        self.model = PandasModel(parent=self, data_frame=data_frame)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        for label in data_frame.columns.tolist()[:-1]:
            cb = QCheckBox(label)
            self.checkboxes.append(cb)
            layout.addWidget(cb)

        self.btn_ok = QPushButton("Показать выбранные")
        self.btn_ok.clicked.connect(self.show_checked)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def show_checked(self):
        checked = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        y_column = self.data_frame.columns.tolist()[-1]
        for x_column in checked:
            Plot(
                parent=self,
                data_frame=self.data_frame,
                x_column=x_column,
                y_column=y_column,
            ).show()


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

        self.setLayout(Layout(self.start_date, self.start_time, self.end_date, self.end_time, self.city_combo, self.btn_show))

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
            self.btn_show.setToolTip("Время начала не может быть больше времени окончания")
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
        CheckboxDialog(self, dataframe).exec()
        city = self.city_combo.currentText()
