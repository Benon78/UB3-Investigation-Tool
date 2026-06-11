from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from core.resource_path import resource_path


class SplashScreen(QSplashScreen):

    def __init__(self):

        image_path = resource_path(
            "assets/splash/wassha_logo.jpeg"
        )

        pixmap = QPixmap(image_path)

        super().__init__(pixmap)

        self.showMessage(
            "Loading UB3 Analyzer...",
            Qt.AlignBottom | Qt.AlignCenter,
            Qt.white
        )