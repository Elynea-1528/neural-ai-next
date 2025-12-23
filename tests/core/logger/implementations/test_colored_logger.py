"""ColoredLogger tesztelése."""

import logging
import sys
from io import StringIO

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


class TestColoredLogger:
    """ColoredLogger osztály tesztjei."""

    def test_colored_logger_initialization_default_values(self) -> None:
        """Teszteli a logger alapértelmezett inicializálását."""
        logger = ColoredLogger("test_logger")

        assert logger.logger.name == "test_logger"
        assert logger.logger.level == logging.INFO
        assert len(logger.logger.handlers) == 1
        assert not logger.logger.propagate

    def test_colored_logger_initialization_custom_level(self) -> None:
        """Teszteli a logger inicializálását egyéni log szinttel."""
        logger = ColoredLogger("test_logger", level=logging.DEBUG)

        assert logger.logger.level == logging.DEBUG

    def test_colored_logger_initialization_custom_stream(self) -> None:
        """Teszteli a logger inicializálását egyéni streammel."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        assert logger.logger.handlers[0].stream == stream

    def test_colored_logger_initialization_custom_format(self) -> None:
        """Teszteli a logger inicializálását egyéni formátummal."""
        format_str = "%(levelname)s - %(message)s"
        logger = ColoredLogger("test_logger", format=format_str)

        assert logger.logger.handlers[0].formatter is not None

    def test_colored_logger_removes_existing_handlers(self) -> None:
        """Teszteli, hogy a logger eltávolítja a korábbi handlereket."""
        # Először hozzunk létre egy loggert handlerekkel
        temp_logger = logging.getLogger("test_handler_removal")
        temp_logger.addHandler(logging.StreamHandler(sys.stdout))

        # Most hozzuk létre a ColoredLogger-t
        logger = ColoredLogger("test_handler_removal")

        # Csak egy handler legyen (az új)
        assert len(logger.logger.handlers) == 1

    def test_colored_logger_debug_method(self) -> None:
        """Teszteli a debug metódust."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream, level=logging.DEBUG)

        logger.debug("Test debug message")

        output = stream.getvalue()
        assert "Test debug message" in output

    def test_colored_logger_info_method(self) -> None:
        """Teszteli az info metódust."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        logger.info("Test info message")

        output = stream.getvalue()
        assert "Test info message" in output

    def test_colored_logger_warning_method(self) -> None:
        """Teszteli a warning metódust."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        logger.warning("Test warning message")

        output = stream.getvalue()
        assert "Test warning message" in output

    def test_colored_logger_error_method(self) -> None:
        """Teszteli az error metódust."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        logger.error("Test error message")

        output = stream.getvalue()
        assert "Test error message" in output

    def test_colored_logger_critical_method(self) -> None:
        """Teszteli a critical metódust."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        logger.critical("Test critical message")

        output = stream.getvalue()
        assert "Test critical message" in output

    def test_colored_logger_set_level(self) -> None:
        """Teszteli a log szint beállítását."""
        logger = ColoredLogger("test_logger")

        logger.set_level(logging.DEBUG)

        assert logger.logger.level == logging.DEBUG
        assert logger.logger.handlers[0].level == logging.DEBUG

    def test_colored_logger_get_level(self) -> None:
        """Teszteli a log szint lekérését."""
        logger = ColoredLogger("test_logger", level=logging.WARNING)

        level = logger.get_level()

        assert level == logging.WARNING

    def test_colored_logger_no_propagation(self) -> None:
        """Teszteli, hogy a logger nem propagálja a bejegyzéseket."""
        logger = ColoredLogger("test_logger")

        assert not logger.logger.propagate

    def test_colored_logger_with_extra_kwargs(self) -> None:
        """Teszteli a logger metódusokat extra kwargokkal."""
        stream = StringIO()
        logger = ColoredLogger("test_logger", stream=stream)

        logger.info("Test message", custom_field="custom_value")

        output = stream.getvalue()
        assert "Test message" in output

    def test_colored_logger_handler_count(self) -> None:
        """Teszteli, hogy pontosan egy handler van a loggeren."""
        logger = ColoredLogger("test_logger")

        assert len(logger.logger.handlers) == 1

    def test_colored_logger_handler_type(self) -> None:
        """Teszteli, hogy a handler StreamHandler típusú."""
        logger = ColoredLogger("test_logger")

        assert isinstance(logger.logger.handlers[0], logging.StreamHandler)

    def test_colored_logger_formatter_type(self) -> None:
        """Teszteli, hogy a formatter ColoredFormatter típusú."""
        from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

        logger = ColoredLogger("test_logger")

        assert isinstance(logger.logger.handlers[0].formatter, ColoredFormatter)
