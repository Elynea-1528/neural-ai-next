"""Konfigurációkezelő interfészek.

Ez a modul tartalmazza a konfigurációkezelő komponens interfészeit.
"""

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface

__all__ = ["ConfigManagerInterface", "ConfigManagerFactoryInterface"]
