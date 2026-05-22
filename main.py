from PySide6.QtWidgets import QApplication
from window import AppWindow

import sys

app = QApplication(sys.argv)

window = AppWindow()
window.show()

sys.exit(app.exec())