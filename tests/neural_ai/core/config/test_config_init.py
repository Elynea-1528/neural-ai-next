"""Unit tesztek a neural_ai.core.config __init__ modulhoz.

# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
# Pytest tmp_path fixture és mock type inference hibák.

Ez a modul teszteli a config modul publikus API-ját és exportált interfészeit.
"""

import pytest


class TestConfigModuleExports:
    """Tesztek a config modul exportálásához."""

    def test_config_module_imports_exceptions(self) -> None:
        """Ellenőrzi, hogy a config modul exportálja a kivétel osztályokat."""
        # When
        from neural_ai.core.config import (
            ConfigError,
            ConfigKeyError,
            ConfigLoadError,
            ConfigSaveError,
            ConfigTypeError,
            ConfigValidationError,
        )

        # Then
        assert ConfigError is not None
        assert ConfigLoadError is not None
        assert ConfigSaveError is not None
        assert ConfigValidationError is not None
        assert ConfigTypeError is not None
        assert ConfigKeyError is not None

    def test_config_module_imports_factory(self) -> None:
        """Ellenőrzi, hogy a config modul exportálja a factory osztályt."""
        # When
        from neural_ai.core.config import ConfigManagerFactory

        # Then
        assert ConfigManagerFactory is not None
        assert hasattr(ConfigManagerFactory, "get_manager")
        assert hasattr(ConfigManagerFactory, "create_manager")

    def test_config_module_imports_interfaces(self) -> None:
        """Ellenőrzi, hogy a config modul exportálja az interfészeket."""
        # When
        from neural_ai.core.config import (
            ConfigManagerFactoryInterface,
            ConfigManagerInterface,
        )

        # Then
        assert ConfigManagerInterface is not None
        assert ConfigManagerFactoryInterface is not None

    def test_config_module_all_exports(self) -> None:
        """Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet."""
        # When
        from neural_ai.core.config import __all__

        # Then
        expected_exports = [
            "ConfigError",
            "ConfigLoadError",
            "ConfigSaveError",
            "ConfigValidationError",
            "ConfigTypeError",
            "ConfigKeyError",
            "ConfigManagerFactory",
            "ConfigManagerInterface",
            "ConfigManagerFactoryInterface",
        ]
        assert set(__all__) == set(expected_exports)


class TestConfigFactoryIntegration:
    """Integrációs tesztek a config factory használatához."""

    def test_factory_creates_yaml_manager(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        """Ellenőrzi, hogy a factory létrehoz egy YAML config manager példányt."""
        # Given
        from neural_ai.core.config import ConfigManagerFactory

        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("test_key: test_value", encoding="utf-8")

        # When
        config = ConfigManagerFactory.get_manager(str(config_file))

        # Then
        assert config is not None
        assert hasattr(config, "get")
        assert config.get("test_key") == "test_value"

    def test_factory_get_manager_method_exists(self) -> None:
        """Ellenőrzi, hogy a factory get_manager metódusa elérhető."""
        # When
        from neural_ai.core.config import ConfigManagerFactory

        # Then
        assert callable(ConfigManagerFactory.get_manager)

    def test_factory_create_manager_method_exists(self) -> None:
        """Ellenőrzi, hogy a factory create_manager metódusa elérhető."""
        # When
        from neural_ai.core.config import ConfigManagerFactory

        # Then
        assert callable(ConfigManagerFactory.create_manager)


class TestConfigExceptionHierarchy:
    """Tesztek a config kivétel hierarchiához."""

    def test_config_error_is_base_exception(self) -> None:
        """Ellenőrzi, hogy a ConfigError az Exception leszármazottja."""
        # When
        from neural_ai.core.config import ConfigError

        # Then
        assert issubclass(ConfigError, Exception)

    def test_specific_errors_inherit_from_config_error(self) -> None:
        """Ellenőrzi, hogy a specifikus hibák a ConfigError leszármazottai."""
        # When
        from neural_ai.core.config import (
            ConfigError,
            ConfigKeyError,
            ConfigLoadError,
            ConfigSaveError,
            ConfigTypeError,
            ConfigValidationError,
        )

        # Then
        assert issubclass(ConfigLoadError, ConfigError)
        assert issubclass(ConfigSaveError, ConfigError)
        assert issubclass(ConfigValidationError, ConfigError)
        assert issubclass(ConfigTypeError, ConfigError)
        assert issubclass(ConfigKeyError, ConfigError)

    def test_config_errors_can_be_raised(self) -> None:
        """Ellenőrzi, hogy a config hibák dobhatók."""
        # When
        from neural_ai.core.config import ConfigError

        # Then
        with pytest.raises(ConfigError) as exc_info:
            raise ConfigError("Teszt hiba")

        assert "Teszt hiba" in str(exc_info.value)
