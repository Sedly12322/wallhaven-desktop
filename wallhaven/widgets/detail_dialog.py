import os
from pathlib import Path
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices, QColor
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QFileDialog,
    QScrollArea,
    QWidget,
    QFrame,
    QMessageBox,
    QCheckBox,
)
from wallhaven.api import WallpaperItem, api
from wallhaven.config import config
from wallhaven.image_loader import loader
from wallhaven.wallpaper import set_desktop_wallpaper


class DetailFetchWorker(QThread):
    finished = pyqtSignal(WallpaperItem)
    failed = pyqtSignal(str)

    def __init__(self, wallpaper_id: str):
        super().__init__()
        self.wallpaper_id = wallpaper_id

    def run(self):
        try:
            full_item = api.get_wallpaper_detail(self.wallpaper_id)
            self.finished.emit(full_item)
        except Exception as e:
            self.failed.emit(str(e))


class DownloadWorker(QThread):
    progress = pyqtSignal(int, int)  # downloaded, total
    finished = pyqtSignal(str)       # saved file path
    failed = pyqtSignal(str)

    def __init__(self, url: str, dest_path: str):
        super().__init__()
        self.url = url
        self.dest_path = dest_path
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            ok = api.download_file(
                self.url,
                self.dest_path,
                progress_callback=lambda d, t: self.progress.emit(d, t),
                is_cancelled=lambda: self._cancelled,
            )
            if ok:
                self.finished.emit(self.dest_path)
            else:
                self.failed.emit("Stahování bylo zrušeno")
        except Exception as e:
            self.failed.emit(str(e))


