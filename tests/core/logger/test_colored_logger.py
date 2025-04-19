"""Színes logger tesztek."""

import logging
from io import StringIO

import pytest

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


@pytest.fixture
def logger_name() -> str:
    """Logger név fixture."""
    return "test_logger"


@pytest.fixture
def output_stream() -> StringIO:
    """Teszt output stream."""
    return StringIO()


class TestColoredLogger:
    """ColoredLogger tesztosztály."""

    def test_initialization(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a logger inicializálását."""
        logger = ColoredLogger(name=logger_name, stream=output_stream)
        assert logger.logger.name == logger_name
        assert isinstance(logger.logger.handlers[0].formatter, ColoredFormatter)

    def test_custom_format(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli egyéni formátum beállítását."""
        custom_format = "%(levelname)s - %(message)s"
        logger = ColoredLogger(name=logger_name, stream=output_stream, format=custom_format)
        formatter = logger.logger.handlers[0].formatter
        assert isinstance(formatter, ColoredFormatter)
        assert formatter._fmt == custom_format

    def test_debug_logging_with_color(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a színes debug logolást."""
        logger = ColoredLogger(
            name=logger_name,
            stream=output_stream,
            level=logging.DEBUG,
            format="%(levelname)s: %(message)s",
        )
        message = "Debug message"
        logger.debug(message)
        assert "DEBUG: Debug message" in output_stream.getvalue()

    def test_info_logging_with_color(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a színes info logolást."""
        logger = ColoredLogger(
            name=logger_name, stream=output_stream, format="%(levelname)s: %(message)s"
        )
        message = "Info message"
        logger.info(message)
        assert "INFO: Info message" in output_stream.getvalue()

    def test_warning_logging_with_color(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a színes warning logolást."""
        logger = ColoredLogger(
            name=logger_name, stream=output_stream, format="%(levelname)s: %(message)s"
        )
        message = "Warning message"
        logger.warning(message)
        assert "WARNING: Warning message" in output_stream.getvalue()

    def test_error_logging_with_color(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a színes error logolást."""
        logger = ColoredLogger(
            name=logger_name, stream=output_stream, format="%(levelname)s: %(message)s"
        )
        message = "Error message"
        logger.error(message)
        assert "ERROR: Error message" in output_stream.getvalue()

    def test_critical_logging_with_color(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli a színes critical logolást."""
        logger = ColoredLogger(
            name=logger_name, stream=output_stream, format="%(levelname)s: %(message)s"
        )
        message = "Critical message"
        logger.critical(message)
        assert "CRITICAL: Critical message" in output_stream.getvalue()

    def test_extra_kwargs_logging(self, logger_name: str, output_stream: StringIO) -> None:
        """Teszteli extra kulcsszavas paraméterek kezelését."""
        logger = ColoredLogger(name=logger_name, stream=output_stream)
        logger.info("Test message", key="value")
        assert "Test message" in output_stream.getvalue()

    def test_log_level_management(self, logger_name: str) -> None:
        """Teszteli a log szint kezelését."""
        logger = ColoredLogger(name=logger_name)

        # Alapértelmezett szint ellenőrzése
        assert logger.get_level() == logging.INFO

        # Szint módosítása
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        # Handler szint ellenőrzése
        assert logger.logger.handlers[0].level == logging.DEBUG
