THEME = """
QWidget {
    background-color: #111111;
    color: #e8e8e8;
    font-family: Segoe UI;
    font-size: 12px;
}

QFrame#mainPanel {
    background-color: #16181a;
    border: 1px solid #2c2f33;
}

QLabel {
    color: #e8e8e8;
}

QLineEdit,
QTextEdit,
QComboBox {
    background-color: #1f2226;
    border: 1px solid #33363b;
    color: #f0f0f0;
    padding: 5px;
    selection-background-color: #4b6eaf;
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
    border-top: 5px solid #d6d6d6;
    margin-right: 6px;
}

QPushButton {
    background-color: #2f343b;
    border: 1px solid #4a525a;
    color: #e8e8e8;
    padding: 6px 14px;
}

QPushButton:hover {
    background-color: #3d444d;
}

QPushButton:pressed {
    background-color: #23272a;
}

QScrollBar:vertical {
    background: #16181a;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #3e4349;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
