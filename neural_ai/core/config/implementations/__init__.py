"""Konfigurációkezelő implementációk.

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat,
köztük a YAML alapú konfigurációkezelőt és a hozzá tartozó factory osztályt.

A modul a következő fő komponenseket exportálja:
    - ConfigManagerFactory: Factory osztály konfigurációkezelők létrehozásához
    - YAMLConfigManager: YAML fájlokat kezelő konfigurációkezelő implementáció

Példa használat:
    >>> from neural_ai.core.config.implementations import ConfigManagerFactory
    >>> factory = ConfigManagerFactory()
    >>> config = factory.get_manager("config.yaml")
    >>> value = config.get("database", "host")
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config_manager_factory import ConfigManagerFactory as ConfigManagerFactory
    from .yaml_config_manager import YAMLConfigManager as YAMLConfigManager

from .config_manager_factory import ConfigManagerFactory
from .yaml_config_manager import YAMLConfigManager

__all__ = [
    "ConfigManagerFactory",
    "YAMLConfigManager",
]
