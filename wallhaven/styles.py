"""Dark modern stylesheet for Wallhaven Desktop."""

DARK_STYLESHEET = """
QWidget {
    background-color: #16181d;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'Inter', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Header & Panels */
QFrame#headerPanel {
    background-color: #1e2128;
    border-bottom: 1px solid #2d3139;
    padding: 8px 16px;
}

QFrame#filterPanel {
    background-color: #1a1d24;
    border-bottom: 1px solid #282c35;
    padding: 8px 16px;
}

QFrame#colorBarFrame {
    background-color: #15171c;
    border-bottom: 1px solid #242730;
    padding: 4px 16px;
}

/* Inputs */
QLineEdit {
    background-color: #262933;
    color: #f1f5f9;
    border: 1px solid #3b3f4d;
    border-radius: 8px;
    padding: 7px 12px;
    selection-background-color: #4f46e5;
}

QLineEdit:focus {
    border: 1px solid #6366f1;
    background-color: #2b2e3a;
}

/* Combo boxes */
QComboBox {
    background-color: #262933;
    color: #e2e8f0;
    border: 1px solid #3b3f4d;
    border-radius: 8px;
    padding: 6px 12px;
    min-width: 90px;
}

QComboBox:hover {
    border-color: #4f46e5;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #22252e;
    color: #e2e8f0;
    border: 1px solid #3b3f4d;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    outline: none;
    padding: 4px;
}

/* Push Buttons */
QPushButton {
    background-color: #262933;
    color: #e2e8f0;
    border: 1px solid #3b3f4d;
    border-radius: 8px;
    padding: 7px 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #323644;
    border-color: #6366f1;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #20232c;
}

QPushButton#primaryButton {
    background-color: #4f46e5;
    border: 1px solid #6366f1;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #4338ca;
    border-color: #818cf8;
}

QPushButton#primaryButton:pressed {
    background-color: #3730a3;
}

/* Filter Toggle Buttons (Checked State) */
QPushButton#filterChip {
    background-color: #232630;
    border: 1px solid #363a47;
    border-radius: 14px;
    padding: 5px 12px;
    font-size: 12px;
}

QPushButton#filterChip:hover {
    border-color: #6366f1;
    background-color: #2a2e3a;
}

QPushButton#filterChip:checked {
    background-color: #312e81;
    border: 1px solid #6366f1;
    color: #e0e7ff;
    font-weight: bold;
}

QPushButton#nsfwChip:checked {
    background-color: #7f1d1d;
    border: 1px solid #ef4444;
    color: #fecaca;
    font-weight: bold;
}

QPushButton#sketchyChip:checked {
    background-color: #78350f;
    border: 1px solid #f59e0b;
    color: #fef3c7;
    font-weight: bold;
}

/* ScrollArea */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: #16181d;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2e3340;
    min-height: 24px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #4a5166;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Wallpaper Card */
QFrame#wallpaperCard {
    background-color: #1f222a;
    border: 1px solid #2d313b;
    border-radius: 10px;
}

QFrame#wallpaperCard:hover {
    border: 1px solid #6366f1;
    background-color: #242732;
}

/* Badges */
QLabel#badge {
    background-color: rgba(15, 17, 23, 0.85);
    color: #e2e8f0;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
    font-weight: bold;
}

QLabel#categoryBadge {
    background-color: rgba(30, 58, 138, 0.85);
    color: #93c5fd;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
    font-weight: bold;
}

/* Progress bar */
QProgressBar {
    background-color: #262933;
    border: 1px solid #3b3f4d;
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    height: 16px;
}

QProgressBar::chunk {
    background-color: #4f46e5;
    border-radius: 5px;
}

/* Tooltips */
QToolTip {
    background-color: #1e2128;
    color: #f1f5f9;
    border: 1px solid #4a5166;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
}

/* Status bar */
QStatusBar {
    background-color: #1a1d24;
    color: #94a3b8;
    border-top: 1px solid #282c35;
    font-size: 12px;
}
"""
