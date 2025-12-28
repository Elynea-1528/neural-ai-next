# FileStorage

## Áttekintés

A `FileStorage` osztály fájlrendszer alapú tárolási megoldást nyújt, támogatva a különböző adatformátumokat (CSV, Excel, JSON) és Python objektumokat. Az osztály a [`StorageInterface`](../../interfaces/storage_interface.md) interfészt implementálja.

## Osztály leírás

**Teljes név**: `neural_ai.core.storage.implementations.file_storage.FileStorage`

**Interfész**: `StorageInterface`

## Főbb jellemzők

- **Támogatott DataFrame formátumok**: CSV, Excel
- **Támogatott objektum formátumok**: JSON
- **Atomi írás**: Temp fájllal és átnevezéssel biztosított
- **Jogosultság ellenőrzés**: Olvasási és írási jogosultságok ellenőrzése
- **Lemezterület ellenőrzés**: Szükséges lemezterület ellenőrzése mentés előtt
- **Hibatűrő**: Robusztus hibakezelés IO műveletekhez

## Inicializálás

```python
from neural_ai.core.storage.implementations.file_storage import FileStorage
from pathlib import Path

# Alapértelmezett útvonallal
storage = FileStorage()

# Egyéni útvonallal
storage = FileStorage(base_path="/path/to/data")

# Loggerrel
from neural_ai.core.logger.factory import LoggerFactory
logger = LoggerFactory.get_logger()
storage = FileStorage(base_path="/data", logger=logger)
```

**Paraméterek:**
- `base_path`: Alap könyvtár útvonala (alapértelmezett: aktuális könyvtár)
- `logger`: Logger példány (opcionális)
- `**kwargs`: További paraméterek (figyelmen kívül hagyva)

## Metódusok

### Adatmentés és betöltés

#### `save_dataframe()`

DataFrame mentése különböző formátumokban.

```python
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: str,
    fmt: str | None = None,
    **kwargs: Any,
) -> None
```

**Példák:**

```python
import pandas as pd

df = pd.DataFrame({'id': [1, 2, 3], 'name': ['a', 'b', 'c']})

# CSV mentés
storage.save_dataframe(df, "data.csv")

# Excel mentés
storage.save_dataframe(df, "data.xlsx")

# Egyéni paraméterekkel
storage.save_dataframe(df, "data.csv", sep=';', index=False)
```

#### `load_dataframe()`

DataFrame betöltése fájlból.

```python
def load_dataframe(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any,
) -> pd.DataFrame
```

**Példák:**

```python
# CSV betöltés
df = storage.load_dataframe("data.csv")

# Excel betöltés
df = storage.load_dataframe("data.xlsx")

# Oszlopok szűrése
df = storage.load_dataframe("data.csv", usecols=['id', 'name'])
```

#### `save_object()`

Python objektum mentése JSON formátumban.

```python
def save_object(
    self,
    obj: Any,
    path: str,
    fmt: str | None = None,
    **kwargs: Any,
) -> None
```

**Példák:**

```python
# Szótár mentése
config = {'key': 'value', 'number': 42}
storage.save_object(config, "config.json")

# Lista mentése
data = [1, 2, 3, 4, 5]
storage.save_object(data, "data.json")

# Egyéni formázással
storage.save_object(config, "config.json", indent=2)
```

#### `load_object()`

Python objektum betöltése JSON fájlból.

```python
def load_object(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any,
) -> Any
```

**Példák:**

```python
# Objektum betöltése
config = storage.load_object("config.json")
data = storage.load_object("data.json")
```

### Fájlműveletek

#### `exists()`

Ellenőrzi, hogy egy fájl vagy könyvtár létezik-e.

```python
def exists(self, path: str) -> bool
```

**Példa:**
```python
if storage.exists("data.csv"):
    print("A fájl létezik")
```

#### `get_metadata()`

Fájl vagy könyvtár metaadatainak lekérdezése.

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

