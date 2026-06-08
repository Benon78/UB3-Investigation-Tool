from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from ui.widgets.dashboard_card import DashboardCard


class DashboardTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        cards_layout = QHBoxLayout()

        self.ub3_card = DashboardCard(
            "UB3 Found"
        )

        self.records_card = DashboardCard(
            "Records"
        )

        self.balance_card = DashboardCard(
            "Balance"
        )

        self.risk_card = DashboardCard(
            "Risk"
        )

        cards_layout.addWidget(
            self.ub3_card
        )

        cards_layout.addWidget(
            self.records_card
        )

        cards_layout.addWidget(
            self.balance_card
        )

        cards_layout.addWidget(
            self.risk_card
        )

        layout.addLayout(cards_layout)

        self.setLayout(layout)