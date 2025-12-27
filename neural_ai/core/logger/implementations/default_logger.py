"""Alapértelmezett logger implementáció.

Ez a modul a standard logging könyvtár alapú logger implementációt tartalmazza,
amely a Python beépített logging rendszerét használja.
"""

import logging
from typing import Any

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class DefaultLogger(LoggerInterface):
    """Alapértelmezett logger implementáció a Python logging moduljával.

    Ez az osztály a Python standard library logging rendszerét használja,
    és implementálja a LoggerInterface-t. Konfigurálható log szinttel,
    formátummal és stream handlerrel.

    Attributes:
        logger: A belső Python logger objektum
    """

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Logger inicializálása.

        A konstruktor létrehoz egy Python logger objektumot a megadott névvel,
        eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet,
        formátumot és stream handlert a kapott paraméterek alapján.

        Args:
            name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
            **kwargs: Opcionális kulcsszó argumentumok:
                - level (int): Log szint (pl. logging.DEBUG, logging.INFO).
                  Alapértelmezett: logging.INFO.
                - format (str): Log formátum string. Alapértelmezett:
                  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                - stream: Kimeneti stream. Alapértelmezett: sys.stderr.

        Példa:
            >>> logger = DefaultLogger("my_app")
            >>> logger = DefaultLogger("my_app", level=logging.DEBUG)
            >>> logger = DefaultLogger("my_app",
            ...                       format="%(levelname)s: %(message)s")
        """
        self.logger: logging.Logger = logging.getLogger(name)

        # Korábbi handlerek eltávolítása a duplikáció elkerülésére
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Log szint beállítása
        level: int = kwargs.get("level", logging.INFO)
        self.logger.setLevel(level)

        # Handler hozzáadása ha nincs még
        if not self.logger.handlers:
            stream = kwargs.get("stream")
            handler = logging.StreamHandler(stream)
            formatter = logging.Formatter(
                kwargs.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Propagate kikapcsolása a duplikált üzenetek elkerülésére
        self.logger.propagate = False

        # DI Container kompatibilitás: _initialized flag beállítása
        self._initialized = True

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.debug("Hibakeresési üzenet", user_id=123)
        """
        self.logger.debug(message, extra=kwargs if kwargs else None)

    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.info("Sikeres művelet", duration=0.5)
        """
        self.logger.info(message, extra=kwargs if kwargs else None)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.warning("Elavult API hívás", version="1.0")
        """
        self.logger.warning(message, extra=kwargs if kwargs else None)

    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.error("Adatbázis kapcsolat hiba", db="main")
        """
        self.logger.error(message, extra=kwargs if kwargs else None)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.critical("Kritikus rendszerhiba", component="auth")
        """
        self.logger.critical(message, extra=kwargs if kwargs else None)

    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        A metódus beállítja a logger és a hozzá tartozó handler minimális
        log szintjét. Ez határozza meg, hogy melyik szintű üzenetek kerüljenek
        naplózásra.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO,
                logging.WARNING, logging.ERROR, logging.CRITICAL).

        Példa:
            >>> logger.set_level(logging.DEBUG)
        """
        self.logger.setLevel(level)
        # Handler szintjének is beállítása konzisztencia érdekében
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint numerikus értéke. A visszaadott érték
                a logging modul konstansainak egyike (pl. logging.INFO -> 20).

        Példa:
            >>> level = logger.get_level()
            >>> print(f"Aktuális log szint: {level}")
        """
        return self.logger.level
