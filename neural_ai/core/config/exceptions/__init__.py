"""Kivételek a konfigurációkezelő modulhoz.

Ez a modul exportálja az összes konfigurációkezelési kivétel osztályt.
"""

from .config_error import (
    ConfigError,
    ConfigKeyError,
    ConfigLoadError,
    ConfigSaveError,
    ConfigTypeError,
    ConfigValidationError,
)

__all__ = [
    "ConfigError",
    "ConfigLoadError",
    "ConfigSaveError",
    "ConfigValidationError",
    "ConfigTypeError",
    "ConfigKeyError",
]
