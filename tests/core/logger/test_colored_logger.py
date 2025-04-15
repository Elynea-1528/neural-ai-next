"""ColoredLogger tesztek.

Ez a modul a ColoredLogger implementáció tesztjeit tartalmazza.
"""

import logging
from io import StringIO
from typing import Iterator

import pytest

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


class TestColoredLogger:
    """ColoredLogger tesztek."""

    @pytest.fixture(autouse=False)  # type: ignore
    def string_io(self) -> Iterator[StringIO]:
        """Létrehoz egy StringIO objektumot a kimenet elfogásához."""
        string_io = StringIO()
        with pytest.MonkeyPatch().context() as monkeypatch:
            monkeypatch.setattr("sys.stdout", string_io)
            yield string_io

    @pytest.fixture(autouse=False)  # type: ignore
    def logger(self) -> ColoredLogger:
        """Létrehoz egy logger objektumot."""
        return ColoredLogger("test_logger")

    def test_initialization(self) -> None:
        """Teszteli a logger inicializálását."""
        logger = ColoredLogger("test_logger")
        assert isinstance(logger._logger, logging.Logger)
        assert logger._logger.name == "test_logger"
        assert len(logger._logger.handlers) > 0
        assert isinstance(logger._logger.handlers[0], logging.StreamHandler)

    def test_custom_format(self) -> None:
        """Teszteli az egyéni formátum beállítását."""
        format_str = "%(levelname)s - %(message)s"
        logger = ColoredLogger("test_format", format_str=format_str)
        handler = logger._logger.handlers[0]
        assert isinstance(handler.formatter, logging.Formatter)
        assert "%(levelname)s - %(message)s" in str(handler.formatter._fmt)

    def test_debug_logging_with_color(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli a debug szintű logolást színkódokkal."""
        message = "Debug message"
        logger.debug(message)
        output = string_io.getvalue()
        assert "\033[94m" in output  # Kék színkód
        assert message in output
        assert "\033[0m" in output  # Reset színkód

    def test_info_logging_with_color(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli az info szintű logolást színkódokkal."""
        message = "Info message"
        logger.info(message)
        output = string_io.getvalue()
        assert "\033[92m" in output  # Zöld színkód
        assert message in output
        assert "\033[0m" in output  # Reset színkód

    def test_warning_logging_with_color(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli a warning szintű logolást színkódokkal."""
        message = "Warning message"
        logger.warning(message)
        output = string_io.getvalue()
        assert "\033[93m" in output  # Sárga színkód
        assert message in output
        assert "\033[0m" in output  # Reset színkód

    def test_error_logging_with_color(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli az error szintű logolást színkódokkal."""
        message = "Error message"
        logger.error(message)
        output = string_io.getvalue()
        assert "\033[91m" in output  # Piros színkód
        assert message in output
        assert "\033[0m" in output  # Reset színkód

    def test_critical_logging_with_color(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli a critical szintű logolást színkódokkal."""
        message = "Critical message"
        logger.critical(message)
        output = string_io.getvalue()
        assert "\033[97;41m" in output  # Fehér szöveg piros háttéren
        assert message in output
        assert "\033[0m" in output  # Reset színkód

    def test_extra_kwargs_logging(self, logger: ColoredLogger, string_io: StringIO) -> None:
        """Teszteli a további kontextus információk logolását."""
        message = "Test message"
        logger.info(message, extra_field="test_value")
        output = string_io.getvalue()
        assert message in output
