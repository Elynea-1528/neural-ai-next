"""Tesztek a konfigurációkezelő kivételeihez.

Ez a modul tartalmazza a neural_ai.core.config.exceptions modul
összes kivétel osztályának tesztjeit.
"""

import pytest

from neural_ai.core.config.exceptions import (
    ConfigError,
    ConfigKeyError,
    ConfigLoadError,
    ConfigSaveError,
    ConfigTypeError,
    ConfigValidationError,
)


class TestConfigError:
    """Tesztek a ConfigError alaposztályhoz."""

    def test_config_error_basic_initialization(self) -> None:
        """Teszteli a ConfigError alap inicializálását."""
        error = ConfigError("Alap hibaüzenet")

        assert str(error) == "Alap hibaüzenet"
        assert error.error_code is None

    def test_config_error_with_error_code(self) -> None:
        """Teszteli a ConfigError inicializálását hibakóddal."""
        error = ConfigError("Hibaüzenet", error_code="TEST_ERROR")

        assert str(error) == "Hibaüzenet"
        assert error.error_code == "TEST_ERROR"

    def test_config_error_is_exception(self) -> None:
        """Teszteli, hogy a ConfigError az Exception osztályból származik."""
        error = ConfigError("Hiba")

        assert isinstance(error, Exception)
        assert isinstance(error, ConfigError)


class TestConfigLoadError:
    """Tesztek a ConfigLoadError osztályhoz."""

    def test_config_load_error_basic_initialization(self) -> None:
        """Teszteli a ConfigLoadError alap inicializálását."""
        error = ConfigLoadError("Betöltési hiba")

        assert str(error) == "Betöltési hiba"
        assert error.error_code == "CONFIG_LOAD_ERROR"
        assert error.file_path is None
        assert error.original_error is None

    def test_config_load_error_with_file_path(self) -> None:
        """Teszteli a ConfigLoadError inicializálását fájlúttal."""
        error = ConfigLoadError("Betöltési hiba", file_path="/path/to/config.yaml")

        assert str(error) == "Betöltési hiba"
        assert error.file_path == "/path/to/config.yaml"
        assert error.original_error is None

    def test_config_load_error_with_original_error(self) -> None:
        """Teszteli a ConfigLoadError inicializálását eredeti hibával."""
        original = FileNotFoundError("Fájl nem található")
        error = ConfigLoadError("Betöltési hiba", original_error=original)

        assert str(error) == "Betöltési hiba"
        assert error.original_error == original

    def test_config_load_error_inheritance(self) -> None:
        """Teszteli a ConfigLoadError öröklődési láncolatát."""
        error = ConfigLoadError("Hiba")

        assert isinstance(error, ConfigLoadError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)


class TestConfigSaveError:
    """Tesztek a ConfigSaveError osztályhoz."""

    def test_config_save_error_basic_initialization(self) -> None:
        """Teszteli a ConfigSaveError alap inicializálását."""
        error = ConfigSaveError("Mentési hiba")

        assert str(error) == "Mentési hiba"
        assert error.error_code == "CONFIG_SAVE_ERROR"
        assert error.file_path is None
        assert error.original_error is None

    def test_config_save_error_with_file_path(self) -> None:
        """Teszteli a ConfigSaveError inicializálását fájlúttal."""
        error = ConfigSaveError("Mentési hiba", file_path="/path/to/output.yaml")

        assert str(error) == "Mentési hiba"
        assert error.file_path == "/path/to/output.yaml"

    def test_config_save_error_with_original_error(self) -> None:
        """Teszteli a ConfigSaveError inicializálását eredeti hibával."""
        original = PermissionError("Hozzáférés megtagadva")
        error = ConfigSaveError("Mentési hiba", original_error=original)

        assert str(error) == "Mentési hiba"
        assert error.original_error == original

    def test_config_save_error_inheritance(self) -> None:
        """Teszteli a ConfigSaveError öröklődési láncolatát."""
        error = ConfigSaveError("Hiba")

        assert isinstance(error, ConfigSaveError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)


class TestConfigValidationError:
    """Tesztek a ConfigValidationError osztályhoz."""

    def test_config_validation_error_basic_initialization(self) -> None:
        """Teszteli a ConfigValidationError alap inicializálását."""
        error = ConfigValidationError("Validációs hiba")

        assert str(error) == "Validációs hiba"
        assert error.error_code == "CONFIG_VALIDATION_ERROR"
        assert error.field_path is None
        assert error.invalid_value is None

    def test_config_validation_error_with_field_path(self) -> None:
        """Teszteli a ConfigValidationError inicializálását mezőúttal."""
        error = ConfigValidationError("Validációs hiba", field_path="database.host")

        assert str(error) == "Validációs hiba"
        assert error.field_path == "database.host"

    def test_config_validation_error_with_invalid_value(self) -> None:
        """Teszteli a ConfigValidationError inicializálását érvénytelen értékkel."""
        error = ConfigValidationError("Validációs hiba", invalid_value="invalid_value")

        assert str(error) == "Validációs hiba"
        assert error.invalid_value == "invalid_value"

    def test_config_validation_error_inheritance(self) -> None:
        """Teszteli a ConfigValidationError öröklődési láncolatát."""
        error = ConfigValidationError("Hiba")

        assert isinstance(error, ConfigValidationError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)


