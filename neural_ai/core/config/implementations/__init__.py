"""Konfigurációkezelő implementációk.

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat.
"""

from .config_manager_factory import ConfigManagerFactory
from .yaml_config_manager import YAMLConfigManager

__all__ = [
    "ConfigManagerFactory",
    "YAMLConfigManager",
]
