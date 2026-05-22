import sys

from PySide6.QtWidgets import QApplication
from window import AppWindow


def main():
    qt_app = QApplication(sys.argv)

    window = AppWindow()
    window.show()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()