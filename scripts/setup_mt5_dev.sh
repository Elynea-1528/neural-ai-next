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

# Wine prefix létrehozása és konfigurálása
setup_wine_prefix() {
    if [ ! -d "$MT5_PREFIX" ]; then
        echo -e "${YELLOW}Wine prefix létrehozása...${NC}"
        export WINEPREFIX="$MT5_PREFIX"
        export WINEARCH=win64
        winecfg
        winetricks corefonts vcrun2019 dotnet48
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
    # EA fájlok
    ln -sf "$PROJECT_ROOT/experts/mt5_collector_ea.mq5" "$MQL5_PATH/Experts/NeuralAI/"
    ln -sf "$PROJECT_ROOT/experts/include/"* "$MQL5_PATH/Include/NeuralAI/"
    ln -sf "$PROJECT_ROOT/experts/libraries/"* "$MQL5_PATH/Libraries/NeuralAI/"
}

# MT5 indítása
start_mt5() {
    echo -e "${YELLOW}MetaTrader 5 indítása...${NC}"
    export WINEPREFIX="$MT5_PREFIX"
    export WINEARCH=win64
    wine "$MT5_PATH/terminal64.exe" &
}

# Registry beállítások
setup_registry() {
    echo -e "${YELLOW}Registry beállítások...${NC}"
    cat > /tmp/mt5_reg.reg << EOF
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Wine\Direct3D]
"MaxVersionGL"="32768"
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

# Fő függvény
main() {
    echo -e "${GREEN}MT5 fejlesztői környezet beállítása...${NC}"
    check_wine
    setup_wine_prefix
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
