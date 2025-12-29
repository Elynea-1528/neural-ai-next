"""Rotating file logger implementáció tesztei."""
import logging
import tempfile
from pathlib import Path

import pytest

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
            RotatingFileLogger("test_no_file")  # type: ignore[call-arg]

    def test_init_with_empty_file_raises_error(self) -> None:
        """Logger inicializálás üres fájlnévvel hibát dob.
        
        Ez a teszt lefedi a 60. sort, ahol a ValueError-t dobjuk.
        """
        with pytest.raises(ValueError, match="A 'log_file' paraméter kötelező"):
            RotatingFileLogger("test_empty_file", log_file="")

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
            logger = RotatingFileLogger(
                "test_debug_log", log_file=str(log_file), level=logging.DEBUG
            )
            logger.debug("Test debug message", extra_data="debug_value")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test debug message" in content

    def test_debug_logging_without_kwargs(self) -> None:
        """Debug üzenet logolásának tesztelése kwargs nélkül.
        
        Ez a teszt lefedi a 106. sort.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_debug_no_kwargs.log"
            logger = RotatingFileLogger(
                "test_debug_no_kwargs", log_file=str(log_file), level=logging.DEBUG
            )
            logger.debug("Test debug message without kwargs")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test debug message without kwargs" in content

    def test_info_logging(self) -> None:
        """Info üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_info.log"
            logger = RotatingFileLogger("test_info_log", log_file=str(log_file))
            logger.info("Test info message", user="test_user")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test info message" in content

    def test_info_logging_without_kwargs(self) -> None:
        """Info üzenet logolásának tesztelése kwargs nélkül.
        
        Ez a teszt lefedi a 118. sort.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_info_no_kwargs.log"
            logger = RotatingFileLogger("test_info_no_kwargs", log_file=str(log_file))
            logger.info("Test info message without kwargs")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test info message without kwargs" in content

    def test_warning_logging(self) -> None:
        """Warning üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_warning.log"
            logger = RotatingFileLogger("test_warning_log", log_file=str(log_file))
            logger.warning("Test warning message", reason="test_reason")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test warning message" in content

    def test_warning_logging_without_kwargs(self) -> None:
        """Warning üzenet logolásának tesztelése kwargs nélkül.
        
        Ez a teszt lefedi a 130. sort.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_warning_no_kwargs.log"
            logger = RotatingFileLogger("test_warning_no_kwargs", log_file=str(log_file))
            logger.warning("Test warning message without kwargs")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test warning message without kwargs" in content

    def test_error_logging(self) -> None:
        """Error üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_error.log"
            logger = RotatingFileLogger("test_error_log", log_file=str(log_file))
            logger.error("Test error message", error_code=500)
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test error message" in content

    def test_error_logging_without_kwargs(self) -> None:
        """Error üzenet logolásának tesztelése kwargs nélkül.
        
        Ez a teszt lefedi a 142. sort.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_error_no_kwargs.log"
            logger = RotatingFileLogger("test_error_no_kwargs", log_file=str(log_file))
            logger.error("Test error message without kwargs")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test error message without kwargs" in content

    def test_critical_logging(self) -> None:
        """Critical üzenet logolásának tesztelése."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_critical.log"
            logger = RotatingFileLogger("test_critical_log", log_file=str(log_file))
            logger.critical("Test critical message", component="test_component")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test critical message" in content

    def test_critical_logging_without_kwargs(self) -> None:
        """Critical üzenet logolásának tesztelése kwargs nélkül.
        
        Ez a teszt lefedi a 154. sort.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_critical_no_kwargs.log"
            logger = RotatingFileLogger("test_critical_no_kwargs", log_file=str(log_file))
            logger.critical("Test critical message without kwargs")
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test critical message without kwargs" in content

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
                RotatingFileLogger("test_invalid", log_file=str(log_file), rotation_type="invalid")  # type: ignore[arg-type]

    def test_time_based_rotation(self) -> None:
        """Időalapú rotáció tesztelése.
        
        Ez a teszt lefedi a 75. sort, ahol a TimedRotatingFileHandler-t hozzuk létre.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_time_rotation.log"
            logger = RotatingFileLogger(
                "test_time_rotation",
                log_file=str(log_file),
                rotation_type="time",
                when="H"  # Óránkénti rotáció
            )
            assert isinstance(logger.logger, logging.Logger)
            assert len(logger.logger.handlers) == 1
            # Ellenőrizzük, hogy TimedRotatingFileHandler-t használ
            assert "TimedRotatingFileHandler" in str(type(logger.logger.handlers[0]))

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

    def test_existing_handlers_removed(self) -> None:
        """Teszteli, hogy a meglévő handlerek eltávolításra kerülnek.
        
        Ez a teszt lefedi a 56. sort, ahol a meglévő handlerek
        eltávolítása történik.
        """
        # Először hozzunk létre egy loggert és adjunk hozzá egy handlert
        logger_name = "test_handler_removal_rotating"
        temp_logger = logging.getLogger(logger_name)
        
        # Adjunk hozzá egy handler-t
        import io
        buffer = io.StringIO()
        handler = logging.StreamHandler(buffer)
        temp_logger.addHandler(handler)
        temp_logger.propagate = False
        
        # Ellenőrizzük, hogy a handler hozzáadásra került
        assert len(temp_logger.handlers) == 1
        
        # Most hozzuk létre a RotatingFileLogger-t ugyanazzal a névvel
        # Ez eltávolítania kell a meglévő handlert
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test_handler_removal.log"
            rotating_logger = RotatingFileLogger(logger_name, log_file=str(log_file))
            
            # Ellenőrizzük, hogy csak egy handler van (az új)
            assert len(rotating_logger.logger.handlers) == 1
            
            # Ellenőrizzük, hogy az új handler RotatingFileHandler vagy TimedRotatingFileHandler
            handler_type = type(rotating_logger.logger.handlers[0]).__name__
            assert "RotatingFileHandler" in handler_type or "TimedRotatingFileHandler" in handler_type