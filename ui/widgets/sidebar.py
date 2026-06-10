from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame
)

from PySide6.QtCore import Qt


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(240)

        self.setStyleSheet("""
            QWidget { 
                background:#0F172A; 
            }

            QLabel {
                color: white; 
                font-size: 20px; 
                font-weight: bold; 
                padding: 15px;
            }

            #sidebarSubtitle {
                color: #94A3B8;
                font-size: 11px;
                padding-bottom: 10px;
            }

            QPushButton {
                background: #1E293B;
                color: #E2E8F0;
                text-align: left;
                padding: 14px;
                border: none;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
            }

            QPushButton:hover {
                background: #1E293B;
                color: white;
            }

            QPushButton:checked {
                background: #F58220;
                color: white;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        subtitle = QLabel("Investigation Platform")
        subtitle.setObjectName("sidebarSubtitle")

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)

        self.search_btn = QPushButton(
            "🔍 Search Center"
        )

        self.dashboard_btn = QPushButton(
            "📊 Dashboard"
        )

        self.timeline_btn = QPushButton(
            "📅 Timeline"
        )

        self.fraud_btn = QPushButton(
            "🛡 Fraud Center"
        )

        self.rawdata_btn = QPushButton(
            "📂 Data Explorer"
        )

        self.reports_btn = QPushButton(
            "📄 Reports"
        )

        self.about_btn = QPushButton(
            "ℹ About"
        )

        buttons = [
            self.search_btn,
            self.dashboard_btn,
            self.timeline_btn,
            self.fraud_btn,
            self.rawdata_btn,
            self.reports_btn,
            self.about_btn
        ]

        for btn in buttons:
            btn.setCheckable(True)
            layout.addWidget(btn)

        self.search_btn.setChecked(True)

        layout.insertWidget(0, subtitle)
        layout.insertWidget(1, divider)

        layout.addStretch()

        version = QLabel(
            "v0.6.0"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        version.setStyleSheet("""
            color:#64748B;
            font-size:11px;
        """)

        layout.addWidget(version)

        self.setLayout(layout)