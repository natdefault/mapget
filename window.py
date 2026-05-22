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
    QCheckBox,
    QToolButton
)

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from manager import MappingManager

import sys
from themes.xp import THEME as XP_THEME
from themes.vista import THEME as VISTA_THEME
from themes.void import THEME as VOID_THEME
from themes.dark import THEME as DARK_THEME
from themes.win95 import THEME as WIN95_THEME


THEME = VOID_THEME

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

        settings_menu = QMenu(self)

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

        settings_button = QToolButton()
        settings_button.setText("settings")
        settings_button.setMenu(settings_menu)
        settings_button.setPopupMode(
            QToolButton.InstantPopup
        )
        settings_button.setFixedHeight(24)

        toolbar.addWidget(settings_button)

        themes_menu = QMenu(self)

        self.theme_group = []

        theme_names = [
            "xp",
            "vista",
            "void",
            "dark",
            "win95"
        ]

        self.current_theme = "void"

        for theme_name in theme_names:
            checkbox = QCheckBox(theme_name)

            checkbox.clicked.connect(
                lambda checked, name=theme_name:
                self.change_theme(name)
            )

            self.theme_group.append(checkbox)

            action = QWidgetAction(themes_menu)
            action.setDefaultWidget(checkbox)

            themes_menu.addAction(action)

        for checkbox in self.theme_group:
            if checkbox.text() == self.current_theme:
                checkbox.setChecked(True)

        themes_button = QToolButton()
        themes_button.setText("themes")
        themes_button.setMenu(themes_menu)
        themes_button.setPopupMode(
            QToolButton.InstantPopup
        )
        themes_button.setFixedHeight(24)

        toolbar.addWidget(themes_button)

        toolbar.addSeparator()

        about_button = QPushButton("about")
        about_button.setFixedHeight(24)

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

    def change_theme(self, theme_name):
        self.current_theme = theme_name

        for checkbox in self.theme_group:
            checkbox.blockSignals(True)

            checkbox.setChecked(
                checkbox.text() == theme_name
            )

            checkbox.blockSignals(False)

        if theme_name == "xp":
            self.setStyleSheet(XP_THEME)

        elif theme_name == "vista":
            self.setStyleSheet(VISTA_THEME)

        elif theme_name == "void":
            self.setStyleSheet(VOID_THEME)

        elif theme_name == "dark":
            self.setStyleSheet(DARK_THEME)
            
        elif theme_name == "win95":
            self.setStyleSheet(WIN95_THEME)