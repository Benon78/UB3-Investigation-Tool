from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PySide6.QtCore import Qt


class AboutTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(
            20, 20, 20, 20
        )

        title = QLabel(
            "WASSHA UB3 Analyzer"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#0F172A;
        """)

        version = QLabel(
            "Version 1.0.0"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        version.setStyleSheet("""
            color:#64748B;
            font-size:14px;
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

        info = QLabel("""
            Developed For

            WASSHA Hardware Investigation Team

            Modules:
            ✓ Customer Search
            ✓ Multi-UB3 Analysis
            ✓ Dashboard Analytics
            ✓ Timeline Investigation
            ✓ Fraud Detection
            ✓ Risk Assessment
            ✓ Data Explorer
            ✓ Reporting Center

            Developer:
            Benjamin William
        """)

        info.setStyleSheet("""
            font-size:14px;
            line-height:20px;
        """)

        card_layout.addWidget(info)

        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addSpacing(10)
        layout.addWidget(card)
        layout.addStretch()

        self.setLayout(layout)