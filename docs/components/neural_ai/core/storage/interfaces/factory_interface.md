# StorageFactoryInterface

## Áttekintés

A `StorageFactoryInterface` egy absztrakt alaposztály, amely egy gyártó (factory) mintát definiál a különböző tárolási implementációk létrehozásához. Ez az interfész lehetővé teszi a tárolási osztályok dinamikus regisztrálását és példányosítását, ezzel függetleníti a rendszert a konkrét tárolási megoldásoktól.

## Cél

A factory minta alkalmazásával a rendszer rugalmasabbá válik:
- Új tárolási típusok egyszerűen regisztrálhatók futásidőben.
- A kód független a konkrét tárolási osztályoktól.
- Könnyű tesztelhetőség mock objektumokkal.

## Interfész Metódusok

### `register_storage`

```python
@classmethod
@abstractmethod
def register_storage(
    cls,
    storage_type: str,
    storage_class: type[StorageInterface],
) -> None
```

Új tárolási típus regisztrálása a factory számára.

**Paraméterek:**
- `storage_type` (str): A tárolási típus egyedi azonosítója (pl. 'file', 's3').
- `storage_class` (type[StorageInterface]): A tárolási osztály, amely megvalósítja a `StorageInterface`-t.

**Kivételek:**
- `ValueError`: Ha a `storage_type` üres string.
- `TypeError`: Ha a `storage_class` nem egy osztály, vagy nem valósítja meg a `StorageInterface`-t.

### `get_storage`

```python
@classmethod
@abstractmethod
def get_storage(
    cls,
    storage_type: str = "file",
    base_path: str | Path | None = None,
    **kwargs: dict[str, object],
) -> StorageInterface
```

Tárolási példány létrehozása a megadott típus alapján.

**Paraméterek:**
- `storage_type` (str, opcionális): A kért tárolási típus azonosítója. Alapértelmezett: 'file'.
- `base_path` (str | Path | None, opcionális): Az alap könyvtár útvonala a fájl alapú tároláshoz.
- `**kwargs` (dict[str, object], opcionális): További, a tárolási implementáció specifikus paraméterek.

**Visszatérési érték:**
- `StorageInterface`: Egy inicializált tárolási példány.

**Kivételek:**
- `KeyError`: Ha a megadott tárolási típus nincs regisztrálva.
- `ValueError`: Ha a megadott paraméterek érvénytelenek.

## Használati Példa

```python
from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
from pathlib import Path

# 1. Saját tárolási osztály definiálása
class MyCustomStorage(StorageInterface):
    def __init__(self, base_path: Path | None = None, **kwargs):
        self._base_path = base_path or Path.cwd()
    
    # ... implementáció ...

# 2. Saját factory osztály létrehozása
class MyStorageFactory(StorageFactoryInterface):
    _storage_types: dict[str, type[StorageInterface]] = {}
    
    @classmethod
    def register_storage(cls, storage_type: str, storage_class: type[StorageInterface]) -> None:
        cls._storage_types[storage_type] = storage_class
    
    @classmethod
    def get_storage(cls, storage_type: str = "file", base_path: str | Path | None = None, **kwargs) -> StorageInterface:
        if storage_type not in cls._storage_types:
            raise KeyError(f"Unknown storage type: {storage_type}")
        return cls._storage_types[storage_type](base_path=base_path, **kwargs)

# 3. Tárolási típus regisztrálása
MyStorageFactory.register_storage("custom", MyCustomStorage)

# 4. Tárolási példány létrehozása
storage = MyStorageFactory.get_storage("custom", base_path=Path("/tmp/data"))
```

## Implementációk

A projektben a [`StorageFactory`](../../../neural_ai/core/storage/implementations/storage_factory.py) osztály valósítja meg ezt az interfészt, és biztosítja a beépített tárolási típusok (pl. file storage) kezelését.

## Kapcsolódó Dokumentáció

- [`StorageInterface`](storage_interface.md): A tárolási műveletek interfésze.
- [`StorageFactory`](../implementations/storage_factory.md): A konkrét factory implementáció.
- [Core Dependencies](../../../development/core_dependencies.md): A core komponensek függőségi struktúrája.