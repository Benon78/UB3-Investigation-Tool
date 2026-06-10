import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from PySide6.QtGui import QIcon

from ui.splash_screen import SplashScreen

app = QApplication(sys.argv)
app.setWindowIcon(
    QIcon("assets/icons/app.ico")
)

splash = SplashScreen()
splash.show()
app.processEvents()

window = MainWindow()
window.show()

splash.finish(window)

app.exec()