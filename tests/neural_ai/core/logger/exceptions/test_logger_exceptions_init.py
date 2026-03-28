"""Unit tesztek a neural_ai.core.logger.exceptions.__init__ modulhoz."""

import neural_ai.core.logger.exceptions as exceptions_module
from neural_ai.core.logger.exceptions.logger_error import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)


class TestLoggerExceptionsInit:
    """Tesztek a neural_ai.core.logger.exceptions.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(exceptions_module, "__all__")
        assert isinstance(exceptions_module.__all__, list)

    def test_all_exports_logger_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LoggerError-t."""
        assert "LoggerError" in exceptions_module.__all__

    def test_all_exports_logger_configuration_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LoggerConfigurationError-t."""
        assert "LoggerConfigurationError" in exceptions_module.__all__

    def test_all_exports_logger_initialization_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LoggerInitializationError-t."""
        assert "LoggerInitializationError" in exceptions_module.__all__

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 3 elemet tartalmaz."""
        assert len(exceptions_module.__all__) == 3

    def test_logger_error_importable(self) -> None:
        """Teszteli, hogy a LoggerError importálható."""
        assert hasattr(exceptions_module, "LoggerError")

    def test_logger_configuration_error_importable(self) -> None:
        """Teszteli, hogy a LoggerConfigurationError importálható."""
        assert hasattr(exceptions_module, "LoggerConfigurationError")

    def test_logger_initialization_error_importable(self) -> None:
        """Teszteli, hogy a LoggerInitializationError importálható."""
        assert hasattr(exceptions_module, "LoggerInitializationError")

    def test_logger_error_is_correct_class(self) -> None:
        """Teszteli, hogy a LoggerError a helyes osztály."""
        assert exceptions_module.LoggerError is LoggerError

    def test_logger_configuration_error_is_correct_class(self) -> None:
        """Teszteli, hogy a LoggerConfigurationError a helyes osztály."""
        assert exceptions_module.LoggerConfigurationError is LoggerConfigurationError

    def test_logger_initialization_error_is_correct_class(self) -> None:
        """Teszteli, hogy a LoggerInitializationError a helyes osztály."""
        assert (
            exceptions_module.LoggerInitializationError is LoggerInitializationError
        )

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert exceptions_module.__doc__ is not None
        assert len(exceptions_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert exceptions_module.__doc__ is not None
        assert "Logger" in exceptions_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in exceptions_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in exceptions_module.__all__:
            assert hasattr(exceptions_module, name)

    def test_all_exports_are_exception_classes(self) -> None:
        """Teszteli, hogy az összes export Exception osztály."""
        assert issubclass(exceptions_module.LoggerError, Exception)
        assert issubclass(exceptions_module.LoggerConfigurationError, Exception)
        assert issubclass(exceptions_module.LoggerInitializationError, Exception)
