# Storage Modul

## Áttekintés

A Storage modul a Neural AI Next rendszer tárolási rétegét implementálja. Ez a modul felelős a különböző adatok (DataFrame-ek, objektumok) tárolásáért, betöltéséért és kezeléséért.

## Fő Komponensek

### Implementációk
- **[`FileStorage`](implementations/file_storage.md)**: Fájlrendszer alapú tárolási megoldás
- **[`ParquetStorageService`](implementations/parquet_storage.md)**: Particionált Parquet tároló szolgáltatás

### Interfészek
- **[`StorageInterface`](interfaces/storage_interface.md)**: Alapvető tárolási műveletek
- **[`StorageFactoryInterface`](interfaces/factory_interface.md)**: Tároló objektumok létrehozásáért felelős gyártó

### Backend-ek
- **[`PandasBackend`](backends/pandas_backend.md)**: Pandas alapú tárolási backend
- **[`PolarsBackend`](backends/polars_backend.md)**: Polars alapú tárolási backend

### Kivételek
- **[`StorageError`](exceptions/__init__.md)**: Storage komponens kivételek

## Verzióinformáció

- **`__version__`**: A modul verziója (pl. "1.0.0")
- **`__schema_version__`**: Konfigurációs séma verzió (pl. "1.0")

## Használat

```python
from neural_ai.core.storage import StorageFactory, FileStorage
from neural_ai.core.storage.interfaces import StorageInterface

# Storage példány létrehozása
storage = StorageFactory.get_storage("file", base_path="data")

# DataFrame mentése
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
storage.save_dataframe(df, "test.csv")

# Objektum mentése
config = {"key": "value"}
storage.save_object(config, "config.json")
```

## Függőség Injektálás

A modul támogatja a függőség injektálást (Dependency Injection) a logger és config komponensek számára, így elkerülve a körkörös importproblémákat.

```python
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.config.interfaces import ConfigManagerInterface

class CustomStorage:
    def __init__(
        self,
        logger: LoggerInterface,
        config: ConfigManagerInterface
    ):
        self._logger = logger
        self._config = config
```

## Exportált Típusok

- `StorageInterface`: Alap tárolási interfész
- `StorageFactoryInterface`: Factory interfész
- `FileStorage`: Fájl alapú tároló
- `ParquetStorageService`: Parquet tároló szolgáltatás
- `LoggerInterface`: Logger interfész típus
- `ConfigManagerInterface`: Config manager interfész típus