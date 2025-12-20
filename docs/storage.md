# Storage Komponens Dokumentáció

## 1. Áttekintés

A storage komponens a Neural AI Next rendszer fájl alapú adattárolási rétegét biztosítja. Ez a komponens felelős a strukturált adatok (DataFrame-ek) és általános Python objektumok tartós tárolásáért, betöltéséért és kezeléséért.

### 1.1 Cél és szerep

A komponens fő céljai:
- **DataFrame kezelés**: Pandas DataFrame-ek mentése és betöltése CSV, Excel formátumokban
- **Objektum tárolás**: Python objektumok JSON formátumban történő szerializálása és deszerializálása
- **Fájlműveletek**: Létezés ellenőrzés, metaadatok lekérése, törlés, könyvtárlistázás
- **Biztonságos írás**: Atomi fájlírás temp fájllal és átnevezéssel
- **Erőforrás ellenőrzés**: Lemezterület és jogosultság ellenőrzések

### 1.2 Fájlok listája

A komponens 8 Python fájlból áll:

1. [`neural_ai/core/storage/__init__.py`](neural_ai/core/storage/__init__.py:1) - Modul inicializálás
2. [`neural_ai/core/storage/exceptions.py`](neural_ai/core/storage/exceptions.py:1) - Kivétel osztályok
3. [`neural_ai/core/storage/interfaces/__init__.py`](neural_ai/core/storage/interfaces/__init__.py:1) - Interfészek export
4. [`neural_ai/core/storage/interfaces/storage_interface.py`](neural_ai/core/storage/interfaces/storage_interface.py:1) - Storage interfész
5. [`neural_ai/core/storage/interfaces/factory_interface.py`](neural_ai/core/storage/interfaces/factory_interface.py:1) - Factory interfész
6. [`neural_ai/core/storage/implementations/__init__.py`](neural_ai/core/storage/implementations/__init__.py:1) - Implementációk export
7. [`neural_ai/core/storage/implementations/file_storage.py`](neural_ai/core/storage/implementations/file_storage.py:1) - FileStorage implementáció
8. [`neural_ai/core/storage/implementations/storage_factory.py`](neural_ai/core/storage/implementations/storage_factory.py:1) - StorageFactory implementáció

### 1.3 Architektúra

A komponens **interfész-alapú architektúrát** követ:
- **Interfészek** definiálják a szerződéseket
- **Implementációk** biztosítják a konkrét funkcionalitást
- **Factory mintázat** lehetővé teszi a különböző storage típusok egységes létrehozását
- **Kivételek** részletes hibakezelést biztosítanak

## 2. Fájlstruktúra

```
neural_ai/core/storage/
├── __init__.py
├── exceptions.py
├── implementations/
│   ├── __init__.py
│   ├── file_storage.py
│   └── storage_factory.py
└── interfaces/
    ├── __init__.py
    ├── factory_interface.py
    └── storage_interface.py
```

## 3. Főbb komponensek és logikájuk

### 3.1 Interfészek

#### StorageInterface

A [`neural_ai/core/storage/interfaces/storage_interface.py:1`](neural_ai/core/storage/interfaces/storage_interface.py:1) fájl definiálja a storage műveletek absztrakt interfészét.

**Metódusok:**

| Metódus          | Leírás                         | Visszatérési érték | Kivételek                                                                           |
| ---------------- | ------------------------------ | ------------------ | ----------------------------------------------------------------------------------- |
| `save_dataframe` | DataFrame mentése              | `None`             | StorageIOError, StorageFormatError, StorageSerializationError                       |
| `load_dataframe` | DataFrame betöltése            | `pd.DataFrame`     | StorageNotFoundError, StorageFormatError, StorageSerializationError, StorageIOError |
| `save_object`    | Objektum mentése               | `None`             | StorageIOError, StorageFormatError, StorageSerializationError                       |
| `load_object`    | Objektum betöltése             | `Any`              | StorageNotFoundError, StorageFormatError, StorageSerializationError, StorageIOError |
| `exists`         | Útvonal létezés ellenőrzés     | `bool`             | -                                                                                   |
| `get_metadata`   | Metaadatok lekérése            | `Dict[str, Any]`   | StorageNotFoundError, StorageIOError                                                |
| `delete`         | Fájl/könyvtár törlése          | `None`             | StorageNotFoundError, StorageIOError                                                |
| `list_dir`       | Könyvtár tartalmának listázása | `Sequence[Path]`   | StorageNotFoundError, StorageIOError                                                |

