"""Logger komponens fő inicializációs modulja.

Ez a modul biztosítja a Neural-AI-Next rendszer naplózási funkcionalitását.
Központi exportmodulként szolgál, amely összegyűjti és elérhetővé teszi
a logger komponens összes fontos osztályát és interfészét.

A modul a következő fő komponenseket exportálja:
    - Interfészek: LoggerInterface, LoggerFactoryInterface
    - Implementációk: ColoredLogger, DefaultLogger, LoggerFactory, RotatingFileLogger
    - Kivételek: LoggerError, LoggerConfigurationError, LoggerInitializationError

Példa használatra:
    >>> from neural_ai.core.logger import LoggerFactory, DefaultLogger
    >>> logger = DefaultLogger()
    >>> logger.info("Alkalmazás indítása...")
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.exceptions import (
        LoggerConfigurationError,
        LoggerError,
        LoggerInitializationError,
    )
    from neural_ai.core.logger.implementations import (
        ColoredLogger,
        DefaultLogger,
        LoggerFactory,
        RotatingFileLogger,
    )
    from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

from neural_ai.core.logger.exceptions import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)
from neural_ai.core.logger.implementations import (
    ColoredLogger,
    DefaultLogger,
    LoggerFactory,
    RotatingFileLogger,
)
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

__all__ = [
    # Interfaces
    "LoggerInterface",
    "LoggerFactoryInterface",
    # Implementations
    "ColoredLogger",
    "DefaultLogger",
    "LoggerFactory",
    "RotatingFileLogger",
    # Exceptions
    "LoggerError",
    "LoggerConfigurationError",
    "LoggerInitializationError",
]
