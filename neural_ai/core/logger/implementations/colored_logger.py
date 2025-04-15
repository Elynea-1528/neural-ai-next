"""Színes logger implementáció.

Ez a modul a logger komponens színes megjelenítést biztosító implementációját tartalmazza.
"""

import logging
import sys
from typing import Any, Optional

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.interfaces import LoggerInterface


class ColoredLogger(LoggerInterface):
    """Színes megjelenítést biztosító logger implementáció.

    Ez az osztály a standard logging modult használja színes konzol kimenettel.
    A különböző log szintek különböző színekkel jelennek meg.
    """

    def __init__(self, name: str, format_str: Optional[str] = None) -> None:
        """Logger inicializálása.

        Args:
            name: A logger neve
            format_str: Opcionális formátum string. Ha nincs megadva, az alapértelmezett
                       formátumot használja.
        """
        self._logger: logging.Logger = logging.getLogger(name)

        # Ha nincs még handler, hozzáadjuk a konzol handlert színes formázással
        if not self._logger.handlers:
            # Konzol handler létrehozása
            console_handler = logging.StreamHandler(sys.stdout)

            # Formátum string beállítása
            if format_str is None:
                format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

            # Színes formatter beállítása
            formatter = ColoredFormatter(format_str)
            console_handler.setFormatter(formatter)

            # Handler hozzáadása a loggerhez
            self._logger.addHandler(console_handler)

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
