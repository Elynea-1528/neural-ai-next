# FileStorage

## Áttekintés

A `FileStorage` egy fájlrendszer alapú tárolási implementáció, amely a `StorageInterface`-t valósítja meg. Ez az osztály felelős a DataFrame-ek és általános Python objektumok fájlrendszerben történő tárolásáért, betöltéséért és kezeléséért.

## Osztály

```python
class FileStorage(StorageInterface)
```

## Inicializálás

```python
def __init__(
    self,
    base_path: str | Path | None = None,
    logger: Optional[LoggerInterface] = None
) -> None
```

**Paraméterek:**
- `base_path`: Alap könyvtár útvonala (alapértelmezett: aktuális munkakönyvtár)
- `logger`: Logger példány (opcionális)

**Példa:**

```python
from neural_ai.core.storage import FileStorage
from neural_ai.core.logger import LoggerFactory

# Alapértelmezett inicializálás
storage = FileStorage()

# Egyéni útvonallal
storage = FileStorage(base_path="/data/storage")

# Loggerrel
logger = LoggerFactory.get_logger("file_storage")
storage = FileStorage(base_path="/data", logger=logger)
```

## Támogatott Formátumok

### DataFrame Formátumok
- **CSV** (`.csv`)
- **Excel** (`.xlsx`, `.xls`)

### Objektum Formátumok
- **JSON** (`.json`)

## Metódusok

### `save_dataframe()`

DataFrame mentése a megadott útvonalra.

```python
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> None
```

**Paraméterek:**
- `df`: A mentendő DataFrame
- `path`: A mentés útvonala
- `fmt`: A mentés formátuma (ha None, akkor a kiterjesztésből)
- `**kwargs`: További formátum-specifikus paraméterek

**Kivételek:**
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageIOError`: Ha a mentés sikertelen
- `InsufficientDiskSpaceError`: Ha nincs elég lemezterület
- `PermissionDeniedError`: Ha nincs írási jogosultság

**Példák:**

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Budapest", "Debrecen", "Szeged"]
})

# CSV mentés
storage.save_dataframe(df, "users.csv")

# Excel mentés index nélkül
storage.save_dataframe(df, "users.xlsx", index=False)

# CSV mentés egyéni elválasztóval
storage.save_dataframe(df, "users.csv", sep=";")
```

### `load_dataframe()`

DataFrame betöltése a megadott útvonalról.

```python
def load_dataframe(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> pd.DataFrame
```

**Paraméterek:**
- `path`: A betöltendő fájl útvonala
- `fmt`: A fájl formátuma (ha None, akkor a kiterjesztésből)
- `**kwargs`: További formátum-specifikus paraméterek

**Visszatérési érték:**
- `pd.DataFrame`: A betöltött DataFrame

**Kivételek:**
- `StorageNotFoundError`: Ha a fájl nem található
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageIOError`: Ha a betöltés sikertelen
- `PermissionDeniedError`: Ha nincs olvasási jogosultság

**Példák:**

```python
# Egyszerű betöltés
df = storage.load_dataframe("users.csv")

# Betöltés csak bizonyos oszlopokkal
df = storage.load_dataframe("users.csv", usecols=["name", "age"])

# Excel betöltés adott munkalapról
df = storage.load_dataframe("users.xlsx", sheet_name="Sheet1")

