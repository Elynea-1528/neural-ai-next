# neural_ai/data/storage/implementations/file_storage.py

FileStorage implementáció.

A modulban található:
    - FileStorage: Fájlrendszer alapú tárolási implementáció Parquet formátummal.

## Importok

```python
import os
import pickle
from collections.abc import Mapping
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from neural_ai.core.config.interfaces.types import StorageConfig
# ... és még 15 import
```

## Osztály: `FileStorage(StorageInterface)`

Fájlrendszer alapú tárolási implementáció.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', config: 'ConfigInterface | None' = None, event_bus: 'EventBusInterface | None' = None, base_path: str | Path | None = None, hardware: 'HardwareInterface | None' = None) -> None
```

Inicializálja a FileStorage példányt backend selectorral. Hardver detekció alapján kiválasztja a megfelelő tárolási backend-et. Ha AVX2 elérhető, PolarsBackend-et használ, különben PandasBackend-et.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): Logger interfész
- **`config`** (`'ConfigInterface | None'`) = `None`: Konfiguráció interfész
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Eseménybusz interfész
- **`base_path`** (`str | Path | None`) = `None`: Alap könyvtár útvonala
- **`hardware`** (`'HardwareInterface | None'`) = `None`: Hardver interfész (opcionális) **kwargs: További paraméterek

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

#### `_check_disk_space()`

```python
def _check_disk_space(self, file_path: Path, required_bytes: int) -> None
```

Ellenőrzi, hogy van-e elég lemezterület a művelethez.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`): A célfájl útvonala
- **`required_bytes`** (`int`): Szükséges bájtok száma a művelethez

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`InsufficientDiskSpaceError`**: Ha nincs elég lemezterület

#### `_check_permissions()`

```python
def _check_permissions(self, file_path: Path, check_write: bool = True) -> None
```

Ellenőrzi a fájl/könyvtár jogosultságokat.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`): A célfájl útvonala
- **`check_write`** (`bool`) = `True`: Ha True, ellenőrzi az írási jogosultságot is

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`PermissionDeniedError`**: Ha a jogosultságok nem megfelelőek
- **`StorageIOError`**: Ha az útvonal ellenőrzése sikertelen

#### `get_storage_info()`

```python
def get_storage_info(self, directory: str | Path) -> dict[str, Any]
```

Tárolási információk lekérdezése egy könyvtárhoz.

**Paraméterek:**

- **`self`**
- **`directory`** (`str | Path`): Az ellenőrizendő könyvtár útvonala

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Tárolási információk, beleértve a teljes, használt és szabad területet

**Kivételek:**

- **`StorageIOError`**: Ha nem lehet lekérdezni a tárolási információkat

#### `base_path()`

```python
def base_path(self) -> Path
```

A tárolási alapútvonal lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`
- Path: Az alapútvonal

#### `_get_full_path()`

```python
def _get_full_path(self, path: str | Path) -> Path
```

Teljes útvonal előállítása.

**Paraméterek:**

- **`self`**
- **`path`** (`str | Path`): Relatív vagy abszolút útvonal

**Visszatérési érték:**

- Típus: `Path`
- Path: Teljes útvonal

#### `save_dataframe()`

```python
def save_dataframe(self, df: 'pd.DataFrame', path: str) -> None
```

Menti a DataFrame objektumot Parquet formátumban.

**Paraméterek:**

- **`self`**
- **`df`** (`'pd.DataFrame'`): A mentendő DataFrame
- **`path`** (`str`): A mentés útvonala (.parquet kiterjesztéssel) **kwargs: További formátum-specifikus paraméterek (fmt: formátum)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageFormatError`**: Ha a formátum nem parquet
- **`StorageIOError`**: Ha a mentés sikertelen

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> 'pd.DataFrame'
```

Betölti a DataFrame objektumot Parquet formátumból.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A betöltendő fájl útvonala (.parquet kiterjesztéssel) **kwargs: További formátum-specifikus paraméterek (fmt: formátum)

**Visszatérési érték:**

- Típus: `'pd.DataFrame'`
- pd.DataFrame: A betöltött DataFrame

**Kivételek:**

- **`StorageNotFoundError`**: Ha a fájl nem található
- **`StorageFormatError`**: Ha a formátum nem parquet
- **`StorageIOError`**: Ha a betöltés sikertelen

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

Menti a Python objektumot pickle formátumban.

**Paraméterek:**

- **`self`**
- **`obj`** (`object`): A mentendő objektum
- **`path`** (`str`): A mentés útvonala (.pkl kiterjesztéssel) **kwargs: További formátum-specifikus paraméterek (fmt: formátum)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageFormatError`**: Ha a formátum nem pkl
- **`StorageSerializationError`**: Ha az objektum nem szerializálható
- **`StorageIOError`**: Ha a mentés sikertelen

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

Betölti a Python objektumot pickle formátumból.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A betöltendő fájl útvonala (.pkl kiterjesztéssel) **kwargs: További formátum-specifikus paraméterek (fmt: formátum)

**Visszatérési érték:**

- Típus: `object`
- Any: A betöltött objektum

**Kivételek:**

- **`StorageNotFoundError`**: Ha a fájl nem található
- **`StorageFormatError`**: Ha a formátum nem pkl
- **`StorageSerializationError`**: Ha az objektum nem deszerializálható
- **`StorageIOError`**: Ha a betöltés sikertelen

#### `exists()`

```python
def exists(self, path: str) -> bool
```

Ellenőrzi az útvonal létezését.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): Az ellenőrizendő útvonal

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha létezik, False ha nem

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

Lekéri a fájl vagy könyvtár metaadatait.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A fájl vagy könyvtár útvonala

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A metaadatok

**Kivételek:**

- **`StorageNotFoundError`**: Ha a fájl nem található
- **`StorageIOError`**: Ha a lekérés sikertelen

#### `delete()`

```python
def delete(self, path: str) -> None
```

Törli a megadott fájlt vagy könyvtárat.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A törlendő útvonal

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageNotFoundError`**: Ha a fájl nem található
- **`StorageIOError`**: Ha a törlés sikertelen

#### `list_dir()`

```python
def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]
```

Listázza egy könyvtár tartalmát.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A könyvtár útvonala
- **`pattern`** (`str | None`) = `None`: Szűrő minta a fájlnevekre

**Visszatérési érték:**

- Típus: `Sequence[Path]`
- Sequence[Path]: A könyvtár tartalma Path objektumokként

**Kivételek:**

- **`StorageNotFoundError`**: Ha a könyvtár nem található
- **`StorageIOError`**: Ha a listázás sikertelen

---

**Forrásfájl:** [`neural_ai/data/storage/implementations/file_storage.py`](../../neural_ai/data/storage/implementations/file_storage.py)
