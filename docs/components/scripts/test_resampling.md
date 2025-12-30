# Tick -> OHLCV Resampling Demo Script

## Áttekintés

Ez a szkript demonstrálja a Tick adatok OHLCV (Open, High, Low, Close, Volume) formátumba való konvertálását 1 perces (M1) és 1 órás (H1) időkeretekben a Neural AI Next rendszerben.

## Fájl információ

- **Fájl:** [`scripts/test_resampling.py`](scripts/test_resampling.py)
- **Verzió:** 1.0.0
- **Szerző:** Neural AI Next Team

## Funkciók

A szkript a következő fő funkciókat tartalmazza:

### 1. Bootstrap: Rendszer inicializálása
- Hardware detekció (AVX2 támogatás ellenőrzése)
- Storage factory létrehozása Parquet tárolóval
- Backend automatikus kiválasztása (Polars vagy Pandas)

### 2. Discovery: Elérhető dátumok lekérdezése
- Automatikus dátum felfedezés az EURUSD szimbólumhoz
- Dátumok listázása és az első elérhető nap kiválasztása

### 3. Load: Tick adatok betöltése
- Tick adatok betöltése a kiválasztott dátumról
- Adatok konvertálása Polars DataFrame-re

### 4. Resample M1: 1 perces OHLCV generálás
- Tick adatok aggregálása 1 perces időkeretekbe
- OHLCV értékek számítása:
  - **Open:** Az első bid ár az időkeretben
  - **High:** A legmagasabb bid ár az időkeretben
  - **Low:** A legalacsonyabb bid ár az időkeretben
  - **Close:** Az utolsó bid ár az időkeretben
  - **Volume:** Tick-ek száma az időkeretben

### 5. Resample H1: 1 órás OHLCV generálás
- Ugyanaz a folyamat 1 órás időkeretekkel

### 6. Display: Eredmények színes megjelenítése
- Az első 5-5 sor megjelenítése mindkét időkeretből
- Színes kimenet az ár változás alapján:
  - 🟢 Zöld: Növekedés (Close > Open)
  - 🔴 Piros: Csökkenés (Close < Open)
  - 🟡 Sárga: Változatlan (Close = Open)

### 7. Export: CSV fájlba mentés
- M1 OHLCV adatok mentése: `output/test_candles_m1.csv`
- H1 OHLCV adatok mentése: `output/test_candles_h1.csv`

## A "Varázslat" Magja

A resampling művelet a Polars `group_by_dynamic` funkcióját használja, ami lehetővé teszi az időalapú ablakokban történő hatékony aggregációt:

```python
ohlcv = df.group_by_dynamic("timestamp", every=timeframe).agg([
    pl.col("bid").first().alias("open"),
    pl.col("bid").max().alias("high"),
    pl.col("bid").min().alias("low"),
    pl.col("bid").last().alias("close"),
    pl.col("bid").count().alias("ticks")
])
```

## Függőségek

- **Python:** 3.12+
- **Polars:** 2.5.1+
- **Colorama:** Színes konzol kimenethez
- **Neural AI Next Core:**
  - `neural_ai.core.storage.factory.StorageFactory`
  - `neural_ai.core.utils.factory.HardwareFactory`

## Futtatás

### Előfeltételek

1. **Adatok ellenőrzése:**
   ```bash
   ls -R data/tick/EURUSD/
   ```
   
   Ha nincsenek adatok, először töltsön le adatokat:
   ```bash
   python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-01-01
   ```

2. **Környezet aktiválása:**
   ```bash
   conda activate neural-ai-next
   ```

### Futtatás

```bash
python scripts/test_resampling.py
```

## Kimeneti példa

```
================================================================================
🚀 TICK -> OHLCV RESAMPLING DEMO
================================================================================

✅ Rendszer inicializálva
   - Hardware: HardwareInfo
   - Storage: ParquetStorageService
   - Backend: PolarsBackend

────────────────────────────────────────────────────────────────────────────────
🔍 1. FÁZIS: DÁTUMOK FELFEDEZÉSE
────────────────────────────────────────────────────────────────────────────────

✅ Elérhető dátumok megtalálva: 2 nap

   1. 2023-01-01 (Sunday)
   2. 2023-01-13 (Friday)

📅 Kiválasztott dátum: 2023-01-01

────────────────────────────────────────────────────────────────────────────────
📂 2. FÁZIS: TICK ADATOK BETÖLTÉSE
────────────────────────────────────────────────────────────────────────────────

⏳ Betöltés folyamatban...
   - Szimbólum: EURUSD
   - Dátumtartomány: 2023-01-01 - 2023-01-02

✅ Tick adatok sikeresen betöltve
   - Sorok száma: 86,400
   - Időtartomány: 2023-01-01 00:00:00.123 - 2023-01-01 23:59:59.987

────────────────────────────────────────────────────────────────────────────────
🔄 3. FÁZIS: OHLCV KONVERZIÓ (RESAMPLING)
────────────────────────────────────────────────────────────────────────────────

🕐 3.1 M1 (1 perces) OHLCV generálása...
✅ M1 OHLCV kész: 1,440 sor

🕐 3.2 H1 (1 órás) OHLCV generálása...
✅ H1 OHLCV kész: 24 sor

────────────────────────────────────────────────────────────────────────────────
📊 4. FÁZIS: EREDMÉNYEK MEGJELENÍTÉSE
────────────────────────────────────────────────────────────────────────────────

📊 M1 (1 perces) OHLCV adatok (első 5 sor):
────────────────────────────────────────────────────────────────────────────────

Időbélyeg                 Open         High         Low          Close        Ticks      
────────────────────────────────────────────────────────────────────────────────
2023-01-01 00:00:00       1.23456      1.23478      1.23445      1.23467      1,234
2023-01-01 00:01:00       1.23467      1.23489      1.23456      1.23478      1,245
2023-01-01 00:02:00       1.23478      1.23499      1.23467      1.23489      1,256
2023-01-01 00:03:00       1.23489      1.23501      1.23478      1.23490      1,267
2023-01-01 00:04:00       1.23490      1.23512      1.23489      1.23501      1,278

📊 H1 (1 órás) OHLCV adatok (első 5 sor):
────────────────────────────────────────────────────────────────────────────────

Időbélyeg                 Open         High         Low          Close        Ticks      
────────────────────────────────────────────────────────────────────────────────
2023-01-01 00:00:00       1.23456      1.23890      1.23345      1.23878      86,400
2023-01-01 01:00:00       1.23878      1.24123      1.23789      1.24098      86,400
2023-01-01 02:00:00       1.24098      1.24345      1.23987      1.24234      86,400
2023-01-01 03:00:00       1.24234      1.24567      1.24123      1.24456      86,400
2023-01-01 04:00:00       1.24456      1.24789      1.24345      1.24678      86,400

────────────────────────────────────────────────────────────────────────────────
💾 5. FÁZIS: EXPORTÁLÁS CSV FÁJLBA
────────────────────────────────────────────────────────────────────────────────

⏳ M1 adatok exportálása: output/test_candles_m1.csv
✅ M1 exportálás kész

⏳ H1 adatok exportálása: output/test_candles_h1.csv
✅ H1 exportálás kész

================================================================================
✅ DEMO SIKERESEN BEFEJEZVE!
================================================================================

📈 Összefoglaló:
   - Betöltött tick-ek: 86,400
   - M1 gyertya: 1,440
   - H1 gyertya: 24
   - Exportált fájlok: test_candles_m1.csv, test_candles_h1.csv
   - Kimeneti könyvtár: /home/elynea/Dokumentumok/neural-ai-next/output
```

