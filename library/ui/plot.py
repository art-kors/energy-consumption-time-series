"""Plot dialog module."""

from typing import Self, override

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from pandas import DataFrame
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget


class Plot(QDialog):
    """Plot dialog."""

    @override
    def __init__(
        self: Self,
        parent: QWidget,
        data_frame: DataFrame,
        x_column: str,
        y_column: str,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("График зависимости")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(figure=self.figure)

        self.ax.plot(
            data_frame[x_column],
            data_frame[y_column],
            marker="o",
            linestyle="-",
        )
        self.ax.set_xlabel(xlabel=x_column)
        self.ax.set_ylabel(ylabel=y_column)
        self.ax.set_title(label=f"Зависимость {y_column} от {x_column}")
        self.ax.grid(visible=True)

        self.canvas.draw()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
