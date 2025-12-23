"""Logger komponens kivételeinek tesztjei.

Ez a modul tartalmazza a logger komponens kivételeinek teszteseteit.
"""

import pytest

from neural_ai.core.logger.exceptions import (
    LoggerConfigurationError,
    LoggerError,
    LoggerInitializationError,
)


class TestLoggerError:
    """LoggerError kivétel tesztjei."""

    def test_raise_logger_error(self) -> None:
        """Teszteli a LoggerError kivétel dobását."""
        with pytest.raises(LoggerError):
            raise LoggerError("Teszt hibaüzenet")

    def test_logger_error_message(self) -> None:
        """Teszteli a LoggerError hibaüzenetét."""
        test_message = "Teszt hibaüzenet"
        with pytest.raises(LoggerError) as exc_info:
            raise LoggerError(test_message)

        assert str(exc_info.value) == test_message

    def test_logger_error_inheritance(self) -> None:
        """Teszteli, hogy a LoggerError az Exception osztályból származik."""
        assert issubclass(LoggerError, Exception)


class TestLoggerConfigurationError:
    """LoggerConfigurationError kivétel tesztjei."""

    def test_raise_logger_configuration_error(self) -> None:
        """Teszteli a LoggerConfigurationError kivétel dobását."""
        with pytest.raises(LoggerConfigurationError):
            raise LoggerConfigurationError("Konfigurációs hiba")

    def test_logger_configuration_error_message(self) -> None:
        """Teszteli a LoggerConfigurationError hibaüzenetét."""
        test_message = "Érvénytelen konfiguráció"
        with pytest.raises(LoggerConfigurationError) as exc_info:
            raise LoggerConfigurationError(test_message)

        assert str(exc_info.value) == test_message

    def test_logger_configuration_error_inheritance(self) -> None:
        """Teszteli, hogy a LoggerConfigurationError a LoggerError-ből származik."""
        assert issubclass(LoggerConfigurationError, LoggerError)

    def test_logger_configuration_error_is_exception(self) -> None:
        """Teszteli, hogy a LoggerConfigurationError az Exception osztályból származik."""
        assert issubclass(LoggerConfigurationError, Exception)


class TestLoggerInitializationError:
    """LoggerInitializationError kivétel tesztjei."""

    def test_raise_logger_initialization_error(self) -> None:
        """Teszteli a LoggerInitializationError kivétel dobását."""
        with pytest.raises(LoggerInitializationError):
            raise LoggerInitializationError("Inicializálási hiba")

    def test_logger_initialization_error_message(self) -> None:
        """Teszteli a LoggerInitializationError hibaüzenetét."""
        test_message = "Nem sikerült inicializálni a loggert"
        with pytest.raises(LoggerInitializationError) as exc_info:
            raise LoggerInitializationError(test_message)

        assert str(exc_info.value) == test_message

    def test_logger_initialization_error_inheritance(self) -> None:
        """Teszteli, hogy a LoggerInitializationError a LoggerError-ből származik."""
        assert issubclass(LoggerInitializationError, LoggerError)

    def test_logger_initialization_error_is_exception(self) -> None:
        """Teszteli, hogy a LoggerInitializationError az Exception osztályból származik."""
        assert issubclass(LoggerInitializationError, Exception)
