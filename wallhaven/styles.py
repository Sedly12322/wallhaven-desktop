"""Ultra-Modern Multi-Theme Engine for Wallhaven Desktop.

Supports curated Linux & cross-platform themes:
- Wallhaven Dark (Default Obsidian & Indigo)
- Catppuccin Mocha (Community favorite Lavender & Deep Base)
- Tokyo Night (Cyberpunk Blue & Deep Violet)
- Nord Frost (Arctic Frost & Polar Night)
- Dracula (Gothic Vampire Purple & Slate)
- Gruvbox Dark (Warm Retro Gold & Charcoal)
- Cyberpunk 2077 (Electric Neon Cyan & Hot Pink)
- OLED Pure Black (Pure #000000 & Electric Sapphire)
- Linux System / Pywal Palette (Dynamic desktop adaptation)
"""
import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

_ASSETS_DIR = Path(__file__).parent.parent / "assets"
_CHEVRON_NORMAL = str(_ASSETS_DIR / "chevron_down.png").replace("\\", "/")
_CHEVRON_HOVER = str(_ASSETS_DIR / "chevron_down_hover.png").replace("\\", "/")

# Curated theme palettes
THEME_PALETTES: Dict[str, Dict[str, str]] = {
    "dark": {
        "name": "🌌 Wallhaven Dark",
        "bg_base": "#0d1017",
        "bg_surface": "#12151f",
        "bg_subsurface": "#0f121a",
        "bg_capsule": "#0b0d14",
        "bg_input": "#151824",
        "bg_input_hover": "#1e2434",
        "bg_card_hover": "#161a27",
        "border": "#232838",
        "border_subtle": "#1c2230",
        "border_hover": "#3b4461",
        "accent": "#6366f1",
        "accent_hover": "#818cf8",
        "accent_gradient_start": "#4f46e5",
        "accent_gradient_end": "#6366f1",
        "accent_surface": "#262463",
        "accent_text": "#ffffff",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
    },
    "catppuccin": {
        "name": "🌸 Catppuccin Mocha",
        "bg_base": "#1e1e2e",
        "bg_surface": "#181825",
        "bg_subsurface": "#11111b",
        "bg_capsule": "#11111b",
        "bg_input": "#313244",
        "bg_input_hover": "#45475a",
        "bg_card_hover": "#252739",
        "border": "#45475a",
        "border_subtle": "#313244",
        "border_hover": "#585b70",
        "accent": "#cba6f7",
        "accent_hover": "#b4befe",
        "accent_gradient_start": "#995bf5",
        "accent_gradient_end": "#cba6f7",
        "accent_surface": "#3f3657",
        "accent_text": "#ffffff",
        "text_primary": "#cdd6f4",
        "text_secondary": "#a6adc8",
        "text_muted": "#6c7086",
    },
    "tokyo_night": {
        "name": "🌃 Tokyo Night",
        "bg_base": "#1a1b26",
        "bg_surface": "#16161e",
        "bg_subsurface": "#13141c",
        "bg_capsule": "#101016",
        "bg_input": "#24283b",
        "bg_input_hover": "#2f354f",
        "bg_card_hover": "#1f2335",
        "border": "#292e42",
        "border_subtle": "#1f2335",
        "border_hover": "#414868",
        "accent": "#7aa2f7",
        "accent_hover": "#89b4fa",
        "accent_gradient_start": "#5981f4",
        "accent_gradient_end": "#7aa2f7",
        "accent_surface": "#233154",
        "accent_text": "#ffffff",
        "text_primary": "#c0caf5",
        "text_secondary": "#9aa5ce",
        "text_muted": "#565f89",
    },
    "nord": {
        "name": "❄️ Nord Frost",
        "bg_base": "#242933",
        "bg_surface": "#2e3440",
        "bg_subsurface": "#272c36",
        "bg_capsule": "#1e222a",
        "bg_input": "#3b4252",
        "bg_input_hover": "#434c5e",
        "bg_card_hover": "#353c4a",
        "border": "#434c5e",
        "border_subtle": "#2e3440",
        "border_hover": "#4c566a",
        "accent": "#88c0d0",
        "accent_hover": "#8fbcbb",
        "accent_gradient_start": "#5e81ac",
        "accent_gradient_end": "#88c0d0",
        "accent_surface": "#2d4350",
        "accent_text": "#eceff4",
        "text_primary": "#eceff4",
        "text_secondary": "#d8dee9",
        "text_muted": "#7b88a1",
    },
    "dracula": {
        "name": "🧛 Dracula",
        "bg_base": "#21222c",
        "bg_surface": "#282a36",
        "bg_subsurface": "#1e1f29",
        "bg_capsule": "#181920",
        "bg_input": "#343746",
        "bg_input_hover": "#44475a",
        "bg_card_hover": "#2d303e",
        "border": "#44475a",
        "border_subtle": "#2e303e",
        "border_hover": "#6272a4",
        "accent": "#bd93f9",
        "accent_hover": "#ff79c6",
        "accent_gradient_start": "#9a6df7",
        "accent_gradient_end": "#bd93f9",
        "accent_surface": "#422e5a",
        "accent_text": "#ffffff",
        "text_primary": "#f8f8f2",
        "text_secondary": "#bfbfbf",
        "text_muted": "#6272a4",
    },
    "gruvbox": {
        "name": "📻 Gruvbox Dark",
        "bg_base": "#1d2021",
        "bg_surface": "#282828",
        "bg_subsurface": "#242424",
        "bg_capsule": "#191b1c",
        "bg_input": "#3c3836",
        "bg_input_hover": "#504945",
        "bg_card_hover": "#32302f",
        "border": "#504945",
        "border_subtle": "#32302f",
        "border_hover": "#665c54",
        "accent": "#fabd2f",
        "accent_hover": "#fe8019",
        "accent_gradient_start": "#d65d0e",
        "accent_gradient_end": "#fabd2f",
        "accent_surface": "#4e3d1f",
        "accent_text": "#1d2021",
        "text_primary": "#ebdbb2",
        "text_secondary": "#d5c4a1",
        "text_muted": "#928374",
    },
    "cyberpunk": {
        "name": "⚡ Cyberpunk Neon",
        "bg_base": "#0a0b12",
        "bg_surface": "#111320",
        "bg_subsurface": "#0d0f19",
        "bg_capsule": "#07080d",
        "bg_input": "#181b2e",
        "bg_input_hover": "#222640",
        "bg_card_hover": "#171a2b",
        "border": "#272c4a",
        "border_subtle": "#1a1d30",
        "border_hover": "#3e4775",
        "accent": "#00f0ff",
        "accent_hover": "#f72585",
        "accent_gradient_start": "#f72585",
        "accent_gradient_end": "#00f0ff",
        "accent_surface": "#1a3547",
        "accent_text": "#ffffff",
        "text_primary": "#e0fbfc",
        "text_secondary": "#90e0ef",
        "text_muted": "#52796f",
    },
    "oled": {
        "name": "🖤 OLED Pure Black",
        "bg_base": "#000000",
        "bg_surface": "#0a0a0a",
        "bg_subsurface": "#050505",
        "bg_capsule": "#000000",
        "bg_input": "#141414",
        "bg_input_hover": "#222222",
        "bg_card_hover": "#111111",
        "border": "#282828",
        "border_subtle": "#161616",
        "border_hover": "#444444",
        "accent": "#3b82f6",
        "accent_hover": "#60a5fa",
        "accent_gradient_start": "#1d4ed8",
        "accent_gradient_end": "#3b82f6",
        "accent_surface": "#13274f",
        "accent_text": "#ffffff",
        "text_primary": "#ffffff",
        "text_secondary": "#a1a1aa",
        "text_muted": "#71717a",
    },
}


