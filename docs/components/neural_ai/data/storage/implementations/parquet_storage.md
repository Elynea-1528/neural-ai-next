# neural_ai/data/storage/implementations/parquet_storage.py

ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez a modul implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb
backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

Szerző: Neural AI Next csapat
Verzió: 2.0.0

## Importok

```python
import asyncio
import hashlib
from collections.abc import Sequence
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from pydantic import BaseModel
# ... és még 38 import
```

## Konstansok

- **`DataFrame`**
: `pd.DataFrame | pl.DataFrame`


## Osztály: `ParquetWriteConfig(BaseModel)`

Parquet írás opciók konfigurációja.

## Osztály: `ParquetReadConfig(BaseModel)`

Parquet olvasás opciók konfigurációja.

## Osztály: `ParquetStorageService(StorageInterface)`

Particionált Parquet tároló szolgáltatás backend selectorral.

Ez az osztály felelős a Tick adatok particionált Parquet formátumban történő
tárolásáért és lekérdezéséért. A particionálás dátum és szimbólum alapú,
ami lehetővé teszi a gyors és hatékony adatlekérdezést.

A szolgáltatás automatikusan detektálja a hardver képességeket és kiválasztja
a legoptimálisabb tárolási backend-et:
- PolarsBackend: AVX2 támogatással gyorsabb feldolgozás
- PandasBackend: Kompatibilitási mód régebbi CPU-khoz

Attributes:
    BASE_PATH: A tárolás alapútvonala
    engine: A Parquet engine ('fastparquet' vagy 'polars')
    compression: Tömörítési algoritmus ('snappy')
    backend: A kiválasztott tárolási backend

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', config: 'ConfigInterface | None' = None, event_bus: 'EventBusInterface | None' = None, base_path: str | Path | None = None, compression: str = 'snappy', hardware: 'HardwareInterface | None' = None) -> None
```

Inicializálja a ParquetStorageService-t backend selectorral. A hardver detekció alapján kiválasztja a megfelelő tárolási backend-et. Ha az AVX2 utasításkészlet elérhető, a PolarsBackend-et használja, egyébként a PandasBackend-et kompatibilitási módban.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): A naplózásért felelős interfész
- **`config`** (`'ConfigInterface | None'`) = `None`: A konfigurációért felelős interfész
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Az eseménybusz interfész
- **`base_path`** (`str | Path | None`) = `None`: Az alapútvonal a tároláshoz (opcionális)
- **`compression`** (`str`) = `'snappy'`: A tömörítési algoritmus (alapértelmezett: 'snappy')
- **`hardware`** (`'HardwareInterface | None'`) = `None`: A hardverképességek detektálásáért felelős interfész (opcionális) **kwargs: További opcionális paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `_select_backend()`

```python
def _select_backend(self) -> None
```

Backend kiválasztása hardver detekció alapján. Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért a hardver képességek alapján. Külön metódusba van kiszervezve, hogy a tesztek könnyen mockolhassák.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_get_path()`

```python
def _get_path(self, symbol: str, date: datetime, unique_id: str | None = None) -> Path
```

Elérési út generálása a megadott szimbólumhoz és dátumhoz.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma (pl. 'EURUSD')
- **`date`** (`datetime`): A dátum
- **`unique_id`** (`str | None`) = `None`: Egyedi azonosító a fájlnévhez (opcionális)

**Visszatérési érték:**

- Típus: `Path`
- A teljes elérési út a Parquet fájlhoz

**Példák:**

```python
    >>> service = ParquetStorageService()
    >>> date = datetime(2023, 12, 23)
    >>> path = service._get_path('EURUSD', date)
    >>> print(path)
    /data/tick/EURUSD/tick/year=2023/month=12/day=23/tick_20231223_abc123.parquet
```

#### `store_tick_data()`

```python
async def store_tick_data(self, symbol: str, data: Any, date: datetime, unique_id: str | None = None) -> None
```

Tick adatok tárolása particionált Parquet formátumban.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma
- **`data`** (`Any`): A Tick adatokat tartalmazó DataFrame
- **`date`** (`datetime`): A dátum, ami alapján a particionálás történik
- **`unique_id`** (`str | None`) = `None`: Egyedi azonosító a fájlnévhez (opcionális)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

#### `read_tick_data()`

```python
async def read_tick_data(self, symbol: str, start_date: datetime, end_date: datetime) -> Any
```

Tick adatok olvasása dátumtartományból.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma
- **`start_date`** (`datetime`): A kezdő dátum
- **`end_date`** (`datetime`): A záró dátum

**Visszatérési érték:**

- Típus: `Any`
- A Tick adatokat tartalmazó DataFrame Példa: >>> from datetime import datetime, timedelta >>> >>> service = ParquetStorageService() >>> start = datetime(2023, 12, 1) >>> end = datetime(2023, 12, 31) >>> >>> data = await service.read_tick_data('EURUSD', start, end) >>> print(f"Betöltött {len(data)} tick-ek")

#### `_read_parquet_async()`

```python
async def _read_parquet_async(self, path: Path) -> Any
```

Aszinkron Parquet olvasás.

**Paraméterek:**

- **`self`**
- **`path`** (`Path`): A Parquet fájl elérési útja

**Visszatérési érték:**

- Típus: `Any`
- A beolvasott DataFrame

#### `_concat_dataframes()`

