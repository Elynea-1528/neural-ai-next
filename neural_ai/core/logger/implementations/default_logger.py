"""Alapértelmezett logger implementáció."""

import logging
from typing import Any

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class DefaultLogger(LoggerInterface):
    """Alapértelmezett logger implementáció."""

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            **kwargs: További paraméterek:
                - level: Log szint (alapértelmezett: INFO)
                - format: Log formátum string
        """
        self.logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # Log szint beállítása
        level = kwargs.get("level", logging.INFO)
        self.logger.setLevel(level)

        # Handler hozzáadása ha nincs még
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                kwargs.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Propagate kikapcsolása a duplikált üzenetek elkerülésére
        self.logger.propagate = False

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.debug(message, extra=kwargs if kwargs else None)

    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.info(message, extra=kwargs if kwargs else None)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.warning(message, extra=kwargs if kwargs else None)

    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.error(message, extra=kwargs if kwargs else None)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.critical(message, extra=kwargs if kwargs else None)

    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        Args:
            level: Az új log szint
        """
        self.logger.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint
        """
        return self.logger.level
