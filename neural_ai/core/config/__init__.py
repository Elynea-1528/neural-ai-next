"""Konfigurációs modul a Neural AI rendszerhez.

Ez a modul a konfigurációkezeléshez szükséges alapvető osztályokat,
interfészeket és kivételeket exportálja. A modul tartalmazza:

- Konfigurációs kivételek: ConfigError és leszármazottai
- Konfigurációkezelő interfészek: ConfigManagerInterface, ConfigManagerFactoryInterface
- Konfigurációkezelő implementációk: YAMLConfigManager, ConfigManagerFactory

Példa a modul használatára:
    from neural_ai.core.config import ConfigManagerFactory, ConfigError

    try:
        factory = ConfigManagerFactory()
        config_manager = factory.create_manager('yaml')
    except ConfigError as e:
        print(f"Konfigurációs hiba: {e}")
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
