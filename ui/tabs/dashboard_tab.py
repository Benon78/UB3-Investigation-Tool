from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QHeaderView,
    QScrollArea
)

from ui.widgets.dashboard_card import DashboardCard


class DashboardTab(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            20, 20, 20, 20
        )
        layout.setSpacing(15)

        # =====================================
        # TITLE
        # =====================================

        title = QLabel(
            "Analytics Dashboard"
        )

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#0F172A;
        """)

        # =====================================
        # KPI ROW 1
        # =====================================

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

        # =====================================
        # KPI ROW 2
        # =====================================

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

        # =====================================
        # KPI ROW 3
        # =====================================

        row3 = QHBoxLayout()

        self.reboot_card = DashboardCard(
            "Reboots"
        )

        self.airwatt_card = DashboardCard(
            "Airwatt Short"
        )

        self.unique_sn_card = DashboardCard(
            "Lantern Events"
        )

        self.days_card = DashboardCard(
            "Days"
        )

        row3.addWidget(self.reboot_card)
        row3.addWidget(self.airwatt_card)
        row3.addWidget(self.unique_sn_card)
        row3.addWidget(self.days_card)

        # =====================================
        # CUSTOMER SUMMARY
        # =====================================

        customer_frame = QFrame()

        customer_frame.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:10px;
            }
        """)

        customer_layout = QVBoxLayout()

        customer_title = QLabel(
            "Customer Summary"
        )

        customer_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.customer_summary = QLabel(
            "Run analysis to load customer summary."
        )

        self.customer_summary.setWordWrap(
            True
        )

        self.customer_summary.setMaximumHeight(
            140
        )

        customer_layout.addWidget(
            customer_title
        )

        customer_layout.addWidget(
            self.customer_summary
        )

        customer_frame.setLayout(
            customer_layout
        )

        # =====================================
        # OPERATIONS TABLE
        # =====================================

        operations_frame = QFrame()

        operations_frame.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:10px;
            }
        """)

        operations_layout = QVBoxLayout()

        operations_title = QLabel(
            "Operation Summary"
        )

        operations_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.operations_table = QTableWidget()

        self.operations_table.setColumnCount(2)

        self.operations_table.setHorizontalHeaderLabels([
            "Operation",
            "Count"
        ])

        self.operations_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.operations_table.verticalHeader().setVisible(
            False
        )

        self.operations_table.setAlternatingRowColors(
            True
        )

        self.operations_table.setMaximumHeight(
            250
        )

        operations_layout.addWidget(
            operations_title
        )

        operations_layout.addWidget(
            self.operations_table
        )

        operations_frame.setLayout(
            operations_layout
        )

        # =====================================
        # INVESTIGATION SUMMARY
        # =====================================

        investigation_frame = QFrame()

        investigation_frame.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:10px;
            }
        """)

        investigation_layout = QVBoxLayout()

        investigation_title = QLabel(
            "Investigation Summary"
        )

        investigation_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.investigation_label = QLabel(
            "No analysis loaded."
        )

        self.investigation_label.setWordWrap(
            True
        )

        self.investigation_label.setStyleSheet("""
            padding:10px;
            font-size:14px;
        """)

        investigation_layout.addWidget(
            investigation_title
        )

        investigation_layout.addWidget(
            self.investigation_label
        )

        investigation_layout.addStretch()

        investigation_frame.setLayout(
            investigation_layout
        )

        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(
            operations_frame,
            2
        )

        bottom_layout.addWidget(
            investigation_frame,
            1
        )

        # =====================================
        # BUILD PAGE
        # =====================================

        layout.addWidget(title)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        layout.addWidget(
            customer_frame
        )

        layout.addLayout(
            bottom_layout
        )

        layout.addStretch()

        container.setLayout(layout)

        scroll.setWidget(container)

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)