"""Átfogó tesztek a konfigurációs kivételekhez.

Ez a modul tartalmazza a ConfigError és leszármazott osztályok
részletes tesztelését, beleértve az attribútumok ellenőrzését.
"""

import pytest

from neural_ai.core.config.exceptions.config_error import (
    ConfigError,
    ConfigKeyError,
    ConfigLoadError,
    ConfigSaveError,
    ConfigTypeError,
    ConfigValidationError,
)


class TestConfigError:
    """ConfigError alaposztály tesztjei."""

    def test_base_error_creation(self) -> None:
        """Teszteli az alap ConfigError létrehozását."""
        error = ConfigError("Alap hibaüzenet")
        assert str(error) == "Alap hibaüzenet"
        assert error.error_code is None

    def test_base_error_with_code(self) -> None:
        """Teszteli a ConfigError létrehozását hibakóddal."""
        error = ConfigError("Hibaüzenet", "ERROR_001")
        assert str(error) == "Hibaüzenet"
        assert error.error_code == "ERROR_001"


class TestConfigLoadError:
    """ConfigLoadError tesztjei."""

    def test_load_error_creation(self) -> None:
        """Teszteli a ConfigLoadError létrehozását."""
        original_error = FileNotFoundError("Fájl nem található")
        error = ConfigLoadError(
            "Betöltési hiba",
            file_path="/path/to/config.yaml",
            original_error=original_error
        )
        assert str(error) == "Betöltési hiba"
        assert error.file_path == "/path/to/config.yaml"
        assert error.original_error is original_error
        assert error.error_code == "CONFIG_LOAD_ERROR"

    def test_load_error_without_optional_params(self) -> None:
        """Teszteli a ConfigLoadError létrehozását opcionális paraméterek nélkül."""
        error = ConfigLoadError("Betöltési hiba")
        assert str(error) == "Betöltési hiba"
        assert error.file_path is None
        assert error.original_error is None
        assert error.error_code == "CONFIG_LOAD_ERROR"


class TestConfigSaveError:
    """ConfigSaveError tesztjei."""

    def test_save_error_creation(self) -> None:
        """Teszteli a ConfigSaveError létrehozását."""
        original_error = PermissionError("Hozzáférés megtagadva")
        error = ConfigSaveError(
            "Mentési hiba",
            file_path="/path/to/output.yaml",
            original_error=original_error
        )
        assert str(error) == "Mentési hiba"
        assert error.file_path == "/path/to/output.yaml"
        assert error.original_error is original_error
        assert error.error_code == "CONFIG_SAVE_ERROR"

    def test_save_error_without_optional_params(self) -> None:
        """Teszteli a ConfigSaveError létrehozását opcionális paraméterek nélkül."""
        error = ConfigSaveError("Mentési hiba")
        assert str(error) == "Mentési hiba"
        assert error.file_path is None
        assert error.original_error is None
        assert error.error_code == "CONFIG_SAVE_ERROR"


class TestConfigValidationError:
    """ConfigValidationError tesztjei."""

    def test_validation_error_creation(self) -> None:
        """Teszteli a ConfigValidationError létrehozását."""
        error = ConfigValidationError(
            "Érvénytelen érték",
            field_path="database.host",
            invalid_value=None
        )
        assert str(error) == "Érvénytelen érték"
        assert error.field_path == "database.host"
        assert error.invalid_value is None
        assert error.error_code == "CONFIG_VALIDATION_ERROR"

    def test_validation_error_without_optional_params(self) -> None:
        """Teszteli a ConfigValidationError létrehozását opcionális paraméterek nélkül."""
        error = ConfigValidationError("Érvénytelen érték")
        assert str(error) == "Érvénytelen érték"
        assert error.field_path is None
        assert error.invalid_value is None
        assert error.error_code == "CONFIG_VALIDATION_ERROR"


class TestConfigTypeError:
    """ConfigTypeError tesztjei."""

    def test_type_error_creation(self) -> None:
        """Teszteli a ConfigTypeError létrehozását."""
        error = ConfigTypeError(
            "Típus hiba",
            field_path="server.port",
            expected_type="int",
            actual_type="str"
        )
        assert str(error) == "Típus hiba"
        assert error.field_path == "server.port"
        assert error.expected_type == "int"
        assert error.actual_type == "str"
        assert error.error_code == "CONFIG_TYPE_ERROR"

    def test_type_error_without_optional_params(self) -> None:
        """Teszteli a ConfigTypeError létrehozását opcionális paraméterek nélkül."""
        error = ConfigTypeError("Típus hiba")
        assert str(error) == "Típus hiba"
        assert error.field_path is None
        assert error.expected_type is None
        assert error.actual_type is None
        assert error.error_code == "CONFIG_TYPE_ERROR"


class TestConfigKeyError:
    """ConfigKeyError tesztjei."""

    def test_key_error_creation(self) -> None:
        """Teszteli a ConfigKeyError létrehozását."""
        error = ConfigKeyError(
            "Kulcs nem található",
            key_path="database.password",
            available_keys=["host", "port", "username"]
        )
        assert str(error) == "Kulcs nem található"
        assert error.key_path == "database.password"
        assert error.available_keys == ["host", "port", "username"]
        assert error.error_code == "CONFIG_KEY_ERROR"

    def test_key_error_without_optional_params(self) -> None:
        """Teszteli a ConfigKeyError létrehozását opcionális paraméterek nélkül."""
        error = ConfigKeyError("Kulcs nem található")
        assert str(error) == "Kulcs nem található"
        assert error.key_path is None
        assert error.available_keys == []
        assert error.error_code == "CONFIG_KEY_ERROR"

    def test_key_error_with_none_available_keys(self) -> None:
        """Teszteli a ConfigKeyError létrehozását None available_keys paraméterrel."""
        error = ConfigKeyError("Kulcs nem található", available_keys=None)
        assert error.available_keys == []


class TestExceptionHierarchy:
    """Kivétel hierarchia tesztjei."""

    def test_exception_inheritance(self) -> None:
        """Teszteli, hogy a kivételek helyesen öröklődnek."""
        assert issubclass(ConfigLoadError, ConfigError)
        assert issubclass(ConfigSaveError, ConfigError)
        assert issubclass(ConfigValidationError, ConfigError)
        assert issubclass(ConfigTypeError, ConfigError)
        assert issubclass(ConfigKeyError, ConfigError)

    def test_exception_is_exception(self) -> None:
        """Teszteli, hogy minden kivétel az Exception leszármazottja."""
        assert issubclass(ConfigError, Exception)
        assert issubclass(ConfigLoadError, Exception)
        assert issubclass(ConfigSaveError, Exception)
        assert issubclass(ConfigValidationError, Exception)
        assert issubclass(ConfigTypeError, Exception)
        assert issubclass(ConfigKeyError, Exception)