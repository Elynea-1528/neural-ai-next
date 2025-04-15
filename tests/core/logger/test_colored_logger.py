"""ColoredLogger tesztek.

Ez a modul a ColoredLogger implementáció tesztjeit tartalmazza.
"""

import logging
from io import StringIO

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


class TestColoredLogger:
    """ColoredLogger tesztek."""

    def test_initialization(self) -> None:
        """Teszteli a logger inicializálását."""
        logger = ColoredLogger("test_logger")
        # pylint: disable=protected-access
        assert isinstance(logger._logger, logging.Logger)
        assert logger._logger.name == "test_logger"
        assert len(logger._logger.handlers) > 0
        assert isinstance(logger._logger.handlers[0], logging.StreamHandler)

    def test_custom_format(self) -> None:
        """Teszteli az egyéni formátum beállítását."""
        format_str = "%(levelname)s - %(message)s"
        logger = ColoredLogger("test_format", format_str=format_str)
        # pylint: disable=protected-access
        handler = logger._logger.handlers[0]
        assert isinstance(handler.formatter, logging.Formatter)
        assert "%(levelname)s - %(message)s" in str(handler.formatter._fmt)

    def test_debug_logging_with_color(self) -> None:
        """Teszteli a debug szintű logolást színkódokkal."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Debug message"
        logger.debug(message)
        result = output.getvalue()
        assert "\033[94m" in result  # Kék színkód
        assert message in result
        assert "\033[0m" in result  # Reset színkód

    def test_info_logging_with_color(self) -> None:
        """Teszteli az info szintű logolást színkódokkal."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Info message"
        logger.info(message)
        result = output.getvalue()
        assert "\033[92m" in result  # Zöld színkód
        assert message in result
        assert "\033[0m" in result  # Reset színkód

    def test_warning_logging_with_color(self) -> None:
        """Teszteli a warning szintű logolást színkódokkal."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Warning message"
        logger.warning(message)
        result = output.getvalue()
        assert "\033[93m" in result  # Sárga színkód
        assert message in result
        assert "\033[0m" in result  # Reset színkód

    def test_error_logging_with_color(self) -> None:
        """Teszteli az error szintű logolást színkódokkal."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Error message"
        logger.error(message)
        result = output.getvalue()
        assert "\033[91m" in result  # Piros színkód
        assert message in result
        assert "\033[0m" in result  # Reset színkód

    def test_critical_logging_with_color(self) -> None:
        """Teszteli a critical szintű logolást színkódokkal."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Critical message"
        logger.critical(message)
        result = output.getvalue()
        assert "\033[97;41m" in result  # Fehér szöveg piros háttéren
        assert message in result
        assert "\033[0m" in result  # Reset színkód

    def test_extra_kwargs_logging(self) -> None:
        """Teszteli a további kontextus információk logolását."""
        output = StringIO()
        logger = ColoredLogger("test_color", stream=output)
        message = "Test message"
        logger.info(message, extra_field="test_value")
        result = output.getvalue()
        assert message in result
