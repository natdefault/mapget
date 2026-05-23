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
    QToolButton,
    QDialog,
    QProgressBar
)

from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Qt, QTimer

import os
import sys
import sqlite3
from manager import MappingManager
from themes.xp import THEME as XP_THEME
from themes.vista import THEME as VISTA_THEME
from themes.void import THEME as VOID_THEME
from themes.dark import THEME as DARK_THEME
from themes.win95 import THEME as WIN95_THEME


# version only if compilesd
try:
    from version import VERSION, BUILD_DATE
except ImportError:
    VERSION = "" #  default if not compiled
    BUILD_DATE = ""


def get_asset_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename


def load_settings():
    settings = {
        "theme": "void",
        "auto_detect": True,
        "variant_buttons": False,
        "debug": False,
        "update_check": True
    }
    try:
        conn = sqlite3.connect(".mgcfg")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        cursor.execute("SELECT key, value FROM settings")
        for row in cursor.fetchall():
            k, v = row[0], row[1]
            if k == "theme":
                settings["theme"] = v
            elif k in ["auto_detect", "variant_buttons", "debug", "update_check"]:
                settings[k] = v == "True"
        conn.close()
    except Exception:
        pass
    return settings


def save_setting(key, value):
    try:
        conn = sqlite3.connect(".mgcfg")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()
    except Exception:
        pass


THEME = VOID_THEME


