THEME = """
QWidget {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #eef4fb, stop:1 #d9e3f2);
    color: #1f2b3d;
    font-family: Segoe UI;
    font-size: 12px;
}

QFrame#mainPanel {
    background-color: rgba(255, 255, 255, 0.88);
    border: 1px solid #9ab3d6;
}

QLabel {
    color: #1f2b3d;
}

QLineEdit,
QTextEdit,
QComboBox {
    background-color: #ffffff;
    border: 1px solid #a7bdd7;
    color: #1f2b3d;
    padding: 5px;
    selection-background-color: #8aa7d9;
}

QTextEdit {
    padding: 6px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #1f2b3d;
    margin-right: 6px;
}

QPushButton {
    background-color: #dce6f6;
    border: 1px solid #8aa7d9;
    color: #1f2b3d;
    padding: 6px 14px;
}

QPushButton:hover {
    background-color: #c3d4ee;
}

QPushButton:pressed {
    background-color: #b0c5e3;
}

QScrollBar:vertical {
    background: #e7eff8;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #8aa7d9;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
