from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QSpinBox,
    QDateEdit
)

from PySide6.QtCore import QDate


class TimelineTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # =====================================
        # Title
        # =====================================

        title = QLabel(
            "Activity Timeline"
        )

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #0F172A;
        """)

        # =====================================
        # Filter Row 1
        # =====================================

        filter_layout_1 = QHBoxLayout()

        self.operation_filter = QComboBox()

        self.operation_filter.setMinimumWidth(
            220
        )

        self.operation_filter.setEditable(
            False
        )

        self.operation_filter.addItem(
            "All Operations"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search Operation, S/N..."
        )

        filter_layout_1.addWidget(
            QLabel("Operation")
        )

        filter_layout_1.addWidget(
            self.operation_filter
        )

        filter_layout_1.addWidget(
            QLabel("Keyword")
        )

        filter_layout_1.addWidget(
            self.search_input
        )

        # =====================================
        # Filter Row 2
        # =====================================

        filter_layout_2 = QHBoxLayout()

        self.min_balance = QSpinBox()
        self.min_balance.setMaximum(
            99999999
        )

        self.max_balance = QSpinBox()
        self.max_balance.setMaximum(
            99999999
        )

        self.max_balance.setValue(
            99999999
        )

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(
            True
        )

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(
            True
        )

        today = QDate.currentDate()

        self.date_from.setDate(
            today.addYears(-1)
        )

        self.date_to.setDate(
            today
        )

        filter_layout_2.addWidget(
            QLabel("Min Balance")
        )

        filter_layout_2.addWidget(
            self.min_balance
        )

        filter_layout_2.addWidget(
            QLabel("Max Balance")
        )

        filter_layout_2.addWidget(
            self.max_balance
        )

        filter_layout_2.addWidget(
            QLabel("From")
        )

        filter_layout_2.addWidget(
            self.date_from
        )

        filter_layout_2.addWidget(
            QLabel("To")
        )

        filter_layout_2.addWidget(
            self.date_to
        )

        # =====================================
        # Buttons
        # =====================================

        buttons_layout = QHBoxLayout()

        self.filter_btn = QPushButton(
            "Apply Filters"
        )

        self.reset_btn = QPushButton(
            "Reset"
        )

        buttons_layout.addWidget(
            self.filter_btn
        )

        buttons_layout.addWidget(
            self.reset_btn
        )

        buttons_layout.addStretch()

        # =====================================
        # Summary
        # =====================================

        self.timeline_summary = QLabel(
            "Records Found: 0"
        )

        self.timeline_summary.setStyleSheet("""
            background-color: #FFF7ED;
            border: 1px solid #FED7AA;
            border-radius: 8px;
            padding: 10px;
            color: #9A3412;
            font-weight: bold;
        """)

        # =====================================
        # Timeline Table
        # =====================================

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Time",
            "Operation",
            "Payment",
            "Balance",
            "S/N"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setSortingEnabled(
            True
        )

        # =====================================
        # Layout
        # =====================================

        layout.addWidget(title)

        layout.addLayout(
            filter_layout_1
        )

        layout.addLayout(
            filter_layout_2
        )

        layout.addLayout(
            buttons_layout
        )

        layout.addWidget(
            self.timeline_summary
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(layout)