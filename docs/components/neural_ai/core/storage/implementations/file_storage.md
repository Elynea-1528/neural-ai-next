# FileStorage

A `FileStorage` osztály a fájlrendszer alapú tárolási megoldás implementációja a Neural AI Next projektben. Ez az osztály biztosítja a DataFrame-ek és Python objektumok perzisztens tárolását különböző formátumokban (CSV, Excel, JSON).

## Osztály áttekintése

```python
class FileStorage(StorageInterface):
    """Fájlrendszer alapú storage implementáció."""
```

## Konstruktor

### `__init__`

```python
def __init__(
    self,
    base_path: str | Path | None = None,
    logger: Optional["LoggerInterface"] = None
) -> None
```

Inicializálja a FileStorage példányt.

**Paraméterek:**

- `base_path` (str | Path | None): Az alap könyvtár útvonala, ahol a fájlok tárolódnak. Ha None, akkor a jelenlegi munkakönyvtárat használja.
- `logger` (Optional[LoggerInterface]): Logger példány a naplózáshoz. Opcionális, ha nincs megadva, akkor a műveletek nem lesznek naplózva.

**Kivételek:**

- `StorageIOError`: Ha az alap könyvtár nem hozható létre vagy nem írható.

## Metódusok

### DataFrame Műveletek

#### `save_dataframe`

```python
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> None
```

Menti a DataFrame objektumot a megadott formátumban.

**Paraméterek:**

- `df` (pd.DataFrame): A mentendő DataFrame
- `path` (str): A mentés útvonala
- `fmt` (str | None): A mentés formátuma (csv, excel). Ha None, akkor a kiterjesztésből határozza meg.
- `**kwargs`: További formátum-specifikus paraméterek

**Kivételek:**

- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageIOError`: Ha a mentés sikertelen

**Példa:**

```python
storage = FileStorage()
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
storage.save_dataframe(df, "data.csv")
```

#### `load_dataframe`

```python
def load_dataframe(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> pd.DataFrame
```

Betölti a DataFrame objektumot a fájlból.

**Paraméterek:**

- `path` (str): A betöltendő fájl útvonala
- `fmt` (str | None): A fájl formátuma (csv, excel). Ha None, akkor a kiterjesztésből határozza meg.
- `**kwargs`: További formátum-specifikus paraméterek

**Visszatérési érték:**

- `pd.DataFrame`: A betöltött DataFrame

**Kivételek:**

- `StorageNotFoundError`: Ha a fájl nem található
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageIOError`: Ha a betöltés sikertelen
- `PermissionDeniedError`: Ha nincs olvasási jogosultság

**Példa:**

```python
storage = FileStorage()
df = storage.load_dataframe("data.csv")
```

### Objektum Műveletek

#### `save_object`

```python
def save_object(
    self,
    obj: Any,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> None
```

Menti a Python objektumot JSON formátumban.

**Paraméterek:**

- `obj` (Any): A mentendő objektum
- `path` (str): A mentés útvonala
- `fmt` (str | None): A mentés formátuma (jelenleg csak json támogatott)
- `**kwargs`: További formátum-specifikus paraméterek

**Kivételek:**

- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageSerializationError`: Ha az objektum nem szerializálható
- `StorageIOError`: Ha a mentés sikertelen

**Példa:**

```python
storage = FileStorage()
data = {"key": "value", "number": 42}
storage.save_object(data, "config.json")
```

#### `load_object`

```python
def load_object(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> Any
```

Betölti a Python objektumot a fájlból.

**Paraméterek:**

- `path` (str): A betöltendő fájl útvonala
- `fmt` (str | None): A fájl formátuma (jelenleg csak json támogatott)
- `**kwargs`: További formátum-specifikus paraméterek

**Visszatérési érték:**

- `Any`: A betöltött objektum

**Kivételek:**

- `StorageNotFoundError`: Ha a fájl nem található
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageSerializationError`: Ha az objektum nem deszerializálható
- `StorageIOError`: Ha a betöltés sikertelen
- `PermissionDeniedError`: Ha nincs olvasási jogosultság

**Példa:**

```python
storage = FileStorage()
data = storage.load_object("config.json")
```

### Fájl Műveletek

#### `exists`

```python
def exists(self, path: str) -> bool
```

Ellenőrzi, hogy az útvonal létezik-e.

**Paraméterek:**

- `path` (str): Az ellenőrizendő útvonal

**Visszatérési érték:**

- `bool`: True, ha létezik, False ha nem

#### `get_metadata`

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

Lekéri a fájl vagy könyvtár metaadatait.

**Paraméterek:**

- `path` (str): A fájl vagy könyvtár útvonala

**Visszatérési érték:**

- `dict[str, Any]`: A metaadatok (size, created, modified, accessed, is_file, is_dir)

**Kivételek:**

- `StorageNotFoundError`: Ha a fájl nem található
- `StorageIOError`: Ha a lekérés sikertelen

#### `delete`

```python
def delete(self, path: str) -> None
```

Törli a megadott fájlt vagy könyvtárat.

**Paraméterek:**

- `path` (str): A törlendő útvonal

**Kivételek:**

- `StorageNotFoundError`: Ha a fájl nem található
- `StorageIOError`: Ha a törlés sikertelen

#### `list_dir`

```python
def list_dir(
    self,
    path: str,
    pattern: str | None = None
) -> Sequence[Path]
```

Listázza egy könyvtár tartalmát.

**Paraméterek:**

- `path` (str): A könyvtár útvonala
- `pattern` (str | None): Szűrő minta a fájlnevekre (pl. "*.csv")

**Visszatérési érték:**

- `Sequence[Path]`: A könyvtár tartalma Path objektumokként

**Kivételek:**

- `StorageNotFoundError`: Ha a könyvtár nem található
- `StorageIOError`: Ha a listázás sikertelen

### Tárhely Információ

#### `get_storage_info`

```python
def get_storage_info(self, directory: str | Path) -> dict[str, Any]
```

Lekéri a tárhely információkat egy könyvtárhoz.

**Paraméterek:**

- `directory` (str | Path): A könyvtár útvonala

**Visszatérési érték:**

- `dict[str, Any]`: Tárhely információk (total_space_gb, used_space_gb, free_space_gb, free_space_percent)

**Kivételek:**

- `StorageIOError`: Ha az információk lekérése sikertelen

## Támogatott Formátumok

### DataFrame Formátumok

- **CSV** (.csv): Comma-separated values
- **Excel** (.xlsx, .xls): Microsoft Excel formátum

### Objektum Formátumok

- **JSON** (.json): JavaScript Object Notation

## Dependency Injection

A `FileStorage` osztály támogatja a függőség injektálást a logger komponens esetében:

```python
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.storage.implementations.file_storage import FileStorage

# Logger létrehozása
logger = DefaultLogger(name="StorageLogger")

# FileStorage létrehozása loggerrel
storage = FileStorage(base_path="/path/to/storage", logger=logger)
```

Ha nincs logger megadva, a műveletek nem lesznek naplózva, de az osztály továbbra is működik.

## Hibakezelés

A `FileStorage` osztály átfogó hibakezelést biztosít:

- **StorageNotFoundError**: A kért fájl vagy könyvtár nem található
- **StorageFormatError**: Nem támogatott fájlformátum
- **StorageIOError**: I/O hiba történt (pl. lemez hiba, hozzáférés megtagadva)
- **StorageSerializationError**: Az objektum nem szerializálható/deszerializálható
- **PermissionDeniedError**: Nincs megfelelő jogosultság a művelethez

## Teljesítmény és Biztonság

- **Atomi írás**: A fájlok atomi módon kerülnek mentésre temp fájl használatával
- **Lemezterület ellenőrzés**: A mentés előtt ellenőrzi a szükséges lemezterületet
- **Jogosultság ellenőrzés**: Ellenőrzi az olvasási/írási jogosultságokat
- **Kivétel láncolás**: A hibák megfelelően láncolva vannak (`raise ... from e`)

## Példa Használat

```python
import pandas as pd
from neural_ai.core.storage.implementations.file_storage import FileStorage

# FileStorage létrehozása
storage = FileStorage(base_path="./data")

# DataFrame mentése
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "London", "Tokyo"]
})
storage.save_dataframe(df, "users.csv")

# DataFrame betöltése
loaded_df = storage.load_dataframe("users.csv")
print(loaded_df)

# Objektum mentése
config = {
    "database": {"host": "localhost", "port": 5432},
    "logging": {"level": "INFO"}
}
storage.save_object(config, "config.json")

# Objektum betöltése
loaded_config = storage.load_object("config.json")
print(loaded_config)

# Fájl információk lekérése
if storage.exists("users.csv"):
    metadata = storage.get_metadata("users.csv")
    print(f"File size: {metadata['size']} bytes")

# Könyvtár listázása
files = storage.list_dir(".", pattern="*.csv")
print(f"CSV files: {[f.name for f in files]}")

# Tárhely információk
info = storage.get_storage_info(".")
print(f"Free space: {info['free_space_gb']:.2f} GB")
```

## Kapcsolódó Dokumentáció

- [Storage Interface](../interfaces/storage_interface.md)
- [Storage Exceptions](../exceptions.md)
- [Core Dependencies](../../../development/core_dependencies.md)