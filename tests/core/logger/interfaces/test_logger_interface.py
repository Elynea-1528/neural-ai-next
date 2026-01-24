"""Logger interfész tesztek."""

from collections.abc import Mapping
from typing import Any, AnyStr

import pytest

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerInterface:
    """LoggerInterface osztály tesztei."""

    def test_interface_is_abstract(self) -> None:
        """Interfész absztrakt osztály-e."""
        with pytest.raises(TypeError):
            LoggerInterface("test")  # type: ignore

    def test_interface_has_required_methods(self) -> None:
        """Interfész tartalmazza a szükséges metódusokat."""
        required_methods = [
            "__init__",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
            "set_level",
            "get_level",
        ]
        for method_name in required_methods:
            assert hasattr(LoggerInterface, method_name)
            method = getattr(LoggerInterface, method_name)
            assert callable(method)

    def test_all_abstract_methods_implemented(self) -> None:
        """Összes absztrakt metódus implementálva van-e."""

        class MockLogger(LoggerInterface):
            """Mock logger implementáció a teszteléshez."""

            def __init__(
                self, name: str, config: Any | None = None, **kwargs: Mapping[str, AnyStr]
            ) -> None:
                super().__init__(name, config, **kwargs)
                self.name = name
                self.config = config
                self.kwargs = kwargs
                self.level = 10
                self.messages: list[dict[str, Any]] = []

            def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
                super().debug(message, **kwargs)
                self.messages.append({"level": "debug", "message": message, **kwargs})

            def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
                super().info(message, **kwargs)
                self.messages.append({"level": "info", "message": message, **kwargs})

            def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
                super().warning(message, **kwargs)
                self.messages.append({"level": "warning", "message": message, **kwargs})

            def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
                super().error(message, **kwargs)
                self.messages.append({"level": "error", "message": message, **kwargs})

            def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
                super().critical(message, **kwargs)
                self.messages.append({"level": "critical", "message": message, **kwargs})

            def set_level(self, level: int) -> None:
                super().set_level(level)
                self.level = level

            def get_level(self) -> int:
                super().get_level()
                return self.level

        # Teszt: Logger létrehozása és inicializálása
        mock_logger = MockLogger("test_logger")
        assert mock_logger.name == "test_logger"
        assert mock_logger.level == 10

        # Teszt: Debug metódus
        mock_logger.debug("debug message")
        assert len(mock_logger.messages) == 1
        assert mock_logger.messages[0]["level"] == "debug"
        assert mock_logger.messages[0]["message"] == "debug message"

        # Teszt: Info metódus
        mock_logger.info("info message")
        assert len(mock_logger.messages) == 2
        assert mock_logger.messages[1]["level"] == "info"

        # Teszt: Warning metódus
        mock_logger.warning("warning message")
        assert len(mock_logger.messages) == 3
        assert mock_logger.messages[2]["level"] == "warning"

        # Teszt: Error metódus
        mock_logger.error("error message")
        assert len(mock_logger.messages) == 4
        assert mock_logger.messages[3]["level"] == "error"

        # Teszt: Critical metódus
        mock_logger.critical("critical message")
        assert len(mock_logger.messages) == 5
        assert mock_logger.messages[4]["level"] == "critical"

        # Teszt: set_level metódus
        mock_logger.set_level(20)
        assert mock_logger.level == 20

        # Teszt: get_level metódus
        level = mock_logger.get_level()
        assert level == 20

        # Teszt: Összes metódus meghívva lett
        assert len(mock_logger.messages) == 5
