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
from neural_ai.core.config.interfaces.types import (  # noqa: F401
    CollectorsConfig,
    ConfigSchema,
    DatabaseConfig,
    EventsConfig,
    LoggingConfig,
    ProcessorsConfig,
    StorageConfig,
    SystemConfig,
)

__all__ = [
    "ConfigManagerInterface",
    "ConfigManagerFactoryInterface",
    "SystemConfig",
    "StorageConfig",
    "ProcessorsConfig",
    "LoggingConfig",
    "DatabaseConfig",
    "EventsConfig",
    "CollectorsConfig",
    "ConfigSchema",
]
