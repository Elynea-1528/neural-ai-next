"""LoggerInterface tesztelése."""

from abc import ABC
from collections.abc import Mapping
from typing import Any, AnyStr

import pytest

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class ConcreteLogger(LoggerInterface):
    """Konkrét logger implementáció teszteléshez."""

    def __init__(self, name: str, config: Any = None, **kwargs: Mapping[str, AnyStr]) -> None:
        """Inicializálja a konkrét logger implementációt."""
        self.name = name
        self.config = config
        self.kwargs = kwargs
        self.level = 0
        self.messages: list[tuple[str, str]] = []

    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Debug üzenet naplózása."""
        self.messages.append(("DEBUG", message))

    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Info üzenet naplózása."""
        self.messages.append(("INFO", message))

    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Warning üzenet naplózása."""
        self.messages.append(("WARNING", message))

    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Error üzenet naplózása."""
        self.messages.append(("ERROR", message))

    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        """Critical üzenet naplózása."""
        self.messages.append(("CRITICAL", message))

    def set_level(self, level: int) -> None:
        """Naplózási szint beállítása."""
        self.level = level

    def get_level(self) -> int:
        """Aktuális naplózási szint lekérdezése."""
        return self.level


class TestLoggerInterface:
    """LoggerInterface metódusainak tesztelése."""

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        """Az absztrakt osztály nem példányosítható."""
        with pytest.raises(TypeError):
            LoggerInterface(name="test")  # type: ignore

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Konkrét implementáció példányosítható."""
        logger = ConcreteLogger(name="test_logger")
        assert isinstance(logger, LoggerInterface)
        assert logger.name == "test_logger"

    def test_initialization_with_config(self) -> None:
        """Logger inicializálása konfigurációval."""
        mock_config = {"level": "DEBUG"}
        logger = ConcreteLogger(name="test", config=mock_config)
        assert logger.config == mock_config

    def test_initialization_with_kwargs(self) -> None:
        """Logger inicializálása további paraméterekkel."""
        logger = ConcreteLogger(name="test", file_path="/tmp/log.txt", level="INFO")
        assert "file_path" in logger.kwargs
        assert "level" in logger.kwargs

    def test_debug_method(self) -> None:
        """Debug metódus helyes működése."""
        logger = ConcreteLogger(name="test")
        logger.debug("Debug message", extra="value")
        assert logger.messages[-1] == ("DEBUG", "Debug message")

    def test_info_method(self) -> None:
        """Info metódus helyes működése."""
        logger = ConcreteLogger(name="test")
        logger.info("Info message", exc_info="True")
        assert logger.messages[-1] == ("INFO", "Info message")

    def test_warning_method(self) -> None:
        """Warning metódus helyes működése."""
        logger = ConcreteLogger(name="test")
        logger.warning("Warning message")
        assert logger.messages[-1] == ("WARNING", "Warning message")

    def test_error_method(self) -> None:
        """Error metódus helyes működése."""
        logger = ConcreteLogger(name="test")
        logger.error("Error message", extra="error_data")
        assert logger.messages[-1] == ("ERROR", "Error message")

    def test_critical_method(self) -> None:
        """Critical metódus helyes működése."""
        logger = ConcreteLogger(name="test")
        logger.critical("Critical message")
        assert logger.messages[-1] == ("CRITICAL", "Critical message")

    def test_set_level_method(self) -> None:
        """Naplózási szint beállítása."""
        logger = ConcreteLogger(name="test")
        logger.set_level(20)
        assert logger.get_level() == 20

    def test_get_level_method(self) -> None:
        """Naplózási szint lekérdezése."""
        logger = ConcreteLogger(name="test")
        logger.set_level(30)
        level = logger.get_level()
        assert level == 30

    def test_all_log_levels(self) -> None:
        """Összes naplózási szint tesztelése."""
        logger = ConcreteLogger(name="test")

        logger.debug("Debug")
        logger.info("Info")
        logger.warning("Warning")
        logger.error("Error")
        logger.critical("Critical")

        assert len(logger.messages) == 5
        assert logger.messages[0] == ("DEBUG", "Debug")
        assert logger.messages[1] == ("INFO", "Info")
        assert logger.messages[2] == ("WARNING", "Warning")
        assert logger.messages[3] == ("ERROR", "Error")
        assert logger.messages[4] == ("CRITICAL", "Critical")

    def test_level_change_affects_behavior(self) -> None:
        """Szint változtatásának hatása."""
        logger = ConcreteLogger(name="test")

        logger.set_level(0)
        assert logger.get_level() == 0

        logger.set_level(50)
        assert logger.get_level() == 50

    def test_logger_has_name_attribute(self) -> None:
        """Loggernek van name attribútuma."""
        logger = ConcreteLogger(name="my_logger")
        assert hasattr(logger, "name")
        assert logger.name == "my_logger"

    def test_is_instance_of_abc(self) -> None:
        """A logger implementációja ABC."""
        logger = ConcreteLogger(name="test")
        assert isinstance(logger, ABC)
