"""Logger interfészek inicializáló modulja.

Ez a modul exportálja a logger komponens által definiált interfészeket.
A TYPE_CHECKING blokk segítségével elkerüljük a körkörös importokat.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.factory_interface import (
        LoggerFactoryInterface,
    )
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

__all__ = [
    "LoggerInterface",
    "LoggerFactoryInterface",
]
