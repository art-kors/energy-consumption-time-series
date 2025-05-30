"""Main application module."""

from tkinter import Tk

from library.ui.time_picker import TimePicker


class App(Tk):
    """Main application class."""

    def __init__(self) -> None:
        """Initialize main application class."""
        super().__init__()
        self.time_picker = TimePicker(self)
        self.time_picker.pack()


if __name__ == "__main__":
    App().mainloop()
