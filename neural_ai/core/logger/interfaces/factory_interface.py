"""Logger factory interfész."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class LoggerFactoryInterface(ABC):
    """Logger factory interfész."""

    @classmethod
    @abstractmethod
    def register_logger(cls, logger_type: str, logger_class: Type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása.

        Args:
            logger_type: A logger típus neve
            logger_class: A logger osztály
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása vagy visszaadása.

        Args:
            name: A logger neve
            logger_type: A kért logger típus
            **kwargs: További paraméterek a loggernek

        Returns:
            LoggerInterface: Az inicializált logger
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def configure(cls, config: Dict[str, Any]) -> None:
        """Logger rendszer konfigurálása.

        Args:
            config: Konfigurációs beállítások
        """
        raise NotImplementedError
