THEME = """
QMainWindow {
    background-color: #000000;
}

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
    background: transparent;
}

QToolBar {
    background-color: #090909;
    border-bottom: 1px solid #272727;
    spacing: 4px;
    padding: 4px;
}

QCheckBox {
    spacing: 6px;
    background: transparent;
}

QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #3a3a3a;
    background: #111111;
}

QCheckBox::indicator:checked {
    background: #444444;
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
    border-top: 5px solid #f2f2f2;

    margin-right: 6px;
}

QAbstractItemView {
    background-color: #111111;
    border: 1px solid #2e2e2e;
    selection-background-color: #1f1f1f;
    color: #f8f8f8;
}

QPushButton {
    background-color: #131313;
    border: 1px solid #3a3a3a;
    color: #f2f2f2;

    padding: 6px 14px;
    min-height: 20px;
    border-radius: 0px;
}

QPushButton:hover {
    background-color: #1f1f1f;
}

QPushButton:pressed {
    background-color: #080808;
}

QToolButton {
    background-color: #131313;
    border: 1px solid #3a3a3a;
    color: #f2f2f2;

    padding: 6px 14px;
    min-height: 20px;
    border-radius: 0px;
}

QToolButton:hover {
    background-color: #1f1f1f;
}

QToolButton:pressed {
    background-color: #080808;
}

QToolButton::menu-indicator {
    image: none;
    width: 0px;
}


QScrollBar:vertical {
    background: #0d0d0d;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #323232;
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

QMenu {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #151515,
        stop:1 #090909
    );

    border: 1px solid #323232;
    padding: 6px;
}

QMenu::item {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #181818,
        stop:1 #101010
    );

    border: 1px solid #252525;

    padding: 7px 18px;

    margin-top: 2px;
    margin-bottom: 2px;

    min-width: 170px;
}

QMenu::item:selected {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #222222,
        stop:1 #181818
    );

    border: 1px solid #4a4a4a;
}

QCheckBox {
    spacing: 5px;
    background: transparent;
}

QCheckBox::indicator {
    width: 9px;
    height: 9px;

    border-radius: 0px;

    border: 1px solid #5a5a5a;

    background: #111111;
}

QCheckBox::indicator:checked {
    background: #dcdcdc;
}

QToolBar::separator {
    background: "#2e2e2e";

    width: 2px;

    margin-top: 2px;
    margin-bottom: 2px;
    margin-left: 4px;
    margin-right: 4px;
}

"""