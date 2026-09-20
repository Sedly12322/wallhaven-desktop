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
from wallhaven.osu import osu_manager
from wallhaven.moewalls import moewalls_manager
from wallhaven.config import config
from wallhaven.i18n import tr, i18n
from wallhaven.widgets.grid_widget import WallpaperGridWidget
from wallhaven.widgets.color_bar import ColorBar
from wallhaven.widgets.detail_dialog import DetailDialog, DownloadWorker
from wallhaven.widgets.settings_dialog import SettingsDialog
from wallhaven.wallpaper import set_desktop_wallpaper


class SearchWorker(QThread):
    finished = pyqtSignal(int, SearchResult)
    failed = pyqtSignal(int, str)

    def __init__(self, search_id: int, **kwargs):
        super().__init__()
        self.search_id = search_id
        self.kwargs = kwargs

    def run(self):
        try:
            res = api.search(**self.kwargs)
            self.finished.emit(self.search_id, res)
        except Exception as e:
            self.failed.emit(self.search_id, str(e))


class OsuSearchWorker(QThread):
    finished = pyqtSignal(int, SearchResult)
    failed = pyqtSignal(int, str)

    def __init__(self, search_id: int, **kwargs):
        super().__init__()
        self.search_id = search_id
        self.kwargs = kwargs

    def run(self):
        try:
            res = osu_manager.search(**self.kwargs)
            self.finished.emit(self.search_id, res)
        except Exception as e:
            self.failed.emit(self.search_id, str(e))


