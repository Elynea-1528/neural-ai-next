"""Konfigurációkezelő interfészek.

Ez a modul tartalmazza a konfigurációkezelő komponens interfészeit,
beleértve a ConfigManagerInterface és ConfigManagerFactoryInterface osztályokat.

A modul biztosítja a konfigurációkezeléshez szükséges alapvető interfészeket,
amelyek lehetővé teszik a különböző konfigurációs formátumok és tárolási
módok egységes kezelését.
"""

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import (
    ConfigManagerFactoryInterface,
)

__all__ = ["ConfigManagerInterface", "ConfigManagerFactoryInterface"]
