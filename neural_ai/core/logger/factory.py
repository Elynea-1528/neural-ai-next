"""Logger factory implementáció.

Ez a modul biztosítja a LoggerFactory osztályt, amely felelős a különböző
típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve
lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

A factory támogatja a következő logger típusokat:
- default: Alapértelmezett konzol logger
- colored: Színes kimenetű konzol logger
- rotating: Fájlba író, automatikusan rotáló logger
"""

import logging
import sys
from typing import TYPE_CHECKING, Any, cast

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

if TYPE_CHECKING:
    from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
    from neural_ai.core.logger.implementations.default_logger import DefaultLogger
    from neural_ai.core.logger.implementations.rotating_file_logger import (
        RotatingFileLogger,
    )
else:
    from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
    from neural_ai.core.logger.implementations.default_logger import DefaultLogger
    from neural_ai.core.logger.implementations.rotating_file_logger import (
        RotatingFileLogger,
    )


class LoggerFactory(LoggerFactoryInterface):
    """Factory osztály loggerek létrehozásához.

    A factory mintát követve centralizálja a logger példányosítást és
    életciklus kezelést. Támogatja a különböző logger implementációk
    regisztrálását és lekérdezését.

    Attributes:
        _logger_types: Regisztrált logger típusok és osztályaik.
        _instances: Létrehozott logger példányok gyorsítótárban.
    """

    _logger_types: dict[str, type[LoggerInterface]] = cast(
        dict[str, type[LoggerInterface]],
        {
            "default": DefaultLogger,
            "colored": ColoredLogger,
            "rotating": RotatingFileLogger,
        },
    )

    _instances: dict[str, LoggerInterface] = {}
    _schema_version: str = "1.0.0"

    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása.

        Args:
            logger_type: A logger típus neve.
            logger_class: A logger osztály.

        Raises:
            TypeError: Ha a logger_class nem implementálja a LoggerInterface-t.
        """
        cls._logger_types[logger_type] = logger_class

    @classmethod
    def get_logger(
        cls,
        name: str,
        logger_type: str = "default",
        **kwargs: Any,
    ) -> LoggerInterface:
        """Logger példány létrehozása vagy visszaadása.

        Args:
            name: A logger egyedi neve.
            logger_type: A kért logger típus ('default', 'colored', 'rotating').
            **kwargs: További paraméterek a loggernek (pl. log_file, level).

        Returns:
            LoggerInterface: Az inicializált logger példány.

        Raises:
            ValueError: Ha a 'rotating' típushoz nincs megadva 'log_file'.
            TypeError: Ha a létrehozott logger nem implementálja az interfészt.

        Példa:
            >>> logger = LoggerFactory.get_logger("my_app")
            >>> colored = LoggerFactory.get_logger("app", logger_type="colored")
            >>> file_logger = LoggerFactory.get_logger(
            ...     "file_app",
            ...     logger_type="rotating",
            ...     log_file="/var/log/app.log"
            ... )
        """
        # Ha már létezik ilyen nevű logger, azt adjuk vissza
        if name in cls._instances:
            return cls._instances[name]

        # Ha nincs megadott típus vagy nem létezik, használjuk az alapértelmezettet
        if logger_type not in cls._logger_types:
            logger_type = "default"

        # Rotating logger esetén kötelező a log_file paraméter
        if logger_type == "rotating" and "log_file" not in kwargs:
            raise ValueError(
                "A 'rotating' logger típushoz kötelező megadni a 'log_file' paramétert"
            )

        logger_class = cls._logger_types[logger_type]
        logger = logger_class(name=name, **kwargs)

        cls._instances[name] = logger
        return logger

    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása.

        Args:
            config: Konfigurációs dict a következő struktúrával:
                {
                    'default_level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'date_format': '%Y-%m-%d %H:%M:%S',
                    'handlers': {
                        'console': {
                            'enabled': True,
                            'level': 'INFO'
                        },
                        'file': {
                            'enabled': True,
                            'filename': 'app.log',
                            'level': 'DEBUG'
                        }
                    }
                }
        """
        # Alap beállítások
        default_level = getattr(logging, config.get("default_level", "INFO"))
        log_format = config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        date_format = config.get("date_format", "%Y-%m-%d %H:%M:%S")

        # Root logger konfigurálása
        logging.basicConfig(
            level=default_level,
            format=log_format,
            datefmt=date_format,
        )

        # Handlerek beállítása
        handlers = config.get("handlers", {})
        root_logger = logging.getLogger()

        # Console handler
        console_config = handlers.get("console", {})
        if console_config.get("enabled", False):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, console_config.get("level", "INFO")))
            console_handler.setFormatter(logging.Formatter(log_format))
            root_logger.addHandler(console_handler)

        # File handler
        file_config = handlers.get("file", {})
        if file_config.get("enabled", False):
            filename = file_config.get("filename")
            if filename:
                file_handler = logging.FileHandler(filename)
                file_handler.setLevel(getattr(logging, file_config.get("level", "DEBUG")))
                file_handler.setFormatter(logging.Formatter(log_format))
                root_logger.addHandler(file_handler)

    @classmethod
    def get_schema_version(cls) -> str:
        """A logger factory sémaváltozatának lekérdezése.

        Returns:
            str: A sémaváltozat string formátumban (pl. '1.0.0').
        """
        return cls._schema_version

    @classmethod
    def set_schema_version(cls, version: str) -> None:
        """A logger factory sémaváltozatának beállítása.

        Args:
            version: Az új sémaváltozat (pl. '1.1.0').
        """
        cls._schema_version = version

    @classmethod
    def clear_instances(cls) -> None:
        """Összes logger példány törlése a gyorsítótárból.

        Ez a metódus hasznos teszteléskor vagy amikor teljesen
        új logger példányokat szeretnénk létrehozni.
        """
        cls._instances.clear()

    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Regisztrált logger típusok listázása.

        Returns:
            list[str]: A regisztrált logger típusok neveinek listája.
        """
        return list(cls._logger_types.keys())

    @classmethod
    def is_logger_registered(cls, logger_type: str) -> bool:
        """Ellenőrzi, hogy egy logger típus regisztrálva van-e.

        Args:
            logger_type: A logger típus neve.

        Returns:
            bool: True, ha a logger típus regisztrálva van, egyébként False.
        """
        return logger_type in cls._logger_types
