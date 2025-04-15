"""LoggerFactory implementáció tesztek.

Ez a modul tartalmazza a LoggerFactory implementáció tesztjeit.
"""

from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.implementations import DefaultLogger, LoggerFactory


class TestLoggerFactory:
    """LoggerFactory osztály tesztjei."""

    @pytest.fixture
    def logger_name(self):
        """Logger név fixture."""
        return "test_logger"

    @pytest.fixture
    def config(self):
        """Konfiguráció fixture."""
        return {
            "default_level": "INFO",
            "format": "%(message)s",
            "date_format": "%Y-%m-%d",
            "handlers": {
                "console": {"enabled": True, "level": "INFO"},
                "file": {"enabled": True, "level": "DEBUG", "filename": "test.log"},
            },
        }

    def test_get_logger_creates_new_instance(self, logger_name):
        """Teszteli új logger példány létrehozását."""
        logger = LoggerFactory.get_logger(logger_name)
        assert isinstance(logger, DefaultLogger)

    def test_get_logger_returns_existing_instance(self, logger_name):
        """Teszteli létező logger példány visszaadását."""
        logger1 = LoggerFactory.get_logger(logger_name)
        logger2 = LoggerFactory.get_logger(logger_name)
        assert logger1 is logger2

    def test_configure_basic_settings(self, config):
        """Teszteli az alap konfiguráció beállítását."""
        with patch("logging.basicConfig") as mock_basic_config:
            LoggerFactory.configure(config)

            mock_basic_config.assert_called_once_with(
                level=20, format="%(message)s", datefmt="%Y-%m-%d"  # INFO level
            )

    def test_configure_handlers(self, config):
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
            assert mock_stream_handler.called
            mock_console.setLevel.assert_called_once_with(20)  # INFO level
            mock_console.setFormatter.assert_called_once()

            # File handler ellenőrzése
            mock_file_handler.assert_called_once_with(filename="test.log", encoding="utf-8")
            mock_file.setLevel.assert_called_once_with(10)  # DEBUG level
            mock_file.setFormatter.assert_called_once()

            # Handler-ek hozzáadásának ellenőrzése
            assert mock_root_logger.addHandler.call_count == 2
