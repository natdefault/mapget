THEME = """
QWidget {
    background-color: #000000;
    color: #f2f2f2;
    font-family: Segoe UI;
    font-size: 12px;
}

QFrame#mainPanel {
    background-color: #090909;
    border: 1px solid #272727;
}

QLabel {
    color: #f2f2f2;
}

QLineEdit,
QTextEdit,
QComboBox {
    background-color: #111111;
    border: 1px solid #2e2e2e;
    color: #f8f8f8;
    padding: 5px;
    selection-background-color: #444444;
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
    border-top: 5px solid #f2f2f2;
    margin-right: 6px;
}

QPushButton {
    background-color: #131313;
    border: 1px solid #3a3a3a;
    color: #f2f2f2;
    padding: 6px 14px;
}

QPushButton:hover {
    background-color: #1f1f1f;
}

QPushButton:pressed {
    background-color: #080808;
}

QScrollBar:vertical {
    background: #0d0d0d;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #323232;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
