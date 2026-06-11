import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.resource_path import resource_path
from ui.splash_screen import SplashScreen
from ui.main_window import MainWindow

app = QApplication(sys.argv)

app.setWindowIcon(
    QIcon(
        resource_path(
            "assets/icons/app.ico"
        )
    )
)

splash = SplashScreen()
splash.show()

app.processEvents()

window = MainWindow()

window.setWindowIcon(
    QIcon(
        resource_path(
            "assets/icons/app.ico"
        )
    )
)

window.show()

splash.finish(window)

sys.exit(app.exec())