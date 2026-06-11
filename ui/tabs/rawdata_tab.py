from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class RawDataTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(
            20, 20, 20, 20
        )

        layout.setSpacing(15)

        # ==========================
        # TITLE
        # ==========================

        title = QLabel(
            "Raw Data Explorer"
        )

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#0F172A;
        """)

        # ==========================
        # FILTER BAR
        # ==========================

        filter_layout = QHBoxLayout()

        self.operation_filter = QComboBox()
        self.operation_filter.addItem(
            "All Operations"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search S/N, Customer, Operation..."
        )

        self.refresh_btn = QPushButton(
            "Refresh"
        )

        self.export_btn = QPushButton(
            "Export Filtered"
        )

        filter_layout.addWidget(
            QLabel("Operation")
        )

        filter_layout.addWidget(
            self.operation_filter
        )

        filter_layout.addWidget(
            self.search_input
        )

        filter_layout.addWidget(
            self.refresh_btn
        )

        filter_layout.addWidget(
            self.export_btn
        )

        # ==========================
        # SUMMARY
        # ==========================

        self.summary_label = QLabel(
            "Records Loaded: 0"
        )

        self.summary_label.setStyleSheet("""
            background:#EFF6FF;
            border:1px solid #BFDBFE;
            border-radius:8px;
            padding:10px;
            font-weight:bold;
        """)

        # ==========================
        # TABLE
        # ==========================

        self.table = QTableWidget()

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setSortingEnabled(
            True
        )

        # Horizontal scroll enabled
        self.table.setHorizontalScrollMode(
            QTableWidget.ScrollPerPixel
        )

        # Better column sizing
        self.table.horizontalHeader().setStretchLastSection(
            False
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self.table.setWordWrap(False)

        # ==========================
        # BUILD
        # ==========================

        layout.addWidget(title)
        layout.addLayout(filter_layout)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.table)

        self.setLayout(layout)