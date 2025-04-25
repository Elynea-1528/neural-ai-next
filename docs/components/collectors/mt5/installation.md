# MetaTrader 5 Linux Telepítési Útmutató

## Rendszerkövetelmények

### Linux rendszer
- Ubuntu 20.04 vagy újabb (ajánlott)
- Wine 6.0 vagy újabb
- Winetricks
- X11 támogatás

### Szükséges csomagok
```bash
# Wine és függőségek telepítése
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y wine64 wine32 winetricks

# X11 csomagok
sudo apt install -y xorg openbox
```

## MetaTrader 5 Telepítés

### 1. Wine konfiguráció
```bash
# Wine prefix létrehozása
export WINEPREFIX=~/.wine_mt5
export WINEARCH=win64
winecfg

# Szükséges komponensek telepítése
winetricks corefonts vcrun2019 dotnet48
```

### 2. XM MT5 Telepítés
```bash
# Letöltött telepítő futtatása
cd ~/Letöltések
wine xm.com5setup.exe
```

### 3. Wine Registry Beállítások
```bash
# Registry szerkesztő megnyitása
wine regedit

# Kulcs: HKEY_CURRENT_USER\Software\Wine\Direct3D
# Érték: "MaxVersionGL" = "32768"
```

## MetaTrader 5 Konfiguráció

### 1. Alapbeállítások
- Terminal indítása: `wine ~/.wine_mt5/drive_c/Program\ Files/XM\ MT5/terminal64.exe`
- Felhasználói adatok megadása
- Szerverválasztás: "XM-Demo" vagy "XM-Real"

### 2. Expert Advisor Beállítások
```plaintext
Tools -> Options -> Expert Advisors

[x] Allow automated trading
[x] Allow DLL imports
[x] Allow WebRequest for listed URL
    - Adja hozzá: "localhost:8765" (vagy a konfigurált portot)
```

### 3. Automatikus Indítás Script
```bash
#!/bin/bash
# start_mt5.sh

export DISPLAY=:0
export WINEPREFIX=~/.wine_mt5
export WINEARCH=win64

# X11 szerver indítása (ha szükséges)
Xvfb :0 -screen 0 1024x768x16 &

# Várakozás az X szerver indulására
sleep 2

# MT5 indítása
wine ~/.wine_mt5/drive_c/Program\ Files/XM\ MT5/terminal64.exe
```

## Hibaelhárítás

### 1. Grafikus Problémák
```bash
# Wine OpenGL beállítások
export WINE_FULLSCREEN_FSR=1
export WINE_FULLSCREEN_INTEGER_SCALING=1
```

### 2. Hálózati Problémák
```bash
# Tűzfal beállítások
sudo ufw allow 8765/tcp  # WebSocket port
sudo ufw allow 443/tcp   # MT5 kapcsolat
```

### 3. Teljesítmény Optimalizáció
```bash
# Wine CPU prioritás
renice -n -5 -p $(pgrep -f terminal64.exe)

# I/O prioritás
ionice -c 2 -n 0 -p $(pgrep -f terminal64.exe)
```

## EA Telepítés

### 1. EA Könyvtár Helye
```
~/.wine_mt5/drive_c/Program Files/XM MT5/MQL5/Experts/
```

### 2. EA Fájlok Másolása
```bash
# EA másolása
cp NeuralAICollector.ex5 ~/.wine_mt5/drive_c/Program\ Files/XM\ MT5/MQL5/Experts/

# Könyvtárak létrehozása
mkdir -p ~/.wine_mt5/drive_c/Program\ Files/XM\ MT5/MQL5/Files/NeuralAI
mkdir -p ~/.wine_mt5/drive_c/Program\ Files/XM\ MT5/MQL5/Logs/NeuralAI
```

## Monitoring

### 1. Log Fájlok
```
~/.wine_mt5/drive_c/Program Files/XM MT5/MQL5/Logs/
```

### 2. Rendszer Monitor
```bash
# Wine folyamatok figyelése
watch -n 1 'ps aux | grep terminal64.exe'

# Hálózati forgalom
sudo tcpdump -i any port 8765
```

## Automatikus Újraindítás

### 1. Systemd Service
```ini
# /etc/systemd/system/mt5.service
[Unit]
Description=MetaTrader 5 Terminal
After=network.target

[Service]
Type=simple
User=your_username
Environment=DISPLAY=:0
Environment=WINEPREFIX=/home/your_username/.wine_mt5
Environment=WINEARCH=win64
ExecStart=/home/your_username/start_mt5.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Service Kezelés
```bash
# Service engedélyezése
sudo systemctl enable mt5.service

# Service indítása
sudo systemctl start mt5.service

# Státusz ellenőrzése
sudo systemctl status mt5.service
```

## Biztonsági Megfontolások

1. **Hozzáférés Korlátozása**
   - Wine prefix jogosultságok
   - EA konfiguráció védelem
   - Hálózati hozzáférés korlátozása

2. **Monitoring**
   - Rendszer erőforrás figyelés
   - Hálózati forgalom monitorozás
   - Log elemzés

3. **Backup**
   - Rendszeres EA konfiguráció mentés
   - Wine prefix biztonsági mentés
   - Log archiválás
