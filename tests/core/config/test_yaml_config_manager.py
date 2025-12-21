"""YAML config manager tesztek."""

import os
from pathlib import Path
from typing import Any
from unittest.mock import mock_open, patch

import pytest
import yaml

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations import YAMLConfigManager


@pytest.fixture
def sample_config_data() -> dict[str, Any]:
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
def config_manager(sample_config_data: dict[str, Any]) -> YAMLConfigManager:
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

    with open(filename, encoding="utf-8") as f:
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


def test_get_with_non_dict_intermediate_value(config_manager: YAMLConfigManager) -> None:
    """Lekérés, amikor egy köztes érték nem dict."""
    # A 'logging' kulcshoz tartozó érték egy dict, de a 'level' egy string
    # Ha megpróbáljuk lekérni a 'level' alatt egy másik kulcsot, hibát kell kapjunk
    # Módosítjuk a 'level' értékét egy stringre, ami nem dict
    config_manager._config["logging"]["level"] = "INFO"  # pylint: disable=protected-access
    # A 'get' metódusnak a 'level' kulcs alól nem szabad tovább mennie
    # A teszt arra szolgál, hogy lefedje a 66. sort, ahol a get metódus ellenőrzi, hogy a rész-érték dict-e
    # Mivel a 'level' egy string, a get metódusnak a default értéket kell visszaadnia
    result = config_manager.get("logging", "level", "nonexistent", default="default_value")
    assert result == "default_value"


def test_set_with_empty_keys_raises_valueerror(config_manager: YAMLConfigManager) -> None:
    """Beállítás üres kulcslistával hiba."""
    with pytest.raises(ValueError):
        config_manager.set(value="value")


def test_save_raises_valueerror_on_invalid_data(config_manager: YAMLConfigManager) -> None:
    """Mentés érvénytelen adatokkal hiba."""
    # A YAML dumpolás során fellépő hibát mock-oljuk
    with patch("yaml.safe_dump") as mock_dump:
        mock_dump.side_effect = ValueError("Invalid data")
        with pytest.raises(ValueError):
            config_manager.save("test.yaml")


def test_load_file_not_found_raises_configloaderror() -> None:
    """Fájl nem található betöltéskor hiba."""
    manager = YAMLConfigManager()
    with pytest.raises(ConfigLoadError):
        manager.load("nonexistent.yaml")


