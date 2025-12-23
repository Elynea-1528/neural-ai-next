"""Tesztek a neural_ai.core.logger.__init__ modulhoz.

Ez a modul tartalmazza a logger komponens fő inicializációs moduljának
tesztjeit, amelyek ellenőrzik az exportált osztályok és interfészek
helyes elérhetőségét.
"""

import pytest

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
)


class TestLoggerInit:
    """Tesztosztály a logger __init__ modul ellenőrzésére."""

    def test_logger_interface_import(self) -> None:
        """Teszteli, hogy a LoggerInterface importálható-e."""
        assert LoggerInterface is not None
        assert hasattr(LoggerInterface, "__abstractmethods__")

    def test_logger_factory_interface_import(self) -> None:
        """Teszteli, hogy a LoggerFactoryInterface importálható-e."""
        assert LoggerFactoryInterface is not None
        assert hasattr(LoggerFactoryInterface, "__abstractmethods__")

    def test_default_logger_import(self) -> None:
        """Teszteli, hogy a DefaultLogger importálható-e."""
        assert DefaultLogger is not None
        assert hasattr(DefaultLogger, "__init__")

    def test_colored_logger_import(self) -> None:
        """Teszteli, hogy a ColoredLogger importálható-e."""
        assert ColoredLogger is not None
        assert hasattr(ColoredLogger, "__init__")

    def test_rotating_file_logger_import(self) -> None:
        """Teszteli, hogy a RotatingFileLogger importálható-e."""
        assert RotatingFileLogger is not None
        assert hasattr(RotatingFileLogger, "__init__")

    def test_logger_factory_import(self) -> None:
        """Teszteli, hogy a LoggerFactory importálható-e."""
        assert LoggerFactory is not None
        assert hasattr(LoggerFactory, "__init__")

    def test_logger_error_import(self) -> None:
        """Teszteli, hogy a LoggerError kivétel importálható-e."""
        assert LoggerError is not None
        assert issubclass(LoggerError, Exception)

    def test_logger_configuration_error_import(self) -> None:
        """Teszteli, hogy a LoggerConfigurationError kivétel importálható-e."""
        assert LoggerConfigurationError is not None
        assert issubclass(LoggerConfigurationError, LoggerError)

    def test_logger_initialization_error_import(self) -> None:
        """Teszteli, hogy a LoggerInitializationError kivétel importálható-e."""
        assert LoggerInitializationError is not None
        assert issubclass(LoggerInitializationError, LoggerError)

    def test_all_imports_complete(self) -> None:
        """Teszteli, hogy minden exportált elem importálható-e."""
        # Ellenőrizzük, hogy az __all__ lista minden eleme elérhető-e
        import neural_ai.core.logger as logger_module

        for name in logger_module.__all__:
            assert hasattr(logger_module, name), f"Hiányzó export: {name}"

    def test_type_checking_imports(self) -> None:
        """Teszteli, hogy a TYPE_CHECKING blokkban lévő típusok is elérhetők-e."""
        # Ez a teszt ellenőrzi, hogy a TYPE_CHECKING blokk nem zavarja meg
        # a futási időben történő importálást
        from neural_ai.core.logger.implementations import DefaultLogger as DL
        from neural_ai.core.logger.interfaces import LoggerInterface as LI

        assert DL is DefaultLogger
        assert LI is LoggerInterface

    def test_logger_interface_instantiation_fails(self) -> None:
        """Teszteli, hogy az interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError):
            LoggerInterface()  # type: ignore

    def test_logger_factory_interface_instantiation_fails(self) -> None:
        """Teszteli, hogy a factory interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError):
            LoggerFactoryInterface()  # type: ignore
