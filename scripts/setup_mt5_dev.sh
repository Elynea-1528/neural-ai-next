#!/bin/bash
# MT5 fejlesztői környezet beállítása

# Konstansok
MT5_PREFIX="$HOME/.wine_mt5"
MT5_PATH="$MT5_PREFIX/drive_c/Program Files/XM MT5"
MQL5_PATH="$MT5_PATH/MQL5"
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
EA_NAME="NeuralAICollector"

# Színek
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ellenőrizzük, hogy telepítve van-e a Wine
check_wine() {
    if ! command -v wine &> /dev/null; then
        echo -e "${RED}Wine nincs telepítve. Telepítse a Wine-t először.${NC}"
        exit 1
    fi
}

# Wine prefix létrehozása és konfigurálása (csak 64 bit)
setup_wine_prefix() {
    if [ ! -d "$MT5_PREFIX" ]; then
        echo -e "${YELLOW}Wine prefix létrehozása (64-bit)...${NC}"
        export WINEPREFIX="$MT5_PREFIX"
        export WINEARCH=win64
        winecfg
        winetricks vcrun2019 dotnet48
    fi
}

# Könyvtárak létrehozása
setup_directories() {
    echo -e "${YELLOW}Könyvtárak létrehozása...${NC}"
    mkdir -p "$MQL5_PATH/Experts/NeuralAI"
    mkdir -p "$MQL5_PATH/Include/NeuralAI"
    mkdir -p "$MQL5_PATH/Libraries/NeuralAI"
    mkdir -p "$MQL5_PATH/Files/NeuralAI"
    mkdir -p "$MQL5_PATH/Logs/NeuralAI"
}

# Szimbolikus linkek létrehozása a fejlesztéshez
create_symlinks() {
    echo -e "${YELLOW}Szimbolikus linkek létrehozása...${NC}"
    ln -sf "$PROJECT_ROOT/experts/mt5_collector_ea.mq5" "$MQL5_PATH/Experts/NeuralAI/"
    ln -sf "$PROJECT_ROOT/experts/include/"* "$MQL5_PATH/Include/NeuralAI/"
    ln -sf "$PROJECT_ROOT/experts/libraries/"* "$MQL5_PATH/Libraries/NeuralAI/"
}

# MT5 indítása
start_mt5() {
    echo -e "${YELLOW}MetaTrader 5 indítása...${NC}"
    export WINEPREFIX="$MT5_PREFIX"
    export WINEARCH=win64
    export WINE_FULLSCREEN_FSR=1
    export WINE_FULLSCREEN_INTEGER_SCALING=1
    export WINEDEBUG="+all"
    wine "$MT5_PATH/terminal64.exe" &> "$MT5_PREFIX/mt5_debug.log" &
    echo -e "${GREEN}Debug log: $MT5_PREFIX/mt5_debug.log${NC}"
}

# Registry beállítások
setup_registry() {
    echo -e "${YELLOW}Registry beállítások...${NC}"
    cat > /tmp/mt5_reg.reg << EOF
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Wine\Direct3D]
"MaxVersionGL"="32768"

[HKEY_CURRENT_USER\Software\Wine\X11 Driver]
"GrabFullscreen"="Y"
"Decorated"="Y"
"DXGrab"="Y"
EOF
    wine regedit /tmp/mt5_reg.reg
    rm /tmp/mt5_reg.reg
}

# File watch és automatikus másolás
watch_files() {
    echo -e "${YELLOW}Fájlok figyelése módosításra...${NC}"
    while inotifywait -e modify -r "$PROJECT_ROOT/experts/"; do
        echo -e "${GREEN}Változás észlelve, fájlok másolása...${NC}"
        create_symlinks
    done
}

# Diagnosztika
check_dependencies() {
    echo -e "${YELLOW}Függőségek ellenőrzése...${NC}"
    local deps=("wine" "winetricks" "inotifywait")
    local missing=()
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}Hiányzó függőségek: ${missing[*]}${NC}"
        echo -e "${YELLOW}Telepítse a következő paranccsal:${NC}"
        echo "sudo apt install wine winetricks inotify-tools"
        exit 1
    fi
}

# Wine prefix ellenőrzése
check_mt5_installation() {
    if [ ! -f "$MT5_PATH/terminal64.exe" ]; then
        echo -e "${RED}MT5 nincs telepítve a $MT5_PATH útvonalon${NC}"
        echo -e "${YELLOW}Kérem telepítse az XM MT5-öt:${NC}"
        echo "wine ~/Letöltések/xm.com5setup.exe"
        exit 1
    fi
}

# Fő függvény
main() {
    echo -e "${GREEN}MT5 fejlesztői környezet beállítása...${NC}"
    check_dependencies
    check_wine
    setup_wine_prefix
    check_mt5_installation
    setup_directories
    create_symlinks
    setup_registry
    echo -e "${GREEN}Beállítás kész!${NC}"
    echo -e "${YELLOW}MetaTrader 5 indítása...${NC}"
    start_mt5
    echo -e "${YELLOW}Fájlok figyelése...${NC}"
    watch_files
}

# Script futtatása
main
