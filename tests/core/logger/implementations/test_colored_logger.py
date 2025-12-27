"""Colored logger implementáció tesztei."""
import logging
import pytest
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


class TestColoredLogger:
    """ColoredLogger osztály tesztei."""

    def test_init_basic(self):
        """Alap logger inicializálás tesztelése."""
        logger = ColoredLogger("test_basic")
        assert isinstance(logger.logger, logging.Logger)
        assert logger.get_level() == logging.INFO

    def test_init_with_custom_level(self):
        """Logger inicializálás egyéni szinttel."""
        logger = ColoredLogger("test_debug", level=logging.DEBUG)
        assert logger.get_level() == logging.DEBUG

    def test_debug_logging(self, monkeypatch):
        """Debug üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_debug_log", level=logging.DEBUG, stream=buffer)
        logger.debug("Test debug message", extra_data="debug_value")
        output = buffer.getvalue()
        assert "Test debug message" in output

    def test_info_logging(self, monkeypatch):
        """Info üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_info_log", stream=buffer)
        logger.info("Test info message", user="test_user")
        output = buffer.getvalue()
        assert "Test info message" in output

    def test_warning_logging(self, monkeypatch):
        """Warning üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_warning_log", stream=buffer)
        logger.warning("Test warning message", reason="test_reason")
        output = buffer.getvalue()
        assert "Test warning message" in output

    def test_error_logging(self, monkeypatch):
        """Error üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_error_log", stream=buffer)
        logger.error("Test error message", error_code=500)
        output = buffer.getvalue()
        assert "Test error message" in output

    def test_critical_logging(self, monkeypatch):
        """Critical üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_critical_log", stream=buffer)
        logger.critical("Test critical message", component="test_component")
        output = buffer.getvalue()
        assert "Test critical message" in output

    def test_set_level(self):
        """Log szint módosításának tesztelése."""
        logger = ColoredLogger("test_set_level")
        assert logger.get_level() == logging.INFO
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        logger.set_level(logging.ERROR)
        assert logger.get_level() == logging.ERROR

    def test_logger_name(self):
        """Logger nevének ellenőrzése."""
        logger_name = "test_unique_name"
        logger = ColoredLogger(logger_name)
        assert logger.logger.name == logger_name

    def test_colored_formatter_present(self):
        """Színes formázó jelenlétének ellenőrzése."""
        logger = ColoredLogger("test_formatter")
        assert len(logger.logger.handlers) > 0
        formatter = logger.logger.handlers[0].formatter
        assert formatter is not None
        assert "Colored" in type(formatter).__name__