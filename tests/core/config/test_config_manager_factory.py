"""Konfigurációkezelő factory tesztek."""

from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.config.implementations import ConfigManagerFactory, YAMLConfigManager
from neural_ai.core.config.interfaces import ConfigManagerInterface


class DummyConfigManager(ConfigManagerInterface):
    """Dummy konfiguráció kezelő a tesztekhez."""

    def __init__(self, filename: Optional[str] = None, **kwargs: Any) -> None:
        """Inicializálja a dummy kezelőt."""
        self._filename = filename
        self._config: Dict[str, Any] = {}

    def get(self, *keys: str, default: Any = None) -> Any:
        """Dummy get metódus."""
        return default

    def get_section(self, section: str) -> Dict[str, Any]:
        """Dummy get_section metódus."""
        return {}

    def set(self, *keys: str, value: Any) -> None:
        """Dummy set metódus."""

    def save(self, filename: Optional[str] = None) -> None:
        """Dummy save metódus."""

    def load(self, filename: str) -> None:
        """Dummy load metódus."""

    def validate(self, schema: Dict[str, Any]) -> tuple[bool, Optional[Dict[str, str]]]:
        """Dummy validate metódus."""
        return True, None


class TestConfigManagerFactory:
    """Factory osztály tesztek."""

    def setup_method(self) -> None:
        """Teszt setup."""
        ConfigManagerFactory._MANAGERS.clear()  # pylint: disable=protected-access

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", create=True)
    def test_get_manager_with_yaml_extension(
        self, patched_open: MagicMock, mock_exists: MagicMock
    ) -> None:
        """YAML kiterjesztés esetén YAMLConfigManager-t ad vissza."""
        yaml_content = "key: value\n"
        patched_open.return_value.__enter__.return_value.read.return_value = yaml_content
        patched_open.return_value.__enter__.return_value.name = "config.yaml"
        manager = ConfigManagerFactory.get_manager("config.yaml")
        assert isinstance(manager, YAMLConfigManager)
        mock_exists.assert_called_once_with("config.yaml")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", create=True)
    def test_get_manager_with_yml_extension(
        self, patched_open: MagicMock, mock_exists: MagicMock
    ) -> None:
        """YML kiterjesztés esetén YAMLConfigManager-t ad vissza."""
        yaml_content = "key: value\n"
        patched_open.return_value.__enter__.return_value.read.return_value = yaml_content
        patched_open.return_value.__enter__.return_value.name = "config.yml"
        manager = ConfigManagerFactory.get_manager("config.yml")
        assert isinstance(manager, YAMLConfigManager)
        mock_exists.assert_called_once_with("config.yml")

    def test_get_manager_with_invalid_extension(self) -> None:
        """Érvénytelen kiterjesztés esetén hibát dob."""
        with pytest.raises(ValueError) as exc_info:
            ConfigManagerFactory.get_manager("config.invalid")
        assert "No configuration manager found for extension" in str(exc_info.value)

    def test_register_manager(self) -> None:
        """Új kezelő regisztrálása."""
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        manager = ConfigManagerFactory.get_manager("config.test")
        assert isinstance(manager, DummyConfigManager)

    def test_register_manager_without_dot(self) -> None:
        """Pont nélküli kiterjesztés regisztrálása."""
        ConfigManagerFactory.register_manager("test", DummyConfigManager)
        manager = ConfigManagerFactory.get_manager("config.test")
        assert isinstance(manager, DummyConfigManager)

    def test_get_manager_with_kwargs(self) -> None:
        """Extra paraméterek átadása a kezelőnek."""
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        kwargs = {"encoding": "utf-8", "mode": "r"}
        manager = ConfigManagerFactory.get_manager("config.test", **kwargs)
        assert isinstance(manager, DummyConfigManager)

    def test_get_supported_extensions(self) -> None:
        """Támogatott kiterjesztések lekérése."""
        ConfigManagerFactory._MANAGERS.clear()  # pylint: disable=protected-access
        ConfigManagerFactory.register_manager(".test", DummyConfigManager)
        extensions = ConfigManagerFactory.get_supported_extensions()

        assert isinstance(extensions, dict)
        assert ".test" in extensions
        assert extensions[".test"] is DummyConfigManager

    def test_default_extensions(self) -> None:
        """Alapértelmezett kiterjesztések ellenőrzése."""
        extensions = ConfigManagerFactory.get_supported_extensions()
        assert ".yaml" in extensions
        assert ".yml" in extensions
        assert extensions[".yaml"] is YAMLConfigManager
        assert extensions[".yml"] is YAMLConfigManager
