"""Logger factory interfész tesztelése.

Ez a modul tartalmazza a LoggerFactoryInterface interfész
teszteseteit, amelyek ellenőrzik a factory működésének
alapvető szabványait és elvárt viselkedését.
"""

from abc import ABC
from typing import Any
from unittest.mock import Mock

import pytest

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class ConcreteLoggerFactory(LoggerFactoryInterface, ABC):
    """Konkrét logger factory implementáció teszteléshez.

    Ez egy részleges implementáció, amely lehetővé teszi
    az interfész metódusainak tesztelését.
    """

    _logger_types: dict[str, type[LoggerInterface]] = {}
    _instances: dict[str, LoggerInterface] = {}

    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása a factory számára."""
        if not isinstance(logger_type, str) or not logger_type:
            raise ValueError("logger_type must be a non-empty string")
        if not isinstance(logger_class, type):
            raise TypeError("logger_class must be a type")
        if not issubclass(logger_class, LoggerInterface):
            raise TypeError("logger_class must implement LoggerInterface")
        if logger_type in cls._logger_types:
            raise ValueError(f"Logger type '{logger_type}' already registered")
        cls._logger_types[logger_type] = logger_class

    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása vagy visszaadása."""
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if logger_type not in cls._logger_types:
            raise KeyError(f"Logger type '{logger_type}' not registered")

        instance_key = f"{name}_{logger_type}"
        if instance_key not in cls._instances:
            logger_class = cls._logger_types[logger_type]
            cls._instances[instance_key] = logger_class(name=name, **kwargs)

        return cls._instances[instance_key]

    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása."""
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")
        if not config:
            raise ValueError("config cannot be empty")


class TestLoggerFactoryInterface:
    """LoggerFactoryInterface interfész tesztesetei."""

    def setup_method(self) -> None:
        """Teszteset előkészítése."""
        ConcreteLoggerFactory._logger_types.clear()
        ConcreteLoggerFactory._instances.clear()

    def test_register_logger_success(self) -> None:
        """Sikeres logger regisztráció tesztelése."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str):
                self.name = name

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("mock", MockLogger)

        assert "mock" in ConcreteLoggerFactory._logger_types
        assert ConcreteLoggerFactory._logger_types["mock"] is MockLogger

    def test_register_logger_empty_type_raises_value_error(self) -> None:
        """Üres logger típus esetén ValueError-t várunk."""
        mock_logger_class = Mock(spec=LoggerInterface)

        with pytest.raises(ValueError, match="non-empty string"):
            ConcreteLoggerFactory.register_logger("", mock_logger_class)

    def test_register_logger_invalid_class_raises_type_error(self) -> None:
        """Érvénytelen osztály esetén TypeError-t várunk."""
        with pytest.raises(TypeError, match="must be a type"):
            ConcreteLoggerFactory.register_logger("invalid", "not_a_class")  # type: ignore

    def test_register_logger_duplicate_raises_value_error(self) -> None:
        """Duplikált logger típus esetén ValueError-t várunk."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str):
                self.name = name

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("duplicate", MockLogger)

        with pytest.raises(ValueError, match="already registered"):
            ConcreteLoggerFactory.register_logger("duplicate", MockLogger)

    def test_get_logger_success(self) -> None:
        """Sikeres logger lekérés tesztelése."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str):
                self.name = name

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("test", MockLogger)
        logger = ConcreteLoggerFactory.get_logger("test_logger", "test")

        assert isinstance(logger, MockLogger)
        assert logger.name == "test_logger"

    def test_get_logger_caches_instances(self) -> None:
        """Logger példányok gyorsítótárazásának tesztelése."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str):
                self.name = name

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("cache_test", MockLogger)

        logger1 = ConcreteLoggerFactory.get_logger("cached_logger", "cache_test")
        logger2 = ConcreteLoggerFactory.get_logger("cached_logger", "cache_test")

        assert logger1 is logger2

    def test_get_logger_empty_name_raises_value_error(self) -> None:
        """Üres név esetén ValueError-t várunk."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str):
                self.name = name

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("test", MockLogger)

        with pytest.raises(ValueError, match="non-empty string"):
            ConcreteLoggerFactory.get_logger("", "test")

    def test_get_logger_unregistered_type_raises_key_error(self) -> None:
        """Nem regisztrált típus esetén KeyError-t várunk."""
        with pytest.raises(KeyError, match="not registered"):
            ConcreteLoggerFactory.get_logger("test", "unregistered")

    def test_configure_success(self) -> None:
        """Sikeres konfiguráció tesztelése."""
        config: dict[str, Any] = {"log_level": "DEBUG", "handlers": ["console"]}

        # Should not raise
        ConcreteLoggerFactory.configure(config)

    def test_configure_empty_config_raises_value_error(self) -> None:
        """Üres konfiguráció esetén ValueError-t várunk."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ConcreteLoggerFactory.configure({})

    def test_configure_invalid_config_raises_value_error(self) -> None:
        """Érvénytelen konfiguráció esetén ValueError-t várunk."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            ConcreteLoggerFactory.configure("invalid_config")  # type: ignore

    def test_get_logger_with_kwargs(self) -> None:
        """Logger létrehozása további paraméterekkel."""

        class MockLogger(LoggerInterface):
            def __init__(self, name: str, level: str = "INFO", format: str = "text"):
                self.name = name
                self.level = level
                self.format = format

            def debug(self, message: str, **kwargs: Any) -> None:
                pass

            def info(self, message: str, **kwargs: Any) -> None:
                pass

            def warning(self, message: str, **kwargs: Any) -> None:
                pass

            def error(self, message: str, **kwargs: Any) -> None:
                pass

            def critical(self, message: str, **kwargs: Any) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 10

        ConcreteLoggerFactory.register_logger("kwargs_test", MockLogger)
        logger = ConcreteLoggerFactory.get_logger(
            "test_logger", "kwargs_test", level="DEBUG", format="json"
        )

        assert isinstance(logger, MockLogger)
        assert logger.name == "test_logger"
        assert logger.level == "DEBUG"
        assert logger.format == "json"

    def test_interface_has_abstract_methods(self) -> None:
        """Az interfész tartalmazza az összes szükséges absztrakt metódust."""
        assert hasattr(LoggerFactoryInterface, "register_logger")
        assert hasattr(LoggerFactoryInterface, "get_logger")
        assert hasattr(LoggerFactoryInterface, "configure")

        # Ellenőrizzük, hogy valóban absztrakt metódusok
        assert getattr(LoggerFactoryInterface.register_logger, "__isabstractmethod__", False)
        assert getattr(LoggerFactoryInterface.get_logger, "__isabstractmethod__", False)
        assert getattr(LoggerFactoryInterface.configure, "__isabstractmethod__", False)
