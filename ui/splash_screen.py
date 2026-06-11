from PySide6.QtWidgets import (
    QSplashScreen
)

from PySide6.QtGui import (
    QPixmap
)

from PySide6.QtCore import Qt


class SplashScreen(QSplashScreen):

    def __init__(self):

        pixmap = QPixmap(
            "assets/splash/splash_v1.png"
        )

        super().__init__(pixmap)

        self.showMessage(
            "Loading UB3 Analyzer...",
            Qt.AlignBottom | Qt.AlignCenter,
            Qt.white
        )