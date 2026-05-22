THEME = """
QMainWindow {
    background: #008080;
}

QWidget {
    background: #c0c0c0;
    color: #000000;

    font-family: "MS Sans Serif";
    font-size: 11px;
}

QFrame#mainPanel {
    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

QLabel {
    background: transparent;
    color: #000000;
}

QToolBar {
    spacing: 2px;
    padding: 2px;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #808080;
    border-bottom: 2px solid #808080;
}

QToolBar::separator {
    width: 2px;

    background: #808080;

    margin: 2px;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox {
    background: #ffffff;
    color: #000000;

    padding: 2px;

    border-top: 2px solid #404040;
    border-left: 2px solid #404040;

    border-right: 2px solid #ffffff;
    border-bottom: 2px solid #ffffff;

    selection-background-color: #000080;
    selection-color: #ffffff;

    min-height: 16px;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus {
    border-top: 2px solid #000000;
    border-left: 2px solid #000000;

    border-right: 2px solid #dfdfdf;
    border-bottom: 2px solid #dfdfdf;
}

QComboBox {
    padding-right: 18px;
}

QComboBox::drop-down {
    width: 18px;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

QComboBox::down-arrow {
    image: none;

    width: 7px;
    height: 7px;

    background: transparent;

    border: none;
}

QAbstractItemView {
    background: #ffffff;
    color: #000000;

    border: 2px solid #404040;

    selection-background-color: #000080;
    selection-color: #ffffff;
}

QPushButton,
QToolButton {
    min-height: 20px;

    padding-left: 8px;
    padding-right: 8px;

    color: #000000;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

QPushButton:hover,
QToolButton:hover {
    background: #d4d0c8;
}

QPushButton:pressed,
QToolButton:pressed {
    padding-top: 1px;
    padding-left: 1px;

    border-top: 2px solid #404040;
    border-left: 2px solid #404040;

    border-right: 2px solid #ffffff;
    border-bottom: 2px solid #ffffff;

    background: #b0b0b0;
}

QToolButton::menu-indicator {
    image: none;
    width: 0px;
}

QMenu {
    background: #c0c0c0;

    border: 2px solid #404040;

    padding: 2px;
}

QMenu::item {
    padding: 4px 20px;

    background: transparent;
}

QMenu::item:selected {
    background: #000080;
    color: #ffffff;
}

QCheckBox {
    spacing: 4px;

    background: transparent;
}

QCheckBox::indicator {
    width: 11px;
    height: 11px;

    background: #ffffff;

    border-top: 2px solid #404040;
    border-left: 2px solid #404040;

    border-right: 2px solid #ffffff;
    border-bottom: 2px solid #ffffff;
}

QCheckBox::indicator:checked {
    background: #000080;
}

QScrollBar:vertical {
    width: 16px;

    background: #c0c0c0;
}

QScrollBar::handle:vertical {
    min-height: 24px;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 16px;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

QScrollBar::up-arrow:vertical {
    image: none;

    width: 0px;
    height: 0px;

    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #000000;
}

QScrollBar::down-arrow:vertical {
    image: none;

    width: 0px;
    height: 0px;

    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #000000;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: #c0c0c0;
}

QTreeView::item:selected,
QListView::item:selected,
QTableView::item:selected {
    background: #000080;
    color: #ffffff;
}

QTabWidget::pane {
    background: #c0c0c0;

    border: 2px solid #404040;
}

QTabBar::tab {
    padding: 4px 8px;

    background: #c0c0c0;

    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;

    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;

    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #c0c0c0;

    border-bottom: 2px solid #c0c0c0;
}
"""