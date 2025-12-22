# setup_wine_mt5.sh - Wine és MetaTrader 5 Telepítő Script

## 📝 Áttekintés

Ez a bash script Wine és MetaTrader 5 automatikus telepítését végzi Linux rendszereken. A script támogatja a Fedora, Ubuntu, Linux Mint és Debian disztribúciókat, valamint több bróker konfigurációját.

## 🎯 Főbb Funkciók

### Támogatott Rendszerek
- **Fedora Linux** (42+ verziók)
- **Ubuntu** (20.04+ verziók)
- **Linux Mint** (20+ verziók)
- **Debian GNU/Linux** (11+ verziók)

### Támogatott Brókerek
1. **MetaTrader 5** (MetaQuotes Demo)
2. **XM Forex MT5**

### Telepítési Lépések
1. Rendszer frissítése és Wine telepítése
2. Wine prefix létrehozása MT5-hez
3. Wine inicializálása Windows 11 kompatibilitással
4. WebView2 Runtime telepítése
5. MetaTrader 5 telepítése
6. Letöltött fájlok takarítása

## 📁 Fájl Információk

- **Elérési út:** `scripts/install/scripts/setup_wine_mt5.sh`
- **Típus:** Bash Script
- **Szerző:** MetaQuotes Ltd. (módosítva a Neural AI Next projekt számára)
- **Copyright:** 2000-2025, MetaQuotes Ltd.

## 🔧 Konfiguráció

### Környezeti Változók

```bash
# MetaTrader 5 letöltési URL (alapértelmezett: MetaQuotes Demo)
URL_MT5="https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe"

# WebView2 Runtime letöltési URL
URL_WEBVIEW="https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/f2910a1e-e5a6-4f17-b52d-7faf525d17f8/MicrosoftEdgeWebview2Setup.exe"

# Wine verzió (stable vagy devel)
WINE_VERSION="stable"

# Wine prefix elérési útja
WINEPREFIX_MT5="$HOME/.mt5"
```

### Bróker Választás

A script futásakor a felhasználó kiválaszthatja a kívánt brókert:

1. **MetaTrader 5 (MetaQuotes Demo)** - Alapértelmezett
2. **XM Forex MT5** - XM specifikus telepítő

## 🚀 Használat

### Futtatás

```bash
# Script futtathatóvá tétele
chmod +x scripts/install/scripts/setup_wine_mt5.sh

# Futtatás
./scripts/install/scripts/setup_wine_mt5.sh
```

### MT5 Indítása Telepítés Után

```bash
# Wine prefix beállítása
export WINEPREFIX=~/.mt5

# MT5 indítása
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe
```

## 📋 Telepítési Folyamat

### 1. Rendszer Frissítés
- Csomaglisták frissítése
- Rendszer komponensek frissítése

### 2. Wine Telepítés
- WineHQ repository hozzáadása (disztribúció specifikus)
- Wine és Wine Mono telepítése
- 32-bit architektúra támogatás engedélyezése (Debian alapú rendszerek)

### 3. Wine Prefix Létrehozása
- Dedikált Wine prefix létrehozása MT5-hez (`~/.mt5`)
- Wine inicializálása
- Windows verzió beállítása Windows 11-re

### 4. WebView2 Runtime Telepítés
- Microsoft Edge WebView2 Runtime letöltése
- Automatikus telepítés csendes módban

### 5. MetaTrader 5 Telepítés
- Kiválasztott bróker telepítőjének letöltése
- Interaktív telepítés futtatása

### 6. Takarítás
- Letöltött telepítőfájlok törlése

## 🔍 Részletes Leírás

### Fedora Linux Támogatás

A script a Fedora verziószámától függően a megfelelő WineHQ repository-t konfigurálja:
- Fedora 42+: `winehq.repo` (42-es verzióból)
- Fedora 41: `winehq.repo` (41-es verzióból)

### Ubuntu Támogatás

Az Ubuntu különböző verzióinak támogatása:
- Ubuntu 24.10+ (Plucky): `winehq-plucky.sources`
- Ubuntu 24.04 (Noble): `winehq-noble.sources`
- Ubuntu 23.04-23.10 (Lunar): `winehq-lunar.sources`
- Ubuntu 22.10 (Kinetic): `winehq-kinetic.sources`
- Ubuntu 21.04-22.04 (Jammy): `winehq-jammy.sources`
- Ubuntu 20.04-20.10 (Focal): `winehq-focal.sources`
- Régebbi verziók: `winehq-bionic.sources`

### Linux Mint Támogatás

- Linux Mint 22+: Ubuntu Noble repository
- Linux Mint 20-21: Ubuntu Focal repository

### Debian Támogatás

- Debian 13+ (Trixie): `winehq-trixie.sources`
- Debian 12 (Bookworm): `winehq-bookworm.sources`

## ⚠️ Fontos Megjegyzések

1. **Jogosultságok:** A script sudo parancsokat használ, ezért rendszergazdai jogosultság szükséges.
2. **Rendszer Újraindítás:** A telepítés után ajánlott a rendszert újraindítani.
3. **Internet Kapcsolat:** A telepítéshez stabil internetkapcsolat szükséges.
4. **Tárhely:** Győződjön meg róla, hogy elegendő szabad tárhely áll rendelkezésre.

## 🐛 Hibaelhárítás

### Wine Verzió Problémák

Ha a Wine telepítése során hibák lépnek fel:

```bash
# WineHQ repository manuális hozzáadása
sudo dnf config-manager --add-repo https://dl.winehq.org/wine-builds/fedora/winehq.repo

# Telepítés
sudo dnf install winehq-stable
```

### WebView2 Runtime Telepítési Hiba

Ha a WebView2 Runtime telepítése sikertelen:

```bash
# Manuális telepítés
WINEPREFIX=~/.mt5 wine ~/Downloads/webview2.exe /silent /install
```

### MT5 Indítási Problémák

Ha az MT5 nem indul el:

```bash
# Wine prefix ellenőrzése
ls -la ~/.mt5

# Wine konfiguráció ellenőrzése
WINEPREFIX=~/.mt5 winecfg
```

## 📚 Kapcsolódó Dokumentáció

- [Telepítési Útmutató](../../../INSTALLATION_GUIDE.md)
- [Wine és MT5 Kommunikációs Beállítások](../../../WINE_MT5_SETUP.md)
- [Fejlesztői Dokumentáció](../../../development/TASK_TREE_SCRIPTS.md)

## 🔄 Verzió Történet

- **v1.0** - Kezdeti verzió, alapvető Wine és MT5 telepítés támogatással
- **v1.1** - Több bróker támogatás hozzáadása (XM Forex)
- **v1.2** - WebView2 Runtime automatikus telepítés hozzáadása
- **v1.3** - Windows 11 kompatibilitás beállítása

## 📞 Támogatás

Probléma esetén kérjük, nyisson egy issue-t a projekt GitHub repository-jában, vagy forduljon a fejlesztői dokumentációhoz.

---
*Utolsó frissítés: 2025-12-22*
