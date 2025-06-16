"""Plot dialog module."""

from typing import Self, override

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from pandas import DataFrame
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from library.ui.settings import Settings


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
        super().__init__(parent, Qt.WindowType.Window)

        self.setWindowTitle("График зависимости")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(figure=self.figure)

        median_series = data_frame.groupby(x_column)[y_column].mean()

        self.ax.plot(
            median_series.index,
            median_series.to_numpy(),
            marker=Settings.plot_marker(),
            linestyle=Settings.plot_linestyle(),
            color=Settings.plot_color(),
        )
        self.ax.set_xlabel(xlabel=x_column)
        self.ax.set_ylabel(ylabel=y_column)
        self.ax.set_title(label=f"Зависимость {y_column} от {x_column}")
        self.ax.grid(visible=True)

        self.canvas.draw()

        self.save_button = QPushButton("Сохранить график")
        self.save_button.clicked.connect(self.save_plot)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_plot(self: Self) -> None:
        """Open a file dialog to save the current plot as an image file."""
        file_types = (
            "PNG Files (*.png)",
            "JPEG Files (*.jpeg)",
            "PDF Files (*.pdf)",
            "All Files (*)",
        )
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Сохранить график",
            filter=";;".join(file_types),
        )
        if file_path:
            self.figure.savefig(file_path)
