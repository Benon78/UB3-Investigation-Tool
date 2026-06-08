import os
from datetime import datetime
import pandas as pd

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QFileDialog, QVBoxLayout, QFrame, QApplication,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
     QHeaderView, QScrollArea, QTabWidget, QCheckBox
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

        self.timeline_tab.filter_btn.clicked.connect(
            self.filter_timeline
        )
        self.timeline_tab.filter_btn.clicked.connect(
            self.filter_timeline
        )

        self.timeline_tab.reset_btn.clicked.connect(
            self.reset_timeline_filters
        )

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
        risk_score, flags, operation_counts = calculate_risk(df)

        self.session.balance_summary = balance
        self.session.risk_score = risk_score
        self.session.flags = flags
        self.session.operation_counts = (
            operation_counts
        )
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
            df["S/N"].nunique()
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
        self.tabs.setCurrentWidget(
            self.fraud_tab
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

        risk_level = self.session.risk_level
        risk_score = self.session.risk_score

        ops = self.session.operation_counts

        # =====================================
        # Summary Banner
        # =====================================

        self.fraud_tab.summary_label.setText(
            f"Risk Level: {risk_level} | "
            f"Flags: {len(self.session.flags)} | "
            f"Records: {self.session.record_count}"
        )

        self.fraud_tab.summary_details.setText(
            f"""
            Risk Score: {risk_score}
            Risk Level: {risk_level}

            Records Analyzed: {self.session.record_count}

            Flags Detected: {len(self.session.flags)}

            Recommendation: Review Alerts, Operations and Recommendations tabs for detailed investigation results.
            """
                )

        # =====================================
        # Dashboard Cards
        # =====================================

        self.fraud_tab.score_card.update_value(
            risk_score
        )

        self.fraud_tab.level_card.update_value(
            risk_level
        )

        self.fraud_tab.flags_card.update_value(
            len(self.session.flags)
        )

        # =====================================
        # Risk Colors
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
            font-size: 28px;
            font-weight: bold;
            color: {color};
            """
        )

        # =====================================
        # Alerts
        # =====================================

        suspicious_count = len(
            self.session.flags
        )

        self.fraud_tab.operations_card.update_value(
            suspicious_count
        )

        if suspicious_count == 0:

            self.fraud_tab.flags_list.addItem(
                "🟢 No alerts detected"
            )

        else:

            for flag in self.session.flags:

                self.fraud_tab.flags_list.addItem(
                    f"⚠ {flag}"
                )

        # =====================================
        # Operations Table
        # =====================================

        table = self.fraud_tab.operations_table

        table.clearContents()

        table.setRowCount(
            len(ops)
        )

        sorted_ops = sorted(
            ops.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for row, (operation, count) in enumerate(
            sorted_ops
        ):

            op_item = QTableWidgetItem(
                operation
            )

            count_item = QTableWidgetItem(
                str(count)
            )

            if operation in [
                "UL.Fail",
                "P.Fail",
                "F.Reboot",
                "UL.Airwatt short",
                "AL.Unlocked"
            ]:

                op_item.setBackground(
                    QColor("#FFE5E5")
                )

                count_item.setBackground(
                    QColor("#FFE5E5")
                )

            table.setItem(
                row,
                0,
                op_item
            )

            table.setItem(
                row,
                1,
                count_item
            )

        table.resizeColumnsToContents()

        # =====================================
        # Recommendations
        # =====================================

        actions = []

        ul_fail = ops.get(
            "UL.Fail",
            0
        )

        p_fail = ops.get(
            "P.Fail",
            0
        )

        reboot = ops.get(
            "F.Reboot",
            0
        )

        airwatt_short = ops.get(
            "UL.Airwatt short",
            0
        )

        if ul_fail > 20:

            actions.append(
                f"🔴 Critical: {ul_fail} unlock failures detected. Immediate investigation required."
            )

        elif ul_fail > 5:

            actions.append(
                f"🟠 Review unlock failures ({ul_fail})."
            )

        if p_fail > 10:

            actions.append(
                f"🔴 Review passcode abuse activity ({p_fail} failures)."
            )

        if reboot > 10:

            actions.append(
                f"🟠 Device rebooted {reboot} times. Check hardware stability."
            )

        if airwatt_short > 5:

            actions.append(
                f"🟡 Low balance unlock attempts detected."
            )

        if len(actions) == 0:

            actions.append(
                "🟢 No suspicious activity detected."
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


