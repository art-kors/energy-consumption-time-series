"""Menu widget module."""

from collections.abc import Callable, Iterable
from functools import wraps
from tkinter import Menu, Misc, Variable
from tkinter.ttk import Menubutton


class SelectionMenu[T: object](Menubutton):
    """Menu widget."""

    def __init__(
        self,
        master: Misc,
        items: Iterable[T],
        callback: Callable[[T], None] | None = None,
    ) -> None:
        """Initialize menu widget."""
        self._value = Variable(master, next(iter(items)))
        self.callback = callback
        self.menu = Menu(master)
        self.set_items(items)
        super().__init__(master, menu=self.menu, textvariable=self._value)

    def set_items(self, items: Iterable[T]) -> None:
        """Set menu items."""
        self.menu.delete(0, "end")
        for item in items:
            self.menu.add_command(label=item, command=self.wrap_callback(item))

    def wrap_callback(self, value: T) -> Callable[[], None]:
        """Wraps callback: set selected value before calling callback."""
        @wraps(self.callback)
        def wrapper() -> None:
            self.value = value
            if self.callback is not None:
                self.callback(value)

        return wrapper

    @property
    def value(self) -> T:
        """Get menu's selected value."""
        return self._value.get()

    @value.setter
    def value(self, value: T) -> None:
        self._value.set(value)
