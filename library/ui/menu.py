from typing import Iterable, Callable
from functools import wraps

from tkinter import Menu, Misc, Variable
from tkinter.ttk import Menubutton


class SelectionMenu[T: object](Menubutton):
    def __init__(self, master: Misc, items: Iterable[T], callback: Callable[[T], object]):
        self._value = Variable(master, next(iter(items)))
        self.callback = callback
        self.menu = Menu(master)
        self.set_items(items)
        super().__init__(master, menu=self.menu, textvariable=self._value)

    def set_items(self, items: Iterable[T]):
        self.menu.delete(0, "end")
        for item in items:
            self.menu.add_command(label=item, command=self.wrap_callback(item))

    def wrap_callback(self, value: T):
        @wraps(self.callback)
        def wrapper():
            self.value = value
            return self.callback(value)
        return wrapper

    @property
    def value(self) -> T:
        return self._value.get()

    @value.setter
    def value(self, value: T):
        self._value.set(value)
