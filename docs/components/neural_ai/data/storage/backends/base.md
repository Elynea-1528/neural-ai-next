# neural_ai/data/storage/backends/base.py

Storage Backend Base Modul.

Ez a modul tartalmazza a tárolási backend-ek absztrakt alaposztályát,
amely definiálja a kötelező interfészt minden tárolási implementációhoz.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Protocol
from typing import cast
from neural_ai.core.logger.interfaces import LoggerInterface
```

## Osztály: `DataFrameProtocol(Protocol)`

Protokoll a DataFrame-szerű objektumok típusozásához.

### Metódusok

#### `columns()`

```python
def columns(self) -> list[str]
```

Lekéri a DataFrame oszlopait.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`

#### `__len__()`

```python
def __len__(self) -> int
```

Visszaadja a DataFrame sorainak számát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

## Osztály: `StorageBackend(ABC)`

Absztrakt alaposztály a tárolási backend-ek számára.

Ez az osztály definiálja a kötelező interfészt, amelyet minden tárolási
backend implementációjának támogatnia kell. A backend-ek felelősek a
DataFrame-ek tárolásáért, olvasásáért és hozzáfűzéséért különböző
formátumokban (elsősorban Parquet).

A backend-eknek támogatniuk kell a chunkolást és aszinkron műveleteket
a nagy adathalmazok hatékony kezeléséhez.

Attribútumok:
    name: A backend neve (pl. 'polars', 'pandas')
    supported_formats: A támogatott fájlformátumok listája
    is_async: Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: LoggerInterface, name: str, supported_formats: list[str], is_async: bool = True) -> None
```

Inicializálja a StorageBackend példányt.

**Paraméterek:**

- **`self`**
- **`logger`** (`LoggerInterface`): A logger interfész példánya
- **`name`** (`str`): A backend egyedi neve
- **`supported_formats`** (`list[str]`): A támogatott fájlformátumok listája
- **`is_async`** (`bool`) = `True`: Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket

**Visszatérési érték:**

- Típus: `None`

#### `write()`

```python
def write(self, data: Any, path: str) -> None
```

DataFrame adatok írása a megadott elérési útra.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): A tárolandó DataFrame
- **`path`** (`str`): A cél elérési út **kwargs: További konfigurációs paraméterek - compression: Tömörítési algoritmus (pl. 'snappy', 'gzip') - partition_by: Particionálási oszlopok listája - schema: Adatséma definíció

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az adatok érvénytelenek vagy az elérési út nem létezik
- **`FileNotFoundError`**: Ha a célkönyvtár nem létezik
- **`RuntimeError`**: Ha a tárolási művelet sikertelen

#### `read()`

```python
def read(self, path: str) -> Any
```

DataFrame adatok olvasása a megadott elérési útról.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrás elérési út **kwargs: További konfigurációs paraméterek - columns: Csak ezen oszlopok betöltése - filters: Szűrők a partíciókra (pl. [('year', '=', 2023)]) - chunk_size: Chunk méret chunkolás esetén

**Visszatérési érték:**

- Típus: `Any`
- A beolvasott DataFrame

**Kivételek:**

- **`FileNotFoundError`**: Ha a forrásfájl nem létezik
- **`ValueError`**: Ha a fájlformátum nem támogatott
- **`RuntimeError`**: Ha az olvasási művelet sikertelen

#### `append()`

```python
def append(self, data: Any, path: str) -> None
```

DataFrame adatok hozzáfűzése egy meglévő fájlhoz. Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi az új adatokat a meglévőhöz.

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

Fájl információinak lekérdezése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): Az elérési út

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A fájl információit tartalmazó dictionary: - size: Fájlméret bájtban - rows: Sorok száma - columns: Oszlopok listája - format: Fájlformátum - created: Létrehozás dátuma - modified: Módosítás dátuma

**Kivételek:**

- **`FileNotFoundError`**: Ha a fájl nem létezik

#### `validate_data()`

```python
def validate_data(self, data: Any) -> bool
```

DataFrame érvényességének ellenőrzése.

**Paraméterek:**

- **`self`**
- **`data`** (`Any`): Az ellenőrizendő DataFrame

**Visszatérési érték:**

- Típus: `bool`
- True, ha a DataFrame érvényes, egyébként False

#### `__repr__()`

```python
def __repr__(self) -> str
```

A backend szöveges reprezentációja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`

---

**Forrásfájl:** [`neural_ai/data/storage/backends/base.py`](../../neural_ai/data/storage/backends/base.py)
