THEME = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d9ecff, stop:1 #c6e0fb);
}

QWidget {
    background: #f0f4f8;
    color: #000000;

    font-family: Tahoma, Arial, sans-serif;
    font-size: 11px;
}

QFrame#mainPanel {
    background: #ffffff;
    border: 1px solid #9bb5d6;
}

QLabel {
    background: transparent;
    color: #000000;
}

QToolBar {
    spacing: 4px;
    padding: 4px;
    border-top: 1px solid #ffffff;
    border-bottom: 1px solid #7aa0d9;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #eaf6ff, stop:1 #cfe9ff);
}

QToolBar::separator {
    width: 1px;
    background: #c2d9ee;
    margin: 4px;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox {
    background: #ffffff;
    color: #000000;
    padding: 3px;
    border: 1px solid #b7d0ea;
    selection-background-color: #0a64ad;
    selection-color: #ffffff;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus {
    border: 1px solid #0a64ad;
}

QComboBox { padding-right: 20px; }
QComboBox::drop-down { width: 20px; border-left: 1px solid #b7d0ea; background: #eaf6ff; }
QComboBox::down-arrow { image: none; }

QPushButton,
QToolButton {
    color: #000000;
    min-height: 22px;
    padding: 4px 8px;
    border: 1px solid #7aa0d9;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #d6eafc);
}

QPushButton:hover,
QToolButton:hover {
    border: 1px solid #0a64ad;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e7f3ff, stop:1 #cfe9ff);
}

QPushButton:pressed,
QToolButton:pressed {
    border: 1px solid #5b8fc0;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c0e2fb, stop:1 #a6d8f8);
}

QToolButton::menu-indicator { image: none; }

QMenu {
    background: #ffffff;
    border: 1px solid #9bb5d6;
}


QPlainTextEdit#output, QTextEdit#output {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e9f6ff);
    border-top: 1px solid #ffffff;
    border-left: 1px solid #ffffff;
    border-bottom: 1px solid #9bb5d6;
    border-right: 1px solid #9bb5d6;
    padding: 6px;
}

QMenu::item { padding: 5px 24px; }
QMenu::item:selected { color: #ffffff; background: #0a64ad; }

QCheckBox { spacing: 6px; }
QCheckBox::indicator { width: 14px; height: 14px; background: #ffffff; border: 1px solid #b7d0ea; }
QCheckBox::indicator:checked { background: #0a64ad; }

QScrollBar:vertical { width: 16px; background: #f0f4f8; border-left: 1px solid #d0e6f6; }
QScrollBar::handle:vertical { min-height: 24px; border: 1px solid #9bb5d6; background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #eaf6ff, stop:1 #9ec9f1); }
QScrollBar::handle:vertical:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #f0f9ff, stop:1 #a8d1f6); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 16px; border: 1px solid #b7d0ea; background: #eaf6ff; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: #f0f4f8; }

QTreeView::item:selected, QListView::item:selected, QTableView::item:selected { background: #0a64ad; color: #ffffff; }

QTabWidget::pane { border: 1px solid #9bb5d6; background: #ffffff; }
QTabBar::tab { padding: 4px 8px; background: #eaf6ff; border: 1px solid #b7d0ea; margin-right: 2px; }
QTabBar::tab:selected { background: #ffffff; border-bottom: 1px solid #ffffff; }
"""