def test_validate_dict_with_non_dict_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a dict schema nem dict értéket talál."""
    # A 'database.host' egy string, de a schema dict-ként várja
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {
                    "type": "dict",  # Típus eltérés: a valós érték string
                    "schema": {"nested": {"type": "str"}},
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.host" in errors


def test_validate_required_with_none_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor egy kötelező mező értéke None."""
    # Beállítunk egy kötelező mezőt None-ra
    config_manager._config["database"]["host"] = None  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {"type": "str"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.host" in errors


def test_validate_type_with_missing_type_in_schema(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a schema nem tartalmaz type mezőt."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {},  # Nincs 'type' mező
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    # A _validate_type metódusnak kezelnie kell ezt az esetet
    # A teszt arra szolgál, hogy lefedje a 164. sort, ahol a 'type' kulcs hiánya kezelődik
    assert valid  # Mivel nincs típusellenőrzés, a validáció sikeres
    assert errors is None


def test_validate_type_with_unknown_type(config_manager: YAMLConfigManager) -> None:
    """Validálás ismeretlen típussal."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {"type": "unknown_type"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.host" in errors


def test_validate_nested_with_non_dict_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a nested schema nem dict értéket talál."""
    # A 'database.credentials' egy dict, de a 'username' egy string
    # A schema a 'username' alá nested schema-t vár
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "credentials": {
                    "type": "dict",
                    "schema": {
                        "username": {  # A valós érték string, de nested schema van megadva
                            "type": "dict",
                            "schema": {"nested": {"type": "str"}},
                        },
                    },
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.credentials.username" in errors


def test_validate_range_invalid_min(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor egy számérték kisebb a megengedettnél."""
    # Először módosítjuk a port értékét, hogy kisebb legyen a minimumánál
    config_manager._config["database"]["port"] = 500  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "port": {
                    "type": "int",
                    "min": 1000,
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.port" in errors


def test_validate_range_invalid_max(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor egy számérték nagyobb a megengedettnél."""
    # Először módosítjuk a port értékét, hogy nagyobb legyen a maximumánál
    config_manager._config["database"]["port"] = 10000  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "port": {
                    "type": "int",
                    "max": 9999,
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.port" in errors


def test_validate_range_valid(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor egy számérték a megengedett tartományban van."""
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "port": {
                    "type": "int",
                    "min": 1000,
                    "max": 9999,
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert valid
    assert errors is None


def test_load_yaml_with_none_content(tmp_path: Path) -> None:
    """YAML fájl betöltése, ami None tartalmat ad vissza."""
    filename = str(tmp_path / "none_content.yaml")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")  # Üres fájl, ami yaml.safe_load() során None-t ad vissza

    manager = YAMLConfigManager()
    manager.load(filename)
    # Az üres fájlból betöltött konfigurációnak üres dict-nek kell lennie
    assert manager._config == {}  # pylint: disable=protected-access


def test_load_yaml_with_non_dict_content(tmp_path: Path) -> None:
    """YAML fájl betöltése, ami nem dict tartalmat ad vissza."""
    filename = str(tmp_path / "non_dict.yaml")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("- item1\n- item2")  # Lista, nem dict

    manager = YAMLConfigManager()
    with pytest.raises(ConfigLoadError):
        manager.load(filename)


def test_save_with_no_filename_raises_valueerror(config_manager: YAMLConfigManager) -> None:
    """Mentés fájlnév nélkül hiba."""
    # A manager nem lett inicializálva fájlnévvel, és a save sem kapott
    with pytest.raises(ValueError, match="Nincs fájlnév megadva a mentési művelethez"):
        config_manager.save()


def test_validate_dict_with_none_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a dict schema None értéket talál."""
    # A 'database' kulcsot None-ra állítjuk
    config_manager._config["database"] = None  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "optional": True,  # Opcionálissá tesszük, hogy a _validate_required ne kapja el
            "schema": {
                "host": {"type": "str"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database" in errors
    assert "Dictionary típusú érték szükséges" in errors["database"]


def test_validate_type_with_none_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a típusellenőrzés None értéket kap."""
    # A 'database.host' kulcsot None-ra állítjuk
    config_manager._config["database"]["host"] = None  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "host": {"type": "str"},
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    # A _validate_type metódusnak a None értéknél True-t kell visszaadnia (163. sor)
    # A hiba a _validate_required-ban keletkezik, mert a mező kötelező
    assert not valid
    assert errors is not None
    assert "database.host" in errors


def test_validate_nested_with_none_value(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor a nested schema None értéket talál."""
    # A 'database.credentials' kulcsot None-ra állítjuk
    config_manager._config["database"]["credentials"] = None  # pylint: disable=protected-access
    schema = {
        "database": {
            "type": "dict",
            "schema": {
                "credentials": {
                    "type": "dict",
                    "optional": True,  # Opcionálissá tesszük, hogy a _validate_required ne kapja el
                    "schema": {
                        "username": {"type": "str"},
                    },
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "database.credentials" in errors
    assert "Dictionary típusú érték szükséges" in errors["database.credentials"]


def test_validate_choices_invalid(config_manager: YAMLConfigManager) -> None:
    """Validálás, amikor egy érték nincs a választható értékek között."""
    schema = {
        "logging": {
            "type": "dict",
            "schema": {
                "level": {
                    "type": "str",
                    "choices": ["DEBUG", "WARNING", "ERROR"],  # Nincs INFO
                },
            },
        },
    }
    valid, errors = config_manager.validate(schema)
    assert not valid
    assert errors is not None
    assert "logging.level" in errors
    assert "Értéknek a következőek egyikének kell lennie:" in errors["logging.level"]