# CSV betöltés egyéni elválasztóval
df = storage.load_dataframe("users.csv", sep=";")
```

### `save_object()`

Python objektum mentése a megadott útvonalra.

```python
def save_object(
    self,
    obj: Any,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> None
```

**Paraméterek:**
- `obj`: A mentendő objektum
- `path`: A mentés útvonala
- `fmt`: A mentés formátuma (ha None, akkor a kiterjesztésből)
- `**kwargs`: További formátum-specifikus paraméterek

**Kivételek:**
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageSerializationError`: Ha az objektum nem szerializálható
- `StorageIOError`: Ha a mentés sikertelen
- `InsufficientDiskSpaceError`: Ha nincs elég lemezterület
- `PermissionDeniedError`: Ha nincs írási jogosultság

**Példák:**

```python
# Szótár mentése
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "user": "admin"
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}
storage.save_object(config, "config.json")

# Lista mentése
data = [1, 2, 3, 4, 5]
storage.save_object(data, "numbers.json")

# JSON mentés indentálással
storage.save_object(config, "config.json", indent=4)
```

### `load_object()`

Python objektum betöltése a megadott útvonalról.

```python
def load_object(
    self,
    path: str,
    fmt: str | None = None,
    **kwargs: Any
) -> Any
```

**Paraméterek:**
- `path`: A betöltendő fájl útvonala
- `fmt`: A fájl formátuma (ha None, akkor a kiterjesztésből)
- `**kwargs`: További formátum-specifikus paraméterek

**Visszatérési érték:**
- `Any`: A betöltött objektum

**Kivételek:**
- `StorageNotFoundError`: Ha a fájl nem található
- `StorageFormatError`: Ha a formátum nem támogatott
- `StorageSerializationError`: Ha az objektum nem deszerializálható
- `StorageIOError`: Ha a betöltés sikertelen
- `PermissionDeniedError`: Ha nincs olvasási jogosultság

**Példák:**

```python
# Konfiguráció betöltése
config = storage.load_object("config.json")

# Adatok betöltése
data = storage.load_object("numbers.json")

# JSON betöltés egyéni dekóderrel
import json
def custom_decoder(dct):
    # Egyéni dekódolási logika
    return dct

config = storage.load_object("config.json", object_hook=custom_decoder)
```

### `exists()`

Ellenőrzi az útvonal létezését.

```python
def exists(self, path: str) -> bool
```

**Paraméterek:**
- `path`: Az ellenőrizendő útvonal

**Visszatérési érték:**
- `bool`: True, ha létezik, False ha nem

**Példa:**

```python
if storage.exists("data.csv"):
    df = storage.load_dataframe("data.csv")
else:
    df = create_default_dataframe()
    storage.save_dataframe(df, "data.csv")
```

### `get_metadata()`

Lekéri a fájl vagy könyvtár metaadatait.

```python
def get_metadata(self, path: str) -> dict[str, Any]
```

**Paraméterek:**
- `path`: A fájl vagy könyvtár útvonala

**Visszatérési érték:**
- `dict[str, Any]`: A metaadatok szótárba rendezve

**Metaadatok:**
- `size`: Fájlméret bájtban
- `created`: Létrehozás dátuma
- `modified`: Módosítás dátuma
- `accessed`: Utolsó hozzáférés dátuma
- `is_file`: True, ha fájl
- `is_dir`: True, ha könyvtár

**Kivételek:**
- `StorageNotFoundError`: Ha a fájl nem található
- `StorageIOError`: Ha a lekérés sikertelen

**Példa:**

```python
metadata = storage.get_metadata("data.csv")
print(f"Méret: {metadata['size']} bájt")
print(f"Létrehozva: {metadata['created']}")
print(f"Módosítva: {metadata['modified']}")
```

### `delete()`

Törli a megadott fájlt vagy könyvtárat.

```python
def delete(self, path: str) -> None
```

**Paraméterek:**
- `path`: A törlendő útvonal

**Kivételek:**
- `StorageNotFoundError`: Ha a fájl nem található
- `StorageIOError`: Ha a törlés sikertelen

**Példa:**

```python
# Fájl törlése
storage.delete("old_data.csv")

# Csak üres könyvtárak törölhetők
storage.delete("empty_directory")
```

### `list_dir()`

Listázza egy könyvtár tartalmát.

```python
def list_dir(
    self,
    path: str,
    pattern: str | None = None
) -> Sequence[Path]
```

**Paraméterek:**
- `path`: A könyvtár útvonala
- `pattern`: Szűrő minta a fájlnevekre (pl. "*.csv")

**Visszatérési érték:**
- `Sequence[Path]`: A könyvtár tartalma Path objektumokként

**Kivételek:**
- `StorageNotFoundError`: Ha a könyvtár nem található
- `StorageIOError`: Ha a listázás sikertelen

**Példák:**

```python
# Összes fájl listázása
files = storage.list_dir("/data")
for file in files:
    print(file)

# Csak CSV fájlok listázása
csv_files = storage.list_dir("/data", pattern="*.csv")

# Rekurzív keresés
all_files = storage.list_dir("/data", pattern="**/*.csv")
```

### `get_storage_info()`

Lekéri a tárolási információkat egy könyvtárhoz.

```python
def get_storage_info(self, directory: str | Path) -> dict[str, Any]
```

**Paraméterek:**
- `directory`: A könyvtár útvonala

**Visszatérési érték:**
- `dict[str, Any]`: Tárolási információk

**Információk:**
- `total_space_gb`: Teljes lemezterület GB-ban
- `used_space_gb`: Használt terület GB-ban
- `free_space_gb`: Szabad terület GB-ban
- `free_space_percent`: Szabad terület százalékban

**Kivételek:**
- `StorageIOError`: Ha az információk lekérése sikertelen

**Példa:**

```python
info = storage.get_storage_info("/data")
print(f"Teljes terület: {info['total_space_gb']:.2f} GB")
print(f"Szabad terület: {info['free_space_gb']:.2f} GB")
print(f"Szabad terület: {info['free_space_percent']:.1f}%")
```

## Belső Metódusok

### `_setup_format_handlers()`

Beállítja a formátum kezelőket. Ez a metódus automatikusan meghívódik az inicializáláskor.

### `_check_disk_space()`

Ellenőrzi, hogy van-e elég lemezterület a művelethez.

```python
def _check_disk_space(self, file_path: Path, required_bytes: int) -> None
```

**Kivételek:**
- `InsufficientDiskSpaceError`: Ha nincs elég lemezterület
- `StorageIOError`: Ha a lemezterület ellenőrzése sikertelen

### `_check_permissions()`

Ellenőrzi a fájl/könyvtár jogosultságokat.

```python
def _check_permissions(self, file_path: Path, check_write: bool = True) -> None
```

**Kivételek:**
- `PermissionDeniedError`: Ha a jogosultságok nem megfelelőek
- `StorageIOError`: Ha az útvonal ellenőrzése sikertelen

### `_get_full_path()`

Teljes útvonal előállítása.

```python
def _get_full_path(self, path: str | Path) -> Path
```

### `_atomic_write()`

Atomi fájlírás temp fájllal és átnevezéssel.

```python
def _atomic_write(
    self,
    file_path: Path,
    content: str | bytes | Any,
    mode: str = "w",
    fmt: str = "json",
    **kwargs: Any
) -> None
```

## Komplex Példák

### Adatok mentése és betöltése

```python
import pandas as pd
from neural_ai.core.storage import FileStorage

# Inicializálás
storage = FileStorage(base_path="/data")

# DataFrame létrehozása
df = pd.DataFrame({
    "timestamp": pd.date_range("2023-01-01", periods=100, freq="H"),
    "value": range(100),
    "category": ["A", "B", "C"] * 33 + ["A"]
})

# Mentés különböző formátumokban
storage.save_dataframe(df, "data.csv")
storage.save_dataframe(df, "data.xlsx")
storage.save_dataframe(df, "data.csv", index=False, sep=";")

# Betöltés
df_csv = storage.load_dataframe("data.csv")
df_excel = storage.load_dataframe("data.xlsx")

# Konfiguráció mentése
config = {
    "version": "1.0",
    "settings": {
        "debug": True,
        "timeout": 30
    }
}
storage.save_object(config, "config.json", indent=2)

# Konfiguráció betöltése
loaded_config = storage.load_object("config.json")
```

### Hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageNotFoundError,
    StorageIOError,
    StorageFormatError
)

