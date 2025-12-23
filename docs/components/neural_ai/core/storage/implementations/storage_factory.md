# Storage Factory

## Áttekintés

A `StorageFactory` egy factory osztály, amely felelős a különböző tároló komponensek létrehozásáért a factory design pattern segítségével. Alapértelmezetten a `FileStorage` implementációt támogatja, de további storage típusok is regisztrálhatók dinamikusan.

## Osztály

```python
class StorageFactory(StorageFactoryInterface)
```

## Metódusok

### `register_storage()`

Új storage típus regisztrálása a factory számára.

```python
@classmethod
def register_storage(
    cls,
    storage_type: str,
    storage_class: Type[StorageInterface]
) -> None
```

**Paraméterek:**

- `storage_type` (str): A storage típus egyedi azonosítója (pl. "s3", "database").
- `storage_class` (Type[StorageInterface]): A storage osztály, amely implementálja a StorageInterface-t.

**Kivételek:**

- `ValueError`: Ha a storage_class nem implementálja a StorageInterface-t.

**Példa:**

```python
from neural_ai.core.storage.interfaces import StorageInterface

class S3Storage(StorageInterface):
    pass

StorageFactory.register_storage("s3", S3Storage)
```

### `get_storage()`

Storage példány létrehozása a megadott típus alapján.

```python
@classmethod
def get_storage(
    cls,
    storage_type: str = "file",
    base_path: str | Path | None = None,
    **kwargs: object,
) -> StorageInterface
```

**Paraméterek:**

- `storage_type` (str, opcionális): A kért storage típus azonosítója (alapértelmezett: "file").
- `base_path` (str | Path | None, opcionális): Alap könyvtár útvonal a file alapú tároláshoz.
- `**kwargs` (object): További paraméterek a storage osztály konstruktorának.

**Visszatérési érték:**

- `StorageInterface`: Az inicializált storage példány.

**Kivételek:**

- `StorageError`: Ha nem található a kért storage típus vagy a példányosítás sikertelen.

**Példa:**

```python
# Alapértelmezett file storage
storage = StorageFactory.get_storage()

# Egyéni útvonallal
storage = StorageFactory.get_storage(base_path="data")

# Egyéni paraméterekkel
storage = StorageFactory.get_storage(base_path="data", create_if_missing=True)
```

## Használat

### Alapvető használat

```python
from neural_ai.core.storage.implementations import StorageFactory

# Alapértelmezett file storage létrehozása
storage = StorageFactory.get_storage()

# Objektum mentése
storage.save_object({"key": "value"}, "config.json")

# Objektum betöltése
data = storage.load_object("config.json")
```

### Egyéni storage regisztrálása

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.storage.implementations import StorageFactory

class CustomStorage(StorageInterface):
    def __init__(self, connection_string: str, **kwargs: object):
        self.connection_string = connection_string
        # További inicializálás...

    # Implementáld a szükséges metódusokat...

# Storage regisztrálása
StorageFactory.register_storage("custom", CustomStorage)

# Használat
storage = StorageFactory.get_storage(
    "custom",
    connection_string="sqlite:///mydb.db"
)
```

## Hibakezelés

A factory megfelelő hibakezelést biztosít a következő esetekben:

1. **Ismeretlen storage típus**: `StorageError` kerül kivételre, ha nem létező típust kérünk le.

2. **Példányosítási hiba**: `StorageError` kerül kivételre, ha a storage osztályt nem sikerül létrehozni (pl. hibás paraméterek).

3. **Váratlan hibák**: `StorageError` kerül kivételre, ha bármilyen egyéb hiba történik a példányosítás során.

**Példa hibakezelésre:**

```python
from neural_ai.core.storage.exceptions import StorageError

try:
    storage = StorageFactory.get_storage("nonexistent")
except StorageError as e:
    print(f"Hiba történt: {e}")
```

## Implementáció részletei

### Belső állapot

- `_storage_types: Dict[str, Type[StorageInterface]]`: A regisztrált storage típusok nyilvántartása.

### Alapértelmezett támogatás

Alapértelmezés szerint a következő storage típusok vannak regisztrálva:

- `"file"`: `FileStorage` - Fájl alapú tárolás

### Dependency Injection

A factory támogatja a dependency injection-t a `**kwargs` paramétereken keresztül, lehetővé téve a storage osztályok rugalmas konfigurálását.

## Kapcsolódó komponensek

- [`StorageInterface`](../interfaces/storage_interface.md): A storage komponensek interfésze.
- [`FileStorage`](file_storage.md): Fájl alapú tároló implementáció.
- [`StorageFactoryInterface`](../interfaces/factory_interface.md): A factory interfésze.
- [`StorageError`](../exceptions.md): Storage kivételek.

## Tesztelés

A komponens teljes körűen tesztelve van, 100% kódlefedettséggel. A tesztek a következő eseteket fedik le:

- Storage regisztráció és lekérdezés
- Hibakezelés (érvénytelen típusok, példányosítási hibák)
- Paraméterátadás és konfiguráció
- Több storage típus támogatása

## Jövőbeli fejlesztések

- Több beépített storage típus támogatása (pl. S3, database)
- Konfiguráció alapú storage inicializálás
- Storage pool kezelés
- Titkosítási támogatás