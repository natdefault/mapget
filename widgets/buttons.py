from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class PrimaryButton(QPushButton):
    def __init__(self, label="", parent=None):
        super().__init__(label, parent)
        self.setCursor(Qt.PointingHandCursor)
