"""Time picker widget module."""

from calendar import monthrange
from datetime import UTC, datetime, timedelta
from tkinter import Misc
from tkinter.ttk import Frame

from library.ui.menu import SelectionMenu


class TimePicker(Frame):
    """Time picker frame."""

    def __init__(self, master: Misc) -> None:
        """Initialize time picker frame."""
        super().__init__(master)

        datetime_now = datetime.now(UTC)

        self.year_menu = SelectionMenu(
            self,
            range(datetime_now.year, datetime_now.year + 10),
        )
        self.month_menu = SelectionMenu(self, range(1, 13), self.on_month_selected)
        _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
        self.day_menu = SelectionMenu(self, range(1, days_in_month + 1))
        self.hour_menu = SelectionMenu(self, range(24))
        self.minute_menu = SelectionMenu(self, range(60))

        self.check_selected_time()

        self.year_menu.pack()
        self.month_menu.pack()
        self.day_menu.pack()
        self.hour_menu.pack()
        self.minute_menu.pack()

    def check_selected_time(self) -> None:
        """Check that selected time is greater than now UTC time."""
        datetime_now = datetime.now(UTC)
        datetime_selected = self.value

        if datetime_now - datetime_selected >= timedelta(minutes=1):
            self.value = datetime_now

        self.after(1, self.check_selected_time)

    def on_month_selected(self, _selected_month: int) -> None:
        """Check days menu, when month selected."""
        _, days_in_month = monthrange(self.year_menu.value, self.month_menu.value)
        self.day_menu.set_items(range(1, days_in_month + 1))
        self.day_menu.value = min(self.day_menu.value, days_in_month)
    
    @property
    def value(self) -> datetime:
        return datetime(
            year=self.year_menu.value,
            month=self.month_menu.value,
            day=self.day_menu.value,
            hour=self.hour_menu.value,
            minute=self.minute_menu.value,
            tzinfo=UTC,
        )
    
    @value.setter
    def value(self, value: datetime) -> None:
        self.year_menu.value = value.year
        self.month_menu.value = value.month

        _, days_in_month = monthrange(value.year, value.month)
        self.day_menu.set_items(range(1, days_in_month + 1))
        self.day_menu.value = value.day

        self.hour_menu.value = value.hour
        self.minute_menu.value = value.minute
