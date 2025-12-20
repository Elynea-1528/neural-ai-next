"""Konfiguráció kezelő factory tesztek."""

import os
import tempfile
from collections.abc import Generator
from typing import Any

import pytest
import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory,
)
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class MockConfigManager(ConfigManagerInterface):
    """Mock konfiguráció kezelő teszteléshez."""

    def __init__(self, filename: str | None = None) -> None:
        """Mock inicializálás."""
        self.filename = filename

    def get(self, *keys: str, default: Any = None) -> Any:
        """Mock implementáció."""
        return None

    def get_section(self, section: str) -> dict[str, Any]:
        """Mock implementáció."""
        return {}

    def set(self, *keys: str, value: Any) -> None:
        """Mock implementáció."""
        pass

    def save(self, filename: str | None = None) -> None:
        """Mock implementáció."""
        pass

    def load(self, filename: str) -> None:
        """Mock implementáció."""
        pass

    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Mock implementáció."""
        return True, None


@pytest.fixture
def temp_config_dir() -> Generator[str, None, None]:
    """Ideiglenes könyvtár fixture teszteléshez."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def yaml_config_file(temp_config_dir: str) -> str:
    """YAML konfigurációs fájl fixture."""
    config_data = {"test": {"key": "value"}}
    config_path = os.path.join(temp_config_dir, "config.yaml")

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    return config_path


class TestConfigManagerFactory:
    """ConfigManagerFactory tesztosztály."""

    def setup_method(self) -> None:
        """Teszt setup."""
        # Reset manager types before each test
        ConfigManagerFactory._manager_types.clear()
        # Register default types
        ConfigManagerFactory._manager_types[".yml"] = YAMLConfigManager
        ConfigManagerFactory._manager_types[".yaml"] = YAMLConfigManager

    def test_get_manager_with_yaml_extension(self, yaml_config_file: str) -> None:
        """Teszteli .yaml kiterjesztésű fájl kezelő létrehozását."""
        manager = ConfigManagerFactory.get_manager(yaml_config_file)
        assert isinstance(manager, YAMLConfigManager)

    def test_get_manager_with_yml_extension(self, temp_config_dir: str) -> None:
        """Teszteli .yml kiterjesztésű fájl kezelő létrehozását."""
        config_path = os.path.join(temp_config_dir, "config.yml")
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump({"test": True}, f)

        manager = ConfigManagerFactory.get_manager(config_path)
        assert isinstance(manager, YAMLConfigManager)

    def test_get_manager_with_invalid_extension(self) -> None:
        """Teszteli nem támogatott kiterjesztés kezelését."""
        with pytest.raises(ConfigLoadError):
            ConfigManagerFactory.get_manager("config.invalid")

    def test_register_manager(self, temp_config_dir: str) -> None:
        """Teszteli új kezelő típus regisztrálását."""
        config_path = os.path.join(temp_config_dir, "config.mock")
        ConfigManagerFactory.register_manager(".mock", MockConfigManager)
        manager = ConfigManagerFactory.get_manager(config_path)
        assert isinstance(manager, MockConfigManager)

    def test_register_manager_without_dot(self, temp_config_dir: str) -> None:
        """Teszteli pont nélküli kiterjesztés regisztrálását."""
        config_path = os.path.join(temp_config_dir, "config.mock")
        ConfigManagerFactory.register_manager("mock", MockConfigManager)
        manager = ConfigManagerFactory.get_manager(config_path)
        assert isinstance(manager, MockConfigManager)

    def test_get_manager_with_kwargs(self, yaml_config_file: str) -> None:
        """Teszteli kezelő létrehozását paraméterekkel."""
        manager = ConfigManagerFactory.get_manager(filename=yaml_config_file)
        assert isinstance(manager, YAMLConfigManager)

    def test_get_supported_extensions(self) -> None:
        """Teszteli támogatott kiterjesztések lekérését."""
        extensions = ConfigManagerFactory.get_supported_extensions()
        assert ".yml" in extensions
        assert ".yaml" in extensions

    def test_default_extensions(self) -> None:
        """Teszteli az alapértelmezett támogatott kiterjesztéseket."""
        extensions = set(ConfigManagerFactory.get_supported_extensions())
        assert extensions == {".yml", ".yaml"}
