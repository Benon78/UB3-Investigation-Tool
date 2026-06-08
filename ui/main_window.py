import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QVBoxLayout, QFrame, QApplication,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)
from PySide6.QtCore import Qt
from core.customer_finder import find_customer_recursive
from core.csv_merger import merge_customer_data, export_excel


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("UB3 Customer Analyzer")
        self.resize(1280, 800)
        self.setMinimumSize(1100, 700)

        self.folder_path = ""
        self.search_btn = None

        self.setStyleSheet(self.styles())

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("UB3 CUSTOMER ANALYZER")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Card container
        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)

        # Folder
        self.folder_label = QLabel("Root Folder: Not selected")
        self.folder_label.setStyleSheet("""
            color: #F58220;
            font-weight: bold;
            background-color: #FFF7ED;
            padding: 8px;
            border-radius: 6px;
        """)

        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.select_folder)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #0F172A;
            font-weight: bold;
            background-color: #FFF7ED;
            padding: 8px;
            border-radius: 6px;
        """)

        # Customer ID input
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Enter Customer ID e.g. 33883")

        # Search button
        self.search_btn = QPushButton("Find Customer")
        self.search_btn.setObjectName("primaryBtn")
        self.search_btn.clicked.connect(self.search_customer)
        self.search_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.setCursor(Qt.PointingHandCursor)

        # Analyze button
        buttons_layout = QHBoxLayout()
        self.analyze_selected_btn = QPushButton(
            "Analyze Selected"
        )

        self.analyze_all_btn = QPushButton(
            "Analyze All"
        )

        buttons_layout.addWidget(
            self.analyze_selected_btn
        )

        buttons_layout.addWidget(
            self.analyze_all_btn
        )
        self.analyze_all_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_selected_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.setCursor(Qt.PointingHandCursor)

        self.analyze_selected_btn.clicked.connect(
            self.analyze_selected
        )

        self.analyze_all_btn.clicked.connect(
            self.analyze_all
        )

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setMinimumHeight(350)

        self.results_table.setHorizontalHeaderLabels([
            "UB3 Serial Number",
            "Customer ID",
            "CSV Files",
            "Folder Path"
        ])

        self.results_table.setAlternatingRowColors(True)
        self.results_table.setShowGrid(False)
        self.results_table.setSortingEnabled(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(35)

        self.results_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.results_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.results_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.results_table.setSelectionMode(
            QTableWidget.MultiSelection
        )

        header = self.results_table.horizontalHeader()

        header.setStretchLastSection(True)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        # Summary Label
        self.summary_label = QLabel(
            "Matches: 0 | CSV Files: 0"
        )

        card_layout.addWidget(self.folder_label)
        card_layout.addWidget(browse_btn)
        card_layout.addWidget(self.customer_input)
        card_layout.addWidget(self.search_btn)
        card_layout.addWidget(
            self.results_table,
            stretch=1
        )
        # card_layout.addWidget(self.analyze_btn)
        card_layout.addWidget(self.summary_label)
        card_layout.addWidget(self.status_label)
        card_layout.addLayout(buttons_layout)

        card.setLayout(card_layout)

        main_layout.addWidget(title)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Root Folder"
        )

        if folder:
            self.folder_path = folder
            self.folder_label.setText(f"Root Folder: {folder}")

    def styles(self):
        return """
        QWidget {
            background-color: #F8F9FA;
            font-family: Segoe UI;
            font-size: 14px;
            color: #111827;
        }

        #title {
            font-size: 24px;
            font-weight: bold;
            color: #0F172A;
            margin-bottom: 10px;
        }

        #card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #E5E7EB;
        }

        QLabel {
            color: #111827;
            font-weight: 500;
        }

        QLineEdit {
            padding: 12px;
            border: 2px solid #D1D5DB;
            border-radius: 8px;
            color: #000000;
            background-color: white;
        }

        QLineEdit:focus {
            border: 2px solid #F58220;
        }

        QPushButton {
            background-color: #F58220;
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
            min-height: 18px;
        }

        QPushButton:hover {
            background-color: #E67310;
        }

        QPushButton:pressed {
            background-color: #D46008;
        }

        QTableWidget {
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            alternate-background-color: #F9FAFB;
            selection-background-color: #F58220;
            selection-color: white;
            gridline-color: transparent;
            padding: 5px;
        }

        QHeaderView::section {
            background-color: #0F172A;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px;
            min-height: 35px;
        }

        QTableCornerButton::section {
            background-color: #0F172A;
            border: none;
        }

        QScrollBar:vertical {
            width: 10px;
            border: none;
        }

        QScrollBar::handle:vertical {
            background: #CBD5E1;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #94A3B8;
        }
        """

    def set_table_item(self, row, col, value, tooltip=False):

        item = QTableWidgetItem(str(value))

        item.setTextAlignment(
            Qt.AlignCenter
        )

        if tooltip:
            item.setToolTip(str(value))

        self.results_table.setItem(
            row,
            col,
            item
        )

    def search_customer(self):

        customer_id = self.customer_input.text().strip()

        if not self.folder_path or not customer_id:
            self.folder_label.setText("Select folder and enter Customer ID")
            return

        results = find_customer_recursive(self.folder_path, customer_id)

        if not results:
            self.folder_label.setText("No customer found")
            return

        self.results_table.setRowCount(
            len(results)
        )

        total_csv = 0

        for row, result in enumerate(results):

            csv_count = len(
                result["csv_files"]
            )

            total_csv += csv_count

            self.set_table_item(
                row,
                0,
                result["ub3_folder"]
            )

            self.set_table_item(
                row,
                1,
                result["customer_id"]
            )

            self.set_table_item(
                row,
                2,
                csv_count
            )

            self.set_table_item(
                row,
                3,
                result["id_path"],
                tooltip=True
            )

        self.summary_label.setText(
            f"Matches: {len(results)} | CSV Files: {total_csv}"
        )

        # self.results_table.resizeRowsToContents()

        self.results_table.resizeColumnsToContents()

        self.results_table.setColumnWidth(
            3,
            550
        )

        self.search_results = results
    
    def analyze_selected(self):
        selected_rows = set()

        for item in self.results_table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            self.status_label.setText(
                "No rows selected"
            )
            return

        selected_results = []

        for row in selected_rows:
            selected_results.append(
                self.search_results[row]
            )

        self.run_analysis(
            selected_results
        )
    
    def analyze_all(self):

        if not self.search_results:
            return

        self.run_analysis(
            self.search_results
        )

    def run_analysis(self, selected_results):

        self.status_label.setText(
            "Analyzing..."
        )

        QApplication.processEvents()

        df = merge_customer_data(
            selected_results
        )

        if df is None:

            self.status_label.setText(
                "No CSV data found"
            )

            return

        output_file = os.path.join(
            self.folder_path,
            f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        export_excel(
            df,
            output_file
        )

        self.status_label.setText(
            f"Completed | Records: {len(df)}"
        )

