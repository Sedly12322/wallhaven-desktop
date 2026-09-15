# 🌌 Wallhaven Desktop pro Arch Linux

Moderní grafická desktopová aplikace v **Pythonu (PyQt6)** pro procházení, vyhledávání a stahování tapet ze serveru [Wallhaven.cc](https://wallhaven.cc).

Vytvořeno přímo na míru pro **Arch Linux** a prostředí Wayland / Hyprland / X11.

---

## 🚀 Jak aplikaci spustit

Aplikace je plně nainstalována a připravena:

### 1. Z aplikačního menu (Rofi / Wofi / Hyprland)
Stiskněte svoji klávesovou zkratku pro spuštění aplikací (např. `Super` nebo `Super + Space`) a vyhledejte:
```text
Wallhaven Desktop
```

### 2. Z terminálu
Aplikace je dostupná přímo v `$PATH` (`~/.local/bin`):
```bash
wallhaven-desktop
# nebo zkráceně:
wallhaven
```

### 3. Přímo ze složky projektu
```bash
cd ~/projects/wallhaven-desktop
./run.sh
```

---

## ✨ Funkce a možnosti

- **🎨 Moderní tmavý vzhled (Dark Theme):**
  - Stylové rozhraní ladící s estetikou Arch Linuxu a Hyprlandu.
  - Plynulé zobrazení náhledů, responzivní mřížka karet a přehledné štítky.

- **🔍 Pokročilé vyhledávání a filtry:**
  - **Vyhledávací pole:** fulltextové hledání (např. `nature`, `cyberpunk`, `anime`, `@autor`, `#tag`).
  - **Kategorie:** přepínání *General*, *Anime*, *People*.
  - **Purity:** *SFW*, *Sketchy* a *NSFW* (s podporou zadání API klíče).
  - **Řazení:** *Toplist*, *Hot*, *Nejnovější*, *Nejnavštěvovanější*, *Oblíbené*, *Náhodné*, *Relevance*.
  - **Časový rozsah (pro Toplist):** *1 Den*, *3 Dny*, *1 Týden*, *1 Měsíc*, *3 Měsíce*, *1 Rok*.
  - **Poměr stran (Aspect Ratio):** *16:9*, *16:10*, *21:9 Ultrawide*, *32:9 Superwide*, *9:16 Mobilní*.
  - **Minimální rozlišení:** *1080p*, *1440p (2K)*, *4K UHD*, *8K UHD*.
  - **Barevný filtr (Color search):** paleta oficiálních barev Wallhaven pro filtrování podle dominantního odstínu.

- **🖼️ Detailní náhled tapety:**
  - Kliknutím na jakoukoliv tapetu se otevře detailní okno s velkým náhledem.
  - Zobrazení všech metadat: přesné rozlišení, poměr stran, velikost souboru, formát (PNG/JPG), počet zhlédnutí a oblíbených.
  - **Klikatelné štítky (Tags):** kliknutím na jakýkoliv tag se okamžitě vyhledají další podobné tapety.
  - Dominantní barevná paleta tapety.
  - Odkaz pro otevření přímo na webu Wallhaven.cc.

- **💾 Stahování a automatické nastavení tapety:**
  - **Automatické nastavení tapety:** po stažení tapety se obrázek může automaticky okamžitě nastavit jako tapeta vaší plochy (včetně integrace s Hyprlandem / quickshell `switchwall.sh` a generováním barevných schémat).
  - Tlačítko **🖼️ Auto-tapeta** v horní liště pro rychlé zapnutí/vypnutí automatického nastavování.
  - V detailu tapety je navíc k dispozici samostatné tlačítko **🖼️ Nastavit jako tapetu nyní**.
  - Při každém stažení se otevře dialog pro výběr umístění a názvu souboru (s předvyplněným doporučeným názvem a výchozí složkou, např. `~/Obrázky/Wallpapers`).
  - Zobrazení průběhu stahování s ukazatelem v MB a procentech.
  - Tlačítko pro okamžité otevření složky se staženým obrázkem ve vašem správci souborů.

- **⚙️ Nastavení a API klíč:**
  - Možnost vložit vlastní Wallhaven API klíč pro odemčení NSFW tapet a vašich vlastních kolekcí.
  - Volba výchozí složky pro stahování.
  - Zobrazení velikosti mezipaměti náhledů a možnost jejího vymazání.

- **⚡ Rychlost a mezipaměť:**
  - Asynchronní stahování náhledů na pozadí (UI nikdy nezamrzá).
  - Inteligentní mezipaměť v `~/.cache/wallhaven-desktop/` pro okamžité procházení.

---

## 📁 Umístění souborů

- **Kód projektu:** `~/projects/wallhaven-desktop/`
- **Virtuální prostředí (Python venv):** `~/projects/wallhaven-desktop/.venv/`
- **Konfigurace:** `~/.config/wallhaven-desktop/config.json`
- **Mezipaměť (náhledy):** `~/.cache/wallhaven-desktop/`
- **Spouštěcí ikona (.desktop):** `~/.local/share/applications/wallhaven-desktop.desktop`
- **Spouštěcí příkaz:** `~/.local/bin/wallhaven-desktop`
