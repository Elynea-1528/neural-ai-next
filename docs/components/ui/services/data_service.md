# Data Service

## Áttekintés

A `DataService` osztály az adatkezelési szolgáltatást implementálja, amely az adatok betöltését, szűrését és kezelését végzi Big Data támogatással. Ez az osztály a CoreBridge-en keresztül éri el a backend komponenseket (Bi5Downloader, ParquetStorage).

## Architektúra

- **Interfész:** [`DataServiceInterface`](../../../neural_ai/ui/interfaces/data_service_interface.py)
- **Implementáció:** [`DataService`](../../../neural_ai/ui/services/data_service.py)
- **Függőségek:**
  - `CoreBridgeInterface`: A backend komponensek eléréséhez
  - `IJForexDownloader`: Történelmi adatok letöltéséhez
  - `StorageInterface`: Adatok Parquet formátumban történő tárolásához

## Főbb metódusok

### `download_history(symbol, start, end)`

Történelmi adatok letöltése aszinkron módon. Ez a metódus a CoreBridge-en keresztül eléri a Bi5Downloader-t, és valós adatletöltést végez a Dukascopy .bi5 formátumból.

**Paraméterek:**
- `symbol` (str): A szimbólum (pl. 'EURUSD')
- `start` (datetime): A kezdő dátum
- `end` (datetime): A záró dátum

**Visszatérési érték:**
- `dict[str, Any]`: A letöltött adatok metaadatai és az adatok
  - `symbol`: A letöltött szimbólum
  - `start_date`: Kezdő dátum ISO formátumban
  - `end_date`: Záró dátum ISO formátumban
  - `status`: Letöltési állapot ('downloaded', 'failed', 'partial')
  - `records`: Letöltött rekordok száma
  - `size_mb`: Letöltött adatok mérete MB-ban
  - `format`: Az adatformátum ('parquet')
  - `path`: A tárolási útvonal
  - `successful_dates`: Sikeres dátumok száma
  - `failed_dates`: Sikertelen dátumok száma
  - `total_days`: Összes napok száma

**Kivételek:**
- `ValueError`: Ha a dátumtartomány érvénytelen
- `RuntimeError`: Ha a letöltés sikertelen

**Működés:**
1. Dátumtartomány ellenőrzése (kezdő dátum nem lehet későbbi, mint a záró dátum, és nem lehet a jövőben)
2. Bi5Downloader komponens lekérése a CoreBridge-en keresztül
3. ParquetStorage komponens lekérése a mentéshez
4. Dátumok iterálása és adatok letöltése naponként
5. Tick adatok konvertálása Polars DataFrame-re
6. Volume oszlop hozzáadása (`ask_volume` + `bid_volume`)
7. Adatok mentése a storage-ba óra szintű `unique_id`-vel
8. Állapot meghatározása a sikeres/sikertelen dátumok alapján

### `load_data(source, filters, chunk_size)`

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**
- `source` (str): Az adatforrás azonosítója
- `filters` (dict[str, Any] | None): Szűrőfeltételek
- `chunk_size` (int): A chunkok mérete (alapértelmezett: 10000)

**Visszatérési érték:**
- `Generator[list[dict[str, Any]], None, None]`: Adat chunkok

**Kivételek:**
- `ValueError`: Ha az adatforrás ismeretlen

### `get_data_sources()`

Elérhető adatforrások lekérdezése.

**Visszatérési érték:**
- `list[dict[str, str]]`: Az adatforrások listája

### `get_data_info(source)`

Adatforrás információk lekérdezése.

**Paraméterek:**
- `source` (str): Az adatforrás azonosítója

**Visszatérési érték:**
- `dict[str, Any]`: Az adatforrás metaadatai

**Kivételek:**
- `ValueError`: Ha az adatforrás ismeretlen

### `apply_filters(data, filters)`

Szűrők alkalmazása adatokra.

**Paraméterek:**
- `data` (list[dict[str, Any]]): A szűrendő adatok
- `filters` (dict[str, Any]): Az alkalmazandó szűrők

**Visszatérési érték:**
- `list[dict[str, Any]]`: A szűrt adatok

### `export_data(data, format, destination)`

Adatok exportálása különböző formátumokba.

**Paraméterek:**
- `data` (list[dict[str, Any]]): Az exportálandó adatok
- `format` (str): A célformátum (parquet, csv, json)
- `destination` (str): A cél útvonal

**Visszatérési érték:**
- `bool`: True, ha sikeres az exportálás

**Kivételek:**
- `ValueError`: Ha a formátum nem támogatott

## Adatforrások

A DataService a következő adatforrásokat támogatja:

1. **Tick Adatok** (`tick_data`): Valós idejű tick adatok
2. **OHLC Adatok** (`ohlc_data`): Nyitó, magas, alacsony, záró adatok
3. **Piaci Adatok** (`market_data`): Általános piaci adatok

## Big Data támogatás

A DataService a következő Big Data funkciókat támogatja:

- **Chunkolás:** Az adatok kisebb darabokban való betöltése
- **Aszinkronitás:** A letöltések és mentések aszinkron módon történnek
- **Parquet formátum:** A hatékony oszlop-alapú tárolási formátum

## Polars DataFrame konverzió

A `download_history` metódus a letöltött tick adatokat Polars DataFrame-re konvertálja a következő oszlopokkal:

- `timestamp`: Az adat időbélyege
- `bid`: A bid ár
- `ask`: Az ask ár
- `ask_volume`: Az ask volumen
- `bid_volume`: A bid volumen
- `source`: Az adat forrása (pl. 'jforex')
- `volume`: A technikai volume oszlop (`ask_volume` + `bid_volume`)

## Mentés a Storage-ba

A konvertált DataFrame-eket a ParquetStorage komponens segítségével menti a következő paraméterekkel:

- `symbol`: A szimbólum
- `data`: A Polars DataFrame
- `date`: A dátum
- `unique_id`: Az óra száma (pl. "12")

## Tesztelés

A DataService-t a [`tests/ui/services/test_data_service.py`](../../../tests/ui/services/test_data_service.py) fájlban lévő tesztek ellenőrzik. A tesztek a következőket ellenőrzik:

- Inicializálás és adatforrások lekérdezése
- Adatok betöltése és szűrése
- Történelmi adatok letöltése és mentése
- Hibakezelés érvénytelen dátumtartomány esetén
- Hibakezelés, ha a letöltő vagy tároló komponens nem érhető el
- Viselkedés, ha egy adott dátumra nincs adat

## Használati példa

```python
from datetime import datetime, UTC
from neural_ai.ui.services.data_service import DataService
from neural_ai.ui.core_bridge import CoreBridge

# CoreBridge inicializálása
bridge = CoreBridge()
bridge.initialize(config, logger)

# DataService példányosítása
data_service = DataService(bridge)

# Történelmi adatok letöltése
start_date = datetime.now(UTC) - timedelta(days=1)
end_date = datetime.now(UTC)
result = await data_service.download_history("EURUSD", start_date, end_date)

print(f"Letöltött rekordok: {result['records']}")
print(f"Státusz: {result['status']}")
print(f"Méret: {result['size_mb']} MB")
```

## Kapcsolódó dokumentáció

- [Architektúra szabványok](../../development/architecture_standards.md)
- [Core Bridge](../core_bridge.md)
- [Storage Interface](../../../neural_ai/core/storage/interfaces/storage_interface.py)
- [JForex Downloader Interface](../../../neural_ai/collectors/jforex/interfaces/downloader_interface.py)