"""DefaultLogger implementáció tesztek.

Ez a modul tartalmazza a DefaultLogger implementáció tesztjeit.
"""

from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.implementations import DefaultLogger


class TestDefaultLogger:
    """DefaultLogger osztály tesztjei."""

    @pytest.fixture
    def logger_name(self):
        """Logger név fixture."""
        return "test_logger"

    @pytest.fixture
    def mock_stdlib_logger(self):
        """Mock stdlib logger fixture."""
        with patch("logging.getLogger") as mock_getLogger:
            mock_logger = Mock()
            mock_getLogger.return_value = mock_logger
            yield mock_logger

    def test_initialization(self, logger_name, mock_stdlib_logger):
        """Teszteli a logger helyes inicializálását."""
        logger = DefaultLogger(logger_name)
        assert logger._logger == mock_stdlib_logger

    def test_debug_logging(self, logger_name, mock_stdlib_logger):
        """Teszteli a debug szintű logolást."""
        logger = DefaultLogger(logger_name)
        message = "Debug üzenet"
        extra = {"key": "value"}

        logger.debug(message, **extra)
        mock_stdlib_logger.debug.assert_called_once_with(message, extra=extra)

    def test_info_logging(self, logger_name, mock_stdlib_logger):
        """Teszteli az info szintű logolást."""
        logger = DefaultLogger(logger_name)
        message = "Info üzenet"
        extra = {"key": "value"}

        logger.info(message, **extra)
        mock_stdlib_logger.info.assert_called_once_with(message, extra=extra)

    def test_warning_logging(self, logger_name, mock_stdlib_logger):
        """Teszteli a warning szintű logolást."""
        logger = DefaultLogger(logger_name)
        message = "Warning üzenet"
        extra = {"key": "value"}

        logger.warning(message, **extra)
        mock_stdlib_logger.warning.assert_called_once_with(message, extra=extra)

    def test_error_logging(self, logger_name, mock_stdlib_logger):
        """Teszteli az error szintű logolást."""
        logger = DefaultLogger(logger_name)
        message = "Error üzenet"
        extra = {"key": "value"}

        logger.error(message, **extra)
        mock_stdlib_logger.error.assert_called_once_with(message, extra=extra)

    def test_critical_logging(self, logger_name, mock_stdlib_logger):
        """Teszteli a critical szintű logolást."""
        logger = DefaultLogger(logger_name)
        message = "Critical üzenet"
        extra = {"key": "value"}

        logger.critical(message, **extra)
        mock_stdlib_logger.critical.assert_called_once_with(message, extra=extra)
