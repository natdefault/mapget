from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QToolBar,
    QMenu,
    QWidgetAction,
    QCheckBox
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from manager import MappingManager

import sys


THEME = """
QMainWindow {
    background: #dfe8f6;
}

QWidget {
    background: #eef3fb;
    color: #000000;
    font-family: Segoe UI;
    font-size: 12px;
}

QToolBar {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #f7fbff,
        stop:1 #d6e4f5
    );

    border-bottom: 1px solid #8aa6c1;
    spacing: 4px;
    padding: 2px;
}

QFrame#mainPanel {
    background: #f5f8fd;
    border: 1px solid #8aa6c1;
}

QLabel {
    background: transparent;
    color: #000000;
}

QLineEdit,
QComboBox,
QTextEdit {
    background: white;

    border-top: 1px solid #7f9db9;
    border-left: 1px solid #7f9db9;
    border-right: 1px solid #b7c9dc;
    border-bottom: 1px solid #b7c9dc;

    padding: 2px;
    min-height: 18px;
}

QComboBox {
    padding-right: 18px;
}

QComboBox::drop-down {
    width: 18px;
    border-left: 1px solid #a6b8cb;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:1 #d9e7f7
    );
}

QPushButton {
    min-height: 20px;

    padding-left: 8px;
    padding-right: 8px;

    border-top: 1px solid #ffffff;
    border-left: 1px solid #ffffff;
    border-right: 1px solid #7f9db9;
    border-bottom: 1px solid #7f9db9;

    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:1 #dbe8f7
    );
}

QPushButton:hover {
    background: qlineargradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:0 #ffffff,
        stop:1 #cfe4ff
    );
}

QPushButton:pressed {
    background: #c7d8eb;
}

QMenu {
    background: #f7fbff;
    border: 1px solid #7f9db9;
    padding: 4px;
}

QCheckBox {
    spacing: 6px;
    background: transparent;
}

QTextEdit {
    background: white;
}

QScrollBar:vertical {
    width: 14px;
    background: #e8eef7;
}

QScrollBar::handle:vertical {
    background: #c1d2e8;
    border: 1px solid #8aa6c1;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = MappingManager()

        self.setWindowTitle("mapget")
        self.resize(620, 430)

        self.setStyleSheet(THEME)

        self.mcp_versions = [
            "1.12.2",
            "1.11.2",
            "1.10.2",
            "1.8.9"
        ]

        self.normal_versions = [
            "1.21.1",
            "1.21",
            "1.20.6",
            "1.20.4",
            "1.20.1",
            "1.19.4",
            "1.18.2",
            "1.17.1",
            "1.16.5",
            "1.12.2",
            "1.8.9"
        ]

        self.build_toolbar()
        self.build_ui()

    def build_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        settings_button = QPushButton("settings")
        settings_button.setFixedHeight(22)

        settings_menu = QMenu()

        self.auto_detect_checkbox = QCheckBox(
            "enable auto detection"
        )

        self.variant_buttons_checkbox = QCheckBox(
            "show variant buttons"
        )

        self.debug_checkbox = QCheckBox(
            "enable debug output"
        )

        self.auto_detect_checkbox.setChecked(True)

        for checkbox in [
            self.auto_detect_checkbox,
            self.variant_buttons_checkbox,
            self.debug_checkbox
        ]:
            action = QWidgetAction(settings_menu)
            action.setDefaultWidget(checkbox)
            settings_menu.addAction(action)

        settings_button.setMenu(settings_menu)

        toolbar.addWidget(settings_button)

        toolbar.addSeparator()

        about_button = QPushButton("about")
        about_button.setFixedHeight(22)

        toolbar.addWidget(about_button)

    def build_ui(self):
        container = QWidget()

        self.setCentralWidget(container)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(6)

        panel = QFrame()
        panel.setObjectName("mainPanel")

        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(10, 10, 10, 10)
        panel_layout.setSpacing(6)

        title = QLabel("mapget")
        title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        panel_layout.addWidget(title)

        query_label = QLabel("query / search for")
        panel_layout.addWidget(query_label)

        self.input_box = QLineEdit()

        self.input_box.setPlaceholderText(
            "field_12345 / class_1234 / net.minecraft..."
        )

        self.input_box.returnPressed.connect(self.search)

        panel_layout.addWidget(self.input_box)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(6)

        mapping_layout = QVBoxLayout()
        mapping_layout.setSpacing(2)

        mapping_label = QLabel("mapping")
        mapping_layout.addWidget(mapping_label)

        self.mapping_box = QComboBox()

        self.mapping_box.addItems([
            "auto",
            "yarn",
            "mojmap",
            "mcp",
            "obfuscated"
        ])

        self.mapping_box.currentTextChanged.connect(
            self.update_versions
        )

        mapping_layout.addWidget(self.mapping_box)

        version_layout = QVBoxLayout()
        version_layout.setSpacing(2)

        version_label = QLabel("version")
        version_layout.addWidget(version_label)

        self.version_box = QComboBox()

        self.version_box.addItems(self.normal_versions)

        self.version_box.setCurrentText("1.20.1")

        version_layout.addWidget(self.version_box)

        row_layout.addLayout(mapping_layout)
        row_layout.addLayout(version_layout)

        panel_layout.addLayout(row_layout)

        button_row = QHBoxLayout()
        button_row.setSpacing(4)

        self.search_button = QPushButton("search")
        self.search_button.setFixedHeight(24)
        self.search_button.clicked.connect(self.search)

        button_row.addWidget(self.search_button)

        self.copy_button = QPushButton("copy")
        self.copy_button.setFixedHeight(24)

        button_row.addWidget(self.copy_button)

        button_row.addStretch()

        panel_layout.addLayout(button_row)

        results_label = QLabel("results")
        panel_layout.addWidget(results_label)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        panel_layout.addWidget(self.output)

        panel.setLayout(panel_layout)

        root_layout.addWidget(panel)

        container.setLayout(root_layout)

    def update_versions(self):
        current_mapping = self.mapping_box.currentText()

        current_version = self.version_box.currentText()

        self.version_box.clear()

        if current_mapping == "mcp":
            self.version_box.addItems(self.mcp_versions)

            if current_version in self.mcp_versions:
                self.version_box.setCurrentText(
                    current_version
                )
            else:
                self.version_box.setCurrentIndex(0)

        else:
            self.version_box.addItems(self.normal_versions)

            if current_version in self.normal_versions:
                self.version_box.setCurrentText(
                    current_version
                )

    def search(self):
        query = self.input_box.text().strip()

        mapping = self.mapping_box.currentText()

        version = self.version_box.currentText()

        result = self.manager.handle_query(
            query,
            mapping,
            version
        )

        self.output.setPlainText(result)


def main():
    app = QApplication(sys.argv)

    window = AppWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()