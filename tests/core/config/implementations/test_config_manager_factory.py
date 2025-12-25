"""Konfiguráció kezelő factory tesztjei."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.implementations.yaml_config_manager import (
    YAMLConfigManager,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class TestConfigManagerFactory:
    """ConfigManagerFactory osztály tesztjei."""

    def test_register_manager(self) -> None:
        """Teszteli a manager regisztrálását."""

        # Egyéni manager osztály létrehozása
        class JSONConfigManager(ConfigManagerInterface):
            def load(self, filename: str) -> None:
                pass

            def save(self, filename: str | None = None) -> None:
                pass

            def get(self, *keys: str, default: object = None) -> object:
                return default

            def get_section(self, section: str) -> dict[str, object]:
                return {}

            def set(self, *keys: str, value: object) -> None:
                pass

            def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]:
                return True, None

        # Regisztrálás
        ConfigManagerFactory.register_manager(".json", JSONConfigManager)

        # Ellenőrzés
        assert ".json" in ConfigManagerFactory._manager_types
        assert ConfigManagerFactory._manager_types[".json"] == JSONConfigManager

    def test_register_manager_without_dot(self) -> None:
        """Teszteli a manager regisztrálását pont nélküli kiterjesztéssel."""

        class TestManager(ConfigManagerInterface):
            def load(self, filename: str) -> None:
                pass

            def save(self, filename: str | None = None) -> None:
                pass

            def get(self, *keys: str, default: object = None) -> object:
                return default

            def get_section(self, section: str) -> dict[str, object]:
                return {}

            def set(self, *keys: str, value: object) -> None:
                pass

            def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]:
                return True, None

        # Regisztrálás pont nélkül
        ConfigManagerFactory.register_manager("test", TestManager)

        # Ellenőrzés, hogy ponttal lett-e elmentve
        assert ".test" in ConfigManagerFactory._manager_types
        assert ConfigManagerFactory._manager_types[".test"] == TestManager

    def test_get_manager_by_yaml_extension(self) -> None:
        """Teszteli a manager lekérését YAML kiterjesztés alapján."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config.yaml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config.yaml")

    def test_get_manager_by_yml_extension(self) -> None:
        """Teszteli a manager lekérését YML kiterjesztés alapján."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config.yml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config.yml")

    def test_get_manager_by_path_object(self) -> None:
        """Teszteli a manager lekérését Path objektummal."""
        path = Path("config.yaml")
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager(path)

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config.yaml")

    def test_get_manager_with_explicit_type(self) -> None:
        """Teszteli a manager lekérését explicit típus megadásával."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config", manager_type="yaml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config")

    def test_get_manager_with_explicit_type_with_dot(self) -> None:
        """Teszteli a manager lekérését explicit típussal, ponttal."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config", manager_type=".yaml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config")

    def test_get_manager_unsupported_extension(self) -> None:
        """Teszteli a manager lekérését nem támogatott kiterjesztéssel."""
        with pytest.raises(ConfigLoadError, match="Nem található konfig kezelő"):
            ConfigManagerFactory.get_manager("config.xyz")

    def test_get_manager_unknown_explicit_type(self) -> None:
        """Teszteli a manager lekérését ismeretlen explicit típussal."""
        with pytest.raises(ConfigLoadError, match="Ismeretlen konfig kezelő típus"):
            ConfigManagerFactory.get_manager("config", manager_type="xyz")

    def test_get_manager_default_to_yaml_no_extension(self) -> None:
        """Teszteli, hogy alapértelmezésként YAML kezelőt ad vissza, ha nincs kiterjesztés."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config")

    def test_get_supported_extensions(self) -> None:
        """Teszteli a támogatott kiterjesztések lekérdezését."""
        extensions = ConfigManagerFactory.get_supported_extensions()

        assert ".yml" in extensions
        assert ".yaml" in extensions
        assert isinstance(extensions, list)

    def test_create_manager_with_type(self) -> None:
        """Teszteli a manager létrehozását típus alapján."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.create_manager("yaml", filename="test.yaml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="test.yaml")

    def test_create_manager_with_type_and_args(self) -> None:
        """Teszteli a manager létrehozását típus és argumentumok alapján."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.create_manager("yaml", filename="test.yaml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="test.yaml")

    def test_create_manager_unknown_type(self) -> None:
        """Teszteli a manager létrehozását ismeretlen típussal."""
        with pytest.raises(ConfigLoadError, match="Ismeretlen konfig kezelő típus"):
            ConfigManagerFactory.create_manager("xyz", filename="test.xyz")

    def test_create_manager_with_type_without_dot(self) -> None:
        """Teszteli a manager létrehozását pont nélküli típussal."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.create_manager("yml", filename="test.yml")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="test.yml")

    def test_case_insensitive_extension(self) -> None:
        """Teszteli a kis- és nagybetűérzéketlen kiterjesztés-egyeztetést."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
            manager = ConfigManagerFactory.get_manager("config.YAML")

            assert isinstance(manager, YAMLConfigManager)
            mock_init.assert_called_once_with(filename="config.YAML")

    def test_get_manager_with_temp_file(self) -> None:
        """Teszteli a manager lekérését ideiglenes fájllal."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_file = f.name

        try:
            with patch.object(YAMLConfigManager, "__init__", return_value=None) as mock_init:
                manager = ConfigManagerFactory.get_manager(temp_file)
                assert isinstance(manager, YAMLConfigManager)
                mock_init.assert_called_once_with(filename=temp_file)
        finally:
            import os

            os.unlink(temp_file)

    def test_factory_singleton_behavior(self) -> None:
        """Teszteli, hogy a factory metódusok mindig új példányt adnak vissza."""
        with patch.object(YAMLConfigManager, "__init__", return_value=None):
            manager1 = ConfigManagerFactory.get_manager("config.yaml")
            manager2 = ConfigManagerFactory.get_manager("config.yaml")

            # Két különböző példányt kell kapnunk
            assert manager1 is not manager2
            assert isinstance(manager1, YAMLConfigManager)
            assert isinstance(manager2, YAMLConfigManager)

    def test_manager_types_dict_immutability(self) -> None:
        """Teszteli, hogy a _manager_types szótár módosítása globálisan érvényes."""
        # Elmentjük az eredeti állapotot
        original_count = len(ConfigManagerFactory._manager_types)

        # Új manager regisztrálása egyedi kiterjesztéssel
        class TestManager(ConfigManagerInterface):
            def load(self, filename: str) -> None:
                pass

            def save(self, filename: str | None = None) -> None:
                pass

            def get(self, *keys: str, default: object = None) -> object:
                return default

            def get_section(self, section: str) -> dict[str, object]:
                return {}

            def set(self, *keys: str, value: object) -> None:
                pass

            def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]:
                return True, None

        ConfigManagerFactory.register_manager(".unique", TestManager)

        # Ellenőrizzük, hogy a szótár tényleg módosult
        assert ".unique" in ConfigManagerFactory._manager_types
        assert len(ConfigManagerFactory._manager_types) == original_count + 1
