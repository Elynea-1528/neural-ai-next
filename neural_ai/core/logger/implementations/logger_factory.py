"""Logger factory implementáció.

Ez a modul tartalmazza a logger factory alapértelmezett implementációját,
ami felelős a logger példányok létrehozásáért és konfigurálásáért.
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, Union

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface


class LoggerFactory(LoggerFactoryInterface):
    """Logger factory az logger példányok kezeléséhez.

    Ez az osztály felelős a különböző logger implementációk példányainak
    létrehozásáért és a globális logger beállítások kezeléséért.
    """

    _loggers: Dict[str, LoggerInterface] = {}

    # pylint: disable=undefined-variable
    @staticmethod
    def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
        """Logger példány létrehozása vagy meglévő visszaadása.

        Args:
            name: A logger neve
            config: Opcionális konfiguráció. A következő kulcsokat támogatja:
                   - type: Logger típusa ("default", "colored", "rotating")
                   - format: Log formátum
                   - rotation_type: Rotáció típusa ("size" vagy "time")
                   - max_bytes: Maximum fájlméret
                   - backup_count: Backup fájlok száma
                   - when: Időalapú rotáció időpontja
                   - filename: Log fájl neve (rotating logger esetén)

        Returns:
            LoggerInterface: Új vagy meglévő logger példány
        """
        if name not in LoggerFactory._loggers:
            config = config or {}
            logger_type = config.get("type", "default")
            format_str = config.get("format")

            if logger_type == "colored":
                LoggerFactory._loggers[name] = ColoredLogger(name, format_str)
            elif logger_type == "rotating":
                LoggerFactory._loggers[name] = RotatingFileLogger(
                    name=name,
                    filename=config.get("filename", "logs/app.log"),
                    rotation_type=config.get("rotation_type", "size"),
                    max_bytes=config.get("max_bytes", 1024 * 1024),
                    backup_count=config.get("backup_count", 5),
                    when=config.get("when", "midnight"),
                    format_str=format_str,
                )
            else:  # default logger
                LoggerFactory._loggers[name] = DefaultLogger(name)

        return LoggerFactory._loggers[name]

    # pylint: disable=undefined-variable
    @staticmethod
    def configure(config: Dict[str, Any]) -> None:
        """Globális logger konfiguráció beállítása.

        Args:
            config: A logger rendszer konfigurációja
        """
        level: str = config.get("default_level", "INFO")
        default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        format_str: str = config.get("format", default_format)
        date_format: str = config.get("date_format", "%Y-%m-%d %H:%M:%S")

        # Alap konfiguráció beállítása
        logging.basicConfig(level=getattr(logging, level), format=format_str, datefmt=date_format)

        # Handler-ek konfigurálása
        handlers_config: Dict[str, Any] = config.get("handlers", {})

        # Konzol handler
        console_config: Dict[str, Any] = handlers_config.get("console", {})
        if console_config.get("enabled", True):
            console_handler: logging.StreamHandler = logging.StreamHandler()
            if console_config.get("colored", False):
                console_handler.setFormatter(ColoredFormatter(format_str))
            else:
                console_handler.setFormatter(logging.Formatter(format_str, date_format))
            console_handler.setLevel(getattr(logging, console_config.get("level", "INFO")))
            logging.getLogger().addHandler(console_handler)

        # Fájl handler
        file_config: Dict[str, Any] = handlers_config.get("file", {})
        if file_config.get("enabled", False):
            handler: Union[logging.FileHandler, RotatingFileHandler]
            if file_config.get("rotating", False):
                handler = RotatingFileHandler(
                    filename=file_config.get("filename", "logs/app.log"),
                    maxBytes=file_config.get("max_bytes", 1024 * 1024),
                    backupCount=file_config.get("backup_count", 5),
                    encoding="utf-8",
                )
            else:
                handler = logging.FileHandler(
                    filename=file_config.get("filename", "logs/app.log"), encoding="utf-8"
                )
            handler.setFormatter(logging.Formatter(format_str, date_format))
            handler.setLevel(getattr(logging, file_config.get("level", "DEBUG")))
            logging.getLogger().addHandler(handler)
