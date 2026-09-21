"""Ultra-Modern Dark Obsidian Stylesheet for Wallhaven Desktop."""
from pathlib import Path

_ASSETS_DIR = Path(__file__).parent.parent / "assets"
_CHEVRON_NORMAL = str(_ASSETS_DIR / "chevron_down.png").replace("\\", "/")
_CHEVRON_HOVER = str(_ASSETS_DIR / "chevron_down_hover.png").replace("\\", "/")

_RAW_STYLESHEET = """
QWidget {
    background-color: #0d1017;
    color: #e2e8f0;
    font-family: 'Inter', 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Header & Filter Panels */
QFrame#headerPanel {
    background-color: #12151f;
    border-bottom: 1px solid #1c2230;
    padding: 8px 16px;
}

QFrame#filterPanel {
    background-color: #0f121a;
    border-bottom: 1px solid #191d29;
    padding: 6px 14px;
}

QFrame#colorBarFrame {
    background-color: #0b0d14;
    border-bottom: 1px solid #181c26;
    padding: 6px 16px;
}

/* Navigation Capsule Container */
QFrame#tabsContainer, QWidget#tabsContainer {
    background-color: #0b0d14;
    border: 1px solid #1c2230;
    border-radius: 9px;
    padding: 2px;
}

QPushButton#navTab {
    background: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 7px;
    padding: 4px 9px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#navTab:hover {
    background-color: #171b26;
    color: #f1f5f9;
}

QPushButton#navTab:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #6366f1);
    color: #ffffff;
    font-weight: bold;
}

/* Search Box & Inputs */
QLineEdit {
    background-color: #151824;
    color: #f8fafc;
    border: 1.5px solid #232838;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12.5px;
    selection-background-color: #6366f1;
}

QLineEdit:hover {
    border-color: #333b52;
    background-color: #181c2b;
}

QLineEdit:focus {
    border: 1.5px solid #6366f1;
    background-color: #1b2030;
    color: #ffffff;
}

/* Combo Boxes */
QComboBox {
    background-color: #151824;
    color: #e2e8f0;
    border: 1.5px solid #232838;
    border-radius: 8px;
    padding: 3px 6px;
    padding-right: 18px;
    font-size: 11.5px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: #6366f1;
    background-color: #191e2e;
    color: #ffffff;
}

QComboBox:focus {
    border-color: #818cf8;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border: none;
}

QComboBox::down-arrow {
    image: url("__CHEVRON_NORMAL__");
    width: 10px;
    height: 10px;
}

QComboBox::down-arrow:hover {
    image: url("__CHEVRON_HOVER__");
}

QComboBox QAbstractItemView {
    background-color: #141722;
    color: #e2e8f0;
    border: 1px solid #282f42;
    border-radius: 8px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    outline: none;
    padding: 4px;
}

/* Header Tool Buttons (Auto-Wallpaper, Settings) */
QPushButton#headerToolBtn {
    background-color: #151824;
    color: #cbd5e1;
    border: 1.5px solid #232838;
    border-radius: 8px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#headerToolBtn:hover {
    background-color: #1e2434;
    border-color: #3b4461;
    color: #ffffff;
}

QPushButton#headerToolBtn:checked {
    background-color: #1e1b4b;
    border: 1.5px solid #6366f1;
    color: #c7d2fe;
}

QPushButton#toolButton {
    background-color: #151824;
    color: #cbd5e1;
    border: 1.5px solid #232838;
    border-radius: 7px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 600;
}

QPushButton#toolButton:hover {
    background-color: #1e2434;
    border-color: #3b4461;
    color: #ffffff;
}

QPushButton#toolButton:checked {
    background-color: #1e1b4b;
    border: 1.5px solid #6366f1;
    color: #c7d2fe;
}

/* Primary Vibrant Button (Search, Download) */
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #6366f1);
    border: 1px solid #818cf8;
    color: #ffffff;
    font-weight: bold;
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 12px;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #4f46e5);
    border-color: #a5b4fc;
}

QPushButton#primaryButton:pressed {
    background-color: #3730a3;
}

/* Standard Push Buttons */
QPushButton {
    background-color: #151824;
    color: #e2e8f0;
    border: 1.5px solid #232838;
    border-radius: 8px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1e2434;
    border-color: #6366f1;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #11141e;
    border-color: #4f46e5;
}

/* Filter Chips */
QPushButton#filterChip {
    background-color: #141722;
    color: #94a3b8;
    border: 1.5px solid #202536;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#filterChip:hover {
    border-color: #6366f1;
    background-color: #1c2130;
    color: #ffffff;
}

QPushButton#filterChip:checked {
    background-color: #262463;
    border: 1.5px solid #6366f1;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#nsfwChip {
    background-color: #141722;
    color: #94a3b8;
    border: 1.5px solid #202536;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#nsfwChip:hover {
    border-color: #f43f5e;
    background-color: #1c2130;
    color: #ffffff;
}

QPushButton#nsfwChip:checked {
    background-color: #881337;
    border: 1.5px solid #f43f5e;
    color: #ffe4e6;
    font-weight: bold;
}

QPushButton#sketchyChip {
    background-color: #141722;
    color: #94a3b8;
    border: 1.5px solid #202536;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#sketchyChip:hover {
    border-color: #f59e0b;
    background-color: #1c2130;
    color: #ffffff;
}

QPushButton#sketchyChip:checked {
    background-color: #78350f;
    border: 1.5px solid #f59e0b;
    color: #fef3c7;
    font-weight: bold;
}

QPushButton#themeChip {
    background-color: #141722;
    border: 1.5px solid #202536;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    color: #94a3b8;
}

QPushButton#themeChip:hover {
    border-color: #ec4899;
    background-color: #1c2130;
    color: #ffffff;
}

QPushButton#themeChip:checked {
    background-color: #831843;
    border: 1.5px solid #ec4899;
    color: #fce7f3;
    font-weight: bold;
}

/* Scroll Area & Sleek Modern Scrollbar */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
    margin: 4px 2px 4px 0;
}

QScrollBar::handle:vertical {
    background: #232838;
    min-height: 28px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #47506c;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Wallpaper Card */
QFrame#wallpaperCard {
    background-color: #12151f;
    border: 1.5px solid #1e2434;
    border-radius: 12px;
}

QFrame#wallpaperCard:hover {
    border: 1.5px solid #6366f1;
    background-color: #161a27;
}

/* Card Badges (Glassmorphic) */
QLabel#badge {
    background-color: rgba(13, 16, 23, 0.88);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 10.5px;
    font-weight: bold;
}

QLabel#categoryBadge {
    background-color: rgba(49, 46, 129, 0.85);
    color: #c7d2fe;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 10.5px;
    font-weight: bold;
}

/* Pagination Frame & Badges */
QFrame#paginationFrame {
    background-color: #0f121a;
    border-top: 1px solid #1a1e2b;
    padding: 6px 16px;
}

QLabel#pageBadge {
    background-color: #141722;
    border: 1px solid #252c3e;
    border-radius: 7px;
    padding: 4px 10px;
    min-width: 100px;
    qproperty-alignment: AlignCenter;
    font-weight: bold;
    color: #f1f5f9;
    font-size: 12px;
}

/* SpinBox */
QSpinBox {
    background-color: #151824;
    color: #f8fafc;
    border: 1.5px solid #232838;
    border-radius: 8px;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 600;
}

QSpinBox:focus {
    border-color: #6366f1;
}

/* Status Bar */
QStatusBar {
    background-color: #0b0d14;
    color: #8590a6;
    border-top: 1px solid #161922;
    font-size: 12px;
    padding: 3px 12px;
}

/* Tooltips */
QToolTip {
    background-color: #141722;
    color: #f8fafc;
    border: 1.5px solid #333c54;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}
"""

DARK_STYLESHEET = _RAW_STYLESHEET.replace(
    "__CHEVRON_NORMAL__", _CHEVRON_NORMAL
).replace(
    "__CHEVRON_HOVER__", _CHEVRON_HOVER
)
