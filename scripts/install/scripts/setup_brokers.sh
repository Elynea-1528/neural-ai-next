#!/bin/bash
# Neural AI Next - Broker Setup Script
# Supports: MetaTrader 5 (MetaQuotes, XM, Dukascopy) and JForex4

set -e

# Configuration
WINEPREFIX_MT5="${WINEPREFIX_MT5:-$HOME/.mt5}"
JFOREIX_INSTALL_DIR="${JFOREIX_INSTALL_DIR:-$HOME/jforex}"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download URLs
URL_MT5_METAQUOTES="https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe"
URL_MT5_XM="https://xm.com/download/mt5/xm-mt5-setup.exe"
URL_MT5_DUKASCOPY="https://download.mql5.com/cdn/web/dukascopy.bank.sa/mt5/dukascopy5setup.exe"
URL_JFOREX4="https://platform.dukascopy.com/jforex4-installer/JForex4_unix_64_JRE_bundled.sh"
URL_WEBVIEW2="https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/f2910a1e-e5a6-4f17-b52d-7faf525d17f8/MicrosoftEdgeWebview2Setup.exe"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
print_banner() {
    echo "=========================================="
    echo "Neural AI Next - Broker Telepítő"
    echo "=========================================="
    echo ""
}

# Check if Wine is installed
check_wine() {
    if ! command -v wine &> /dev/null; then
        echo -e "${RED}✗ Wine nincs telepítve!${NC}"
        echo "Telepítsd Wine-t először:"
        echo "  Ubuntu/Debian: sudo apt install wine-stable"
        echo "  Fedora: sudo dnf install wine"
        exit 1
    fi
    echo -e "${GREEN}✓ Wine telepítve van${NC}"
}

# Check if Java is installed
check_java() {
    if ! command -v java &> /dev/null; then
        echo -e "${RED}✗ Java nincs telepítve!${NC}"
        echo "A JForex4 Java alapú alkalmazás, telepíteni kell a Java-t:"
        echo "  Ubuntu/Debian: sudo apt install openjdk-11-jdk"
        echo "  Fedora: sudo dnf install java-11-openjdk"
        echo ""
        echo "Alternatívaként használhatod a JRE-t tartalmazó JForex4 telepítőt."
        return 1
    fi
    
    local java_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
    if [ "$java_version" -lt 8 ]; then
        echo -e "${YELLOW}⚠️  Figyelmeztetés: A Java verzió túl régi ($java_version). JForex4-hoz Java 8 vagy újabb szükséges.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Java telepítve van ($(java -version 2>&1 | head -n 1))${NC}"
    return 0
}

# Setup Wine environment
setup_wine() {
    local wineprefix="$1"
    local broker_name="$2"
    
    echo -e "\n${BLUE}=== $broker_name Wine környezet beállítása ===${NC}"
    
    mkdir -p "$wineprefix"
    export WINEPREFIX="$wineprefix"
    
    echo "Wine inicializálása..."
    wineboot 2>/dev/null || true
    sleep 3
    
    echo "Windows verzió beállítása Windows 11-re..."
    WINEPREFIX="$wineprefix" winecfg -v=win11 2>/dev/null || true
    
    echo -e "${GREEN}✓ Wine környezet kész${NC}"
}

# Install WebView2 Runtime
install_webview2() {
    local wineprefix="$1"
    
    echo -e "\n${BLUE}=== WebView2 Runtime telepítése ===${NC}"
    
    if [ ! -f "~/Downloads/webview2.exe" ]; then
        echo "WebView2 Runtime letöltése..."
        cd ~/Downloads
        curl -L "$URL_WEBVIEW2" --output webview2.exe
    fi
    
    echo "WebView2 telepítése..."
    WINEPREFIX="$wineprefix" wine ~/Downloads/webview2.exe /silent /install 2>/dev/null || true
    sleep 3
    
    echo -e "${GREEN}✓ WebView2 Runtime telepítve${NC}"
}

# Install MetaTrader 5
install_mt5() {
    local broker_choice="$1"
    local wineprefix="$2"
    
    case $broker_choice in
        1)
            broker_name="MetaTrader 5 (MetaQuotes Demo)"
            url="$URL_MT5_METAQUOTES"
            setup_file="mt5setup.exe"
            ;;
        2)
            broker_name="XM Forex MT5"
            url="$URL_MT5_XM"
            setup_file="xm-mt5-setup.exe"
            ;;
        3)
            broker_name="Dukascopy MT5"
            url="$URL_MT5_DUKASCOPY"
            setup_file="dukascopy5setup.exe"
            ;;
    esac
    
    echo -e "\n${BLUE}=== $broker_name telepítése ===${NC}"
    
    # Download MT5 setup
    echo "MT5 letöltése..."
    cd ~/Downloads
    curl -L "$url" --output "$setup_file"
    
    # Install MT5
    echo "MT5 telepítése..."
    WINEPREFIX="$wineprefix" wine "$setup_file" 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Figyelmeztetés: Az MT5 telepítő ablakot manuálisan kell bezárni${NC}"
        echo "Kérlek várj 10 másodpercet a telepítés befejezéséhez..."
        sleep 10
    }
    
    # Clean up
    rm -f ~/Downloads/"$setup_file"
    
    echo -e "${GREEN}✓ $broker_name telepítve${NC}"
}

