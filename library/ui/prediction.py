"""Prediction dialog module."""

from enum import StrEnum
from typing import Self, override

from pandas import DataFrame
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from library.ui.plot import Plot
from library.ui.table import PandasModel


class TableFormat(StrEnum):
    """Table export formats."""

    XLSX = "EXCEL (*.xlsx)"
    CSV = "CSV (*.csv)"
    XML = "XML (*.xml)"
    HTML = "HTML (*.html)"
    JSON = "JSON (*.json)"


class PredictionDialog(QDialog):
    """Prediction dialog."""

    @override
    def __init__(self: Self, parent: QWidget, data_frame: DataFrame) -> None:
        super().__init__(parent=parent, f=Qt.WindowType.Window)
        self.setWindowTitle("Предсказание")

        self.data_frame = data_frame
        self.graphs = []

        layout = QVBoxLayout()

        self.table = self.create_table(data_frame=data_frame)
        layout.addWidget(self.table)

        self.export_button = QPushButton("Экспортировать таблицу")
        self.export_button.clicked.connect(self.export_table)
        layout.addWidget(self.export_button)

        layout.addWidget(
            QLabel(
                text="Выберите графики зависимости предсказания",
                alignment=Qt.AlignmentFlag.AlignCenter,
            ),
        )

        main_checkbox_layout = QHBoxLayout()
        columns = data_frame.columns.tolist()[:-1]
        for i in range(0, len(columns), 4):
            checkbox_layout = QVBoxLayout()
            for j in range(i, i + 4):
                if j >= len(columns):
                    break
                label = columns[j]
                graph = QCheckBox(label)
                self.graphs.append(graph)
                checkbox_layout.addWidget(graph)
            main_checkbox_layout.addLayout(checkbox_layout)
        layout.addLayout(main_checkbox_layout)

        self.show_graphs_button = QPushButton("Показать графики")
        self.show_graphs_button.clicked.connect(self.show_selected_graphs)
        layout.addWidget(self.show_graphs_button)

        self.setLayout(layout)

    def create_table(self: Self, data_frame: DataFrame) -> QTableView:
        """Create prediction table."""
        table = QTableView()
        table.setModel(PandasModel(parent=self, data_frame=data_frame))
        table.horizontalHeader().setStretchLastSection(True)
        return table

    def export_table(self: Self) -> None:
        """Export table to file."""
        file_path, file_type = QFileDialog.getSaveFileName(
            parent=self,
            caption="Сохранить таблицу",
            filter=";;".join(
                table_format.value for table_format in TableFormat
            ),
        )
        if file_path:
            match file_type:
                case TableFormat.XLSX:
                    self.data_frame.to_excel(file_path)
                case TableFormat.CSV:
                    self.data_frame.to_csv(file_path)
                case TableFormat.XML:
                    self.data_frame.to_xml(file_path)
                case TableFormat.HTML:
                    self.data_frame.to_html(file_path)
                case TableFormat.JSON:
                    self.data_frame.to_json(file_path)

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
