# neural_ai/core/config/interfaces/__init__.py

Konfigurációkezelő interfészek.

Ez a modul tartalmazza a konfigurációkezelő komponens interfészeit,
beleértve a ConfigManagerInterface és ConfigManagerFactoryInterface osztályokat.

A modul biztosítja a konfigurációkezeléshez szükséges alapvető interfészeket,
amelyek lehetővé teszik a különböző konfigurációs formátumok és tárolási
módok egységes kezelését.

## Importok

```python
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface
from neural_ai.core.config.interfaces.types import CollectorsConfig
from neural_ai.core.config.interfaces.types import ConfigSchema
from neural_ai.core.config.interfaces.types import DatabaseConfig
from neural_ai.core.config.interfaces.types import EventsConfig
from neural_ai.core.config.interfaces.types import LoggingConfig
from neural_ai.core.config.interfaces.types import ProcessorsConfig
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.config.interfaces.types import SystemConfig
```

## Konstansok

- **`__all__`**
: `['ConfigManagerInterface', 'ConfigManagerFactoryInterface', 'SystemConfig', 'StorageConfig', 'ProcessorsConfig', 'LoggingConfig', 'DatabaseConfig', 'EventsConfig', 'CollectorsConfig', 'ConfigSchema']`


---

**Forrásfájl:** [`neural_ai/core/config/interfaces/__init__.py`](../../neural_ai/core/config/interfaces/__init__.py)
