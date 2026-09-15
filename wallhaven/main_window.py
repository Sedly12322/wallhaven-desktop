import os
from pathlib import Path
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QScrollArea,
    QFrame,
    QMessageBox,
    QFileDialog,
    QSpinBox,
    QStatusBar,
    QApplication,
)
from wallhaven.api import WallpaperItem, SearchResult, api
from wallhaven.config import config
from wallhaven.widgets.grid_widget import WallpaperGridWidget
from wallhaven.widgets.color_bar import ColorBar
from wallhaven.widgets.detail_dialog import DetailDialog, DownloadWorker
from wallhaven.widgets.settings_dialog import SettingsDialog
from wallhaven.wallpaper import set_desktop_wallpaper


class SearchWorker(QThread):
    finished = pyqtSignal(SearchResult)
    failed = pyqtSignal(str)

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    def run(self):
        try:
            res = api.search(**self.kwargs)
            self.finished.emit(res)
        except Exception as e:
            self.failed.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallhaven Desktop")
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)

        self.current_page = 1
        self.last_page = 1
        self.current_color = ""
        self.active_search_worker: SearchWorker | None = None
        self.quick_download_worker: DownloadWorker | None = None

        self._init_ui()
        self.perform_search(page=1)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Top Header
        header = QFrame()
        header.setObjectName("headerPanel")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 8, 16, 8)
        h_layout.setSpacing(12)

        logo = QLabel("🌌 <b>Wallhaven</b>")
        logo.setStyleSheet("font-size: 18px; color: #818cf8; letter-spacing: 0.5px;")
        h_layout.addWidget(logo)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Hledat tapety... (např. cyberpunk, anime, nature, minimal, landscape)")
        self.search_input.returnPressed.connect(self._on_search_triggered)
        self.search_input.setClearButtonEnabled(True)
        h_layout.addWidget(self.search_input, stretch=1)

        self.search_btn = QPushButton("Hledat")
        self.search_btn.setObjectName("primaryButton")
        self.search_btn.clicked.connect(self._on_search_triggered)
        h_layout.addWidget(self.search_btn)

        # Toggle Color Bar button
        self.color_toggle_btn = QPushButton("🎨 Barvy")
        self.color_toggle_btn.setCheckable(True)
        self.color_toggle_btn.clicked.connect(self._toggle_color_bar)
        h_layout.addWidget(self.color_toggle_btn)

        # Auto-wallpaper toggle button
        self.auto_wall_btn = QPushButton("🖼️ Auto-tapeta")
        self.auto_wall_btn.setCheckable(True)
        self.auto_wall_btn.setChecked(config.auto_set_wallpaper)
        self.auto_wall_btn.setToolTip("Při stažení automaticky nastavit tapetu na plochu")
        self.auto_wall_btn.clicked.connect(self._on_auto_wall_toggled)
        h_layout.addWidget(self.auto_wall_btn)

        # Settings button
        settings_btn = QPushButton("⚙ Nastavení")
        settings_btn.clicked.connect(self._open_settings)
        h_layout.addWidget(settings_btn)

        main_layout.addWidget(header)

        # 2. Filter Bar
        filter_bar = QFrame()
        filter_bar.setObjectName("filterPanel")
        f_layout = QHBoxLayout(filter_bar)
        f_layout.setContentsMargins(16, 6, 16, 6)
        f_layout.setSpacing(10)

        # Category Chips
        cat_lbl = QLabel("Kategorie:")
        cat_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(cat_lbl)

        self.cat_general = QPushButton("General")
        self.cat_general.setObjectName("filterChip")
        self.cat_general.setCheckable(True)
        self.cat_general.setChecked(True)
        self.cat_general.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_general)

        self.cat_anime = QPushButton("Anime")
        self.cat_anime.setObjectName("filterChip")
        self.cat_anime.setCheckable(True)
        self.cat_anime.setChecked(True)
        self.cat_anime.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_anime)

        self.cat_people = QPushButton("People")
        self.cat_people.setObjectName("filterChip")
        self.cat_people.setCheckable(True)
        self.cat_people.setChecked(True)
        self.cat_people.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_people)

        f_layout.addSpacing(8)

        # Purity Chips
        pur_lbl = QLabel("Purity:")
        pur_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(pur_lbl)

        self.pur_sfw = QPushButton("SFW")
        self.pur_sfw.setObjectName("filterChip")
        self.pur_sfw.setCheckable(True)
        self.pur_sfw.setChecked(True)
        self.pur_sfw.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.pur_sfw)

        self.pur_sketchy = QPushButton("Sketchy")
        self.pur_sketchy.setObjectName("sketchyChip")
        self.pur_sketchy.setCheckable(True)
        self.pur_sketchy.setChecked(False)
        self.pur_sketchy.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.pur_sketchy)

        self.pur_nsfw = QPushButton("NSFW")
        self.pur_nsfw.setObjectName("nsfwChip")
        self.pur_nsfw.setCheckable(True)
        self.pur_nsfw.setChecked(False)
        self.pur_nsfw.clicked.connect(self._on_nsfw_clicked)
        f_layout.addWidget(self.pur_nsfw)

        f_layout.addSpacing(8)

        # Sorting combo
        sort_lbl = QLabel("Řazení:")
        sort_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(sort_lbl)

        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Toplist (Nejlepší)", "toplist")
        self.sort_combo.addItem("Hot (Populární)", "hot")
        self.sort_combo.addItem("Nejnovější", "date_added")
        self.sort_combo.addItem("Zhlédnutí", "views")
        self.sort_combo.addItem("Oblíbené", "favorites")
        self.sort_combo.addItem("Náhodné", "random")
        self.sort_combo.addItem("Relevance", "relevance")
        self.sort_combo.currentIndexChanged.connect(self._on_sorting_changed)
        f_layout.addWidget(self.sort_combo)

        # Top Range combo
        self.range_combo = QComboBox()
        self.range_combo.addItem("1 Měsíc", "1M")
        self.range_combo.addItem("1 Den", "1d")
        self.range_combo.addItem("3 Dny", "3d")
        self.range_combo.addItem("1 Týden", "1w")
        self.range_combo.addItem("3 Měsíce", "3M")
        self.range_combo.addItem("6 Měsíců", "6M")
        self.range_combo.addItem("1 Rok", "1y")
        self.range_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.range_combo)

        # Aspect Ratio combo
        self.ratio_combo = QComboBox()
        self.ratio_combo.addItem("Jakýkoliv poměr", "")
        self.ratio_combo.addItem("16:9 (Standard)", "16x9")
        self.ratio_combo.addItem("16:10", "16x10")
        self.ratio_combo.addItem("21:9 (Ultrawide)", "21x9")
        self.ratio_combo.addItem("32:9 (Super Ultrawide)", "32x9")
        self.ratio_combo.addItem("9:16 (Mobilní)", "9x16")
        self.ratio_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.ratio_combo)

        # Min Resolution combo
        self.res_combo = QComboBox()
        self.res_combo.addItem("Jakékoliv rozlišení", "")
        self.res_combo.addItem("1080p (≥ 1920x1080)", "1920x1080")
        self.res_combo.addItem("1440p (≥ 2560x1440)", "2560x1440")
        self.res_combo.addItem("4K UHD (≥ 3840x2160)", "3840x2160")
        self.res_combo.addItem("8K UHD (≥ 7680x4320)", "7680x4320")
        self.res_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.res_combo)

        f_layout.addStretch()
        main_layout.addWidget(filter_bar)

        # 3. Color Bar (Collapsible)
        self.color_bar = ColorBar()
        self.color_bar.setVisible(False)
        self.color_bar.color_changed.connect(self._on_color_changed)
        main_layout.addWidget(self.color_bar)

        # 4. Scrollable Wallpaper Grid Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.grid_widget = WallpaperGridWidget()
        self.grid_widget.card_clicked.connect(self._on_card_clicked)
        self.grid_widget.download_requested.connect(self._on_quick_download)
        self.scroll_area.setWidget(self.grid_widget)
        main_layout.addWidget(self.scroll_area, stretch=1)

        # 5. Pagination Bar
        self.pagination_frame = QFrame()
        self.pagination_frame.setObjectName("headerPanel")
        p_layout = QHBoxLayout(self.pagination_frame)
        p_layout.setContentsMargins(16, 6, 16, 6)
        p_layout.setSpacing(8)

        self.first_btn = QPushButton("« První")
        self.first_btn.clicked.connect(lambda: self.perform_search(page=1))
        p_layout.addWidget(self.first_btn)

        self.prev_btn = QPushButton("‹ Předchozí")
        self.prev_btn.clicked.connect(lambda: self.perform_search(page=self.current_page - 1))
        p_layout.addWidget(self.prev_btn)

        self.page_info_lbl = QLabel("Stránka 1 z 1")
        self.page_info_lbl.setStyleSheet("font-weight: bold; color: #f1f5f9; padding: 0 10px;")
        p_layout.addWidget(self.page_info_lbl)

        self.next_btn = QPushButton("Další ›")
        self.next_btn.clicked.connect(lambda: self.perform_search(page=self.current_page + 1))
        p_layout.addWidget(self.next_btn)

        self.last_btn = QPushButton("Poslední »")
        self.last_btn.clicked.connect(lambda: self.perform_search(page=self.last_page))
        p_layout.addWidget(self.last_btn)

        p_layout.addSpacing(16)
        goto_lbl = QLabel("Přejít na:")
        goto_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        p_layout.addWidget(goto_lbl)

        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 9999)
        self.page_spin.setValue(1)
        p_layout.addWidget(self.page_spin)

        goto_btn = QPushButton("Přejít")
        goto_btn.clicked.connect(lambda: self.perform_search(page=self.page_spin.value()))
        p_layout.addWidget(goto_btn)

        p_layout.addStretch()

        self.total_count_lbl = QLabel("Nalezeno: 0 tapet")
        self.total_count_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        p_layout.addWidget(self.total_count_lbl)

        main_layout.addWidget(self.pagination_frame)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Připraveno")

    def _toggle_color_bar(self):
        is_visible = self.color_toggle_btn.isChecked()
        self.color_bar.setVisible(is_visible)

    def _on_color_changed(self, hex_code: str):
        self.current_color = hex_code
        self.perform_search(page=1)

    def _on_sorting_changed(self):
        sort_val = self.sort_combo.currentData()
        # Only show top_range when sort is toplist
        self.range_combo.setVisible(sort_val == "toplist")
        self.perform_search(page=1)

    def _on_filter_changed(self):
        self.perform_search(page=1)

    def _on_nsfw_clicked(self):
        if self.pur_nsfw.isChecked() and not config.api_key:
            res = QMessageBox.question(
                self,
                "Vyžadován API klíč",
                "Pro zobrazení NSFW tapet vyžaduje Wallhaven API klíč.\n\n"
                "Chcete nyní otevřít nastavení a zadat svůj API klíč?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if res == QMessageBox.StandardButton.Yes:
                self._open_settings()
            if not config.api_key:
                self.pur_nsfw.setChecked(False)
                return
        self.perform_search(page=1)

    def _open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            self.auto_wall_btn.setChecked(config.auto_set_wallpaper)
            # If API key changed, refresh
            self.perform_search(page=self.current_page)

    def _on_auto_wall_toggled(self):
        config.auto_set_wallpaper = self.auto_wall_btn.isChecked()
        status = "Zapnuto" if config.auto_set_wallpaper else "Vypnuto"
        self.status_bar.showMessage(f"Automatické nastavení tapety po stažení: {status}", 4000)

    def _on_search_triggered(self):
        self.perform_search(page=1)

    def _get_categories_str(self) -> str:
        g = "1" if self.cat_general.isChecked() else "0"
        a = "1" if self.cat_anime.isChecked() else "0"
        p = "1" if self.cat_people.isChecked() else "0"
        # If none checked, default to all
        if g == "0" and a == "0" and p == "0":
            return "111"
        return f"{g}{a}{p}"

    def _get_purity_str(self) -> str:
        s = "1" if self.pur_sfw.isChecked() else "0"
        k = "1" if self.pur_sketchy.isChecked() else "0"
        n = "1" if (self.pur_nsfw.isChecked() and config.api_key) else "0"
        if s == "0" and k == "0" and n == "0":
            return "100"
        return f"{s}{k}{n}"

    def perform_search(self, page: int = 1):
        if page < 1:
            page = 1

        self.status_bar.showMessage(f"Vyhledávání tapet (stránka {page})...")
        self.search_btn.setEnabled(False)

        # Cancel any active search
        if self.active_search_worker and self.active_search_worker.isRunning():
            self.active_search_worker.terminate()

        query = self.search_input.text().strip()
        cats = self._get_categories_str()
        purity = self._get_purity_str()
        sorting = self.sort_combo.currentData()
        top_range = self.range_combo.currentData() if sorting == "toplist" else ""
        ratios = self.ratio_combo.currentData()
        atleast = self.res_combo.currentData()
        colors = self.current_color

        self.active_search_worker = SearchWorker(
            query=query,
            categories=cats,
            purity=purity,
            sorting=sorting,
            top_range=top_range,
            ratios=ratios,
            atleast=atleast,
            colors=colors,
            page=page,
        )
        self.active_search_worker.finished.connect(self._on_search_success)
        self.active_search_worker.failed.connect(self._on_search_failed)
        self.active_search_worker.start()

    def _on_search_success(self, result: SearchResult):
        self.search_btn.setEnabled(True)
        self.current_page = result.current_page
        self.last_page = max(1, result.last_page)

        self.grid_widget.set_items(result.items)
        # Scroll back to top
        self.scroll_area.verticalScrollBar().setValue(0)

        # Update pagination
        self.page_info_lbl.setText(f"Stránka {self.current_page} z {self.last_page}")
        self.page_spin.setRange(1, self.last_page)
        self.page_spin.setValue(self.current_page)
        self.total_count_lbl.setText(f"Nalezeno: {result.total:,} tapet")

        self.prev_btn.setEnabled(self.current_page > 1)
        self.first_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.last_page)
        self.last_btn.setEnabled(self.current_page < self.last_page)

        self.status_bar.showMessage(f"Načteno {len(result.items)} tapet. Celkem výsledků: {result.total:,}")

    def _on_search_failed(self, error: str):
        self.search_btn.setEnabled(True)
        self.status_bar.showMessage(f"Chyba vyhledávání: {error}")
        QMessageBox.warning(self, "Chyba načítání", f"Nepodařilo se načíst tapety z Wallhaven:\n{error}")

    def _on_card_clicked(self, item: WallpaperItem):
        dlg = DetailDialog(item, self)
        dlg.tag_clicked.connect(self._search_by_tag)
        dlg.download_completed.connect(self._on_download_completed)
        dlg.exec()

    def _search_by_tag(self, tag_name: str):
        self.search_input.setText(tag_name)
        self.perform_search(page=1)

    def _on_quick_download(self, item: WallpaperItem):
        # User requested quick download from card button
        # Respect user requirement: "Při každém stažení se zeptat dialogem na umístění"
        ext = os.path.splitext(item.path)[1] or ".jpg"
        suggested_name = f"wallhaven-{item.id}{ext}"
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

        self.status_bar.showMessage(f"Stahování tapety #{item.id} do {os.path.basename(save_path)}...")

        self.quick_download_worker = DownloadWorker(item.path, save_path)
        self.quick_download_worker.progress.connect(
            lambda cur, tot: self.status_bar.showMessage(
                f"Stahování tapety #{item.id}: {cur // (1024*1024)} MB / {tot // (1024*1024)} MB..."
            )
        )
        self.quick_download_worker.finished.connect(
            lambda path: self._on_download_completed(path)
        )
        self.quick_download_worker.failed.connect(
            lambda err: QMessageBox.critical(self, "Chyba", f"Nepodařilo se stáhnout tapetu: {err}")
        )
        self.quick_download_worker.start()

    def _on_download_completed(self, path: str):
        filename = os.path.basename(path)
        if config.auto_set_wallpaper:
            ok, msg = set_desktop_wallpaper(path, config.custom_wallpaper_cmd)
            if ok:
                self.status_bar.showMessage(f"✓ Tapeta {filename} byla uložena a nastavena na plochu!", 8000)
            else:
                self.status_bar.showMessage(f"✓ Uloženo: {filename} (chyba nastavení tapety: {msg})", 8000)
        else:
            self.status_bar.showMessage(f"✓ Tapeta byla úspěšně uložena: {filename}", 8000)
