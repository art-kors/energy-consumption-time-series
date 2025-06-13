from PySide6.QtCore import QTime
from PySide6.QtWidgets import QTimeEdit


class TimeSelector(QTimeEdit):
    def __init__(self, on_time_changed):
        super().__init__()
        self.setDisplayFormat("HH:mm")
        self.setTime(QTime.currentTime())
        self.timeChanged.connect(on_time_changed)
