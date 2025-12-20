"""Rotáló fájl logger implementáció."""

import logging
import os
import shutil
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Any

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class RotatingFileLogger(LoggerInterface):
    """File alapú logger, ami automatikusan rotálja a log fájlokat."""

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Logger inicializálása.

        Args:
            name: Logger neve
            **kwargs: További paraméterek:
                - log_file: Log fájl útvonala (kötelező)
                - level: Log szint (alapértelmezett: INFO)
                - max_bytes: Maximum fájlméret rotálás előtt (alapértelmezett: 1MB)
                - backup_count: Megtartott backup fájlok száma (alapértelmezett: 5)
                - format: Log formátum string
                - rotation_type: Rotáció típusa ('size' vagy 'time', alapértelmezett: 'size')
                - when: Időalapú rotáció esetén az időegység ('S', 'M', 'H', 'D', stb.)
        """
        self.logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # Paraméterek ellenőrzése
        log_file = kwargs.get("log_file")
        if not log_file:
            raise ValueError("log_file parameter is required")

        level = kwargs.get("level", logging.INFO)
        self.logger.setLevel(level)

        # Könyvtár létrehozása ha nem létezik
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_dir.exists():
            os.makedirs(log_dir)

        # Handler létrehozása a rotáció típusa alapján
        rotation_type = kwargs.get("rotation_type", "size")
        if rotation_type not in ["size", "time"]:
            raise ValueError("Invalid rotation_type. Must be 'size' or 'time'")

        if rotation_type == "time":
            handler = TimedRotatingFileHandler(
                str(log_file),
                when=kwargs.get("when", "D"),
                backupCount=kwargs.get("backup_count", 5),
                encoding="utf-8",
            )
        else:  # size alapú rotáció
            handler = RotatingFileHandler(
                str(log_file),
                maxBytes=kwargs.get("max_bytes", 1024 * 1024),  # 1MB
                backupCount=kwargs.get("backup_count", 5),
                encoding="utf-8",
            )

        # Formázó beállítása
        format_str = kwargs.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(logging.Formatter(format_str))
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

    @staticmethod
    def clean_old_logs(log_dir: str | Path) -> None:
        """Régi log fájlok eltávolítása.

        Args:
            log_dir: Log könyvtár útvonala
        """
        log_dir = Path(log_dir)
        if log_dir.exists():
            shutil.rmtree(log_dir)