# Install JForex4
install_jforex4() {
    echo -e "\n${BLUE}=== Dukascopy JForex4 telepítése ===${NC}"
    
    # Check Java (opcionális, mert a telepítő tartalmaz JRE-t)
    echo "Java állapot ellenőrzése..."
    if check_java; then
        echo -e "${GREEN}✓ Java telepítve van${NC}"
    else
        echo -e "${YELLOW}⚠️  Java nincs telepítve, de a JForex4 telepítő tartalmaz JRE-t${NC}"
        echo "A telepítés folytatható a bundled JRE-vel."
    fi
    
    # Download JForex4 installer
    echo "JForex4 letöltése..."
    cd ~/Downloads
    if [ -f "JForex4_installer.sh" ]; then
        echo "A telepítő már létezik, újra letöltés kihagyása."
    else
        curl -L "$URL_JFOREX4" --output JForex4_installer.sh
    fi
    
    # Make it executable
    chmod +x JForex4_installer.sh
    
    # Install JForex4
    echo "JForex4 telepítése..."
    echo -e "${YELLOW}⚠️  A JForex4 telepítő grafikus felülettel rendelkezik${NC}"
    echo "Kérlek kövesd a telepítő utasításait..."
    echo "A telepítés alapértelmezett helye: $HOME/jforex vagy /opt/jforex"
    echo ""
    echo "A telepítés automatikusan elindul 5 másodperc múlva..."
    sleep 5
    
    # Run installer natively (not with Wine)
    ./JForex4_installer.sh || {
        echo -e "${YELLOW}⚠️  A JForex4 telepítést manuálisan kell elvégezni${NC}"
        echo "Indítsd el a telepítőt:"
        echo "  cd ~/Downloads"
        echo "  ./JForex4_installer.sh"
        echo ""
        echo "A telepítés után a JForex4 a következő helyen lesz elérhető:"
        echo "  $HOME/jforex vagy /opt/jforex"
    }
    
    echo -e "${GREEN}✓ JForex4 telepítve${NC}"
    echo "A JForex4 natív Linux alkalmazásként lett telepítve."
    echo ""
    echo "Indítási parancsok:"
    echo "  ~/jforex/JForex4  # vagy"
    echo "  /opt/jforex/JForex4"
}

# Setup broker configuration
setup_broker_config() {
    local broker_choice="$1"
    
    echo -e "\n${BLUE}=== Broker konfiguráció beállítása ===${NC}"
    
    case $broker_choice in
        1|2|3)
            # MT5 brokers - konfigurációs fájlok a configs/collectors/mt5/-ben vannak
            local config_dir="configs/collectors/mt5"
            local broker_name=""
            
            case $broker_choice in
                1) broker_name="metaquotes" ;;
                2) broker_name="xm" ;;
                3) broker_name="dukascopy" ;;
            esac
            
            echo "MT5 konfiguráció ellenőrzése: $broker_name"
            
            # Ellenőrizzük, hogy létezik-e a konfigurációs fájl
            if [ ! -f "$config_dir/broker_$broker_name.yaml" ]; then
                echo -e "${YELLOW}⚠️  Konfigurációs fájl nem található: $config_dir/broker_$broker_name.yaml${NC}"
                echo "Kérlek hozd létre manuálisan a konfigurációs fájlt."
            else
                echo -e "${GREEN}✓ Konfigurációs fájl megtalálva: $config_dir/broker_$broker_name.yaml${NC}"
            fi
            ;;
        4)
            # JForex - konfigurációs fájl a configs/collectors/jforex/-ben van
            local config_dir="configs/collectors/jforex"
            
            echo "JForex konfiguráció ellenőrzése"
            
            if [ ! -f "$config_dir/jforex_config.yaml" ]; then
                echo -e "${YELLOW}⚠️  Konfigurációs fájl nem található: $config_dir/jforex_config.yaml${NC}"
                echo "Kérlek hozd létre manuálisan a konfigurációs fájlt."
            else
                echo -e "${GREEN}✓ Konfigurációs fájl megtalálva: $config_dir/jforex_config.yaml${NC}"
            fi
            ;;
    esac
}

