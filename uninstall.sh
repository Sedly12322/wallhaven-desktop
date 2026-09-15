#!/usr/bin/env bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Odinstalace Wallhaven Desktop ===${NC}"

INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/wallhaven-desktop"
BIN_DIR="$HOME/.local/bin"
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
ICON_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/256x256/apps"

rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/wallhaven-desktop"
rm -f "$BIN_DIR/wallhaven"
rm -f "$APP_DIR/wallhaven-desktop.desktop"
rm -f "$ICON_DIR/wallhaven-desktop.png"

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APP_DIR" || true

echo -e "${GREEN}✓ Wallhaven Desktop byl úspěšně odinstalován.${NC}"
