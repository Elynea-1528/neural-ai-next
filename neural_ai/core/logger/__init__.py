"""Logger komponens fő inicializációs modulja.

Ez a modul biztosítja a Neural-AI-Next rendszer naplózási funkcionalitását.
Központi exportmodulként szolgál, amely összegyűjti és elérhetővé teszi
a logger komponens publikus API-ját (Interface + Factory + Exceptions).

A modul a következő fő komponenseket exportálja:
    - Interfészek: LoggerInterface, LoggerFactoryInterface
    - Factory: LoggerFactory
    - Kivételek: LoggerError, LoggerConfigurationError, LoggerInitializationError

DDD Szabály:
    Az implementációk (ColoredLogger, DefaultLogger, RotatingFileLogger) NEM exportáltak.
    Ezeket közvetlenül a LoggerFactory hozza létre.

Verziókezelés:
    A modul importálja a projekt verzióinformációit a fő neural_ai csomagból,
    és biztosítja a konfigurációs séma verzióját a kompatibilitás ellenőrzéséhez.

Példa használatra:
    >>> from neural_ai.core.logger import LoggerFactory
    >>> logger = LoggerFactory.get_logger(__name__)
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
    from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

from neural_ai.core.logger.exceptions import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

# Verzióinformációk dinamikus betöltése
try:
    _version: str = metadata.version("neural-ai-next")
except metadata.PackageNotFoundError:
    # Fallback verzió, ha a csomag nincs telepítve
    _version = "1.0.0"

__version__: Final[str] = _version


# Sémaváltozat késleltetett betöltéssel (körkörös import elkerülése érdekében)
def _get_schema_version() -> str:
    from neural_ai.core.logger.factory import LoggerFactory

    return LoggerFactory.get_schema_version()


__schema_version__: Final[str] = _get_schema_version()

__all__: Final[list[str]] = [
    # Verzióinformációk
    "__version__",
    "__schema_version__",
    # Interfaces
    "LoggerInterface",
    "LoggerFactoryInterface",
    # Factory
    "LoggerFactory",
    # Exceptions
    "LoggerError",
    "LoggerConfigurationError",
    "LoggerInitializationError",
]
