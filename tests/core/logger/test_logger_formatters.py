"""Logger formázók tesztjei.

Ez a modul a ColoredFormatter osztály tesztjeit tartalmazza.
"""

import logging

from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter


class TestColoredFormatter:
    """ColoredFormatter osztály tesztjei."""

    def test_format_debug_level(self) -> None:
        """DEBUG szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=logging.DEBUG,
            pathname="",
            lineno=0,
            msg="Test debug message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        assert "\033[94m" in result  # Kék színkód
        assert "Test debug message" in result
        assert "\033[0m" in result  # Reset színkód

    def test_format_info_level(self) -> None:
        """INFO szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test info message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        assert "\033[92m" in result  # Zöld színkód
        assert "Test info message" in result
        assert "\033[0m" in result  # Reset színkód

    def test_format_warning_level(self) -> None:
        """WARNING szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg="Test warning message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        assert "\033[93m" in result  # Sárga színkód
        assert "Test warning message" in result
        assert "\033[0m" in result  # Reset színkód

    def test_format_error_level(self) -> None:
        """ERROR szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        assert "\033[91m" in result  # Piros színkód
        assert "Test error message" in result
        assert "\033[0m" in result  # Reset színkód

    def test_format_critical_level(self) -> None:
        """CRITICAL szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=logging.CRITICAL,
            pathname="",
            lineno=0,
            msg="Test critical message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        assert "\033[97;41m" in result  # Fehér szöveg piros háttéren
        assert "Test critical message" in result
        assert "\033[0m" in result  # Reset színkód

    def test_format_unknown_level(self) -> None:
        """Ismeretlen szintű log formázásának tesztelése."""
        formatter: ColoredFormatter = ColoredFormatter()
        record: logging.LogRecord = logging.LogRecord(
            name="test",
            level=999,  # Ismeretlen szint
            pathname="",
            lineno=0,
            msg="Test unknown message",
            args=(),
            exc_info=None,
        )

        result: str = formatter.format(record)
        # Ismeretlen szint esetén nem szabad színezést alkalmazni
        assert "Test unknown message" in result
        # Nincs színkód a kimenetben (csak a reset lehet)
        assert result.count("\033[") == 0 or "\033[0m" in result

    def test_colors_class_variable(self) -> None:
        """COLORS osztályváltozó ellenőrzése."""
        assert hasattr(ColoredFormatter, "COLORS")
        assert isinstance(ColoredFormatter.COLORS, dict)
        assert logging.DEBUG in ColoredFormatter.COLORS
        assert logging.INFO in ColoredFormatter.COLORS
        assert logging.WARNING in ColoredFormatter.COLORS
        assert logging.ERROR in ColoredFormatter.COLORS
        assert logging.CRITICAL in ColoredFormatter.COLORS

    def test_reset_class_variable(self) -> None:
        """RESET osztályváltozó ellenőrzése."""
        assert hasattr(ColoredFormatter, "RESET")
        assert ColoredFormatter.RESET == "\033[0m"