class TestConfigTypeError:
    """Tesztek a ConfigTypeError osztályhoz."""

    def test_config_type_error_basic_initialization(self) -> None:
        """Teszteli a ConfigTypeError alap inicializálását."""
        error = ConfigTypeError("Típus hiba")

        assert str(error) == "Típus hiba"
        assert error.error_code == "CONFIG_TYPE_ERROR"
        assert error.field_path is None
        assert error.expected_type is None
        assert error.actual_type is None

    def test_config_type_error_with_field_path(self) -> None:
        """Teszteli a ConfigTypeError inicializálását mezőúttal."""
        error = ConfigTypeError("Típus hiba", field_path="settings.timeout")

        assert str(error) == "Típus hiba"
        assert error.field_path == "settings.timeout"

    def test_config_type_error_with_types(self) -> None:
        """Teszteli a ConfigTypeError inicializálását típusokkal."""
        error = ConfigTypeError("Típus hiba", expected_type="int", actual_type="str")

        assert str(error) == "Típus hiba"
        assert error.expected_type == "int"
        assert error.actual_type == "str"

    def test_config_type_error_complete_initialization(self) -> None:
        """Teszteli a ConfigTypeError teljes inicializálását."""
        error = ConfigTypeError(
            "Típus hiba", field_path="config.port", expected_type="int", actual_type="str"
        )

        assert str(error) == "Típus hiba"
        assert error.field_path == "config.port"
        assert error.expected_type == "int"
        assert error.actual_type == "str"

    def test_config_type_error_inheritance(self) -> None:
        """Teszteli a ConfigTypeError öröklődési láncolatát."""
        error = ConfigTypeError("Hiba")

        assert isinstance(error, ConfigTypeError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)


class TestConfigKeyError:
    """Tesztek a ConfigKeyError osztályhoz."""

    def test_config_key_error_basic_initialization(self) -> None:
        """Teszteli a ConfigKeyError alap inicializálását."""
        error = ConfigKeyError("Kulcs hiba")

        assert str(error) == "Kulcs hiba"
        assert error.error_code == "CONFIG_KEY_ERROR"
        assert error.key_path is None
        assert error.available_keys == []

    def test_config_key_error_with_key_path(self) -> None:
        """Teszteli a ConfigKeyError inicializálását kulcsúttal."""
        error = ConfigKeyError("Kulcs hiba", key_path="missing.key")

        assert str(error) == "Kulcs hiba"
        assert error.key_path == "missing.key"

    def test_config_key_error_with_available_keys(self) -> None:
        """Teszteli a ConfigKeyError inicializálását elérhető kulcsokkal."""
        available = ["key1", "key2", "key3"]
        error = ConfigKeyError("Kulcs hiba", available_keys=available)

        assert str(error) == "Kulcs hiba"
        assert error.available_keys == available

    def test_config_key_error_complete_initialization(self) -> None:
        """Teszteli a ConfigKeyError teljes inicializálását."""
        available = ["host", "port", "database"]
        error = ConfigKeyError("Kulcs hiba", key_path="username", available_keys=available)

        assert str(error) == "Kulcs hiba"
        assert error.key_path == "username"
        assert error.available_keys == available

    def test_config_key_error_inheritance(self) -> None:
        """Teszteli a ConfigKeyError öröklődési láncolatát."""
        error = ConfigKeyError("Hiba")

        assert isinstance(error, ConfigKeyError)
        assert isinstance(error, ConfigError)
        assert isinstance(error, Exception)


class TestExceptionHierarchy:
    """Tesztek a kivétel hierarchiához."""

    def test_exception_hierarchy_structure(self) -> None:
        """Teszteli a kivétel hierarchia szerkezetét."""
        # Alap kivételek
        config_error = ConfigError("Hiba")

        # Leszármazott kivételek
        load_error = ConfigLoadError("Betöltési hiba")
        save_error = ConfigSaveError("Mentési hiba")
        validation_error = ConfigValidationError("Validációs hiba")
        type_error = ConfigTypeError("Típus hiba")
        key_error = ConfigKeyError("Kulcs hiba")

        # Ellenőrzések
        assert isinstance(load_error, ConfigError)
        assert isinstance(save_error, ConfigError)
        assert isinstance(validation_error, ConfigError)
        assert isinstance(type_error, ConfigError)
        assert isinstance(key_error, ConfigError)

        # Gyökér ellenőrzés
        assert isinstance(config_error, Exception)
        assert isinstance(load_error, Exception)
        assert isinstance(save_error, Exception)
        assert isinstance(validation_error, Exception)
        assert isinstance(type_error, Exception)
        assert isinstance(key_error, Exception)


class TestExceptionUsage:
    """Tesztek a kivételek használatához."""

    def test_raise_and_catch_specific_error(self) -> None:
        """Teszteli a specifikus kivétel dobását és elkapását."""
        with pytest.raises(ConfigLoadError) as exc_info:
            raise ConfigLoadError("Fájl nem található")

        assert str(exc_info.value) == "Fájl nem található"
        assert exc_info.value.error_code == "CONFIG_LOAD_ERROR"

    def test_raise_and_catch_base_error(self) -> None:
        """Teszteli az alap kivétel dobását és elkapását."""
        with pytest.raises(ConfigError) as exc_info:
            raise ConfigLoadError("Betöltési hiba")

        assert isinstance(exc_info.value, ConfigLoadError)
        assert str(exc_info.value) == "Betöltési hiba"

    def test_exception_chaining(self) -> None:
        """Teszteli a kivétel láncolatot."""
        original = FileNotFoundError("Fájl nem található")

        with pytest.raises(ConfigLoadError) as exc_info:
            raise ConfigLoadError("Konfiguráció betöltése sikertelen", original_error=original)

        assert exc_info.value.original_error == original
        assert isinstance(exc_info.value.original_error, FileNotFoundError)
