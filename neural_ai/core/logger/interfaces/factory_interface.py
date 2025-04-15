"""Logger factory interfész definíció.

Ez a modul definiálja a logger factory interfészt, amely
felelős a logger példányok létrehozásáért és konfigurálásáért.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class LoggerFactoryInterface(ABC):
    """Logger factory interfész a logger példányok létrehozásához.

    Az interfész definiálja a logger példányok létrehozásáért és
    konfigurálásáért felelős műveleteket.
    """

    @staticmethod
    @abstractmethod
    def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
        """Logger példány létrehozása vagy meglévő visszaadása.

        Args:
            name: A logger neve
            config: Opcionális konfiguráció

        Returns:
            LoggerInterface: Új vagy meglévő logger példány
        """
        pass

    @staticmethod
    @abstractmethod
    def configure(config: Dict[str, Any]) -> None:
        """Globális logger konfiguráció beállítása.

        Args:
            config: A logger rendszer konfigurációja
        """
        pass
