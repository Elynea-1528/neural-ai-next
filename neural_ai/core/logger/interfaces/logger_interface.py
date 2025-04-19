"""Logger interfész definíció."""

from abc import ABC, abstractmethod
from typing import Any


class LoggerInterface(ABC):
    """Logger interfész.

    Ez az interfész definiálja a loggerek által implementálandó metódusokat.
    """

    @abstractmethod
    def __init__(self, name: str, **kwargs: Any) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            **kwargs: További paraméterek
        """

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """

    @abstractmethod
    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        Args:
            level: Az új log szint
        """

    @abstractmethod
    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint
        """
