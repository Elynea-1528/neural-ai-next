# neural_ai/data/storage/interfaces/storage_interface.py

Tárolási interfész modul.

Ez a modul definiálja a tárolási műveletek absztrakt interfészét,
amelyet minden konkrét tárolási implementációnak implementálnia kell.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from collections.abc import Mapping
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
import pandas
```

## Osztály: `StorageInterface(ABC)`

Absztrakt interfész tárolási műveletek definiálásához.

Ez az interfész biztosítja a standardizált tárolási műveleteket
DataFrame-ekkel és általános objektumokkal való munkavégzéshez.

### Metódusok

#### `save_dataframe()`

```python
def save_dataframe(self, df: pd.DataFrame, path: str) -> None
```

DataFrame mentése a megadott útvonalra.

**Paraméterek:**

- **`self`**
- **`df`** (`pd.DataFrame`): A mentendő pandas DataFrame.
- **`path`** (`str`): A célfájl elérési útja. **kwargs: További formázási és mentési opciók.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageIOError`**: Ha I/O hiba történik a mentés során.
- **`StorageFormatError`**: Ha a kért formátum nem támogatott.
- **`StorageSerializationError`**: Ha az adatok nem szerializálhatók.

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> pd.DataFrame
```

DataFrame betöltése a megadott útvonalról.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrásfájl elérési útja. **kwargs: További betöltési és formázási opciók.

**Visszatérési érték:**

- Típus: `pd.DataFrame`
- A betöltött pandas DataFrame.

**Kivételek:**

- **`StorageNotFoundError`**: Ha a forrásfájl nem található.
- **`StorageFormatError`**: Ha a fájl formátuma nem támogatott.
- **`StorageSerializationError`**: Ha az adatok nem deszerializálhatók.
- **`StorageIOError`**: Ha I/O hiba történik a betöltés során.

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

Objektum mentése a megadott útvonalra.

**Paraméterek:**

- **`self`**
- **`obj`** (`object`): A mentendő objektum.
- **`path`** (`str`): A célfájl elérési útja. **kwargs: További szerializációs opciók.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageIOError`**: Ha I/O hiba történik a mentés során.
- **`StorageFormatError`**: Ha a kért formátum nem támogatott.
- **`StorageSerializationError`**: Ha az objektum nem szerializálható.

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

Objektum betöltése a megadott útvonalról.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A forrásfájl elérési útja. **kwargs: További deszerializációs opciók.

**Visszatérési érték:**

- Típus: `object`
- A betöltött objektum.

**Kivételek:**

- **`StorageNotFoundError`**: Ha a forrásfájl nem található.
- **`StorageFormatError`**: Ha a fájl formátuma nem támogatott.
- **`StorageSerializationError`**: Ha az objektum nem deszerializálható.
- **`StorageIOError`**: Ha I/O hiba történik a betöltés során.

#### `exists()`

```python
def exists(self, path: str) -> bool
```

Ellenőrzi, hogy az útvonal létezik-e.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): Az ellenőrizendő útvonal.

**Visszatérési érték:**

- Típus: `bool`
- True, ha az útvonal létezik, egyébként False.

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

Fájl vagy könyvtár metaadatainak lekérdezése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A cél útvonal.

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A metaadatok szótárba rendezve.

**Kivételek:**

- **`StorageNotFoundError`**: Ha az útvonal nem található.
- **`StorageIOError`**: Ha a metaadatok lekérdezése sikertelen.

#### `delete()`

```python
def delete(self, path: str) -> None
```

Fájl vagy könyvtár törlése.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A törlendő útvonal.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`StorageNotFoundError`**: Ha az útvonal nem található.
- **`StorageIOError`**: Ha a törlés sikertelen.

#### `list_dir()`

```python
def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]
```

Könyvtár tartalmának listázása.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A könyvtár elérési útja.
- **`pattern`** (`str | None`) = `None`: Opcionális glob minta a fájlnevek szűrésére.

**Visszatérési érték:**

- Típus: `Sequence[Path]`
- A könyvtárban található elemek Path objektumokként.

**Kivételek:**

- **`StorageNotFoundError`**: Ha a könyvtár nem található.
- **`StorageIOError`**: Ha a listázás sikertelen.

---

**Forrásfájl:** [`neural_ai/data/storage/interfaces/storage_interface.py`](../../neural_ai/data/storage/interfaces/storage_interface.py)
