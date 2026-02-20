# neural_ai/data/storage/backends/pandas_backend.py

Pandas Storage Backend Modul.

Ez a modul tartalmazza a Pandas alapú tárolási backend implementációt,
amely a FastParquet-et használja a DataFrame-ek tárolásához.
A modul lazy importot használ a pandas és fastparquet csomagok számára.

## Importok

```python
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from neural_ai.data.storage.backends.base import StorageBackend
import pandas
import fastparquet
import pandas
```

## Osztály: `PandasDataFrame`

Wrapper osztály a Pandas DataFrame köré lazy importtal.

Ez az osztály biztosítja, hogy a pandas és fastparquet csomagok csak
akkor töltődjön be, amikor az osztályt valóban használják.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

Inicializálja a PandasDataFrame wrapper-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_import_pandas()`

```python
def _import_pandas(self) -> tuple[Any, Any]
```

Lazy import a pandas és fastparquet csomagok számára.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `tuple[Any, Any]`

#### `pd()`

```python
def pd(self) -> Any
```

Pandas modul lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `fp()`

```python
def fp(self) -> Any
```

FastParquet modul lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `pandas()`

```python
def pandas(self) -> Any
```

Pandas modul lekérdezése (teszteléshez).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `fastparquet()`

```python
def fastparquet(self) -> Any
```

FastParquet modul lekérdezése (teszteléshez).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

## Osztály: `PandasBackend(StorageBackend)`

Pandas alapú tárolási backend FastParquet formátumhoz.

Ez a backend a Pandas DataFrame-eket használja és a FastParquet-et
a hatékony Parquet tároláshoz. Támogatja a chunkolást és aszinkron
műveleteket, valamint a particionált tárolást.

A backend lazy importot használ, így a pandas és fastparquet csomagok
csak akkor töltődnek be, amikor az osztályt példányosítják.

Attribútumok:
    name: 'pandas'
    supported_formats: ['parquet']
    is_async: True

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: Any) -> None
```

Inicializálja a PandasBackend példányt. A lazy import miatt a pandas és fastparquet csomagok csak akkor töltődnek be, amikor az első műveletet végrehajtjuk.

**Paraméterek:**

- **`self`**
- **`logger`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `_ensure_initialized()`

```python
def _ensure_initialized(self) -> None
```

Biztosítja, hogy a pandas csomag betöltődött.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `is_initialized()`

```python
def is_initialized(self) -> bool
```

Ellenőrzi, hogy a backend inicializálva van-e (teszteléshez).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `pandas_wrapper()`

```python
def pandas_wrapper(self) -> PandasDataFrame
```

Visszaadja a pandas wrapper-t (teszteléshez).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `PandasDataFrame`

#### `write()`

```python
def write(self, data: Any, path: str) -> None
```

DataFrame adatok írása Parquet formátumban FastParquet használatával.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A tárolandó Pandas DataFrame
- **`path`** (`str`): A cél elérési út (.parquet kiterjesztéssel) **kwargs: További konfigurációs paraméterek - compression: Tömörítési algoritmus (alapértelmezett: 'snappy') - partition_by: Particionálási oszlopok listája - schema: Adatséma definíció - index: Index mentése (alapértelmezett: False)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az adatok érvénytelenek vagy az elérési út hibás
- **`FileNotFoundError`**: Ha a célkönyvtár nem létezik
- **`RuntimeError`**: Ha a tárolási művelet sikertelen

#### `_write_partitioned()`

```python
def _write_partitioned(self, df: 'pd.DataFrame', path: str, partition_by: list[str], compression: str, index: bool) -> None
```

Particionált Parquet fájl írása.

**Paraméterek:**

- **`self`**
- **`df`** (`'pd.DataFrame'`): A tárolandó DataFrame
- **`path`** (`str`): A cél elérési út
- **`partition_by`** (`list[str]`): Particionálási oszlopok listája
- **`compression`** (`str`): Tömörítési algoritmus
- **`index`** (`bool`): Index mentése

**Visszatérési érték:**

- Típus: `None`

#### `read()`

```python
def read(self, path: str) -> 'pd.DataFrame'
```

DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrás elérési út **kwargs: További konfigurációs paraméterek - columns: Csak ezen oszlopok betöltése - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)]) - chunk_size: Chunk méret chunkolás esetén

**Visszatérési érték:**

- Típus: `'pd.DataFrame'`
- A beolvasott Pandas DataFrame

**Kivételek:**

- **`FileNotFoundError`**: Ha a forrásfájl nem létezik
- **`ValueError`**: Ha a fájlformátum nem támogatott
- **`RuntimeError`**: Ha az olvasási művelet sikertelen

#### `_read_chunked()`

```python
def _read_chunked(self, path: str, chunk_size: int, columns: list[str] | None, filters: list[tuple[Any, ...]] | None) -> 'pd.DataFrame'
```

Chunkoltan olvassa a Parquet fájlt.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrás elérési út
- **`chunk_size`** (`int`): Egy chunk mérete sorokban
- **`columns`** (`list[str] | None`): Csak ezen oszlopok betöltése
- **`filters`** (`list[tuple[Any, ...]] | None`): Szűrők a partíciókra

**Visszatérési érték:**

- Típus: `'pd.DataFrame'`
- Az összes chunkból összefűzött DataFrame

#### `append()`

```python
def append(self, data: Any, path: str) -> None
```

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz. Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi az új adatokat a meglévőhöz.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A hozzáfűzendő DataFrame
- **`path`** (`str`): A cél elérési út **kwargs: További konfigurációs paraméterek - compression: Tömörítési algoritmus - schema_validation: Sémavizsgálat engedélyezése - index: Index mentése

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az adatok sémája nem kompatibilis a meglévővel
- **`FileNotFoundError`**: Ha a célkönyvtár nem létezik
- **`RuntimeError`**: Ha a hozzáfűzési művelet sikertelen

#### `_validate_schema()`

```python
def _validate_schema(self, existing: 'pd.DataFrame', new: 'pd.DataFrame') -> bool
```

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

**Paraméterek:**

- **`self`**
- **`existing`** (`'pd.DataFrame'`): A meglévő DataFrame
- **`new`** (`'pd.DataFrame'`): Az új DataFrame

**Visszatérési érték:**

- Típus: `bool`
- True, ha a sémák kompatibilisek, egyébként False

#### `validate_schema()`

```python
def validate_schema(self, existing: 'pd.DataFrame', new: 'pd.DataFrame') -> bool
```

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e (teszteléshez).

**Paraméterek:**

- **`self`**
- **`existing`** (`'pd.DataFrame'`): A meglévő DataFrame
- **`new`** (`'pd.DataFrame'`): Az új DataFrame

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

**Forrásfájl:** [`neural_ai/data/storage/backends/pandas_backend.py`](../../neural_ai/data/storage/backends/pandas_backend.py)
