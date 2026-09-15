from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from wallhaven.api import WallpaperItem
from wallhaven.image_loader import loader
from wallhaven.i18n import tr


class WallpaperCard(QFrame):
    clicked = pyqtSignal(WallpaperItem)
    download_requested = pyqtSignal(WallpaperItem)

    CARD_WIDTH = 290
    CARD_HEIGHT = 220

    def __init__(self, item: WallpaperItem, parent=None):
        super().__init__(parent)
        self.item = item
        self.setObjectName("wallpaperCard")
        self.setFixedSize(self.CARD_WIDTH, self.CARD_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._pixmap: QPixmap | None = None
        self._is_hovered = False

        self._init_ui()
        self._load_thumbnail()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Image preview container
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #12141a; border-radius: 6px;")
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setText(tr("card_loading"))
        layout.addWidget(self.image_label, stretch=1)

        # Bottom info row
        info_row = QHBoxLayout()
        info_row.setContentsMargins(2, 0, 2, 2)
        info_row.setSpacing(6)

        # Resolution badge
        res_text = self.item.resolution
        if self.item.dimension_x >= 3840:
            res_text = f"4K ({self.item.resolution})"
        elif self.item.dimension_x >= 2560:
            res_text = f"2K ({self.item.resolution})"

        self.res_badge = QLabel(res_text)
        self.res_badge.setObjectName("badge")
        info_row.addWidget(self.res_badge)

        # Category badge
        cat_badge = QLabel(self.item.category.capitalize())
        cat_badge.setObjectName("categoryBadge")
        info_row.addWidget(cat_badge)

        # Purity indicator (if sketchy or nsfw)
        if self.item.purity == "sketchy":
            purity_lbl = QLabel("S")
            purity_lbl.setToolTip("Sketchy")
            purity_lbl.setStyleSheet("background: #d97706; color: white; border-radius: 3px; font-weight: bold; font-size: 10px; padding: 1px 4px;")
            info_row.addWidget(purity_lbl)
        elif self.item.purity == "nsfw":
            purity_lbl = QLabel("NSFW")
            purity_lbl.setStyleSheet("background: #dc2626; color: white; border-radius: 3px; font-weight: bold; font-size: 10px; padding: 1px 4px;")
            info_row.addWidget(purity_lbl)

        info_row.addStretch()

        # Favorites counter
        fav_lbl = QLabel(f"★ {self.item.favorites}")
        fav_lbl.setStyleSheet("color: #fbbf24; font-size: 11px;")
        info_row.addWidget(fav_lbl)

        # Quick download button
        self.dl_btn = QPushButton("⬇")
        self.dl_btn.setFixedSize(26, 24)
        self.dl_btn.setToolTip(tr("card_download_tooltip"))
        self.dl_btn.setStyleSheet("""
            QPushButton {
                background: #4f46e5;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                background: #6366f1;
            }
        """)
        self.dl_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dl_btn.clicked.connect(self._on_download_clicked)
        info_row.addWidget(self.dl_btn)

        layout.addLayout(info_row)

    def _load_thumbnail(self):
        thumb_url = self.item.thumb_large or self.item.thumb_small
        if not thumb_url:
            self.image_label.setText(tr("card_no_preview"))
            return

        self._connected = True
        loader.image_loaded.connect(self._on_image_loaded)
        if loader.load_image(thumb_url, is_thumb=True):
            # Already in cache
            pm = loader.cache.get_pixmap(thumb_url, is_thumb=True)
            if pm:
                self._update_pixmap(pm)

    def _cleanup_signal(self):
        if getattr(self, "_connected", False):
            try:
                loader.image_loaded.disconnect(self._on_image_loaded)
            except Exception:
                pass
            self._connected = False

    def _on_image_loaded(self, url: str, pixmap: QPixmap):
        thumb_url = self.item.thumb_large or self.item.thumb_small
        if url == thumb_url:
            self._cleanup_signal()
            self._update_pixmap(pixmap)

    def closeEvent(self, event):
        self._cleanup_signal()
        super().closeEvent(event)

    def _update_pixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        # Scale to fit image label maintaining aspect ratio
        target_size = QSize(self.CARD_WIDTH - 14, self.CARD_HEIGHT - 48)
        scaled = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Crop to center
        x = max(0, (scaled.width() - target_size.width()) // 2)
        y = max(0, (scaled.height() - target_size.height()) // 2)
        cropped = scaled.copy(x, y, target_size.width(), target_size.height())

        # Rounded corners for image
        rounded = QPixmap(cropped.size())
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, cropped.width(), cropped.height(), 6, 6)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, cropped)
        painter.end()

        self.image_label.setPixmap(rounded)
        self.image_label.setText("")

    def _on_download_clicked(self):
        self.download_requested.emit(self.item)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicked inside download button
            if not self.dl_btn.geometry().contains(event.pos()):
                self.clicked.emit(self.item)
        super().mousePressEvent(event)
