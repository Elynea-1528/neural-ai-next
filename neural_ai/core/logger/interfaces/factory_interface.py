"""Logger factory interfész.

Ez az interfész definiálja a logger factory-k alapvető működését,
beleértve a logger típusok regisztrálását, példányosítását és
a logger rendszer konfigurálását.
"""

from abc import ABC, abstractmethod
from typing import Any

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class LoggerFactoryInterface(ABC):
    """Logger factory interfész.

    Az interfész lehetővé teszi különböző logger implementációk
    dinamikus regisztrálását és példányosítását factory pattern
    segítségével.
    """

    @classmethod
    @abstractmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása a factory számára.

        Args:
            logger_type: A logger típus egyedi azonosítója
            logger_class: A logger osztály, amely implementálja a LoggerInterface-t

        Raises:
            ValueError: Ha a logger_type már létezik
            TypeError: Ha a logger_class nem implementálja a LoggerInterface-t
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása vagy visszaadása.

        Args:
            name: A logger egyedi neve
            logger_type: A kért logger típus (alapértelmezett: "default")
            **kwargs: További paraméterek a logger inicializálásához

        Returns:
            LoggerInterface: Az inicializált logger példány

        Raises:
            KeyError: Ha a logger_type nincs regisztrálva
            ValueError: Ha a name üres string
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása.

        Args:
            config: Konfigurációs beállítások dictionary formátumban

        Raises:
            ValueError: Ha a konfiguráció érvénytelen
        """
        raise NotImplementedError
