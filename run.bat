@echo off
setlocal
title Wallhaven Desktop
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [Wallhaven Desktop] Priprava Python prostredi...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py %*
) else (
    start "" ".venv\Scripts\python.exe" main.py %*
)
