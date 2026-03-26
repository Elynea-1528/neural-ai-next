"""Unit tesztek a neural_ai.core.config.exceptions __init__ modulhoz.

Ez a modul teszteli a config exceptions modul publikus API-ját és exportált kivételeit.
"""

import pytest


class TestConfigExceptionsModuleExports:
    """Tesztek a config exceptions modul exportálásához."""

    def test_exceptions_module_exports_config_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigError

        # Then
        assert ConfigError is not None
        assert issubclass(ConfigError, Exception)

    def test_exceptions_module_exports_config_load_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigLoadError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigLoadError

        # Then
        assert ConfigLoadError is not None
        assert issubclass(ConfigLoadError, Exception)

    def test_exceptions_module_exports_config_save_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigSaveError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigSaveError

        # Then
        assert ConfigSaveError is not None
        assert issubclass(ConfigSaveError, Exception)

    def test_exceptions_module_exports_config_validation_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigValidationError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigValidationError

        # Then
        assert ConfigValidationError is not None
        assert issubclass(ConfigValidationError, Exception)

    def test_exceptions_module_exports_config_type_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigTypeError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigTypeError

        # Then
        assert ConfigTypeError is not None
        assert issubclass(ConfigTypeError, Exception)

    def test_exceptions_module_exports_config_key_error(self) -> None:
        """Ellenőrzi, hogy az exceptions modul exportálja a ConfigKeyError-t."""
        # When
        from neural_ai.core.config.exceptions import ConfigKeyError

        # Then
        assert ConfigKeyError is not None
        assert issubclass(ConfigKeyError, Exception)

    def test_exceptions_module_all_exports(self) -> None:
        """Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet."""
        # When
        from neural_ai.core.config.exceptions import __all__

        # Then
        expected_exports = [
            "ConfigError",
            "ConfigLoadError",
            "ConfigSaveError",
            "ConfigValidationError",
            "ConfigTypeError",
            "ConfigKeyError",
        ]
        assert set(__all__) == set(expected_exports)


class TestConfigErrorHierarchy:
    """Tesztek a config kivétel hierarchiához."""

    def test_config_error_is_base_exception(self) -> None:
        """Ellenőrzi, hogy a ConfigError az Exception leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError

        # Then
        assert issubclass(ConfigError, Exception)

    def test_config_load_error_inherits_from_config_error(self) -> None:
        """Ellenőrzi, hogy a ConfigLoadError a ConfigError leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError, ConfigLoadError

        # Then
        assert issubclass(ConfigLoadError, ConfigError)

    def test_config_save_error_inherits_from_config_error(self) -> None:
        """Ellenőrzi, hogy a ConfigSaveError a ConfigError leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError, ConfigSaveError

        # Then
        assert issubclass(ConfigSaveError, ConfigError)

    def test_config_validation_error_inherits_from_config_error(self) -> None:
        """Ellenőrzi, hogy a ConfigValidationError a ConfigError leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError, ConfigValidationError

        # Then
        assert issubclass(ConfigValidationError, ConfigError)

    def test_config_type_error_inherits_from_config_error(self) -> None:
        """Ellenőrzi, hogy a ConfigTypeError a ConfigError leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError, ConfigTypeError

        # Then
        assert issubclass(ConfigTypeError, ConfigError)

    def test_config_key_error_inherits_from_config_error(self) -> None:
        """Ellenőrzi, hogy a ConfigKeyError a ConfigError leszármazottja."""
        # When
        from neural_ai.core.config.exceptions import ConfigError, ConfigKeyError

        # Then
        assert issubclass(ConfigKeyError, ConfigError)


class TestConfigErrorRaising:
    """Tesztek a config kivételek dobásához."""

    def test_config_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigError

        # Then
        with pytest.raises(ConfigError) as exc_info:
            raise ConfigError("Teszt hiba")

        assert "Teszt hiba" in str(exc_info.value)

    def test_config_load_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigLoadError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigLoadError

        # Then
        with pytest.raises(ConfigLoadError) as exc_info:
            raise ConfigLoadError("Betöltési hiba")

        assert "Betöltési hiba" in str(exc_info.value)

    def test_config_save_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigSaveError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigSaveError

        # Then
        with pytest.raises(ConfigSaveError) as exc_info:
            raise ConfigSaveError("Mentési hiba")

        assert "Mentési hiba" in str(exc_info.value)

    def test_config_validation_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigValidationError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigValidationError

        # Then
        with pytest.raises(ConfigValidationError) as exc_info:
            raise ConfigValidationError("Validációs hiba")

        assert "Validációs hiba" in str(exc_info.value)

    def test_config_type_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigTypeError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigTypeError

        # Then
        with pytest.raises(ConfigTypeError) as exc_info:
            raise ConfigTypeError("Típus hiba")

        assert "Típus hiba" in str(exc_info.value)

    def test_config_key_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a ConfigKeyError kivétel dobható."""
        # When
        from neural_ai.core.config.exceptions import ConfigKeyError

        # Then
        with pytest.raises(ConfigKeyError) as exc_info:
            raise ConfigKeyError("Kulcs hiba")

        assert "Kulcs hiba" in str(exc_info.value)


class TestConfigErrorChaining:
    """Tesztek a config kivétel láncoláshoz."""

    def test_config_error_with_chaining(self) -> None:
        """Ellenőrzi a ConfigError exception chaining-et."""
        # When
        from neural_ai.core.config.exceptions import ConfigError

        original_error = ValueError("Eredeti hiba")

        # Then
        with pytest.raises(ConfigError) as exc_info:
            try:
                raise original_error
            except ValueError as e:
                raise ConfigError("Config hiba") from e

        assert exc_info.value.__cause__ is original_error

    def test_config_load_error_with_chaining(self) -> None:
        """Ellenőrzi a ConfigLoadError exception chaining-et."""
        # When
        from neural_ai.core.config.exceptions import ConfigLoadError

        original_error = FileNotFoundError("Fájl nem található")

        # Then
        with pytest.raises(ConfigLoadError) as exc_info:
            try:
                raise original_error
            except FileNotFoundError as e:
                raise ConfigLoadError("Betöltési hiba") from e

        assert exc_info.value.__cause__ is original_error

    def test_config_validation_error_with_chaining(self) -> None:
        """Ellenőrzi a ConfigValidationError exception chaining-et."""
        # When
        from neural_ai.core.config.exceptions import ConfigValidationError

        original_error = ValueError("Érvénytelen érték")

        # Then
        with pytest.raises(ConfigValidationError) as exc_info:
            try:
                raise original_error
            except ValueError as e:
                raise ConfigValidationError("Validációs hiba") from e

        assert exc_info.value.__cause__ is original_error
