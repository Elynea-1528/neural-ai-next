"""Színes konzol logger implementáció.

Ez a modul a ColoredLogger osztályt tartalmazza, amely színes konzol kimenetet
biztosít a log üzenetekhez a Python standard logging könyvtárát felhasználva.
"""

import logging
import sys
from typing import IO, Any

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class ColoredLogger(LoggerInterface):
    """Színes konzol kimenettel rendelkező logger implementáció.

    Ez az osztály a LoggerInterface-t implementálja, és színes formázást alkalmaz
    a log üzenetekhez a konzolon. A színek a log szinttől függenek, ami segít
    a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

    Attributes:
        logger: A belső Python logger objektum
    """

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream: IO[str] = sys.stdout,
        **kwargs: Any,
    ) -> None:
        """Logger inicializálása színes konzol kimenettel.

        Args:
            name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
            level: A log szint (pl. logging.DEBUG, logging.INFO). Alapértelmezett
                értéke a logging.INFO.
            format_str: A log üzenetek formátuma. Alapértelmezett formátum:
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            stream: A kimeneti stream, ahova a logok íródnak. Alapértelmezett
                értéke a sys.stdout.
            **kwargs: További opcionális paraméterek, amelyeket a jövőbeli
                bővíthetőség érdekében elfogad az osztály.

        Példa:
            >>> logger = ColoredLogger("my_app", level=logging.DEBUG)
            >>> logger.info("Alkalmazás elindult")
        """
        self.logger: logging.Logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása, hogy ne legyenek duplikált üzenetek
        for existing_handler in self.logger.handlers[:]:
            self.logger.removeHandler(existing_handler)

        # Log szint beállítása
        self.logger.setLevel(level)

        # Handler beállítása a megadott streammel
        handler: logging.StreamHandler[IO[str]] = logging.StreamHandler(stream)

        # ColoredFormatter alkalmazása a színes kimenethez
        handler.setFormatter(ColoredFormatter(format_str))

        # Handler hozzáadása és propagálás kikapcsolása
        self.logger.addHandler(handler)
        self.logger.propagate = False

        # Ha DEBUG szint van beállítva, a root logger szintjét is állítsuk be
        if level <= logging.DEBUG:
            root_logger: logging.Logger = logging.getLogger()
            root_logger.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Ez a metódus részletes hibakeresési információkat logol, amelyek általában
        csak fejlesztés közben hasznosak.

        Args:
            message: A logolandó debug üzenet.
            **kwargs: További paraméterek, amelyek az extra adatokhoz adhatók
                a log rekordban.

        Példa:
            >>> logger.debug("Adatfeldolgozás elkezdődött", file="data.txt")
        """
        self.logger.debug(message, extra=kwargs if kwargs else None)

    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Ez a metódus általános információkat logol az alkalmazás működéséről.

        Args:
            message: A logolandó info üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.info("Sikeres bejelentkezés", user="admin")
        """
        self.logger.info(message, extra=kwargs if kwargs else None)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Ez a metódus figyelmeztető üzeneteket logol, amelyek nem kritikusak,
        de érdemes rájuk figyelni.

        Args:
            message: A logolandó warning üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.warning("A cache majdnem tele van", usage=85)
        """
        self.logger.warning(message, extra=kwargs if kwargs else None)

    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Ez a metódus hibákat logol, amelyek befolyásolják az alkalmazás
        működését, de nem okoznak leállást.

        Args:
            message: A logolandó error üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.error("Adatbázis kapcsolódási hiba", error=str(e))
        """
        self.logger.error(message, extra=kwargs if kwargs else None)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Ez a metódus kritikus hibákat logol, amelyek az alkalmazás leállását
        okozhatják vagy jelentős problémát jeleznek.

        Args:
            message: A logolandó critical üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.critical("A rendszer leállt", reason="Nincs elég memória")
        """
        self.logger.critical(message, extra=kwargs if kwargs else None)

    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        Ez a metódus lehetővé teszi a log szint dinamikus módosítását futás közben.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO,
                logging.WARNING, logging.ERROR, logging.CRITICAL).

        Példa:
            >>> logger.set_level(logging.DEBUG)
        """
        self.logger.setLevel(level)
        # Handler-ek szintjének frissítése a konzisztencia érdekében
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint numerikus értéke.

        Példa:
            >>> current_level = logger.get_level()
            >>> print(f"Aktuális log szint: {current_level}")
        """
        return self.logger.level
