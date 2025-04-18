"""Konfiguráció menedzser factory interfész.

Ez a modul tartalmazza a konfigurációkezelő factory interfész definícióját.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

from .config_interface import ConfigManagerInterface


class ConfigManagerFactoryInterface(ABC):
    """Interfész a konfigurációkezelő factory osztályokhoz.

    Ez az interfész felelős a megfelelő ConfigManager implementáció
    létrehozásáért a fájl típusa alapján.
    """

    @staticmethod
    @abstractmethod
    def get_manager(filename: str, **kwargs: Any) -> ConfigManagerInterface:
        """Megfelelő ConfigManager példány létrehozása.

        Args:
            filename: A konfigurációs fájl neve
            **kwargs: További paraméterek a manager létrehozásához

        Returns:
            ConfigManagerInterface: A létrehozott manager példány

        Raises:
            ValueError: Ha a fájl típusa nem támogatott
        """
        pass

    @staticmethod
    @abstractmethod
    def register_manager(extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Új manager típus regisztrálása.

        Args:
            extension: Fájl kiterjesztés (pl. ".yaml", ".json")
            manager_class: A manager osztály

        Raises:
            ValueError: Ha a kiterjesztés már regisztrálva van
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_extensions() -> Dict[str, Type[ConfigManagerInterface]]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            Dict[str, Type[ConfigManagerInterface]]: A támogatott kiterjesztések
                és a hozzájuk tartozó manager osztályok
        """
        pass

    @staticmethod
    @abstractmethod
    def configure(config: Optional[Dict[str, Any]] = None) -> None:
        """Factory globális konfigurálása.

        Args:
            config: Opcionális konfigurációs beállítások
        """
        pass
