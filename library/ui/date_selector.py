"""Date selector module."""

from collections.abc import Callable
from typing import Self, override

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateEdit


class DateSelector(QDateEdit):
    """Date selector widget."""

    @override
    def __init__(self: Self, on_date_changed: Callable[[], None]) -> None:
        super().__init__(QDate.currentDate())
        self.setCalendarPopup(True)
        self.dateChanged.connect(on_date_changed)
