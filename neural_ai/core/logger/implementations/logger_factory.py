"""Logger factory implementáció."""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class LoggerFactory:
    """Factory osztály loggerek létrehozásához."""

    @staticmethod
    def get_logger(
        name: str,
        config: Optional[Dict[str, Any]] = None,
        default_path: Optional[Union[str, Path]] = None,
    ) -> LoggerInterface:
        """Logger példány létrehozása.

        Args:
            name: Logger neve
            config: Logger konfiguráció
            default_path: Alapértelmezett log fájl útvonal

        Returns:
            LoggerInterface: A létrehozott logger
        """
        config = config or {}

        # Log szint beállítása
        level = getattr(logging, config.get("level", "INFO").upper())

        # Log fájl útvonal meghatározása
        log_file = config.get("log_file") or default_path

        # Logger típus kiválasztása
        logger_type = config.get("type", "default").lower()

        # Ha van log fájl megadva, használjunk RotatingFileLogger-t
        if log_file:
            return RotatingFileLogger(
                name=name,
                log_file=log_file,
                level=level,
                max_bytes=config.get("max_bytes", 1024 * 1024),  # 1MB
                backup_count=config.get("backup_count", 5),
                format_str=config.get(
                    "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
            )

        # Egyébként a logger_type alapján válasszunk
        if logger_type == "colored" and sys.stdout.isatty():
            return ColoredLogger(
                name=name,
                level=level,
                format_str=config.get(
                    "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
            )

        # Alapértelmezett logger
        return DefaultLogger(
            name=name,
            level=level,
            format_str=config.get(
                "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
        )
