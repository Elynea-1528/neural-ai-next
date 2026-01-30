"""Default logger implementáció tesztei."""

import logging
import structlog
import pytest

from neural_ai.core.logger.implementations.default_logger import DefaultLogger


class TestDefaultLogger:
    """DefaultLogger osztály tesztei."""

    def test_init_basic(self) -> None:
        """Alap logger inicializálás tesztelése."""
        logger = DefaultLogger("test_basic")
        assert hasattr(logger.logger, "debug")
        assert logger.get_level() == logging.INFO

    def test_init_with_custom_level(self) -> None:
        """Logger inicializálás egyéni szinttel."""
        logger = DefaultLogger("test_debug", level=logging.DEBUG)
        assert logger.get_level() == logging.DEBUG

    def test_debug_logging(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Debug üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_debug_log", level=logging.DEBUG)
        logger.debug("Test debug message", extra_data="debug_value")
        captured = capsys.readouterr()
        assert "Test debug message" in captured.out

    def test_info_logging(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Info üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_info_log")
        logger.info("Test info message", user="test_user")
        captured = capsys.readouterr()
        assert "Test info message" in captured.out

    def test_warning_logging(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Warning üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_warning_log")
        logger.warning("Test warning message", reason="test_reason")
        captured = capsys.readouterr()
        assert "Test warning message" in captured.out

    def test_error_logging(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Error üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_error_log")
        logger.error("Test error message", error_code=500)
        captured = capsys.readouterr()
        assert "Test error message" in captured.out

    def test_critical_logging(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Critical üzenet logolásának tesztelése."""
        logger = DefaultLogger("test_critical_log")
        logger.critical("Test critical message", component="test_component")
        captured = capsys.readouterr()
        assert "Test critical message" in captured.out

    def test_set_level(self) -> None:
        """Log szint módosításának tesztelése."""
        logger = DefaultLogger("test_set_level")
        assert logger.get_level() == logging.INFO
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        logger.set_level(logging.ERROR)
        assert logger.get_level() == logging.ERROR

    def test_di_dependencies_none(self) -> None:
        """DI függőségek None értékkel történő elfogadásának tesztelése."""
        logger = DefaultLogger("test_di_none", config=None, event_bus=None)
        # Ellenőrizzük, hogy a logger létrejön None értékekkel
        assert logger is not None
