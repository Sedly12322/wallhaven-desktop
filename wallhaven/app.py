import os
import signal
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from wallhaven.main_window import MainWindow
from wallhaven.styles import DARK_STYLESHEET


def get_asset_path(filename: str) -> Path:
    # Check package directory first
    pkg_asset = Path(__file__).parent.parent / "assets" / filename
    if pkg_asset.exists():
        return pkg_asset
    # Check system icon paths
    sys_asset = Path(f"/usr/share/icons/hicolor/256x256/apps/{filename}")
    if sys_asset.exists():
        return sys_asset
    local_asset = Path.home() / f".local/share/icons/hicolor/256x256/apps/{filename}"
    if local_asset.exists():
        return local_asset
    return pkg_asset


def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Wayland / High DPI friendliness
    os.environ.setdefault("QT_QPA_PLATFORM", "wayland;xcb")

    app = QApplication(sys.argv)
    app.setApplicationName("Wallhaven Desktop")
    app.setApplicationDisplayName("Wallhaven Desktop")
    app.setDesktopFileName("wallhaven-desktop")

    # Set icon if available
    icon_path = get_asset_path("icon.png")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Apply global stylesheet
    app.setStyleSheet(DARK_STYLESHEET)

    window = MainWindow()
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
