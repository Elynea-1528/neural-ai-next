"""Rotáló fájl logger implementáció.

Ez a modul a logger komponens fájl alapú, rotációs implementációját tartalmazza.
A log fájlok automatikusan rotálódnak méret vagy idő alapján.
"""

import glob
import gzip
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Any, Optional, Type, Union

from neural_ai.core.logger.interfaces import LoggerInterface

HandlerType = Union[Type[RotatingFileHandler], Type[TimedRotatingFileHandler]]


class RotatingFileLogger(LoggerInterface):
    """Rotáló fájl alapú logger implementáció.

    Ez az osztály támogatja mind a méret alapú, mind az idő alapú log rotációt.
    A régi log fájlok automatikusan archiválásra kerülnek.
    """

    def __init__(
        self,
        name: str,
        filename: str,
        rotation_type: str = "size",
        max_bytes: int = 1024 * 1024,  # 1MB
        backup_count: int = 5,
        when: str = "midnight",
        encoding: str = "utf-8",
        format_str: Optional[str] = None,
        level: str = "DEBUG",
    ) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            filename: A log fájl útvonala
            rotation_type: Rotáció típusa ("size" vagy "time")
            max_bytes: Maximális fájlméret byte-okban (csak size típusnál)
            backup_count: Megtartandó régi log fájlok száma
            when: Rotáció időpontja (csak time típusnál)
            encoding: Fájl kódolás
            format_str: Opcionális formátum string
            level: Log szint (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Logger létrehozása
        self._logger = logging.Logger(name)  # Új logger példány létrehozása
        self._logger.setLevel(getattr(logging, level))

        # Log könyvtár létrehozása
        log_dir = os.path.dirname(filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Handler létrehozása
        if rotation_type == "time":
            handler_class: HandlerType = TimedRotatingFileHandler
            handler = handler_class(
                filename=filename,
                when=when,
                backupCount=backup_count,
                encoding=encoding,
            )
        else:
            handler = RotatingFileHandler(
                filename=filename,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding=encoding,
            )

        # Formátum string beállítása
        if format_str is None:
            format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)

        # Handler hozzáadása a loggerhez
        self._logger.addHandler(handler)

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

    @staticmethod
    def compress_old_logs(directory: str, pattern: str = "*.log.*") -> None:
        """Régi log fájlok tömörítése.

        Args:
            directory: A log fájlokat tartalmazó könyvtár
            pattern: Log fájl minta
        """
        # Log fájlok keresése
        for log_file in glob.glob(os.path.join(directory, pattern)):
            if not log_file.endswith(".gz"):
                # Tömörítés
                with open(log_file, "rb") as f_in:
                    with gzip.open(f"{log_file}.gz", "wb") as f_out:
                        f_out.writelines(f_in)
                # Eredeti fájl törlése
                os.remove(log_file)
