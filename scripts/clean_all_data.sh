#!/bin/bash

echo "🧹 Összes adat törlése..."

# Kollektor adatok törlése
rm -rf data/collectors/mt5/*

# Warehouse adatok törlése
rm -rf data/warehouse/historical/*

# Logok törlése
rm -rf data/logs/*

# Adatbázis törlése
rm -f data/collectors/mt5/historical_jobs.db

echo "✅ Összes adat törölve!"
echo ""
echo "Új mappa struktúra létrehozása..."

# Mappa struktúra újra létrehozása
mkdir -p data/warehouse/historical
mkdir -p data/logs

# Szimbólumok és időkeretek
SYMBOLS=("EURUSD" "GBPUSD" "USDJPY" "XAUUSD")
TIMEFRAMES=("M1" "M5" "M15" "H1" "H4" "D1")

for symbol in "${SYMBOLS[@]}"; do
    for timeframe in "${TIMEFRAMES[@]}"; do
        mkdir -p "data/warehouse/historical/$symbol/$timeframe"
    done
done

echo "✅ Mappa struktúra létrehozva!"