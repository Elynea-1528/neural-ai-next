"""Colored logger implementáció tesztei."""
import logging

import pytest

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


class TestColoredLogger:
    """ColoredLogger osztály tesztei."""

    def test_init_basic(self) -> None:
        """Alap logger inicializálás tesztelése."""
        logger = ColoredLogger("test_basic")
        assert isinstance(logger.logger, logging.Logger)
        assert logger.get_level() == logging.INFO

    def test_init_with_custom_level(self) -> None:
        """Logger inicializálás egyéni szinttel."""
        logger = ColoredLogger("test_debug", level=logging.DEBUG)
        assert logger.get_level() == logging.DEBUG

    def test_debug_logging(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Debug üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_debug_log", level=logging.DEBUG, stream=buffer)
        logger.debug("Test debug message", extra_data="debug_value")
        output = buffer.getvalue()
        assert "Test debug message" in output

    def test_info_logging(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Info üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_info_log", stream=buffer)
        logger.info("Test info message", user="test_user")
        output = buffer.getvalue()
        assert "Test info message" in output

    def test_warning_logging(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Warning üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_warning_log", stream=buffer)
        logger.warning("Test warning message", reason="test_reason")
        output = buffer.getvalue()
        assert "Test warning message" in output

    def test_error_logging(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Error üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_error_log", stream=buffer)
        logger.error("Test error message", error_code=500)
        output = buffer.getvalue()
        assert "Test error message" in output

    def test_critical_logging(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Critical üzenet logolásának tesztelése."""
        import io
        import sys
        buffer = io.StringIO()
        monkeypatch.setattr(sys, "stdout", buffer)
        logger = ColoredLogger("test_critical_log", stream=buffer)
        logger.critical("Test critical message", component="test_component")
        output = buffer.getvalue()
        assert "Test critical message" in output

    def test_set_level(self) -> None:
        """Log szint módosításának tesztelése."""
        logger = ColoredLogger("test_set_level")
        assert logger.get_level() == logging.INFO
        logger.set_level(logging.DEBUG)
        assert logger.get_level() == logging.DEBUG
        logger.set_level(logging.ERROR)
        assert logger.get_level() == logging.ERROR

    def test_logger_name(self) -> None:
        """Logger nevének ellenőrzése."""
        logger_name = "test_unique_name"
        logger = ColoredLogger(logger_name)
        assert logger.logger.name == logger_name

    def test_colored_formatter_present(self) -> None:
        """Színes formázó jelenlétének ellenőrzése."""
        logger = ColoredLogger("test_formatter")
        assert len(logger.logger.handlers) > 0
        formatter = logger.logger.handlers[0].formatter
        assert formatter is not None
        assert "Colored" in type(formatter).__name__

    def test_existing_handlers_removed(self) -> None:
        """Teszteli, hogy a meglévő handlerek eltávolításra kerülnek.
        
        Ez a teszt lefedi a 54-55. sorokat, ahol a meglévő handlerek
        eltávolítása történik, hogy ne legyenek duplikált üzenetek.
        """
        # Először hozzunk létre egy loggert és adjunk hozzá egy handlert
        logger_name = "test_handler_removal"
        temp_logger = logging.getLogger(logger_name)
        
        # Adjunk hozzá egy handler-t
        import io
        buffer = io.StringIO()
        handler = logging.StreamHandler(buffer)
        temp_logger.addHandler(handler)
        temp_logger.propagate = False
        
        # Ellenőrizzük, hogy a handler hozzáadásra került
        assert len(temp_logger.handlers) == 1
        
        # Most hozzuk létre a ColoredLogger-t ugyanazzal a névvel
        # Ez eltávolítania kell a meglévő handlert
        colored_logger = ColoredLogger(logger_name)
        
        # Ellenőrizzük, hogy csak egy handler van (az új)
        assert len(colored_logger.logger.handlers) == 1
        
        # Ellenőrizzük, hogy az új handler ColoredFormatter-t használ
        formatter = colored_logger.logger.handlers[0].formatter
        assert formatter is not None
        assert "Colored" in type(formatter).__name__