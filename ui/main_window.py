import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QVBoxLayout, QFrame, QApplication,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt
from core.customer_finder import find_customer_recursive
from core.csv_merger import merge_customer_data, export_excel
from ui.widgets.dashboard_card import DashboardCard

from ui.tabs.dashboard_tab import DashboardTab
from ui.tabs.search_tab import SearchTab


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
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        title = QLabel("UB3 CUSTOMER ANALYZER")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignCenter)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")

        # Search tab
        self.search_tab = SearchTab()

        self.search_tab.browse_btn.clicked.connect(
            self.select_folder
        )

        self.search_tab.search_btn.clicked.connect(
            self.search_customer
        )

        self.search_tab.analyze_selected_btn.clicked.connect(
            self.analyze_selected
        )

        self.search_tab.analyze_all_btn.clicked.connect(
            self.analyze_all
        )

        # Dashboard tab
        self.dashboard_tab = DashboardTab()

        self.tabs.addTab(self.search_tab, "Search")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(QWidget(), "Timeline")
        self.tabs.addTab(QWidget(), "Fraud")
        self.tabs.addTab(QWidget(), "Raw Data")
        self.tabs.addTab(QWidget(), "Export")

        main_layout.addWidget(title)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Root Folder"
        )

        if folder:
            self.folder_path = folder
            self.search_tab.folder_label.setText(f"Root Folder: {folder}")

    def styles(self):
        return """
        
        QWidget {
            background: #F5F7FA;
            color: #1E293B;
            font-family: Segoe UI;
            font-size: 13px;
        }

        QLabel {
            color: #1E293B;
        }

        #appTitle {
            font-size: 28px;
            font-weight: 700;
            color: #0F172A;
            padding: 10px;
        }

        QTabWidget::pane {
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            background: white;
            top: -1px;
        }

        QTabBar::tab {
            background: #E5E7EB;
            color: #475569;
            min-width: 130px;
            padding: 12px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
        }

        QTabBar::tab:selected {
            background: #F58220;
            color: white;
            font-weight: bold;
        }

        QTabBar::tab:hover {
            background: #FDBA74;
            color: #111827;
        }

        QPushButton {
            background: #F58220;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }

        QPushButton:hover {
            background: #EA6D0B;
        }

        QPushButton:pressed {
            background: #C85600;
        }

        QLineEdit {
            border: 2px solid #CBD5E1;
            border-radius: 8px;
            padding: 10px;
            background: white;
        }

        QLineEdit:focus {
            border: 2px solid #F58220;
        }

        QTableWidget {
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            background: white;
            alternate-background-color: #F8FAFC;
            selection-background-color: #F58220;
            selection-color: white;
        }

        QHeaderView::section {
            background: #0F172A;
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }

        QScrollBar:vertical {
            width: 10px;
            background: transparent;
        }

        QScrollBar::handle:vertical {
            background: #CBD5E1;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #94A3B8;
        }

        #dashboardCard {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            min-height: 110px;
        }

        #cardValue {
            font-size: 26px;
            font-weight: bold;
            color: #F58220;
        }
        """

    def set_table_item(self, row, col, value, tooltip=False):

        item = QTableWidgetItem(str(value))

        item.setTextAlignment(
            Qt.AlignCenter
        )

        if tooltip:
            item.setToolTip(str(value))

        self.search_tab.results_table.setItem(
            row,
            col,
            item
        )

    def search_customer(self):

        customer_id = self.search_tab.customer_input.text().strip()

        if not self.folder_path or not customer_id:
            self.search_tab.folder_label.setText("Select folder and enter Customer ID")
            return

        results = find_customer_recursive(self.folder_path, customer_id)

        if not results:
            self.search_tab.folder_label.setText("No customer found")
            return

        self.self.search_tab.results_table.setRowCount(
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

        self.search_tab.summary_label.setText(
            f"Matches: {len(results)} | CSV Files: {total_csv}"
        )

        self.search_tab.results_table.resizeRowsToContents()

        self.search_tab.results_table.resizeColumnsToContents()

        self.search_tab.results_table.setColumnWidth(
            3,
            550
        )

        self.search_results = results
    
    def analyze_selected(self):
        selected_rows = set()

        for item in self.search_tab.results_table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            self.search_tab.status_label.setText(
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

        self.search_tab.status_label.setText(
            "Analyzing..."
        )

        QApplication.processEvents()

        df = merge_customer_data(
            selected_results
        )

        from core.analytics import (
            balance_summary
        )

        from core.fraud import (
            calculate_risk
        )

        balance = balance_summary(df)

        risk_score, flags = calculate_risk(df)

        self.ub3_card.update_value(
            len(selected_results)
        )

        self.records_card.update_value(
            len(df)
        )

        self.balance_card.update_value(
            balance["current"]
        )

        if risk_score <= 20:
            risk_text = "LOW"

        elif risk_score <= 50:
            risk_text = "MEDIUM"

        else:
            risk_text = "HIGH"

        self.risk_card.update_value(
            risk_text
        )
        
        if df is None:

            self.search_tab.status_label.setText(
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

        self.search_tab.status_label.setText(
            f"Completed | Records: {len(df)}"
        )

