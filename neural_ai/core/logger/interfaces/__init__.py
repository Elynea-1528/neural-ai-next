"""Logger interfészek inicializáló modulja.

Ez a modul exportálja a logger komponens által definiált interfészeket,
és biztosítja a csomag verzióinformációinak dinamikus betöltését.
A TYPE_CHECKING blokk segítségével elkerüljük a körkörös importokat.

Verziókezelés:
    A modul automatikusan betölti a csomag verzióját a pyproject.toml-ból
    az importlib.metadata segítségével. Ez biztosítja, hogy a verzió
    mindig szinkronban legyen a projekt konfigurációjával.

Példa használat:
    >>> from neural_ai.core.logger.interfaces import (
    ...     LoggerInterface,
    ...     LoggerFactoryInterface,
    ...     __version__
    ... )
    >>> print(f"Logger interfész verzió: {__version__}")
    Logger interfész verzió: 1.0.0
"""

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.factory_interface import (
        LoggerFactoryInterface,
    )
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Dinamikus verzióbetöltés a pyproject.toml-ból
try:
    __version__ = version("neural-ai-next")
except PackageNotFoundError:
    # Fallback verzió, ha a csomag nincs telepítve (pl. fejlesztés közben)
    __version__ = "1.0.0"

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

__all__ = [
    "LoggerInterface",
    "LoggerFactoryInterface",
    "__version__",
]
