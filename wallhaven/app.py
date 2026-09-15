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
    # 1. Check PyInstaller bundle directory
    if hasattr(sys, "_MEIPASS"):
        bundle_asset = Path(sys._MEIPASS) / "assets" / filename
        if bundle_asset.exists():
            return bundle_asset
        bundle_direct = Path(sys._MEIPASS) / filename
        if bundle_direct.exists():
            return bundle_direct

    # 2. Check alongside executable
    exe_dir = Path(sys.executable).parent / "assets" / filename
    if exe_dir.exists():
        return exe_dir

    # 3. Check package directory
    pkg_asset = Path(__file__).parent.parent / "assets" / filename
    if pkg_asset.exists():
        return pkg_asset

    # 4. Check Linux system icon paths
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

    # Windows taskbar grouping & icon setup
    if sys.platform == "win32":
        try:
            import ctypes
            myappid = "sedly.wallhaven.desktop.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
    else:
        # Linux Wayland / High DPI friendliness
        os.environ.setdefault("QT_QPA_PLATFORM", "wayland;xcb")

    app = QApplication(sys.argv)
    app.setApplicationName("Wallhaven Desktop")
    app.setApplicationDisplayName("Wallhaven Desktop")
    app.setDesktopFileName("wallhaven-desktop")

    # Set icon if available (prefer ICO on Windows, PNG on Linux)
    icon_name = "icon.ico" if sys.platform == "win32" else "icon.png"
    icon_path = get_asset_path(icon_name)
    if not icon_path.exists():
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
