import os
import signal
import sys
from pathlib import Path

# Ensure package root is in sys.path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from wallhaven.main_window import MainWindow
from wallhaven.styles import DARK_STYLESHEET


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
    icon_path = Path(__file__).parent / "assets" / "icon.png"
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
