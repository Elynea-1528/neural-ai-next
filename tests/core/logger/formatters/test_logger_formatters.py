"""Logger formatter tesztek."""

import logging

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter


class TestColoredFormatter:
    """ColoredFormatter osztály tesztei."""

    def test_format_debug(self) -> None:
        """Debug szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="",
            lineno=0,
            msg="Test debug message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test debug message" in formatted
        assert "\033[94m" in formatted  # Kék színkód
        assert "\033[0m" in formatted  # Reset színkód

    def test_format_info(self) -> None:
        """Info szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test info message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test info message" in formatted
        assert "\033[92m" in formatted  # Zöld színkód
        assert "\033[0m" in formatted  # Reset színkód

    def test_format_warning(self) -> None:
        """Warning szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="Test warning message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test warning message" in formatted
        assert "\033[93m" in formatted  # Sárga színkód
        assert "\033[0m" in formatted  # Reset színkód

    def test_format_error(self) -> None:
        """Error szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Test error message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test error message" in formatted
        assert "\033[91m" in formatted  # Piros színkód
        assert "\033[0m" in formatted  # Reset színkód

    def test_format_critical(self) -> None:
        """Critical szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.CRITICAL,
            pathname="",
            lineno=0,
            msg="Test critical message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test critical message" in formatted
        assert "\033[97;41m" in formatted  # Fehér szöveg piros háttéren
        assert "\033[0m" in formatted  # Reset színkód

    def test_format_unknown_level(self) -> None:
        """Ismeretlen szintű üzenet formázásának tesztelése."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=999,  # Ismeretlen szint
            pathname="",
            lineno=0,
            msg="Test unknown message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "Test unknown message" in formatted
        # Nincs színkód, mert az ismeretlen szint nincs a COLORS szótárban
        assert "\033[94m" not in formatted
        assert "\033[92m" not in formatted
        assert "\033[93m" not in formatted
        assert "\033[91m" not in formatted
        assert "\033[97;41m" not in formatted
