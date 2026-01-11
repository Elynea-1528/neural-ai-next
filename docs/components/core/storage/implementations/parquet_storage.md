# ParquetStorageService - Particionált Parquet tároló szolgáltatás

## Áttekintés

A `ParquetStorageService` osztály implementálja a Tick adatok particionált Parquet formátumban történő tárolását és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú particionálást használ a gyors lekérdezés érdekében.

## Architektúra

### Osztály hierarchia
```
StorageInterface (ABC)
└── ParquetStorageService (SingletonMeta)
```

### Dependenciák
- **HardwareInterface**: Hardver képességek detektálása
- **LoggerInterface**: Naplózás
- **StorageBackend**: Adatok olvasása/írása (PolarsBackend vagy PandasBackend)

### Főbb komponensek
- **Backend kiválasztás**: AVX2 támogatáson alapuló automatikus backend kiválasztás
- **Particionálás**: Szimbólum / év / hónap / nap szerkezet
- **Aszinkron műveletek**: Párhuzamos adatbetöltés
- **Deduplikáció**: Timestamp + bid + ask alapján
- **Checksum**: Adatintegritás ellenőrzés

## API Referencia

### Inicializáció

```python
service = ParquetStorageService(
    base_path="/data/tick",
    compression="snappy",
    hardware=hardware_interface,
    logger=logger_interface
)
```

### Tick adatok tárolása

```python
await service.store_tick_data(
    symbol="EURUSD",
    data=tick_dataframe,
    date=datetime(2023, 12, 23)
)
```

### Tick adatok olvasása

```python
data = await service.read_tick_data(
    symbol="EURUSD",
    start_date=datetime(2023, 12, 1),
    end_date=datetime(2023, 12, 31)
)
```

### Elérhető dátumok lekérdezése

```python
dates = await service.get_available_dates("EURUSD")
```

### Adatintegritás ellenőrzés

```python
is_valid = await service.verify_data_integrity(
    symbol="EURUSD",
    date=datetime(2023, 12, 23)
)
```

### Checksum számítás

```python
checksum = await service.calculate_checksum(
    symbol="EURUSD",
    date=datetime(2023, 12, 23)
)
```

### Tárolási statisztikák

```python
stats = await service.get_storage_stats(symbol="EURUSD")
```

## Konfiguráció

### Paraméterek
- `base_path`: Alapútvonal (alapértelmezett: "data/tick")
- `compression`: Tömörítési algoritmus (alapértelmezett: "snappy")
- `hardware`: Hardver interfész (opcionális)
- `logger`: Logger interfész (opcionális)

### Környezeti követelmények
- **Python**: 3.12+
- **Polars**: AVX2 támogatással gyorsabb feldolgozás
- **Pandas**: Kompatibilitási mód
- **FastParquet**: Pandas backend-hez

## Adatmodell

### Tick adat struktúra
```python
{
    "timestamp": datetime,
    "bid": float,
    "ask": float,
    "volume": float,
    "ask_volume": float,
    "bid_volume": float,
    "source": str
}
```

### Particionálás szerkezet
```
data/tick/
├── EURUSD/
│   ├── year=2023/
│   │   ├── month=12/
│   │   │   ├── day=23/
│   │   │   │   ├── tick_20231223_abc123.parquet
│   │   │   │   └── tick_20231223_def456.parquet
│   │   │   └── day=24/
│   │   │       └── ...
│   │   └── month=11/
│   │       └── ...
│   └── year=2024/
│       └── ...
└── USDJPY/
    └── ...
```

## Teljesítmény jellemzők

### Backend kiválasztás
- **PolarsBackend**: AVX2 támogatással ~3-5x gyorsabb
- **PandasBackend**: SSE4.2+ támogatással kompatibilitási mód

### Aszinkron feldolgozás
- Párhuzamos fájl olvasás `asyncio.gather()` használatával
- Chunk-olás nagy adathalmazokhoz

### Optimalizációk
- Deduplikáció betöltéskor
- Timestamp szerinti rendezés
- Memória hatékony feldolgozás

## Hibakezelés

### Kivételek
- `StorageIOError`: IO műveletek során
- `StorageNotFoundError`: Hiányzó fájlok/könyvtárak
- `ValueError`: Érvénytelen bemenetek

### Loggolás
- Strukturált naplózás `structlog` használatával
- Debug, info, warning, error szintek
- Teljesítmény metrikák (fájlméret, sorok száma)

## Tesztelés

### Egységtesztek
A szolgáltatás teljes lefedettséget biztosító pytest teszteket tartalmaz:

```bash
pytest tests/core/storage/implementations/test_parquet_storage.py
```

### Lefedett funkciók
- Inicializáció különböző konfigurációkkal
- Backend kiválasztás hardver alapján
- Adatok tárolása és olvasása
- Integritás ellenőrzés
- Statisztikák lekérdezése

## Kapcsolódó komponensek

### Storage modul
- `StorageInterface`: Absztrakt interfész
- `StorageBackend`: Backend implementációk
- `StorageFactory`: Factory minta implementáció

### Egyéb modulok
- `HardwareInterface`: Hardver detektálás
- `LoggerInterface`: Naplózás
- `ConfigInterface`: Konfiguráció kezelés

## Fejlesztési megjegyzések

### Refaktorálás 2023-12-23
- `/ "tick"` útvonal komponens eltávolítása az összes metódusból
- DI és base osztályok használata
- Magyar docstringek és type hintsek
- Lint szabványok betartása

### Jövőbeli fejlesztések
- Big data chunking implementáció
- Elosztott tárolás támogatása
- Automatikus particionálás optimalizáció
