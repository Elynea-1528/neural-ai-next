"""Konfigurációkezelő factory tesztek.

Ez a modul tartalmazza a konfigurációkezelő factory osztály tesztjeit.
"""

from typing import Any, Dict, Optional, Tuple

import pytest

from neural_ai.core.config.implementations import (
    ConfigManagerFactory,
    YAMLConfigManager,
)
from neural_ai.core.config.interfaces import ConfigManagerInterface


class DummyConfigManager(ConfigManagerInterface):
    """Dummy manager implementáció teszteléshez."""

    def __init__(self, filename: Optional[str] = None, **_kwargs: Any) -> None:
        """Inicializálja a dummy managert.

        Args:
            filename: Opcionális konfigurációs fájl neve
            **_kwargs: További paraméterek (ignorálva)
        """
        self._filename = filename

    def get(self, *keys: str, default: Any = None) -> Any:
        """Dummy get implementáció."""
        return default

    def get_section(self, section: str) -> Dict[str, Any]:
        """Dummy get_section implementáció."""
        return {}

    def set(self, *keys: str, value: Any) -> None:
        """Dummy set implementáció."""
        pass

    def save(self, filename: Optional[str] = None) -> None:
        """Dummy save implementáció."""
        pass

    def load(self, filename: str) -> None:
        """Dummy load implementáció."""
        pass

    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Dummy validate implementáció."""
        return True, None


class TestConfigManagerFactory:
    """ConfigManagerFactory tesztek."""

    def setup_method(self) -> None:
        """Teszt környezet előkészítése."""
        # Töröljük a regisztrált managereket
        ConfigManagerFactory._managers.clear()

    def test_register_manager(self) -> None:
        """Teszteli az új manager típus regisztrálását."""
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        assert ".test" in ConfigManagerFactory.get_supported_extensions()

    def test_register_duplicate_extension(self) -> None:
        """Teszteli a duplikált kiterjesztés kezelését."""
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        with pytest.raises(ValueError):
            ConfigManagerFactory.register_manager(".test", DummyConfigManager)

    def test_register_without_dot(self) -> None:
        """Teszteli a pont nélküli kiterjesztés kezelését."""
        ConfigManagerFactory.register_manager("test", DummyConfigManager)
        assert ".test" in ConfigManagerFactory.get_supported_extensions()

    def test_get_manager_unsupported_type(self) -> None:
        """Teszteli a nem támogatott fájltípus kezelését."""
        with pytest.raises(ValueError) as exc_info:
            ConfigManagerFactory.get_manager("config.unsupported")
        assert "Unsupported configuration file type" in str(exc_info.value)

    def test_get_manager_yaml(self, tmp_path) -> None:
        """Teszteli a YAML manager létrehozását."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("")  # Üres fájl létrehozása

        ConfigManagerFactory.register_manager(".yaml", YAMLConfigManager)
        manager = ConfigManagerFactory.get_manager(str(config_file))
        assert isinstance(manager, YAMLConfigManager)

    def test_get_manager_with_kwargs(self) -> None:
        """Teszteli a paraméterek átadását a managernek."""
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        manager = ConfigManagerFactory.get_manager(
            "config.test",
            custom_param="value"
        )
        assert isinstance(manager, DummyConfigManager)

    def test_get_supported_extensions(self) -> None:
        """Teszteli a támogatott kiterjesztések lekérését."""
        ConfigManagerFactory.register_manager(".yaml", YAMLConfigManager)
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)

        extensions = ConfigManagerFactory.get_supported_extensions()
        assert len(extensions) == 2
        assert ".yaml" in extensions
        assert ".test" in extensions
        assert extensions[".yaml"] == YAMLConfigManager
        assert extensions[".test"] == DummyConfigManager

    def test_extension_case_sensitivity(self) -> None:
        """Teszteli a kiterjesztések kis- és nagybetű érzékenységét."""
        ConfigManagerFactory.register_manager(".YAML", YAMLConfigManager)
        with pytest.raises(ValueError):
            ConfigManagerFactory.get_manager("config.yaml")

    def test_configure_method(self) -> None:
        """Teszteli a konfigurációs metódust."""
        # Jelenleg a configure metódus üres implementáció
        ConfigManagerFactory.configure({"some": "config"})
        # Nem dobhat kivételt
