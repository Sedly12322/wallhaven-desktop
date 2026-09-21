"""Ultra-Modern Dark Obsidian Stylesheet for Wallhaven Desktop."""

DARK_STYLESHEET = """
QWidget {
    background-color: #0d1017;
    color: #e2e8f0;
    font-family: 'Inter', 'Segoe UI', 'Noto Sans', -apple-system, sans-serif;
    font-size: 13px;
}

/* Header & Filter Panels */
QFrame#headerPanel {
    background-color: #141722;
    border-bottom: 1px solid #202536;
    padding: 10px 18px;
}

QFrame#filterPanel {
    background-color: #11141d;
    border-bottom: 1px solid #1c2130;
    padding: 8px 18px;
}

QFrame#colorBarFrame {
    background-color: #0f121a;
    border-bottom: 1px solid #1a1e2b;
    padding: 6px 18px;
}

/* Search Box & Inputs */
QLineEdit {
    background-color: #1a1e2b;
    color: #f8fafc;
    border: 1.5px solid #282e42;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    selection-background-color: #6366f1;
}

QLineEdit:hover {
    border-color: #3b4461;
    background-color: #1e2232;
}

QLineEdit:focus {
    border: 1.5px solid #6366f1;
    background-color: #202537;
    color: #ffffff;
}

/* Combo Boxes */
QComboBox {
    background-color: #1a1e2b;
    color: #e2e8f0;
    border: 1.5px solid #282e42;
    border-radius: 9px;
    padding: 6px 12px;
    min-width: 95px;
    font-size: 12px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: #6366f1;
    background-color: #1f2434;
    color: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 22px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #94a3b8;
    margin-right: 8px;
}

QComboBox::down-arrow:hover {
    border-top-color: #6366f1;
}

QComboBox QAbstractItemView {
    background-color: #161924;
    color: #e2e8f0;
    border: 1px solid #2e354a;
    border-radius: 8px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    outline: none;
    padding: 6px;
}

/* Standard Push Buttons */
QPushButton {
    background-color: #1a1e2b;
    color: #e2e8f0;
    border: 1.5px solid #282e42;
    border-radius: 9px;
    padding: 7px 15px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #242a3c;
    border-color: #6366f1;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #161924;
    border-color: #4f46e5;
}

/* Primary Vibrant Button */
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #6366f1);
    border: 1px solid #818cf8;
    color: #ffffff;
    font-weight: bold;
    border-radius: 9px;
    padding: 7px 18px;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #4f46e5);
    border-color: #a5b4fc;
}

QPushButton#primaryButton:pressed {
    background-color: #3730a3;
}

/* Modern Segmented Navigation Tabs */
QPushButton#navTab {
    background-color: #161924;
    color: #94a3b8;
    border: 1.5px solid #23283a;
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#navTab:hover {
    background-color: #1f2434;
    border-color: #4338ca;
    color: #f1f5f9;
}

QPushButton#navTab:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #6366f1);
    border: 1px solid #818cf8;
    color: #ffffff;
    font-weight: bold;
}

/* Filter Chips with Glow */
QPushButton#filterChip {
    background-color: #161924;
    color: #cbd5e1;
    border: 1.5px solid #252a3b;
    border-radius: 15px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#filterChip:hover {
    border-color: #6366f1;
    background-color: #1f2434;
    color: #ffffff;
}

QPushButton#filterChip:checked {
    background-color: #312e81;
    border: 1.5px solid #6366f1;
    color: #e0e7ff;
    font-weight: bold;
}

QPushButton#nsfwChip:checked {
    background-color: #881337;
    border: 1.5px solid #f43f5e;
    color: #ffe4e6;
    font-weight: bold;
}

QPushButton#sketchyChip:checked {
    background-color: #78350f;
    border: 1.5px solid #f59e0b;
    color: #fef3c7;
    font-weight: bold;
}

QPushButton#themeChip {
    background-color: #161924;
    border: 1.5px solid #252a3b;
    border-radius: 15px;
    padding: 5px 14px;
    font-size: 12px;
    color: #cbd5e1;
}

QPushButton#themeChip:hover {
    border-color: #ec4899;
    background-color: #1f2434;
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
    width: 9px;
    margin: 4px 2px 4px 0;
}

QScrollBar::handle:vertical {
    background: #252a3a;
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
    background-color: #141722;
    border: 1.5px solid #202536;
    border-radius: 12px;
}

QFrame#wallpaperCard:hover {
    border: 1.5px solid #6366f1;
    background-color: #191d2b;
}

/* Card Badges (Glassmorphic) */
QLabel#badge {
    background-color: rgba(13, 16, 23, 0.88);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: bold;
}

QLabel#categoryBadge {
    background-color: rgba(49, 46, 129, 0.85);
    color: #c7d2fe;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: bold;
}

/* Progress Bar */
QProgressBar {
    background-color: #1a1e2b;
    border: 1px solid #282e42;
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    height: 18px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #38bdf8);
    border-radius: 7px;
}

/* Tooltips */
QToolTip {
    background-color: #161924;
    color: #f8fafc;
    border: 1.5px solid #3b4461;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}

/* Status Bar */
QStatusBar {
    background-color: #11141d;
    color: #94a3b8;
    border-top: 1px solid #1c2130;
    font-size: 12px;
    padding: 4px 12px;
}

/* SpinBox */
QSpinBox {
    background-color: #1a1e2b;
    color: #f8fafc;
    border: 1.5px solid #282e42;
    border-radius: 8px;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: 600;
}

QSpinBox:focus {
    border-color: #6366f1;
}
"""
