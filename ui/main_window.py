import os
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QVBoxLayout, QFrame, QApplication,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
     QHeaderView, QScrollArea, QTabWidget, QCheckBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from core.customer_finder import find_customer_recursive
from core.csv_merger import merge_customer_data, export_excel
from core.analysis_session import AnalysisSession

from ui.widgets.dashboard_card import DashboardCard
from ui.tabs.dashboard_tab import DashboardTab
from ui.tabs.search_tab import SearchTab
from ui.tabs.timeline_tab import TimelineTab
from ui.tabs.fraud_tab import FraudTab


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("UB3 Customer Analyzer")
        self.resize(1280, 800)
        self.setMinimumSize(1100, 700)

        self.folder_path = ""
        self.search_btn = None

        self.setStyleSheet(self.styles())
        self.session = AnalysisSession()

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
        self.timeline_tab = TimelineTab()
        self.fraud_tab = FraudTab()

        self.tabs.addTab(self.search_tab, "Search")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.timeline_tab,"Timeline")
        self.tabs.addTab( self.fraud_tab,"Fraud")
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

        QCheckBox {
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }

        QCheckBox::indicator:unchecked {
            border: 2px solid #CBD5E1;
            background: white;
            border-radius: 4px;
        }

        QCheckBox::indicator:checked {
            background: #F58220;
            border: 2px solid #F58220;
            border-radius: 4px;
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

        self.search_tab.results_table.setRowCount(
            len(results)
        )

        total_csv = 0

        for row, result in enumerate(results):

            csv_count = len(
                result["csv_files"]
            )

            total_csv += csv_count

            self.add_checkbox(row)

            self.set_table_item(
                row,
                1,
                result["ub3_folder"]
            )

            self.set_table_item(
                row,
                2,
                result["customer_id"]
            )

            self.set_table_item(
                row,
                3,
                csv_count
            )

            self.set_table_item(
                row,
                4,
                result["id_path"],
                tooltip=True
            )

        self.search_tab.summary_label.setText(
            f"Matches: {len(results)} | CSV Files: {total_csv}"
        )

        self.search_tab.results_table.resizeColumnsToContents()

        self.search_tab.results_table.setColumnWidth(
            0,
            40
        )

        self.search_tab.results_table.setColumnWidth(
            4,
            550
        )

        self.search_tab.results_table.cellClicked.connect(
                self.on_table_click
        )

        self.search_tab.select_all_btn.clicked.connect(
            self.select_all_rows
        )

        self.search_results = results
    
    def analyze_selected(self):

        selected_results = []

        for row in range(
            self.search_tab.results_table.rowCount()
        ):

            checkbox = self.search_tab.results_table.cellWidget(
                row,
                0
            )

            if checkbox and checkbox.isChecked():

                selected_results.append(
                    self.search_results[row]
                )

        if not selected_results:

            self.search_tab.status_label.setText(
                "No UB3 selected"
            )

            return

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

        if df is None or df.empty:
            self.search_tab.status_label.setText(
                "No CSV data found"
            )
            return
        
        self.session.df = df
        self.session.selected_results = selected_results
        self.session.ub3_count = len(
            selected_results
        )
        self.session.record_count = len(df)

        from core.analytics import (
            balance_summary
        )

        from core.fraud import (
            calculate_risk
        )

        balance = balance_summary(df)
        risk_score, flags = calculate_risk(df)

        self.session.balance_summary = balance
        self.session.risk_score = risk_score
        self.session.flags = flags

        self.dashboard_tab.ub3_card.update_value(
            len(selected_results)
        )

        self.dashboard_tab.records_card.update_value(
            len(df)
        )

        self.dashboard_tab.balance_card.update_value(
            balance["current"]
        )

        if risk_score < 20:
            risk_text = "LOW"

        elif risk_score < 50:
            risk_text = "MEDIUM"

        elif risk_score < 80:
            risk_text = "HIGH"

        else:
            risk_text = "CRITICAL"
        
        self.session.risk_level = risk_text

        self.dashboard_tab.risk_card.update_value(
            risk_text
        )

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        exports_folder = os.path.join(
            project_root,
            "exports"
        )

        os.makedirs(
            exports_folder,
            exist_ok=True
        )

        output_file = os.path.join(
            exports_folder,
            f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        export_excel(
            df,
            output_file
        )

        self.search_tab.status_label.setText(
            f"Completed | Records: {len(df)} | Saved: {os.path.basename(output_file)}"
        )

        self.load_timeline()
        self.load_fraud_tab()

    def add_checkbox(self, row):
        checkbox = QCheckBox()

        checkbox.stateChanged.connect(
            self.update_checkbox_selection
        )

        self.search_tab.results_table.setCellWidget(
            row,
            0,
            checkbox
        )

    def select_all_rows(self):

        for row in range(
            self.search_tab.results_table.rowCount()
        ):

            checkbox = self.search_tab.results_table.cellWidget(
                row,
                0
            )

            if checkbox:
                checkbox.setChecked(True)

    def update_checkbox_selection(self):

        selected_count = 0

        table = self.search_tab.results_table

        for row in range(table.rowCount()):

            checkbox = table.cellWidget(row, 0)

            checked = (
                checkbox is not None
                and checkbox.isChecked()
            )

            if checked:
                selected_count += 1

            for col in range(
                table.columnCount()
            ):

                item = table.item(row, col)

                if item:

                    if checked:

                        item.setBackground(
                            QColor("#FFF3E6")
                        )

                    else:

                        item.setBackground(
                            QColor("white")
                        )

        self.search_tab.selection_label.setText(
            f"Selected: {selected_count} UB3(s)"
        )

    def on_table_click(self, row, column):

        if column == 0:
            return

        checkbox = self.search_tab.results_table.cellWidget(
            row,
            0
        )

        if checkbox:

            checkbox.setChecked(
                not checkbox.isChecked()
            )

    def load_timeline(self):

        df = self.session.df

        if df is None:
            return

        timeline_df = df[
            [
                "Date",
                "Time",
                "Operation",
                "Payment",
                "Balance",
                "S/N"
            ]
        ]

        table = self.timeline_tab.table

        table.setRowCount(
            len(timeline_df)
        )

        for row, data in enumerate(
            timeline_df.values
        ):

            for col, value in enumerate(data):

                item = QTableWidgetItem(
                    str(value)
                )

                table.setItem(
                    row,
                    col,
                    item
                )

    def load_fraud_tab(self):

        self.fraud_tab.flags_list.clear()

        self.fraud_tab.risk_label.setText(
            f"Risk Level: {self.session.risk_level}"
        )

        for flag in self.session.flags:

            self.fraud_tab.flags_list.addItem(
                str(flag)
            )










