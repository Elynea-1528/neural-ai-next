"""Logger implementációk inicializáló modulja.

Ez a modul exportálja a logger komponens implementációit, és biztosítja
a központosított hozzáférést a különböző logger típusokhoz.

A modul a következő főbb komponenseket exportálja:
    - ColoredLogger: Színes konzol kimenetű logger
    - DefaultLogger: Alapértelmezett logger implementáció
    - LoggerFactory: Logger példányok létrehozásáért felelős gyár
    - RotatingFileLogger: Fájl rotálást támogató logger

Használat:
    >>> from neural_ai.core.logger.implementations import LoggerFactory
    >>> logger = LoggerFactory.get_logger("my_app", logger_type="colored")
    >>> logger.info("Alkalmazás elindult")
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
    from neural_ai.core.logger.implementations.default_logger import DefaultLogger
    from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
    from neural_ai.core.logger.implementations.rotating_file_logger import (
        RotatingFileLogger,
    )

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
from neural_ai.core.logger.implementations.rotating_file_logger import (
    RotatingFileLogger,
)

__all__ = [
    "ColoredLogger",
    "DefaultLogger",
    "LoggerFactory",
    "RotatingFileLogger",
]
