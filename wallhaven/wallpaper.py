import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Tuple


def detect_wallpaper_command() -> list[str]:
    """
    Detects the best wallpaper setter command for the current environment.
    Supports Windows (native API) and Linux (Hyprland/quickshell, swww, feh, etc.).
    """
    if sys.platform == "win32":
        return ["Nativní Windows API (SystemParametersInfoW)"]

    # 1. Quickshell / illogical-impulse switchwall.sh (used by Hyprland dots)
    qs_script = Path.home() / ".config/quickshell/ii/scripts/colors/switchwall.sh"
    if qs_script.exists() and os.access(qs_script, os.X_OK):
        return [str(qs_script), "--image", "{file}"]

    # 2. swww
    if shutil.which("swww"):
        return ["swww", "img", "--transition-type", "grow", "{file}"]

    # 3. waypaper
    if shutil.which("waypaper"):
        return ["waypaper", "--wallpaper", "{file}"]

    # 4. hyprpaper
    if shutil.which("hyprpaper") and shutil.which("hyprctl"):
        return ["hyprctl", "hyprpaper", "wallpaper", ",{file}"]

    # 5. feh
    if shutil.which("feh"):
        return ["feh", "--bg-fill", "{file}"]

    # 6. nitrogen
    if shutil.which("nitrogen"):
        return ["nitrogen", "--set-zoom-fill", "{file}"]

    # 7. GNOME
    if shutil.which("gsettings") and "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
        return ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://{file}"]

    if qs_script.exists():
        return ["bash", str(qs_script), "--image", "{file}"]

    return []


def set_desktop_wallpaper(file_path: str, custom_cmd: str = "") -> Tuple[bool, str]:
    """
    Sets the downloaded wallpaper on the desktop.
    Returns (success: bool, message: str).
    """
    if not os.path.exists(file_path):
        return False, f"Soubor neexistuje: {file_path}"

    abs_path = str(Path(file_path).resolve())

    # If custom command provided
    if custom_cmd.strip():
        cmd_str = custom_cmd.replace("{file}", f'"{abs_path}"')
        try:
            res = subprocess.run(
                cmd_str,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15,
            )
            if res.returncode == 0:
                _send_notification("Tapeta změněna", f"Tapeta byla nastavena na: {os.path.basename(abs_path)}")
                return True, "Tapeta byla úspěšně nastavena."
            return False, f"Příkaz selhal ({res.returncode}): {res.stderr.strip()}"
        except Exception as e:
            return False, str(e)

    # Windows native API
    if sys.platform == "win32":
        try:
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02
            res = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
            )
            if res:
                return True, "Tapeta byla úspěšně nastavena."
            return False, "Volání Windows API (SystemParametersInfoW) selhalo."
        except Exception as e:
            return False, str(e)

    # Linux Automatic detection
    cmd_template = detect_wallpaper_command()
    if not cmd_template:
        return False, "Nebyl nalezen žádný podporovaný nástroj pro nastavení tapety."

    # If using hyprpaper, preload first
    if "hyprpaper" in cmd_template[0]:
        try:
            subprocess.run(
                ["hyprctl", "hyprpaper", "preload", abs_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        except Exception:
            pass

    cmd = [arg.replace("{file}", abs_path) for arg in cmd_template]
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
        if res.returncode == 0:
            _send_notification("Tapeta změněna", f"Tapeta byla nastavena na: {os.path.basename(abs_path)}")
            return True, "Tapeta byla úspěšně nastavena."
        return False, f"Příkaz selhal: {res.stderr.strip()}"
    except Exception as e:
        return False, str(e)


def _send_notification(title: str, msg: str):
    if sys.platform != "win32" and shutil.which("notify-send"):
        try:
            subprocess.run(
                ["notify-send", "-a", "Wallhaven Desktop", title, msg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3,
            )
        except Exception:
            pass
