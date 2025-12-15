# Wine + MetaTrader 5 Telepítési Útmutató

Ez a dokumentum tartalmazza a Wine és MetaTrader 5 telepítésének részletes útmutatóját Linux környezetben.

## Áttekintés

Két fő megoldást fogunk megvizsgálni:
1. **Külön Wine prefix** (.mt5 könyvtár) - ajánlott, elszigetelt
2. **Alap Wine beállítás** - egyszerűbb, de kevésbé biztonságos

## 1. Wine Telepítés

### 1.1 Wine telepítése

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install wine-stable winbind

# Fedora
sudo dnf install wine

# Ellenőrzés
wine --version
```

### 1.2 Wine konfiguráció

```bash
# Wine prefix létrehozása a home könyvtárban
export WINEPREFIX=~/.mt5
winecfg

# A Wine konfiguráció ablakban:
# - Windows Version: Windows 10
# - Graphics: Enable window manager managed windows
# - Audio: ALSA driver
```

## 2. Külön Wine Prefix Megoldás (Ajánlott)

### 2.1 MT5 Wine prefix létrehozása

```bash
# MT5-hez dedikált Wine prefix létrehozása
mkdir -p ~/.mt5
export WINEPREFIX=~/.mt5

# Wine boot beállítása
wineboot

# Windows 10-ra állítása
winecfg  # Windows Version -> Windows 10
```

### 2.2 Szükséges Wine komponensek

```bash
# Fontos komponensek telepítése
winetricks -q corefonts
winetricks -q dotnet48  # MT5-höz szükséges .NET framework
winetricks -q vcrun2019  # Visual C++ runtime
```

### 2.3 MT5 Telepítés

#### Opció A: MetaTrader 5 (MetaQuotes)

```bash
# MT5 letöltése a MetaQuotes-tól
cd ~/Downloads
wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe

# Telepítés a külön Wine prefix-be
WINEPREFIX=~/.mt5 wine mt5setup.exe
```

#### Opció B: XM Forex MT5

```bash
# XM MT5 letöltése
cd ~/Downloads
wget https://xm.com/download/mt5/xm-mt5-setup.exe

# Telepítés a külön Wine prefix-be
WINEPREFIX=~/.mt5 wine xm-mt5-setup.exe
```

### 2.4 MT5 indítása

```bash
# MetaTrader 5 indítása
export WINEPREFIX=~/.mt5
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe

# Vagy XM MT5 esetén
wine ~/.mt5/drive_c/Program\ Files/XM\ MT5/terminal.exe
```

## 3. Alap Wine Beállítás (Egyszerűsített)

### 3.1 Wine konfiguráció

```bash
# Alap Wine beállítás
winecfg
# Windows Version: Windows 10
```

### 3.2 MT5 telepítés

```bash
# MT5 letöltése
cd ~/Downloads
wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe

# Telepítés
wine mt5setup.exe
```

### 3.3 MT5 indítása

```bash
# MT5 indítása
wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe
```

## 4. Gyakori problémák és megoldások

### 4.1 Ablak nem reagál

```bash
# Wine ablakkezelés beállítása
export WINEPREFIX=~/.mt5
winecfg
# Graphics -> Enable window manager managed windows
```

### 4.2 Font problémák

```bash
# Fontok telepítése
winetricks -q corefonts
winetricks -q tahoma
```

### 4.3 .NET framework hiba

```bash
# .NET framework telepítése
winetricks -q dotnet48
```

### 4.4 Audio problémák

```bash
# Audio driver beállítása
winecfg
# Audio -> ALSA driver
```

## 5. Telepítő Script

Hozz létre egy `scripts/setup_wine_mt5.sh` fájlt:

```bash
#!/bin/bash
# Wine + MT5 automatikus telepítő script

set -e

echo "=========================================="
echo "Wine + MetaTrader 5 Telepítő"
echo "=========================================="

# 1. Wine telepítés ellenőrzése
if ! command -v wine &> /dev/null; then
    echo "✗ Wine nincs telepítve!"
    echo "Telepítsd a Wine-t:"
    echo "sudo apt install wine-stable winbind"
    exit 1
fi
echo "✓ Wine telepítve"

# 2. Wine prefix létrehozása
export WINEPREFIX=~/.mt5
mkdir -p ~/.mt5
echo "✓ Wine prefix létrehozva: ~/.mt5"

# 3. Wine boot
echo "Wine inicializálása..."
wineboot
sleep 5

# 4. Wine konfiguráció
echo "Wine konfigurálása..."
winecfg &
sleep 3
pkill -f winecfg

# 5. Szükséges komponensek telepítése
echo "Komponensek telepítése..."
winetricks -q corefonts
winetricks -q dotnet48
winetricks -q vcrun2019

# 6. MT5 letöltés és telepítés
echo "Válaszd ki a brókert:"
echo "1) MetaTrader 5 (MetaQuotes Demo)"
echo "2) XM Forex MT5"
read -p "Választás (1-2): " choice

cd ~/Downloads

case $choice in
    1)
        echo "MetaTrader 5 letöltése..."
        wget -O mt5setup.exe https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe
        echo "MetaTrader 5 telepítése..."
        wine mt5setup.exe
        ;;
    2)
        echo "XM MT5 letöltése..."
        wget -O xm-mt5-setup.exe https://xm.com/download/mt5/xm-mt5-setup.exe
        echo "XM MT5 telepítése..."
        wine xm-mt5-setup.exe
        ;;
    *)
        echo "Érvénytelen választás"
        exit 1
        ;;
