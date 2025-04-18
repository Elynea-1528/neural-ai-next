"""Konfigurációkezelő factory implementáció."""

from typing import Any, Dict, Type

from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.interfaces import ConfigManagerFactoryInterface, ConfigManagerInterface


class ConfigManagerFactory(ConfigManagerFactoryInterface):
    """Konfigurációkezelő factory implementáció."""

    _MANAGERS: Dict[str, Type[ConfigManagerInterface]] = {}

    @classmethod
    def initialize(cls) -> None:
        """Factory inicializálása alapértelmezett kezelőkkel."""
        cls.register_manager("yaml", YAMLConfigManager)
        cls.register_manager("yml", YAMLConfigManager)

    @classmethod
    def register_manager(cls, extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Új konfigurációkezelő regisztrálása.

        Args:
            extension: Fájl kiterjesztés
            manager_class: Kezelő osztály
        """
        if not extension.startswith("."):
            extension = f".{extension}"
        cls._MANAGERS[extension] = manager_class

    @classmethod
    def get_manager(cls, filename: str, **kwargs: Any) -> ConfigManagerInterface:
        """Megfelelő konfigurációkezelő példány létrehozása.

        Args:
            filename: Konfigurációs fájl neve
            **kwargs: További paraméterek a kezelő számára

        Returns:
            ConfigManagerInterface: Konfigurációkezelő példány

        Raises:
            ValueError: Ha nem található megfelelő kezelő
        """
        if not cls._MANAGERS:
            cls.initialize()

        extension = cls._get_extension(filename)
        manager_class = cls._MANAGERS.get(extension)

        if not manager_class:
            raise ValueError(f"No configuration manager found for extension: {extension}")

        init_args = {"filename": filename}
        if kwargs:
            init_args.update(kwargs)

        return manager_class(**init_args)

    @classmethod
    def get_supported_extensions(cls) -> Dict[str, Type[ConfigManagerInterface]]:
        """Támogatott kiterjesztések lekérése.

        Returns:
            Dict[str, Type[ConfigManagerInterface]]: Kiterjesztések és kezelők
        """
        if not cls._MANAGERS:
            cls.initialize()
        return cls._MANAGERS.copy()

    @staticmethod
    def _get_extension(filename: str) -> str:
        """Fájl kiterjesztés kinyerése.

        Args:
            filename: A fájl neve

        Returns:
            str: A kiterjesztés ponttal kezdve
        """
        return "." + filename.split(".")[-1].lower()
