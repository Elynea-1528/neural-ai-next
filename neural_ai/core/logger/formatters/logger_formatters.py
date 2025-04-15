"""Logger formázók.

Ez a modul tartalmazza a különböző logger formázókat, amelyek
a log üzenetek megjelenítését vezérlik (pl. színes kimenet).
"""

import logging
from typing import Dict


class ColoredFormatter(logging.Formatter):
    """Színes megjelenítést biztosító formatter.

    Különböző színekkel jelöli a különböző log szinteket:
    - DEBUG: Kék
    - INFO: Zöld
    - WARNING: Sárga
    - ERROR: Piros
    - CRITICAL: Piros (háttér)
    """

    # ANSI színkódok
    COLORS: Dict[int, str] = {
        logging.DEBUG: "\033[94m",  # Kék
        logging.INFO: "\033[92m",  # Zöld
        logging.WARNING: "\033[93m",  # Sárga
        logging.ERROR: "\033[91m",  # Piros
        logging.CRITICAL: "\033[97;41m",  # Fehér szöveg piros háttéren
    }
    RESET: str = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Log rekord formázása színes kimenettel.

        Args:
            record: A formázandó log rekord

        Returns:
            str: A színes formázott log üzenet
        """
        # Eredeti üzenet formázása
        message: str = super().format(record)

        # Színkód hozzáadása a megfelelő szinthez
        if record.levelno in self.COLORS:
            message = f"{self.COLORS[record.levelno]}{message}{self.RESET}"

        return message
