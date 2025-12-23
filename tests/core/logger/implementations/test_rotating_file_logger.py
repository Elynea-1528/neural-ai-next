"""RotatingFileLogger tesztelése."""

import logging
import os
import tempfile
from pathlib import Path

import pytest

from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger


class TestRotatingFileLogger:
    """RotatingFileLogger osztály tesztjei."""

    def test_rotating_file_logger_initialization_default_values(self) -> None:
        """Teszteli a logger alapértelmezett inicializálását."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            assert logger.logger.name == "test_logger"
            assert logger.logger.level == logging.INFO
            assert len(logger.logger.handlers) == 1
            assert not logger.logger.propagate
            assert Path(log_file).exists()

    def test_rotating_file_logger_initialization_custom_level(self) -> None:
        """Teszteli a logger inicializálását egyéni log szinttel."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, level=logging.DEBUG)

            assert logger.logger.level == logging.DEBUG

    def test_rotating_file_logger_initialization_custom_format(self) -> None:
        """Teszteli a logger inicializálását egyéni formátummal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            format_str = "%(levelname)s - %(message)s"
            logger = RotatingFileLogger("test_logger", log_file=log_file, format_str=format_str)

            assert logger.logger.handlers[0].formatter is not None

    def test_rotating_file_logger_removes_existing_handlers(self) -> None:
        """Teszteli, hogy a logger eltávolítja a korábbi handlereket."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            # Először hozzunk létre egy loggert handlerekkel
            temp_logger = logging.getLogger("test_handler_removal")
            temp_logger.addHandler(logging.StreamHandler())

            # Most hozzuk létre a RotatingFileLogger-t
            logger = RotatingFileLogger("test_handler_removal", log_file=log_file)

            # Csak egy handler legyen (az új)
            assert len(logger.logger.handlers) == 1

    def test_rotating_file_logger_debug_method(self) -> None:
        """Teszteli a debug metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, level=logging.DEBUG)

            logger.debug("Test debug message")

            # Ellenőrizzük, hogy a log fájl létrejött-e és tartalmazza-e az üzenetet
            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test debug message" in content

    def test_rotating_file_logger_info_method(self) -> None:
        """Teszteli az info metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.info("Test info message")

            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test info message" in content

    def test_rotating_file_logger_warning_method(self) -> None:
        """Teszteli a warning metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.warning("Test warning message")

            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test warning message" in content

    def test_rotating_file_logger_error_method(self) -> None:
        """Teszteli az error metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.error("Test error message")

            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test error message" in content

    def test_rotating_file_logger_critical_method(self) -> None:
        """Teszteli a critical metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.critical("Test critical message")

            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test critical message" in content

    def test_rotating_file_logger_set_level(self) -> None:
        """Teszteli a log szint beállítását."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.set_level(logging.DEBUG)

            assert logger.logger.level == logging.DEBUG

    def test_rotating_file_logger_get_level(self) -> None:
        """Teszteli a log szint lekérését."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, level=logging.WARNING)

            level = logger.get_level()

            assert level == logging.WARNING

    def test_rotating_file_logger_no_propagation(self) -> None:
        """Teszteli, hogy a logger nem propagálja a bejegyzéseket."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            assert not logger.logger.propagate

    def test_rotating_file_logger_with_extra_kwargs(self) -> None:
        """Teszteli a logger metódusokat extra kwargokkal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file)

            logger.info("Test message", custom_field="custom_value")

            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Test message" in content

    def test_rotating_file_logger_size_rotation_handler(self) -> None:
        """Teszteli, hogy a méret alapú rotáció esetén RotatingFileHandler jön létre."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, rotation_type="size")

            assert isinstance(logger.logger.handlers[0], logging.handlers.RotatingFileHandler)

    def test_rotating_file_logger_time_rotation_handler(self) -> None:
        """Teszteli, hogy az idő alapú rotáció esetén TimedRotatingFileHandler jön létre."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, rotation_type="time")

            assert isinstance(logger.logger.handlers[0], logging.handlers.TimedRotatingFileHandler)

    def test_rotating_file_logger_custom_max_bytes(self) -> None:
        """Teszteli a max_bytes paraméter beállítását."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, max_bytes=500000)

            handler = logger.logger.handlers[0]
            assert isinstance(handler, logging.handlers.RotatingFileHandler)
            assert handler.maxBytes == 500000

    def test_rotating_file_logger_custom_backup_count(self) -> None:
        """Teszteli a backup_count paraméter beállítását."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, backup_count=10)

            handler = logger.logger.handlers[0]
            assert isinstance(handler, logging.handlers.RotatingFileHandler)
            assert handler.backupCount == 10

    def test_rotating_file_logger_custom_when_parameter(self) -> None:
        """Teszteli a when paraméter beállítását időalapú rotációnál."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger(
                "test_logger", log_file=log_file, rotation_type="time", when="H"
            )

            handler = logger.logger.handlers[0]
            assert isinstance(handler, logging.handlers.TimedRotatingFileHandler)
            assert handler.when == "H"

    def test_rotating_file_logger_creates_directory(self) -> None:
        """Teszteli, hogy a logger létrehozza a könyvtárat, ha az nem létezik."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "subdir", "nested", "test.log")
            RotatingFileLogger("test_logger", log_file=log_file)

            assert Path(log_file).parent.exists()
            assert Path(log_file).exists()

    def test_rotating_file_logger_invalid_rotation_type_raises_error(self) -> None:
        """Teszteli, hogy érvénytelen rotation_type esetén ValueError-t kapunk."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            with pytest.raises(ValueError, match="rotation_type"):
                RotatingFileLogger("test_logger", log_file=log_file, rotation_type="invalid")  # type: ignore[arg-type]

    def test_rotating_file_logger_missing_log_file_raises_error(self) -> None:
        """Teszteli, hogy log_file nélkül ValueError-t kapunk."""
        with pytest.raises(ValueError, match="log_file"):
            RotatingFileLogger("test_logger", log_file="")

    def test_rotating_file_logger_clean_old_logs(self) -> None:
        """Teszteli a clean_old_logs statikus metódust."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir) / "logs"
            log_dir.mkdir()
            (log_dir / "test.log").write_text("test content")

            assert log_dir.exists()
            RotatingFileLogger.clean_old_logs(log_dir)
            assert not log_dir.exists()

    def test_rotating_file_logger_with_extra_kwargs_detailed(self) -> None:
        """Teszteli a logger metódusokat részletes extra kwargokkal a teljes coverage érdekében."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            logger = RotatingFileLogger("test_logger", log_file=log_file, level=logging.DEBUG)

            # Teszteljük az összes log metódust extra kwargokkal
            logger.debug("Debug message", user_id=123, session_id="abc123")
            logger.info("Info message", duration=0.5, status="success")
            logger.warning("Warning message", retry_count=3, component="auth")
            logger.error("Error message", error_code=500, stack_trace="trace")
            logger.critical("Critical message", component="database", action="rollback")

            # Ellenőrizzük, hogy a log fájl tartalmazza az üzeneteket
            assert Path(log_file).exists()
            with open(log_file) as f:
                content = f.read()
                assert "Debug message" in content
                assert "Info message" in content
                assert "Warning message" in content
                assert "Error message" in content
                assert "Critical message" in content
