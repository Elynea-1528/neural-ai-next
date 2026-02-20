# neural_ai/ui/services/data_service.py

Data Service implementáció.

Ez a modul implementálja az adatkezelési szolgáltatást, amely
az adatok betöltését, szűrését és kezelését végzi Big Data támogatással.

## Importok

```python
import asyncio
from collections.abc import Generator
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
import pandas
# ... és még 9 import
```

## Osztály: `DataService(DataServiceInterface)`

Data Service - Adatkezelésért felelős.

Ez az osztály implementálja az adatok lekérdezését és kezelését
végző metódusokat, Big Data támogatással és chunkolással.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: Any, config: DataServiceConfig | None, core_components: Any) -> None
```

A Data Service inicializálása.

**Paraméterek:**

- **`self`**
- **`logger`** (`Any`): A logger példány
- **`config`** (`DataServiceConfig | None`): A szolgáltatás konfiguráció (Pydantic modell)
- **`core_components`** (`Any`): A core komponensek

**Visszatérési érték:**

- Típus: `None`

#### `core_components()`

```python
def core_components(self) -> Any
```

A core komponensek példány visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `data_sources()`

```python
def data_sources(self) -> dict[str, dict[str, str]]
```

Az adatforrások visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, dict[str, str]]`

#### `load_data()`

```python
def load_data(self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000) -> Generator[list[dict[str, Any]], None, None]
```

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**

- **`self`**
- **`source`** (`str`): Az adatforrás azonosítója
- **`filters`** (`dict[str, Any] | None`) = `None`: Szűrőfeltételek
- **`chunk_size`** (`int`) = `10000`: A chunkok mérete Yields: List[Dict[str, Any]]: Adat chunkok

**Visszatérési érték:**

- Típus: `Generator[list[dict[str, Any]], None, None]`

#### `get_data_sources()`

```python
def get_data_sources(self) -> list[dict[str, str]]
```

Elérhető adatforrások lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, str]]`
- List[Dict[str, str]]: Az adatforrások listája

#### `get_data_info()`

```python
def get_data_info(self, source: str) -> dict[str, Any]
```

Adatforrás információk lekérdezése.

**Paraméterek:**

- **`self`**
- **`source`** (`str`): Az adatforrás azonosítója

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Az adatforrás metaadatai

#### `apply_filters()`

```python
def apply_filters(self, data: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]
```

Szűrők alkalmazása adatokra.

**Paraméterek:**

- **`self`**
- **`data`** (`list[dict[str, Any]]`): A szűrendő adatok
- **`filters`** (`dict[str, Any]`): A alkalmazandó szűrők

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`
- List[Dict[str, Any]]: A szűrt adatok

#### `export_data()`

```python
def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool
```

Adatok exportálása különböző formátumokba.

**Paraméterek:**

- **`self`**
- **`data`** (`list[dict[str, Any]]`): Az exportálandó adatok
- **`format`** (`str`): A célformátum (parquet, csv, json)
- **`destination`** (`str`): A cél útvonal

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres az exportálás

#### `_generate_mock_data()`

```python
def _generate_mock_data(self, source: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]
```

Mock adatok generálása teszteléshez.

**Paraméterek:**

