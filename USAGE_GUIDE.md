# 🚀 Tick -> OHLCV Resampling Demo - Gyors Használati Útmutató

## 📋 Áttekintés

Sikeresen létrehoztam a **Tick -> OHLCV Resampling Demo** szkriptet, amely demonstrálja a Tick adatok OHLCV formátumba való konvertálását.

## 📁 Létrehozott fájlok

1. **[`scripts/test_resampling.py`](scripts/test_resampling.py)** - A fő demo szkript
2. **[`docs/components/scripts/test_resampling.md`](docs/components/scripts/test_resampling.md)** - Teljes dokumentáció

## 🎯 Mit csinál a szkript?

1. **Bootstrap**: Inicializálja a rendszert (Hardware + Storage)
2. **Discovery**: Felfedezi az elérhető dátumokat az EURUSD-hoz
3. **Load**: Betölti az első elérhető nap tick adatait
4. **Resample M1**: 1 perces OHLCV gyertyákat generál
5. **Resample H1**: 1 órás OHLCV gyertyákat generál
6. **Display**: Színesen megjeleníti az első 5-5 sort
7. **Export**: Elmenti CSV fájlokba (`output/` könyvtárba)

## ⚡ Gyors futtatás

```bash
# 1. Aktiváld a környezetet
conda activate neural-ai-next

# 2. Futtasd a szkriptet
python scripts/test_resampling.py
```

## 🎨 A "Varázslat" Magja

A szkript a **Polars `group_by_dynamic`** funkcióját használja:

```python
ohlcv = df.group_by_dynamic("timestamp", every="1m").agg([
    pl.col("bid").first().alias("open"),
    pl.col("bid").max().alias("high"),
    pl.col("bid").min().alias("low"),
    pl.col("bid").last().alias("close"),
    pl.col("bid").count().alias("ticks")
])
```

## 📊 Várható kimenet

```
================================================================================
🚀 TICK -> OHLCV RESAMPLING DEMO
================================================================================

✅ Rendszer inicializálva
   - Hardware: HardwareInfo
   - Storage: ParquetStorageService
   - Backend: PolarsBackend

🔍 1. FÁZIS: DÁTUMOK FELFEDEZÉSE
✅ Elérhető dátumok megtalálva: 2 nap
   1. 2023-01-01 (Sunday)
   2. 2023-01-13 (Friday)

📂 2. FÁZIS: TICK ADATOK BETÖLTÉSE
✅ Tick adatok sikeresen betöltve
   - Sorok száma: 86,400
   - Időtartomány: 2023-01-01 00:00:00 - 2023-01-01 23:59:59

🔄 3. FÁZIS: OHLCV KONVERZIÓ
✅ M1 OHLCV kész: 1,440 sor
✅ H1 OHLCV kész: 24 sor

📊 4. FÁZIS: EREDMÉNYEK MEGJELENÍTÉSE
🟢🟢🔴🟡🟢  (színes árak)

💾 5. FÁZIS: EXPORTÁLÁS
✅ M1 exportálás kész: output/test_candles_m1.csv
✅ H1 exportálás kész: output/test_candles_h1.csv

✅ DEMO SIKERESEN BEFEJEZVE!
```

## 📂 Kimeneti fájlok

A szkript létrehozza az `output/` könyvtárat (ha még nem létezik), és elmenti:

- **`output/test_candles_m1.csv`** - 1 perces OHLCV gyertyák
- **`output/test_candles_h1.csv`** - 1 órás OHLCV gyertyák

## 🎯 Színek jelentése

- 🟢 **Zöld**: Close > Open (ár nőtt)
- 🔴 **Piros**: Close < Open (ár csökkent)
- 🟡 **Sárga**: Close = Open (ár változatlan)

## 🔧 Testreszabás

### Más időkeret használata

Szerkeszd a szkriptet és add hozzá:

```python
# 5 perces
ohlcv_m5 = self._resample_to_ohlcv(pl_data, "5m")

# 15 perces
ohlcv_m15 = self._resample_to_ohlcv(pl_data, "15m")
```

### Több sor megjelenítése

```python
self._display_ohlcv_data(ohlcv_m1, "M1 (1 perces)", 10)  # 10 sor
```

## 📚 További információ

Teljes dokumentáció: **[`docs/components/scripts/test_resampling.md`](docs/components/scripts/test_resampling.md)**

## ✅ Commit információk

```
commit 3276b9e
feat(scripts): add Tick->OHLCV resampling demo script

- Create comprehensive resampling demo script
- Implements M1 and H1 OHLCV conversion
- Features: Bootstrap, Discovery, Load, Resample, Display, Export
- Color-coded console output
- CSV export functionality
- Comprehensive documentation
```

## 🎉 Készen állsz!

Most már futtathatod a szkriptet, hogy lásd a Tick -> OHLCV konverzió működését a saját adataidon!

```bash
python scripts/test_resampling.py