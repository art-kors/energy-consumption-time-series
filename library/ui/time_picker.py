from tkinter.ttk import Frame
from calendar import monthrange
from datetime import datetime, timedelta

from library.ui.menu import SelectionMenu


class TimePicker(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        datetime_now = datetime.now()

        self.year_menu = SelectionMenu(self, range(datetime_now.year, datetime_now.year + 10), self.on_year_selected)
        self.month_menu = SelectionMenu(self, range(1, 13), self.on_month_selected)
        _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
        self.day_menu = SelectionMenu(self, range(1, days_in_month + 1), self.on_day_selected)
        self.hour_menu = SelectionMenu(self, range(0, 24), self.on_hour_selected)
        self.minute_menu = SelectionMenu(self, range(0, 60), self.on_minute_selected)
        
        self.after(1, self.check_selected_time)

        self.year_menu.pack()
        self.month_menu.pack()
        self.day_menu.pack()
        self.hour_menu.pack()
        self.minute_menu.pack()
    
    def check_selected_time(self):
        datetime_now = datetime.now()
        datetime_selected = datetime(self.year_menu.value, self.month_menu.value, self.day_menu.value, self.hour_menu.value, self.minute_menu.value)
        
        if datetime_now - datetime_selected >= timedelta(minutes=1):
            self.year_menu.value = datetime_now.year
            self.month_menu.value = datetime_now.month

            _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
            self.day_menu.set_items(range(1, days_in_month + 1))
            self.day_menu.value = datetime_now.day

            self.hour_menu.value = datetime_now.hour
            self.minute_menu.value = datetime_now.minute

        self.after(1, self.check_selected_time)
    
    def on_year_selected(self, selected_year: int):
        print(f"Selected year: {selected_year}")
    
    def on_month_selected(self, selected_mounth: int):
        print(f"Selected mounth: {selected_mounth}")
        _, days_in_month = monthrange(self.year_menu.value, self.month_menu.value)
        self.day_menu.set_items(range(1, days_in_month + 1))
        if self.day_menu.value > days_in_month:
            self.day_menu.value = days_in_month
    
    def on_day_selected(self, selected_day: int):
        print(f"Selected day: {selected_day}")
    
    def on_hour_selected(self, selected_hour: int):
        print(f"Selected hour: {selected_hour}")
    
    def on_minute_selected(self, selected_minute: int):
        print(f"Selected minute: {selected_minute}")
