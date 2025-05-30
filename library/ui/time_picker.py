"""Time picker widget module."""

from calendar import monthrange
from datetime import UTC, datetime, timedelta
from tkinter import Misc
from tkinter.ttk import Frame

from library.ui.menu import SelectionMenu


class TimePicker(Frame):
    """Time picker frame."""

    def __init__(self, master: Misc, *args: object, **kwargs: object) -> None:
        """Initialize time picker frame."""
        super().__init__(master, *args, **kwargs)

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

        self.after(1, self.check_selected_time)

        self.year_menu.pack()
        self.month_menu.pack()
        self.day_menu.pack()
        self.hour_menu.pack()
        self.minute_menu.pack()

    def check_selected_time(self) -> None:
        """Check that selected time is greater than now UTC time."""
        datetime_now = datetime.now(UTC)
        datetime_selected = datetime(
            year=self.year_menu.value,
            month=self.month_menu.value,
            day=self.day_menu.value,
            hour=self.hour_menu.value,
            minute=self.minute_menu.value,
            tzinfo=UTC,
        )

        if datetime_now - datetime_selected >= timedelta(minutes=1):
            self.year_menu.value = datetime_now.year
            self.month_menu.value = datetime_now.month

            _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
            self.day_menu.set_items(range(1, days_in_month + 1))
            self.day_menu.value = datetime_now.day

            self.hour_menu.value = datetime_now.hour
            self.minute_menu.value = datetime_now.minute

        self.after(1, self.check_selected_time)

    def on_month_selected(self, _selected_month: int) -> None:
        """Check days menu, when month selected."""
        _, days_in_month = monthrange(self.year_menu.value, self.month_menu.value)
        self.day_menu.set_items(range(1, days_in_month + 1))
        self.day_menu.value = min(self.day_menu.value, days_in_month)
