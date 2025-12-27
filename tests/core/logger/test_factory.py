"""Logger factory tesztek."""
import logging
import pytest
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerFactory:
    """LoggerFactory osztály tesztei."""

    def test_get_logger_default(self):
        """Alapértelmezett logger létrehozásának tesztelése."""
        logger = LoggerFactory.get_logger("test_default")
        assert isinstance(logger, LoggerInterface)
        assert logger.get_level() == 20  # INFO level

    def test_get_logger_colored(self):
        """Színes logger létrehozásának tesztelése."""
        logger = LoggerFactory.get_logger("test_colored", logger_type="colored")
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_rotating_without_file(self):
        """Rotating logger létrehozása fájl nélkül hibát dob."""
        with pytest.raises(ValueError, match="'log_file' paramétert"):
            LoggerFactory.get_logger("test_rotating", logger_type="rotating")

    def test_get_logger_rotating_with_file(self, tmp_path):
        """Rotating logger létrehozása fájllal."""
        log_file = tmp_path / "test.log"
        logger = LoggerFactory.get_logger(
            "test_rotating", logger_type="rotating", log_file=str(log_file)
        )
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_caching(self):
        """Logger példányok gyorsítótárazásának tesztelése."""
        logger1 = LoggerFactory.get_logger("test_cached")
        logger2 = LoggerFactory.get_logger("test_cached")
        assert logger1 is logger2

    def test_register_logger(self):
        """Új logger típus regisztrálásának tesztelése."""

        class CustomLogger(LoggerInterface):
            def __init__(self, name: str, **kwargs):
                self.logger = None

            def debug(self, message: str, **kwargs) -> None:
                pass

            def info(self, message: str, **kwargs) -> None:
                pass

            def warning(self, message: str, **kwargs) -> None:
                pass

            def error(self, message: str, **kwargs) -> None:
                pass

            def critical(self, message: str, **kwargs) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 20

        LoggerFactory.register_logger("custom", CustomLogger)
        logger = LoggerFactory.get_logger("test_custom", logger_type="custom")
        assert isinstance(logger, CustomLogger)

    def test_get_registered_types(self):
        """Regisztrált logger típusok listázásának tesztelése."""
        types = LoggerFactory.get_registered_types()
        assert "default" in types
        assert "colored" in types
        assert "rotating" in types

    def test_is_logger_registered(self):
        """Logger típus regisztráltságának ellenőrzése."""
        assert LoggerFactory.is_logger_registered("default")
        assert not LoggerFactory.is_logger_registered("nonexistent")

    def test_clear_instances(self):
        """Logger példányok törlésének tesztelése."""
        logger = LoggerFactory.get_logger("test_clear")
        LoggerFactory.clear_instances()
        assert "test_clear" not in LoggerFactory._instances

    def test_configure_basic(self):
        """Alap logger konfiguráció tesztelése."""
        config = {
            "default_level": "DEBUG",
            "handlers": {
                "console": {"enabled": True, "level": "DEBUG", "colored": True},
                "file": {
                    "enabled": False,
                    "filename": "logs/test.log",
                    "level": "DEBUG",
                    "json_format": True,
                },
            },
            "loggers": {"neural_ai": {"level": "DEBUG", "propagate": True}},
        }
        LoggerFactory.configure(config)
        logger = LoggerFactory.get_logger("test_configure", level=logging.DEBUG)
        assert logger.get_level() == 10  # DEBUG level

    def test_get_set_schema_version(self):
        """Sémaváltozat lekérdezésének és beállításának tesztelése."""
        original_version = LoggerFactory.get_schema_version()
        LoggerFactory.set_schema_version("2.0.0")
        assert LoggerFactory.get_schema_version() == "2.0.0"
        LoggerFactory.set_schema_version(original_version)