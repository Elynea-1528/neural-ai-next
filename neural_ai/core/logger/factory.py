"""Logger factory implementáció structlog használatával.

Ez a modul biztosítja a LoggerFactory osztályt, amely felelős a különböző
típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve
lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

A factory kizárólag structlog renderereket használ:
- Console: structlog.dev.ConsoleRenderer(colors=True)
- File: structlog.processors.JSONRenderer()
"""

import logging
import sys
from typing import Any, cast

import structlog
from structlog.processors import JSONRenderer
from structlog.stdlib import ProcessorFormatter
from structlog.types import Processor

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.rotating_file_logger import (
    RotatingFileLogger,
)


class LoggerFactory(LoggerFactoryInterface):
    """Factory osztály loggerek létrehozásához structlog-gal.

    A factory mintát követve centralizálja a logger példányosítást és
    életciklus kezelést. Támogatja a különböző logger implementációk
    regisztrálását és lekérdezését.

    A configure metódus kizárólag structlog renderereket használ:
    - Console: structlog.dev.ConsoleRenderer(colors=True)
    - File: structlog.processors.JSONRenderer()

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
        """Logger rendszer konfigurálása structlog-gal.

        A metódus kizárólag structlog renderereket használ:
        - Console: structlog.dev.ConsoleRenderer(colors=True)
        - File: structlog.processors.JSONRenderer()

        Args:
            config: Konfigurációs dict a következő struktúrával:
                {
                    'default_level': 'DEBUG',
                    'handlers': {
                        'console': {
                            'enabled': True,
                            'level': 'DEBUG',
                            'colored': True
                        },
                        'file': {
                            'enabled': True,
                            'filename': 'logs/neural_ai.log',
                            'level': 'DEBUG',
                            'json_format': True,
                            'rotating': True,
                            'max_bytes': 10485760,
                            'backup_count': 5
                        }
                    },
                    'loggers': {
                        'neural_ai': {'level': 'DEBUG', 'propagate': True},
                        'aiosqlite': {'level': 'WARNING'},
                        'asyncio': {'level': 'WARNING'}
                    }
                }
        """
        from pathlib import Path

        # Alap structlog konfiguráció
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Alap beállítások
        default_level = getattr(logging, config.get("default_level", "DEBUG"))

        # Root logger konfigurálása
        root_logger = logging.getLogger()
        root_logger.setLevel(default_level)

        # Meglévő handlerek törlése, hogy ne legyenek duplikálva
        root_logger.handlers.clear()

        # Handlerek beállítása
        handlers = config.get("handlers", {})

        # Console handler structlog-gal
        console_config = handlers.get("console", {})
        if console_config.get("enabled", False):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, console_config.get("level", "DEBUG")))

            # Console renderer - mindig színes
            console_processors: list[Processor] = [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ]

            console_handler.setFormatter(
                ProcessorFormatter(
                    foreign_pre_chain=[],
                    processors=console_processors,
                )
            )

            root_logger.addHandler(console_handler)

        # File handler structlog-gal
        file_config = handlers.get("file", {})
        if file_config.get("enabled", False):
            filename = file_config.get("filename")
            if filename:
                # Mappa létrehozása, ha nem létezik
                file_path = Path(filename)
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Rotating file handler ellenőrzése
                if file_config.get("rotating", False):
                    from logging.handlers import RotatingFileHandler

                    max_bytes = file_config.get("max_bytes", 10485760)
                    backup_count = file_config.get("backup_count", 5)
                    file_handler = RotatingFileHandler(
                        filename, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
                    )
                else:
                    file_handler = logging.FileHandler(filename, encoding="utf-8")

                file_handler.setLevel(getattr(logging, file_config.get("level", "DEBUG")))

                # File renderer - mindig JSON
                file_processors: list[Processor] = [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    JSONRenderer(),
                ]

                file_handler.setFormatter(
                    ProcessorFormatter(
                        foreign_pre_chain=[],
                        processors=file_processors,
                    )
                )

                root_logger.addHandler(file_handler)

        # Egyedi logger konfigurációk beállítása
        loggers_config = config.get("loggers", {})
        for logger_name, logger_settings in loggers_config.items():
            logger_instance = logging.getLogger(logger_name)
            if "level" in logger_settings:
                logger_instance.setLevel(getattr(logging, logger_settings["level"]))
            if "propagate" in logger_settings:
                logger_instance.propagate = logger_settings["propagate"]

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