## Kimeneti fájlok

### `output/test_candles_m1.csv`

Az 1 perces OHLCV gyertyák CSV formátumban.

**Struktúra:**
```csv
timestamp,open,high,low,close,ticks
2023-01-01 00:00:00,1.23456,1.23478,1.23445,1.23467,1234
2023-01-01 00:01:00,1.23467,1.23489,1.23456,1.23478,1245
...
```

### `output/test_candles_h1.csv`

Az 1 órás OHLCV gyertyák CSV formátumban.

**Struktúra:**
```csv
timestamp,open,high,low,close,ticks
2023-01-01 00:00:00,1.23456,1.23890,1.23345,1.23878,86400
2023-01-01 01:00:00,1.23878,1.24123,1.23789,1.24098,86400
...
```

## Hibakezelés

A szkript robusztus hibakezeléssel rendelkezik:

1. **Nincs adat:**
   ```
   ❌ Hiba: Nincsenek elérhető dátumok az EURUSD szimbólumhoz!
      Kérjük, először töltsön le adatokat a scripts/download_history.py szkripttel.
   ```

2. **Üres adattartomány:**
   ```
   ❌ Hiba: Nincsenek tick adatok a kiválasztott dátumhoz!
   ```

3. **Váratlan hibák:**
   - Teljes stack trace megjelenítése
   - Hibakód: 1

4. **Felhasználói megszakítás (Ctrl+C):**
   ```
   ⚠️  A szkriptet a felhasználó megszakította.
   ```
   - Hibakód: 0

## Technikai részletek

### Performance optimalizációk

1. **Backend kiválasztás:**
   - AVX2 támogatás esetén: PolarsBackend (gyorsabb)
   - Kompatibilitási mód: PandasBackend

2. **Polars group_by_dynamic:**
   - Extremely fast time-based aggregation
   - Lazy evaluation for memory efficiency
   - Multi-threaded execution

3. **Aszinkron I/O:**
   - Párhuzamos fájlolvasás
   - Nem blokkoló műveletek

### Adatfolyam

```
Tick Data (Parquet)
    ↓
Polars DataFrame
    ↓
group_by_dynamic()
    ↓
OHLCV DataFrame
    ↓
CSV Export
```

## Testreszabás

### Időkeretek módosítása

Más időkeretek használata:

```python
# 5 perces
ohlcv_m5 = self._resample_to_ohlcv(pl_data, "5m")

# 15 perces
ohlcv_m15 = self._resample_to_ohlcv(pl_data, "15m")

# Napi
ohlcv_d1 = self._resample_to_ohlcv(pl_data, "1d")
```

### Szimbólum módosítása

Más pénzpár használata:

```python
available_dates = await storage.get_available_dates("GBPUSD")  # vagy más szimbólum
```

### Sorok számának módosítása

Több/m kevesebb sor megjelenítése:

```python
self._display_ohlcv_data(ohlcv_m1, "M1 (1 perces)", 10)  # 10 sor
```

## Kapcsolódó dokumentáció

- [Storage Architektúra](../core/storage/index.md)
- [ParquetStorageService](../core/storage/implementations/parquet_storage.md)
- [Polars Backend](../core/storage/backends/polars_backend.md)
- [Tick Data Collection](../../planning/specs/04_data_warehouse.md)

## Jövőbeli fejlesztések

- [ ] Több szimbólum támogatása egy futtatásban
- [ ] Egyéni időkeretek (pl. 15m, 4h)
- [ ] További aggregációk (VWAP, TWAP)
- [ ] Real-time resampling demo
- [ ] Grafikon generálás matplotlib-pal

## License

Neural AI Next - Proprietary

## Changelog

### v1.0.0 (2025-12-30)
- Kezdeti verzió
- M1 és H1 resampling támogatás
- Színes konzol kimenet
- CSV export
- Átfogó hibakezelés