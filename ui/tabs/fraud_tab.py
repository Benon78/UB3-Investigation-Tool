from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTableWidget,
    QHeaderView,
    QScrollArea,
    QFrame
)

from ui.widgets.dashboard_card import DashboardCard


class FraudTab(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # =====================================
        # TITLE
        # =====================================

        title = QLabel(
            "Fraud Investigation Center"
        )

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#0F172A;
        """)

        # =====================================
        # SUMMARY BANNER
        # =====================================

        self.summary_label = QLabel(
            "No Analysis Loaded"
        )

        self.summary_label.setStyleSheet("""
            background:#FFF7ED;
            border:1px solid #FED7AA;
            border-radius:10px;
            padding:12px;
            font-weight:bold;
            color:#9A3412;
        """)

        # =====================================
        # KPI CARDS
        # =====================================

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

        cards_layout.addWidget(self.score_card)
        cards_layout.addWidget(self.level_card)
        cards_layout.addWidget(self.flags_card)
        cards_layout.addWidget(self.operations_card)

        # =====================================
        # RISK MATRIX
        # =====================================

        risk_frame = QFrame()

        risk_layout = QVBoxLayout()

        risk_title = QLabel(
            "Risk Matrix"
        )

        risk_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.risk_matrix_table = QTableWidget()

        self.risk_matrix_table.setColumnCount(2)

        self.risk_matrix_table.setHorizontalHeaderLabels([
            "Indicator",
            "Count"
        ])

        self.risk_matrix_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.risk_matrix_table.verticalHeader().setVisible(
            False
        )

        risk_layout.addWidget(
            risk_title
        )

        risk_layout.addWidget(
            self.risk_matrix_table
        )

        risk_frame.setLayout(
            risk_layout
        )

        # =====================================
        # SUSPICIOUS LANTERNS
        # =====================================

        lantern_frame = QFrame()

        lantern_layout = QVBoxLayout()

        lantern_title = QLabel(
            "Suspicious Lanterns"
        )

        lantern_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.suspicious_lanterns = QListWidget()

        lantern_layout.addWidget(
            lantern_title
        )

        lantern_layout.addWidget(
            self.suspicious_lanterns
        )

        lantern_frame.setLayout(
            lantern_layout
        )

        # =====================================
        # TOP SECTION
        # =====================================

        top_layout = QHBoxLayout()

        top_layout.addWidget(
            risk_frame,
            2
        )

        top_layout.addWidget(
            lantern_frame,
            1
        )

        # =====================================
        # SUSPICIOUS EVENTS
        # =====================================

        events_title = QLabel(
            "Suspicious Timeline"
        )

        events_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.suspicious_events_table = QTableWidget()

        self.suspicious_events_table.setColumnCount(4)

        self.suspicious_events_table.setHorizontalHeaderLabels([
            "Date",
            "Time",
            "Operation",
            "S/N"
        ])

        self.suspicious_events_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # =====================================
        # FLAGS
        # =====================================

        flags_title = QLabel(
            "Fraud Indicators"
        )

        flags_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.flags_list = QListWidget()

        # =====================================
        # VERDICT
        # =====================================

        verdict_title = QLabel(
            "Investigation Verdict"
        )

        verdict_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.verdict_label = QLabel(
            "No analysis loaded."
        )

        self.verdict_label.setWordWrap(
            True
        )

        self.verdict_label.setStyleSheet("""
            background:white;
            border:1px solid #E2E8F0;
            border-radius:10px;
            padding:15px;
            font-size:14px;
        """)

        # =====================================
        # ACTIONS
        # =====================================

        actions_title = QLabel(
            "Recommended Actions"
        )

        actions_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.actions_list = QListWidget()

        # =====================================
        # BUILD PAGE
        # =====================================

        layout.addWidget(title)

        layout.addWidget(
            self.summary_label
        )

        layout.addLayout(
            cards_layout
        )

        layout.addLayout(
            top_layout
        )

        layout.addWidget(
            events_title
        )

        layout.addWidget(
            self.suspicious_events_table
        )

        layout.addWidget(
            flags_title
        )

        layout.addWidget(
            self.flags_list
        )

        layout.addWidget(
            verdict_title
        )

        layout.addWidget(
            self.verdict_label
        )

        layout.addWidget(
            actions_title
        )

        layout.addWidget(
            self.actions_list
        )

        container.setLayout(
            layout
        )

        scroll.setWidget(
            container
        )

        main_layout.addWidget(
            scroll
        )

        self.setLayout(
            main_layout
        )