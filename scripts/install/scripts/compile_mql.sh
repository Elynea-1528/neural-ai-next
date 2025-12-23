#!/bin/bash
# MQL5 Fordító Script Linuxhoz Wine alatt
# Alternatíva a VS Code bővítményeknek - Közvetlen MetaEditor fordítás

set -e

# Konfiguráció
WINEPREFIX="${WINEPREFIX:-$HOME/.mt5}"
MQL_DIR="$WINEPREFIX/drive_c/Program Files/MetaTrader 5"
METAEDITOR="$MQL_DIR/MetaEditor64.exe"  # MT5 uses MetaEditor64.exe, not metaeditor.exe
SOURCE_DIR="${1:-$(pwd)}"
OUTPUT_DIR="$MQL_DIR/MQL5"
COMPILED_DIR="neural_ai/experts/mt5/compiled"

# Színek a kimenethez
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "MQL5 Fordító Script Linuxhoz"
echo "=========================================="

# Wine telepítésének ellenőrzése
if ! command -v wine &> /dev/null; then
    echo -e "${RED}✗ Wine is not installed!${NC}"
    echo "Install Wine: sudo apt install wine-stable"
    exit 1
fi
echo -e "${GREEN}✓ Wine found${NC}"

# Wine prefix létezésének ellenőrzése
if [ ! -d "$WINEPREFIX" ]; then
    echo -e "${RED}✗ Wine prefix not found: $WINEPREFIX${NC}"
    echo "Run the Wine + MT5 setup first!"
    exit 1
fi
echo -e "${GREEN}✓ Wine prefix found: $WINEPREFIX${NC}"

# MetaEditor létezésének ellenőrzése
if [ ! -f "$METAEDITOR" ]; then
    echo -e "${RED}✗ MetaEditor not found: $METAEDITOR${NC}"
    echo "Install MetaTrader 5 first!"
    exit 1
fi
echo -e "${GREEN}✓ MetaEditor found${NC}"

# Wine prefix exportálása
export WINEPREFIX

# Egyetlen fájl fordítására szolgáló függvény
compile_file() {
    local source_file="$1"
    local filename=$(basename "$source_file")
    local extension="${filename##*.}"

    echo -e "\n${YELLOW}Compiling: $source_file${NC}"

    # Kimeneti alkönyvtár meghatározása a fájltípus alapján
    case $extension in
        mq5)
            case $filename in
                *EA*|*Expert*)
                    OUTPUT_SUBDIR="Experts"
                    ;;
                *Indicator*)
                    OUTPUT_SUBDIR="Indicators"
                    ;;
                *Script*)
                    OUTPUT_SUBDIR="Scripts"
                    ;;
                *)
                    OUTPUT_SUBDIR="Experts"
                    ;;
            esac
            ;;
        mqh)
            echo "  → Header file, skipping compilation"
            return 0
            ;;
        *)
            echo -e "${RED}  → Unknown file type: $extension${NC}"
            return 1
            ;;
    esac

    # Fordítás MetaEditor használatával Wine-en keresztül
    wine "$METAEDITOR" /compile:"$source_file" /log > /tmp/mql_compile.log 2>&1
    local compile_result=$?

    # Fordítás sikerességének ellenőrzése a .ex5 fájl keresésével
    # MT5 sometimes creates the .ex5 in the same directory as the source file
    local source_dir=$(dirname "$source_file")
    local basename_no_ext="${filename%.*}"
    local output_file="$OUTPUT_DIR/$OUTPUT_SUBDIR/$basename_no_ext.ex5"
    local source_dir_ex5="$source_dir/$basename_no_ext.ex5"
    local compiled_dir_ex5="$COMPILED_DIR/$basename_no_ext.ex5"

    # Több lehetséges hely ellenőrzése
    if [ -f "$source_dir_ex5" ]; then
        echo -e "${GREEN}  ✓ Compilation successful${NC}"
        echo -e "${GREEN}  ✓ Output file created: $source_dir_ex5${NC}"

        # Move compiled file to compiled directory
        mkdir -p "$COMPILED_DIR"
        mv "$source_dir_ex5" "$compiled_dir_ex5"
        echo -e "${GREEN}  ✓ Moved to: $compiled_dir_ex5${NC}"

        return 0
    elif [ -f "$output_file" ]; then
        echo -e "${GREEN}  ✓ Compilation successful${NC}"
        echo -e "${GREEN}  ✓ Output file created: $output_file${NC}"

        # Copy compiled file to compiled directory
        mkdir -p "$COMPILED_DIR"
        cp "$output_file" "$compiled_dir_ex5"
        echo -e "${GREEN}  ✓ Copied to: $compiled_dir_ex5${NC}"

        return 0
    else
        echo -e "${RED}  ✗ Compilation FAILED - No .ex5 file created!${NC}"
        echo "  Wine exit code: $compile_result"
        echo "  Searched locations:"
        echo "    $source_dir_ex5"
        echo "    $output_file"
        echo "  Check log: /tmp/mql_compile.log"
        cat /tmp/mql_compile.log
        return 1
    fi
}

