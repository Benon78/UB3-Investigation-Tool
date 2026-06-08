from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from ui.widgets.dashboard_card import DashboardCard


class DashboardTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel(
            "Analytics Dashboard"
        )

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #0F172A;
        """)

        # Row 1

        row1 = QHBoxLayout()

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

        row1.addWidget(self.ub3_card)
        row1.addWidget(self.records_card)
        row1.addWidget(self.balance_card)
        row1.addWidget(self.risk_card)

        # Row 2

        row2 = QHBoxLayout()

        self.ul_success_card = DashboardCard(
            "UL.Success"
        )

        self.ul_fail_card = DashboardCard(
            "UL.Fail"
        )

        self.p_success_card = DashboardCard(
            "P.Success"
        )

        self.p_fail_card = DashboardCard(
            "P.Fail"
        )

        row2.addWidget(self.ul_success_card)
        row2.addWidget(self.ul_fail_card)
        row2.addWidget(self.p_success_card)
        row2.addWidget(self.p_fail_card)

        # Row 3

        row3 = QHBoxLayout()

        self.reboot_card = DashboardCard(
            "Reboots"
        )

        self.airwatt_card = DashboardCard(
            "Airwatt Short"
        )

        self.unique_sn_card = DashboardCard(
            "Lanterns"
        )

        self.days_card = DashboardCard(
            "Days"
        )

        row3.addWidget(self.reboot_card)
        row3.addWidget(self.airwatt_card)
        row3.addWidget(self.unique_sn_card)
        row3.addWidget(self.days_card)

        layout.addWidget(title)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        self.setLayout(layout)