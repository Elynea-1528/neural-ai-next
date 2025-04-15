"""Logger interfészek inicializáló modulja.

Ez a modul exportálja a logger komponens által definiált interfészeket.
"""

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

__all__ = [
    "LoggerInterface",
    "LoggerFactoryInterface",
]
