THEME = """
QMainWindow {
    background: #dbe7f6;
}

QWidget {
    background: #edf3fb;
    color: #000000;

    font-family: Segoe UI;
    font-size: 12px;
}

QFrame#mainPanel {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #fbfdff,
        stop:1 #eef4fb
    );

    border: 1px solid #92a9c0;
}

QLabel {
    background: transparent;
    color: #000000;
}

QToolBar {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #fcfdff,
        stop:0.45 #eef5fc,
        stop:0.46 #dce8f7,
        stop:1 #c8d9ee
    );

    border-bottom: 1px solid #8da4bf;

    spacing: 5px;

    padding-top: 4px;
    padding-bottom: 4px;
    padding-left: 6px;
    padding-right: 6px;
}

QToolBar::separator {
    width: 1px;

    background: "#7891af";

    margin-top: 4px;
    margin-bottom: 4px;
    margin-left: 5px;
    margin-right: 5px;
}

QLineEdit,
QTextEdit,
QComboBox {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:1 #f7fbff
    );

    border-top: 1px solid #7d9ab7;
    border-left: 1px solid #7d9ab7;
    border-right: 1px solid #b7c9db;
    border-bottom: 1px solid #b7c9db;

    padding: 4px;

    selection-background-color: #bcd6f5;

    min-height: 18px;
}

QLineEdit:focus,
QTextEdit:focus,
QComboBox:focus {
    border: 1px solid #5d8cc9;
}

QComboBox {
    padding-right: 22px;
}

QComboBox::drop-down {
    width: 20px;

    border-left: 1px solid #adc0d5;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:0.5 #edf4fc,
        stop:1 #d7e6f7
    );
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

    border: 1px solid #7f9db9;

    selection-background-color: #dbeafe;
    selection-color: #000000;

    padding: 2px;
}

QPushButton,
QToolButton {
    min-height: 22px;

    padding-left: 12px;
    padding-right: 12px;

    border-top: 1px solid #ffffff;
    border-left: 1px solid #ffffff;
    border-right: 1px solid #7f9db9;
    border-bottom: 1px solid #7f9db9;

    border-radius: 2px;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:0.48 #eef5fc,
        stop:0.49 #dfeaf8,
        stop:1 #d2e2f5
    );
}

QPushButton:hover,
QToolButton:hover {
    border: 1px solid #6d91bf;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:0.48 #f4f9ff,
        stop:0.49 #dcecff,
        stop:1 #c7def9
    );
}

QPushButton:pressed,
QToolButton:pressed {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #c8d9ee,
        stop:0.48 #d0dff1,
        stop:0.49 #e0ecfa,
        stop:1 #edf4fc
    );
}

QToolButton::menu-indicator {
    image: none;
    width: 0px;
}

QMenu {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #fdfefe,
        stop:1 #e4eef9
    );

    border: 1px solid #7f9db9;

    padding: 6px;
}

QMenu::item {
    padding: 6px 22px;

    margin-top: 2px;
    margin-bottom: 2px;

    border: 1px solid transparent;

    min-width: 130px;

    background: transparent;
}

QMenu::item:selected {
    border: 1px solid #8cb2e2;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #fff9d9,
        stop:1 #ffe8a6
    );
}

QCheckBox {
    spacing: 6px;
    background: transparent;
}

QCheckBox::indicator {
    width: 10px;
    height: 10px;

    border-radius: 5px;

    border: 1px solid #7f9db9;

    background: #ffffff;
}

QCheckBox::indicator:checked {
    background: #4b6eaf;
}

QScrollBar:vertical {
    width: 15px;

    background: #edf3fb;

    border-left: 1px solid #c2d3e6;
}

QScrollBar::handle:vertical {
    min-height: 24px;

    border: 1px solid #8da4bf;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #fafdff,
        stop:1 #c7dbf1
    );
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:1 #b8d3f2
    );
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}
"""