def _detect_linux_system_accent() -> Optional[str]:
    """Detect GNOME / GTK / Desktop accent color on Linux if available."""
    try:
        res = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "accent-color"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if res.returncode == 0 and res.stdout:
            val = res.stdout.strip().strip("'").strip('"').lower()
            accent_map = {
                "blue": "#3584e4",
                "teal": "#2190a4",
                "green": "#3a944c",
                "yellow": "#e5a50a",
                "orange": "#ed5b00",
                "red": "#e62d42",
                "pink": "#d56199",
                "purple": "#9141ac",
                "slate": "#6d7889",
            }
            return accent_map.get(val)
    except Exception:
        pass
    return None


def _get_pywal_palette() -> Optional[Dict[str, str]]:
    """Load palette generated by Pywal from ~/.cache/wal/colors.json if present."""
    wal_file = Path.home() / ".cache" / "wal" / "colors.json"
    if not wal_file.exists():
        return None
    try:
        with open(wal_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        c = data.get("colors", {})
        sp = data.get("special", {})
        bg = sp.get("background", "#121212")
        fg = sp.get("foreground", "#f0f0f0")
        accent = c.get("color4", "#6366f1")
        accent_alt = c.get("color5", "#818cf8")
        return {
            "name": "🎨 Pywal (System Wallpaper)",
            "bg_base": bg,
            "bg_surface": c.get("color0", "#181818"),
            "bg_subsurface": bg,
            "bg_capsule": bg,
            "bg_input": c.get("color8", "#282828"),
            "bg_input_hover": c.get("color7", "#383838"),
            "bg_card_hover": c.get("color0", "#202020"),
            "border": c.get("color8", "#333333"),
            "border_subtle": c.get("color0", "#222222"),
            "border_hover": accent,
            "accent": accent,
            "accent_hover": accent_alt,
            "accent_gradient_start": accent,
            "accent_gradient_end": accent_alt,
            "accent_surface": c.get("color1", "#2b2244"),
            "accent_text": "#ffffff",
            "text_primary": fg,
            "text_secondary": c.get("color7", "#b0b0b0"),
            "text_muted": c.get("color8", "#777777"),
        }
    except Exception:
        return None


def get_available_themes() -> List[Tuple[str, str]]:
    """Return list of (theme_id, display_name) for theme selection."""
    themes = [(k, v["name"]) for k, v in THEME_PALETTES.items()]
    
    # Check if Linux system accent is detected
    sys_accent = _detect_linux_system_accent()
    if sys_accent:
        themes.append(("system", "🐧 Linux System Accent"))
        
    # Check if Pywal colors are available
    if (Path.home() / ".cache" / "wal" / "colors.json").exists():
        themes.append(("pywal", "🎨 Pywal (Wallpaper Colors)"))

    return themes


def get_palette(theme_id: str = "dark") -> Dict[str, str]:
    """Retrieve color palette dictionary for given theme ID."""
    if theme_id == "pywal":
        wal_pal = _get_pywal_palette()
        if wal_pal:
            return wal_pal
        theme_id = "dark"

    if theme_id == "system":
        sys_accent = _detect_linux_system_accent() or "#3584e4"
        base = dict(THEME_PALETTES["dark"])
        base["name"] = "🐧 Linux System Accent"
        base["accent"] = sys_accent
        base["accent_hover"] = sys_accent
        base["accent_gradient_start"] = sys_accent
        base["accent_gradient_end"] = sys_accent
        base["accent_surface"] = "#1e2a3a"
        return base

    return THEME_PALETTES.get(theme_id, THEME_PALETTES["dark"])


_TEMPLATE_STYLESHEET = """
QWidget {
    background-color: %(bg_base)s;
    color: %(text_primary)s;
    font-family: 'Inter', 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* Header & Filter Panels */
QFrame#headerPanel {
    background-color: %(bg_surface)s;
    border-bottom: 1px solid %(border_subtle)s;
    padding: 8px 16px;
}

QFrame#filterPanel {
    background-color: %(bg_subsurface)s;
    border-bottom: 1px solid %(border_subtle)s;
    padding: 6px 14px;
}

QFrame#colorBarFrame {
    background-color: %(bg_capsule)s;
    border-bottom: 1px solid %(border_subtle)s;
    padding: 6px 16px;
}

QFrame#toolbarSeparator {
    background-color: %(border_subtle)s;
    max-width: 1px;
    margin: 3px 4px;
}

QLabel#filterLabel {
    color: %(text_secondary)s;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.5px;
}

/* Navigation Capsule Container */
QFrame#tabsContainer, QWidget#tabsContainer {
    background-color: %(bg_capsule)s;
    border: 1px solid %(border_subtle)s;
    border-radius: 9px;
    padding: 2px;
}

QPushButton#navTab {
    background: transparent;
    color: %(text_secondary)s;
    border: none;
    border-radius: 7px;
    padding: 4px 9px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#navTab:hover {
    background-color: %(bg_input_hover)s;
    color: %(text_primary)s;
}

QPushButton#navTab:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 %(accent_gradient_start)s, stop:1 %(accent_gradient_end)s);
    color: %(accent_text)s;
    font-weight: bold;
}

/* Search Box & Inputs */
QLineEdit {
    background-color: %(bg_input)s;
    color: %(text_primary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12.5px;
    selection-background-color: %(accent)s;
}

QLineEdit:focus {
    border: 1.5px solid %(accent)s;
    background-color: %(bg_input_hover)s;
    color: %(text_primary)s;
}

/* Combo Boxes */
QComboBox {
    background-color: %(bg_input)s;
    color: %(text_primary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 3px 6px;
    padding-right: 18px;
    font-size: 11.5px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: %(accent)s;
    background-color: %(bg_input_hover)s;
    color: %(text_primary)s;
}

QComboBox:focus {
    border-color: %(accent_hover)s;
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
    background-color: %(bg_input)s;
    color: %(text_primary)s;
    border: 1px solid %(border)s;
    border-radius: 8px;
    selection-background-color: %(accent)s;
    selection-color: %(accent_text)s;
    outline: none;
    padding: 4px;
}

/* Header Tool Buttons */
QPushButton#headerToolBtn {
    background-color: %(bg_input)s;
    color: %(text_secondary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#headerToolBtn:hover {
    background-color: %(bg_input_hover)s;
    border-color: %(border_hover)s;
    color: %(text_primary)s;
}

QPushButton#headerToolBtn:checked {
    background-color: %(accent_surface)s;
    border: 1.5px solid %(accent)s;
    color: %(accent_hover)s;
}

QPushButton#toolButton {
    background-color: %(bg_input)s;
    color: %(text_secondary)s;
    border: 1.5px solid %(border)s;
    border-radius: 7px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 600;
}

QPushButton#toolButton:hover {
    background-color: %(bg_input_hover)s;
    border-color: %(border_hover)s;
    color: %(text_primary)s;
}

QPushButton#toolButton:checked {
    background-color: %(accent_surface)s;
    border: 1.5px solid %(accent)s;
    color: %(accent_hover)s;
}

/* Primary Vibrant Button (Search, Action) */
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 %(accent_gradient_start)s, stop:1 %(accent_gradient_end)s);
    border: 1px solid %(accent_hover)s;
    color: %(accent_text)s;
    font-weight: bold;
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 12px;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 %(accent_hover)s, stop:1 %(accent_gradient_end)s);
    border-color: %(text_primary)s;
}

QPushButton#primaryButton:pressed {
    background-color: %(accent_surface)s;
}

/* Standard Push Buttons */
QPushButton {
    background-color: %(bg_input)s;
    color: %(text_primary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: %(bg_input_hover)s;
    border-color: %(accent)s;
    color: %(text_primary)s;
}

QPushButton:pressed {
    background-color: %(bg_capsule)s;
    border-color: %(accent)s;
}

/* Filter Chips */
QPushButton#filterChip {
    background-color: %(bg_input)s;
    color: %(text_secondary)s;
    border: 1.5px solid %(border)s;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#filterChip:hover {
    border-color: %(accent)s;
    background-color: %(bg_input_hover)s;
    color: %(text_primary)s;
}

QPushButton#filterChip:checked {
    background-color: %(accent_surface)s;
    border: 1.5px solid %(accent)s;
    color: %(accent_text)s;
    font-weight: bold;
}

QPushButton#nsfwChip {
    background-color: %(bg_input)s;
    color: %(text_secondary)s;
    border: 1.5px solid %(border)s;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#nsfwChip:hover {
    border-color: #f43f5e;
    background-color: %(bg_input_hover)s;
    color: #ffffff;
}

QPushButton#nsfwChip:checked {
    background-color: #881337;
    border: 1.5px solid #f43f5e;
    color: #ffe4e6;
    font-weight: bold;
}

QPushButton#sketchyChip {
    background-color: %(bg_input)s;
    color: %(text_secondary)s;
    border: 1.5px solid %(border)s;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton#sketchyChip:hover {
    border-color: #f59e0b;
    background-color: %(bg_input_hover)s;
    color: #ffffff;
}

QPushButton#sketchyChip:checked {
    background-color: #78350f;
    border: 1.5px solid #f59e0b;
    color: #fef3c7;
    font-weight: bold;
}

QPushButton#themeChip {
    background-color: %(bg_input)s;
    border: 1.5px solid %(border)s;
    border-radius: 12px;
    padding: 3px 7px;
    font-size: 11px;
    color: %(text_secondary)s;
}

QPushButton#themeChip:hover {
    border-color: %(accent_hover)s;
    background-color: %(bg_input_hover)s;
    color: %(text_primary)s;
}

QPushButton#themeChip:checked {
    background-color: %(accent_surface)s;
    border: 1.5px solid %(accent)s;
    color: %(accent_text)s;
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
    background: %(border)s;
    min-height: 28px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: %(border_hover)s;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Wallpaper Card */
QFrame#wallpaperCard {
    background-color: %(bg_surface)s;
    border: 1.5px solid %(border)s;
    border-radius: 12px;
}

QFrame#wallpaperCard:hover {
    border: 1.5px solid %(accent)s;
    background-color: %(bg_card_hover)s;
}

/* Card Badges */
QLabel#badge {
    background-color: rgba(0, 0, 0, 0.70);
    color: %(text_primary)s;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 10.5px;
    font-weight: bold;
}

QLabel#categoryBadge {
    background-color: %(accent_surface)s;
    color: %(text_primary)s;
    border: 1px solid %(accent)s;
    border-radius: 5px;
    padding: 2px 6px;
    font-size: 10.5px;
    font-weight: bold;
}

/* Pagination Frame & Badges */
QFrame#paginationFrame {
    background-color: %(bg_subsurface)s;
    border-top: 1px solid %(border_subtle)s;
    padding: 6px 16px;
}

QLabel#pageBadge {
    background-color: %(bg_input)s;
    border: 1px solid %(border)s;
    border-radius: 7px;
    padding: 4px 10px;
    min-width: 100px;
    qproperty-alignment: AlignCenter;
    font-weight: bold;
    color: %(text_primary)s;
    font-size: 12px;
}

/* SpinBox */
QSpinBox {
    background-color: %(bg_input)s;
    color: %(text_primary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 600;
}

QSpinBox:focus {
    border-color: %(accent)s;
}

/* Status Bar */
QStatusBar {
    background-color: %(bg_capsule)s;
    color: %(text_muted)s;
    border-top: 1px solid %(border_subtle)s;
    font-size: 12px;
    padding: 3px 12px;
}

/* Tooltips */
QToolTip {
    background-color: %(bg_surface)s;
    color: %(text_primary)s;
    border: 1.5px solid %(border)s;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}

/* Dialog & Settings */
QDialog {
    background-color: %(bg_base)s;
    color: %(text_primary)s;
}

QGroupBox {
    border: 1px solid %(border)s;
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 12px;
    font-weight: bold;
    color: %(text_primary)s;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    color: %(text_primary)s;
}
"""


def get_stylesheet(theme_id: str = "dark") -> str:
    """Generate complete CSS stylesheet for given theme ID."""
    pal = get_palette(theme_id)
    css = _TEMPLATE_STYLESHEET % pal
    return css.replace(
        "__CHEVRON_NORMAL__", _CHEVRON_NORMAL
    ).replace(
        "__CHEVRON_HOVER__", _CHEVRON_HOVER
    )


DARK_STYLESHEET = get_stylesheet("dark")
