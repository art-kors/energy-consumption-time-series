from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class Layout(QVBoxLayout):
    def __init__(
        self,
        start_date,
        start_time,
        end_date,
        end_time,
        city_combo,
        btn_show,
    ):
        super().__init__()

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(QLabel("Дата начала:"))
        start_date_layout.addWidget(start_date)

        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(QLabel("Время начала:"))
        start_time_layout.addWidget(start_time)

        end_date_layout = QHBoxLayout()
        end_date_layout.addWidget(QLabel("Дата окончания:"))
        end_date_layout.addWidget(end_date)

        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(QLabel("Время окончания:"))
        end_time_layout.addWidget(end_time)

        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("Город:"))
        city_layout.addWidget(city_combo)

        self.addLayout(start_date_layout)
        self.addLayout(start_time_layout)
        self.addLayout(end_date_layout)
        self.addLayout(end_time_layout)
        self.addLayout(city_layout)
        self.addWidget(btn_show)
