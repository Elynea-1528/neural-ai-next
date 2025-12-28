# StorageFactory

## Áttekintés

A `StorageFactory` osztály a factory design pattern implementációja a storage komponensek létrehozásához. Felelős a különböző tárolási implementációk egységes és konfigurálható példányosításáért.

## Osztály leírás

**Teljes név**: `neural_ai.core.storage.factory.StorageFactory`

**Interfész**: `StorageFactoryInterface`

## Metódusok

### `register_storage()`

Új storage típus regisztrálása a factory számára.

```python
@classmethod
def register_storage(cls, storage_type: str, storage_class: type[StorageInterface]) -> None
```

**Paraméterek:**
- `storage_type`: A storage típus egyedi azonosítója (pl. "s3", "database")
- `storage_class`: A storage osztály, amely implementálja a StorageInterface-t

**Kivételek:**
- `ValueError`: Ha a storage_class nem implementálja a StorageInterface-t

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
    hardware: HardwareInterface | None = None,
    **kwargs: object,
) -> StorageInterface
```

**Paraméterek:**
- `storage_type`: A kért storage típus azonosítója (alapértelmezett: "file")
- `base_path`: Alap könyvtár útvonal a file alapú tároláshoz
- `hardware`: A hardverképességek detektálásáért felelős interfész (opcionális)
- `**kwargs`: További paraméterek a storage osztály konstruktorának

**Visszatérési érték:**
- `StorageInterface`: Az inicializált storage példány

**Kivételek:**
- `StorageError`: Ha nem található a kért storage típus vagy a példányosítása sikertelen

**Példák:**

Alap file storage:
```python
storage = StorageFactory.get_storage("file", base_path="data")
```

Parquet storage hardware detektálással:
```python
from neural_ai.core.utils.factory import UtilsFactory

hardware = UtilsFactory.get_hardware_info()
storage = StorageFactory.get_storage("parquet", base_path="data", hardware=hardware)
```

Egyéni paraméterekkel:
```python
storage = StorageFactory.get_storage("file", base_path="data", create_if_missing=True)
```

## Alapértelmezett storage típusok

A factory alapértelmezés szerint a következő storage típusokat támogatja:

1. **`"file"`**: [`FileStorage`](implementations/file_storage.md) - Fájlrendszer alapú tárolás
2. **`"parquet"`**: [`ParquetStorageService`](implementations/parquet_storage.md) - Parquet specifikus tárolás

## Bővíthetőség

A factory könnyen bővíthető új storage típusokkal:

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.storage.factory import StorageFactory

class DatabaseStorage(StorageInterface):
    def __init__(self, connection_string: str, **kwargs):
        # Implementáció
        pass
    
    # StorageInterface metódusok implementációja
    # ...

# Regisztráció
StorageFactory.register_storage("database", DatabaseStorage)

# Használat
db_storage = StorageFactory.get_storage(
    "database", 
    connection_string="sqlite:///data.db"
)
```

## Naplózás

A factory naplózza a műveleteket a `structlog` segítségével:

- **Debug szintű naplózás**: Storage regisztrációk és példányosítások
- **Info szintű naplózás**: Sikeres storage létrehozások
- **Error szintű naplózás**: Sikertelen példányosítások

## Hibakezelés

A factory robusztus hibakezelést valósít meg:

1. **Ismeretlen típus**: `StorageError` dobódik, ha a kért storage típus nincs regisztrálva
2. **Példányosítási hiba**: `StorageError` dobódik, ha a storage osztályt nem sikerül létrehozni
3. **Paraméter hiba**: `StorageError` dobódik, ha a konstruktor paraméterek érvénytelenek

## Tesztelés

A factory-t a [`tests/core/storage/test_factory.py`](../../../tests/core/storage/test_factory.py) teszteli, amely lefedi:

- Storage regisztráció és lekérdezés
- Hibakezelés és érvényesítés
- Paraméter továbbítás
- Alapértelmezett és egyéni storage típusok