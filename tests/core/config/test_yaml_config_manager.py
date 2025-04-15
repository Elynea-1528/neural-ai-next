"""YAML konfiguráció kezelő tesztek.

Ez a modul tartalmazza a YAML alapú konfigurációkezelő tesztjeit.
"""

from typing import Dict, Any, cast

import pytest
import yaml

from neural_ai.core.config.implementations import YAMLConfigManager


class TestYAMLConfigManager:
    """YAML konfiguráció kezelő tesztek."""

    @pytest.fixture
    def config_data(self) -> Dict[str, Any]:
        """Teszt konfigurációs adatok."""
        return {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": "secret"
                }
            },
            "logging": {
                "level": "INFO",
                "file": "app.log"
            },
            "features": ["auth", "cache", "metrics"]
        }

    @pytest.fixture
    def yaml_manager(self) -> YAMLConfigManager:
        """YAML config manager példány."""
        return YAMLConfigManager()

    def test_initialization(self) -> None:
        """Teszteli az inicializálást."""
        manager = YAMLConfigManager()
        assert isinstance(manager, YAMLConfigManager)
        assert manager._config == {}

    def test_initialization_with_file(
        self, config_data: Dict[str, Any], tmp_path
    ) -> None:
        """Teszteli a fájlból történő inicializálást."""
        config_file = tmp_path / "config.yaml"
        yaml_content = yaml.dump(config_data)
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(yaml_content)

        manager = YAMLConfigManager(str(config_file))
        assert manager._config == config_data

    def test_get_nested_value(
        self,
        yaml_manager: YAMLConfigManager,
        config_data: Dict[str, Any]
    ) -> None:
        """Teszteli a beágyazott értékek lekérését."""
        yaml_manager._config = config_data

        assert yaml_manager.get("database", "host") == "localhost"
        assert yaml_manager.get("database", "credentials", "username") == "admin"
        assert yaml_manager.get("nonexistent", default="default") == "default"

    def test_get_section(
        self,
        yaml_manager: YAMLConfigManager,
        config_data: Dict[str, Any]
    ) -> None:
        """Teszteli a teljes szekció lekérését."""
        yaml_manager._config = config_data

        database = yaml_manager.get_section("database")
        assert database["host"] == "localhost"
        assert database["port"] == 5432

        with pytest.raises(KeyError):
            yaml_manager.get_section("nonexistent")

    def test_set_value(self, yaml_manager: YAMLConfigManager) -> None:
        """Teszteli az értékek beállítását."""
        yaml_manager.set("database", "host", value="example.com")
        assert yaml_manager.get("database", "host") == "example.com"

        yaml_manager.set("new", "key", "subkey", value=42)
        assert yaml_manager.get("new", "key", "subkey") == 42

    def test_save_configuration(
        self,
        yaml_manager: YAMLConfigManager,
        config_data: Dict[str, Any],
        tmp_path
    ) -> None:
        """Teszteli a konfiguráció mentését."""
        yaml_manager._config = config_data
        save_file = tmp_path / "save.yaml"

        yaml_manager.save(str(save_file))
        assert save_file.exists()

        # Ellenőrizzük, hogy a mentett tartalom helyes
        loaded_config = yaml.safe_load(save_file.read_text())
        assert loaded_config == config_data

    def test_validation_schema(self, yaml_manager: YAMLConfigManager) -> None:
        """Teszteli a séma alapú validációt."""
        yaml_manager._config = {
            "port": 8080,
            "timeout": 30,
            "retries": -1
        }

        schema = {
            "port": {
                "type": "int",
                "min": 1,
                "max": 65535
            },
            "timeout": {
                "type": "int",
                "min": 0
            },
            "retries": {
                "type": "int",
                "min": 0
            }
        }

        is_valid, errors = yaml_manager.validate(schema)
        assert not is_valid
        assert errors is not None
        assert "retries" in errors
        assert errors["retries"].startswith("Value must be >=")

    def test_type_validation(self, yaml_manager: YAMLConfigManager) -> None:
        """Teszteli a típus validációt."""
        yaml_manager._config = {
            "number": "not_a_number",
            "list": 42
        }

        schema = {
            "number": {"type": "int"},
            "list": {"type": "list"}
        }

        is_valid, errors = yaml_manager.validate(schema)
        assert not is_valid
        errors = cast(Dict[str, str], errors)
        assert len(errors) == 2
        assert errors["number"].startswith("Invalid type")
        assert errors["list"].startswith("Invalid type")

    def test_required_fields(self, yaml_manager: YAMLConfigManager) -> None:
        """Teszteli a kötelező mezők validációját."""
        yaml_manager._config = {
            "optional_field": "value"
        }

        schema = {
            "required_field": {"type": "str"},
            "optional_field": {"type": "str", "optional": True}
        }

        is_valid, errors = yaml_manager.validate(schema)
        assert not is_valid
        assert errors is not None
        assert "required_field" in errors
        assert "missing" in errors["required_field"].lower()

    def test_choice_validation(self, yaml_manager: YAMLConfigManager) -> None:
        """Teszteli a választható értékek validációját."""
        yaml_manager._config = {
            "color": "purple",
            "size": "medium"
        }

        schema = {
            "color": {
                "type": "str",
                "choices": ["red", "green", "blue"]
            },
            "size": {
                "type": "str",
                "choices": ["small", "medium", "large"]
            }
        }

        is_valid, errors = yaml_manager.validate(schema)
        assert not is_valid
        assert errors is not None
        assert "color" in errors
        assert "one of" in errors["color"]
        assert "red" in errors["color"]
        assert "size" not in errors  # size is valid
