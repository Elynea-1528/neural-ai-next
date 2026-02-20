# neural_ai/data/storage/backends/polars_backend.py

Polars Storage Backend Modul.

Ez a modul tartalmazza a Polars alapú tárolási backend implementációt,
amely a Parquet formátumot használja a DataFrame-ek tárolásához.
A modul lazy importot használ a polars és pyarrow csomagok számára.

## Importok

```python
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import cast
from neural_ai.data.storage.backends.base import StorageBackend
import polars
import pyarrow
import pyarrow.parquet
import neural_ai.data.storage.backends.polars_backend
```

## Osztály: `PolarsDataFrame`

Wrapper osztály a Polars DataFrame köré lazy importtal.

Ez az osztály biztosítja, hogy a polars csomag csak akkor töltődjön be,
amikor az osztályt valóban használják.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

Inicializálja a PolarsDataFrame wrapper-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_import_polars()`

```python
def _import_polars(self) -> tuple[Any, Any, Any]
```

Lazy import a polars és pyarrow csomagok számára.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `tuple[Any, Any, Any]`

#### `pl()`

```python
def pl(self) -> Any
```

Polars modul lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `pa()`

```python
def pa(self) -> Any
```

PyArrow modul lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `pq()`

```python
def pq(self) -> Any
```

PyArrow Parquet modul lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

## Osztály: `PolarsBackend(StorageBackend)`

Polars alapú tárolási backend Parquet formátumhoz.

Ez a backend a Polars DataFrame-eket használja a gyors adatfeldolgozáshoz
és a PyArrow Parquet formátumot a hatékony tároláshoz. Támogatja a
chunkolást, aszinkron műveleteket és a particionált tárolást.

A backend lazy importot használ, így a polars és pyarrow csomagok csak
akkor töltődnek be, amikor az osztályt példányosítják.

Attribútumok:
    name: 'polars'
    supported_formats: ['parquet']
    is_async: True

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: Any)
```

Inicializálja a PolarsBackend példányt. A lazy import miatt a polars és pyarrow csomagok csak akkor töltődnek be, amikor az első műveletet végrehajtjuk.

**Paraméterek:**

- **`self`**
- **`logger`** (`Any`)

#### `_ensure_initialized()`

```python
def _ensure_initialized(self) -> None
```

Biztosítja, hogy a polars csomag betöltődött.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `polars_wrapper()`

```python
def polars_wrapper(self) -> PolarsDataFrame
```

Visszaadja a polars wrapper-t (teszteléshez).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `PolarsDataFrame`

#### `write()`

```python
def write(self, data: Any, path: str) -> None
```

DataFrame adatok írása Parquet formátumban.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A tárolandó Polars DataFrame
- **`path`** (`str`): A cél elérési út (.parquet kiterjesztéssel) **kwargs: További konfigurációs paraméterek - compression: Tömörítési algoritmus (alapértelmezett: 'snappy') - partition_by: Particionálási oszlopok listája - schema: Adatséma definíció

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az adatok érvénytelenek vagy az elérési út hibás
- **`FileNotFoundError`**: Ha a célkönyvtár nem létezik
- **`RuntimeError`**: Ha a tárolási művelet sikertelen

#### `read()`

```python
def read(self, path: str) -> Any
```

DataFrame adatok olvasása Parquet fájlból.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrás elérési út **kwargs: További konfigurációs paraméterek - columns: Csak ezen oszlopok betöltése - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)]) - chunk_size: Chunk méret chunkolás esetén

**Visszatérési érték:**

- Típus: `Any`
- A beolvasott Polars DataFrame

**Kivételek:**

- **`FileNotFoundError`**: Ha a forrásfájl nem létezik
- **`ValueError`**: Ha a fájlformátum nem támogatott
- **`RuntimeError`**: Ha az olvasási művelet sikertelen

#### `_read_chunked()`

```python
def _read_chunked(self, path: str, chunk_size: int, columns: list[str] | None, filters: list[tuple[Any, ...]] | None) -> Any
```

Chunkoltan olvassa a Parquet fájlt.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrás elérési út
- **`chunk_size`** (`int`): Egy chunk mérete sorokban
- **`columns`** (`list[str] | None`): Csak ezen oszlopok betöltése
- **`filters`** (`list[tuple[Any, ...]] | None`): Szűrők a partíciókra

**Visszatérési érték:**

- Típus: `Any`
- Az összes chunkból összefűzött DataFrame

#### `append()`

```python
def append(self, data: Any, path: str) -> None
```

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz. Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi az új adatokat a meglévőhöz.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A hozzáfűzendő DataFrame
- **`path`** (`str`): A cél elérési út **kwargs: További konfigurációs paraméterek - compression: Tömörítési algoritmus - schema_validation: Sémavizsgálat engedélyezése

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az adatok sémája nem kompatibilis a meglévővel
- **`FileNotFoundError`**: Ha a célkönyvtár nem létezik
- **`RuntimeError`**: Ha a hozzáfűzési művelet sikertelen

#### `_validate_schema()`

```python
def _validate_schema(self, existing: Any, new: Any) -> bool
```

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

**Paraméterek:**

- **`self`**
- **`existing`** (`Any`): A meglévő DataFrame
- **`new`** (`Any`): Az új DataFrame

**Visszatérési érték:**

- Típus: `bool`
- True, ha a sémák kompatibilisek, egyébként False

#### `supports_format()`

```python
def supports_format(self, format_name: str) -> bool
```

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

**Paraméterek:**

- **`self`**
- **`format_name`** (`str`): A formátum neve (pl. 'parquet', 'csv')

**Visszatérési érték:**

- Típus: `bool`
- True, ha a formátum támogatott, egyébként False

#### `get_info()`

```python
def get_info(self, path: str) -> dict[str, Any]
```

Parquet fájl információinak lekérdezése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): Az elérési út

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A fájl információit tartalmazó dictionary: - size: Fájlméret bájtban - rows: Sorok száma - columns: Oszlopok listája - format: 'parquet' - created: Létrehozás dátuma - modified: Módosítás dátuma

**Kivételek:**

- **`FileNotFoundError`**: Ha a fájl nem létezik

---

**Forrásfájl:** [`neural_ai/data/storage/backends/polars_backend.py`](../../neural_ai/data/storage/backends/polars_backend.py)
