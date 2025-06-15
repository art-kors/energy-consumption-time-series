from typing import Self

from pandas import DataFrame
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHeaderView,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from library.ui.plot import Plot
from library.ui.table import PandasModel


class ResultDialog(QDialog):
    def __init__(self: Self, parent: QWidget, data_frame: DataFrame) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle("Выберите варианты")

        self.data_frame = data_frame
        self.checkboxes = []

        layout = QVBoxLayout()

        self.table = self.create_table(data_frame=data_frame)
        layout.addWidget(self.table)

        for label in data_frame.columns.tolist()[:-1]:
            cb = QCheckBox(label)
            self.checkboxes.append(cb)
            layout.addWidget(cb)

        self.btn_ok = QPushButton("Показать выбранные")
        self.btn_ok.clicked.connect(self.show_checked)
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def create_table(self: Self, data_frame: DataFrame) -> QTableView:
        table = QTableView()
        table.setModel(PandasModel(parent=self, data_frame=data_frame))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # self.table.horizontalHeader().setStretchLastSection(True)
        return table

    def show_checked(self: Self):
        checked = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        y_column = self.data_frame.columns.tolist()[-1]
        for x_column in checked:
            Plot(
                parent=self,
                data_frame=self.data_frame,
                x_column=x_column,
                y_column=y_column,
            ).show()
