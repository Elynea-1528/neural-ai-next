"""Logger __init__.py export tesztjei."""

from unittest.mock import patch

from neural_ai.core.logger import (
    ColoredLogger,
    DefaultLogger,
    LoggerConfigurationError,
    LoggerError,
    LoggerFactory,
    LoggerFactoryInterface,
    LoggerInitializationError,
    LoggerInterface,
    RotatingFileLogger,
    __schema_version__,
    __version__,
)


class TestLoggerInitExports:
    """Logger modul exportjainak tesztelése."""

    def test_version_export(self) -> None:
        """Verziószám exportálásának ellenőrzése."""
        assert isinstance(__version__, str)
        assert __version__ is not None

    def test_schema_version_export(self) -> None:
        """Sémaverzió exportálásának ellenőrzése."""
        assert isinstance(__schema_version__, str)
        assert __schema_version__ is not None

    def test_logger_interface_export(self) -> None:
        """LoggerInterface exportálásának ellenőrzése."""
        assert hasattr(LoggerInterface, "__init__")
        assert hasattr(LoggerInterface, "debug")
        assert hasattr(LoggerInterface, "info")
        assert hasattr(LoggerInterface, "warning")
        assert hasattr(LoggerInterface, "error")
        assert hasattr(LoggerInterface, "critical")
        assert hasattr(LoggerInterface, "set_level")
        assert hasattr(LoggerInterface, "get_level")

    def test_logger_factory_interface_export(self) -> None:
        """LoggerFactoryInterface exportálásának ellenőrzése."""
        assert hasattr(LoggerFactoryInterface, "register_logger")
        assert hasattr(LoggerFactoryInterface, "get_logger")
        assert hasattr(LoggerFactoryInterface, "configure")

    def test_logger_factory_export(self) -> None:
        """LoggerFactory exportálásának ellenőrzése."""
        assert hasattr(LoggerFactory, "register_logger")
        assert hasattr(LoggerFactory, "get_logger")
        assert hasattr(LoggerFactory, "configure")
        assert hasattr(LoggerFactory, "get_registered_types")
        assert hasattr(LoggerFactory, "is_logger_registered")
        assert hasattr(LoggerFactory, "clear_instances")
        assert hasattr(LoggerFactory, "get_schema_version")
        assert hasattr(LoggerFactory, "set_schema_version")

    def test_colored_logger_export(self) -> None:
        """ColoredLogger exportálásának ellenőrzése."""
        assert hasattr(ColoredLogger, "__init__")
        assert hasattr(ColoredLogger, "debug")
        assert hasattr(ColoredLogger, "info")
        assert hasattr(ColoredLogger, "warning")
        assert hasattr(ColoredLogger, "error")
        assert hasattr(ColoredLogger, "critical")
        assert hasattr(ColoredLogger, "set_level")
        assert hasattr(ColoredLogger, "get_level")

    def test_default_logger_export(self) -> None:
        """DefaultLogger exportálásának ellenőrzése."""
        assert hasattr(DefaultLogger, "__init__")
        assert hasattr(DefaultLogger, "debug")
        assert hasattr(DefaultLogger, "info")
        assert hasattr(DefaultLogger, "warning")
        assert hasattr(DefaultLogger, "error")
        assert hasattr(DefaultLogger, "critical")
        assert hasattr(DefaultLogger, "set_level")
        assert hasattr(DefaultLogger, "get_level")

    def test_rotating_file_logger_export(self) -> None:
        """RotatingFileLogger exportálásának ellenőrzése."""
        assert hasattr(RotatingFileLogger, "__init__")
        assert hasattr(RotatingFileLogger, "debug")
        assert hasattr(RotatingFileLogger, "info")
        assert hasattr(RotatingFileLogger, "warning")
        assert hasattr(RotatingFileLogger, "error")
        assert hasattr(RotatingFileLogger, "critical")
        assert hasattr(RotatingFileLogger, "set_level")
        assert hasattr(RotatingFileLogger, "get_level")

    def test_logger_error_export(self) -> None:
        """LoggerError exportálásának ellenőrzése."""
        assert issubclass(LoggerError, Exception)

    def test_logger_configuration_error_export(self) -> None:
        """LoggerConfigurationError exportálásának ellenőrzése."""
        assert issubclass(LoggerConfigurationError, LoggerError)

    def test_logger_initialization_error_export(self) -> None:
        """LoggerInitializationError exportálásának ellenőrzése."""
        assert issubclass(LoggerInitializationError, LoggerError)

    def test_all_exports_in_all_list(self) -> None:
        """Minden export szerepel a __all__ listában."""
        from neural_ai.core.logger import __all__ as logger_all

        expected_exports = [
            "__version__",
            "__schema_version__",
            "LoggerInterface",
            "LoggerFactoryInterface",
            "ColoredLogger",
            "DefaultLogger",
            "LoggerFactory",
            "RotatingFileLogger",
            "LoggerError",
            "LoggerConfigurationError",
            "LoggerInitializationError",
        ]

        for export in expected_exports:
            assert export in logger_all

    def test_import_all_from_logger(self) -> None:
        """Az összes export importálható a __all__ listából."""
        from neural_ai.core.logger import __all__ as logger_all

        # Ellenőrizzük, hogy minden elem importálható
        for export_name in logger_all:
            if not export_name.startswith("__"):
                # Dinamikus importálás
                import importlib

                module = importlib.import_module("neural_ai.core.logger")
                export = getattr(module, export_name)
                assert export is not None

    @patch('importlib.metadata.version')
    def test_version_fallback_on_package_not_found(self, mock_version) -> None:
        """Teszteli a fallback mechanizmust, ha a csomag nincs telepítve."""
        from importlib.metadata import PackageNotFoundError

        mock_version.side_effect = PackageNotFoundError("No package found")

        import sys

        original = sys.modules.get('neural_ai.core.logger')

        try:
            if 'neural_ai.core.logger' in sys.modules:
                del sys.modules['neural_ai.core.logger']

            import neural_ai.core.logger as reloaded_logger

            assert reloaded_logger.__version__ == "1.0.0"
            assert isinstance(reloaded_logger.__version__, str)

        finally:
            if original is not None:
                sys.modules['neural_ai.core.logger'] = original
