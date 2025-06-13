"""Main UI module."""

import sys
from sys import argv

from PySide6.QtCore import QDate, Qt, QTime
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class TimeCitySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор даты, времени и города")

        # Метки
        start_date_label = QLabel("Дата начала:")
        start_time_label = QLabel("Время начала:")
        end_date_label = QLabel("Дата окончания:")
        end_time_label = QLabel("Время окончания:")
        city_label = QLabel("Город:")

        # Виджеты выбора даты
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        # Виджеты выбора времени
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setTime(QTime.currentTime())

        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setTime(QTime.currentTime())

        # Виджет выбора города
        self.city_combo = QComboBox()
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
        self.city_combo.addItems(cities)

        # Кнопка для вывода выбранных значений
        self.btn_show = QPushButton("Показать выбор")
        self.btn_show.clicked.connect(self.show_selection)

        # Компоновка элементов
        layout = QVBoxLayout()

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.start_date)

        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.start_time)

        end_date_layout = QHBoxLayout()
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(self.end_date)

        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(self.end_time)

        city_layout = QHBoxLayout()
        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_combo)

        layout.addLayout(start_date_layout)
        layout.addLayout(start_time_layout)
        layout.addLayout(end_date_layout)
        layout.addLayout(end_time_layout)
        layout.addLayout(city_layout)
        layout.addWidget(self.btn_show)

        self.setLayout(layout)

        # Подключаем слоты для проверки корректности выбора
        self.start_date.dateChanged.connect(self.check_datetime_validity)
        self.start_time.timeChanged.connect(self.check_datetime_validity)
        self.end_date.dateChanged.connect(self.check_datetime_validity)
        self.end_time.timeChanged.connect(self.check_datetime_validity)

        self.check_datetime_validity()

    def check_datetime_validity(self):
        start_dt = self.start_date.date().toPython()
        start_tm = self.start_time.time().toPython()
        end_dt = self.end_date.date().toPython()
        end_tm = self.end_time.time().toPython()

        from datetime import datetime, time

        start = datetime.combine(start_dt, time(start_tm.hour, start_tm.minute))
        end = datetime.combine(end_dt, time(end_tm.hour, end_tm.minute))

        if start > end:
            self.btn_show.setEnabled(False)
            self.btn_show.setToolTip("Время начала не может быть больше времени окончания")
        else:
            self.btn_show.setEnabled(True)
            self.btn_show.setToolTip("")

    def show_selection(self):
        start_date_str = self.start_date.date().toString(Qt.ISODate)
        start_time_str = self.start_time.time().toString("HH:mm")
        end_date_str = self.end_date.date().toString(Qt.ISODate)
        end_time_str = self.end_time.time().toString("HH:mm")
        city = self.city_combo.currentText()

        msg = (f"Дата и время начала: {start_date_str} {start_time_str}\n"
               f"Дата и время окончания: {end_date_str} {end_time_str}\n"
               f"Город: {city}")

        QMessageBox.information(self, "Выбранные данные", msg)

if __name__ == "__main__":
    app = QApplication(argv)
    window = TimeCitySelector()
    window.resize(350, 250)
    window.show()
    sys.exit(app.exec())
