"""Rotáló fájl logger implementáció."""

import logging
import os
import shutil
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Literal

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class RotatingFileLogger(LoggerInterface):
    """File alapú logger, ami automatikusan rotálja a log fájlokat.

    A logger támogatja a méret alapú és idő alapú rotációt is. A méret alapú
    rotáció esetén a fájl elér egy bizonyos méretet, az idő alapú rotáció
    esetén pedig egy adott időközönként történik a rotáció.

    Attributes:
        logger: A Python logging logger példány
    """

    def __init__(
        self,
        name: str,
        log_file: str,
        level: int = logging.INFO,
        max_bytes: int = 1024 * 1024,  # 1MB
        backup_count: int = 5,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        rotation_type: Literal["size", "time"] = "size",
        when: str = "D",
        **kwargs: object,
    ) -> None:
        """Logger inicializálása.

        Args:
            name: A logger egyedi neve.
            log_file: A log fájl teljes útvonala.
            level: A log szint (alapértelmezett: INFO).
            max_bytes: Maximum fájlméret bájtban rotálás előtt (méret alapú rotációhoz).
            backup_count: Megtartott backup fájlok száma.
            format_str: A log üzenetek formátuma.
            rotation_type: A rotáció típusa ('size' vagy 'time').
            when: Időegység időalapú rotáció esetén ('S', 'M', 'H', 'D', stb.).
            **kwargs: További paraméterek (az interfész kompatibilitás miatt).

        Raises:
            ValueError: Ha a log_file nincs megadva vagy érvénytelen a rotation_type.
        """
        self.logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Paraméterek ellenőrzése
        if not log_file:
            raise ValueError("A 'log_file' paraméter kötelező")

        self.logger.setLevel(level)

        # Könyvtár létrehozása ha nem létezik
        log_path = Path(log_file)
        log_dir = log_path.parent
        if not log_dir.exists():
            os.makedirs(log_dir)

        # Handler létrehozása a rotáció típusa alapján
        if rotation_type not in ["size", "time"]:
            raise ValueError("Érvénytelen rotation_type. 'size' vagy 'time' lehet.")

        if rotation_type == "time":
            handler = TimedRotatingFileHandler(
                str(log_file),
                when=when,
                backupCount=backup_count,
                encoding="utf-8",
            )
        else:  # size alapú rotáció
            handler = RotatingFileHandler(
                str(log_file),
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )

        # Formázó beállítása
        handler.setFormatter(logging.Formatter(format_str))
        self.logger.addHandler(handler)

        # Propagate kikapcsolása a duplikált üzenetek elkerülésére
        self.logger.propagate = False

    def debug(self, message: str, **kwargs: object) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).
        """
        if kwargs:
            self.logger.debug(message, extra=kwargs)
        else:
            self.logger.debug(message)

    def info(self, message: str, **kwargs: object) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).
        """
        if kwargs:
            self.logger.info(message, extra=kwargs)
        else:
            self.logger.info(message)

    def warning(self, message: str, **kwargs: object) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).
        """
        if kwargs:
            self.logger.warning(message, extra=kwargs)
        else:
            self.logger.warning(message)

    def error(self, message: str, **kwargs: object) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).
        """
        if kwargs:
            self.logger.error(message, extra=kwargs)
        else:
            self.logger.error(message)

    def critical(self, message: str, **kwargs: object) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).
        """
        if kwargs:
            self.logger.critical(message, extra=kwargs)
        else:
            self.logger.critical(message)

    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO).
        """
        self.logger.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            Az aktuális log szint értéke.
        """
        return self.logger.level

    @staticmethod
    def clean_old_logs(log_dir: str | Path) -> None:
        """Régi log fájlok eltávolítása.

        Figyelmeztetés: Ez a metódus véglegesen törli a log könyvtárat
        és annak teljes tartalmát!

        Args:
            log_dir: A log könyvtár útvonala.
        """
        log_dir = Path(log_dir)
        if log_dir.exists():
            shutil.rmtree(log_dir)
