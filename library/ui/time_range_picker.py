"""Main application module."""

from datetime import datetime
from functools import wraps
from typing import Callable
from tkinter import Misc
from tkinter.ttk import Button, Frame

from library.ui.time_picker import TimePicker


class RangeTimePicker(Frame):
    """Main application class."""

    def __init__(self, master: Misc, button_text: str, callback: Callable[[datetime, datetime], None]) -> None:
        """Initialize main application class."""
        super().__init__(master)

        self.time_picker_from = TimePicker(self)
        self.time_picker_to = TimePicker(self)
        self.confirm_button = Button(self, command=self.wrap_callback(callback), text=button_text)

        self.check_selected_time()

        self.time_picker_from.grid(column=1, row=1)
        self.time_picker_to.grid(column=3, row=1)
        self.confirm_button.grid(column=2, row=2)
    
    def check_selected_time(self) -> None:
        state = f"{"" if self.time_picker_from.value > self.time_picker_to.value else "!"}disabled"
        self.confirm_button.state((state,))
        self.after(1, self.check_selected_time)
    
    def wrap_callback(self, callback: Callable[[datetime, datetime], None]) -> Callable[[], None]:
        @wraps(callback)
        def wrapper():
            callback(self.time_picker_from.value, self.time_picker_to.value)
        return wrapper
