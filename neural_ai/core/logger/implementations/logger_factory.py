"""Logger factory implementáció.

Ez a modul biztosítja a logger factory osztályt, amely felelős a különböző
típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve
lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.
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
    """Factory osztály loggerek létrehozásához."""

    _logger_types: dict[str, type[LoggerInterface]] = cast(
        dict[str, type[LoggerInterface]],
        {
            "default": DefaultLogger,
            "colored": ColoredLogger,
            "rotating": RotatingFileLogger,
        },
    )

    _instances: dict[str, LoggerInterface] = {}

    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása.

        Args:
            logger_type: A logger típus neve
            logger_class: A logger osztály
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
            name: A logger neve
            logger_type: A kért logger típus
            **kwargs: További paraméterek a loggernek

        Returns:
            LoggerInterface: Az inicializált logger
        """
        # Ha már létezik ilyen nevű logger, azt adjuk vissza
        if name in cls._instances:
            return cls._instances[name]

        # Ha nincs megadott típus vagy nem létezik, használjuk az alapértelmezettet
        if logger_type not in cls._logger_types:
            logger_type = "default"

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
