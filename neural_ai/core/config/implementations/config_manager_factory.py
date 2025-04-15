"""Konfigurációkezelő factory implementáció.

Ez a modul tartalmazza a konfigurációkezelő factory implementációját,
amely a megfelelő konfigurációkezelő példányt hozza létre.
"""

import os
from typing import Any, Dict, Optional, Type

from neural_ai.core.config.interfaces import (
    ConfigManagerInterface,
    ConfigManagerFactoryInterface,
)


class ConfigManagerFactory(ConfigManagerFactoryInterface):
    """Konfigurációkezelő factory implementáció.

    Ez az osztály felelős a megfelelő ConfigManager implementáció
    létrehozásáért a fájl típusa alapján.
    """

    _managers: Dict[str, Type[ConfigManagerInterface]] = {}

    @staticmethod
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
        _, ext = os.path.splitext(filename)
        if ext not in ConfigManagerFactory._managers:
            supported = ", ".join(ConfigManagerFactory._managers.keys())
            raise ValueError(
                f"Unsupported configuration file type: {ext}. "
                f"Supported types are: {supported}"
            )

        manager_class = ConfigManagerFactory._managers[ext]
        kwargs["filename"] = filename
        return manager_class(**kwargs)

    @staticmethod
    def register_manager(extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Manager típus regisztrálása.

        Args:
            extension: Fájl kiterjesztés (pl. ".yaml", ".json")
            manager_class: A manager osztály

        Raises:
            ValueError: Ha a kiterjesztés már regisztrálva van
        """
        if not extension.startswith("."):
            extension = f".{extension}"

        if extension in ConfigManagerFactory._managers:
            raise ValueError(f"Manager already registered for extension: {extension}")

        ConfigManagerFactory._managers[extension] = manager_class

    @staticmethod
    def get_supported_extensions() -> Dict[str, Type[ConfigManagerInterface]]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            Dict[str, Type[ConfigManagerInterface]]: A támogatott kiterjesztések
                és a hozzájuk tartozó manager osztályok
        """
        return ConfigManagerFactory._managers.copy()

    @staticmethod
    def configure(config: Optional[Dict[str, Any]] = None) -> None:
        """Factory globális konfigurálása.

        Args:
            config: Opcionális konfigurációs beállítások
        """
        # Jelenleg nincs szükség globális konfigurációra
        pass