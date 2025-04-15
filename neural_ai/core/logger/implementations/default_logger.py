"""Alapértelmezett logger implementáció.

Ez a modul tartalmazza a logger komponens alapértelmezett implementációját,
ami a Python standard library logging moduljára épül.
"""

import logging
from typing import Any

from neural_ai.core.logger.interfaces import LoggerInterface


class DefaultLogger(LoggerInterface):
    """Standard library alapú logger implementáció.

    Ez az osztály a Python beépített logging modulját használja
    a naplózási műveletek megvalósításához.
    """

    def __init__(self, name: str) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
        """
        self._logger: logging.Logger = logging.getLogger(name)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        self._logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Információs szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        self._logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Figyelmeztetés szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        self._logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        self._logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Kritikus hiba szintű üzenet logolása.

        Args:
            message: A naplózandó üzenet
            **kwargs: További kontextus információk
        """
        self._logger.critical(message, extra=kwargs)
