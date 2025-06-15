from typing import Self, override

from pandas import DataFrame
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    Qt,
)


class PandasModel(QAbstractTableModel):
    def __init__(self: Self, parent: QObject, data_frame: DataFrame):
        super().__init__(parent=parent)
        self.data_frame = data_frame

    @override
    def rowCount(self: Self, *_args: object, **_kwargs: object) -> int:
        return len(self.data_frame)

    @override
    def columnCount(self, *_args: object, **_kwargs: object) -> int:
        return self.data_frame.columns.size

    @override
    def data(
        self: Self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.data_frame.iloc[index.row(), index.column()])
        return None

    @override
    def headerData(
        self: Self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.data_frame.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self.data_frame.index[section])
        return None
