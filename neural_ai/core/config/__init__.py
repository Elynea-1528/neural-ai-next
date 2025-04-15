"""Neural AI Next konfigurációkezelő modul.

Ez a modul tartalmazza a Neural AI Next rendszer konfigurációkezelő komponensét.
"""

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface

__all__ = [
    "ConfigManagerInterface",
    "ConfigManagerFactoryInterface",
]
