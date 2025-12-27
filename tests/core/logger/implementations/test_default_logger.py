"""Default logger implementáció tesztei."""
import logging
import pytest
from neural_ai.core.logger.implementations.default_logger import DefaultLogger


class TestDefaultLogger:
    """DefaultLogger osztály tesztei."""

    def test_init_basic(self):
        """Alap logger inicializálás tesztelése."""
        logger = DefaultLogger("test_basic")
        assert isinstance(logger.logger, logging.Logger)
        assert logger.get_level() == logging.INFO

    def test_init_with_custom_level(self):
        """Logger inicializálás egyéni szinttel."""
        logger = DefaultLogger("test_debug", level=logging.DEBUG)
        assert logger.get_level() == logging.DEBUG

    def test_debug_logging(self, capsys):
        """Debug üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_debug_log", level=logging.DEBUG)
        logger.debug("Test debug message", extra_data="debug_value")
        captured = capsys.readouterr()
        assert "Test debug message" in captured.err

    def test_info_logging(self, capsys):
        """Info üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_info_log")
        logger.info("Test info message", user="test_user")
        captured = capsys.readouterr()
        assert "Test info message" in captured.err

    def test_warning_logging(self, capsys):
        """Warning üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_warning_log")
        logger.warning("Test warning message", reason="test_reason")
        captured = capsys.readouterr()
        assert "Test warning message" in captured.err

    def test_error_logging(self, capsys):
        """Error üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_error_log")
        logger.error("Test error message", error_code=500)
        captured = capsys.readouterr()
        assert "Test error message" in captured.err

    def test_critical_logging(self, capsys):
        """Critical üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_critical_log")
        logger.critical("Test critical message", component="test_component")
        captured = capsys.readouterr()
        assert "Test critical message" in captured.err

    def test_set_level(self):
        """Log szint módosításának tesztelése."""
        logger = DefaultLogger("test_set_level")
        assert logger.get_level() == logging.INFO
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        logger.set_level(logging.ERROR)
        assert logger.get_level() == logging.ERROR

    def test_logger_name(self):
        """Logger nevének ellenőrzése."""
        logger_name = "test_unique_name"
        logger = DefaultLogger(logger_name)
        assert logger.logger.name == logger_name

    def test_no_duplicate_handlers(self):
        """Többszöri inicializálás ne okozzon duplikált handlereket."""
        logger_name = "test_no_duplicates"
        logger1 = DefaultLogger(logger_name)
        initial_handler_count = len(logger1.logger.handlers)
        logger2 = DefaultLogger(logger_name)
        assert len(logger2.logger.handlers) == initial_handler_count