class DownloadProgressDialog(QDialog):
    def __init__(self, parent=None, current_theme="void"):
        super().__init__(parent)
        self.cancelled = False
        self.setWindowTitle("downloading...")
        self.setFixedSize(300, 120)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowSystemMenuHint)

        progress_bar_style = ""
        if current_theme == "xp":
            progress_bar_style = """
                QProgressBar {
                    border: 1px solid #7aa0d9;
                    background: #ffffff;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a6e3a1, stop:1 #32c524);
                }
            """
        elif current_theme == "vista":
            progress_bar_style = """
                QProgressBar {
                    border: 1px solid #8da4bf;
                    background: #ffffff;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a3d8f5, stop:1 #4ca8e6);
                }
            """
        elif current_theme == "void":
            progress_bar_style = """
                QProgressBar {
                    border: 1px solid #272727;
                    background: #111111;
                    text-align: center;
                    color: #f2f2f2;
                }
                QProgressBar::chunk {
                    background: #444444;
                }
            """
        elif current_theme == "dark":
            progress_bar_style = """
                QProgressBar {
                    border: 1px solid #33363b;
                    background: #1f2226;
                    text-align: center;
                    color: #f0f0f0;
                }
                QProgressBar::chunk {
                    background: #4b6eaf;
                }
            """
        elif current_theme == "win95":
            progress_bar_style = """
                QProgressBar {
                    border-top: 2px solid #404040;
                    border-left: 2px solid #404040;
                    border-right: 2px solid #ffffff;
                    border-bottom: 2px solid #ffffff;
                    background: #c0c0c0;
                    text-align: center;
                    color: #000000;
                }
                QProgressBar::chunk {
                    background-color: #000080;
                    width: 8px;
                    margin: 1px;
                }
            """
        self.setStyleSheet(parent.styleSheet() + "\n" + progress_bar_style)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        self.icon_label = QLabel()
        icon_name = "dl_invert.png" if current_theme in ["xp", "vista", "win95"] else "dl.png"
        pixmap = QPixmap(get_asset_path(f"assets/{icon_name}"))
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setScaledContents(True)
        header_layout.addWidget(self.icon_label)

        self.text_label = QLabel("starting download...")
        header_layout.addWidget(self.text_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def reject(self):
        self.cancelled = True
        super().reject()

    def update_progress_safe(self, description, percent):
        if self.cancelled:
            return
        if percent == -2:
            return

        self.text_label.setText(description)
        if percent == -1:
            self.progress_bar.setRange(0, 0)
        else:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(percent)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = MappingManager()
        self.settings = load_settings()
        self.current_theme = self.settings.get("theme", "void")

        if VERSION:
            self.setWindowTitle(f"mapget {VERSION}")
        else:
            self.setWindowTitle("mapget")

        self.resize(620, 430)

        self.setWindowIcon(QIcon(get_asset_path("assets/helpsheet.png")))

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
        self.change_theme(self.current_theme)
        self.check_for_updates()

    def build_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        self.settings_menu = QMenu(self)

        self.settings_menu.addSection("functionality")

        self.auto_detect_checkbox = QCheckBox(
            "enable auto detection"
        )

        self.variant_buttons_checkbox = QCheckBox(
            "show variant buttons"
        )

        self.debug_checkbox = QCheckBox(
            "enable debug output"
        )

        self.auto_detect_checkbox.setChecked(self.settings.get("auto_detect", True))
        self.variant_buttons_checkbox.setChecked(self.settings.get("variant_buttons", False))
        self.debug_checkbox.setChecked(self.settings.get("debug", False))

        self.auto_detect_checkbox.clicked.connect(
            lambda checked: save_setting("auto_detect", checked)
        )
        self.variant_buttons_checkbox.clicked.connect(
            lambda checked: save_setting("variant_buttons", checked)
        )
        self.debug_checkbox.clicked.connect(
            lambda checked: save_setting("debug", checked)
        )

        for checkbox in [
            self.auto_detect_checkbox,
            self.variant_buttons_checkbox,
            self.debug_checkbox
        ]:
            action = QWidgetAction(self.settings_menu)
            action.setDefaultWidget(checkbox)
            self.settings_menu.addAction(action)

        self.settings_menu.addSection("program")

        self.update_check_checkbox = QCheckBox(
            "check for updates on startup"
        )
        self.update_check_checkbox.setChecked(self.settings.get("update_check", True))
        self.update_check_checkbox.clicked.connect(
            lambda checked: save_setting("update_check", checked)
        )

        action = QWidgetAction(self.settings_menu)
        action.setDefaultWidget(self.update_check_checkbox)
        self.settings_menu.addAction(action)

        settings_button = QToolButton()
        settings_button.setText("settings")
        settings_button.setMenu(self.settings_menu)
        settings_button.setPopupMode(
            QToolButton.InstantPopup
        )
        settings_button.setFixedHeight(24)

        toolbar.addWidget(settings_button)

        self.themes_menu = QMenu(self)

        self.theme_group = []

        theme_names = [
            "xp",
            "vista",
            "void",
            "dark",
            "win95"
        ]

        for theme_name in theme_names:
            checkbox = QCheckBox(theme_name)

            checkbox.clicked.connect(
                lambda checked, name=theme_name:
                self.change_theme(name)
            )

            self.theme_group.append(checkbox)

            action = QWidgetAction(self.themes_menu)
            action.setDefaultWidget(checkbox)

            self.themes_menu.addAction(action)

        for checkbox in self.theme_group:
            if checkbox.text() == self.current_theme:
                checkbox.setChecked(True)

        themes_button = QToolButton()
        themes_button.setText("themes")
        themes_button.setMenu(self.themes_menu)
        themes_button.setPopupMode(
            QToolButton.InstantPopup
        )
        themes_button.setFixedHeight(24)

        toolbar.addWidget(themes_button)

        self.update_menu_styles(self.current_theme)

        toolbar.addSeparator()

        about_button = QPushButton("about")
        about_button.setFixedHeight(24)

        #new since old one didnt do anything
        about_button.clicked.connect(self.show_about)

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
            "intermediary",
            "srg",
            "tsrg",
            "retromcp",
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

        if not query:
            self.output.setPlainText("Empty query")
            return

        is_cached = False
        github = self.manager.github
        detected_mapping = mapping
        if mapping == "auto":
            detected_mapping = self.manager.detect_mapping_type(query)

        if detected_mapping == "obfuscated":
            is_cached = all(
                (f"{m}_{version}" in github.cache or github.load_cache(m, version) is not None)
                for m in ["yarn", "mojmap", "mcp"]
            )
        else:
            is_cached = (f"{detected_mapping}_{version}" in github.cache or
                         github.load_cache(detected_mapping, version) is not None)

        if is_cached:
            result = self.manager.handle_query(query, mapping, version)
            self.output.setPlainText(result)
            return

        import threading

        dialog = DownloadProgressDialog(self, self.current_theme)

        def progress_callback(description, percent):
            if dialog.cancelled:
                return True
            QTimer.singleShot(0, dialog, lambda: dialog.update_progress_safe(description, percent))
            return False

        def on_search_completed(result):
            if dialog.cancelled:
                self.output.setPlainText("Search cancelled")
                return
            dialog.accept()
            self.output.setPlainText(result or "Error: failed to retrieve mapping data.")

        def thread_target():
            try:
                res = self.manager.handle_query(query, mapping, version, progress_callback=progress_callback)
            except Exception as e:
                res = f"Error: {str(e)}"
            QTimer.singleShot(0, self, lambda: on_search_completed(res))

        threading.Thread(target=thread_target, daemon=True).start()
        dialog.exec()

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        save_setting("theme", theme_name)

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

        self.update_menu_styles(theme_name)

    def show_about(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        from PySide6.QtCore import QSize, Qt
        import webbrowser

        dialog = QDialog(self)
        dialog.setWindowTitle("about")
        dialog.setFixedSize(280, 185)
        dialog.setStyleSheet(self.styleSheet())
        dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        version_text = f"mapget {VERSION}" if VERSION else "mapget"
        lbl_title = QLabel(version_text)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(lbl_title)

        date_str = BUILD_DATE if BUILD_DATE else "dev"
        lbl_date = QLabel(f"build date: {date_str}")
        lbl_date.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_date)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(6)
        # layouts
        
        git_icon = "git_invert.png" if self.current_theme in ["xp", "vista", "win95"] else "git.png"
        btn_github = QPushButton("GitHub")
        btn_github.setIcon(QIcon(get_asset_path(f"assets/{git_icon}")))
        btn_github.setIconSize(QSize(16, 16))
        btn_github.clicked.connect(lambda: webbrowser.open("https://github.com/natdefault/mapget"))
        row_layout.addWidget(btn_github)

        rel_icon = "release_invert.png" if self.current_theme in ["xp", "vista", "win95"] else "release.png"
        btn_releases = QPushButton("Releases")
        btn_releases.setIcon(QIcon(get_asset_path(f"assets/{rel_icon}")))
        btn_releases.setIconSize(QSize(16, 16))
        btn_releases.clicked.connect(lambda: webbrowser.open("https://github.com/natdefault/mapget/releases"))
        row_layout.addWidget(btn_releases)

        layout.addLayout(row_layout)

        ota_icon = "ota_invert.png" if self.current_theme in ["xp", "vista", "win95"] else "ota.png"
        btn_ota = QPushButton("Check for updates")
        btn_ota.setIcon(QIcon(get_asset_path(f"assets/{ota_icon}")))
        btn_ota.setIconSize(QSize(16, 16))
        btn_ota.clicked.connect(lambda: [dialog.accept(), self.check_updates_clicked()])
        layout.addWidget(btn_ota)

        dialog.setLayout(layout)
        dialog.exec()

    def check_for_updates(self):
        if not self.update_check_checkbox.isChecked():
            return

        import threading
        threading.Thread(target=self._run_update_check, daemon=True).start() # query github

    def _run_update_check(self):
        import requests
        try:
            headers = {"User-Agent": "mapget-update-checker"}
            r = requests.get("https://api.github.com/repos/natdefault/mapget/releases/latest", headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                tag_name = data.get("tag_name", "").strip()
                latest_version = tag_name.lstrip("v")
                current_version = VERSION.strip().lstrip("v")

                if current_version and latest_version:
                    curr_parts = [int(x) for x in current_version.split(".") if x.isdigit()]
                    late_parts = [int(x) for x in latest_version.split(".") if x.isdigit()]

                    is_newer = False
                    for i in range(max(len(curr_parts), len(late_parts))):
                        c = curr_parts[i] if i < len(curr_parts) else 0
                        l = late_parts[i] if i < len(late_parts) else 0
                        if l > c:
                            is_newer = True
                            break
                        elif c > l:
                            break

                    if is_newer:
                        from PySide6.QtCore import QTimer
                        QTimer.singleShot(0, self, lambda: self.prompt_update(latest_version, data.get("html_url"))) # ask
        except Exception:
            pass

    def prompt_update(self, latest_version, url):
        from PySide6.QtWidgets import QMessageBox
        import webbrowser

        msg = QMessageBox(self)
        msg.setWindowTitle("update available")
        msg.setText(f"a new version is available : {latest_version}")
        msg.setInformativeText("would you like to open the releases page to download it?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setStyleSheet(self.styleSheet())

        if msg.exec() == QMessageBox.Yes:
            webbrowser.open(url)

    def update_menu_styles(self, theme_name):
        if theme_name == "xp":
            sep_color = "#adc0d5"
        elif theme_name == "vista":
            sep_color = "#8da4bf"
        elif theme_name == "void":
            sep_color = "#272727"
        elif theme_name == "dark":
            sep_color = "#2c2f33"
        elif theme_name == "win95":
            sep_color = "#808080"
        else:
            sep_color = "#2e2e2e"

        style = f"""
            QMenu {{
                border-radius: 0px;
                padding: 4px;
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {sep_color};
                margin-top: 8px;
                margin-bottom: 8px;
            }}
            QCheckBox {{
                padding: 6px 16px;
                min-width: 150px;
            }}
        """
        self.settings_menu.setStyleSheet(style)
        self.themes_menu.setStyleSheet(style)

    def check_updates_clicked(self):
        self.output.setPlainText("Checking for updates...")
        import threading
        threading.Thread(target=self._run_manual_update_check, daemon=True).start()

    def _run_manual_update_check(self):
        import requests
        from PySide6.QtCore import QTimer
        try:
            headers = {"User-Agent": "mapget-update-checker"}
            r = requests.get("https://api.github.com/repos/natdefault/mapget/releases/latest", headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                tag_name = data.get("tag_name", "").strip()
                latest_version = tag_name.lstrip("v")
                current_version = VERSION.strip().lstrip("v")

                if current_version:
                    curr_parts = [int(x) for x in current_version.split(".") if x.isdigit()]
                    late_parts = [int(x) for x in latest_version.split(".") if x.isdigit()]

                    is_newer = False
                    for i in range(max(len(curr_parts), len(late_parts))):
                        c = curr_parts[i] if i < len(curr_parts) else 0
                        l = late_parts[i] if i < len(late_parts) else 0
                        if l > c:
                            is_newer = True
                            break
                        elif c > l:
                            break

                    if is_newer:
                        msg = f"Update available: {latest_version}\nReleases URL: {data.get('html_url')}"
                        QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))
                        QTimer.singleShot(0, self, lambda: self.prompt_update(latest_version, data.get("html_url")))
                    else:
                        msg = f"up to date (version {VERSION})"
                        QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))
                else:
                    msg = f"Running development version.\nLatest release: {latest_version}\nReleases URL: {data.get('html_url')}"
                    QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))
            elif r.status_code == 404:
                msg = "No data."
                QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))
            else:
                msg = f"Failed to check for updates. Status code: {r.status_code}"
                QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))
        except Exception as e:
            msg = f"Error checking for updates: {str(e)}"
            QTimer.singleShot(0, self, lambda: self.output.setPlainText(msg))