# Download History Script

## Áttekintés

A `download_history.py` script a Neural AI Next rendszer történelmi tick adatainak tömeges letöltésére szolgál a JForex adatforrásból. A script **Direct Storage Mode**-ban működik, ami azt jelenti, hogy a letöltött adatokat közvetlenül a ParquetStorageService segítségével menti, kikerülve az EventBus-t a maximális sebesség érdekében.

## Funkciók

- **Tömeges adatletöltés**: Több évnyi tick adat letöltése egyetlen parancs kiadásával
- **Óránkénti feldolgozás**: Az adatokat óránkénti részletekben dolgozza fel a JForex bi5 formátumának megfelelően
- **Determinisztikus fájlnevek**: Az óra alapján generált időbélyeggel ellátott fájlnevek (pl. `EURUSD_20231223_150000.parquet`)
- **Direct Storage**: Közvetlen mentés a Parquet tárolóba, magas teljesítmény érdekében
- **Hibatűrés**: Automatikus hibakezelés és visszaállítás a hálózati problémák esetén
- **Részletes naplózás**: Folyamatjelzés és statisztikák a letöltés folyamán

## Használat

### Alapvető használat

```bash
python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-12-31
```

### Paraméterek

- `--symbol`: A pénzpár szimbóluma (pl. EURUSD, GBPUSD, stb.)
- `--start`: A letöltés kezdő dátuma (YYYY-MM-DD formátumban)
- `--end`: A letöltés záró dátuma (YYYY-MM-DD formátumban)

### Példa

```bash
# Letöltés 1 nap adataira
python scripts/download_history.py --symbol EURUSD --start 2024-03-20 --end 2024-03-20

# Letöltés 1 hónap adataira
python scripts/download_history.py --symbol GBPUSD --start 2024-01-01 --end 2024-01-31

# Letöltés 1 év adataira
python scripts/download_history.py --symbol XAUUSD --start 2023-01-01 --end 2023-12-31
```

## Működési elv

### 1. Inicializálás

A script először inicializálja a Neural AI Next core rendszert:
- Konfiguráció betöltése
- Logger létrehozása
- ParquetStorageService inicializálása
- Bi5Downloader létrehozása (EventBus nélkül)

### 2. Adatletöltés

A letöltés naponként és óránként történik:

1. **Napok feldolgozása**: A script végigmegy az összes napon a kezdő és záró dátum között
2. **Órák feldolgozása**: Minden napon belül 0-tól 23 óráig minden órát letölt
3. **Tick adatok letöltése**: A Bi5Downloader segítségével letölti az adott órához tartozó tick adatokat
4. **Közvetlen mentés**: Az adatokat azonnal menti a Parquet tárolóba

### 3. Mentési folyamat

A `_save_ticks_direct` függvény végzi az adatok mentését:

```python
async def _save_ticks_direct(
    storage: "StorageInterface",
    symbol: str,
    ticks: list,
    date: datetime,
    logger: "LoggerInterface | None" = None,
) -> None:
    """Tick adatok közvetlen mentése a storage-ba (Direct Storage Mode)."""
```

**Lépések:**
1. Tick adatok konvertálása Polars DataFrame-re
2. Technikai 'volume' oszlop hozzáadása
3. Dátum és idő formázása a fájlnévhez
4. Mentés a storage-ba `unique_id` paraméterrel

### 4. Fájlnevek formátuma

A mentett fájlok neve determinisztikus, az óra alapján generált időbélyeget tartalmaz:

```
{SZIMBÓLUM}_{DÁTUM}_{ÓRA}0000.parquet
```

Példák:
- `EURUSD_20240320_150000.parquet` (2024. március 20., 15:00 óra)
- `GBPUSD_20240115_090000.parquet` (2024. január 15., 09:00 óra)

### 5. Statisztikák

A letöltés végén a script kiírja a statisztikákat:
- Sikeres napok száma
- Sikertelen napok száma
- Kihagyott órák száma
- Összes letöltött tick száma

## Adatstruktúra

A mentett Parquet fájlok a következő oszlopokat tartalmazzák:

| Oszlop | Típus | Leírás |
|--------|-------|---------|
| timestamp | datetime | A tick időbélyege (UTC) |
| bid | float | A bid ár |
| ask | float | Az ask ár |
| ask_volume | float | Az ask volumen |
| bid_volume | float | A bid volumen |
| source | string | Az adatforrás (jforex) |
| volume | float | Technikai volumen (ask_volume + bid_volume) |

## Hibakezelés

A script a következő hibákat kezeli:

- **DataNotAvailableError**: Az adott órához nem érhető el adat
- **DownloadError**: Hálózati hiba a letöltés során
- **DecodeError**: Hiba a bi5 adatok dekódolásakor
- **Exception**: Váratlan hibák

Minden hiba esetén a script naplózza a hibát és folytatja a következő órával.

## Teljesítmény

A Direct Storage Mode jelentős teljesítményjavulást nyújt:

- **Gyorsabb mentés**: Az adatok közvetlenül a Parquet fájlba kerülnek
- **Kisebb memóriahasználat**: Nincs szükség az adatok EventBus-on történő átvitelére
- **Párhuzamos feldolgozás**: Több óra adatai párhuzamosan is feldolgozhatók

## Kimenet

A script részletes kimenetet nyújt a letöltés folyamán:

```
🚀 Történelmi adat letöltés indítása (DIRECT STORAGE MODE)...
   Szimbólum: EURUSD
   Dátumtartomány: 2024-03-20 - 2024-03-20

📥 [1/1] Letöltés: 2024-03-20 00:00
   ✅ 3,540 tick letöltve
   ✅ 3,540 tick mentve -> EURUSD_20240320_000000.parquet

...

📊 LETÖLTÉS BEFEJEZVE - ÖSSZESÍTÉS
✅ Sikeres napok: 1/1
❌ Sikertelen napok: 0/1
⚠️  Kihagyott órák: 0
📈 Összes tick: 84,720
```

## Függőségek

- `neural_ai.collectors.jforex`: JForex adatgyűjtő komponensek
- `neural_ai.core.storage`: Parquet tároló szolgáltatás
- `neural_ai.core.logger`: Naplózási rendszer
- `polars`: Adatkeret kezelés
- `asyncio`: Aszinkron műveletek

## Kapcsolódó dokumentáció

- [JForex Collector](../collectors/jforex/index.md)
- [Parquet Storage](../core/storage/implementations/parquet_storage.md)
- [System Architecture](../../planning/specs/01_system_architecture.md)