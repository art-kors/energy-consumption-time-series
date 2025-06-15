"""Time selector module."""

from collections.abc import Callable
from typing import Self, override

from PySide6.QtCore import QTime
from PySide6.QtWidgets import QTimeEdit


class TimeSelector(QTimeEdit):
    """Time selector widget."""

    @override
    def __init__(self: Self, on_time_changed: Callable[[], None]) -> None:
        super().__init__()
        self.setDisplayFormat("HH")
        self.setTime(QTime.currentTime())
        self.timeChanged.connect(on_time_changed)
