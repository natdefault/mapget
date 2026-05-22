from PySide6.QtWidgets import QComboBox


class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(False)
