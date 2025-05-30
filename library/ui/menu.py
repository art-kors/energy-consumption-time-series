from typing import Iterable, Callable
from functools import wraps

from tkinter import Menu, Misc, Variable
from tkinter.ttk import Menubutton


class SelectionMenu[T: object](Menubutton):
    def __init__(self, master: Misc, items: Iterable[T], callback: Callable[[T], object]):
        self.selected = Variable(master)
        self.callback = callback
        self.menu = Menu(master)
        self.set_items(items)
        super().__init__(master, menu=self.menu, textvariable=self.selected)

    def set_items(self, items: Iterable[object]):
        self.menu.delete(0, "end")
        for item in items:
            self.menu.add_command(label=item, command=self.wrap_callback(item))

    def wrap_callback(self, value):
        @wraps(self.callback)
        def wrapper():
            self.value = value
            return self.callback(value)
        return wrapper

    @property
    def value(self) -> T:
        return self.selected.get()

    @value.setter
    def value(self, value: T):
        self.selected.set(value)
