# ParquetStorageService

## Áttekintés

A `ParquetStorageService` egy particionált Parquet tároló szolgáltatás, amely a Neural AI Next rendszer Tick adatait tárolja és kezeli. A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

## Jellemzők

- **Dátum és szimbólum alapú particionálás**: Gyors és hatékony adatlekérdezés
- **Automatikus backend kiválasztás**: AVX2 támogatás esetén Polars, egyébként Pandas
- **Tömörítés**: Snappy algoritmus használata
- **Deduplikáció**: Timestamp + Bid + Ask alapú duplikátum eltávolítás
- **Aszinkron műveletek**: Párhuzamos fájlműveletek
- **Adatintegritás ellenőrzés**: Checksum számítás és rendezettség ellenőrzés

## Architektúra

### Osztályszerkezet

```python
class ParquetStorageService(StorageInterface, metaclass=SingletonMeta):
    """Particionált Parquet tároló szolgáltatás backend selectorral."""
    
    def __init__(
        self,
        base_path: str | Path | None = None,
        compression: str = "snappy",
        hardware: "HardwareInterface | None" = None,
        logger: "LoggerInterface | None" = None,
        **kwargs: Any
    ) -> None:
```

### Attribútumok

- `BASE_PATH`: A tárolás alapútvonala (alapértelmezett: `/data/tick`)
- `engine`: A Parquet engine ('fastparquet' vagy 'polars')
- `compression`: Tömörítési algoritmus ('snappy')
- `backend`: A kiválasztott tárolási backend
- `hardware`: Hardverképességek detektálásáért felelős interfész
- `logger`: Naplózásért felelős interfész

## Metódusok

### `__init__`

Inicializálja a ParquetStorageService-t backend selectorral.

**Paraméterek:**
- `base_path`: Az alapútvonal a tároláshoz (opcionális)
- `compression`: A tömörítési algoritmus (alapértelmezett: 'snappy')
- `hardware`: A hardverképességek detektálásáért felelős interfész (opcionális)
- `logger`: A naplózásért felelős interfész (opcionális)
- `**kwargs`: További opcionális paraméterek

### `_select_backend`

Backend kiválasztása hardver detekció alapján. Ha az AVX2 utasításkészlet elérhető, a PolarsBackend-et használja, egyébként a PandasBackend-et kompatibilitási módban.

### `_get_path`

Elérési út generálása a megadott szimbólumhoz és dátumhoz.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma (pl. 'EURUSD')
- `date`: A dátum
- `unique_id`: Egyedi azonosító a fájlnévhez (opcionális)

**Visszatérési érték:** A teljes elérési út a Parquet fájlhoz

### `store_tick_data`

Tick adatok tárolása particionált Parquet formátumban.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `data`: A Tick adatokat tartalmazó DataFrame
- `date`: A dátum, ami alapján a particionálás történik
- `unique_id`: Egyedi azonosító a fájlnévhez (opcionális)

**Kivételek:**
- `ValueError`: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

**Megvalósítás:**
- **Append-only logika**: Minden adat egyedi fájlba kerül mentésre, nincs read-modify-write művelet
- Ez biztosítja a 100%-os adatmentést, a deduplikációt olvasáskor végezzük
- Ha `unique_id` meg van adva, a fájlnév tartalmazza ezt az azonosítót
- Egyébként automatikusan generált időbélyeggel készül a fájlnév (Live mód)

### `read_tick_data`

Tick adatok olvasása dátumtartományból.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:** A Tick adatokat tartalmazó DataFrame

### `_read_parquet_async`

Aszinkron Parquet olvasás.

**Paraméterek:**
- `path`: A Parquet fájl elérési útja

**Visszatérési érték:** A beolvasott DataFrame

### `_concat_dataframes`

DataFrame-ek összefűzése a backend típusának megfelelően.

**Paraméterek:**
- `dfs`: Az összefűzendő DataFrame-ek listája

**Visszatérési érték:** Az összefűzött DataFrame

### `_deduplicate_data`

**KRITIKUS METÓDUS** - Adatok deduplikációja timestamp + bid + ask alapján.

Ez a metódus felelős azért, hogy csak akkor távolítson el duplikátumokat, ha az időbélyeg, bid és ask értékek tökéletesen megegyeznek. Így megőrizzük az azonos időbélyegű, de eltérő árú tick-eket (intra-millisecond ticks).

**Paraméterek:**
- `data`: A deduplikálandó DataFrame

**Visszatérési érték:** A deduplikált DataFrame

**Implementáció:**
- Polars backend: `pl_df.unique(subset=["timestamp", "bid", "ask"], maintain_order=False)`
- Pandas backend: `pd_df.drop_duplicates(subset=["timestamp", "bid", "ask"], keep="first")`

### `_sort_by_timestamp`

DataFrame rendezése timestamp szerint.

