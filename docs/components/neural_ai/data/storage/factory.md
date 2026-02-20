# neural_ai/data/storage/factory.py

Adattárolási factory implementáció a különböző tároló komponensek létrehozásához.

Ez a modul felelős a tárolási implementációk példányosításáért a factory
minta segítségével. Alapértelmezetten a FileStorage implementációt támogatja,
de további tárolási típusok is regisztrálhatók dinamikusan.

## Importok

```python
from pathlib import Path
from typing import TYPE_CHECKING
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.data.storage.exceptions import StorageError
from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.data.storage.interfaces.factory_interface import StorageFactoryInterface
# ... és még 5 import
```

## Osztály: `StorageFactory(StorageFactoryInterface)`

Factory osztály tárolási komponensek létrehozásához.

Ez az osztály felelős a különböző tárolási implementációk példányosításáért.
Alapértelmezetten a FileStorage implementációt támogatja, de további
tárolási típusok is regisztrálhatók.

### Metódusok

#### `register_storage()`

```python
def register_storage(cls, storage_type: str, storage_class: type[StorageInterface]) -> None
```

Új tárolási típus regisztrálása a factory számára.

**Paraméterek:**

- **`cls`**
- **`storage_type`** (`str`): A tárolási típus egyedi azonosítója (pl. "s3", "database").
- **`storage_class`** (`type[StorageInterface]`): A tárolási osztály, amely implementálja a StorageInterface-t.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a storage_class nem implementálja a StorageInterface-t.

**Példák:**

```python
    >>> from neural_ai.data.storage.interfaces import StorageInterface
    >>> class S3Storage(StorageInterface):
    ...     pass
    >>> StorageFactory.register_storage("s3", S3Storage)
```

#### `get_registered_types()`

```python
def get_registered_types(cls) -> dict[str, type[StorageInterface]]
```

Visszaadja a regisztrált tárolási típusokat.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `dict[str, type[StorageInterface]]`
- A regisztrált tárolási típusok szótára.

#### `get_storage()`

```python
def get_storage(cls, logger: 'LoggerInterface | None' = None, config: 'ConfigManagerInterface | None' = None, event_bus: 'EventBusInterface | None' = None, storage_type: str = 'file', base_path: str | Path | None = None, hardware: 'HardwareInterface | None' = None) -> StorageInterface
```

Tárolási példány létrehozása a megadott típus alapján.

**Paraméterek:**

- **`cls`**
- **`logger`** (`'LoggerInterface | None'`) = `None`: A naplózásért felelős interfész.
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: A konfigurációért felelős interfész.
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Az eseménybusz interfész.
- **`storage_type`** (`str`) = `'file'`: A kért tárolási típus azonosítója (alapértelmezett: "file").
- **`base_path`** (`str | Path | None`) = `None`: Alap könyvtár útvonal a fájl alapú tároláshoz.
- **`hardware`** (`'HardwareInterface | None'`) = `None`: A hardverképességek detektálásáért felelős interfész (opcionális). **kwargs: További paraméterek a tárolási osztály konstruktorának.

**Visszatérési érték:**

- Típus: `StorageInterface`
- StorageInterface: Az inicializált tárolási példány.

**Kivételek:**

- **`StorageError`**: Ha nem található a kért tárolási típus vagy a

**Példák:**

```python
    >>> storage = StorageFactory.get_storage(logger_instance, "file", base_path="data")
    >>> storage.save_object({"key": "value"}, "config.json")
    >>> # Egyéni paraméterekkel
    >>> storage = StorageFactory.get_storage(logger_instance, "file", base_path="data",
    ...                                       create_if_missing=True)
```

---

**Forrásfájl:** [`neural_ai/data/storage/factory.py`](../../neural_ai/data/storage/factory.py)
