"""Rotating file logger implementáció tesztei."""
import logging
import os
import pytest
import tempfile
from pathlib import Path
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger


class TestRotatingFileLogger:
    """RotatingFileLogger osztály tesztei."""

    def test_init_basic(self) -> None:
        """Alap logger inicializálás tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            logger = RotatingFileLogger("test_basic", log_file=str(log_file))
            assert isinstance(logger.logger, logging.Logger)
            assert logger.get_level() == logging.INFO

    def test_init_without_file_raises_error(self) -> None:
        """Logger inicializálás fájl nélkül hibát dob."""
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'log_file'"):
            RotatingFileLogger("test_no_file")

    def test_init_with_custom_level(self) -> None:
        """Logger inicializálás egyéni szinttel."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_debug.log"
            logger = RotatingFileLogger("test_debug", log_file=str(log_file), level=logging.DEBUG)
            assert logger.get_level() == logging.DEBUG

    def test_init_creates_directory(self) -> None:
        """Logger létrehozza a könyvtárat, ha az nem létezik."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "nonexistent_dir"
            log_file = log_dir / "test.log"
            assert not log_dir.exists()
            logger = RotatingFileLogger("test_dir", log_file=str(log_file))
            assert log_dir.exists()
            assert isinstance(logger.logger, logging.Logger)

    def test_debug_logging(self) -> None:
        """Debug üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_debug.log"
            logger = RotatingFileLogger("test_debug_log", log_file=str(log_file), level=logging.DEBUG)
            logger.debug("Test debug message", extra_data="debug_value")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test debug message" in content

    def test_info_logging(self) -> None:
        """Info üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_info.log"
            logger = RotatingFileLogger("test_info_log", log_file=str(log_file))
            logger.info("Test info message", user="test_user")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test info message" in content

    def test_warning_logging(self) -> None:
        """Warning üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_warning.log"
            logger = RotatingFileLogger("test_warning_log", log_file=str(log_file))
            logger.warning("Test warning message", reason="test_reason")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test warning message" in content

    def test_error_logging(self) -> None:
        """Error üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_error.log"
            logger = RotatingFileLogger("test_error_log", log_file=str(log_file))
            logger.error("Test error message", error_code=500)
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test error message" in content

    def test_critical_logging(self) -> None:
        """Critical üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_critical.log"
            logger = RotatingFileLogger("test_critical_log", log_file=str(log_file))
            logger.critical("Test critical message", component="test_component")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test critical message" in content

    def test_set_level(self) -> None:
        """Log szint módosításának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_set_level.log"
            logger = RotatingFileLogger("test_set_level", log_file=str(log_file))
            assert logger.get_level() == logging.INFO
            logger.set_level(logging.DEBUG)
            assert logger.get_level() == logging.DEBUG
            logger.set_level(logging.ERROR)
            assert logger.get_level() == logging.ERROR

    def test_logger_name(self) -> None:
        """Logger nevének ellenőrzése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_name.log"
            logger_name = "test_unique_name"
            logger = RotatingFileLogger(logger_name, log_file=str(log_file))
            assert logger.logger.name == logger_name

    def test_invalid_rotation_type_raises_error(self) -> None:
        """Érvénytelen rotáció típus hibát dob."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_invalid.log"
            with pytest.raises(ValueError, match="Érvénytelen rotation_type"):
                RotatingFileLogger("test_invalid", log_file=str(log_file), rotation_type="invalid")

    def test_clean_old_logs(self) -> None:
        """Régi log fájlok törlésének tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs_to_clean"
            log_dir.mkdir()
            test_file = log_dir / "old.log"
            test_file.write_text("old content")
            assert test_file.exists()
            RotatingFileLogger.clean_old_logs(log_dir)
            assert not log_dir.exists()