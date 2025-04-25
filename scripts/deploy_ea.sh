#!/bin/bash
# MT5 Expert Advisor telepítő script

# Színek
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Konstansok
MT5_PREFIX="$HOME/.wine"  # Használjuk az eredeti wine prefix-et
MT5_PATH="$MT5_PREFIX/drive_c/Program Files/XM MT5"
MQL5_PATH="$MT5_PATH/MQL5"
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
EA_NAME="NeuralAICollector"

# EA fájlok helye a projektben
EA_SOURCE="$PROJECT_ROOT/experts/mt5_collector_ea.mq5"
INCLUDE_SOURCE="$PROJECT_ROOT/experts/include"
LIBRARIES_SOURCE="$PROJECT_ROOT/experts/libraries"

# Célkönyvtárak az MT5-ben
EA_TARGET="$MQL5_PATH/Experts/NeuralAI"
INCLUDE_TARGET="$MQL5_PATH/Include/NeuralAI"
LIBRARIES_TARGET="$MQL5_PATH/Libraries/NeuralAI"

# Függvények
create_directories() {
    echo -e "${YELLOW}Könyvtárak létrehozása...${NC}"
    mkdir -p "$EA_TARGET"
    mkdir -p "$INCLUDE_TARGET"
    mkdir -p "$LIBRARIES_TARGET"
    mkdir -p "$MQL5_PATH/Files/NeuralAI"
    mkdir -p "$MQL5_PATH/Logs/NeuralAI"
}

copy_files() {
    echo -e "${YELLOW}Fájlok másolása...${NC}"

    # EA másolása
    cp "$EA_SOURCE" "$EA_TARGET/"

    # Include fájlok másolása
    if [ -d "$INCLUDE_SOURCE" ]; then
        cp -r "$INCLUDE_SOURCE/"* "$INCLUDE_TARGET/"
    fi

    # Library fájlok másolása
    if [ -d "$LIBRARIES_SOURCE" ]; then
        cp -r "$LIBRARIES_SOURCE/"* "$LIBRARIES_TARGET/"
    fi
}

setup_file_watcher() {
    echo -e "${YELLOW}Fájl figyelő beállítása...${NC}"

    while inotifywait -e modify -r "$PROJECT_ROOT/experts/"; do
        echo -e "${GREEN}Változás észlelve, fájlok frissítése...${NC}"
        copy_files
    done
}

# Ellenőrzések
if [ ! -d "$MT5_PATH" ]; then
    echo -e "${RED}MT5 nem található: $MT5_PATH${NC}"
    exit 1
fi

if [ ! -f "$EA_SOURCE" ]; then
    echo -e "${RED}EA forrásfájl nem található: $EA_SOURCE${NC}"
    exit 1
fi

# Fő folyamat
echo -e "${GREEN}EA telepítése...${NC}"

create_directories
copy_files

echo -e "${GREEN}Telepítés kész!${NC}"
echo -e "${YELLOW}Fájlok figyelése...${NC}"

# Fájl figyelő indítása
setup_file_watcher