# Print usage instructions
print_usage() {
    local broker_choice="$1"
    
    echo -e "\n${GREEN}=========================================="
    echo "✓ Broker telepítés sikeres!"
    echo "==========================================${NC}"
    echo ""
    
    case $broker_choice in
        1|2|3)
            echo "MT5 indítása:"
            echo "  export WINEPREFIX=~/.mt5"
            echo "  wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe"
            echo ""
            echo "Demo fiók létrehozása az MT5-ben"
            echo ""
            echo "MQL5 fordítása:"
            echo "  bash $INSTALL_DIR/compile_mql.sh"
            echo ""
            echo "Konfiguráció: configs/collectors/mt5/"
            ;;
        4)
           echo "JForex4 indítása:"
           echo "  ~/jforex/JForex4  # vagy a telepítés helye szerint"
           echo ""
           echo "Ha a JForex4 más helyre lett telepítve:"
           echo "  /opt/jforex/JForex4  # vagy a telepítő által megadott elérési út"
           echo ""
           echo "Demo fiók létrehozása a JForex4-ben"
           echo ""
           echo "Konfiguráció: configs/collectors/jforex/"
           echo ""
           echo "Megjegyzés: A JForex4 natív Linux alkalmazás, nem Wine-on fut!"
           ;;
        5)
            echo "MT5 indítása:"
            echo "  export WINEPREFIX=~/.mt5"
            echo "  wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe"
            echo ""
            echo "Demo fiók létrehozása az MT5-ben"
            echo ""
            echo "MQL5 fordítása:"
            echo "  bash $INSTALL_DIR/compile_mql.sh"
            echo ""
            echo "Konfigurációk:"
            echo "  MetaQuotes: configs/collectors/mt5/broker_metaquotes.yaml"
            echo "  XM: configs/collectors/mt5/broker_xm.yaml"
            echo "  Dukascopy: configs/collectors/mt5/broker_dukascopy.yaml"
            ;;
    esac
    
    echo ""
    echo "További információ: docs/INSTALLATION_GUIDE.md"
    echo ""
}

# Main function
main() {
    print_banner
    
    # Check Wine
    check_wine
    
    # Broker selection
    echo "Válaszd ki a brókert:"
    echo "1) MetaTrader 5 (MetaQuotes Demo)"
    echo "2) XM Forex MT5"
    echo "3) Dukascopy MT5"
    echo "4) Dukascopy JForex4"
    echo "5) Összes MT5 bróker (MetaQuotes, XM, Dukascopy)"
    echo "6) Összes JForex bróker (JForex4)"
    echo "7) Minden bróker telepítése"
    echo ""
    read -p "Választás (1-7): " BROKER_CHOICE
    
    case $BROKER_CHOICE in
        1|2|3)
            # MT5 installation
            setup_wine "$WINEPREFIX_MT5" "MT5"
            install_webview2 "$WINEPREFIX_MT5"
            install_mt5 "$BROKER_CHOICE" "$WINEPREFIX_MT5"
            setup_broker_config "$BROKER_CHOICE"
            print_usage "$BROKER_CHOICE"
            ;;
        4)
           # JForex4 installation
           install_jforex4
           setup_broker_config "$BROKER_CHOICE"
           print_usage "$BROKER_CHOICE"
           ;;
        5)
            # All MT5 brokers
            echo -e "\n${BLUE}=== Összes MT5 bróker telepítése ===${NC}"
            setup_wine "$WINEPREFIX_MT5" "MT5"
            install_webview2 "$WINEPREFIX_MT5"
            
            for choice in 1 2 3; do
                install_mt5 "$choice" "$WINEPREFIX_MT5"
                setup_broker_config "$choice"
            done
            
            echo -e "\n${GREEN}✓ Összes MT5 bróker telepítve${NC}"
            print_usage "5"
            ;;
        6)
           # All JForex brokers
           echo -e "\n${BLUE}=== Összes JForex bróker telepítése ===${NC}"
           install_jforex4
           setup_broker_config "4"
           
           echo -e "\n${GREEN}✓ Összes JForex bróker telepítve${NC}"
           print_usage "4"
           ;;
        7)
            # All brokers
            echo -e "\n${BLUE}=== Minden bróker telepítése ===${NC}"
            
            # MT5 brokers
            setup_wine "$WINEPREFIX_MT5" "MT5"
            install_webview2 "$WINEPREFIX_MT5"
            
            for choice in 1 2 3; do
                install_mt5 "$choice" "$WINEPREFIX_MT5"
                setup_broker_config "$choice"
            done
            
            # JForex brokers
            install_jforex4
            setup_broker_config "4"
            
            echo -e "\n${GREEN}✓ Minden bróker telepítve${NC}"
            echo -e "\n${GREEN}=========================================="
            echo "✓ Összes bróker telepítés sikeres!"
            echo "==========================================${NC}"
            echo ""
            echo "MT5 indítása:"
            echo "  export WINEPREFIX=~/.mt5"
            echo "  wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe"
            echo ""
            echo "JForex4 indítása:"
            echo "  ~/jforex/JForex4  # vagy a telepítés helye szerint"
            echo ""
            echo "Megjegyzés: A JForex4 natív Linux alkalmazás, nem Wine-on fut!"
            echo ""
            echo "Konfigurációk:"
            echo "  MT5: configs/collectors/mt5/"
            echo "  JForex: configs/collectors/jforex/"
            echo ""
            echo "További információ: docs/INSTALLATION_GUIDE.md"
            echo ""
            ;;
        *)
            echo -e "${RED}Érvénytelen választás!${NC}"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"