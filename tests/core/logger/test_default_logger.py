"""Alapértelmezett logger tesztek."""

from collections.abc import Iterator
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.implementations.default_logger import DefaultLogger


@pytest.fixture
def logger_name() -> str:
    """Logger név fixture."""
    return "test_logger"


@pytest.fixture
def mock_stdlib_logger(logger_name: str) -> Iterator[Mock]:
    """Mock stdlib logger fixture."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_logger.handlers = []  # üres handler lista inicializálása
        mock_logger.name = logger_name  # név beállítása
        mock_logger.level = 20  # INFO szint
        mock_get_logger.return_value = mock_logger
        yield mock_logger


class TestDefaultLogger:
    """DefaultLogger tesztosztály."""

    def test_initialization(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli a logger inicializálása."""
        DefaultLogger(name=logger_name)  # Logger létrehozás a mock használatához
        assert mock_stdlib_logger.name == logger_name
        assert mock_stdlib_logger.level == 20  # INFO

    def test_debug_logging(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli a debug szintű logolást."""
        logger = DefaultLogger(name=logger_name)
        message = "Debug üzenet"
        extra = {"key": "value"}

        logger.debug(message, **extra)
        mock_stdlib_logger.debug.assert_called_once_with(message, extra=extra)

    def test_info_logging(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli az info szintű logolást."""
        logger = DefaultLogger(name=logger_name)
        message = "Info üzenet"
        extra = {"key": "value"}

        logger.info(message, **extra)
        mock_stdlib_logger.info.assert_called_once_with(message, extra=extra)

    def test_warning_logging(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli a warning szintű logolást."""
        logger = DefaultLogger(name=logger_name)
        message = "Warning üzenet"
        extra = {"key": "value"}

        logger.warning(message, **extra)
        mock_stdlib_logger.warning.assert_called_once_with(message, extra=extra)

    def test_error_logging(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli az error szintű logolást."""
        logger = DefaultLogger(name=logger_name)
        message = "Error üzenet"
        extra = {"key": "value"}

        logger.error(message, **extra)
        mock_stdlib_logger.error.assert_called_once_with(message, extra=extra)

    def test_critical_logging(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli a critical szintű logolást."""
        logger = DefaultLogger(name=logger_name)
        message = "Critical üzenet"
        extra = {"key": "value"}

        logger.critical(message, **extra)
        mock_stdlib_logger.critical.assert_called_once_with(message, extra=extra)

    def test_log_level_management(self, logger_name: str, mock_stdlib_logger: Mock) -> None:
        """Teszteli a log szint kezelését."""
        logger = DefaultLogger(name=logger_name)

        # Alapértelmezett szint ellenőrzése
        mock_stdlib_logger.level = 20  # INFO
        assert logger.get_level() == 20

        # Szint módosítása és ellenőrzése
        logger.set_level(10)  # DEBUG
        mock_stdlib_logger.setLevel.assert_called_with(10)
        mock_stdlib_logger.level = 10  # Mock szintjének frissítése
        assert logger.get_level() == 10
