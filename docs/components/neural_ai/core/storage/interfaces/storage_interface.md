# StorageInterface

## Áttekintés

A `StorageInterface` egy absztrakt interfész, amely a tárolási műveletek standardizált definícióját biztosítja a Neural AI Next projektben. Ez az interfész garantálja, hogy minden konkrét tárolási implementáció követi a közös szerződést, lehetővé téve a egységes adatkezelést.

## Verzióinformáció

- **Modul verzió**: `1.0.0`
- **Séma verzió**: `1.0`
- **Kompatibilitás**: Neural AI Next 1.0.0+

A verziókezelés a `neural_ai.core.storage.__init__.py` modulban van implementálva, dinamikusan betöltve az `importlib.metadata` segítségével a `pyproject.toml`-ból.

## Cél

Az interfész célja a következő:
- **Standardizáció**: Közös API biztosítása különböző tárolási megoldásokhoz
- **Típusbiztonság**: Erős típusosság a `Mapping[str, Any]` használatával
- **Bővíthetőség**: Könnyű új tárolási módok hozzáadása
- **Hibakezelés**: Egységes kivételkezelés a storage specifikus hibákra

## Metódusok

### `save_dataframe(df, path, **kwargs)`

DataFrame mentése a megadott útvonalra.

**Paraméterek:**
- `df` (pd.DataFrame): A mentendő pandas DataFrame
- `path` (str): A célfájl elérési útja
- `**kwargs` (Mapping[str, Any]): További formázási és mentési opciók

**Kivételek:**
- `StorageIOError`: I/O hiba esetén
- `StorageFormatError`: Nem támogatott formátum esetén
- `StorageSerializationError`: Szerializációs hiba esetén

### `load_dataframe(path, **kwargs)`

DataFrame betöltése a megadott útvonalról.

**Paraméterek:**
- `path` (str): A forrásfájl elérési útja
- `**kwargs` (Mapping[str, Any]): További betöltési opciók

**Visszatérési érték:**
- `pd.DataFrame`: A betöltött DataFrame

**Kivételek:**
- `StorageNotFoundError`: Fájl nem található
- `StorageFormatError`: Nem támogatott formátum
- `StorageSerializationError`: Deszerializációs hiba
- `StorageIOError`: I/O hiba

### `save_object(obj, path, **kwargs)`

Objektum mentése a megadott útvonalra.

**Paraméterek:**
- `obj` (object): A mentendő objektum
- `path` (str): A célfájl elérési útja
- `**kwargs` (Mapping[str, Any]): További szerializációs opciók

**Kivételek:**
- `StorageIOError`: I/O hiba esetén
- `StorageFormatError`: Nem támogatott formátum
- `StorageSerializationError`: Szerializációs hiba

### `load_object(path, **kwargs)`

Objektum betöltése a megadott útvonalról.

**Paraméterek:**
- `path` (str): A forrásfájl elérési útja
- `**kwargs` (Mapping[str, Any]): További deszerializációs opciók

**Visszatérési érték:**
- `object`: A betöltött objektum

**Kivételek:**
- `StorageNotFoundError`: Fájl nem található
- `StorageFormatError`: Nem támogatott formátum
- `StorageSerializationError`: Deszerializációs hiba
- `StorageIOError`: I/O hiba

### `exists(path)`

Ellenőrzi, hogy az útvonal létezik-e.

**Paraméterek:**
- `path` (str): Az ellenőrizendő útvonal

**Visszatérési érték:**
- `bool`: True, ha létezik, egyébként False

### `get_metadata(path)`

Fájl vagy könyvtár metaadatainak lekérdezése.

**Paraméterek:**
- `path` (str): A cél útvonal

**Visszatérési érték:**
- `dict[str, Any]`: A metaadatok szótárba rendezve

**Kivételek:**
- `StorageNotFoundError`: Útvonal nem található
- `StorageIOError`: Metaadatok lekérdezése sikertelen

### `delete(path)`

Fájl vagy könyvtár törlése.

**Paraméterek:**
- `path` (str): A törlendő útvonal

**Kivételek:**
- `StorageNotFoundError`: Útvonal nem található
- `StorageIOError`: Törlés sikertelen

### `list_dir(path, pattern=None)`

Könyvtár tartalmának listázása.

**Paraméterek:**
- `path` (str): A könyvtár elérési útja
- `pattern` (str | None): Opcionális glob minta

**Visszatérési érték:**
- `Sequence[Path]`: A könyvtárban található elemek

**Kivételek:**
- `StorageNotFoundError`: Könyvtár nem található
- `StorageIOError`: Listázás sikertelen

## Implementációk

A `StorageInterface`-t a következő osztályok implementálják:

- [`FileStorage`](../implementations/file_storage.md): Fájlrendszer alapú tárolás
- Egyéni implementációk a specifikus igényekre

## Használati Példa

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.storage.implementations import FileStorage
import pandas as pd

# Storage inicializálása
storage: StorageInterface = FileStorage(base_path="/data")

# DataFrame mentése
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
storage.save_dataframe(df, "test.csv")

# DataFrame betöltése
loaded_df = storage.load_dataframe("test.csv")

# Objektum mentése és betöltése
data = {"key": "value", "number": 42}
storage.save_object(data, "data.pkl")
loaded_data = storage.load_object("data.pkl")

# Egyéb műveletek
if storage.exists("test.csv"):
    metadata = storage.get_metadata("test.csv")
    print(f"File size: {metadata.get('size')} bytes")
```

## Tervezési Döntések

### Típusbiztonság (Pylance Strict Compliance)

A `StorageInterface` szigorú típusbiztonságot követel meg a Pylance strict mode-nak megfelelően:

- **Explicit típusannotációk**: Minden paraméternek és visszatérési értéknek explicit típusa van
- **Strict típusellenőrzés**: Nincs `# type: ignore` komment használata, minden típushiba kijavításra kerül
- **Típusváltozók minimalizálása**: A `typing.Any` használata kerülendő, helyette specifikus típusok használata
- **Circular import kezelés**: A `TYPE_CHECKING` blokk használata a körkörös importok elkerülésére
- **Mapping típus**: A `**kwargs` helyett `Mapping[str, Any]` típust használunk a metódusokban
- **Assert és cast**: Típusbiztonság érdekében `assert` és `cast()` használata szükség esetén

### Kivételkezelés

- Specifikus storage kivételek használata (`StorageError` leszármazottak)
- Egyértelmű hibajelzés a különböző hibaesetekre
- Részletes hibaüzenetek a hibakereséshez

### Bővíthetőség

- Absztrakt metódusok használata a kötelező műveletekhez
- Opcionális paraméterek a rugalmas konfigurációhoz
- Egyszerű interfész új implementációkhoz

## Kapcsolódó Dokumentáció

- [Storage Kivételek](../exceptions.md)
- [FileStorage Implementáció](../implementations/file_storage.md)
- [Storage Factory](../implementations/storage_factory.md)