from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel
from wallhaven.api import WallpaperItem
from wallhaven.widgets.wallpaper_card import WallpaperCard


class WallpaperGridWidget(QWidget):
    card_clicked = pyqtSignal(WallpaperItem)
    download_requested = pyqtSignal(WallpaperItem)
    uninstall_requested = pyqtSignal(WallpaperItem)
    set_wall_requested = pyqtSignal(WallpaperItem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: list[WallpaperCard] = []
        self.items: list[WallpaperItem] = []

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(16, 16, 16, 16)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.current_cols = 4

    def set_items(self, items: list[WallpaperItem]):
        self.clear()
        self.items = items

        for item in items:
            card = WallpaperCard(item)
            card.clicked.connect(self.card_clicked)
            card.download_requested.connect(self.download_requested)
            card.uninstall_requested.connect(self.uninstall_requested)
            card.set_wall_requested.connect(self.set_wall_requested)
            self.cards.append(card)

        self._relayout()

    def clear(self):
        for card in self.cards:
            self.grid_layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()
        self.items.clear()

    def _calc_columns(self) -> int:
        card_w = WallpaperCard.CARD_WIDTH + 16
        available_w = self.width() - 32
        cols = max(1, available_w // card_w)
        return min(cols, 6)

    def _relayout(self):
        cols = self._calc_columns()
        self.current_cols = cols

        for idx, card in enumerate(self.cards):
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(card, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_cols = self._calc_columns()
        if new_cols != self.current_cols:
            self._relayout()
