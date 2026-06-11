import os
from datetime import datetime
import pandas as pd

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QVBoxLayout, QFrame, QApplication,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
     QHeaderView, QScrollArea, QTabWidget, QCheckBox,
     QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon

from core.customer_finder import find_customer_recursive
from core.csv_merger import merge_customer_data, export_excel
from core.analysis_session import AnalysisSession
from core.report_generator import (
    build_executive_report,
    build_fraud_report,
    build_timeline_report,
    build_preview
)
from core.resource_path import resource_path

from ui.widgets.dashboard_card import DashboardCard
from ui.tabs.dashboard_tab import DashboardTab
from ui.tabs.search_tab import SearchTab
from ui.tabs.timeline_tab import TimelineTab
from ui.tabs.fraud_tab import FraudTab
from ui.tabs.about_tab import AboutTab
from ui.tabs.reports_tab import ReportsTab
from ui.tabs.rawdata_tab import RawDataTab
from ui.widgets.sidebar import Sidebar


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WASSHA UB3 Analyzer v1.0.0")
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

        logo = QLabel()
        pixmap = QPixmap(
            resource_path(
                "assets/logos/wassha_logo_white.png"
            )
        )

        logo.setPixmap(
            pixmap.scaledToHeight(
                45,
                Qt.SmoothTransformation
            )
        )
        logo.setMaximumHeight(45)

        title = QLabel(
            "UB3 CUSTOMER ANALYZER"
        )

        title.setObjectName("appTitle")

        # Header setting
        header_layout = QHBoxLayout()
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Sidebar setting
        self.sidebar = Sidebar()
        self.pages = QStackedWidget()

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
        self.reports_tab = ReportsTab()
        self.about_tab = AboutTab()
        self.rawdata_tab = RawDataTab()

        self.pages.addWidget(
            self.search_tab
        )

        self.pages.addWidget(
            self.dashboard_tab
        )

        self.pages.addWidget(
            self.timeline_tab
        )

        self.pages.addWidget(
            self.fraud_tab
        )

        self.pages.addWidget(
            self.rawdata_tab
        )

        self.pages.addWidget(
            self.reports_tab
        )

        self.pages.addWidget(
            self.about_tab
        )

        self.timeline_tab.filter_btn.clicked.connect(
            self.filter_timeline
        )
        self.timeline_tab.filter_btn.clicked.connect(
            self.filter_timeline
        )

        self.timeline_tab.reset_btn.clicked.connect(
            self.reset_timeline_filters
        )

        self.timeline_tab.operation_filter.currentTextChanged.connect(
            self.filter_timeline
        )

        self.timeline_tab.search_input.textChanged.connect(
            self.filter_timeline
        )

        self.sidebar.search_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(0),
                self.activate_sidebar_button(
                    self.sidebar.search_btn
                )
            )
        )

        self.sidebar.dashboard_btn.clicked.connect(
            self.show_dashboard
        )

        self.sidebar.timeline_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(2),
                self.activate_sidebar_button(
                    self.sidebar.timeline_btn
                )
            )
        )

        self.sidebar.fraud_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(3),
                self.activate_sidebar_button(
                    self.sidebar.fraud_btn
                )
            )
        )

        self.sidebar.rawdata_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(4),
                self.activate_sidebar_button(
                    self.sidebar.rawdata_btn
                )
            )
        )

        self.sidebar.reports_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(5),
                self.activate_sidebar_button(
                    self.sidebar.reports_btn
                )
            )
        )

        self.sidebar.about_btn.clicked.connect(
            lambda: (
                self.pages.setCurrentIndex(6),
                self.activate_sidebar_button(
                    self.sidebar.about_btn
                )
            )
        )

        self.rawdata_tab.operation_filter.currentTextChanged.connect(
            self.filter_raw_data
        )

        self.rawdata_tab.search_input.textChanged.connect(
            self.filter_raw_data
        )

        self.rawdata_tab.refresh_btn.clicked.connect(
            self.refresh_raw_data
        )

        self.rawdata_tab.export_btn.clicked.connect(
            self.export_filtered_data
        )

        self.reports_tab.export_report_btn.clicked.connect(
            self.export_report
        )

        self.reports_tab.preview_btn.clicked.connect(
            self.preview_report
        )

        self.reports_tab.executive_report.toggled.connect(
            self.preview_report
        )

        self.reports_tab.fraud_report.toggled.connect(
            self.preview_report
        )

        self.reports_tab.timeline_report.toggled.connect(
            self.preview_report
        )

        main_layout.addLayout(header_layout)
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages, 1)
        main_layout.addLayout(content_layout)

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
            font-size:22px;
            font-weight:700;
            color:#0F172A;
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
            min-height: 85px;
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

        QRadioButton {
            spacing: 8px;
            font-size: 13px;
            color: #1E293B;
        }

        QRadioButton::indicator {
            width: 18px;
            height: 18px;
        }

        QRadioButton::indicator:unchecked {
            border: 2px solid #CBD5E1;
            border-radius: 9px;
            background: white;
        }

        QRadioButton::indicator:checked {
            border: 2px solid #F58220;
            border-radius: 9px;
            background: #F58220;
        }

        QRadioButton:hover {
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

        df, stats = merge_customer_data(
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
        (
            risk_score,
            flags,
            operation_counts,
            risk_matrix,
            suspicious_lanterns,
            suspicious_events,
            verdict
        ) = calculate_risk(df)

        self.session.balance_summary = balance
        self.session.risk_score = risk_score
        self.session.flags = flags
        self.session.operation_counts = operation_counts
        self.session.risk_matrix = risk_matrix
        self.session.suspicious_lanterns = (
            suspicious_lanterns
        )
        self.session.suspicious_events = (
            suspicious_events
        )
        self.session.verdict = verdict
        ops = operation_counts

        self.dashboard_tab.ul_success_card.update_value(
            ops.get("UL.Success", 0)
        )

        self.dashboard_tab.ul_fail_card.update_value(
            ops.get("UL.Fail", 0)
        )

        self.dashboard_tab.p_success_card.update_value(
            ops.get("P.Success", 0)
        )

        self.dashboard_tab.p_fail_card.update_value(
            ops.get("P.Fail", 0)
        )

        self.dashboard_tab.reboot_card.update_value(
            ops.get("F.Reboot", 0)
        )

        self.dashboard_tab.airwatt_card.update_value(
            ops.get("UL.Airwatt short", 0)
        )

        self.dashboard_tab.unique_sn_card.update_value(
            self.count_lanterns(df)
        )

        self.dashboard_tab.days_card.update_value(
            df["Date"].nunique()
        )

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

        # =====================================
        # Customer Summary Panel
        # =====================================

        customer_ids = (
            df["CustomerID"]
            .dropna()
            .astype(str)
            .unique()
        )

        customer_text = ", ".join(
            customer_ids[:5]
        )

        if len(customer_ids) > 5:
            customer_text += " ..."

        self.dashboard_tab.customer_summary.setText(
            f"""
        Customer IDs: {customer_text}
        UB3 Devices: {len(selected_results)}
        Lanterns: {self.count_lanterns(df)}
        Records: {len(df)}
        Activity Days: {df['Date'].nunique()}
        Current Balance: {balance['current']}
        """
        )

        # =====================================
        # Operation Summary Table
        # =====================================

        table = self.dashboard_tab.operations_table

        table.clearContents()

        sorted_ops = sorted(
            ops.items(),
            key=lambda x: x[1],
            reverse=True
        )

        table.setRowCount(
            len(sorted_ops)
        )

        for row, (operation, count) in enumerate(
            sorted_ops
        ):

            table.setItem(
                row,
                0,
                QTableWidgetItem(operation)
            )

            table.setItem(
                row,
                1,
                QTableWidgetItem(str(count))
            )

        table.resizeColumnsToContents()

        # =====================================
        # Investigation Summary
        # =====================================

        top_operation = "N/A"

        if len(sorted_ops) > 0:

            top_operation = (
                f"{sorted_ops[0][0]} "
                f"({sorted_ops[0][1]})"
            )

        self.dashboard_tab.investigation_label.setText(
            f"""
        Risk Level: {risk_text}
        Risk Score: {risk_score}
        Flags Detected: {len(flags)}
        Most Common Operation: {top_operation}

        Merged Files: {stats['merged_files']}
        Failed Files: {stats['failed_files']}
        """
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

        if stats["failed_files"] > 0:

            QMessageBox.warning(
                self,
                "Import Warnings",
                "\n".join(
                    stats["errors"][:10]
                )
            )

        self.search_tab.status_label.setText(
            f"Completed | "
            f"Records: {len(df)} | "
            f"Merged: {stats['merged_files']} | "
            f"Skipped Unlock: {stats['skipped_unlock']} | "
            f"Failed: {stats['failed_files']}"
        )

        self.load_timeline()
        self.load_raw_data()
        self.load_fraud_tab()

        self.pages.setCurrentWidget(
            self.dashboard_tab
        )

        self.activate_sidebar_button(
            self.sidebar.dashboard_btn
        )

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

        if self.session.df is None:
            return

        self.load_timeline_filters()

        timeline_df = self.session.df[
            [
                "Date",
                "Time",
                "Operation",
                "Payment",
                "Balance",
                "S/N"
            ]
        ]

        self.populate_timeline_table(
            timeline_df
        )

        self.timeline_tab.timeline_summary.setText(
            f"Records Found: {len(timeline_df)}"
        )

    def load_fraud_tab(self):

        self.fraud_tab.flags_list.clear()
        self.fraud_tab.actions_list.clear()
        self.fraud_tab.suspicious_lanterns.clear()

        risk_level = self.session.risk_level
        risk_score = self.session.risk_score
        flags = self.session.flags
        ops = self.session.operation_counts
        df = self.session.df

        # =====================================
        # HEADER
        # =====================================

        self.fraud_tab.summary_label.setText(
            f"Risk Level: {risk_level} | "
            f"Risk Score: {risk_score} | "
            f"Records: {self.session.record_count}"
        )

        # =====================================
        # KPI CARDS
        # =====================================

        self.fraud_tab.score_card.update_value(
            risk_score
        )

        self.fraud_tab.level_card.update_value(
            risk_level
        )

        self.fraud_tab.flags_card.update_value(
            len(flags)
        )

        suspicious_ops = (
            ops.get("UL.Fail", 0)
            + ops.get("P.Fail", 0)
            + ops.get("F.Reboot", 0)
            + ops.get("UL.Airwatt short", 0)
            + ops.get("AL.Unlocked", 0)
        )

        self.fraud_tab.operations_card.update_value(
            suspicious_ops
        )

        # =====================================
        # RISK COLOR
        # =====================================

        if risk_level == "LOW":
            color = "#22C55E"

        elif risk_level == "MEDIUM":
            color = "#EAB308"

        elif risk_level == "HIGH":
            color = "#F97316"

        else:
            color = "#DC2626"

        self.fraud_tab.level_card.value_label.setStyleSheet(
            f"""
            font-size:28px;
            font-weight:bold;
            color:{color};
            """
        )

        # =====================================
        # RISK MATRIX
        # =====================================

        matrix = [
            ("UL.Fail", ops.get("UL.Fail", 0)),
            ("P.Fail", ops.get("P.Fail", 0)),
            ("F.Reboot", ops.get("F.Reboot", 0)),
            ("UL.Airwatt short", ops.get("UL.Airwatt short", 0)),
            ("AL.Unlocked", ops.get("AL.Unlocked", 0))
        ]

        table = self.fraud_tab.risk_matrix_table

        table.clearContents()
        table.setRowCount(len(matrix))

        for row, (name, count) in enumerate(matrix):

            table.setItem(
                row,
                0,
                QTableWidgetItem(name)
            )

            table.setItem(
                row,
                1,
                QTableWidgetItem(str(count))
            )

        # =====================================
        # FLAGS
        # =====================================

        if len(flags) == 0:

            self.fraud_tab.flags_list.addItem(
                "🟢 No fraud indicators detected."
            )

        else:

            for flag in flags:

                self.fraud_tab.flags_list.addItem(
                    f"⚠ {flag}"
                )

        # =====================================
        # SUSPICIOUS LANTERNS
        # =====================================

        suspicious_ops_list = [
            "UL.Fail",
            "P.Fail",
            "F.Reboot",
            "UL.Airwatt short",
            "AL.Unlocked"
        ]

        suspicious_df = df[
            df["Operation"].isin(
                suspicious_ops_list
            )
        ]

        if not suspicious_df.empty:

            lanterns = (
                suspicious_df["S/N"]
                .dropna()
                .astype(str)
                .unique()
            )

            for sn in lanterns[:50]:

                self.fraud_tab.suspicious_lanterns.addItem(
                    sn
                )

        else:

            self.fraud_tab.suspicious_lanterns.addItem(
                "No suspicious lanterns"
            )

        # =====================================
        # SUSPICIOUS EVENTS TABLE
        # =====================================

        events_table = (
            self.fraud_tab.suspicious_events_table
        )

        events_table.clearContents()

        if not suspicious_df.empty:

            events_df = suspicious_df[
                [
                    "Date",
                    "Time",
                    "Operation",
                    "S/N"
                ]
            ].head(100)

            events_table.setRowCount(
                len(events_df)
            )

            for row, values in enumerate(
                events_df.values
            ):

                for col, value in enumerate(values):

                    events_table.setItem(
                        row,
                        col,
                        QTableWidgetItem(
                            str(value)
                        )
                    )

        else:

            events_table.setRowCount(0)

        # =====================================
        # INVESTIGATION VERDICT
        # =====================================

        if risk_score >= 80:

            verdict = """
            CRITICAL RISK

            Strong evidence of abnormal activity.

            Immediate field investigation is recommended.

            Review unlock failures, passcode abuse,
            device reboots and low-balance attempts.
            """

        elif risk_score >= 50:

            verdict = """
            HIGH RISK

            Multiple suspicious indicators detected.

            Recommend customer history review and
            hardware verification.
            """

        elif risk_score >= 20:

            verdict = """
            MEDIUM RISK

            Some unusual activity detected.

            Monitor customer activity and review
            high-frequency operations.
            """

        else:

            verdict = """
            LOW RISK

            No significant fraud indicators detected.

            Customer behavior appears normal.
            """

        self.fraud_tab.verdict_label.setText(
            verdict
        )

        # =====================================
        # RECOMMENDED ACTIONS
        # =====================================

        actions = []

        if ops.get("UL.Fail", 0) > 5:

            actions.append(
                "Review repeated unlock failures."
            )

        if ops.get("P.Fail", 0) > 5:

            actions.append(
                "Investigate passcode abuse activity."
            )

        if ops.get("F.Reboot", 0) > 5:

            actions.append(
                "Check hardware stability and firmware."
            )

        if ops.get("UL.Airwatt short", 0) > 5:

            actions.append(
                "Review low balance unlock attempts."
            )

        if len(actions) == 0:

            actions.append(
                "No corrective action required."
            )

        for action in actions:

            self.fraud_tab.actions_list.addItem(
                action
            )

    def filter_timeline(self):

        df = self.session.df

        if df is None or df.empty:
            return

        filtered = df.copy()

        # ==========================
        # Operation Filter
        # ==========================

        operation = (
            self.timeline_tab.operation_filter.currentText()
        )

        if operation != "All Operations":

            filtered = filtered[
                filtered["Operation"] == operation
            ]

        # ==========================
        # Keyword Filter
        # ==========================

        keyword = (
            self.timeline_tab.search_input.text()
            .strip()
            .lower()
        )

        if keyword:

            filtered = filtered[

                filtered["Operation"]
                .astype(str)
                .str.lower()
                .str.contains(
                    keyword,
                    na=False
                )

                |

                filtered["S/N"]
                .astype(str)
                .str.lower()
                .str.contains(
                    keyword,
                    na=False
                )
            ]

        # ==========================
        # Balance Filter
        # ==========================

        min_balance = (
            self.timeline_tab.min_balance.value()
        )

        max_balance = (
            self.timeline_tab.max_balance.value()
        )

        if "Balance" in filtered.columns:

            balance_series = (
                filtered["Balance"]
                .astype(str)
                .str.replace(
                    ",",
                    "",
                    regex=False
                )
            )

            balance_series = balance_series.replace(
                "",
                "0"
            )

            filtered["Balance_Num"] = (
                balance_series.astype(float)
            )

            filtered = filtered[

                (
                    filtered["Balance_Num"]
                    >= min_balance
                )

                &

                (
                    filtered["Balance_Num"]
                    <= max_balance
                )
            ]

        # ==========================
        # Date Filter
        # ==========================

        try:

            from_date = (
                self.timeline_tab.date_from.date()
                .toPython()
            )

            to_date = (
                self.timeline_tab.date_to.date()
                .toPython()
            )

            date_series = (
                filtered["Date"]
                .astype(str)
            )

            parsed_dates = None

            for fmt in [
                "%Y/%m/%d",
                "%Y-%m-%d",
                "%d/%m/%Y"
            ]:

                try:

                    parsed_dates = pd.to_datetime(
                        date_series,
                        format=fmt,
                        errors="coerce"
                    )

                    if parsed_dates.notna().sum() > 0:
                        break

                except:
                    pass

            if parsed_dates is not None:

                filtered = filtered[
                    (
                        parsed_dates.dt.date
                        >= from_date
                    )

                    &

                    (
                        parsed_dates.dt.date
                        <= to_date
                    )
                ]

        except Exception as e:

            print(
                f"Date Filter Error: {e}"
            )

        # ==========================
        # Display Results
        # ==========================

        timeline_df = filtered[
            [
                "Date",
                "Time",
                "Operation",
                "Payment",
                "Balance",
                "S/N"
            ]
        ]

        self.populate_timeline_table(
            timeline_df
        )

        self.timeline_tab.timeline_summary.setText(
            f"Records Found: {len(timeline_df)}"
        )

    def populate_timeline_table(self, timeline_df):

        table = self.timeline_tab.table

        table.setSortingEnabled(False)

        table.clearContents()

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

        table.setSortingEnabled(True)

    def reset_timeline_filters(self):

        if self.session.df is None:
            return

        # Reset Controls

        self.timeline_tab.operation_filter.setCurrentIndex(
            0
        )

        self.timeline_tab.search_input.clear()

        self.timeline_tab.min_balance.setValue(
            0
        )

        self.timeline_tab.max_balance.setValue(
            99999999
        )

        # Reset Dates

        from PySide6.QtCore import QDate

        today = QDate.currentDate()

        self.timeline_tab.date_from.setDate(
            today.addYears(-1)
        )

        self.timeline_tab.date_to.setDate(
            today
        )

        # Reload Original Dataset

        timeline_df = self.session.df[
            [
                "Date",
                "Time",
                "Operation",
                "Payment",
                "Balance",
                "S/N"
            ]
        ]

        self.populate_timeline_table(
            timeline_df
        )

        self.timeline_tab.timeline_summary.setText(
            f"Records Found: {len(timeline_df)}"
        )

    def activate_sidebar_button(self, active_button):

        buttons = [
            self.sidebar.search_btn,
            self.sidebar.dashboard_btn,
            self.sidebar.timeline_btn,
            self.sidebar.fraud_btn,
            self.sidebar.rawdata_btn,
            self.sidebar.reports_btn,
            self.sidebar.about_btn
        ]

        for btn in buttons:
            btn.setChecked(False)

        active_button.setChecked(True)

    def show_dashboard(self):
        self.pages.setCurrentIndex(1)
        self.activate_sidebar_button(
            self.sidebar.dashboard_btn
        )

    def load_timeline_filters(self):

        if self.session.df is None:
            return

        operations = sorted(
            self.session.df["Operation"]
            .dropna()
            .astype(str)
            .unique()
        )

        self.timeline_tab.operation_filter.clear()

        self.timeline_tab.operation_filter.addItem(
            "All Operations"
        )

        self.timeline_tab.operation_filter.addItems(
            operations
        )

    def count_lanterns(self, df):

        valid_models = (
            "AF80",
            "AC20",
            "AC40",
            "AC10",
            "A100",
            "B100",
            "160A"
        )

        serials = (
            df["S/N"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

        lantern_rows = serials[
            serials.str.endswith(
                valid_models,
                na=False
            )
        ]

        self.session.lanterns = lantern_rows.tolist()

        return len(lantern_rows)

    def load_raw_data(self):

        if self.session.df is None:
            return

        df = self.session.df.copy()

        table = self.rawdata_tab.table

        table.clear()

        table.setColumnCount(
            len(df.columns)
        )

        table.setHorizontalHeaderLabels(
            list(df.columns)
        )

        table.setRowCount(
            len(df)
        )

        for row in range(len(df)):

            for col in range(len(df.columns)):

                value = str(
                    df.iloc[row, col]
                )

                item = QTableWidgetItem(
                    value
                )

                item.setToolTip(
                    value
                )

                table.setItem(
                    row,
                    col,
                    item
                )

        table.resizeColumnsToContents()

        self.rawdata_tab.summary_label.setText(
            f"Records Loaded: {len(df):,}"
        )

        self.load_raw_filters()

    def load_raw_filters(self):

        if self.session.df is None:
            return

        operations = sorted(
            self.session.df["Operation"]
            .dropna()
            .astype(str)
            .unique()
        )

        self.rawdata_tab.operation_filter.clear()

        self.rawdata_tab.operation_filter.addItem(
            "All Operations"
        )

        self.rawdata_tab.operation_filter.addItems(
            operations
        )

    def filter_raw_data(self):

        if self.session.df is None:
            return

        df = self.session.df.copy()

        operation = (
            self.rawdata_tab.operation_filter.currentText()
        )

        if operation != "All Operations":

            df = df[
                df["Operation"] == operation
            ]

        keyword = (
            self.rawdata_tab.search_input.text()
            .strip()
            .lower()
        )

        if keyword:

            mask = df.astype(str).apply(
                lambda x:
                x.str.lower().str.contains(
                    keyword,
                    na=False
                )
            )

            df = df[
                mask.any(axis=1)
            ]

        table = self.rawdata_tab.table

        table.setRowCount(
            len(df)
        )

        for row in range(len(df)):

            for col in range(len(df.columns)):

                item = QTableWidgetItem(
                    str(
                        df.iloc[row, col]
                    )
                )

                table.setItem(
                    row,
                    col,
                    item
                )

        self.rawdata_tab.summary_label.setText(
            f"Records Loaded: {len(df):,}"
        )

        table.resizeColumnsToContents()

    def refresh_raw_data(self):

        self.load_raw_data()

        self.rawdata_tab.search_input.clear()

        self.rawdata_tab.operation_filter.setCurrentIndex(
            0
        )

    def export_filtered_data(self):

        if self.session.df is None:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export Filtered Data",
            "filtered_data.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not file_name:
            return

        operation = (
            self.rawdata_tab.operation_filter.currentText()
        )

        keyword = (
            self.rawdata_tab.search_input.text()
            .strip()
            .lower()
        )

        df = self.session.df.copy()

        # ==========================
        # Operation Filter
        # ==========================

        if operation != "All Operations":

            df = df[
                df["Operation"] == operation
            ]

        # ==========================
        # Keyword Filter
        # ==========================

        if keyword:

            mask = df.astype(str).apply(
                lambda x:
                x.str.lower().str.contains(
                    keyword,
                    na=False
                )
            )

            df = df[
                mask.any(axis=1)
            ]

        # ==========================
        # No Data
        # ==========================

        if df.empty:

            self.rawdata_tab.summary_label.setText(
                "No records to export"
            )

            return

        # ==========================
        # Export Using Central Engine
        # ==========================

        export_excel(
            df,
            file_name
        )

        self.rawdata_tab.summary_label.setText(
            f"Exported {len(df):,} records"
        )

    def generate_report(self):

        if self.session.df is None:

            QMessageBox.warning(
                self,
                "No Data",
                "Run analysis first."
            )

            return

        report_folder = os.path.join(
            os.getcwd(),
            "reports"
        )

        os.makedirs(
            report_folder,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        generated = []

        # =====================================
        # Executive Report
        # =====================================

        if self.reports_tab.executive_report.isChecked():

            report = build_executive_report(
                self.session
            )

            file_path = os.path.join(
                report_folder,
                f"Executive_Report_{timestamp}.txt"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(report)

            generated.append(
                os.path.basename(file_path)
            )

        # =====================================
        # Fraud Report
        # =====================================

        if self.reports_tab.fraud_report.isChecked():

            report = build_fraud_report(
                self.session
            )

            file_path = os.path.join(
                report_folder,
                f"Fraud_Report_{timestamp}.txt"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(report)

            generated.append(
                os.path.basename(file_path)
            )

        # =====================================
        # Timeline Report
        # =====================================

        if self.reports_tab.timeline_report.isChecked():

            report = build_timeline_report(
                self.session
            )

            file_path = os.path.join(
                report_folder,
                f"Timeline_Report_{timestamp}.txt"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(report)

            generated.append(
                os.path.basename(file_path)
            )

        # =====================================
        # No Selection
        # =====================================

        if len(generated) == 0:

            QMessageBox.warning(
                self,
                "Reports",
                "Select at least one report."
            )

            return

        QMessageBox.information(
            self,
            "Reports Generated",
            "\n".join(generated)
        )

    def preview_report(self):

        self.reports_tab.preview_text.clear()

        report_type = self.get_selected_report_type()

        if report_type is None:
            return

        if self.session.df is None:

            QMessageBox.warning(
                self,
                "No Analysis",
                "Run analysis first."
            )

            return

        preview = build_preview(
            self.session
        )

        self.reports_tab.preview_text.setText(
            preview
        )

        self.reports_tab.status_label.setText(
            f"Preview Loaded: {report_type.title()} Report"
        )

    def export_report(self):

        if self.session.df is None:

            QMessageBox.warning(
                self,
                "No Analysis",
                "Run analysis first."
            )

            return

        report_text = ""

        if self.reports_tab.executive_report.isChecked():

            report_text += (
                build_executive_report(
                    self.session
                )
                + "\n\n"
            )

        if self.reports_tab.fraud_report.isChecked():

            report_text += (
                build_fraud_report(
                    self.session
                )
                + "\n\n"
            )

        if self.reports_tab.timeline_report.isChecked():

            report_text += (
                build_timeline_report(
                    self.session
                )
                + "\n\n"
            )

        if not report_text:

            QMessageBox.warning(
                self,
                "No Report Selected",
                "Select at least one report."
            )

            return

        reports_folder = os.path.join(
            os.getcwd(),
            "reports"
        )

        os.makedirs(
            reports_folder,
            exist_ok=True
        )

        customer = "UNKNOWN"

        if self.session.selected_results:

            customer = (
                self.session.selected_results[0]
                .get("customer_id", "UNKNOWN")
            )

            file_path = os.path.join(
                reports_folder,
                f"report_{customer}_{self.session.risk_level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                report_text
            )

        QMessageBox.information(
            self,
            "Report Generated",
            f"Saved:\n{file_path}"
        )

    def get_selected_report_type(self):

        if self.reports_tab.executive_report.isChecked():
            return "executive"

        if self.reports_tab.fraud_report.isChecked():
            return "fraud"

        if self.reports_tab.timeline_report.isChecked():
            return "timeline"

        return None
