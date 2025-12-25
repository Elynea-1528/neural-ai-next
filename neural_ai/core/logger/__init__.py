"""Logger komponens fő inicializációs modulja.

Ez a modul biztosítja a Neural-AI-Next rendszer naplózási funkcionalitását.
Központi exportmodulként szolgál, amely összegyűjti és elérhetővé teszi
a logger komponens összes fontos osztályát és interfészét.

A modul a következő fő komponenseket exportálja:
    - Interfészek: LoggerInterface, LoggerFactoryInterface
    - Implementációk: ColoredLogger, DefaultLogger, LoggerFactory, RotatingFileLogger
    - Kivételek: LoggerError, LoggerConfigurationError, LoggerInitializationError

Verziókezelés:
    A modul importálja a projekt verzióinformációit a fő neural_ai csomagból,
    és biztosítja a konfigurációs séma verzióját a kompatibilitás ellenőrzéséhez.

Példa használatra:
    >>> from neural_ai.core.logger import LoggerFactory, DefaultLogger
    >>> logger = DefaultLogger()
    >>> logger.info("Alkalmazás indítása...")
    >>> print(f"Logger verzió: {__version__}")
"""

from importlib import metadata
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from neural_ai.core.logger.exceptions import (
        LoggerConfigurationError,
        LoggerError,
        LoggerInitializationError,
    )
    from neural_ai.core.logger.factory import LoggerFactory
    from neural_ai.core.logger.implementations import (
        ColoredLogger,
        DefaultLogger,
        RotatingFileLogger,
    )
    from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

from neural_ai.core.logger.exceptions import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.implementations import (
    ColoredLogger,
    DefaultLogger,
    RotatingFileLogger,
)
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

# Verzióinformációk dinamikus betöltése
try:
    _version: str = metadata.version("neural-ai-next")
except metadata.PackageNotFoundError:
    # Fallback verzió, ha a csomag nincs telepítve
    _version = "1.0.0"

__version__: Final[str] = _version
__schema_version__: Final[str] = LoggerFactory.get_schema_version()

__all__: Final[list[str]] = [
    # Verzióinformációk
    "__version__",
    "__schema_version__",
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