esac

echo "=========================================="
echo "✓ Telepítés sikeres!"
echo "=========================================="
echo "MT5 indítása:"
echo "export WINEPREFIX=~/.mt5"
echo "wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe"
```

## 6. MT5 Konfiguráció

### 6.1 Demo fiók létrehozása

1. Indítsd el az MT5-öt
2. File -> Open an Account
3. Válaszd ki a brókert (MetaQuotes vagy XM)
4. Töltsd ki a regisztrációs űrlapot
5. Erősítsd meg az email címet

### 6.2 Adatgyűjtés beállítása

1. Tools -> Options
2. Charts -> Max bars in chart: 50000
3. Expert Advisors -> Allow automated trading: True
4. OK

## 7. Expert Advisor Fejlesztés

### 7.1 MQL5 Editor telepítése

```bash
# MQL5 Editor indítása
export WINEPREFIX=~/.mt5
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/metaeditor.exe
```

### 7.2 EA létrehozása

1. Nyisd meg a MetaEditor-t
2. File -> New -> Expert Advisor
3. Töltsd ki az adatokat
4. Kód generálása

### 7.3 EA tesztelése

1. MT5-ben: View -> Strategy Tester
2. Válaszd ki az EA-t
3. Beállítások konfigurálása
4. Start

## 8. Integráció a Pythonnal

### 8.1 Kommunikációs könyvtár létrehozása

```bash
mkdir -p ~/mt5_ea_communication
```

### 8.2 Fájl alapú kommunikáció

Az EA és a Python között fájl alapú kommunikációt használunk:

```
~/mt5_ea_communication/
├── request.json    # Python -> EA
└── response.json   # EA -> Python
```

### 8.3 EA kód sablon

```mql
// neural_ai_mt5_collector.mq5

#property copyright "Neural AI Next"
#property link      "https://github.com/neural-ai-next"
#property version   "1.00"

input string CommunicationDir = "C:\\Users\\YourUser\\mt5_ea_communication";
input string RequestFile = "request.json";
input string ResponseFile = "response.json";

int OnInit() {
    Print("Neural AI MT5 Collector EA initialized");
    return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason) {
    Print("Neural AI MT5 Collector EA deinitialized");
}

void OnTick() {
    // Ellenőrzi a kérés fájlt
    CheckForRequests();
}

void CheckForRequests() {
    string requestPath = CommunicationDir + "\\" + RequestFile;

    if (FileExists(requestPath)) {
        // Beolvassa a kérést
        string request = ReadFile(requestPath);

        // Feldolgozza a kérést
        string response = ProcessRequest(request);

        // Írja a választ
        string responsePath = CommunicationDir + "\\" + ResponseFile;
        WriteFile(responsePath, response);

        // Törli a kérés fájlt
        FileDelete(requestPath);
    }
}

string ProcessRequest(string request) {
    // JSON parse
    // Adatgyűjtés CopyRates() segítségével
    // JSON válasz generálás
    return response;
}
```

## 9. Tesztelés

### 9.1 MT5 tesztelése

```bash
# MT5 indítása
export WINEPREFIX=~/.mt5
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe
```

### 9.2 EA tesztelése

1. MT5-ben: Navigator -> Expert Advisors
2. Húzd az EA-t egy chartra
3. Engedélyezd az automated tradinget
4. Ellenőrizd a logokat

## 10. Hibaelhárítás

### 10.1 Wine debug mód

```bash
# Részletes logolás
export WINEDEBUG=+all
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe
```

### 10.2 Wine prefix törlése

```bash
# Ha problémák vannak, töröld a Wine prefix-et
rm -rf ~/.mt5
# És telepítsd újra az egészet
```

### 10.3 MT5 újratelepítés

```bash
# MT5 eltávolítása
wine uninstaller
# Válaszd ki az MT5-öt és távolítsd el
# Majd telepítsd újra
```

## 11. Teljesítmény optimalizálás

### 11.1 Wine beállítások

```bash
# Wine performance beállítások
export WINEPREFIX=~/.mt5
winecfg
# Staging -> Enable CSMT
# Libraries -> Add: ntdll, kernel32 (Native, then Builtin)
```

### 11.2 MT5 beállítások

1. Tools -> Options
2. Charts -> Max bars in history: 50000
3. Charts -> Max bars in chart: 50000
4. Expert Advisors -> Max bars: 50000

## 12. Biztonság

### 12.1 Wine prefix elkülönítése

```bash
# Ne ossz meg más Wine prefix-ekkel
export WINEPREFIX=~/.mt5
```

### 12.2 Fájl jogosultságok

```bash
# Kommunikációs könyvtár biztonságos beállítása
chmod 700 ~/mt5_ea_communication
```

## 13. Hasznos parancsok

```bash
# Wine prefix törlése
rm -rf ~/.mt5

# Wine regiszter megnyitása
export WINEPREFIX=~/.mt5
wine regedit

# Wine program eltávolítása
wine uninstaller

# Wine konfiguráció
winecfg

# Winetricks
winetricks
```

## 14. További források

- [Wine HQ](https://wiki.winehq.org/)
- [MQL5 Dokumentáció](https://www.mql5.com/en/docs)
- [MetaTrader 5](https://www.metatrader5.com/)

---

**Dokumentum verzió**: 1.0
**Utolsó frissítés**: 2025-12-15
**Felelős**: Architect Mode
