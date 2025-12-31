"""Logger error exception tesztek."""

import pytest

from neural_ai.core.logger.exceptions.logger_error import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)


class TestLoggerError:
    """LoggerError osztály tesztei."""

    def test_logger_error_is_exception(self) -> None:
        """LoggerError Exception-ből származik."""
        assert issubclass(LoggerError, Exception)

    def test_logger_error_can_be_raised(self) -> None:
        """LoggerError kiváltható."""
        with pytest.raises(LoggerError):
            raise LoggerError("Test error")

    def test_logger_error_has_message(self) -> None:
        """LoggerError tartalmaz üzenetet."""
        error = LoggerError("Test error message")
        assert str(error) == "Test error message"

    def test_logger_error_without_message(self) -> None:
        """LoggerError hozható létre üzenet nélkül."""
        error = LoggerError()
        assert str(error) == ""


class TestLoggerConfigurationError:
    """LoggerConfigurationError osztály tesztei."""

    def test_logger_configuration_error_is_logger_error(self) -> None:
        """LoggerConfigurationError LoggerError-ből származik."""
        assert issubclass(LoggerConfigurationError, LoggerError)

    def test_logger_configuration_error_can_be_raised(self) -> None:
        """LoggerConfigurationError kiváltható."""
        with pytest.raises(LoggerConfigurationError):
            raise LoggerConfigurationError("Configuration error")

    def test_logger_configuration_error_has_message(self) -> None:
        """LoggerConfigurationError tartalmaz üzenetet."""
        error = LoggerConfigurationError("Invalid configuration")
        assert str(error) == "Invalid configuration"

    def test_logger_configuration_error_without_message(self) -> None:
        """LoggerConfigurationError hozható létre üzenet nélkül."""
        error = LoggerConfigurationError()
        assert str(error) == ""


class TestLoggerInitializationError:
    """LoggerInitializationError osztály tesztei."""

    def test_logger_initialization_error_is_logger_error(self) -> None:
        """LoggerInitializationError LoggerError-ből származik."""
        assert issubclass(LoggerInitializationError, LoggerError)

    def test_logger_initialization_error_can_be_raised(self) -> None:
        """LoggerInitializationError kiváltható."""
        with pytest.raises(LoggerInitializationError):
            raise LoggerInitializationError("Initialization error")

    def test_logger_initialization_error_has_message(self) -> None:
        """LoggerInitializationError tartalmaz üzenetet."""
        error = LoggerInitializationError("Failed to initialize logger")
        assert str(error) == "Failed to initialize logger"

    def test_logger_initialization_error_without_message(self) -> None:
        """LoggerInitializationError hozható létre üzenet nélkül."""
        error = LoggerInitializationError()
        assert str(error) == ""


class TestLoggerErrorHierarchy:
    """Logger error hierarchia tesztek."""

    def test_logger_error_hierarchy(self) -> None:
        """A kivételek helyes hierarchiát alkotnak."""
        assert issubclass(LoggerConfigurationError, LoggerError)
        assert issubclass(LoggerInitializationError, LoggerError)
        assert issubclass(LoggerError, Exception)

    def test_catch_logger_error_catches_subclasses(self) -> None:
        """LoggerError elkapja az összes alosztályt."""

        def raise_config_error() -> None:
            raise LoggerConfigurationError("Config error")

        def raise_init_error() -> None:
            raise LoggerInitializationError("Init error")

        # LoggerConfigurationError elkapása LoggerError-rel
        with pytest.raises(LoggerError):
            raise_config_error()

        # LoggerInitializationError elkapása LoggerError-rel
        with pytest.raises(LoggerError):
            raise_init_error()
