from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class DashboardCard(QFrame):

    def __init__(self, title, value="0"):
        super().__init__()

        self.setObjectName("dashboardCard")

        layout = QVBoxLayout()

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.value_label = QLabel(str(value))
        self.value_label.setAlignment(Qt.AlignCenter)

        self.value_label.setObjectName("cardValue")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        self.setLayout(layout)

    def update_value(self, value):
        self.value_label.setText(str(value))