# neural_ai/core/config/__init__.py

Konfigurációs modul a Neural AI rendszerhez.

Ez a modul a konfigurációkezeléshez szükséges alapvető osztályokat,
interfészeket és kivételeket exportálja.

A modul a következő komponenseket tartalmazza:

- **Kivételek**: Konfigurációs hibakezelés speciális kivétel osztályokkal
- **Interfészek**: Konfigurációkezelő és gyártó interfészek
- **Factory**: Konfigurációkezelő gyártó osztály

Komponensek:
    ConfigError: Alap konfigurációs kivétel osztály
    ConfigKeyError: Konfigurációs kulcs hibák
    ConfigLoadError: Konfiguráció betöltési hibák
    ConfigSaveError: Konfiguráció mentési hibák
    ConfigTypeError: Típus hibák a konfigurációban
    ConfigValidationError: Validációs hibák
    ConfigManagerFactory: Konfigurációkezelő gyártó
    ConfigManagerInterface: Konfigurációkezelő interfész
    ConfigManagerFactoryInterface: Gyártó interfész

Példa a modul használatára:
    ```python
    from neural_ai.core.config import ConfigManagerFactory, ConfigError

    try:
        factory = ConfigManagerFactory()
        config_manager = factory.create_manager('yaml')
        value = config_manager.get('database.host', 'localhost')
    except ConfigError as e:
        logger.error("Konfigurációs hiba: %s", e, extra={"error": str(e)})
    ```

További információkért lásd:
    - docs/components/neural_ai/core/config/__init__.md

## Importok

```python
from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.exceptions import ConfigKeyError
from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.exceptions import ConfigSaveError
from neural_ai.core.config.exceptions import ConfigTypeError
from neural_ai.core.config.exceptions import ConfigValidationError
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface
```

## Konstansok

- **`__all__`**
: `['ConfigError', 'ConfigLoadError', 'ConfigSaveError', 'ConfigValidationError', 'ConfigTypeError', 'ConfigKeyError', 'ConfigManagerFactory', 'ConfigManagerInterface', 'ConfigManagerFactoryInterface']`


---

**Forrásfájl:** [`neural_ai/core/config/__init__.py`](../../neural_ai/core/config/__init__.py)
