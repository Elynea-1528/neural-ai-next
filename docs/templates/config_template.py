"""
Template a Neural-AI-Next konfigurációs kezelőjéhez.
"""

import os
from typing import Any, Dict, List, Optional, Union  # noqa: F401 - Sablon részeként szerepel

import yaml

from neural_ai.core.config.exceptions import (
    ConfigNotFoundException,
    ConfigParseError,
    ConfigSectionNotFoundError,
)
from neural_ai.core.config.interfaces.config_manager_interface import ConfigManagerInterface


class YAMLConfigManager(ConfigManagerInterface):
    """
    YAML alapú konfigurációs kezelő implementálása.
    """

    def __init__(self, config_path: str):
        """
        YAML konfigurációs kezelő inicializálása.

        Args:
            config_path: A konfigurációs fájl elérési útja

        Raises:
            ConfigNotFoundException: Ha a konfig fájl nem található
            ConfigParseError: Ha a konfig fájl nem érvényes YAML
        """
        self.config_path = config_path
        self.config_data: Dict[str, Any] = {}

        # Konfig fájl betöltése
        self._load_config()

    def _load_config(self) -> None:
        """
        Konfig fájl betöltése.

        Raises:
            ConfigNotFoundException: Ha a konfig fájl nem található
            ConfigParseError: Ha a konfig fájl nem érvényes YAML
        """
        if not os.path.exists(self.config_path):
            raise ConfigNotFoundException(f"Konfiguráció nem található: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config_data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigParseError(f"Hiba a konfiguráció feldolgozásakor: {str(e)}")
        except Exception as e:
            raise ConfigParseError(f"Váratlan hiba a konfiguráció betöltésekor: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Konfigurációs érték lekérése.

        Args:
            key: A konfigurációs kulcs (pl. "app.debug")
            default: Az alapértelmezett érték, ha a kulcs nem található

        Returns:
            Any: A konfigurációs érték vagy az alapértelmezett
        """
        # Beágyazott kulcsok kezelése (pl. "app.debug")
        parts = key.split(".")
        value = self.config_data

        try:
            for part in parts:
                value = value.get(part, {})

            # Ha az érték üres dict és ez volt az utolsó kulcsrész, akkor nincs ilyen beállítás
            if value == {} and parts[-1] in self.config_data:
                return default

            return value if value != {} else default
        except (AttributeError, KeyError):
            return default

    def get_section(self, section: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Konfigurációs szekció lekérése.

        Args:
            section: A szekció neve
            default: Az alapértelmezett szekció, ha nem található

        Returns:
            Dict[str, Any]: A konfigurációs szekció vagy az alapértelmezett

        Raises:
            ConfigSectionNotFoundError: Ha a szekció nem található és nincs alapértelmezett
        """
        section_value = self.config_data.get(section, None)

        if section_value is None:
            if default is not None:
                return default
            raise ConfigSectionNotFoundError(
                f"Nem található konfiguráció ehhez a szekcióhoz: {section}"
            )

        return section_value

    def get_all(self) -> Dict[str, Any]:
        """
        A teljes konfiguráció lekérése.

        Returns:
            Dict[str, Any]: A teljes konfigurációs objektum
        """
        return self.config_data


class ConfigManagerFactory:
    """Factory osztály a konfiguráció kezelők létrehozásához."""

    @staticmethod
    def get_manager(
        config_path: str,
        format_type: Optional[str] = None,
        create_if_not_exists: bool = False,
        logger=None,
    ) -> ConfigManagerInterface:
        """
        Konfiguráció kezelő példány létrehozása.

        Args:
            config_path: A konfigurációs fájl útvonala
            format_type: A konfiguráció formátuma (yaml, json, ini, stb.)
            create_if_not_exists: Létrehozza a konfigurációs fájlt, ha nem létezik
            logger: Logger példány vagy None

        Returns:
            ConfigManagerInterface: Konfiguráció kezelő példány

        Raises:
            ValueError: Ha a formátum típus nem támogatott
        """
        log = logger or LoggerFactory.get_logger(__name__)

        # Ha nincs megadva formátum típus, próbáljuk kitalálni a kiterjesztésből
        if format_type is None:
            _, ext = os.path.splitext(config_path)
            format_type = ext.lstrip(".").lower()

        # Ha a fájl nem létezik és kérték a létrehozást
        if create_if_not_exists and not os.path.exists(config_path):
            log.info(f"Creating default config file: {config_path}")
            return ConfigManagerFactory.create_default_config(config_path, format_type)

        # Támogatott formátumok kezelése
        if format_type in ["yaml", "yml"]:
            return YAMLConfigManager(config_path, logger)
        # További formátumok támogatása itt...
        else:
            log.error(f"Unsupported config format: {format_type}")
            raise ValueError(f"Unsupported config format: {format_type}")

    @staticmethod
    def create_default_config(config_path: str, format_type: str) -> ConfigManagerInterface:
        """
        Alapértelmezett konfiguráció létrehozása.

        Args:
            config_path: A konfigurációs fájl útvonala
            format_type: A konfiguráció formátuma

        Returns:
            ConfigManagerInterface: Konfiguráció kezelő példány az alapértelmezett konfigurációval

        Raises:
            ValueError: Ha a formátum típus nem támogatott
        """
        # Könyvtár létrehozása, ha nem létezik
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        # Alapértelmezett konfiguráció
        default_config = {
            "app": {"name": "neural-ai-next", "version": "1.0.0", "environment": "development"},
            "logging": {
                "level": "INFO",
                "file": "logs/app.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "storage": {"path": "data/", "format": "parquet"},
        }

        # Konfiguráció mentése a megfelelő formátumban
        if format_type in ["yaml", "yml"]:
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return YAMLConfigManager(config_path)
        # További formátumok támogatása itt...
        else:
            raise ValueError(f"Unsupported config format: {format_type}")
