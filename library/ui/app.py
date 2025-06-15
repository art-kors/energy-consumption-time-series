"""Main UI module."""

from datetime import datetime, time

from PySide6.QtWidgets import (
    QComboBox,
    QMessageBox,
    QPushButton,
    QWidget,
    QDialog,
    QVBoxLayout,
    QCheckBox,
)

import pandas as pd
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtWidgets import QHeaderView


from library.ui.date_selector import DateSelector
from library.ui.layout import Layout
from library.ui.time_selector import TimeSelector



import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class PlotDialog(QDialog):
    def __init__(self, df, x_col, y_col, parent=None):
        super().__init__(parent)
        self.setWindowTitle("График зависимости")

        layout = QVBoxLayout(self)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Построение графика
        self.ax.plot(df[x_col], df[y_col], marker='o', linestyle='-')
        self.ax.set_xlabel(x_col)
        self.ax.set_ylabel(y_col)
        self.ax.set_title(f'Зависимость {y_col} от {x_col}')
        self.ax.grid(True)

        self.canvas.draw()


class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()):
        return len(self._dataframe)

    def columnCount(self, parent=QModelIndex()):
        return self._dataframe.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None


class CheckboxDialog(QDialog):
    def __init__(self, parent, dataframe):
        super().__init__(parent)
        self.dataframe = dataframe
        self.setWindowTitle("Выберите варианты")
        self.checkboxes = []
        layout = QVBoxLayout()

        self.table = QTableView()
        self.model = PandasModel(dataframe)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        for label in dataframe.columns.tolist()[:-1]:
            cb = QCheckBox(label)
            self.checkboxes.append(cb)
            layout.addWidget(cb)

        self.btn_ok = QPushButton("Показать выбранные")
        self.btn_ok.clicked.connect(self.show_checked)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def show_checked(self):
        checked = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        print("Отмеченные чекбоксы:", checked)
        for col in checked:
            PlotDialog(self.dataframe, col, self.dataframe.columns.tolist()[-1], self).show()


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