# EA forrás és .ex5 másolása az MT5 mappába
copy_to_mt5() {
    local source_file="$1"
    local filename=$(basename "$source_file")
    local basename_no_ext="${filename%.*}"
    local source_dir=$(dirname "$source_file")
    local mt5_ea_dir="$MQL_DIR/MQL5/Experts"
    local output_file="$OUTPUT_DIR/Experts/$basename_no_ext.ex5"
    local source_dir_ex5="$source_dir/$basename_no_ext.ex5"
    local compiled_dir_ex5="$COMPILED_DIR/$basename_no_ext.ex5"

    echo -e "${YELLOW}Copying EA to MT5 folder...${NC}"

    # Experts könyvtár létrehozása, ha nem létezik
    mkdir -p "$mt5_ea_dir"

    # Forrásfájl (.mq5) másolása
    if cp "$source_file" "$mt5_ea_dir/$filename"; then
        echo -e "${GREEN}✓ Source copied to: $mt5_ea_dir/$filename${NC}"
    else
        echo -e "${RED}✗ Failed to copy source${NC}"
        return 1
    fi

    # .ex5 fájl keresése és másolása (először a fordított, majd a forrás, végül a kimeneti könyvtár ellenőrzése)
    local ex5_found=false
    local ex5_source=""

    if [ -f "$compiled_dir_ex5" ]; then
        ex5_source="$compiled_dir_ex5"
        ex5_found=true
    elif [ -f "$source_dir_ex5" ]; then
        ex5_source="$source_dir_ex5"
        ex5_found=true
    elif [ -f "$output_file" ]; then
        ex5_source="$output_file"
        ex5_found=true
    fi

    if [ "$ex5_found" = true ]; then
        # Mindig másolás (felülírás, ha létezik)
        if cp -f "$ex5_source" "$mt5_ea_dir/$basename_no_ext.ex5"; then
            echo -e "${GREEN}✓ .ex5 copied to: $mt5_ea_dir/$basename_no_ext.ex5${NC}"
            return 0
        else
            echo -e "${RED}✗ Failed to copy .ex5${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ ERROR: .ex5 file not found for copying!${NC}"
        echo "  Searched locations:"
        echo "    $compiled_dir_ex5"
        echo "    $source_dir_ex5"
        echo "    $output_file"
        return 1
    fi
}

# Fő fordítási logika
if [ $# -eq 0 ]; then
    # Nincs argumentum: az összes .mq5 fájl fordítása az aktuális könyvtárban
    echo "Az összes .mq5 fájl fordítása az aktuális könyvtárban..."
    for file in "$SOURCE_DIR"/*.mq5; do
        [ -e "$file" ] || continue
        compile_file "$file" && copy_to_mt5 "$file"
    done
else
    # Megadott fájl
    if [ -f "$1" ]; then
        if compile_file "$1"; then
            copy_to_mt5 "$1"
        fi
    else
        echo -e "${RED}✗ File not found: $1${NC}"
        exit 1
    fi
fi

# Fordítás sikerességének ellenőrzése
if [ $? -eq 0 ]; then
    echo -e "\n=========================================="
    echo -e "${GREEN}✓ Fordítás és másolás sikeres${NC}"
    echo "=========================================="
    echo ""
    echo "Az EA készen áll itt:"
    echo "  Projekt: $COMPILED_DIR/"
    echo "  MT5: $MQL_DIR/MQL5/Experts/"
    echo ""
    echo "Használat MT5-ben:"
    echo "  1. Nyisd meg az MT5-öt"
    echo "  2. Navigator → Expert Advisors"
    echo "  3. keresd meg az EA-t és húzd a chartra"
else
    echo -e "\n=========================================="
    echo -e "${RED}✗ Fordítás SIKERTELEN${NC}"
    echo "=========================================="
    echo ""
    echo "Ellenőrizd a fenti hibákat és próbáld újra."
    exit 1
fi
