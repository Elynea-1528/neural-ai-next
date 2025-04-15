"""Logger interfész definíció.

Ez a modul definiálja a naplózási funkcionalitás interfészét, amely
meghatározza a különböző szintű naplózási műveleteket.
"""

from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """Logger interfész a naplózási funkcionalitás definiálásához.

    Az interfész definiálja az alapvető naplózási műveleteket különböző
    részletességi szinteken (debug, info, warning, error, critical).
    """

    @abstractmethod
    def debug(self, message: str, **kwargs) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def info(self, message: str, **kwargs) -> None:
        """Információs szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None:
        """Figyelmeztetés szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> None:
        """Hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs) -> None:
        """Kritikus hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        pass
