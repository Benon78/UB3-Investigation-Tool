from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget
)


class FraudTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.risk_label = QLabel(
            "Risk Level: Not Analyzed"
        )

        self.flags_list = QListWidget()

        layout.addWidget(
            self.risk_label
        )

        layout.addWidget(
            self.flags_list
        )

        self.setLayout(layout)