**Visszatérési érték:**
```python
{
    'size': 1024,  # Fájlméret bájtban
    'created': datetime(...),  # Létrehozás ideje
    'modified': datetime(...),  # Módosítás ideje
    'accessed': datetime(...),  # Utolsó hozzáférés ideje
    'is_file': True,  # Fájl-e
    'is_dir': False   # Könyvtár-e
}
```

**Példa:**
```python
metadata = storage.get_metadata("data.csv")
print(f"Méret: {metadata['size']} bájt")
print(f"Létrehozva: {metadata['created']}")
```

#### `delete()`

Fájl vagy üres könyvtár törlése.

```python
def delete(self, path: str) -> None
```

**Példa:**
```python
storage.delete("temp.csv")
```

#### `list_dir()`

Könyvtár tartalmának listázása.

```python
def list_dir(
    self,
    path: str,
    pattern: str | None = None,
) -> Sequence[Path]
```

**Példák:**

```python
# Összes fájl listázása
files = storage.list_dir("data")

# Csak CSV fájlok
csv_files = storage.list_dir("data", pattern="*.csv")

# Minden fájl és alkönyvtár
all_items = storage.list_dir("data", pattern="*")
```

### Tároló információk

#### `get_storage_info()`

Tároló információk lekérdezése (összes, használt és szabad terület).

```python
def get_storage_info(self, directory: str | Path) -> dict[str, Any]
```

**Visszatérési érték:**
```python
{
    'total_space_gb': 500.0,    # Összes terület GB-ban
    'used_space_gb': 250.0,     # Használt terület GB-ban
    'free_space_gb': 250.0,     # Szabad terület GB-ban
    'free_space_percent': 50.0  # Szabad terület százalékban
}
```

**Példa:**
```python
info = storage.get_storage_info("/data")
print(f"Szabad terület: {info['free_space_gb']:.2f} GB")
```

## Hibakezelés

A `FileStorage` robusztus hibakezelést valósít meg:

### Kivételek

- **`StorageNotFoundError`**: Fájl vagy könyvtár nem található
- **`StorageFormatError`**: Nem támogatott formátum
- **`StorageIOError`**: IO művelet sikertelen
- **`StorageSerializationError`**: Szerializációs hiba
- **`InsufficientDiskSpaceError`**: Nincs elég lemezterület
- **`PermissionDeniedError`**: Nincs megfelelő jogosultság

### Példa hibakezelésre

```python
from neural_ai.core.storage.exceptions import (
    StorageNotFoundError,
    StorageIOError
)

try:
    df = storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError as e:
    print(f"Fájl nem található: {e}")
except StorageIOError as e:
    print(f"IO hiba: {e}")
```

## Belső működés

### Formátum kezelők

A `FileStorage` dinamikusan regisztrálja a formátum kezelőket:

- **DataFrame formátumok**: CSV, Excel
- **Objektum formátumok**: JSON

Minden formátumhoz tartozik egy `save` és egy `load` függvény.

### Atomi írás

A mentési műveletek atomiak, temp fájl használatával:

1. Tartalom írása temp fájlba
2. Temp fájl átnevezése a célfájl névre
3. Ha bármilyen hiba történik, a temp fájl törlődik

### Biztonsági ellenőrzések

- **Jogosultság ellenőrzés**: Olvasási/írási jogosultságok ellenőrzése
- **Lemezterület ellenőrzés**: Szükséges terület ellenőrzése (10% pufferrel)
- **Útvonal ellenőrzés**: Relatív és abszolút útvonalak kezelése

## Teljesítmény

- **Gyorsítás**: Formátum-specifikus optimalizációk
- **Memóriakezelés**: Hatékony DataFrame kezelés
- **Párhuzamosság**: Biztonságos több szálból való használatra

## Tesztelés

A `FileStorage`-t a [`tests/core/storage/implementations/test_file_storage.py`](../../../tests/core/storage/implementations/test_file_storage.py) teszteli, amely lefedi:

- Alapvető mentési és betöltési műveletek
- Hibakezelés és érvényesítés
- Formátum specifikus műveletek
- Fájlműveletek (létezés, metaadatok, törlés, listázás)
- Biztonsági ellenőrzések
- Tároló információk lekérdezése