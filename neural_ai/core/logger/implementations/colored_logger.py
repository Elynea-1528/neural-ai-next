"""Színes konzol logger implementáció."""

import logging
import sys
from typing import Any

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class ColoredLogger(LoggerInterface):
    """Színes konzol kimenettel rendelkező logger."""

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        """Logger inicializálása.

        Args:
            name: Logger neve
            level: Log szint
            format_str: Log formátum string
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Handler beállítása
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter(format_str))
        self.logger.addHandler(handler)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A log üzenet
            **kwargs: További paraméterek
        """
        self.logger.critical(message, **kwargs)

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