class MoeSearchWorker(QThread):
    finished = pyqtSignal(int, SearchResult)
    failed = pyqtSignal(int, str)

    def __init__(self, search_id: int, **kwargs):
        super().__init__()
        self.search_id = search_id
        self.kwargs = kwargs

    def run(self):
        try:
            res = moewalls_manager.search(**self.kwargs)
            self.finished.emit(self.search_id, res)
        except Exception as e:
            self.failed.emit(self.search_id, str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)

        self.current_mode = "wallhaven"
        self.osu_theme = "all"
        self.current_search_id = 0

        self.current_page = 1
        self.last_page = 1
        self.total_count = 0
        self.current_color = ""
        self.active_search_worker: SearchWorker | OsuSearchWorker | None = None
        self.quick_download_worker: DownloadWorker | None = None

        self._init_ui()
        i18n.language_changed.connect(self.retranslate_ui)
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

        # Navigation Mode Tabs: [ Wallhaven ] [ osu! Seasonal ]
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(6)

        self.tab_wallhaven = QPushButton()
        self.tab_wallhaven.setObjectName("navTab")
        self.tab_wallhaven.setCheckable(True)
        self.tab_wallhaven.setChecked(True)
        self.tab_wallhaven.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tab_wallhaven.clicked.connect(lambda: self._set_mode("wallhaven"))
        tabs_layout.addWidget(self.tab_wallhaven)

        self.tab_moewalls = QPushButton()
        self.tab_moewalls.setObjectName("navTab")
        self.tab_moewalls.setCheckable(True)
        self.tab_moewalls.setChecked(False)
        self.tab_moewalls.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tab_moewalls.clicked.connect(lambda: self._set_mode("moewalls"))
        tabs_layout.addWidget(self.tab_moewalls)

        self.tab_osu = QPushButton()
        self.tab_osu.setObjectName("navTab")
        self.tab_osu.setCheckable(True)
        self.tab_osu.setChecked(False)
        self.tab_osu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tab_osu.clicked.connect(lambda: self._set_mode("osu"))
        tabs_layout.addWidget(self.tab_osu)

        h_layout.addLayout(tabs_layout)

        # Search box
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self._on_search_triggered)
        self.search_input.setClearButtonEnabled(True)
        h_layout.addWidget(self.search_input, stretch=1)

        self.search_btn = QPushButton()
        self.search_btn.setObjectName("primaryButton")
        self.search_btn.clicked.connect(self._on_search_triggered)
        h_layout.addWidget(self.search_btn)

        # Toggle Color Bar button (Wallhaven only)
        self.color_toggle_btn = QPushButton()
        self.color_toggle_btn.setCheckable(True)
        self.color_toggle_btn.clicked.connect(self._toggle_color_bar)
        h_layout.addWidget(self.color_toggle_btn)

        # Auto-wallpaper toggle button
        self.auto_wall_btn = QPushButton()
        self.auto_wall_btn.setCheckable(True)
        self.auto_wall_btn.setChecked(config.auto_set_wallpaper)
        self.auto_wall_btn.clicked.connect(self._on_auto_wall_toggled)
        h_layout.addWidget(self.auto_wall_btn)

        # Settings button
        self.settings_btn = QPushButton()
        self.settings_btn.clicked.connect(self._open_settings)
        h_layout.addWidget(self.settings_btn)

        main_layout.addWidget(header)

        # 2A. Wallhaven Filter Bar
        self.wallhaven_filter_bar = QFrame()
        self.wallhaven_filter_bar.setObjectName("filterPanel")
        f_layout = QHBoxLayout(self.wallhaven_filter_bar)
        f_layout.setContentsMargins(16, 6, 16, 6)
        f_layout.setSpacing(10)

        # Category Chips
        self.cat_lbl = QLabel()
        self.cat_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(self.cat_lbl)

        self.cat_general = QPushButton()
        self.cat_general.setObjectName("filterChip")
        self.cat_general.setCheckable(True)
        self.cat_general.setChecked(True)
        self.cat_general.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_general)

        self.cat_anime = QPushButton()
        self.cat_anime.setObjectName("filterChip")
        self.cat_anime.setCheckable(True)
        self.cat_anime.setChecked(True)
        self.cat_anime.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_anime)

        self.cat_people = QPushButton()
        self.cat_people.setObjectName("filterChip")
        self.cat_people.setCheckable(True)
        self.cat_people.setChecked(True)
        self.cat_people.clicked.connect(self._on_filter_changed)
        f_layout.addWidget(self.cat_people)

        f_layout.addSpacing(8)

        # Purity Chips
        self.pur_lbl = QLabel()
        self.pur_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(self.pur_lbl)

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
        self.sort_lbl = QLabel()
        self.sort_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        f_layout.addWidget(self.sort_lbl)

        self.sort_combo = QComboBox()
        self.sort_combo.currentIndexChanged.connect(self._on_sorting_changed)
        f_layout.addWidget(self.sort_combo)

        # Top Range combo
        self.range_combo = QComboBox()
        self.range_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.range_combo)

        # Aspect Ratio combo
        self.ratio_combo = QComboBox()
        self.ratio_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.ratio_combo)

        # Min Resolution combo
        self.res_combo = QComboBox()
        self.res_combo.currentIndexChanged.connect(self._on_filter_changed)
        f_layout.addWidget(self.res_combo)

        f_layout.addStretch()
        main_layout.addWidget(self.wallhaven_filter_bar)

        # 2B. osu! Seasonal Filter Bar
        self.osu_filter_bar = QFrame()
        self.osu_filter_bar.setObjectName("filterPanel")
        self.osu_filter_bar.setVisible(False)
        osu_layout = QHBoxLayout(self.osu_filter_bar)
        osu_layout.setContentsMargins(16, 6, 16, 6)
        osu_layout.setSpacing(10)

        # Season selector
        self.osu_season_lbl = QLabel()
        self.osu_season_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        osu_layout.addWidget(self.osu_season_lbl)

        self.osu_season_combo = QComboBox()
        self.osu_season_combo.currentIndexChanged.connect(self._on_osu_filter_changed)
        osu_layout.addWidget(self.osu_season_combo)

        osu_layout.addSpacing(8)

        # Theme chips
        self.osu_theme_lbl = QLabel()
        self.osu_theme_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        osu_layout.addWidget(self.osu_theme_lbl)

        self.theme_chips: dict[str, QPushButton] = {}
        themes = [
            ("all", "theme_all"),
            ("Spring", "theme_spring"),
            ("Summer", "theme_summer"),
            ("Autumn", "theme_autumn"),
            ("Winter", "theme_winter"),
            ("Halloween", "theme_halloween"),
        ]
        for key, tr_key in themes:
            btn = QPushButton()
            btn.setObjectName("themeChip")
            btn.setCheckable(True)
            if key == "all":
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, k=key: self._on_osu_theme_clicked(k))
            osu_layout.addWidget(btn)
            self.theme_chips[key] = btn

        osu_layout.addSpacing(8)

        # Sorting combo
        self.osu_sort_lbl = QLabel()
        self.osu_sort_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        osu_layout.addWidget(self.osu_sort_lbl)

        self.osu_sort_combo = QComboBox()
        self.osu_sort_combo.currentIndexChanged.connect(self._on_osu_filter_changed)
        osu_layout.addWidget(self.osu_sort_combo)

        osu_layout.addStretch()
        main_layout.addWidget(self.osu_filter_bar)

        # 2C. MoeWalls (Live Wallpapers) Filter Bar
        self.moe_filter_bar = QFrame()
        self.moe_filter_bar.setObjectName("filterPanel")
        self.moe_filter_bar.setVisible(False)
        moe_layout = QHBoxLayout(self.moe_filter_bar)
        moe_layout.setContentsMargins(16, 6, 16, 6)
        moe_layout.setSpacing(10)

        self.moe_cat_lbl = QLabel(tr("moe_category_label"))
        self.moe_cat_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        moe_layout.addWidget(self.moe_cat_lbl)

        self.moe_cat_combo = QComboBox()
        self.moe_cat_combo.setMinimumWidth(160)
        for cat_id, cat_name in moewalls_manager.get_categories():
            self.moe_cat_combo.addItem(cat_name, cat_id)
        self.moe_cat_combo.currentIndexChanged.connect(lambda: self.perform_search(page=1))
        moe_layout.addWidget(self.moe_cat_combo)

        moe_badge = QLabel("🎬 20 000+ 2K / 4K 60FPS Video Wallpapers (MP4)")
        moe_badge.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: bold; margin-left: 8px;")
        moe_layout.addWidget(moe_badge)

        moe_layout.addStretch()
        main_layout.addWidget(self.moe_filter_bar)

        # 3. Color Bar (Collapsible, Wallhaven only)
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

        self.first_btn = QPushButton()
        self.first_btn.clicked.connect(lambda: self.perform_search(page=1))
        p_layout.addWidget(self.first_btn)

        self.prev_btn = QPushButton()
        self.prev_btn.clicked.connect(lambda: self.perform_search(page=self.current_page - 1))
        p_layout.addWidget(self.prev_btn)

        self.page_info_lbl = QLabel()
        self.page_info_lbl.setStyleSheet("font-weight: bold; color: #f1f5f9; padding: 0 10px;")
        p_layout.addWidget(self.page_info_lbl)

        self.next_btn = QPushButton()
        self.next_btn.clicked.connect(lambda: self.perform_search(page=self.current_page + 1))
        p_layout.addWidget(self.next_btn)

        self.last_btn = QPushButton()
        self.last_btn.clicked.connect(lambda: self.perform_search(page=self.last_page))
        p_layout.addWidget(self.last_btn)

        p_layout.addSpacing(16)
        self.goto_lbl = QLabel()
        self.goto_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        p_layout.addWidget(self.goto_lbl)

        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 9999)
        self.page_spin.setValue(1)
        p_layout.addWidget(self.page_spin)

        self.goto_btn = QPushButton()
        self.goto_btn.clicked.connect(lambda: self.perform_search(page=self.page_spin.value()))
        p_layout.addWidget(self.goto_btn)

        p_layout.addStretch()

        self.total_count_lbl = QLabel()
        self.total_count_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        p_layout.addWidget(self.total_count_lbl)

        main_layout.addWidget(self.pagination_frame)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.retranslate_ui()
        self.status_bar.showMessage(tr("status_ready"))

    def _retranslate_combos(self):
        def _populate(combo: QComboBox, items: list[tuple[str, str]]):
            cur = combo.currentData()
            combo.blockSignals(True)
            combo.clear()
            for text, val in items:
                combo.addItem(text, val)
            if cur is not None:
                idx = combo.findData(cur)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
            combo.blockSignals(False)

        _populate(self.sort_combo, [
            (tr("sort_toplist"), "toplist"),
            (tr("sort_hot"), "hot"),
            (tr("sort_latest"), "date_added"),
            (tr("sort_views"), "views"),
            (tr("sort_favorites"), "favorites"),
            (tr("sort_random"), "random"),
            (tr("sort_relevance"), "relevance"),
        ])

        _populate(self.range_combo, [
            (tr("range_1M"), "1M"),
            (tr("range_1d"), "1d"),
            (tr("range_3d"), "3d"),
            (tr("range_1w"), "1w"),
            (tr("range_3M"), "3M"),
            (tr("range_6M"), "6M"),
            (tr("range_1y"), "1y"),
        ])

        _populate(self.ratio_combo, [
            (tr("ratio_any"), ""),
            (tr("ratio_16x9"), "16x9"),
            (tr("ratio_16x10"), "16x10"),
            (tr("ratio_21x9"), "21x9"),
            (tr("ratio_32x9"), "32x9"),
            (tr("ratio_9x16"), "9x16"),
        ])

        _populate(self.res_combo, [
            (tr("res_any"), ""),
            (tr("res_1080p"), "1920x1080"),
            (tr("res_1440p"), "2560x1440"),
            (tr("res_4k"), "3840x2160"),
            (tr("res_8k"), "7680x4320"),
        ])

    def _retranslate_osu_combos(self):
        # 1. Seasons
        cur_season = self.osu_season_combo.currentData()
        self.osu_season_combo.blockSignals(True)
        self.osu_season_combo.clear()
        self.osu_season_combo.addItem(tr("season_all", count=osu_manager.total_count), "all")
        for s in osu_manager.get_seasons():
            self.osu_season_combo.addItem(s, s)
        if cur_season is not None:
            idx = self.osu_season_combo.findData(cur_season)
            if idx >= 0:
                self.osu_season_combo.setCurrentIndex(idx)
        self.osu_season_combo.blockSignals(False)

        # 2. Sorting
        cur_sort = self.osu_sort_combo.currentData()
        self.osu_sort_combo.blockSignals(True)
        self.osu_sort_combo.clear()
        self.osu_sort_combo.addItem(tr("sort_osu_votes"), "votes")
        self.osu_sort_combo.addItem(tr("sort_osu_newest"), "newest")
        self.osu_sort_combo.addItem(tr("sort_osu_random"), "random")
        if cur_sort is not None:
            idx = self.osu_sort_combo.findData(cur_sort)
            if idx >= 0:
                self.osu_sort_combo.setCurrentIndex(idx)
        self.osu_sort_combo.blockSignals(False)

        # 3. Theme Chips
        theme_keys = {
            "all": "theme_all",
            "Spring": "theme_spring",
            "Summer": "theme_summer",
            "Autumn": "theme_autumn",
            "Winter": "theme_winter",
            "Halloween": "theme_halloween",
        }
        for key, tr_key in theme_keys.items():
            if key in self.theme_chips:
                self.theme_chips[key].setText(tr(tr_key))

    def retranslate_ui(self):
        self.setWindowTitle(tr("app_title"))
        self.tab_wallhaven.setText(tr("tab_wallhaven"))
        self.tab_moewalls.setText(tr("tab_moewalls"))
        self.tab_osu.setText(tr("tab_osu"))

        if self.current_mode == "osu":
            self.search_input.setPlaceholderText(tr("osu_search_placeholder"))
        elif self.current_mode == "moewalls":
            self.search_input.setPlaceholderText(tr("moe_search_placeholder"))
        else:
            self.search_input.setPlaceholderText(tr("search_placeholder"))

        self.search_btn.setText(tr("search_button"))
        self.color_toggle_btn.setText(tr("colors_button"))
        self.auto_wall_btn.setText(tr("auto_wallpaper"))
        self.auto_wall_btn.setToolTip(tr("auto_wallpaper_tip"))
        self.settings_btn.setText(tr("settings_button"))

        # Wallhaven filter labels
        self.cat_lbl.setText(tr("categories_label"))
        self.cat_general.setText(tr("cat_general"))
        self.cat_anime.setText(tr("cat_anime"))
        self.cat_people.setText(tr("cat_people"))
        self.pur_lbl.setText(tr("purity_label"))
        self.sort_lbl.setText(tr("sorting_label"))
        self._retranslate_combos()

        # MoeWalls filter labels
        self.moe_cat_lbl.setText(tr("moe_category_label"))

        # osu! filter labels
        self.osu_season_lbl.setText(tr("season_label"))
        self.osu_theme_lbl.setText(tr("theme_label"))
        self.osu_sort_lbl.setText(tr("sorting_label"))
        self._retranslate_osu_combos()

        # Pagination
        self.first_btn.setText(tr("first_page"))
        self.prev_btn.setText(tr("prev_page"))
        self.page_info_lbl.setText(tr("page_info", current=self.current_page, last=self.last_page))
        self.next_btn.setText(tr("next_page"))
        self.last_btn.setText(tr("last_page"))
        self.goto_lbl.setText(tr("goto_page"))
        self.goto_btn.setText(tr("goto_btn"))

        if self.current_mode == "osu":
            self.total_count_lbl.setText(tr("osu_total_found", total=f"{self.total_count:,}"))
        elif self.current_mode == "moewalls":
            self.total_count_lbl.setText(tr("moe_total_found", total=f"{self.total_count:,}"))
        else:
            self.total_count_lbl.setText(tr("total_found", total=f"{self.total_count:,}"))

    def _set_mode(self, mode: str):
        if mode == self.current_mode:
            self.tab_wallhaven.setChecked(mode == "wallhaven")
            self.tab_moewalls.setChecked(mode == "moewalls")
            self.tab_osu.setChecked(mode == "osu")
            return

        self.current_mode = mode
        self.tab_wallhaven.setChecked(mode == "wallhaven")
        self.tab_moewalls.setChecked(mode == "moewalls")
        self.tab_osu.setChecked(mode == "osu")

        is_wall = (mode == "wallhaven")
        is_moe = (mode == "moewalls")
        is_osu = (mode == "osu")

        self.wallhaven_filter_bar.setVisible(is_wall)
        self.moe_filter_bar.setVisible(is_moe)
        self.osu_filter_bar.setVisible(is_osu)
        self.color_toggle_btn.setVisible(is_wall)
        if not is_wall:
            self.color_bar.setVisible(False)
        else:
            self.color_bar.setVisible(self.color_toggle_btn.isChecked())

        self.search_input.clear()
        if is_wall:
            self.search_input.setPlaceholderText(tr("search_placeholder"))
        elif is_moe:
            self.search_input.setPlaceholderText(tr("moe_search_placeholder"))
        else:
            self.search_input.setPlaceholderText(tr("osu_search_placeholder"))

        self.perform_search(page=1)

    def _on_osu_theme_clicked(self, selected_key: str):
        self.osu_theme = selected_key
        for key, btn in self.theme_chips.items():
            btn.blockSignals(True)
            btn.setChecked(key == selected_key)
            btn.blockSignals(False)
        self.perform_search(page=1)

    def _on_osu_filter_changed(self):
        self.perform_search(page=1)

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
                tr("nsfw_req_title"),
                tr("nsfw_req_msg"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
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
        status = tr("status_auto_wall_on") if config.auto_set_wallpaper else tr("status_auto_wall_off")
        self.status_bar.showMessage(tr("status_auto_wall_msg", status=status), 4000)

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

        self.current_search_id += 1
        search_id = self.current_search_id

        self.status_bar.showMessage(tr("status_searching", page=page))
        self.search_btn.setEnabled(False)

        query = self.search_input.text().strip()

        if self.current_mode == "moewalls":
            cat = self.moe_cat_combo.currentData() or "all"
            self.active_search_worker = MoeSearchWorker(
                search_id=search_id,
                query=query,
                category=cat,
                page=page,
            )
        elif self.current_mode == "osu":
            season = self.osu_season_combo.currentData() or "all"
            theme = self.osu_theme
            sorting = self.osu_sort_combo.currentData() or "votes"
            self.active_search_worker = OsuSearchWorker(
                search_id=search_id,
                query=query,
                season=season,
                theme=theme,
                sorting=sorting,
                page=page,
                per_page=24,
            )
        else:
            cats = self._get_categories_str()
            purity = self._get_purity_str()
            sorting = self.sort_combo.currentData()
            top_range = self.range_combo.currentData() if sorting == "toplist" else ""
            ratios = self.ratio_combo.currentData()
            atleast = self.res_combo.currentData()
            colors = self.current_color

            self.active_search_worker = SearchWorker(
                search_id=search_id,
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

    def _on_search_success(self, search_id: int, result: SearchResult):
        if search_id != self.current_search_id:
            return

        self.search_btn.setEnabled(True)
        self.current_page = result.current_page
        self.last_page = max(1, result.last_page)
        self.total_count = result.total

        self.grid_widget.set_items(result.items)
        # Scroll back to top
        self.scroll_area.verticalScrollBar().setValue(0)

        # Update pagination
        self.page_info_lbl.setText(tr("page_info", current=self.current_page, last=self.last_page))
        self.page_spin.setRange(1, self.last_page)
        self.page_spin.setValue(self.current_page)

        if self.current_mode == "osu":
            self.total_count_lbl.setText(tr("osu_total_found", total=f"{result.total:,}"))
        elif self.current_mode == "moewalls":
            self.total_count_lbl.setText(tr("moe_total_found", total=f"{result.total:,}"))
        else:
            self.total_count_lbl.setText(tr("total_found", total=f"{result.total:,}"))

        self.prev_btn.setEnabled(self.current_page > 1)
        self.first_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.last_page)
        self.last_btn.setEnabled(self.current_page < self.last_page)

        self.status_bar.showMessage(tr("status_loaded", count=len(result.items), total=f"{result.total:,}"))

    def _on_search_failed(self, search_id: int, error: str):
        if search_id != self.current_search_id:
            return

        self.search_btn.setEnabled(True)
        self.status_bar.showMessage(tr("status_search_error", error=error))
        QMessageBox.warning(self, tr("search_failed_title"), tr("search_failed_msg", error=error))

    def _on_card_clicked(self, item: WallpaperItem):
        dlg = DetailDialog(item, self)
        dlg.tag_clicked.connect(self._search_by_tag)
        dlg.download_completed.connect(self._on_download_completed)
        dlg.exec()

    def _search_by_tag(self, tag_name: str):
        clean_tag = tag_name.lstrip("#")
        self.search_input.setText(clean_tag)
        self.perform_search(page=1)

    def _on_quick_download(self, item: WallpaperItem):
        # User requested quick download from card button
        # Respect user requirement: "Při každém stažení se zeptat dialogem na umístění"
        is_animated = getattr(item, "is_animated", False)
        ext = ".mp4" if is_animated else (os.path.splitext(item.path)[1] or ".jpg")

        if getattr(item, "_osu_meta", None):
            meta = item._osu_meta
            artist = "".join(c for c in meta.get("artist", "artist") if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
            title = "".join(c for c in meta.get("title", item.id) if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
            season = "".join(c for c in meta.get("season", "osu") if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
            suggested_name = f"osu-{season}-{artist}-{title}{ext}"
        elif is_animated:
            clean_title = "".join(c for c in getattr(item, "_display_title", item.id) if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
            suggested_name = f"moewalls-{clean_title}{ext}"
        else:
            suggested_name = f"wallhaven-{item.id}{ext}"

        default_dir = Path(config.default_download_dir)
        default_dir.mkdir(parents=True, exist_ok=True)
        initial_path = str(default_dir / suggested_name)

        filter_str = "Video (*.mp4 *.webm);;All Files (*)" if is_animated else tr("images_filter", ext=ext)
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("save_dialog_title"),
            initial_path,
            filter_str,
        )

        if not save_path:
            return

        self.status_bar.showMessage(tr("status_downloading", id=item.id, filename=os.path.basename(save_path)))

        self.quick_download_worker = DownloadWorker(item, save_path)
        self.quick_download_worker.progress.connect(
            lambda cur, tot: self.status_bar.showMessage(
                tr("status_download_progress", id=item.id, cur=cur // (1024 * 1024), tot=tot // (1024 * 1024))
            )
        )
        self.quick_download_worker.finished.connect(
            lambda path: self._on_download_completed(path)
        )
        self.quick_download_worker.failed.connect(
            lambda err: QMessageBox.critical(self, tr("download_failed_title"), tr("download_failed_msg", error=err))
        )
        self.quick_download_worker.start()

    def _on_download_completed(self, path: str):
        filename = os.path.basename(path)
        if config.auto_set_wallpaper:
            ok, msg = set_desktop_wallpaper(
                path,
                config.custom_wallpaper_cmd,
                config.wallpaper_setter,
                config.custom_video_wallpaper_cmd,
            )
            if ok:
                self.status_bar.showMessage(tr("status_download_done_wall", filename=filename), 8000)
            else:
                self.status_bar.showMessage(tr("status_download_fail_wall", filename=filename, error=msg), 8000)
        else:
            self.status_bar.showMessage(tr("status_download_done", filename=filename), 8000)
