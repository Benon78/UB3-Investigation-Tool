from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QCheckBox,
    QPushButton,
    QFrame
)


class ReportsTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(
            20,20,20,20
        )

        title = QLabel(
            "Reports Center"
        )

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#0F172A;
        """)

        card = QFrame()

        card.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #E2E8F0;
                border-radius:12px;
                padding:15px;
            }
        """)

        card_layout = QVBoxLayout()

        card_layout.addWidget(
            QLabel("Report Types")
        )

        self.executive_report = QCheckBox(
            "Executive Report"
        )

        self.fraud_report = QCheckBox(
            "Fraud Investigation Report"
        )

        self.timeline_report = QCheckBox(
            "Timeline Report"
        )

        self.generate_pdf_btn = QPushButton(
            "Generate PDF"
        )

        self.generate_excel_btn = QPushButton(
            "Generate Excel"
        )

        card_layout.addWidget(
            self.executive_report
        )

        card_layout.addWidget(
            self.fraud_report
        )

        card_layout.addWidget(
            self.timeline_report
        )

        card_layout.addSpacing(15)

        card_layout.addWidget(
            self.generate_pdf_btn
        )

        card_layout.addWidget(
            self.generate_excel_btn
        )

        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(card)
        layout.addStretch()

        self.setLayout(layout)