**Paraméterek:**
- `data`: A rendezendő DataFrame

**Visszatérési érték:** A rendezett DataFrame

### `_filter_by_timestamp`

DataFrame szűrése időbélyeg alapján.

**Paraméterek:**
- `data`: A szűrendő DataFrame
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:** A szűrt DataFrame

### `get_available_dates`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma

**Visszatérési érték:** Az elérhető dátumok listája

### `calculate_checksum`

Adatok checksum számítása integritás ellenőrzéshez.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:** A checksum SHA256 hash (az összes fájlra vonatkozik az adott napon)

### `verify_data_integrity`

Adatintegritás ellenőrzése.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:** True ha az adatok integritása megfelelő, egyébként False

### `get_storage_stats`

Tárolási statisztikák lekérdezése.

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:** A statisztikákat tartalmazó dictionary

## StorageInterface Implementáció

A `ParquetStorageService` implementálja a `StorageInterface`-t, ami a következő metódusokat tartalmazza:

- `save_dataframe(df, path, **kwargs)`: DataFrame mentése
- `load_dataframe(path, **kwargs)`: DataFrame betöltése
- `save_object(obj, path, **kwargs)`: Objektum mentése
- `load_object(path, **kwargs)`: Objektum betöltése
- `exists(path)`: Létezés ellenőrzése
- `get_metadata(path)`: Metaadatok lekérdezése
- `delete(path)`: Fájl vagy könyvtár törlése
- `list_dir(path, pattern)`: Könyvtár tartalmának listázása

## Használati példa

```python
import polars as pl
from datetime import datetime
from neural_ai.core.storage.factory import StorageFactory

# Szolgáltatás létrehozása
service = StorageFactory.get_storage("parquet")

# Adatok tárolása
data = pl.DataFrame({
    'timestamp': [datetime.now()],
    'bid': [1.1000],
    'ask': [1.1002],
    'volume': [1000],
    'source': ['jforex']
})

await service.store_tick_data('EURUSD', data, datetime.now())

# Adatok olvasása
start = datetime(2023, 12, 1)
end = datetime(2023, 12, 31)
loaded_data = await service.read_tick_data('EURUSD', start, end)
print(f"Loaded {len(loaded_data)} ticks")
```

## Deduplikáció Részletek

A deduplikáció logikája a következő kritériumok alapján működik:

**Régi logika (2026.01.02 előtt):**
- `subset=["timestamp", "source"]` vagy csak `["timestamp"]`
- Ez azt jelentette, hogy az azonos időbélyegű és forrású tick-eket eltávolította

**Új logika (2026.01.02-től):**
- `subset=["timestamp", "bid", "ask"]`
- Ez azt jelenti, hogy csak akkor távolít el duplikátumokat, ha az időbélyeg, bid és ask értékek tökéletesen megegyeznek
- **Előny**: Megőrzi az azonos időbélyegű, de eltérő árú tick-eket (intra-millisecond ticks), ami pontosabb ármozgásokat tükröz

## Fájlszerkezet

A tárolt adatok a következő könyvtárszerkezetet követik:

```
/data/tick/
├── EURUSD/
│   └── tick/
│       └── year=2023/
│           └── month=12/
│               └── day=23/
│                   ├── tick_20231223_abc123.parquet
│                   └── tick_20231223_def456.parquet
└── GBPUSD/
    └── tick/
        └── year=2023/
            └── month=12/
                └── day=23/
                    └── tick_20231223_ghi789.parquet
```

## Függőségek

- `polars`: AVX2 gyorsításhoz
- `pandas`: Kompatibilitási módhoz
- `fastparquet`: Parquet fájlok kezeléséhez
- `structlog`: Naplózáshoz

## Hibakezelés

A szolgáltatás a következő kivételeket dobhatja:

- `StorageIOError`: I/O hibák esetén
- `StorageNotFoundError`: Fájl nem található esetén
- `ValueError`: Érvénytelen adatok esetén

## Teljesítmény

- **PolarsBackend**: Akár 10x gyorsabb feldolgozás AVX2 támogatással
- **PandasBackend**: Kompatibilitási mód régebbi CPU-khoz
- **Párhuzamos olvasás**: Több fájl egyidejű betöltése
- **Particionálás**: Gyors dátumtartományos lekérdezések

## Verziótörténet

- **v2.0.0**: Hardver-gyorsítás detekció, automatikus backend kiválasztás
- **2026.01.02**: Deduplikáció módosítása timestamp + bid + ask alapúra
- **2026.01.03**: Append-only logika bevezetése - a `_read_existing_data_for_date` metódus eltávolítva
  - Minden adat egyedi fájlba kerül mentésre, nincs read-modify-write művelet
  - 100%-os adatmentés garantálása
  - Deduplikáció csak olvasáskor történik