- **`self`**
- **`source`** (`str`): Az adatforrás azonosítója
- **`filters`** (`dict[str, Any] | None`) = `None`: Szűrőfeltételek

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`
- List[Dict[str, Any]]: A generált mock adatok

#### `get_default_date_range()`

```python
def get_default_date_range(self) -> tuple[datetime, datetime]
```

Alapértelmezett dátumtartomány lekérdezése a konfigurációból. A metódus kiolvassa a configból a `jforex.date_range.start` és `end` értékeit, és datetime objektumokká konvertálja őket. Ha a konfiguráció üres vagy hiba történik, akkor fallback értékeket használ.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `tuple[datetime, datetime]`
- tuple[datetime, datetime]: A kezdő és záró dátum tuple-ben. Fallback: (2020-01-01, ma)

#### `download_history()`

```python
async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]
```

Történelmi adatok letöltése aszinkron módon. Ez a metódus a CoreBridge-en keresztül eléri a Bi5Downloader-t, és valós adatletöltést végez a Dukascopy .bi5 formátumból.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum (pl. 'EURUSD' vagy 'ALL' az összesre)
- **`start`** (`datetime`): A kezdő dátum
- **`end`** (`datetime`): A záró dátum

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- dict[str, Any]: A letöltött adatok metaadatai és az adatok - symbol: A letöltött szimbólum (vagy 'ALL') - start_date: Kezdő dátum ISO formátumban - end_date: Záró dátum ISO formátumban - status: Letöltési állapot ('downloaded', 'failed', 'partial') - records: Letöltött rekordok száma - size_mb: Letöltött adatok mérete MB-ban - format: Az adatformátum ('parquet') - path: A tárolási útvonal - successful_dates: Sikeres napok száma - failed_dates: Sikertelen napok száma - total_days: Összes napok száma

**Kivételek:**

- **`ValueError`**: Ha a dátumtartomány érvénytelen
- **`RuntimeError`**: Ha a letöltés sikertelen

#### `_download_all_symbols()`

```python
async def _download_all_symbols(self, start: datetime, end: datetime) -> dict[str, Any]
```

Összes konfigurált szimbólum letöltése.

**Paraméterek:**

- **`self`**
- **`start`** (`datetime`): A kezdő dátum
- **`end`** (`datetime`): A záró dátum

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- dict[str, Any]: Összesített letöltési eredmények

#### `list_available_data()`

```python
def list_available_data(self, symbol: str | None = None) -> pd.DataFrame
```

Elérhető adatok listázása DataFrame formátumban. Ez a metódus a core_components-en keresztül eléri a ParquetStorage-t, és valós adatokról állít össze listát.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str | None`) = `None`: Opcionális szimbólum szűréshez

**Visszatérési érték:**

- Típus: `pd.DataFrame`
- pd.DataFrame: Az elérhető adatok DataFrame-je, amely tartalmazza: - source_id: Az adatforrás azonosítója - name: Az adatforrás neve - description: Leírás - format: Az adatformátum - size_gb: Méret GB-ban - records: Rekordok száma - last_updated: Utolsó frissítés időpontja - available_dates: Elérhető dátumok száma

#### `_get_storage_stats_async()`

```python
async def _get_storage_stats_async(self, storage: 'StorageInterface', symbol: str) -> dict[str, Any]
```

Segédfüggvény a storage statisztikák aszinkron lekérdezéséhez.

**Paraméterek:**

- **`self`**
- **`storage`** (`'StorageInterface'`): A storage interfész példány
- **`symbol`** (`str`): A szimbólum

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- dict[str, Any]: A statisztikák

#### `get_storage_path()`

```python
def get_storage_path(self) -> Path
```

Az adattárolási útvonal lekérdezése. Ez a metódus a core_components-en keresztül eléri a ParquetStorage-t, és a tényleges tárolási útvonalat adja vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`
- Path: Az adattárolási útvonal

**Kivételek:**

- **`RuntimeError`**: Ha a storage komponens nem érhető el

#### `get_configured_symbols()`

```python
def get_configured_symbols(self) -> list[str]
```

Konfigurált szimbólumok lekérdezése. A metódus eléri a konfigurációt a CoreBridge-en keresztül, és kiolvassa a JForex collectorhoz tartozó szimbólumokat. Ha a konfiguráció üres vagy hiba történik a lekérdezés során, akkor egy alapértelmezett szimbólumlistát ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A konfigurált szimbólumok listája. Alapértelmezett esetben ["EURUSD"]-t ad vissza, ha a konfigurációból nem sikerül lekérdezni a szimbólumokat.

**Példák:**

```python
    >>> data_service = DataService(bridge)
    >>> symbols = data_service.get_configured_symbols()
    >>> print(symbols)
    ['EURUSD', 'GBPUSD', 'USDJPY']
```

---

**Forrásfájl:** [`neural_ai/ui/services/data_service.py`](../../neural_ai/ui/services/data_service.py)
