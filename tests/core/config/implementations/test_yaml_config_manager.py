"""YAML konfigurációkezelő tesztjei."""

import os
import tempfile

import pytest
import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations.yaml_config_manager import (
    YAMLConfigManager,
)


class TestYAMLConfigManager:
    """YAMLConfigManager osztály tesztjei."""

    @pytest.fixture
    def temp_config_file(self) -> str:
        """Létrehoz egy ideiglenes konfigurációs fájlt.

        Returns:
            str: Az ideiglenes fájl elérési útja
        """
        config_data = {
            "database": {"host": "localhost", "port": 5432, "username": "admin"},
            "logging": {"level": "INFO", "file": "/var/log/app.log"},
            "features": {"enabled": True, "max_connections": 100},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f, default_flow_style=False)
            temp_file = f.name

        yield temp_file

        os.unlink(temp_file)

    def test_init_without_file(self) -> None:
        """Teszteli az inicializálást fájl nélkül."""
        manager = YAMLConfigManager()
        assert manager._config == {}
        assert manager._filename is None

    def test_init_with_file(self, temp_config_file: str) -> None:
        """Teszteli az inicializálást fájllal."""
        manager = YAMLConfigManager(filename=temp_config_file)
        assert manager._config is not None
        assert manager._filename == temp_config_file
        assert "database" in manager._config

    def test_load_valid_file(self, temp_config_file: str) -> None:
        """Teszteli az érvényes fájl betöltését."""
        manager = YAMLConfigManager()
        manager.load(temp_config_file)

        assert manager._config is not None
        assert manager._filename == temp_config_file
        assert manager.get("database", "host") == "localhost"

    def test_load_nonexistent_file(self) -> None:
        """Teszteli a nem létező fájl betöltését."""
        manager = YAMLConfigManager()

        with pytest.raises(ConfigLoadError, match="Fájl nem található"):
            manager.load("/nonexistent/path/config.yaml")

    def test_load_invalid_yaml(self) -> None:
        """Teszteli az érvénytelen YAML fájl betöltését."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_file = f.name

        try:
            manager = YAMLConfigManager()
            with pytest.raises(ConfigLoadError, match="Konfiguráció betöltése sikertelen"):
                manager.load(temp_file)
        finally:
            os.unlink(temp_file)

    def test_get_simple_value(self, temp_config_file: str) -> None:
        """Teszteli az egyszerű érték lekérését."""
        manager = YAMLConfigManager(filename=temp_config_file)

        assert manager.get("database", "host") == "localhost"
        assert manager.get("database", "port") == 5432

    def test_get_nested_value(self, temp_config_file: str) -> None:
        """Teszteli a beágyazott érték lekérését."""
        manager = YAMLConfigManager(filename=temp_config_file)

        result = manager.get("database")
        assert isinstance(result, dict)
        assert result["host"] == "localhost"

    def test_get_with_default(self, temp_config_file: str) -> None:
        """Teszteli az alapértelmezett érték használatát."""
        manager = YAMLConfigManager(filename=temp_config_file)

        assert manager.get("nonexistent", default="default_value") == "default_value"
        assert manager.get("database", "nonexistent", default=999) == 999

    def test_get_section(self, temp_config_file: str) -> None:
        """Teszteli a teljes szekció lekérését."""
        manager = YAMLConfigManager(filename=temp_config_file)

        database_section = manager.get_section("database")
        assert database_section["host"] == "localhost"
        assert database_section["port"] == 5432

    def test_get_section_nonexistent(self, temp_config_file: str) -> None:
        """Teszteli a nem létező szekció lekérését."""
        manager = YAMLConfigManager(filename=temp_config_file)

        with pytest.raises(KeyError, match="Konfigurációs szekció nem található"):
            manager.get_section("nonexistent")

    def test_set_simple_value(self) -> None:
        """Teszteli az egyszerű érték beállítását."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        assert manager.get("key") == "value"

    def test_set_nested_value(self) -> None:
        """Teszteli a beágyazott érték beállítását."""
        manager = YAMLConfigManager()
        manager.set("database", "host", value="localhost")
        manager.set("database", "port", value=5432)

        assert manager.get("database", "host") == "localhost"
        assert manager.get("database", "port") == 5432

    def test_set_without_keys(self) -> None:
        """Teszteli az érték beállítását kulcsok nélkül."""
        manager = YAMLConfigManager()

        with pytest.raises(ValueError, match="Legalább egy kulcsot meg kell adni"):
            manager.set(value="test")

    def test_save_to_file(self, temp_config_file: str) -> None:
        """Teszteli a konfiguráció mentését fájlba."""
        manager = YAMLConfigManager()
        manager.set("test", "key", value="value")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_save_file = f.name

        try:
            manager.save(temp_save_file)

            loaded_manager = YAMLConfigManager(filename=temp_save_file)
            assert loaded_manager.get("test", "key") == "value"
        finally:
            os.unlink(temp_save_file)

    def test_save_without_filename(self) -> None:
        """Teszteli a mentést fájlnév nélkül."""
        manager = YAMLConfigManager()
        manager.set("test", value="value")

        with pytest.raises(ValueError, match="Nincs fájlnév megadva"):
            manager.save()

    def test_validate_valid_schema(self, temp_config_file: str) -> None:
        """Teszteli az érvényes séma validálását."""
        manager = YAMLConfigManager(filename=temp_config_file)

        schema = {
            "database": {
                "type": "dict",
                "schema": {
                    "host": {"type": "str"},
                    "port": {"type": "int"},
                    "username": {"type": "str", "optional": True},
                },
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid
        assert errors is None

    def test_validate_invalid_schema(self, temp_config_file: str) -> None:
        """Teszteli az érvénytelen séma validálását."""
        manager = YAMLConfigManager(filename=temp_config_file)

        schema = {
            "database": {
                "type": "dict",
                "schema": {
                    "host": {"type": "int"},  # Típus hiba
                    "required_field": {"type": "str"},  # Hiányzó kötelező mező
                },
            }
        }

        is_valid, errors = manager.validate(schema)
        assert not is_valid
        assert errors is not None
        assert len(errors) > 0

    def test_validate_type_constraints(self) -> None:
        """Teszteli a típus korlátok validálását."""
        manager = YAMLConfigManager()
        manager.set("test", "string_value", value="hello")
        manager.set("test", "int_value", value=42)
        manager.set("test", "float_value", value=3.14)

        schema = {
            "test": {
                "type": "dict",
                "schema": {
                    "string_value": {"type": "str"},
                    "int_value": {"type": "int", "min": 0, "max": 100},
                    "float_value": {"type": "float", "min": 0.0, "max": 10.0},
                },
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid
        assert errors is None

    def test_validate_choices(self) -> None:
        """Teszteli a választható értékek validálását."""
        manager = YAMLConfigManager()
        manager.set("log_level", value="INFO")

        schema = {"log_level": {"type": "str", "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]}}

        is_valid, errors = manager.validate(schema)
        assert is_valid
        assert errors is None

    def test_validate_invalid_choices(self) -> None:
        """Teszteli az érvénytelen választék validálását."""
        manager = YAMLConfigManager()
        manager.set("log_level", value="INVALID")

        schema = {"log_level": {"type": "str", "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]}}

        is_valid, errors = manager.validate(schema)
        assert not is_valid
        assert errors is not None

    def test_dependency_injection(self) -> None:
        """Teszteli a függőség injektálást."""
        from unittest.mock import Mock

        mock_logger = Mock()
        mock_storage = Mock()

        manager = YAMLConfigManager(logger=mock_logger, storage=mock_storage)

        assert manager._logger is mock_logger
        assert manager._storage is mock_storage

    def test_ensure_dict_with_dict(self) -> None:
        """Teszteli a dictionary ellenőrzést dictionary értékkel."""
        result = YAMLConfigManager._ensure_dict({"key": "value"})
        assert result == {"key": "value"}

    def test_ensure_dict_with_none(self) -> None:
        """Teszteli a dictionary ellenőrzést None értékkel."""
        result = YAMLConfigManager._ensure_dict(None)
        assert result == {}

    def test_ensure_dict_with_invalid_type(self) -> None:
        """Teszteli a dictionary ellenőrzést érvénytelen típussal."""
        with pytest.raises(ConfigLoadError, match="dictionary típusúnak kell lennie"):
            YAMLConfigManager._ensure_dict("not a dict")