**Típusok:**
- `pd.DataFrame` - Pandas DataFrame típus
- `pathlib.Path` - Fájlútvonal kezelés
- `typing.Any` - Tetszőleges Python objektum
- `typing.Dict[str, Any]` - Szótár típus
- `typing.Sequence[Path]` - Path objektumok sorozata

#### FactoryInterface

A [`neural_ai/core/storage/interfaces/factory_interface.py:1`](neural_ai/core/storage/interfaces/factory_interface.py:1) fájl definiálja a factory mintázat interfészét.

**Metódusok:**

| Metódus            | Leírás                         | Paraméterek                                                                   |
| ------------------ | ------------------------------ | ----------------------------------------------------------------------------- |
| `register_storage` | Új storage típus regisztrálása | `storage_type: str`, `storage_class: Type[StorageInterface]`                  |
| `get_storage`      | Storage példány létrehozása    | `storage_type: str`, `base_path: Optional[Union[str, Path]]`, `**kwargs: Any` |

### 3.2 Implementációk

#### FileStorage

A [`neural_ai/core/storage/implementations/file_storage.py:1`](neural_ai/core/storage/implementations/file_storage.py:1) fájl tartalmazza a fájlrendszer alapú storage implementációt.

**Főbb jellemzők:**

1. **Támogatott formátumok:**
   - DataFrame: CSV, Excel
   - Objektum: JSON

2. **DataFrame kezelés:**
   - Automatikus formátumfelismerés fájlkiterjesztés alapján
   - Pandas DataFrame cast-olás a visszatérési értékeknél
   - Alapértelmezett `index=False` beállítás (nem menti az index oszlopot)

3. **Metódusok és típusaik:**

```python
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: str,
    fmt: Optional[str] = None,
    **kwargs: Any
) -> None

def load_dataframe(
    self,
    path: str,
    fmt: Optional[str] = None,
    **kwargs: Any
) -> pd.DataFrame

def save_object(
    self,
    obj: Any,
    path: str,
    fmt: Optional[str] = None,
    **kwargs: Any
) -> None

def load_object(
    self,
    path: str,
    fmt: Optional[str] = None,
    **kwargs: Any
) -> Any
```

4. **Biztonsági funkciók:**
   - **Atomi írás**: Temp fájllal és átnevezéssel
   - **Lemezterület ellenőrzés**: `_check_disk_space()` metódus
   - **Jogosultság ellenőrzés**: `_check_permissions()` metódus
   - **Fájl szinkronizáció**: `os.fsync()` hívás

5. **Speciális metódusok:**
   - `get_storage_info()` - Lemezterület információk lekérése
   - `_atomic_write()` - Biztonságos fájlírás
   - `_get_full_path()` - Relatív/abszolút útvonal kezelés

#### StorageFactory

A [`neural_ai/core/storage/implementations/storage_factory.py:1`](neural_ai/core/storage/implementations/storage_factory.py:1) fájl tartalmazza a factory implementációt.

**Funkcionalitás:**

1. **Regisztráció:**
   - `register_storage()` - Új storage típusok regisztrálása
   - Alapértelmezett "file" típus támogatott

2. **Létrehozás:**
   - `get_storage()` - Storage példány létrehozása
   - Dinamikus paraméterátadás a storage osztályoknak
   - Hibakezelés ismeretlen típusok esetén

**Használat:**

```python
# Alapértelmezett file storage
storage = StorageFactory.get_storage("file", base_path="data")

# Egyéni storage regisztrálása
StorageFactory.register_storage("s3", S3Storage)
s3_storage = StorageFactory.get_storage("s3", bucket="my-bucket")
```

### 3.3 Kivételek

A [`neural_ai/core/storage/exceptions.py:1`](neural_ai/core/storage/exceptions.py:1) fájl definiálja a storage specifikus kivétel osztályokat.

**Kivétel hierarchia:**

```
StorageError (Exception)
├── StorageFormatError
├── StorageSerializationError
├── StorageIOError
├── StorageNotFoundError
└── StorageValidationError
```

**Kivételek jelentése:**

