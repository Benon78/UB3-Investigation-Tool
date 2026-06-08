from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QAbstractItemView,
    QCheckBox
)

from PySide6.QtCore import Qt


class SearchTab(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Customer Search")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #0F172A;
        """)

        self.folder_label = QLabel(
            "Root Folder: Not Selected"
        )

        self.browse_btn = QPushButton(
            "Browse Folder"
        )

        self.customer_input = QLineEdit()

        self.customer_input.setPlaceholderText(
            "Enter Customer ID"
        )

        search_layout = QHBoxLayout()

        self.search_btn = QPushButton(
            "Find Customer"
        )

        search_layout.addWidget(
            self.customer_input
        )

        search_layout.addWidget(
            self.search_btn
        )

        self.summary_label = QLabel(
            "Matches: 0 | CSV Files: 0"
        )

        self.results_table = QTableWidget()

        self.results_table.setColumnCount(5)

        self.results_table.setHorizontalHeaderLabels([
            "",
            "UB3",
            "Customer ID",
            "CSV Files",
            "Folder Path"
        ])

        self.results_table.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        self.results_table.setMinimumHeight(350)

        self.results_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.results_table.setSelectionMode(
            QAbstractItemView.MultiSelection
        )

        self.selection_label = QLabel(
            "Selected: 0 UB3(s)"
        )

        # self.results_table.cellClicked.connect(
        #     self.on_table_click
        # )

        button_layout = QHBoxLayout()

        self.analyze_selected_btn = QPushButton(
            "Analyze Selected"
        )

        self.analyze_all_btn = QPushButton(
            "Analyze All"
        )

        self.select_all_btn = QPushButton(
            "Select All"
        )

        button_layout.addWidget(
            self.select_all_btn
        )

        button_layout.addWidget(
            self.analyze_selected_btn
        )

        button_layout.addWidget(
            self.analyze_all_btn
        )

        self.status_label = QLabel(
            "Ready"
        )

        layout.addWidget(title)

        layout.addWidget(
            self.folder_label
        )

        layout.addWidget(
            self.browse_btn
        )

        layout.addLayout(
            search_layout
        )

        layout.addWidget(
            self.summary_label
        )

        layout.addWidget(
            self.results_table
        )

        layout.addWidget(
            self.selection_label
        )

        layout.addLayout(
            button_layout
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(layout)
