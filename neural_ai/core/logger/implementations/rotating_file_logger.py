"""Rotáló fájl logger implementáció."""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Union

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class RotatingFileLogger(LoggerInterface):
    """File alapú logger, ami automatikusan rotálja a log fájlokat."""

    def __init__(
        self,
        name: str,
        log_file: Union[str, Path],
        level: int = logging.INFO,
        max_bytes: int = 1024 * 1024,  # 1MB
        backup_count: int = 5,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        """Logger inicializálása.

        Args:
            name: Logger neve
            log_file: Log fájl útvonala
            level: Log szint
            max_bytes: Maximum fájlméret rotálás előtt
            backup_count: Megtartott backup fájlok száma
            format_str: Log formátum string
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Könyvtár létrehozása ha nem létezik
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_dir.exists():
            os.makedirs(log_dir)

        # Handler beállítása
        handler = RotatingFileHandler(
            str(log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter(format_str))
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
