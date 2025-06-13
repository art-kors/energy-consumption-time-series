from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit


class DateSelector(QDateEdit):
    def __init__(self, on_date_changed):
        super().__init__(QDate.currentDate())
        self.setCalendarPopup(True)
        self.dateChanged.connect(on_date_changed)
