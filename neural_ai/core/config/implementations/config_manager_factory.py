"""Konfiguráció kezelő factory implementáció."""

from pathlib import Path
from typing import Dict, Optional, Type, Union

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
        if not extension.startswith("."):
            extension = f".{extension}"
        cls._manager_types[extension] = manager_class

    @classmethod
    def get_manager(
        cls, filename: Union[str, Path], manager_type: Optional[str] = None
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
        filename_str = str(filename)

        # Ha explicit módon meg van adva a típus
        if manager_type:
            ext = f".{manager_type}" if not manager_type.startswith(".") else manager_type
            if ext in cls._manager_types:
                manager_class = cls._manager_types[ext]
                return manager_class(filename=filename_str)
            raise ConfigLoadError(f"Ismeretlen konfig kezelő típus: {manager_type}")

        # Fájl kiterjesztés alapján
        _, ext = Path(filename_str).suffix.lower(), Path(filename_str).suffix
        if ext in cls._manager_types:
            manager_class = cls._manager_types[ext]
            return manager_class(filename=filename_str)

        # Alapértelmezett: YAML
        if not ext:
            return YAMLConfigManager(filename=filename_str)

        raise ConfigLoadError(
            f"Nem található konfig kezelő a következő kiterjesztéshez: {ext}. "
            f"Támogatott kiterjesztések: {list(cls._manager_types.keys())}"
        )

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            list[str]: A támogatott kiterjesztések listája
        """
        return list(cls._manager_types.keys())
