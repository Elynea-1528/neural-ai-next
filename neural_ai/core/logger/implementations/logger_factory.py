"""Logger factory implementáció.

Ez a modul tartalmazza a logger factory alapértelmezett implementációját,
ami felelős a logger példányok létrehozásáért és konfigurálásáért.
"""

import logging
from typing import Any, Dict, Optional

from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface


class LoggerFactory(LoggerFactoryInterface):
    """Logger factory az alapértelmezett logger példányok kezeléséhez.

    Ez az osztály felelős a DefaultLogger példányok létrehozásáért
    és a globális logger beállítások kezeléséért.
    """

    _loggers: Dict[str, LoggerInterface] = {}

    @staticmethod
    def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
        """Logger példány létrehozása vagy meglévő visszaadása.

        Args:
            name: A logger neve
            config: Opcionális konfiguráció

        Returns:
            LoggerInterface: Új vagy meglévő logger példány
        """
        if name not in LoggerFactory._loggers:
            LoggerFactory._loggers[name] = DefaultLogger(name)

        return LoggerFactory._loggers[name]

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
            console_handler.setLevel(getattr(logging, console_config.get("level", "INFO")))
            console_handler.setFormatter(logging.Formatter(format_str, date_format))
            logging.getLogger().addHandler(console_handler)

        # Fájl handler
        file_config: Dict[str, Any] = handlers_config.get("file", {})
        if file_config.get("enabled", False):
            file_handler: logging.FileHandler = logging.FileHandler(
                filename=file_config.get("filename", "logs/app.log"), encoding="utf-8"
            )
            file_handler.setLevel(getattr(logging, file_config.get("level", "DEBUG")))
            file_handler.setFormatter(logging.Formatter(format_str, date_format))
            logging.getLogger().addHandler(file_handler)
