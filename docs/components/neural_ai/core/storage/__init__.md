# neural_ai.core.storage

A Neural AI storage komponens fő modulja, amely a tárolási funkciók központi exportjait tartalmazza.

## Áttekintés

Ez a modul a storage komponens fő exportjait tartalmazza, beleértve a `FileStorage` és `StorageFactory` osztályokat, valamint a hozzájuk tartozó interfészeket és típusokat. A modul támogatja a függőség injektálást (Dependency Injection) a logger és config komponensek számára, így elkerülve a körkörös importproblémákat.

## Exportok

### Implementációk

- **[`FileStorage`](file_storage.md)** - Fájlrendszer alapú tároló implementáció
- **[`StorageFactory`](storage_factory.md)** - Factory osztály storage komponensek létrehozásához

### Interfészek

- **[`StorageInterface`](../interfaces/storage_interface.md)** - A tárolási műveletek absztrakt interfésze
- **[`StorageFactoryInterface`](../interfaces/factory_interface.md)** - A storage factory absztrakt interfésze

### Típusok

- **[`LoggerInterface`](../logger/interfaces/logger_interface.md)** - Logger interfész típus definíció
- **[`ConfigManagerInterface`](../config/interfaces/config_interface.md)** - Konfiguráció kezelő interfész típus definíció

## Használat

### Alapvető Importálás

```python
from neural_ai.core.storage import FileStorage, StorageFactory
```

### Függőség Injektálással

```python
from neural_ai.core.storage import FileStorage
from neural_ai.core.logger import LoggerInterface
from neural_ai.core.config import ConfigManagerInterface

# Logger és Config injektálása
logger: LoggerInterface = ...
config: ConfigManagerInterface = ...

storage = FileStorage(
    base_path="/path/to/storage",
    logger=logger,
    config=config
)
```

### Factory Használata

```python
from neural_ai.core.storage import StorageFactory

# Alapértelmezett file storage létrehozása
storage = StorageFactory.get_storage(
    storage_type="file",
    base_path="/path/to/storage"
)

# DataFrame mentése
import pandas as pd
df = pd.DataFrame({"column": [1, 2, 3]})
storage.save_dataframe(df, "data.csv")
```

## Architektúra

### Függőség Injektálás (DI)

A modul a `TYPE_CHECKING` blokkot használja a típusdefiníciókhoz, ami megakadályozza a körkörös importproblémákat. A futásidőben csak a szükséges implementációk kerülnek importálásra.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.implementations.file_storage import FileStorage
    from neural_ai.core.storage.implementations.storage_factory import StorageFactory
    from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
```

### Típusos Exportok

A modul explicit módon exportálja a szükséges osztályokat és interfészeket a `__all__` listán keresztül:

```python
__all__ = [
    # Implementációk
    "FileStorage",
    "StorageFactory",
    # Interfészek
    "StorageInterface",
    "StorageFactoryInterface",
    # Típusok
    "LoggerInterface",
    "ConfigManagerInterface",
]
```

## Jellemzők

- **Típusbiztonság**: A modul teljes mértékben típusos, `mypy` kompatibilis
- **Függőség Injektálás**: Támogatja a logger és config komponensek injektálását
- **Körkörös Importok Elkerülése**: `TYPE_CHECKING` blokk használatával
- **Modularitás**: Tiszta interfész-alapú tervezés
- **Bővíthetőség**: Egyszerűen hozzáadhatóak új storage implementációk

## Kapcsolódó Dokumentáció

- [Storage Implementációk](implementations/)
- [Storage Interfészek](interfaces/)
- [Core Komponensek Függőségi Analízis](../../../development/core_dependencies.md)

## Verzió

- **Modul**: neural_ai.core.storage
- **Verzió**: 1.0.0
- **Utolsó Frissítés**: 2025-12-23

## Fejlesztés

### Tesztelés

A modulhoz tartozó tesztek a `tests/core/storage/test___init__.py` fájlban találhatók.

```bash
# Teszt futtatása
pytest tests/core/storage/test___init__.py -v
```

### Kódminőség Ellenőrzés

```bash
# Ruff linter
ruff check neural_ai/core/storage/__init__.py

# MyPy típusellenőrzés
mypy neural_ai/core/storage/__init__.py

# Pytest coverage
pytest tests/core/storage/ --cov=neural_ai.core.storage --cov-report=html
```

## Hibák és Jelentések

Ha hibát találsz vagy javaslatod van, kérjük hozz létre egy issue-t a projekt GitHub oldalán.