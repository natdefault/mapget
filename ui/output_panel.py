from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class OutputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QTextEdit())
        self.setLayout(layout)
