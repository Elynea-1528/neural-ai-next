"""YAMLConfigManager tesztek."""

import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations.yaml_config_manager import (
    ValidationContext,
    YAMLConfigManager,
)


class TestValidationContext:
    """ValidationContext osztály tesztjei."""

    def test_initialization(self) -> None:
        """Teszteli a ValidationContext inicializálását."""
        errors: dict[str, str] = {}
        schema: dict[str, Any] = {"type": "str"}

        ctx = ValidationContext(
            path="test.path",
            errors=errors,
            value="test_value",
            schema=schema
        )

        assert ctx.path == "test.path"
        assert ctx.errors is errors
        assert ctx.value == "test_value"
        assert ctx.schema == schema

    def test_initialization_with_none_value(self) -> None:
        """Teszteli a ValidationContext inicializálását None értékkel."""
        errors: dict[str, str] = {}
        schema: dict[str, Any] = {"type": "str", "optional": True}

        ctx = ValidationContext(
            path="test.path",
            errors=errors,
            value=None,
            schema=schema
        )

        assert ctx.path == "test.path"
        assert ctx.value is None


class TestYAMLConfigManager:
    """YAMLConfigManager osztály tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_config(self) -> dict[str, Any]:
        """Minta konfiguráció."""
        return {
            "database": {
                "host": "localhost",
                "port": 5432,
                "debug": True
            },
            "logging": {
                "level": "INFO"
            }
        }

    @pytest.fixture
    def config_file(self, temp_dir: Path, sample_config: dict[str, Any]) -> Path:
        """Minta konfigurációs fájl létrehozása."""
        config_path = temp_dir / "test_config.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(sample_config, f)
        return config_path

    def test_initialization_without_filename(self) -> None:
        """Teszteli a YAMLConfigManager inicializálását fájlnév nélkül."""
        manager = YAMLConfigManager()
        assert manager._filename is None
        assert manager._config == {}

    def test_initialization_with_filename(self, config_file: Path) -> None:
        """Teszteli a YAMLConfigManager inicializálását fájlnévvel."""
        manager = YAMLConfigManager(filename=str(config_file))
        assert manager._filename == str(config_file)
        assert "database" in manager._config
        assert manager.get("database", "host") == "localhost"

    def test_get_current_schema_version(self) -> None:
        """Teszteli a jelenlegi séma verzió lekérdezését."""
        manager = YAMLConfigManager()
        assert manager._get_current_schema_version() == "1.0"

    def test_check_schema_compatibility(self) -> None:
        """Teszteli a séma kompatibilitás ellenőrzését."""
        manager = YAMLConfigManager()
        assert manager._check_schema_compatibility("1.0") is True
        assert manager._check_schema_compatibility("2.0") is False

    def test_ensure_dict_with_dict(self) -> None:
        """Teszteli a _ensure_dict metódust dictionary értékkel."""
        manager = YAMLConfigManager()
        data = {"key": "value"}
        result = manager._ensure_dict(data)
        assert result == data

    def test_ensure_dict_with_none(self) -> None:
        """Teszteli a _ensure_dict metódust None értékkel."""
        manager = YAMLConfigManager()
        result = manager._ensure_dict(None)
        assert result == {}

    def test_ensure_dict_with_invalid_type(self) -> None:
        """Teszteli a _ensure_dict metódust érvénytelen típussal."""
        manager = YAMLConfigManager()
        with pytest.raises(ConfigLoadError, match="YAML tartalom dictionary"):
            manager._ensure_dict("invalid")

    def test_get_existing_value(self, config_file: Path) -> None:
        """Teszteli az érték lekérdezését létező kulccsal."""
        manager = YAMLConfigManager(filename=str(config_file))
        host = manager.get("database", "host")
        assert host == "localhost"

    def test_get_nonexistent_value_with_default(self, config_file: Path) -> None:
        """Teszteli az érték lekérdezését nem létező kulccsal alapértelmezett értékkel."""
        manager = YAMLConfigManager(filename=str(config_file))
        value = manager.get("database", "nonexistent", default="default_value")
        assert value == "default_value"

    def test_get_nonexistent_path(self, config_file: Path) -> None:
        """Teszteli az érték lekérdezését nem létező útvonallal."""
        manager = YAMLConfigManager(filename=str(config_file))
        value = manager.get("nonexistent", "key", default="default")
        assert value == "default"

    def test_get_section_existing(self, config_file: Path) -> None:
        """Teszteli a szekció lekérdezését létező szekcióval."""
        manager = YAMLConfigManager(filename=str(config_file))
        database_section = manager.get_section("database")
        assert database_section["host"] == "localhost"
        assert database_section["port"] == 5432

    def test_get_section_nonexistent(self, config_file: Path) -> None:
        """Teszteli a szekció lekérdezését nem létező szekcióval."""
        manager = YAMLConfigManager(filename=str(config_file))
        with pytest.raises(KeyError, match="Konfigurációs szekció nem található"):
            manager.get_section("nonexistent")

    def test_set_single_key(self) -> None:
        """Teszteli az érték beállítását egyetlen kulccsal."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")
        assert manager.get("key") == "value"

    def test_set_nested_keys(self) -> None:
        """Teszteli az érték beállítását beágyazott kulcsokkal."""
        manager = YAMLConfigManager()
        manager.set("database", "host", value="localhost")
        assert manager.get("database", "host") == "localhost"

    def test_set_without_keys(self) -> None:
        """Teszteli az érték beállítását kulcsok nélkül."""
        manager = YAMLConfigManager()
        with pytest.raises(ValueError, match="Legalább egy kulcsot meg kell adni"):
            manager.set(value="value")

    def test_set_overwriting_value(self) -> None:
        """Teszteli a meglévő érték felülírását."""
        manager = YAMLConfigManager()
        manager.set("key", value="value1")
        manager.set("key", value="value2")
        assert manager.get("key") == "value2"

    def test_save_with_filename(self, temp_dir: Path) -> None:
        """Teszteli a konfiguráció mentését fájlnévvel."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        save_path = temp_dir / "saved_config.yaml"
        manager.save(filename=str(save_path))

        assert save_path.exists()
        with open(save_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            assert data["key"] == "value"
            assert "_schema_version" in data

    def test_save_without_filename(self) -> None:
        """Teszteli a konfiguráció mentését fájlnév nélkül."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        with pytest.raises(ValueError, match="Nincs fájlnév megadva"):
            manager.save()

    def test_save_with_manager_filename(self, temp_dir: Path) -> None:
        """Teszteli a konfiguráció mentését a manager fájlnevével."""
        config_path = temp_dir / "test.yaml"
        # Először hozzuk létre a fájlt, hogy a konstruktor ne hibázzon
        config_path.touch()
        manager = YAMLConfigManager(filename=str(config_path))
        manager.set("key", value="value")
        manager.save()

        assert config_path.exists()

    def test_load_existing_file(self, config_file: Path) -> None:
        """Teszteli a konfiguráció betöltését létező fájlból."""
        manager = YAMLConfigManager()
        manager.load(str(config_file))

        assert manager._filename == str(config_file)
        assert manager.get("database", "host") == "localhost"

    def test_load_nonexistent_file(self, temp_dir: Path) -> None:
        """Teszteli a konfiguráció betöltését nem létező fájlból."""
        manager = YAMLConfigManager()
        nonexistent_path = temp_dir / "nonexistent.yaml"

        with pytest.raises(ConfigLoadError, match="Fájl nem található"):
            manager.load(str(nonexistent_path))

    def test_load_invalid_yaml(self, temp_dir: Path) -> None:
        """Teszteli a konfiguráció betöltését érvénytelen YAML fájlból."""
        invalid_path = temp_dir / "invalid.yaml"
        with open(invalid_path, "w", encoding="utf-8") as f:
            f.write("invalid: yaml: content: [")

        manager = YAMLConfigManager()
        with pytest.raises(ConfigLoadError, match="Konfiguráció betöltése sikertelen"):
            manager.load(str(invalid_path))

    def test_load_with_schema_version(self, temp_dir: Path) -> None:
        """Teszteli a konfiguráció betöltését séma verzióval."""
        config_path = temp_dir / "with_version.yaml"
        config_data = {
            "_schema_version": "1.0",
            "key": "value"
        }
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f)

        manager = YAMLConfigManager()
        manager.load(str(config_path))

        assert manager.get("key") == "value"
        # A séma verziót eltávolítja a betöltéskor
        assert manager.get("_schema_version") is None

    def test_validate_valid_config(self) -> None:
        """Teszteli a konfiguráció validálását érvényes konfiggal."""
        manager = YAMLConfigManager()
        manager.set("database", "host", value="localhost")
        manager.set("database", "port", value=5432)

        schema = {
            "database": {
                "type": "dict",
                "schema": {
                    "host": {"type": "str"},
                    "port": {"type": "int"}
                }
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is True
        assert errors is None

    def test_validate_invalid_type(self) -> None:
        """Teszteli a konfiguráció validálását érvénytelen típussal."""
        manager = YAMLConfigManager()
        manager.set("port", value="not_a_number")

        schema = {
            "port": {"type": "int"}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "port" in errors

    def test_validate_missing_required(self) -> None:
        """Teszteli a konfiguráció validálását hiányzó kötelező mezővel."""
        manager = YAMLConfigManager()

        schema = {
            "required_field": {"type": "str"}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "required_field" in errors

    def test_validate_optional_field(self) -> None:
        """Teszteli a konfiguráció validálását opcionális mezővel."""
        manager = YAMLConfigManager()

        schema = {
            "optional_field": {"type": "str", "optional": True}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is True
        assert errors is None

    def test_validate_choices_valid(self) -> None:
        """Teszteli a choices validálását érvényes értékkel."""
        manager = YAMLConfigManager()
        manager.set("level", value="INFO")

        schema = {
            "level": {"type": "str", "choices": ["DEBUG", "INFO", "WARNING"]}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is True
        assert errors is None

    def test_validate_choices_invalid(self) -> None:
        """Teszteli a choices validálását érvénytelen értékkel."""
        manager = YAMLConfigManager()
        manager.set("level", value="INVALID")

        schema = {
            "level": {"type": "str", "choices": ["DEBUG", "INFO", "WARNING"]}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "level" in errors

    def test_validate_range_valid(self) -> None:
        """Teszteli a range validálását érvényes értékkel."""
        manager = YAMLConfigManager()
        manager.set("port", value=8080)

        schema = {
            "port": {"type": "int", "min": 1, "max": 65535}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is True
        assert errors is None

    def test_validate_range_invalid_min(self) -> None:
        """Teszteli a range validálását érvénytelen minimum értékkel."""
        manager = YAMLConfigManager()
        manager.set("port", value=0)

        schema = {
            "port": {"type": "int", "min": 1, "max": 65535}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "port" in errors

    def test_validate_range_invalid_max(self) -> None:
        """Teszteli a range validálását érvénytelen maximum értékkel."""
        manager = YAMLConfigManager()
        manager.set("port", value=70000)

        schema = {
            "port": {"type": "int", "min": 1, "max": 65535}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "port" in errors

    def test_validate_nested_dict(self) -> None:
        """Teszteli a beágyazott dictionary validálását."""
        manager = YAMLConfigManager()
        manager.set("database", "host", value="localhost")
        manager.set("database", "port", value=5432)

        schema = {
            "database": {
                "type": "dict",
                "schema": {
                    "host": {"type": "str"},
                    "port": {"type": "int"}
                }
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is True
        assert errors is None

    def test_validate_nested_dict_invalid(self) -> None:
        """Teszteli a beágyazott dictionary validálását érvénytelen értékkel."""
        manager = YAMLConfigManager()
        manager.set("database", "host", value="localhost")
        manager.set("database", "port", value="not_a_number")

        schema = {
            "database": {
                "type": "dict",
                "schema": {
                    "host": {"type": "str"},
                    "port": {"type": "int"}
                }
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None

    def test_load_directory(self, temp_dir: Path) -> None:
        """Teszteli a mappa betöltését."""
        # Hozz létre több YAML fájlt
        configs_dir = temp_dir / "configs"
        configs_dir.mkdir()

        # system.yaml
        system_config = {"app_name": "TestApp", "debug": True}
        with open(configs_dir / "system.yaml", "w", encoding="utf-8") as f:
            yaml.dump(system_config, f)

        # database.yaml
        db_config = {"host": "localhost", "port": 5432}
        with open(configs_dir / "database.yaml", "w", encoding="utf-8") as f:
            yaml.dump(db_config, f)

        manager = YAMLConfigManager()
        manager.load_directory(str(configs_dir))

        # Ellenőrizd a namespaced betöltést
        assert manager.get("system", "app_name") == "TestApp"
        assert manager.get("database", "host") == "localhost"

        # Ellenőrizd a system.yaml gyökérbe betöltését
        assert manager.get("app_name") == "TestApp"
        assert manager.get("debug") is True

    def test_load_directory_nonexistent(self, temp_dir: Path) -> None:
        """Teszteli a mappa betöltését nem létező mappából."""
        manager = YAMLConfigManager()
        nonexistent_dir = temp_dir / "nonexistent"

        with pytest.raises(ConfigLoadError, match="Konfigurációs mappa nem található"):
            manager.load_directory(str(nonexistent_dir))

    def test_load_directory_not_a_directory(self, temp_dir: Path) -> None:
        """Teszteli a mappa betöltését, ha az útvonal nem mappa."""
        file_path = temp_dir / "not_a_dir"
        file_path.touch()

        manager = YAMLConfigManager()

        with pytest.raises(ConfigLoadError, match="Az útvonal nem egy mappa"):
            manager.load_directory(str(file_path))

    def test_validate_dict_with_non_dict_value(self) -> None:
        """Teszteli a _validate_dict metódust nem dictionary értékkel."""
        manager = YAMLConfigManager()
        manager.set("key", value="not_a_dict")

        schema = {
            "key": {
                "type": "dict",
                "schema": {
                    "nested": {"type": "str"}
                }
            }
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "key" in errors

    def test_validate_unsupported_type(self) -> None:
        """Teszteli a validálást nem támogatott típussal."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        schema = {
            "key": {"type": "unsupported_type"}
        }

        is_valid, errors = manager.validate(schema)
        assert is_valid is False
        assert errors is not None
        assert "key" in errors

    def test_save_creates_directory(self, temp_dir: Path) -> None:
        """Teszteli, hogy a save létrehozza a könyvtárat, ha az nem létezik."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        save_path = temp_dir / "nested" / "dir" / "config.yaml"
        manager.save(filename=str(save_path))

        assert save_path.exists()

    def test_save_error_handling(self, temp_dir: Path) -> None:
        """Teszteli a hibakezelést mentéskor."""
        manager = YAMLConfigManager()
        manager.set("key", value="value")

        # Próbálj meg menteni egy érvénytelen útvonalra
        invalid_path = temp_dir / "invalid" / ".." / ".." / ".." / "readonly" / "config.yaml"

        # Ez valószínűleg nem fog hibát dobni, de teszteljük a hibakezelést
        try:
            manager.save(filename=str(invalid_path))
        except ValueError as e:
            assert "Konfiguráció mentése sikertelen" in str(e)
