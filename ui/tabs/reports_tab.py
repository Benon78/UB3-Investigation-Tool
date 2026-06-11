from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFrame,
    QSplitter,
    QRadioButton,
    QButtonGroup
)

from PySide6.QtCore import Qt


class ReportsTab(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            15, 15, 15, 15
        )
        main_layout.setSpacing(8)

        # =====================================
        # TITLE
        # =====================================

        title = QLabel(
            "Reports Center"
        )

        title.setStyleSheet("""
            font-size:18px;
            font-weight:700;
            color:#0F172A;
            padding:2px;
        """)

        # =====================================
        # SPLITTER
        # =====================================

        splitter = QSplitter(
            Qt.Horizontal
        )

        # =====================================
        # LEFT PANEL
        # =====================================

        left_panel = QFrame()

        left_panel.setMaximumWidth(
            320
        )

        left_panel.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:10px;
            }
        """)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(
            15, 15, 15, 15
        )
        left_layout.setSpacing(10)

        report_title = QLabel(
            "Report Builder"
        )

        report_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        # =====================================
        # REPORT TYPES
        # =====================================

        self.executive_report = QRadioButton(
            "Executive Report"
        )

        self.fraud_report = QRadioButton(
            "Fraud Investigation Report"
        )

        self.timeline_report = QRadioButton(
            "Timeline Report"
        )

        self.executive_report.setChecked(
            True
        )

        self.report_group = QButtonGroup()

        self.report_group.addButton(
            self.executive_report
        )

        self.report_group.addButton(
            self.fraud_report
        )

        self.report_group.addButton(
            self.timeline_report
        )

        # =====================================
        # BUTTONS
        # =====================================

        self.preview_btn = QPushButton(
            "Preview Report"
        )

        self.export_report_btn = QPushButton(
            "Export Report (.txt)"
        )

        left_layout.addWidget(
            report_title
        )

        left_layout.addSpacing(5)

        left_layout.addWidget(
            self.executive_report
        )

        left_layout.addWidget(
            self.fraud_report
        )

        left_layout.addWidget(
            self.timeline_report
        )

        left_layout.addSpacing(15)

        left_layout.addWidget(
            self.preview_btn
        )

        left_layout.addWidget(
            self.export_report_btn
        )

        left_layout.addStretch()

        left_panel.setLayout(
            left_layout
        )

        # =====================================
        # RIGHT PANEL
        # =====================================

        right_panel = QFrame()

        right_panel.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:10px;
            }
        """)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(
            15, 15, 15, 15
        )

        preview_title = QLabel(
            "Report Preview"
        )

        preview_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.preview_text = QTextEdit()

        self.preview_text.setReadOnly(
            True
        )

        self.preview_text.setPlaceholderText(
            "Select a report type to preview..."
        )

        right_layout.addWidget(
            preview_title
        )

        right_layout.addWidget(
            self.preview_text
        )

        right_panel.setLayout(
            right_layout
        )

        # =====================================
        # SPLITTER
        # =====================================

        splitter.addWidget(
            left_panel
        )

        splitter.addWidget(
            right_panel
        )

        splitter.setSizes(
            [300, 900]
        )

        # =====================================
        # STATUS BAR
        # =====================================

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setStyleSheet("""
            background:#FFF7ED;
            border:1px solid #FED7AA;
            border-radius:8px;
            padding:8px;
            color:#9A3412;
            font-weight:bold;
        """)

        # =====================================
        # BUILD PAGE
        # =====================================

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            splitter,
            1
        )

        main_layout.addWidget(
            self.status_label
        )

        self.setLayout(
            main_layout
        )