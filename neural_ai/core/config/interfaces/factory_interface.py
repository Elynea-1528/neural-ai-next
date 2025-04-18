"""Konfiguráció kezelő factory interfész."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class ConfigManagerFactoryInterface(ABC):
    """Konfiguráció kezelő factory interfész."""

    @classmethod
    @abstractmethod
    def register_manager(cls, extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Új konfiguráció kezelő típus regisztrálása.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml")
            manager_class: A kezelő osztály
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_manager(
        cls, filename: str, manager_type: Optional[str] = None
    ) -> ConfigManagerInterface:
        """Megfelelő konfiguráció kezelő létrehozása.

        Args:
            filename: Konfigurációs fájl neve
            manager_type: Kért kezelő típus (opcionális)

        Returns:
            ConfigManagerInterface: A létrehozott kezelő
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create_manager(cls, manager_type: str, *args: Any, **kwargs: Any) -> ConfigManagerInterface:
        """Konfiguráció kezelő létrehozása típus alapján.

        Args:
            manager_type: A kért kezelő típus
            *args: Pozícionális paraméterek
            **kwargs: Kulcsszavas paraméterek

        Returns:
            ConfigManagerInterface: A létrehozott kezelő
        """
        raise NotImplementedError
