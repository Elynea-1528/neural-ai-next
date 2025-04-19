"""Színes konzol logger implementáció."""

import logging
import sys
from typing import Any

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class ColoredLogger(LoggerInterface):
    """Színes konzol kimenettel rendelkező logger."""

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            **kwargs: További paraméterek:
                - level: Log szint (alapértelmezett: INFO)
                - format: Log formátum string
                - stream: Kimeneti stream (alapértelmezett: sys.stdout)
        """
        self.logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # Log szint beállítása
        level = kwargs.get("level", logging.INFO)
        self.logger.setLevel(level)

        # Handler beállítása
        stream = kwargs.get("stream", sys.stdout)
        handler = logging.StreamHandler(stream)

        # Formázó beállítása
        format_str = kwargs.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(ColoredFormatter(format_str))

        # Handler hozzáadása és propagálás kikapcsolása
        self.logger.addHandler(handler)
        self.logger.propagate = False

        # Debug mód bekapcsolása ha szükséges
        if level <= logging.DEBUG:
            # Root logger és handler szintjének beállítása
            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)

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
        # Handler-ek szintjének frissítése
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint
        """
        return self.logger.level
