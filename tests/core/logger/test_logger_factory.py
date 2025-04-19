"""Logger factory tesztek."""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


@pytest.fixture
def logger_name() -> str:
    """Logger név fixture."""
    return "test_logger"


@pytest.fixture
def config() -> Dict[str, Any]:
    """Teszt konfiguráció fixture."""
    return {
        "default_level": "INFO",
        "format": "%(message)s",
        "date_format": "%Y-%m-%d",
        "handlers": {
            "console": {"enabled": True, "level": "INFO"},
            "file": {"enabled": True, "filename": "test.log", "level": "DEBUG"},
        },
    }


class TestLoggerFactory:
    """LoggerFactory tesztosztály."""

    def setup_method(self) -> None:
        """Teszt setup."""
        # Reset singleton state
        LoggerFactory._instances.clear()
        # Reset registered types
        LoggerFactory._logger_types.clear()
        # Register default types
        LoggerFactory._logger_types["default"] = DefaultLogger
        LoggerFactory._logger_types["colored"] = ColoredLogger

    def test_get_logger_returns_logger_interface(self, logger_name: str) -> None:
        """Teszteli, hogy get_logger LoggerInterface-t ad vissza."""
        logger = LoggerFactory.get_logger(logger_name)
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_returns_existing_instance(self, logger_name: str) -> None:
        """Teszteli létező logger példány visszaadását."""
        logger1 = LoggerFactory.get_logger(logger_name)
        logger2 = LoggerFactory.get_logger(logger_name)
        assert logger1 is logger2

    def test_configure_basic_settings(self, config: Dict[str, Any]) -> None:
        """Teszteli az alap konfiguráció beállítását."""
        with patch("logging.basicConfig") as mock_basic_config:
            LoggerFactory.configure(config)
            mock_basic_config.assert_called_once_with(
                level=20,  # INFO
                format="%(message)s",
                datefmt="%Y-%m-%d",
            )

    def test_configure_handlers(self, config: Dict[str, Any]) -> None:
        """Teszteli a handler-ek konfigurálását."""
        with (
            patch("logging.StreamHandler") as mock_stream_handler,
            patch("logging.FileHandler") as mock_file_handler,
            patch("logging.getLogger") as mock_get_logger,
        ):
            # Mock handler példányok
            mock_console = Mock()
            mock_file = Mock()
            mock_stream_handler.return_value = mock_console
            mock_file_handler.return_value = mock_file

            # Mock root logger
            mock_root_logger = Mock()
            mock_get_logger.return_value = mock_root_logger

            LoggerFactory.configure(config)

            # Console handler ellenőrzése
            mock_stream_handler.assert_called_once()
            assert mock_console.setLevel.called
            assert mock_root_logger.addHandler.call_count == 2

            # File handler ellenőrzése
            mock_file_handler.assert_called_once_with("test.log")
            assert mock_file.setLevel.called
            assert mock_root_logger.addHandler.call_count == 2
