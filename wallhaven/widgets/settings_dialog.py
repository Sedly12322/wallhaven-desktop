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
)
from wallhaven.config import config
from wallhaven.cache import CACHE_DIR
from wallhaven.wallpaper import detect_wallpaper_command


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nastavení Wallhaven Desktop")
        self.setMinimumWidth(540)
        self.setModal(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Nastavení")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # API Key Section
        api_group = QGroupBox("Wallhaven API Klíč")
        api_group.setStyleSheet("""
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
        api_layout = QVBoxLayout(api_group)
        api_layout.setSpacing(10)

        api_desc = QLabel(
            "API klíč umožňuje odemknout <b>NSFW</b> obsah a vyhledávat bez omezení.<br>"
            "Svůj klíč najdeš na: <a href='https://wallhaven.cc/settings/api' style='color: #6366f1;'>wallhaven.cc/settings/api</a>"
        )
        api_desc.setOpenExternalLinks(True)
        api_desc.setWordWrap(True)
        api_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        api_layout.addWidget(api_desc)

        api_input_row = QHBoxLayout()
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Vlož svůj Wallhaven API klíč...")
        self.api_key_input.setText(config.api_key)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_input_row.addWidget(self.api_key_input)

        self.toggle_key_btn = QPushButton("👁")
        self.toggle_key_btn.setToolTip("Zobrazit / Skrýt klíč")
        self.toggle_key_btn.setFixedWidth(36)
        self.toggle_key_btn.clicked.connect(self._toggle_api_visibility)
        api_input_row.addWidget(self.toggle_key_btn)

        api_layout.addLayout(api_input_row)
        layout.addWidget(api_group)

        # Download Directory Section
        dir_group = QGroupBox("Výchozí složka pro stahování")
        dir_group.setStyleSheet("""
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
        dir_layout = QVBoxLayout(dir_group)
        dir_layout.setSpacing(10)

        dir_desc = QLabel("Při každém stažení se otevře dialog pro uložení s touto výchozí složkou.")
        dir_desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        dir_layout.addWidget(dir_desc)

        dir_input_row = QHBoxLayout()
        self.dir_input = QLineEdit()
        self.dir_input.setText(config.default_download_dir)
        dir_input_row.addWidget(self.dir_input)

        browse_btn = QPushButton("Procházet...")
        browse_btn.clicked.connect(self._on_browse_dir)
        dir_input_row.addWidget(browse_btn)

        dir_layout.addLayout(dir_input_row)
        layout.addWidget(dir_group)

        # Wallpaper Section
        wall_group = QGroupBox("Tapeta plochy")
        wall_group.setStyleSheet("""
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
        wall_layout = QVBoxLayout(wall_group)
        wall_layout.setSpacing(8)

        self.auto_wall_cb = QCheckBox("Automaticky nastavit tapetu na plochu ihned po stažení")
        self.auto_wall_cb.setChecked(config.auto_set_wallpaper)
        self.auto_wall_cb.setStyleSheet("font-weight: bold; color: #f1f5f9; font-size: 12px;")
        wall_layout.addWidget(self.auto_wall_cb)

        detected_list = detect_wallpaper_command()
        detected_str = " ".join(detected_list) if detected_list else "Nenalezeno"
        det_lbl = QLabel(f"Detekovaný nástroj v systému: <code>{detected_str}</code>")
        det_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        wall_layout.addWidget(det_lbl)

        custom_cmd_lbl = QLabel("Vlastní příkaz pro nastavení tapety (ponechte prázdné pro automatiku):")
        custom_cmd_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        wall_layout.addWidget(custom_cmd_lbl)

        self.custom_cmd_input = QLineEdit()
        self.custom_cmd_input.setPlaceholderText("např. swww img {file} nebo feh --bg-fill {file}")
        self.custom_cmd_input.setText(config.custom_wallpaper_cmd)
        wall_layout.addWidget(self.custom_cmd_input)

        layout.addWidget(wall_group)

        # Cache Section
        cache_group = QGroupBox("Mezipaměť (Cache)")
        cache_group.setStyleSheet("""
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
        cache_layout = QHBoxLayout(cache_group)

        self.cache_size_lbl = QLabel(self._get_cache_size_str())
        self.cache_size_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        cache_layout.addWidget(self.cache_size_lbl)

        cache_layout.addStretch()

        clear_cache_btn = QPushButton("Vymazat mezipaměť")
        clear_cache_btn.setStyleSheet("color: #f87171; border-color: #7f1d1d;")
        clear_cache_btn.clicked.connect(self._on_clear_cache)
        cache_layout.addWidget(clear_cache_btn)

        layout.addWidget(cache_group)

        layout.addStretch()

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        save_btn = QPushButton("Uložit")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)

        layout.addLayout(btn_row)

    def _toggle_api_visibility(self):
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _on_browse_dir(self):
        cur = self.dir_input.text() or str(Path.home())
        chosen = QFileDialog.getExistingDirectory(self, "Vyberte výchozí složku pro tapety", cur)
        if chosen:
            self.dir_input.setText(chosen)

    def _get_cache_size_str(self) -> str:
        try:
            if not CACHE_DIR.exists():
                return "Velikost cache: 0 MB"
            total = sum(f.stat().st_size for f in CACHE_DIR.glob("**/*") if f.is_file())
            mb = total / (1024 * 1024)
            return f"Velikost cache: {mb:.1f} MB"
        except Exception:
            return "Velikost cache: Neznámá"

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
            QMessageBox.information(self, "Hotovo", "Mezipaměť byla úspěšně vymazána.")
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Nepodařilo se vymazat mezipaměť: {e}")

    def _on_save(self):
        config.api_key = self.api_key_input.text().strip()
        chosen_dir = self.dir_input.text().strip()
        if chosen_dir and os.path.isdir(chosen_dir):
            config.default_download_dir = chosen_dir
        config.auto_set_wallpaper = self.auto_wall_cb.isChecked()
        config.custom_wallpaper_cmd = self.custom_cmd_input.text().strip()
        config.save()
        self.accept()
