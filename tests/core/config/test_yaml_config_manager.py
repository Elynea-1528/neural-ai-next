"""YAML config manager tesztek."""

import os
from pathlib import Path
from typing import Any, Dict
from unittest.mock import mock_open, patch

import pytest
import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations import YAMLConfigManager


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """Teszt konfiguráció."""
    return {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "secret",
            },
        },
        "logging": {
            "level": "INFO",
            "file": "app.log",
        },
    }


@pytest.fixture
def config_manager(sample_config_data: Dict[str, Any]) -> YAMLConfigManager:
    """YAML config manager fixture."""
    manager = YAMLConfigManager()
    manager._config = sample_config_data  # pylint: disable=protected-access
    return manager


def test_init_with_filename() -> None:
    """Filename paraméterrel inicializálás."""
    filename = "test.yaml"
    mock_yaml_content = "key: value"

    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_yaml_content)),
    ):
        manager = YAMLConfigManager(filename)
        assert manager._config == {"key": "value"}  # pylint: disable=protected-access


def test_get_existing_value(config_manager: YAMLConfigManager) -> None:
    """Létező érték lekérése."""
    assert config_manager.get("database", "host") == "localhost"
    assert config_manager.get("database", "port") == 5432
    assert config_manager.get("database", "credentials", "username") == "admin"


def test_get_with_default(config_manager: YAMLConfigManager) -> None:
    """Default érték használata nem létező kulcsnál."""
    assert config_manager.get("nonexistent", default="default") == "default"
    assert config_manager.get("database", "nonexistent", default=123) == 123


def test_get_section_existing(config_manager: YAMLConfigManager) -> None:
    """Létező szekció lekérése."""
    section = config_manager.get_section("database")
    assert section == {
        "host": "localhost",
        "port": 5432,
        "credentials": {
            "username": "admin",
            "password": "secret",
        },
    }


def test_get_section_nonexistent(config_manager: YAMLConfigManager) -> None:
    """Nem létező szekció lekérése."""
    with pytest.raises(KeyError):
        config_manager.get_section("nonexistent")


def test_set_new_value(config_manager: YAMLConfigManager) -> None:
    """Új érték beállítása."""
    config_manager.set("new", "key", value="value")
    assert config_manager.get("new", "key") == "value"


def test_set_existing_value(config_manager: YAMLConfigManager) -> None:
    """Létező érték felülírása."""
    config_manager.set("database", "host", value="newhost")
    assert config_manager.get("database", "host") == "newhost"


def test_set_nested_value(config_manager: YAMLConfigManager) -> None:
    """Beágyazott érték beállítása."""
    config_manager.set("database", "credentials", "newkey", value="value")
    assert config_manager.get("database", "credentials", "newkey") == "value"


def test_set_invalid_path(config_manager: YAMLConfigManager) -> None:
    """Érvénytelen út esetén hiba."""
    with pytest.raises(ValueError):
        config_manager.set("database", "host", "invalid", value="value")


def test_save(tmp_path: Path, config_manager: YAMLConfigManager) -> None:
    """Konfiguráció mentése."""
    filename = str(tmp_path / "config.yaml")
    config_manager.save(filename)

    with open(filename, "r", encoding="utf-8") as f:
        saved_config = yaml.safe_load(f)
        assert saved_config == config_manager._config  # pylint: disable=protected-access


def test_save_create_dirs(tmp_path: Path, config_manager: YAMLConfigManager) -> None:
    """Hiányzó könyvtárak létrehozása mentéskor."""
    filename = str(tmp_path / "subdir" / "config.yaml")
    config_manager.save(filename)
    assert os.path.exists(filename)


def test_validate_required_fields(config_manager: YAMLConfigManager) -> None:
    """Kötelező mezők validálása."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {"type": "str"},
                "port": {"type": "int"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert valid
    assert errors is None


def test_validate_missing_required(config_manager: YAMLConfigManager) -> None:
    """Hiányzó kötelező mezők validálása."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "missing": {"type": "str"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.missing" in errors


def test_validate_invalid_type(config_manager: YAMLConfigManager) -> None:
    """Hibás típus validálása."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {"type": "int"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.host" in errors


def test_validate_choices(config_manager: YAMLConfigManager) -> None:
    """Választható értékek validálása."""
    schema = {
        "logging": {
            "type": "dict",
            "schema": {
                "level": {
                    "type": "str",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert valid
    assert errors is None


def test_load_invalid_yaml(tmp_path: Path) -> None:
    """Érvénytelen YAML fájl betöltése."""
    filename = str(tmp_path / "invalid.yaml")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("invalid: yaml: content}")

    manager = YAMLConfigManager()
    with pytest.raises(ConfigLoadError):
        manager.load(filename)
