@echo off
setlocal enabledelayedexpansion
title Wallhaven Desktop - Windows Build
cd /d "%~dp0\.."

echo ======================================================================
echo  [Wallhaven Desktop] Zahajuji sestaveni pro Windows (PyInstaller + Inno Setup)
echo ======================================================================
echo.

:: 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [CHYBA] Python nebyl nalezen v PATH.
    pause
    exit /b 1
)

:: 2. Setup/activate virtualenv or install tools
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [1/3] Instaluji PyInstaller a zavislosti...
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller

echo.
echo [2/3] Kompiluji standalone executable pres PyInstaller...
pyinstaller --noconsole --onefile --clean --icon=assets/icon.ico --add-data="assets;assets" --add-data="wallhaven/data;wallhaven/data" --collect-all PyQt6 --name="Wallhaven-Desktop" main.py

if %errorlevel% neq 0 (
    echo [CHYBA] PyInstaller sestaveni selhalo.
    pause
    exit /b 1
)

echo.
echo [3/3] Kompiluji instalator (Inno Setup)...
where iscc >nul 2>nul
if %errorlevel% equ 0 (
    iscc windows\installer.iss
    echo [OK] Instalator vytvoren v dist\Wallhaven-Desktop-Setup.exe
) else (
    echo [INFO] Inno Setup (iscc) nebyl nalezen v PATH. Instalator byl preskocen.
    echo Standalone soubor je pripraven v dist\Wallhaven-Desktop.exe
)

echo.
echo ======================================================================
echo  [HOTOVO] Sestaveni uspesne dokonceno!
echo  Vystup naleznete ve slozce dist\
echo ======================================================================
pause
