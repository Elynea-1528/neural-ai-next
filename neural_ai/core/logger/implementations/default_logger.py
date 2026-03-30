"""Alapértelmezett logger implementáció.

Ez a modul a standard logging könyvtár alapú logger implementációt tartalmazza,
amely a Python beépített logging rendszerét használja.
"""

import logging
from typing import TYPE_CHECKING, Any

import structlog

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface


class DefaultLogger(LoggerInterface):
    """Alapértelmezett logger implementáció a Python logging moduljával.

    Ez az osztály a Python standard library logging rendszerét használja,
    és implementálja a LoggerInterface-t. Konfigurálható log szinttel,
    formátummal és stream handlerrel.

    Attributes:
        logger: A belső Python logger objektum
    """

    def __init__(
        self,
        name: str,
        config: "ConfigManagerInterface | None" = None,
        event_bus: "EventBusInterface | None" = None,
        level: int = logging.INFO,
        **kwargs: Any,
    ) -> None:
        """Logger inicializálása.

        A konstruktor létrehoz egy Python logger objektumot a megadott névvel,
        eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet,
        formátumot és stream handlert a kapott paraméterek alapján.

        Args:
            name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
            config: Opcionális konfigurációs interfész.
            event_bus: Opcionális esemény busz interfész.
            level: A logger alapértelmezett szintje (pl. logging.DEBUG, logging.INFO).
            **kwargs: Opcionális kulcsszó argumentumok:
                - format (str): Log formátum string. Alapértelmezett:
                  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                - stream: Kimeneti stream. Alapértelmezett: sys.stderr.

        Példa:
            >>> logger = DefaultLogger("my_app")
            >>> logger = DefaultLogger("my_app", level=logging.DEBUG)
            >>> logger = DefaultLogger("my_app",
            ...                       format="%(levelname)s: %(message)s")
        """
        # Standard logging.Logger létrehozása (kompatibilitás miatt)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Structlog wrapper a strukturált logoláshoz
        self._structlog = structlog.get_logger(name)

        # A központi LoggerFactory.configure() intézi a handler-eket és formázást
        # Structlog automatikusan kezeli a színes kimenetet és JSON logging-ot

        # DI: függőségek tárolása
        self._config = config
        self._event_bus = event_bus
        self._level = level

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
        # Standard logger (tesztek miatt)
        self.logger.debug(message, extra=kwargs if kwargs else None)
        # Structlog (strukturált logolás)
        self._structlog.debug(message, extra=kwargs if kwargs else None)

    def info(self, message: str, **kwargs: Any) -> None:
        """Info szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.info("Sikeres művelet", duration=0.5)
        """
        # Standard logger (tesztek miatt)
        self.logger.info(message, extra=kwargs if kwargs else None)
        # Structlog (strukturált logolás)
        self._structlog.info(message, extra=kwargs if kwargs else None)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.warning("Elavult API hívás", version="1.0")
        """
        # Standard logger (tesztek miatt)
        self.logger.warning(message, extra=kwargs if kwargs else None)
        # Structlog (strukturált logolás)
        self._structlog.warning(message, extra=kwargs if kwargs else None)

    def error(self, message: str, **kwargs: Any) -> None:
        """Error szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek. Ha exc_info van, külön kezeljük.

        Példa:
            >>> logger.error("Adatbázis kapcsolat hiba", db="main")
        """
        exc_info = kwargs.pop("exc_info", None)
        # Standard logger (tesztek miatt)
        self.logger.error(message, exc_info=exc_info, extra=kwargs if kwargs else None)
        # Structlog (strukturált logolás)
        self._structlog.error(message, exc_info=exc_info, extra=kwargs if kwargs else None)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek. Ha exc_info van, külön kezeljük.

        Példa:
            >>> logger.critical("Kritikus rendszerhiba", component="auth")
        """
        exc_info = kwargs.pop("exc_info", None)
        # Standard logger (tesztek miatt)
        self.logger.critical(message, exc_info=exc_info, extra=kwargs if kwargs else None)
        # Structlog (strukturált logolás)
        self._structlog.critical(message, exc_info=exc_info, extra=kwargs if kwargs else None)

    def set_level(self, level: int) -> None:
        """Logger log szintjének beállítása.

        Beállítja a logger szintjét a példány szintjén.

        Args:
            level: Az új log szint.

        Példa:
            >>> logger.set_level(logging.DEBUG)
        """
        self._level = level
        self.logger.setLevel(level)

    def get_level(self) -> int:
        """Aktuális log szint lekérése.

        Visszaadja a konstruktorban beállított log szintet.

        Returns:
            int: A beállított log szint.

        Példa:
            >>> level = logger.get_level()
            >>> print(f"Aktuális log szint: {level}")
        """
        return self._level
