# neural_ai/data/storage/__init__.py

Neural AI adattárolási komponens.

Ez a modul az adattárolási komponens fő exportjait tartalmazza, beleértve a FileStorage
és StorageFactory osztályokat, valamint a hozzájuk tartozó interfészeket és típusokat.

A modul támogatja a függőség injektálást (Dependency Injection) a logger és config
komponensek számára, így elkerülve a körkörös importproblémákat.

## Importok

```python
from importlib import metadata
from typing import TYPE_CHECKING
from typing import Final
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.data.ingestion.market_data_persister import MarketDataPersister
from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.data.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
# ... és még 4 import
```

## Konstansok

- **`_version`**
: `'1.0.0'`


---

**Forrásfájl:** [`neural_ai/data/storage/__init__.py`](../../neural_ai/data/storage/__init__.py)
