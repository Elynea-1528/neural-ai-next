#!/bin/bash
# Copyright 2000-2025, MetaQuotes Ltd.
# Modified for Neural AI Next project

# MetaTrader and WebView2 download urls
URL_MT5="https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe"
URL_WEBVIEW="https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/f2910a1e-e5a6-4f17-b52d-7faf525d17f8/MicrosoftEdgeWebview2Setup.exe"

# Wine version to install: stable or devel
WINE_VERSION="stable"

# Wine prefix for MT5
WINEPREFIX_MT5="$HOME/.mt5"

# Prepare versions
. /etc/os-release

echo "=========================================="
echo "Neural AI Next - Wine + MT5 Telepítő"
echo "=========================================="
echo "OS: $NAME $VERSION_ID"
echo "Wine Prefix: $WINEPREFIX_MT5"
echo ""

# Ask user for broker choice
echo "Válaszd ki a brókert:"
echo "1) MetaTrader 5 (MetaQuotes Demo)"
echo "2) XM Forex MT5"
read -p "Választás (1-2): " BROKER_CHOICE

case $BROKER_CHOICE in
    1)
        BROKER_NAME="MetaTrader 5"
        ;;
    2)
        BROKER_NAME="XM Forex MT5"
        URL_MT5="https://xm.com/download/mt5/xm-mt5-setup.exe"
        ;;
    *)
        echo "Érvénytelen választás, alapértelmezett: MetaTrader 5"
        BROKER_NAME="MetaTrader 5"
        ;;
esac

echo ""
echo "Telepítés: $BROKER_NAME"
echo ""

# Update and install Wine
echo "Rendszer frissítése és Wine telepítése..."
if [ "$NAME" = "Fedora Linux" ]; then
    echo "Rendszer frissítése"
    sudo dnf update
    sudo dnf upgrade -y

    echo "Wine repo választása"
    sudo rm -f /etc/yum.repos.d/winehq*
    if (( $VERSION_ID >= 43 )); then
       sudo dnf5 config-manager addrepo --from-repofile=https://dl.winehq.org/wine-builds/fedora/42/winehq.repo
    elif (( $VERSION_ID >= 42 )); then
       sudo dnf5 config-manager addrepo --from-repofile=https://dl.winehq.org/wine-builds/fedora/42/winehq.repo
    else
       sudo dnf5 config-manager addrepo --from-repofile=https://dl.winehq.org/wine-builds/fedora/41/winehq.repo
    fi

    echo "Wine és Wine Mono telepítése"
    sudo dnf update
    sudo dnf install winehq-$WINE_VERSION -y
    sudo dnf install wine-mono -y
else
    echo "Rendszer frissítése"
    sudo apt update
    sudo apt upgrade -y

    echo "Teljes verzió lekérése"
    sudo apt install bc wget curl -y
    VERSION_FULL=$(echo "$VERSION_ID * 100" | bc -l | cut -d "." -f1)

    echo "Wine repo választása"
    sudo rm -f /etc/apt/sources.list.d/winehq*

    sudo dpkg --add-architecture i386
    sudo mkdir -pm755 /etc/apt/keyrings
    sudo wget -O - https://dl.winehq.org/wine-builds/winehq.key | sudo gpg --dearmor -o /etc/apt/keyrings/winehq-archive.key -

    if [ "$NAME" = "Ubuntu" ]; then
        echo "Ubuntu észlelve: $NAME $VERSION_ID"
        # Choose repository based on Ubuntu version
        if (( $VERSION_FULL >= 2410 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/plucky/winehq-plucky.sources
        elif (( $VERSION_FULL < 2410 )) && (( $VERSION_FULL >= 2400 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources
        elif (( $VERSION_FULL < 2400 )) && (( $VERSION_FULL >= 2300 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/lunar/winehq-lunar.sources
        elif (( $VERSION_FULL < 2300 )) && (( $VERSION_FULL >= 2210 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/kinetic/winehq-kinetic.sources
        elif (( $VERSION_FULL < 2210 )) && (( $VERSION_FULL >= 2100 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
        elif (( $VERSION_FULL < 2100 )) && (($VERSION_FULL >= 2000 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/focal/winehq-focal.sources
        else
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/bionic/winehq-bionic.sources
        fi
    elif [ "$NAME" = "Linux Mint" ]; then
        echo "Linux Mint észlelve: $NAME $VERSION_ID"
        # Choose repository based on Linux Mint version
        if (( $VERSION_FULL >= 2200 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources
        else
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/focal/winehq-focal.sources
        fi
    elif [ "$NAME" = "Debian GNU/Linux" ]; then
        echo "Debian Linux észlelve: $NAME $VERSION_ID"
        # Choose repository based on Debian version
        if (( $VERSION_FULL >= 13 )); then
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/trixie/winehq-trixie.sources
        else
           sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources
        fi
    else
        echo "$NAME $VERSION_ID nem támogatott"
        exit 1
    fi

    echo "Wine és Wine Mono telepítése"
    sudo apt update
    sudo apt install --install-recommends winehq-$WINE_VERSION -y
fi

echo ""
echo "✓ Wine telepítve"
echo ""

# Create MT5 Wine prefix
echo "MT5 Wine prefix létrehozása: $WINEPREFIX_MT5"
mkdir -p "$WINEPREFIX_MT5"
export WINEPREFIX="$WINEPREFIX_MT5"

# Initialize Wine
echo "Wine inicializálása..."
wineboot
sleep 5

# Set Windows version to 11
echo "Windows verzió beállítása Windows 11-re"
WINEPREFIX="$WINEPREFIX_MT5" winecfg -v=win11

# Download MetaTrader and WebView2 Runtime
echo ""
echo "MetaTrader 5 és WebView2 Runtime letöltése..."
cd ~/Downloads
curl -L "$URL_MT5" --output mt5setup.exe
curl -L "$URL_WEBVIEW" --output webview2.exe

# Install WebView2 Runtime
echo ""
echo "WebView2 Runtime telepítése..."
WINEPREFIX="$WINEPREFIX_MT5" wine webview2.exe /silent /install
sleep 5

# Install MetaTrader 5
echo ""
echo "$BROKER_NAME telepítése..."
WINEPREFIX="$WINEPREFIX_MT5" wine mt5setup.exe

# Clean up
echo ""
echo "Letöltött fájlok törlése..."
rm -f ~/Downloads/mt5setup.exe ~/Downloads/webview2.exe

echo ""
echo "=========================================="
echo "✓ Telepítés sikeres!"
echo "=========================================="
echo ""
echo "Következő lépések:"
echo ""
echo "1. MT5 indítása:"
echo "   export WINEPREFIX=~/.mt5"
echo "   wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe"
echo ""
echo "2. Demo fiók létrehozása az MT5-ben"
echo ""
echo "3. Kommunikációs könyvtár lásd: docs/WINE_MT5_SETUP.md"
echo ""
echo "4. További információ: docs/WINE_MT5_SETUP.md"
echo ""
echo "Kérlek indítsd újra a rendszert!"
echo ""