try:
    df = storage.load_dataframe("missing.csv")
except StorageNotFoundError:
    print("A fájl nem található, létrehozzuk az alapértelmezett adatokat")
    df = create_default_dataframe()
    storage.save_dataframe(df, "missing.csv")
except StorageIOError as e:
    print(f"IO hiba: {e}")
    # Próbáljuk meg újra
    time.sleep(1)
    df = storage.load_dataframe("missing.csv")
except StorageFormatError as e:
    print(f"Formátum hiba: {e}")
    # Konvertálás más formátumra
    convert_file("missing.csv", "missing_fixed.csv")
    df = storage.load_dataframe("missing_fixed.csv")
```

### Fájlkezelés

```python
# Fájl létezés ellenőrzése
if storage.exists("data.csv"):
    # Metaadatok lekérése
    metadata = storage.get_metadata("data.csv")
    print(f"Fájlméret: {metadata['size']} bájt")
    
    # Fájl törlése
    if metadata['size'] > 1000000:  # 1MB
        storage.delete("data.csv")
        print("A fájl törölve lett")

# Könyvtár tartalmának listázása
files = storage.list_dir("/data", pattern="*.csv")
print(f"CSV fájlok: {len(files)} db")

# Tárolási információk
info = storage.get_storage_info("/data")
if info['free_space_percent'] < 10:
    print("Figyelmeztetés: Kevés a szabad lemezterület!")
```

## Best Practices

1. **Relatív útvonalak**: Használjunk relatív útvonalakat a `base_path`-hoz képest
2. **Formátum megadása**: Mindig adjuk meg a formátumot, ha nem egyértelmű
3. **Hibakezelés**: Kezeljük a lehetséges kivételeket
4. **Metaadatok**: Használjuk a `get_metadata()` metódust a fájl információk lekéréséhez
5. **Tároló állapot**: Ellenőrizzük a szabad lemezterületet nagy fájlok írása előtt
