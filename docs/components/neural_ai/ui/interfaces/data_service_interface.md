# neural_ai/ui/interfaces/data_service_interface.py

Data Service interfész definíciója.

Ez az interfész definiálja az adatkezelési szolgáltatás szerződését,
amely az adatok betöltését, szűrését és kezelését végzi.

## Importok

```python
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import runtime_checkable
import pandas
```

## Osztály: `DataServiceInterface(Protocol)`

Data Service interfész - Adatkezelésért felelős.

Ez az interfész definiálja az adatok lekérdezését és kezelését
végző metódusokat, Big Data támogatással.

### Metódusok

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

#### `get_default_date_range()`

```python
def get_default_date_range(self) -> tuple[datetime, datetime]
```

Alapértelmezett dátumtartomány lekérdezése a konfigurációból. A metódus kiolvassa a configból a dátumokat, és datetime objektumokká konvertálja őket. Ha a konfiguráció üres vagy hiba történik, akkor fallback értékeket használ.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `tuple[datetime, datetime]`
- tuple[datetime, datetime]: A kezdő és záró dátum tuple-ben. Fallback: (2020-01-01, ma)

#### `download_history()`

```python
async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]
```

Történelmi adatok letöltése aszinkron módon a Data Hub-ból.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum (pl. 'EURUSD' vagy 'ALL' az összesre)
- **`start`** (`datetime`): A kezdő dátum
- **`end`** (`datetime`): A záró dátum

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A letöltés eredménye és metaadatok

#### `list_available_data()`

```python
def list_available_data(self, symbol: str | None = None) -> pd.DataFrame
```

Elérhető adatok listázása a Data Hub-ban.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str | None`) = `None`: Opcionális szimbólum szűréshez

**Visszatérési érték:**

- Típus: `pd.DataFrame`
- pd.DataFrame: Az elérhető adatok táblázata

#### `get_storage_path()`

```python
def get_storage_path(self) -> Path
```

A Data Hub tárhelyének elérési útjának lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`
- Path: A tárhely elérési útja

#### `get_configured_symbols()`

```python
def get_configured_symbols(self) -> list[str]
```

Konfigurált szimbólumok lekérdezése. A metódus a konfigurációból kiolvassa a JForex collectorhoz tartozó szimbólumokat. Ha a konfiguráció üres vagy hiba történik, akkor egy alapértelmezett szimbólumlistát ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A konfigurált szimbólumok listája. Alapértelmezett esetben ["EURUSD"]-t ad vissza.

---

**Forrásfájl:** [`neural_ai/ui/interfaces/data_service_interface.py`](../../neural_ai/ui/interfaces/data_service_interface.py)
