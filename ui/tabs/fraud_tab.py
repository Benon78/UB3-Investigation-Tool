from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextEdit
)

from ui.widgets.dashboard_card import DashboardCard


class FraudTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel(
            "Fraud Investigation"
        )

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #0F172A;
        """)

        self.summary_label = QLabel(
            "No Analysis Loaded"
        )

        self.summary_label.setStyleSheet("""
            background: #FFF7ED;
            padding: 12px;
            border-radius: 8px;
            color: #9A3412;
            font-weight: bold;
        """)

        cards_layout = QHBoxLayout()

        self.score_card = DashboardCard(
            "Risk Score"
        )

        self.level_card = DashboardCard(
            "Risk Level"
        )

        self.flags_card = DashboardCard(
            "Flags"
        )

        self.operations_card = DashboardCard(
            "Suspicious Ops"
        )

        cards_layout.addWidget(
            self.score_card
        )

        cards_layout.addWidget(
            self.level_card
        )

        cards_layout.addWidget(
            self.flags_card
        )

        cards_layout.addWidget(
            self.operations_card
        )

        self.flags_list = QListWidget()

        self.operations_table = QTableWidget()

        self.operations_table.setColumnCount(2)

        self.operations_table.setHorizontalHeaderLabels([
            "Operation",
            "Count"
        ])

        self.operations_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.actions_box = QTextEdit()
        self.actions_box.setReadOnly(True)
        self.actions_box.setMinimumHeight(180)

        layout.addWidget(
            self.summary_label
        )
        layout.addWidget(title)
        layout.addLayout(cards_layout)

        layout.addWidget(
            QLabel("Detected Alerts")
        )

        layout.addWidget(
            self.flags_list
        )

        layout.addWidget(
            QLabel("Operation Breakdown")
        )

        layout.addWidget(
            self.operations_table
        )

        layout.addWidget(
            QLabel("Recommended Actions")
        )

        layout.addWidget(
            self.actions_box
        )

        self.setLayout(layout)