class DetailDialog(QDialog):
    tag_clicked = pyqtSignal(str)
    download_completed = pyqtSignal(str)

    def __init__(self, item: WallpaperItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.download_worker: DownloadWorker | None = None
        self.saved_path: str = ""

        self.setWindowTitle(f"Tapeta {item.id} - Wallhaven ({item.resolution})")
        self.resize(1100, 720)
        self.setMinimumSize(850, 550)

        self._init_ui()
        self._load_preview()
        self._fetch_full_details()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Left: Large Preview Container
        preview_container = QFrame()
        preview_container.setStyleSheet("background-color: #12141a; border-radius: 8px;")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_label = QLabel("Načítání náhledu...")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: #64748b; font-size: 14px;")
        preview_layout.addWidget(self.preview_label)

        main_layout.addWidget(preview_container, stretch=3)

        # Right: Info & Actions Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(330)
        sidebar.setStyleSheet("background-color: #1a1d24; border-radius: 8px; padding: 12px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(12)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)

        # Wallpaper ID and Wallhaven link
        id_row = QHBoxLayout()
        id_lbl = QLabel(f"<b>#{self.item.id}</b>")
        id_lbl.setStyleSheet("font-size: 16px; color: #ffffff;")
        id_row.addWidget(id_lbl)

        id_row.addStretch()

        open_web_btn = QPushButton("Otevřít na webu ↗")
        open_web_btn.setStyleSheet("font-size: 11px; padding: 4px 8px;")
        open_web_btn.clicked.connect(self._open_in_browser)
        id_row.addWidget(open_web_btn)
        sidebar_layout.addLayout(id_row)

        # Metadata Table / List
        meta_frame = QFrame()
        meta_frame.setStyleSheet("background: #21242d; border-radius: 6px; padding: 8px;")
        meta_layout = QVBoxLayout(meta_frame)
        meta_layout.setSpacing(6)

        def add_meta_row(label: str, val: str):
            r = QHBoxLayout()
            l = QLabel(label)
            l.setStyleSheet("color: #94a3b8; font-size: 12px;")
            v = QLabel(f"<b>{val}</b>")
            v.setStyleSheet("color: #f1f5f9; font-size: 12px;")
            r.addWidget(l)
            r.addStretch()
            r.addWidget(v)
            meta_layout.addLayout(r)

        add_meta_row("Rozlišení", self.item.resolution)
        add_meta_row("Poměr stran", self.item.ratio)
        add_meta_row("Velikost souboru", self.item.human_file_size)
        add_meta_row("Formát", self.item.file_type or "image/jpeg")
        add_meta_row("Kategorie", self.item.category.capitalize())
        add_meta_row("Purity", self.item.purity.upper())
        add_meta_row("Zobrazení", f"{self.item.views:,}")
        add_meta_row("Oblíbené", f"★ {self.item.favorites:,}")

        sidebar_layout.addWidget(meta_frame)

        # Colors row
        if self.item.colors:
            colors_title = QLabel("Barevná paleta:")
            colors_title.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
            sidebar_layout.addWidget(colors_title)

            colors_layout = QHBoxLayout()
            colors_layout.setSpacing(4)
            for c in self.item.colors:
                color_chip = QLabel()
                color_chip.setFixedSize(24, 18)
                color_chip.setStyleSheet(f"background-color: {c}; border-radius: 3px; border: 1px solid #333845;")
                color_chip.setToolTip(c)
                colors_layout.addWidget(color_chip)
            colors_layout.addStretch()
            sidebar_layout.addLayout(colors_layout)

        # Tags Section with scroll
        tags_title = QLabel("Štítky (Tags):")
        tags_title.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        sidebar_layout.addWidget(tags_title)

        tags_scroll = QScrollArea()
        tags_scroll.setWidgetResizable(True)
        tags_scroll.setFixedHeight(120)
        tags_scroll.setStyleSheet("background: #181a21; border-radius: 6px; border: 1px solid #2d313b;")

        self.tags_container = QWidget()
        self.tags_layout = QVBoxLayout(self.tags_container)
        self.tags_layout.setContentsMargins(6, 6, 6, 6)
        self.tags_layout.setSpacing(4)
        self.tags_status_lbl = QLabel("Načítání štítků...")
        self.tags_status_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        self.tags_layout.addWidget(self.tags_status_lbl)
        self.tags_layout.addStretch()

        tags_scroll.setWidget(self.tags_container)
        sidebar_layout.addWidget(tags_scroll)

        sidebar_layout.addStretch()

        # Download Section
        dl_frame = QFrame()
        dl_frame.setStyleSheet("background: #21242d; border-radius: 6px; padding: 10px;")
        dl_layout = QVBoxLayout(dl_frame)
        dl_layout.setSpacing(8)

        self.dl_btn = QPushButton("⬇ Stáhnout tapetu")
        self.dl_btn.setObjectName("primaryButton")
        self.dl_btn.setFixedHeight(38)
        self.dl_btn.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.dl_btn.clicked.connect(self._on_download_clicked)
        dl_layout.addWidget(self.dl_btn)

        self.set_wall_cb = QCheckBox("Nastavit jako tapetu po stažení")
        self.set_wall_cb.setChecked(config.auto_set_wallpaper)
        self.set_wall_cb.setStyleSheet("color: #cbd5e1; font-size: 11px;")
        dl_layout.addWidget(self.set_wall_cb)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        dl_layout.addWidget(self.progress_bar)

        self.dl_status_lbl = QLabel("")
        self.dl_status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dl_status_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
        self.dl_status_lbl.setVisible(False)
        dl_layout.addWidget(self.dl_status_lbl)

        self.set_wall_now_btn = QPushButton("🖼️ Nastavit jako tapetu nyní")
        self.set_wall_now_btn.setVisible(False)
        self.set_wall_now_btn.clicked.connect(self._on_set_wall_now)
        dl_layout.addWidget(self.set_wall_now_btn)

        self.open_folder_btn = QPushButton("📁 Otevřít ve složce")
        self.open_folder_btn.setVisible(False)
        self.open_folder_btn.clicked.connect(self._on_open_folder)
        dl_layout.addWidget(self.open_folder_btn)

        sidebar_layout.addWidget(dl_frame)

        main_layout.addWidget(sidebar)

    def _load_preview(self):
        # We can use large thumb or full image
        url = self.item.thumb_large or self.item.thumb_original or self.item.thumb_small
        if not url:
            return

        self._connected = True
        loader.image_loaded.connect(self._on_preview_loaded)
        if loader.load_image(url, is_thumb=True):
            pm = loader.cache.get_pixmap(url, is_thumb=True)
            if pm:
                self._update_preview(pm)

    def _cleanup_signal(self):
        if getattr(self, "_connected", False):
            try:
                loader.image_loaded.disconnect(self._on_preview_loaded)
            except Exception:
                pass
            self._connected = False

    def _on_preview_loaded(self, url: str, pixmap: QPixmap):
        target_url = self.item.thumb_large or self.item.thumb_original or self.item.thumb_small
        if url == target_url:
            self._cleanup_signal()
            self._update_preview(pixmap)

    def closeEvent(self, event):
        self._cleanup_signal()
        super().closeEvent(event)

    def _update_preview(self, pixmap: QPixmap):
        # Scale nicely to fit preview label
        lbl_size = self.preview_label.size()
        w = max(400, lbl_size.width())
        h = max(300, lbl_size.height())
        scaled = pixmap.scaled(
            QSize(w, h),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setPixmap(scaled)
        self.preview_label.setText("")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Re-scale preview on dialog resize
        target_url = self.item.thumb_large or self.item.thumb_original or self.item.thumb_small
        pm = loader.cache.get_pixmap(target_url, is_thumb=True)
        if pm and not pm.isNull():
            self._update_preview(pm)

    def _fetch_full_details(self):
        self.fetch_worker = DetailFetchWorker(self.item.id)
        self.fetch_worker.finished.connect(self._on_details_fetched)
        self.fetch_worker.failed.connect(lambda err: self.tags_status_lbl.setText("Štítky nedostupné"))
        self.fetch_worker.start()

    def _on_details_fetched(self, full_item: WallpaperItem):
        self.item = full_item
        # Clear tags status
        while self.tags_layout.count():
            child = self.tags_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if full_item.tags:
            for tag in full_item.tags:
                tag_name = tag.get("name", "")
                tag_btn = QPushButton(f"#{tag_name}")
                tag_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                tag_btn.setStyleSheet("""
                    QPushButton {
                        background: #252833;
                        color: #a5b4fc;
                        border: 1px solid #3b3f4d;
                        border-radius: 4px;
                        padding: 3px 6px;
                        font-size: 11px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background: #312e81;
                        color: #ffffff;
                        border-color: #6366f1;
                    }
                """)
                tag_btn.clicked.connect(lambda checked, t=tag_name: self._on_tag_clicked(t))
                self.tags_layout.addWidget(tag_btn)
        else:
            no_tags = QLabel("Žádné štítky")
            no_tags.setStyleSheet("color: #64748b; font-size: 11px;")
            self.tags_layout.addWidget(no_tags)

        self.tags_layout.addStretch()

    def _on_tag_clicked(self, tag_name: str):
        self.tag_clicked.emit(tag_name)
        self.accept()

    def _open_in_browser(self):
        if self.item.url:
            QDesktopServices.openUrl(QUrl(self.item.url))

    def _on_download_clicked(self):
        ext = os.path.splitext(self.item.path)[1] or ".jpg"
        suggested_name = f"wallhaven-{self.item.id}{ext}"
        default_dir = Path(config.default_download_dir)
        default_dir.mkdir(parents=True, exist_ok=True)
        initial_path = str(default_dir / suggested_name)

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Uložit tapetu jako...",
            initial_path,
            f"Obrázky (*{ext});;Všechny soubory (*)",
        )

        if not save_path:
            return

        self.dl_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.dl_status_lbl.setVisible(True)
        self.dl_status_lbl.setText("Stahování v plném rozlišení...")

        self.download_worker = DownloadWorker(self.item.path, save_path)
        self.download_worker.progress.connect(self._on_download_progress)
        self.download_worker.finished.connect(self._on_download_finished)
        self.download_worker.failed.connect(self._on_download_failed)
        self.download_worker.start()

    def _on_download_progress(self, downloaded: int, total: int):
        if total > 0:
            pct = int((downloaded / total) * 100)
            self.progress_bar.setValue(pct)
            mb_cur = downloaded / (1024 * 1024)
            mb_tot = total / (1024 * 1024)
            self.dl_status_lbl.setText(f"{mb_cur:.1f} MB / {mb_tot:.1f} MB ({pct}%)")
        else:
            self.progress_bar.setRange(0, 0)  # indeterminate

    def _on_download_finished(self, saved_path: str):
        self.saved_path = saved_path
        self.progress_bar.setVisible(False)
        self.dl_btn.setEnabled(True)
        self.dl_btn.setText("✓ Staženo")
        self.dl_btn.setStyleSheet("background: #059669; color: white;")

        # Automatically set desktop wallpaper if requested
        if self.set_wall_cb.isChecked():
            ok, msg = set_desktop_wallpaper(saved_path, config.custom_wallpaper_cmd)
            if ok:
                self.dl_status_lbl.setText("✓ Uloženo a nastaveno na plochu!")
                self.dl_status_lbl.setStyleSheet("color: #34d399; font-size: 11px; font-weight: bold;")
            else:
                self.dl_status_lbl.setText(f"Uloženo, ale tapetu nelze nastavit: {msg}")
                self.dl_status_lbl.setStyleSheet("color: #fbbf24; font-size: 11px;")
        else:
            self.dl_status_lbl.setText(f"Uloženo: {os.path.basename(saved_path)}")
            self.dl_status_lbl.setStyleSheet("color: #34d399; font-size: 11px;")

        self.set_wall_now_btn.setVisible(True)
        self.open_folder_btn.setVisible(True)
        self.download_completed.emit(saved_path)

    def _on_set_wall_now(self):
        if self.saved_path and os.path.exists(self.saved_path):
            ok, msg = set_desktop_wallpaper(self.saved_path, config.custom_wallpaper_cmd)
            if ok:
                self.dl_status_lbl.setText("✓ Nastaveno jako tapeta plochy!")
                self.dl_status_lbl.setStyleSheet("color: #34d399; font-size: 11px; font-weight: bold;")
                QMessageBox.information(self, "Úspěch", "Tapeta byla úspěšně nastavena na plochu!")
            else:
                QMessageBox.warning(self, "Chyba", f"Nepodařilo se nastavit tapetu:\n{msg}")

    def _on_download_failed(self, error: str):
        self.progress_bar.setVisible(False)
        self.dl_btn.setEnabled(True)
        self.dl_status_lbl.setText(f"Chyba: {error}")
        self.dl_status_lbl.setStyleSheet("color: #f87171; font-size: 11px;")
        QMessageBox.critical(self, "Chyba při stahování", f"Tapetu se nepodařilo stáhnout:\n{error}")

    def _on_open_folder(self):
        if self.saved_path and os.path.exists(self.saved_path):
            folder = os.path.dirname(self.saved_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
