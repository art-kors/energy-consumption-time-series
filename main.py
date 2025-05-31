"""Main application module."""

from datetime import datetime
from tkinter import Tk

from library.ui.time_range_picker import RangeTimePicker


class App(Tk):
    """Main application class."""

    def __init__(self) -> None:
        """Initialize main application class."""
        super().__init__()

        self.set_window_geometry()
        
        self.time_picker = RangeTimePicker(self, "Predict", self.predict)
        self.time_picker.pack()
    
    def set_window_geometry(self, width: int = 1280, height: int = 720) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def predict(self, start: datetime, end: datetime) -> None:
        print(f"Prediction: {start} -> {end}")


if __name__ == "__main__":
    App().mainloop()
