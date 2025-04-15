"""Logger interfész tesztek.

Ez a modul tartalmazza a logger interfészek tesztjeit.
"""

import pytest

from neural_ai.core.logger.interfaces import LoggerInterface


class MockLogger(LoggerInterface):
    """Mock logger a LoggerInterface teszteléséhez."""

    def __init__(self):
        """Mock logger inicializálása."""
        self.debug_calls = []
        self.info_calls = []
        self.warning_calls = []
        self.error_calls = []
        self.critical_calls = []

    def debug(self, message: str, **kwargs) -> None:
        """Debug üzenet rögzítése."""
        self.debug_calls.append((message, kwargs))

    def info(self, message: str, **kwargs) -> None:
        """Info üzenet rögzítése."""
        self.info_calls.append((message, kwargs))

    def warning(self, message: str, **kwargs) -> None:
        """Warning üzenet rögzítése."""
        self.warning_calls.append((message, kwargs))

    def error(self, message: str, **kwargs) -> None:
        """Error üzenet rögzítése."""
        self.error_calls.append((message, kwargs))

    def critical(self, message: str, **kwargs) -> None:
        """Critical üzenet rögzítése."""
        self.critical_calls.append((message, kwargs))


class TestLoggerInterface:
    """LoggerInterface tesztek."""

    @pytest.fixture
    def mock_logger(self):
        """Mock logger fixture."""
        return MockLogger()

    def test_debug_logging(self, mock_logger):
        """Debug metódus tesztelése."""
        message = "Debug üzenet"
        extra = {"key": "value"}

        mock_logger.debug(message, **extra)

        assert len(mock_logger.debug_calls) == 1
        assert mock_logger.debug_calls[0] == (message, extra)

    def test_info_logging(self, mock_logger):
        """Info metódus tesztelése."""
        message = "Info üzenet"
        extra = {"key": "value"}

        mock_logger.info(message, **extra)

        assert len(mock_logger.info_calls) == 1
        assert mock_logger.info_calls[0] == (message, extra)

    def test_warning_logging(self, mock_logger):
        """Warning metódus tesztelése."""
        message = "Warning üzenet"
        extra = {"key": "value"}

        mock_logger.warning(message, **extra)

        assert len(mock_logger.warning_calls) == 1
        assert mock_logger.warning_calls[0] == (message, extra)

    def test_error_logging(self, mock_logger):
        """Error metódus tesztelése."""
        message = "Error üzenet"
        extra = {"key": "value"}

        mock_logger.error(message, **extra)

        assert len(mock_logger.error_calls) == 1
        assert mock_logger.error_calls[0] == (message, extra)

    def test_critical_logging(self, mock_logger):
        """Critical metódus tesztelése."""
        message = "Critical üzenet"
        extra = {"key": "value"}

        mock_logger.critical(message, **extra)

        assert len(mock_logger.critical_calls) == 1
        assert mock_logger.critical_calls[0] == (message, extra)
