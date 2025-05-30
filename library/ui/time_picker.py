from tkinter import IntVar, _setit
from tkinter.ttk import OptionMenu, Frame
from calendar import monthrange
from datetime import datetime, timedelta


class TimePicker(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        datetime_now = datetime.now()
        
        self.selected_year = IntVar(self, datetime_now.year)
        self.selected_month = IntVar(self, datetime_now.month)
        self.selected_day = IntVar(self, datetime_now.day)
        self.selected_hour = IntVar(self, datetime_now.hour)
        self.selected_minute = IntVar(self, datetime_now.minute)

        self.year_menu = OptionMenu(self, self.selected_year, self.selected_year.get(), *range(datetime_now.year, datetime_now.year + 5), command=self.on_year_selected)
        self.month_menu = OptionMenu(self, self.selected_month, self.selected_month.get(), *range(1, 13), command=self.on_month_selected)
        _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
        self.day_menu = OptionMenu(self, self.selected_day, self.selected_day.get(), *range(1, days_in_month + 1), command=self.on_day_selected)
        self.hour_menu = OptionMenu(self, self.selected_hour, self.selected_hour.get(), *range(0, 24), command=self.on_hour_selected)
        self.minute_menu = OptionMenu(self, self.selected_minute, self.selected_minute.get(), *range(0, 60), command=self.on_minute_selected)

        self.year_menu.pack()
        self.month_menu.pack()
        self.day_menu.pack()
        self.hour_menu.pack()
        self.minute_menu.pack()

        self.after(1, self.check_selected_time)
    
    def check_selected_time(self):
        datetime_now = datetime.now()
        datetime_selected = datetime(self.selected_year.get(), self.selected_month.get(), self.selected_day.get(), self.selected_hour.get(), self.selected_minute.get())
        
        if datetime_now - datetime_selected >= timedelta(minutes=1):
            self.selected_year.set(datetime_now.year)
            self.selected_month.set(datetime_now.month)

            _, days_in_month = monthrange(datetime_now.year, datetime_now.month)
            self.day_menu["menu"].delete(0, "end")
            for day in range(1, days_in_month + 1):
                self.day_menu["menu"].add_command(label=day, command=_setit(self.selected_day, day))
            self.selected_day.set(datetime_now.day)

            self.selected_hour.set(datetime_now.hour)
            self.selected_minute.set(datetime_now.minute)

        self.after(1, self.check_selected_time)
    
    def on_year_selected(self, selected_year: int):
        print(f"Selected year: {selected_year}")
    
    def on_month_selected(self, selected_mounth: int):
        print(f"Selected mounth: {selected_mounth}")
        _, days_in_month = monthrange(self.selected_year.get(), self.selected_month.get())
        self.day_menu["menu"].delete(0, "end")
        for day in range(1, days_in_month + 1):
            self.day_menu["menu"].add_command(label=day, command=_setit(self.selected_day, day))
        if self.selected_day.get() > days_in_month:
            self.selected_day.set(days_in_month)
    
    def on_day_selected(self, selected_day: int):
        print(f"Selected day: {selected_day}")
    
    def on_hour_selected(self, selected_hour: int):
        print(f"Selected hour: {selected_hour}")
    
    def on_minute_selected(self, selected_minute: int):
        print(f"Selected minute: {selected_minute}")
