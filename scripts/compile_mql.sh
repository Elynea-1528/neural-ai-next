#!/bin/bash
# MQL5 Compilation Script for Linux with Wine
# Alternative to VS Code extensions - Direct MetaEditor compilation

set -e

# Configuration
WINEPREFIX="${WINEPREFIX:-$HOME/.mt5}"
MQL_DIR="$WINEPREFIX/drive_c/Program Files/MetaTrader 5"
METAEDITOR="$MQL_DIR/MetaEditor64.exe"  # MT5 uses MetaEditor64.exe, not metaeditor.exe
SOURCE_DIR="${1:-$(pwd)}"
OUTPUT_DIR="$MQL_DIR/MQL5"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "MQL5 Compilation Script for Linux"
echo "=========================================="

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo -e "${RED}✗ Wine is not installed!${NC}"
    echo "Install Wine: sudo apt install wine-stable"
    exit 1
fi
echo -e "${GREEN}✓ Wine found${NC}"

# Check if Wine prefix exists
if [ ! -d "$WINEPREFIX" ]; then
    echo -e "${RED}✗ Wine prefix not found: $WINEPREFIX${NC}"
    echo "Run the Wine + MT5 setup first!"
    exit 1
fi
echo -e "${GREEN}✓ Wine prefix found: $WINEPREFIX${NC}"

# Check if MetaEditor exists
if [ ! -f "$METAEDITOR" ]; then
    echo -e "${RED}✗ MetaEditor not found: $METAEDITOR${NC}"
    echo "Install MetaTrader 5 first!"
    exit 1
fi
echo -e "${GREEN}✓ MetaEditor found${NC}"

# Export Wine prefix
export WINEPREFIX

# Function to compile a single file
compile_file() {
    local source_file="$1"
    local filename=$(basename "$source_file")
    local extension="${filename##*.}"
    
    echo -e "\n${YELLOW}Compiling: $source_file${NC}"
    
    # Determine output subdirectory based on file type
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
    
    # Compile using MetaEditor through Wine
    wine "$METAEDITOR" /compile:"$source_file" /log > /tmp/mql_compile.log 2>&1
    local compile_result=$?
    
    # Check if compilation was successful by looking for the .ex5 file
    # MT5 sometimes creates the .ex5 in the same directory as the source file
    local source_dir=$(dirname "$source_file")
    local basename_no_ext="${filename%.*}"
    local output_file="$OUTPUT_DIR/$OUTPUT_SUBDIR/$basename_no_ext.ex5"
    local source_dir_ex5="$source_dir/$basename_no_ext.ex5"
    
    # Check multiple possible locations
    if [ -f "$source_dir_ex5" ]; then
        echo -e "${GREEN}  ✓ Compilation successful${NC}"
        echo -e "${GREEN}  ✓ Output file created: $source_dir_ex5${NC}"
        return 0
    elif [ -f "$output_file" ]; then
        echo -e "${GREEN}  ✓ Compilation successful${NC}"
        echo -e "${GREEN}  ✓ Output file created: $output_file${NC}"
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

# Function to copy EA source and .ex5 to MT5 folder
copy_to_mt5() {
    local source_file="$1"
    local filename=$(basename "$source_file")
    local basename_no_ext="${filename%.*}"
    local source_dir=$(dirname "$source_file")
    local mt5_ea_dir="$MQL_DIR/MQL5/Experts"
    local output_file="$OUTPUT_DIR/Experts/$basename_no_ext.ex5"
    local source_dir_ex5="$source_dir/$basename_no_ext.ex5"
    
    echo -e "${YELLOW}Copying EA to MT5 folder...${NC}"
    
    # Create Experts directory if it doesn't exist
    mkdir -p "$mt5_ea_dir"
    
    # Copy source file (.mq5)
    if cp "$source_file" "$mt5_ea_dir/$filename"; then
        echo -e "${GREEN}✓ Source copied to: $mt5_ea_dir/$filename${NC}"
    else
        echo -e "${RED}✗ Failed to copy source${NC}"
        return 1
    fi
    
    # Find and copy .ex5 file (check source directory first, then output directory)
    local ex5_found=false
    local ex5_source=""
    
    if [ -f "$source_dir_ex5" ]; then
        ex5_source="$source_dir_ex5"
        ex5_found=true
    elif [ -f "$output_file" ]; then
        ex5_source="$output_file"
        ex5_found=true
    fi
    
    if [ "$ex5_found" = true ]; then
        if cp "$ex5_source" "$mt5_ea_dir/$basename_no_ext.ex5"; then
            echo -e "${GREEN}✓ .ex5 copied to: $mt5_ea_dir/$basename_no_ext.ex5${NC}"
            return 0
        else
            echo -e "${RED}✗ Failed to copy .ex5${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ ERROR: .ex5 file not found for copying!${NC}"
        echo "  Searched locations:"
        echo "    $source_dir_ex5"
        echo "    $output_file"
        return 1
    fi
}

# Main compilation logic
if [ $# -eq 0 ]; then
    # No arguments: compile all .mq5 files in current directory
    echo "Compiling all .mq5 files in current directory..."
    for file in "$SOURCE_DIR"/*.mq5; do
        [ -e "$file" ] || continue
        compile_file "$file" && copy_to_mt5 "$file"
    done
else
    # Specific file provided
    if [ -f "$1" ]; then
        if compile_file "$1"; then
            copy_to_mt5 "$1"
        fi
    else
        echo -e "${RED}✗ File not found: $1${NC}"
        exit 1
    fi
fi

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo -e "\n=========================================="
    echo -e "${GREEN}✓ Compilation and copy successful${NC}"
    echo "=========================================="
    echo ""
    echo "Your EA is ready in MT5 at:"
    echo "  $MQL_DIR/MQL5/Experts/"
    echo ""
    echo "To use in MT5:"
    echo "  1. Open MT5"
    echo "  2. Navigator → Expert Advisors"
    echo "  3. Find your EA and drag to chart"
else
    echo -e "\n=========================================="
    echo -e "${RED}✗ Compilation FAILED${NC}"
    echo "=========================================="
    echo ""
    echo "Check the errors above and try again."
    exit 1
fi