| Kivétel                     | Leírás                  | Használati kontextus          |
| --------------------------- | ----------------------- | ----------------------------- |
| `StorageError`              | Alap kivétel            | Minden storage művelet alapja |
| `StorageFormatError`        | Nem támogatott formátum | CSV, JSON, Excel formátumok   |
| `StorageSerializationError` | Szerializációs hiba     | Objektum konverziók           |
| `StorageIOError`            | I/O művelet hiba        | Fájl olvasás/írás             |
| `StorageNotFoundError`      | Nem létező erőforrás    | Fájl betöltése, metaadatok    |
| `StorageValidationError`    | Érvénytelen adat        | Adatvalidáció                 |

**További információk:**
- Minden kivétel tartalmazza az eredeti kivételt (`original_error`)
- Reszponzív hibaüzenetekkel rendelkeznek
- Kompatibilisek a base komponens kivételeivel

## 4. Típusbiztonság és Minőségbiztosítás

### 4.1 Típusbiztonság

A komponens szigorú típusellenőrzést alkalmaz:

**Használt típusok:**
- `Union[str, Path]` - Rugalmas útvonal kezelés
- `Optional[T]` - Opcionális paraméterek
- `Type[StorageInterface]` - Osztály típusok
- `Callable[..., Any]` - Függvény típusok
- `Dict[str, Any]` - Szótár típusok
- `Sequence[Path]` - Sorozat típusok

**Pandas DataFrame cast-olás:**
```python
return cast(pd.DataFrame, pd.read_csv(path, **kwargs))
```

### 4.2 Minőségbiztosítás

**Ellenőrzések:**
- **Ruff**: 0 hiba a storage komponensben
- **Mypy --strict**: 8/8 fájl, 0 hiba
- **Típus annotációk**: 100%-os lefedettség

**Kódminőség:**
- ABC (Abstract Base Class) használata interfészekhez
- Docstring formátum: Google style
- Kivétel kezelés: Reszponzív hibajelzés
- Naplózás támogatása: Opcionális logger injektálás

## 5. Használati példák

### 5.1 Alapvető használat

```python
from neural_ai.core.storage import FileStorage, StorageFactory
import pandas as pd

# 1. Direct FileStorage használat
storage = FileStorage(base_path="data")

# DataFrame mentése CSV-be
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
storage.save_dataframe(df, "output.csv")

# DataFrame betöltése
loaded_df = storage.load_dataframe("output.csv")
print(loaded_df)

# 2. Objektum mentése JSON-be
config = {"setting": "value", "number": 42}
storage.save_object(config, "config.json")

# Objektum betöltése
loaded_config = storage.load_object("config.json")
print(loaded_config)
```

### 5.2 Factory használat

```python
from neural_ai.core.storage import StorageFactory

# Storage létrehozása factory-vel
storage = StorageFactory.get_storage(
    storage_type="file",
    base_path="data",
    logger=my_logger
)

# Használat
df = storage.load_dataframe("input.csv")
storage.save_dataframe(df, "output.csv")
```

### 5.3 Fájlműveletek

```python
# Létezés ellenőrzés
if storage.exists("data.csv"):
    print("Fájl létezik")

# Metaadatok lekérése
metadata = storage.get_metadata("data.csv")
print(f"Méret: {metadata['size']} bytes")
print(f"Módosítva: {metadata['modified']}")

# Könyvtár listázása
files = storage.list_dir("data", pattern="*.csv")
for file_path in files:
    print(file_path)

# Fájl törlése
storage.delete("temp.csv")
```

### 5.4 Speciális DataFrame mentés

```python
# Excel formátumban mentés
storage.save_dataframe(
    df,
    "output.xlsx",
    fmt="excel",
    sheet_name="Data",
    index=False
)

# CSV mentés egyéni paraméterekkel
storage.save_dataframe(
    df,
    "output.csv",
    sep=";",
    encoding="utf-8",
    index=False
)
```

### 5.5 Lemezterület ellenőrzés

```python
# Storage információk lekérése
info = storage.get_storage_info("data")
print(f"Szabad hely: {info['free_space_gb']:.2f} GB")
print(f"Szabad hely %: {info['free_space_percent']:.1f}%")
```

## 6. Függőségek

### 6.1 Külső könyvtárak

| Könyvtár   | Verzió   | Használat                             |
| ---------- | -------- | ------------------------------------- |
| `pandas`   | >=2.0.0  | DataFrame kezelés                     |
| `pyarrow`  | >=12.0.0 | Parquet formátum támogatás (jövőbeli) |
| `openpyxl` | >=3.0.0  | Excel formátum támogatás              |

### 6.2 Belső komponensek

