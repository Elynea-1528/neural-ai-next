"""Konfigurációs modul a Neural AI rendszerhez.

Ez a modul a konfigurációkezeléshez szükséges alapvető osztályokat,
interfészeket és kivételeket exportálja.

A modul a következő komponenseket tartalmazza:

- **Kivételek**: Konfigurációs hibakezelés speciális kivétel osztályokkal
- **Interfészek**: Konfigurációkezelő és gyártó interfészek
- **Implementációk**: YAML alapú konfigurációkezelés és gyártó osztály

Komponensek:
    ConfigError: Alap konfigurációs kivétel osztály
    ConfigKeyError: Konfigurációs kulcs hibák
    ConfigLoadError: Konfiguráció betöltési hibák
    ConfigSaveError: Konfiguráció mentési hibák
    ConfigTypeError: Típus hibák a konfigurációban
    ConfigValidationError: Validációs hibák
    ConfigManagerFactory: Konfigurációkezelő gyártó
    YAMLConfigManager: YAML alapú konfigurációkezelő
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
        print(f"Konfigurációs hiba: {e}")
    ```

További információkért lásd:
    - docs/components/neural_ai/core/config/__init__.md
"""

from neural_ai.core.config.exceptions import (
    ConfigError,
    ConfigKeyError,
    ConfigLoadError,
    ConfigSaveError,
    ConfigTypeError,
    ConfigValidationError,
)
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory,
)
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import (
    ConfigManagerFactoryInterface,
)

__all__ = [
    "ConfigError",
    "ConfigLoadError",
    "ConfigSaveError",
    "ConfigValidationError",
    "ConfigTypeError",
    "ConfigKeyError",
    "ConfigManagerFactory",
    "YAMLConfigManager",
    "ConfigManagerInterface",
    "ConfigManagerFactoryInterface",
]
