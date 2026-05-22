THEME = """
QMainWindow {
    background-color: #111111;
}

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
    background: transparent;
}

QToolBar {
    background-color: #16181a;
    border-bottom: 1px solid #2c2f33;
    spacing: 4px;
    padding: 4px;
}

QMenu {
    background-color: #1a1d21;
    border: 1px solid #33363b;
    padding: 4px;
}

QMenu::item {
    padding: 5px 18px;
    background: transparent;
}

QMenu::item:selected {
    background-color: #2b3138;
}

QCheckBox {
    spacing: 6px;
    background: transparent;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #4a525a;
    background: #1f2226;
}

QCheckBox::indicator:checked {
    background: #4b6eaf;
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

QComboBox {
    padding-right: 24px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
    background: transparent;
}

QComboBox::down-arrow {
    image: none;
    width: 0px;
    height: 0px;

    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #d6d6d6;

    margin-right: 6px;
}

QAbstractItemView {
    background-color: #1f2226;
    border: 1px solid #33363b;
    selection-background-color: #3d444d;
    color: #f0f0f0;
}

QPushButton {
    background-color: #2f343b;
    border: 1px solid #4a525a;
    color: #e8e8e8;

    padding: 6px 14px;
    min-height: 20px;
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
    border-radius: 2px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QToolButton {
    background-color: #2f343b;
    border: 1px solid #4a525a;
    color: #e8e8e8;

    padding: 6px 14px;
    min-height: 20px;
}

QToolButton:hover {
    background-color: #3d444d;
}

QToolButton:pressed {
    background-color: #23272a;
}
QToolButton::menu-indicator {
    image: none;
    width: 0px;
}

"""