```python
def _concat_dataframes(self, dfs: list[Any]) -> Any
```

DataFrame-ek összefűzése a backend típusának megfelelően.

**Paraméterek:**

- **`self`**
- **`dfs`** (`list[Any]`)

**Visszatérési érték:**

- Típus: `Any`

#### `_deduplicate_data()`

```python
def _deduplicate_data(self, data: Any) -> Any
```

Adatok deduplikációja timestamp + bid + ask alapján.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A deduplikálandó DataFrame

**Visszatérési érték:**

- Típus: `Any`
- A deduplikált DataFrame

#### `_filter_columns()`

```python
def _filter_columns(self, data: Any) -> Any
```

DataFrame oszlopainak szűrése csak a szükségesekre.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A szűrendő DataFrame

**Visszatérési érték:**

- Típus: `Any`
- A szűrt DataFrame csak a szükséges oszlopokkal

#### `_sort_by_timestamp()`

```python
def _sort_by_timestamp(self, data: Any) -> Any
```

DataFrame rendezése timestamp szerint.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A rendezendő DataFrame

**Visszatérési érték:**

- Típus: `Any`
- A rendezett DataFrame

#### `_filter_by_timestamp()`

```python
def _filter_by_timestamp(self, data: Any, start_date: datetime, end_date: datetime) -> Any
```

DataFrame szűrése időbélyeg alapján.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A szűrendő DataFrame
- **`start_date`** (`datetime`): A kezdő dátum
- **`end_date`** (`datetime`): A záró dátum

**Visszatérési érték:**

- Típus: `Any`
- A szűrt DataFrame

#### `get_available_dates()`

```python
async def get_available_dates(self, symbol: str) -> list[datetime]
```

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma

**Visszatérési érték:**

- Típus: `list[datetime]`
- Az elérhető dátumok listája Példa: >>> service = ParquetStorageService() >>> dates = await service.get_available_dates('EURUSD') >>> print(f"Elérhető dátumok: {len(dates)}")

#### `calculate_checksum()`

```python
async def calculate_checksum(self, symbol: str, date: datetime) -> str
```

Adatok checksum számítása integritás ellenőrzéshez.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma
- **`date`** (`datetime`): A dátum

**Visszatérési érték:**

- Típus: `str`
- A checksum SHA256 hash (az összes fájlra vonatkozik az adott napon) Példa: >>> service = ParquetStorageService() >>> checksum = await service.calculate_checksum('EURUSD', datetime.now()) >>> print(f"Ellenőrző összeg: {checksum}") Note: A checksum mostantól az összes fájlra vonatkozik az adott napon, nem csak egy specifikusra. Az összes fájl adatait összefűzi és az egészre számol checksum-ot.

#### `verify_data_integrity()`

```python
async def verify_data_integrity(self, symbol: str, date: datetime) -> bool
```

Adatintegritás ellenőrzése.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A pénzpár szimbóluma
- **`date`** (`datetime`): A dátum

**Visszatérési érték:**

- Típus: `bool`
- True ha az adatok integritása megfelelő, egyébként False Példa: >>> service = ParquetStorageService() >>> is_valid = await service.verify_data_integrity('EURUSD', datetime.now()) >>> print(f"Adatintegritás: {is_valid}") Note: Az integritás ellenőrzés mostantól az összes fájlra vonatkozik az adott napon. Az összes fájlt beolvassa, összefűzi, deduplikálja és ellenőrzi a rendezettséget.

#### `get_storage_stats()`

```python
async def get_storage_stats(self, symbol: str | None = None) -> dict[str, Any]
```

Tárolási statisztikák lekérdezése.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str | None`) = `None`: Opcionális szimbólum szűréshez

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A statisztikákat tartalmazó dictionary Példa: >>> service = ParquetStorageService() >>> stats = await service.get_storage_stats('EURUSD') >>> print(f"Összes fájlok: {stats['total_files']}")

#### `save_dataframe()`

```python
def save_dataframe(self, df: 'DataFrame', path: str) -> None
```

DataFrame mentése a megadott útvonalra. Ez egy adapter metódus a StorageInterface kompatibilitás érdekében. A ParquetStorageService saját store_tick_data metódusát használja.

**Paraméterek:**

- **`self`**
- **`df`** (`'DataFrame'`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> 'DataFrame'
```

DataFrame betöltése a megadott útvonalról. Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `'DataFrame'`

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

Objektum mentése a megadott útvonalra. Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

**Paraméterek:**

- **`self`**
- **`obj`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

Objektum betöltése a megadott útvonalról. Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `exists()`

```python
def exists(self, path: str) -> bool
```

Ellenőrzi, hogy az útvonal létezik-e.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

Fájl vagy könyvtár metaadatainak lekérdezése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `delete()`

```python
def delete(self, path: str) -> None
```

Fájl vagy könyvtár törlése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `list_dir()`

```python
def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]
```

Könyvtár tartalmának listázása.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)
- **`pattern`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `Sequence[Path]`

#### `_get_full_path()`

```python
def _get_full_path(self, path: str | Path) -> Path
```

Segédfüggvény az útvonal feloldásához.

**Paraméterek:**

- **`self`**
- **`path`** (`str | Path`)

**Visszatérési érték:**

- Típus: `Path`

---

**Forrásfájl:** [`neural_ai/data/storage/implementations/parquet_storage.py`](../../neural_ai/data/storage/implementations/parquet_storage.py)
