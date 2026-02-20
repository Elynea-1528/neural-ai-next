# neural_ai/core/config/implementations/__init__.py

Konfigurációkezelő implementációk.

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat,
köztük a YAML alapú konfigurációkezelőt és a hozzá tartozó factory osztályt.

A modul a következő fő komponenseket exportálja:
    - ConfigManagerFactory: Factory osztály konfigurációkezelők létrehozásához
    - YAMLConfigManager: YAML fájlokat kezelő konfigurációkezelő implementáció

Verziókezelés:
    A modul támogatja a konfigurációs sémák verziókezelését. Minden konfigurációs
    fájl tartalmazhat egy 'schema_version' mezőt, amely a séma verzióját határozza
    meg. Ez lehetővé teszi a verziók közötti migrációkat és kompatibilitás-ellenőrzést.

Példa használat:
    >>> from neural_ai.core.config.implementations import ConfigManagerFactory
    >>> factory = ConfigManagerFactory()
    >>> config = factory.get_manager("config.yaml")
    >>> value = config.get("database", "host")
    >>> schema_version = config.get("schema_version", default="1.0.0")

## Importok

```python
from importlib import metadata
from typing import TYPE_CHECKING
from yaml_config_manager import YAMLConfigManager
from yaml_config_manager import YAMLConfigManager
```

## Konstansok

- **`__version__`**
: `'1.0.0'`


- **`__all__`**
: `['YAMLConfigManager', '__version__', 'SCHEMA_VERSION']`


---

**Forrásfájl:** [`neural_ai/core/config/implementations/__init__.py`](../../neural_ai/core/config/implementations/__init__.py)
