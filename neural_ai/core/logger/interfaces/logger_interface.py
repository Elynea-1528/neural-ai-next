"""Logger interfész definíció.

Ez a modul definiálja a naplózási funkcionalitást definiáló interfészt, amely
meghatározza a különböző szintű naplózási műveleteket.
"""

from abc import ABC, abstractmethod
from typing import Any


class LoggerInterface(ABC):
    """Logger interfész a naplózási funkcionalitás definiálásához.

    Az interfész definiálja az alapvető naplózási műveleteket különböző
    részletességi szinteken (debug, info, warning, error, critical).
    """

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Információs szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Figyelmeztetés szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        """Kritikus hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
