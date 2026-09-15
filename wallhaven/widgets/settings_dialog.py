import os
import shutil
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
    QGroupBox,
    QCheckBox,
    QComboBox,
)
from wallhaven.config import config
from wallhaven.cache import CACHE_DIR
from wallhaven.wallpaper import detect_wallpaper_command
from wallhaven.i18n import tr, i18n


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("settings_title"))
        self.setMinimumWidth(560)
        self.setModal(True)
        self._init_ui()
        i18n.language_changed.connect(self.retranslate_ui)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_lbl = QLabel(tr("settings_title"))
        self.title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.title_lbl)

        # 1. Language Section
        self.lang_group = QGroupBox(tr("lang_section"))
        self._apply_group_style(self.lang_group)
        lang_layout = QHBoxLayout(self.lang_group)
        
        self.lang_label = QLabel(tr("lang_label"))
        self.lang_label.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        lang_layout.addWidget(self.lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Čeština (Czech)", "cs")
        self.lang_combo.addItem("English", "en")
        idx = self.lang_combo.findData(i18n.current_language)
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()

        layout.addWidget(self.lang_group)

        # 2. API Key Section
        self.api_group = QGroupBox(tr("api_group"))
        self._apply_group_style(self.api_group)
        api_layout = QVBoxLayout(self.api_group)
        api_layout.setSpacing(10)

        self.api_desc = QLabel(tr("api_desc"))
        self.api_desc.setOpenExternalLinks(True)
        self.api_desc.setWordWrap(True)
        self.api_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        api_layout.addWidget(self.api_desc)

        api_input_row = QHBoxLayout()
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText(tr("api_placeholder"))
        self.api_key_input.setText(config.api_key)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_input_row.addWidget(self.api_key_input)

        self.toggle_key_btn = QPushButton("👁")
        self.toggle_key_btn.setToolTip(tr("api_toggle_tip"))
        self.toggle_key_btn.setFixedWidth(36)
        self.toggle_key_btn.clicked.connect(self._toggle_api_visibility)
        api_input_row.addWidget(self.toggle_key_btn)

        api_layout.addLayout(api_input_row)
        layout.addWidget(self.api_group)

        # 3. Download Directory Section
        self.dir_group = QGroupBox(tr("dir_group"))
        self._apply_group_style(self.dir_group)
        dir_layout = QVBoxLayout(self.dir_group)
        dir_layout.setSpacing(10)

        self.dir_desc = QLabel(tr("dir_desc"))
        self.dir_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        dir_layout.addWidget(self.dir_desc)

        dir_input_row = QHBoxLayout()
        self.dir_input = QLineEdit()
        self.dir_input.setText(config.default_download_dir)
        dir_input_row.addWidget(self.dir_input)

        self.browse_btn = QPushButton(tr("browse_button"))
        self.browse_btn.clicked.connect(self._on_browse_dir)
        dir_input_row.addWidget(self.browse_btn)

        dir_layout.addLayout(dir_input_row)
        layout.addWidget(self.dir_group)

        # 4. Wallpaper Section
        self.wall_group = QGroupBox(tr("wall_group"))
        self._apply_group_style(self.wall_group)
        wall_layout = QVBoxLayout(self.wall_group)
        wall_layout.setSpacing(8)

        self.auto_wall_cb = QCheckBox(tr("auto_wall_checkbox"))
        self.auto_wall_cb.setChecked(config.auto_set_wallpaper)
        self.auto_wall_cb.setStyleSheet("font-weight: bold; color: #f1f5f9; font-size: 12px;")
        wall_layout.addWidget(self.auto_wall_cb)

        detected_list = detect_wallpaper_command()
        detected_str = " ".join(detected_list) if detected_list else tr("tool_none")
        self.det_lbl = QLabel(tr("detected_tool", tool=detected_str))
        self.det_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        wall_layout.addWidget(self.det_lbl)

        self.custom_cmd_lbl = QLabel(tr("custom_cmd_label"))
        self.custom_cmd_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        wall_layout.addWidget(self.custom_cmd_lbl)

        self.custom_cmd_input = QLineEdit()
        self.custom_cmd_input.setPlaceholderText(tr("custom_cmd_placeholder"))
        self.custom_cmd_input.setText(config.custom_wallpaper_cmd)
        wall_layout.addWidget(self.custom_cmd_input)

        layout.addWidget(self.wall_group)

        # 5. Cache Section
        self.cache_group = QGroupBox(tr("cache_group"))
        self._apply_group_style(self.cache_group)
        cache_layout = QHBoxLayout(self.cache_group)

        self.cache_size_lbl = QLabel(self._get_cache_size_str())
        self.cache_size_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        cache_layout.addWidget(self.cache_size_lbl)

        cache_layout.addStretch()

        self.clear_cache_btn = QPushButton(tr("cache_clear_button"))
        self.clear_cache_btn.setStyleSheet("color: #f87171; border-color: #7f1d1d;")
        self.clear_cache_btn.clicked.connect(self._on_clear_cache)
        cache_layout.addWidget(self.clear_cache_btn)

        layout.addWidget(self.cache_group)

        layout.addStretch()

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.cancel_btn = QPushButton(tr("btn_cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.cancel_btn)

        self.save_btn = QPushButton(tr("btn_save"))
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.save_btn)

        layout.addLayout(btn_row)

    def _apply_group_style(self, group: QGroupBox):
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #333845;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: #818cf8;
            }
        """)

    def _on_language_changed(self):
        new_lang = self.lang_combo.currentData()
        if new_lang:
            i18n.set_language(new_lang)

    def retranslate_ui(self):
        self.setWindowTitle(tr("settings_title"))
        self.title_lbl.setText(tr("settings_title"))
        self.lang_group.setTitle(tr("lang_section"))
        self.lang_label.setText(tr("lang_label"))
        self.api_group.setTitle(tr("api_group"))
        self.api_desc.setText(tr("api_desc"))
        self.api_key_input.setPlaceholderText(tr("api_placeholder"))
        self.dir_group.setTitle(tr("dir_group"))
        self.dir_desc.setText(tr("dir_desc"))
        self.browse_btn.setText(tr("browse_button"))
        self.wall_group.setTitle(tr("wall_group"))
        self.auto_wall_cb.setText(tr("auto_wall_checkbox"))

        detected_list = detect_wallpaper_command()
        detected_str = " ".join(detected_list) if detected_list else tr("tool_none")
        self.det_lbl.setText(tr("detected_tool", tool=detected_str))
        self.custom_cmd_lbl.setText(tr("custom_cmd_label"))
        self.custom_cmd_input.setPlaceholderText(tr("custom_cmd_placeholder"))
        self.cache_group.setTitle(tr("cache_group"))
        self.cache_size_lbl.setText(self._get_cache_size_str())
        self.clear_cache_btn.setText(tr("cache_clear_button"))
        self.cancel_btn.setText(tr("btn_cancel"))
        self.save_btn.setText(tr("btn_save"))

    def _toggle_api_visibility(self):
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _on_browse_dir(self):
        cur = self.dir_input.text() or str(Path.home())
        chosen = QFileDialog.getExistingDirectory(self, tr("browse_dialog_title"), cur)
        if chosen:
            self.dir_input.setText(chosen)

    def _get_cache_size_str(self) -> str:
        try:
            if not CACHE_DIR.exists():
                return tr("cache_size", size="0")
            total = sum(f.stat().st_size for f in CACHE_DIR.glob("**/*") if f.is_file())
            mb = total / (1024 * 1024)
            return tr("cache_size", size=f"{mb:.1f}")
        except Exception:
            return tr("cache_size", size="?")

    def _on_clear_cache(self):
        try:
            if CACHE_DIR.exists():
                for item in CACHE_DIR.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            (CACHE_DIR / "thumbnails").mkdir(parents=True, exist_ok=True)
            (CACHE_DIR / "previews").mkdir(parents=True, exist_ok=True)
            self.cache_size_lbl.setText(self._get_cache_size_str())
            QMessageBox.information(self, tr("cache_cleared_title"), tr("cache_cleared_msg"))
        except Exception as e:
            QMessageBox.critical(self, tr("download_failed_title"), tr("cache_clear_error", error=str(e)))

    def _on_save(self):
        config.api_key = self.api_key_input.text().strip()
        chosen_dir = self.dir_input.text().strip()
        if chosen_dir and os.path.isdir(chosen_dir):
            config.default_download_dir = chosen_dir
        config.auto_set_wallpaper = self.auto_wall_cb.isChecked()
        config.custom_wallpaper_cmd = self.custom_cmd_input.text().strip()
        config.language = self.lang_combo.currentData()
        config.save()
        self.accept()
