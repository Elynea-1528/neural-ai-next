"""Logger interfész tesztek."""

import logging
from collections.abc import Iterator
from typing import Any, cast

import pytest

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class MockLogger(LoggerInterface):
    """Mock logger implementáció teszteléshez."""

    def __init__(self, name: str, **kwargs: Any) -> None:
        """Mock logger inicializálása."""
        self.logger = logging.getLogger(name)
        self.msg_history: list[tuple[str, str]] = []

    def debug(self, message: str, **kwargs: Any) -> None:
        """Debug üzenet."""
        self.msg_history.append(("debug", message))

    def info(self, message: str, **kwargs: Any) -> None:
        """Info üzenet."""
        self.msg_history.append(("info", message))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Warning üzenet."""
        self.msg_history.append(("warning", message))

    def error(self, message: str, **kwargs: Any) -> None:
        """Error üzenet."""
        self.msg_history.append(("error", message))

    def critical(self, message: str, **kwargs: Any) -> None:
        """Critical üzenet."""
        self.msg_history.append(("critical", message))

    def get_level(self) -> int:
        """Log szint lekérése."""
        return self.logger.level

    def set_level(self, level: int) -> None:
        """Log szint beállítása."""
        self.logger.setLevel(level)


class TestLoggerInterface:
    """Logger interfész tesztosztály."""

    @pytest.fixture
    def mock_logger(self) -> Iterator[LoggerInterface]:
        """Mock logger fixture."""
        logger = MockLogger("test_logger")
        yield logger

    def test_debug_logging(self, mock_logger: LoggerInterface) -> None:
        """Debug logolás tesztelése."""
        message = "Test debug message"
        mock_logger.debug(message)
        mock = cast(MockLogger, mock_logger)
        assert ("debug", message) in mock.msg_history

    def test_info_logging(self, mock_logger: LoggerInterface) -> None:
        """Info logolás tesztelése."""
        message = "Test info message"
        mock_logger.info(message)
        mock = cast(MockLogger, mock_logger)
        assert ("info", message) in mock.msg_history

    def test_warning_logging(self, mock_logger: LoggerInterface) -> None:
        """Warning logolás tesztelése."""
        message = "Test warning message"
        mock_logger.warning(message)
        mock = cast(MockLogger, mock_logger)
        assert ("warning", message) in mock.msg_history

    def test_error_logging(self, mock_logger: LoggerInterface) -> None:
        """Error logolás tesztelése."""
        message = "Test error message"
        mock_logger.error(message)
        mock = cast(MockLogger, mock_logger)
        assert ("error", message) in mock.msg_history

    def test_critical_logging(self, mock_logger: LoggerInterface) -> None:
        """Critical logolás tesztelése."""
        message = "Test critical message"
        mock_logger.critical(message)
        mock = cast(MockLogger, mock_logger)
        assert ("critical", message) in mock.msg_history
