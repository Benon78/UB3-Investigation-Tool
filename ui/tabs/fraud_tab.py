from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTableWidget,
    QHeaderView,
    QTabWidget
)

from ui.widgets.dashboard_card import DashboardCard


class FraudTab(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ==========================================
        # Title
        # ==========================================

        title = QLabel(
            "Fraud Investigation Center"
        )

        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #0F172A;
        """)

        # ==========================================
        # Summary Banner
        # ==========================================

        self.summary_label = QLabel(
            "No Analysis Loaded"
        )

        self.summary_label.setStyleSheet("""
            background-color: #FFF7ED;
            border: 1px solid #FED7AA;
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            color: #9A3412;
        """)

        # ==========================================
        # Dashboard Cards
        # ==========================================

        cards_layout = QHBoxLayout()

        self.score_card = DashboardCard(
            "Risk Score"
        )

        self.level_card = DashboardCard(
            "Risk Level"
        )

        self.flags_card = DashboardCard(
            "Flags Found"
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

        # ==========================================
        # Internal Fraud Tabs
        # ==========================================

        self.fraud_tabs = QTabWidget()

        # ==========================================
        # Summary Tab
        # ==========================================

        summary_tab = QWidget()

        summary_layout = QVBoxLayout()

        self.summary_details = QLabel(
            "Run an analysis to view fraud insights."
        )

        self.summary_details.setWordWrap(True)

        self.summary_details.setStyleSheet("""
            font-size: 14px;
            padding: 15px;
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
        """)

        summary_layout.addWidget(
            self.summary_details
        )

        summary_layout.addStretch()

        summary_tab.setLayout(
            summary_layout
        )

        # ==========================================
        # Alerts Tab
        # ==========================================

        alerts_tab = QWidget()

        alerts_layout = QVBoxLayout()

        self.flags_list = QListWidget()

        self.flags_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                background: white;
                padding: 8px;
            }

            QListWidget::item {
                background: #FFF7ED;
                border: 1px solid #FED7AA;
                border-radius: 8px;
                margin: 4px;
                padding: 12px;
                color: #9A3412;
                font-weight: bold;
            }
        """)

        alerts_layout.addWidget(
            self.flags_list
        )

        alerts_tab.setLayout(
            alerts_layout
        )

        # ==========================================
        # Operations Tab
        # ==========================================

        operations_tab = QWidget()

        operations_layout = QVBoxLayout()

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

        operations_layout.addWidget(
            self.operations_table
        )

        operations_tab.setLayout(
            operations_layout
        )

        self.operations_table.setSortingEnabled(True)

        self.operations_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.operations_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        # ==========================================
        # Recommendations Tab
        # ==========================================

        recommendations_tab = QWidget()

        recommendations_layout = QVBoxLayout()

        self.actions_list = QListWidget()

        self.actions_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #D1FAE5;
                background: #ECFDF5;
                border-radius: 10px;
                padding: 8px;
            }

            QListWidget::item {
                margin: 4px;
                padding: 12px;
                color: #065F46;
                font-weight: bold;
            }
        """)

        recommendations_layout.addWidget(
            self.actions_list
        )

        recommendations_tab.setLayout(
            recommendations_layout
        )

        # ==========================================
        # Add Tabs
        # ==========================================

        self.fraud_tabs.addTab(
            summary_tab,
            "📊 Summary"
        )

        self.fraud_tabs.addTab(
            alerts_tab,
            "🚨 Alerts"
        )

        self.fraud_tabs.addTab(
            operations_tab,
            "📋 Operations"
        )

        self.fraud_tabs.addTab(
            recommendations_tab,
            "📝 Recommendations"
        )

        # ==========================================
        # Assemble Layout
        # ==========================================

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            self.summary_label
        )

        main_layout.addLayout(
            cards_layout
        )

        main_layout.addWidget(
            self.fraud_tabs
        )

        self.setLayout(
            main_layout
        )