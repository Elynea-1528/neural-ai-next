"""Kivételek modul a Neural AI Next projektben.

Ez a modul exportálja az összes alap és specifikus kivétel osztályt,
amelyeket a rendszer különböző komponensei használnak.
"""

from .base_error import (
    ComponentNotFoundError,
    ConfigurationError,
    ConnectionError,
    DependencyError,
    InsufficientDiskSpaceError,
    NetworkException,
    NeuralAIException,
    PermissionDeniedError,
    SingletonViolationError,
    StorageException,
    StoragePermissionError,
    StorageReadError,
    StorageWriteError,
    TimeoutError,
)

__all__ = [
    "NeuralAIException",
    "StorageException",
    "StorageWriteError",
    "StorageReadError",
    "StoragePermissionError",
    "ConfigurationError",
    "DependencyError",
    "SingletonViolationError",
    "ComponentNotFoundError",
    "NetworkException",
    "TimeoutError",
    "ConnectionError",
    "InsufficientDiskSpaceError",
    "PermissionDeniedError",
]
