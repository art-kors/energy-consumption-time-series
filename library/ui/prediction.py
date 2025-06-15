"""Prediction dialog module."""

from typing import Self, override

from pandas import DataFrame
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from library.ui.plot import Plot
from library.ui.table import PandasModel


class PredictionDialog(QDialog):
    """Predict dialog."""

    @override
    def __init__(self: Self, parent: QWidget, data_frame: DataFrame) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle("Предсказание")

        self.data_frame = data_frame
        self.graphs = []

        layout = QVBoxLayout()

        self.table = self.create_table(data_frame=data_frame)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Выберите графики зависимости предсказания"))

        for label in data_frame.columns.tolist()[:-1]:
            graph = QCheckBox(label)
            self.graphs.append(graph)
            layout.addWidget(graph)

        self.show_graphs_button = QPushButton("Показать графики")
        self.show_graphs_button.clicked.connect(self.show_selected_graphs)
        layout.addWidget(self.show_graphs_button)

        self.setLayout(layout)

    def create_table(self: Self, data_frame: DataFrame) -> QTableView:
        """Create prediction table."""
        table = QTableView()
        table.setModel(PandasModel(parent=self, data_frame=data_frame))
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )
        # self.table.horizontalHeader().setStretchLastSection(True)
        return table

    def show_selected_graphs(self: Self) -> None:
        """Show selected graphs."""
        checked = [graph.text() for graph in self.graphs if graph.isChecked()]
        y_column = self.data_frame.columns.tolist()[-1]
        for x_column in checked:
            Plot(
                parent=self,
                data_frame=self.data_frame,
                x_column=x_column,
                y_column=y_column,
            ).show()