| Komponens                        | Használat                         |
| -------------------------------- | --------------------------------- |
| `neural_ai.core.base.exceptions` | Alap kivétel osztályok            |
| `neural_ai.core.config`          | Konfiguráció kezelés (opcionális) |
| `neural_ai.core.logger`          | Naplózás (opcionális)             |

### 6.3 Standard library

- `pathlib` - Fájlútvonal kezelés
- `json` - JSON szerializálás
- `os` - Operációs rendszer interfész
- `datetime` - Időbélyegek kezelése
- `typing` - Típus annotációk

## 7. Integrációs lehetőségek

### 7.1 Base komponensekkel

A storage komponens integrálható a base komponensekkel:

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

# Komponensek létrehozása
components: CoreComponents = CoreComponentFactory.create_components(
    config_path="config.yaml",
    log_path="logs",
    storage_path="data"
)

# Storage használata
components.storage.save_dataframe(df, "output.csv")
```

### 7.2 Jövőbeli bővítések

**Tervezett storage típusok:**
- S3Storage - AWS S3 integráció
- DatabaseStorage - Adatbázis alapú tárolás
- MemoryStorage - Memóriában tárolás (teszteléshez)

**Tervezett formátumok:**
- Parquet - Hatékony oszlopos tárolás
- HDF5 - Nagy adatkészletekhez
- Pickle - Python objektumok gyors szerializálása

## 8. Teljesítmény és skálázhatóság

### 8.1 Teljesítmény optimalizációk

- **Atomi írás**: Biztonságos fájlműveletek
- **Formátum specifikus kezelés**: Optimalizált I/O műveletek
- **Laza betöltés**: Nagy fájlokhoz (jövőbeli funkció)

### 8.2 Skálázhatóság

- **Könyvtár struktúra**: Hierarchikus adatszervezés
- **Metaadatok**: Gyors keresés és szűrés
- **Párhuzamos hozzáférés**: Thread-safe műveletek (jövőbeli)

## 9. Hibakeresés és hibaelhárítás

### 9.1 Gyakori hibák

**StorageFormatError:**
```python
# Hiba: Ismeretlen formátum
try:
    storage.save_dataframe(df, "data.xyz")
except StorageFormatError as e:
    print(f"Hiba: {e}")
```

**StorageIOError:**
```python
# Hiba: Írási hiba
try:
    storage.save_dataframe(df, "/root/data.csv")
except StorageIOError as e:
    print(f"IO hiba: {e}")
```

**StorageNotFoundError:**
```python
# Hiba: Fájl nem található
try:
    df = storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError as e:
    print(f"Fájl nem található: {e}")
```

### 9.2 Naplózás

```python
# Logger konfigurálása
storage = FileStorage(base_path="data", logger=my_logger)

# Naplózott műveletek
storage.save_dataframe(df, "data.csv")
# [INFO] DataFrame saved to data.csv
```

## 10. Fejlesztői információk

### 10.1 Kód konvenciók

- **Fájlok**: snake_case elnevezés
- **Osztályok**: PascalCase elnevezés
- **Metódusok**: snake_case elnevezés
- **Típusok**: Teljes típus annotáció

### 10.2 Tesztelés

A komponenshez tartozó tesztek:
- [`tests/core/storage/test_file_storage.py`](tests/core/storage/test_file_storage.py:1)
- [`tests/core/storage/test_storage_factory.py`](tests/core/storage/test_storage_factory.py:1)
- [`tests/core/storage/test_storage_interface.py`](tests/core/storage/test_storage_interface.py:1)

### 10.3 Dokumentáció

- **API dokumentáció**: [`docs/components/storage/api.md`](docs/components/storage/api.md:1)
- **Architektúra**: [`docs/components/storage/architecture.md`](docs/components/storage/architecture.md:1)
- **Példák**: [`docs/components/storage/examples.md`](docs/components/storage/examples.md:1)

## 11. Összefoglalás

A storage komponens egy robusztus, típusbiztos és bővíthető adattárolási réteget biztosít a Neural AI Next rendszer számára. A komponens:

- ✅ Támogatja a DataFrame-ek és általános objektumok tárolását
- ✅ Biztonságos atomi fájlműveleteket valósít meg
- ✅ Reszponzív hibakezelést és naplózást biztosít
- ✅ Teljes típusbiztonságot garantál
- ✅ Factory mintázattal bővíthető architektúrát alkalmaz
- ✅ Integrálható a base komponensekkel

A komponens készen áll produkciós használatra, és alapvető építőeleme a Neural AI Next adatkezelési rendszerének.
