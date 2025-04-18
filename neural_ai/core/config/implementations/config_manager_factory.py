"""Konfiguráció kezelő factory."""

import os
from typing import Any, Dict, Optional, Type

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface


class ConfigManagerFactory(ConfigManagerFactoryInterface):
    """Factory osztály konfiguráció kezelők létrehozásához."""

    _manager_types: Dict[str, Type[ConfigManagerInterface]] = {
        ".yml": YAMLConfigManager,
        ".yaml": YAMLConfigManager,
    }

    @classmethod
    def register_manager(cls, extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Új konfiguráció kezelő típus regisztrálása.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml")
            manager_class: A kezelő osztály
        """
        cls._manager_types[extension] = manager_class

    @classmethod
    def get_manager(
        cls, filename: str, manager_type: Optional[str] = None
    ) -> ConfigManagerInterface:
        """Megfelelő konfiguráció kezelő létrehozása.

        Args:
            filename: Konfigurációs fájl neve
            manager_type: Kért kezelő típus (opcionális)

        Returns:
            ConfigManagerInterface: A létrehozott kezelő

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
        """
        # Ha explicit módon meg van adva a típus
        if manager_type and manager_type in cls._manager_types:
            return cls.create_manager(manager_type, filename=filename)

        # Fájl kiterjesztés alapján
        _, ext = os.path.splitext(filename)
        if ext in cls._manager_types:
            return cls.create_manager(ext, filename=filename)

        # Alapértelmezett: YAML
        if not ext:
            return YAMLConfigManager(filename=filename)

        raise ConfigLoadError(
            f"No config manager found for extension: {ext}. "
            f"Supported extensions: {list(cls._manager_types.keys())}"
        )

    @classmethod
    def create_manager(cls, manager_type: str, *args: Any, **kwargs: Any) -> ConfigManagerInterface:
        """Konfiguráció kezelő létrehozása típus alapján.

        Args:
            manager_type: A kért kezelő típus
            *args: Pozícionális paraméterek
            **kwargs: Kulcsszavas paraméterek

        Returns:
            ConfigManagerInterface: A létrehozott kezelő

        Raises:
            ConfigLoadError: Ha nem található a kért típusú kezelő
        """
        if manager_type in cls._manager_types:
            manager_class = cls._manager_types[manager_type]
            return manager_class(*args, **kwargs)

        raise ConfigLoadError(
            f"Unknown config manager type: {manager_type}. "
            f"Available types: {list(cls._manager_types.keys())}"
        )
