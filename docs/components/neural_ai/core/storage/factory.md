# StorageFactory

## Áttekintés

A `StorageFactory` egy factory osztály, amely felelős a különböző tárolási implementációk példányosításáért a factory minta segítségével. Alapértelmezetten a `FileStorage` implementációt támogatja, de további storage típusok is regisztrálhatók dinamikusan.

## Osztály

```python
class StorageFactory(StorageFactoryInterface)
```

## Metódusok

### `register_storage()`

Új tárolási típus regisztrálása a factory számára.

```python
@classmethod
def register_storage(
    cls,
    storage_type: str,
    storage_class: type[StorageInterface]
) -> None
```

**Paraméterek:**
- `storage_type`: A tárolási típus egyedi azonosítója (pl. "s3", "database")
- `storage_class`: A tárolási osztály, amely implementálja a StorageInterface-t

**Kivételek:**
- `ValueError`: Ha a storage_class nem implementálja a StorageInterface-t

**Példa:**

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.storage import StorageFactory

class S3Storage(StorageInterface):
    def save_dataframe(self, df, path, **kwargs):
        # S3 implementáció
        pass
    
    # További metódusok...

# Regisztrálás
StorageFactory.register_storage("s3", S3Storage)
```

### `get_storage()`

Tárolási példány létrehozása a megadott típus alapján.

```python
@classmethod
def get_storage(
    cls,
    storage_type: str = "file",
    base_path: str | Path | None = None,
    hardware: HardwareInterface | None = None,
    **kwargs: object
) -> StorageInterface
```

**Paraméterek:**
- `storage_type`: A kért tárolási típus azonosítója (alapértelmezett: "file")
- `base_path`: Alap könyvtár útvonal a file alapú tároláshoz
- `hardware`: A hardverképességek detektálásáért felelős interfész (opcionális)
- `**kwargs`: További paraméterek a storage osztály konstruktorának

**Visszatérési érték:**
- `StorageInterface`: Az inicializált tárolási példány

**Kivételek:**
- `StorageError`: Ha nem található a kért tárolási típus vagy a példányosítása sikertelen

**Példák:**

```python
# Alapértelmezett file storage
storage = StorageFactory.get_storage("file", base_path="data")

# Egyéni paraméterekkel
storage = StorageFactory.get_storage(
    "file",
    base_path="data",
    create_if_missing=True
)

# DataFrame mentése
df = pd.DataFrame({"col1": [1, 2, 3]})
storage.save_dataframe(df, "test.csv")

# Objektum mentése
storage.save_object({"key": "value"}, "config.json")
```

## Alapértelmezett Tárolási Típusok

A factory alapértelmezés szerint a következő tárolási típusokat támogatja:

- **`file`**: `FileStorage` - Fájlrendszer alapú tárolás

## Belső Működés

### Tárolási Típusok Regisztrálása

A `_storage_types` szótár tárolja a regisztrált tárolási típusokat:

```python
_storage_types: dict[str, type[StorageInterface]] = {
    "file": FileStorage,
}
```

### Példányosítási Folyamat

1. **Típus ellenőrzése**: A factory ellenőrzi, hogy a kért storage_type létezik-e
2. **Paraméterek átadása**: A base_path és hardware paraméterek hozzáadása a kwargs-hoz
3. **Példányosítás**: A tárolási osztály konstruktorának meghívása
4. **Hibakezelés**: TypeError és egyéb kivételek elkapása és StorageError-rá alakítása

## Hibakezelés

A factory a következő hibákat kezeli:

- **Ismeretlen típus**: `StorageError("Ismeretlen storage típus: ...")`
- **Konstrukciós hiba**: `StorageError("Nem sikerült létrehozni a storage példányt: ...")`
- **Váratlan hiba**: `StorageError("Váratlan hiba történt a storage példányosítása közben: ...")`

## Extensibility

A factory könnyen bővíthető új tárolási típusokkal:

```python
# Egyéni cloud storage hozzáadása
StorageFactory.register_storage("cloud", CloudStorage)

# Használat
cloud_storage = StorageFactory.get_storage("cloud", bucket="my-bucket")
```

Ez a megközelítés lehetővé teszi a rendszer számára, hogy dinamikusan adaptálódjon különböző tárolási megoldásokhoz anélkül, hogy módosítani kellene a core kódot.