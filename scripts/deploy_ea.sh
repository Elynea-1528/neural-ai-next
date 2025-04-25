#!/bin/bash
# MT5 Expert Advisor telepítő script

# Színek
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Konstansok
WINE_PREFIX="$HOME/.wine"
MT5_PATHS=(
    "$WINE_PREFIX/drive_c/Program Files/MetaTrader 5"  # Standard MT5
    "$WINE_PREFIX/drive_c/Program Files/XM MT5"        # XM MT5
)
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
EA_NAME="NeuralAICollector"

# EA fájlok helye a projektben
EA_SOURCE="$PROJECT_ROOT/experts/mt5_collector_ea.mq5"
INCLUDE_SOURCE="$PROJECT_ROOT/experts/include"
LIBRARIES_SOURCE="$PROJECT_ROOT/experts/libraries"

# Függvények
deploy_to_mt5() {
    local mt5_path="$1"
    local platform_name="$2"

    echo -e "${YELLOW}Telepítés: $platform_name${NC}"

    if [ ! -d "$mt5_path" ]; then
        echo -e "${RED}$platform_name nem található: $mt5_path${NC}"
        return
    }

    # MQL5 könyvtár
    local mql5_path="$mt5_path/MQL5"

    # Célkönyvtárak
    local ea_target="$mql5_path/Experts/NeuralAI"
    local include_target="$mql5_path/Include/NeuralAI"
    local libraries_target="$mql5_path/Libraries/NeuralAI"

    # Könyvtárak létrehozása
    mkdir -p "$ea_target"
    mkdir -p "$include_target"
    mkdir -p "$libraries_target"
    mkdir -p "$mql5_path/Files/NeuralAI"
    mkdir -p "$mql5_path/Logs/NeuralAI"

    # Fájlok másolása
    echo -e "${YELLOW}Fájlok másolása...${NC}"

    # EA másolása
    cp "$EA_SOURCE" "$ea_target/"

    # Include fájlok másolása
    if [ -d "$INCLUDE_SOURCE" ]; then
        cp -r "$INCLUDE_SOURCE/"* "$include_target/"
    fi

    # Library fájlok másolása
    if [ -d "$LIBRARIES_SOURCE" ]; then
        cp -r "$LIBRARIES_SOURCE/"* "$libraries_target/"
    fi

    echo -e "${GREEN}Telepítés kész: $platform_name${NC}"
}

# Ellenőrzések
if [ ! -f "$EA_SOURCE" ]; then
    echo -e "${RED}EA forrásfájl nem található: $EA_SOURCE${NC}"
    exit 1
fi

# Fő folyamat
echo -e "${GREEN}EA telepítése mindkét platformra...${NC}"

# Standard MT5
deploy_to_mt5 "${MT5_PATHS[0]}" "MetaTrader 5 (Demo)"

# XM MT5
deploy_to_mt5 "${MT5_PATHS[1]}" "XM MT5 (Live)"

echo -e "${GREEN}Telepítés befejeződött!${NC}"
echo -e "${YELLOW}Fájlok figyelése...${NC}"

# File watch és automatikus másolás
while inotifywait -e modify -r "$PROJECT_ROOT/experts/"; do
    echo -e "${GREEN}Változás észlelve, fájlok frissítése...${NC}"
    deploy_to_mt5 "${MT5_PATHS[0]}" "MetaTrader 5 (Demo)"
    deploy_to_mt5 "${MT5_PATHS[1]}" "XM MT5 (Live)"
done
