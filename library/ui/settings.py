"""Settings module."""

from pathlib import Path
from typing import Self, override

from msgspec import DecodeError
from msgspec.toml import decode, encode
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Settings(QDialog):
    """Application settings."""

    file_name = "./settings.toml"
    plot_markers = ("o", "s", "^")
    plot_linestyles = ("-", "--", "-.", ":")

    @override
    def __init__(self: Self, parent: QWidget) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle("Настройки")

        plot_markers = QComboBox()
        plot_markers.addItems(Settings.plot_markers)
        plot_markers.setCurrentText(self.plot_marker())
        plot_markers.currentTextChanged.connect(
            lambda: self.set_property(
                "plot_marker",
                plot_markers.currentText(),
            ),
        )

        plot_linestyles = QComboBox()
        plot_linestyles.addItems(Settings.plot_linestyles)
        plot_linestyles.setCurrentText(self.plot_linestyle())
        plot_linestyles.currentTextChanged.connect(
            lambda: self.set_property(
                "plot_linestyle",
                plot_linestyles.currentText(),
            ),
        )

        select_color_button = QPushButton("Выберать цвет графика")
        select_color_button.clicked.connect(
            lambda: self.set_property(
                "plot_color",
                QColorDialog.getColor(
                    initial=self.plot_color(),
                    parent=self,
                    title="Выберите цвет графика",
                ).name(),
            ),
        )

        plot_marker_layout = QHBoxLayout()
        plot_marker_layout.addWidget(QLabel("Plot marker:"))
        plot_marker_layout.addWidget(plot_markers)

        plot_linestyle_layout = QHBoxLayout()
        plot_linestyle_layout.addWidget(QLabel("Plot linestyle:"))
        plot_linestyle_layout.addWidget(plot_linestyles)

        layout = QVBoxLayout()
        layout.addLayout(plot_marker_layout)
        layout.addLayout(plot_linestyle_layout)
        layout.addWidget(select_color_button)
        self.setLayout(layout)

    @staticmethod
    def check_file() -> None:
        """Check if file exists."""
        if not Path(Settings.file_name).exists():
            Path(Settings.file_name).touch()

    @staticmethod
    def get_property[T](name: str, default: T = None) -> T:
        """Get property."""
        Settings.check_file()

        with Path(Settings.file_name).open(mode="r") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        if name in data:
            return data[name]

        return default

    @staticmethod
    def set_property[T](name: str, value: T) -> T:
        """Set property."""
        Settings.check_file()

        with Path(Settings.file_name).open(mode="r") as file:
            try:
                data = decode(file.read())
            except DecodeError:
                data = {}

        data[name] = value

        with Path(Settings.file_name).open(mode="wb") as file:
            file.write(encode(data))

        return value

    @staticmethod
    def plot_marker() -> str:
        """Get plot marker."""
        default = Settings.plot_markers[0]
        marker = Settings.get_property("plot_marker", default)

        if marker in Settings.plot_markers:
            return marker
        return default

    @staticmethod
    def plot_linestyle() -> str:
        """Get plot linestyle."""
        default = Settings.plot_linestyles[0]
        linestyle = Settings.get_property("plot_linestyle", default)

        if linestyle in Settings.plot_linestyles:
            return linestyle
        return default

    @staticmethod
    def plot_color() -> str:
        """Get plot color."""
        default = "#000000"
        color = Settings.get_property("plot_color", default)
        if not color.startswith("#"):
            return default
        if len(color) != 7:
            return default
        for c in color[1:]:
            if c not in {
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
            }:
                return default
        return color
