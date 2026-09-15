# 🌌 Wallhaven Desktop

<div align="center">

[![Arch Linux](https://img.shields.io/badge/Arch%20Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)](https://archlinux.org)
[![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/Sedly12322/wallhaven-desktop/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Moderní desktopová aplikace v Pythonu (PyQt6) pro procházení, stahování a automatické nastavování tapet ze serveru [Wallhaven.cc](https://wallhaven.cc).**  
Plně podporuje **Arch Linux** (Wayland / Hyprland / X11) i **Microsoft Windows 10 a 11**.

</div>

---

## 📥 Instalace na Arch Linux

Každý uživatel Arch Linuxu si může aplikaci snadno nainstalovat jedním z následujících způsobů:

### ⚡ Možnost 1: Rychlá instalace přes skript (Doporučeno)

Jednoduše naklonujte repozitář a spusťte instalátor. Nainstaluje aplikaci, ikonu, `.desktop` položku do menu a příkaz do `~/.local/bin`:

```bash
git clone https://github.com/Sedly12322/wallhaven-desktop.git
cd wallhaven-desktop
./install.sh
```

Po instalaci stačí kdekoliv v terminálu napsat:
```bash
wallhaven-desktop
# nebo zkráceně:
wallhaven
```
Nebo aplikaci spustit z vašeho launcheru (Rofi, Wofi, Hyprland, KDE, GNOME).

---

### 📦 Možnost 2: Nativní Arch balíček (`makepkg`)

Pokud preferujete správu přes `pacman` a `makepkg`:

```bash
git clone https://github.com/Sedly12322/wallhaven-desktop.git
cd wallhaven-desktop
makepkg -si
```

---

### 🐍 Možnost 3: Přes `pipx`

```bash
pipx install git+https://github.com/Sedly12322/wallhaven-desktop.git
```

---

### 🚀 Možnost 4: Spuštění bez instalace

Pokud chcete aplikaci jen vyzkoušet bez instalace do systému:

```bash
git clone https://github.com/Sedly12322/wallhaven-desktop.git
cd wallhaven-desktop
./run.sh
```

---

## 🪟 Instalace na Windows (10 / 11)

Pro uživatele Windows jsou k dispozici hotové instalační balíčky na stránce [**GitHub Releases**](https://github.com/Sedly12322/wallhaven-desktop/releases):

1. **Instalátor (.exe):** Stáhněte a spusťte **`Wallhaven-Desktop-Setup.exe`**.  
   *Nainstaluje aplikaci a vytvoří zástupce na ploše i v nabídce Start.*
2. **Přenosná verze (Portable .zip):** Stáhněte **`Wallhaven-Desktop-Portable.zip`**, rozbalte kamkoliv a spusťte přímo `Wallhaven-Desktop.exe` bez nutnosti instalace.

*(Případně lze spustit ze zdrojových kódů dvojklikem na **`run.bat`**).*

---

## ✨ Klíčové funkce

- **🎨 Moderní tmavý vzhled (Dark UI):**
  - Elegantní rozhraní ladící k moderním linuxovým distribucím a Hyprland dotfiles.
  - Responzivní mřížka karet s plynulým scrollováním a štítky s rozlišením (např. `4K UHD`, `2K`, `1080p`).

- **🖼️ Automatické nastavení tapety po stažení:**
  - Po stažení obrázku jej aplikace dokáže ihned nastavit na vaši plochu.
  - Plně integrováno s **Hyprland / quickshell (`switchwall.sh`)** včetně automatického přebarvení systému přes Matugen.
  - Podporuje také obecné nástroje: `swww`, `waypaper`, `hyprpaper`, `feh`, `nitrogen` i vlastní příkazy.
  - Rychlé zapnutí/vypnutí pomocí tlačítka **`🖼️ Auto-tapeta`** v horní liště.

- **🔍 Pokročilé vyhledávání a filtry:**
  - **Fulltext:** klíčová slova, autoři (`@username`), štítky (`#cyberpunk`).
  - **Kategorie:** *General*, *Anime*, *People*.
  - **Purity:** *SFW*, *Sketchy* a *NSFW* (s podporou API klíče).
  - **Řazení:** *Toplist*, *Hot*, *Nejnovější*, *Zhlédnutí*, *Oblíbené*, *Náhodné*, *Relevance*.
  - **Časové rozmezí (Toplist):** od 1 dne až po 1 rok.
  - **Poměr stran:** 16:9, 16:10, 21:9 Ultrawide, 32:9 Superwide, 9:16 Mobilní.
  - **Rozlišení:** od 1080p až po 8K.
  - **Barevná paleta (🎨 Barvy):** 18 oficiálních odstínů Wallhaven pro filtrování podle dominantní barvy.

- **🔍 Detailní náhled tapety:**
  - Kliknutím na libovolnou kartu se otevře velké okno s náhledem, kompletními specifikacemi a dominantní paletou.
  - **Klikatelné štítky (Tags):** jedním klikem vyhledáte další podobné tapety.
  - Samostatné tlačítko **„🖼️ Nastavit jako tapetu nyní“**.

- **💾 Flexibilní ukládání:**
  - Výběr složky a názvu souboru systémovým dialogem.
  - Zobrazení průběhu stahování v MB a procentech.
  - Tlačítko pro okamžité otevření složky se staženou tapetou ve vašem správci souborů.

- **⚙️ Nastavení a API klíč:**
  - Možnost zadat vlastní Wallhaven API klíč pro odemčení NSFW obsahu.
  - Nastavení výchozí složky a vlastního příkazu pro aplikaci tapety.
  - Přehled a snadné promazání mezipaměti náhledů.

---

## 🗑️ Odinstalace

Pokud jste instalovali přes `./install.sh`:
```bash
./uninstall.sh
```

Pokud jste instalovali přes `makepkg -si`:
```bash
sudo pacman -R wallhaven-desktop-git
```

---

## 📄 Licence

Tento projekt je licencován pod licencí [MIT](LICENSE).
