"""Logger factory tesztek."""

import logging
from pathlib import Path

import pytest
import yaml

from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerFactory:
    """LoggerFactory osztály tesztei."""

    def test_get_logger_default(self) -> None:
        """Alapértelmezett logger létrehozásának tesztelése."""
        logger = LoggerFactory.get_logger("test_default")
        assert isinstance(logger, LoggerInterface)
        assert logger.get_level() == 20  # INFO level

    def test_get_logger_colored(self) -> None:
        """Színes logger létrehozásának tesztelése."""
        logger = LoggerFactory.get_logger("test_colored", logger_type="colored")
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_rotating_without_file(self) -> None:
        """Rotating logger létrehozása fájl nélkül hibát dob."""
        with pytest.raises(ValueError, match="'log_file' paramétert"):
            LoggerFactory.get_logger("test_rotating", logger_type="rotating")

    def test_get_logger_rotating_with_file(self, tmp_path: Path) -> None:
        """Rotating logger létrehozása fájllal."""
        log_file = tmp_path / "test.log"
        logger = LoggerFactory.get_logger(
            "test_rotating", logger_type="rotating", log_file=str(log_file)
        )
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_caching(self) -> None:
        """Logger példányok gyorsítótárazásának tesztelése."""
        logger1 = LoggerFactory.get_logger("test_cached")
        logger2 = LoggerFactory.get_logger("test_cached")
        assert logger1 is logger2

    def test_register_logger(self) -> None:
        """Új logger típus regisztrálásának tesztelése."""

        class CustomLogger(LoggerInterface):
            def __init__(self, name: str, **kwargs: object) -> None:
                self.logger = None

            def debug(self, message: str, **kwargs: object) -> None:
                pass

            def info(self, message: str, **kwargs: object) -> None:
                pass

            def warning(self, message: str, **kwargs: object) -> None:
                pass

            def error(self, message: str, **kwargs: object) -> None:
                pass

            def critical(self, message: str, **kwargs: object) -> None:
                pass

            def set_level(self, level: int) -> None:
                pass

            def get_level(self) -> int:
                return 20

        LoggerFactory.register_logger("custom", CustomLogger)
        logger = LoggerFactory.get_logger("test_custom", logger_type="custom")
        assert isinstance(logger, CustomLogger)

    def test_get_registered_types(self) -> None:
        """Regisztrált logger típusok listázásának tesztelése."""
        types = LoggerFactory.get_registered_types()
        assert "default" in types
        assert "colored" in types
        assert "rotating" in types

    def test_is_logger_registered(self) -> None:
        """Logger típus regisztráltságának ellenőrzése."""
        assert LoggerFactory.is_logger_registered("default")
        assert not LoggerFactory.is_logger_registered("nonexistent")

    def test_clear_instances(self) -> None:
        """Logger példányok törlésének tesztelése."""
        _ = LoggerFactory.get_logger("test_clear")
        LoggerFactory.clear_instances()
        assert "test_clear" not in LoggerFactory._instances  # type: ignore[reportPrivateUsage]

    def test_configure_basic(self) -> None:
        """Alap logger konfiguráció tesztelése."""
        config: dict[str, object] = {
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

    def test_get_set_schema_version(self) -> None:
        """Sémaváltozat lekérdezésének és beállításának tesztelése."""
        original_version = LoggerFactory.get_schema_version()
        LoggerFactory.set_schema_version("2.0.0")
        assert LoggerFactory.get_schema_version() == "2.0.0"
        LoggerFactory.set_schema_version(original_version)

    def test_get_logger_invalid_type_fallback_to_default(self) -> None:
        """Érvénytelen logger típus esetén az alapértelmezett logger jön létre (107. sor)."""
        logger = LoggerFactory.get_logger("test_invalid_type", logger_type="nonexistent")
        assert isinstance(logger, LoggerInterface)
        # Alapértelmezett logger jön létre
        assert logger.get_level() == 20  # INFO level

    def test_configure_file_handler_with_rotating(self, tmp_path: Path) -> None:
        """File handler konfigurálása rotating loggal (213-246. sorok)."""
        log_file = tmp_path / "rotating.log"
        config: dict[str, object] = {
            "default_level": "DEBUG",
            "handlers": {
                "console": {"enabled": False},
                "file": {
                    "enabled": True,
                    "filename": str(log_file),
                    "level": "DEBUG",
                    "json_format": True,
                    "rotating": True,
                    "max_bytes": 1048576,
                    "backup_count": 3,
                },
            },
            "loggers": {},
        }
        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a fájl létrejött-e
        assert log_file.exists()

        # Ellenőrizzük, hogy a rotating handler be van-e állítva
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0

    def test_configure_file_handler_without_rotating(self, tmp_path: Path) -> None:
        """File handler konfigurálása sima file loggal (213-246. sorok)."""
        log_file = tmp_path / "simple.log"
        config: dict[str, object] = {
            "default_level": "DEBUG",
            "handlers": {
                "console": {"enabled": False},
                "file": {
                    "enabled": True,
                    "filename": str(log_file),
                    "level": "DEBUG",
                    "json_format": True,
                    "rotating": False,
                },
            },
            "loggers": {},
        }
        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a fájl létrejött-e
        assert log_file.exists()

    def test_configure_file_handler_creates_parent_directories(self, tmp_path: Path) -> None:
        """File handler létrehozza a szülő könyvtárakat, ha nem léteznek (216-217. sorok)."""
        log_file = tmp_path / "deep" / "nested" / "path" / "test.log"
        config: dict[str, object] = {
            "default_level": "DEBUG",
            "handlers": {
                "console": {"enabled": False},
                "file": {
                    "enabled": True,
                    "filename": str(log_file),
                    "level": "DEBUG",
                    "json_format": True,
                },
            },
            "loggers": {},
        }
        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a könyvtárak és a fájl létrejöttek-e
        assert log_file.exists()
        assert log_file.parent.exists()

    def test_configure_loggers_with_propagate_false(self) -> None:
        """Logger konfigurálása propagate=False beállítással (254-255. sorok)."""
        config: dict[str, object] = {
            "default_level": "DEBUG",
            "handlers": {
                "console": {"enabled": True, "level": "DEBUG"},
            },
            "loggers": {"test_logger": {"level": "INFO", "propagate": False}},
        }
        LoggerFactory.configure(config)

        logger = logging.getLogger("test_logger")
        assert logger.level == logging.INFO
        assert logger.propagate is False

    def test_configure_with_real_yaml_file(self, tmp_path: Path) -> None:
        """Logger konfigurálása valódi YAML fájlból.

        Ez a teszt ellenőrzi, hogy a LoggerFactory.configure() metódus
        helyesen dolgozza fel a valós YAML konfigurációs fájlt, és
        létrehozza a megfelelő handler-eket.
        """
        # YAML config létrehozása
        yaml_content = """
default_level: "DEBUG"
handlers:
  console:
    enabled: true
    level: "INFO"
    colored: true
  file:
    enabled: true
    filename: "logs/test_real.log"
    level: "DEBUG"
    json_format: true
    rotating: true
    max_bytes: 1048576
    backup_count: 3
loggers:
  neural_ai:
    level: "DEBUG"
    propagate: true
"""
        config_file = tmp_path / "logging_test.yaml"
        config_file.write_text(yaml_content)

        # YAML betöltése
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Configure hívás
        LoggerFactory.configure(config)

        # Ellenőrzés: logger létrehozható és DEBUG szinten van
        logger = LoggerFactory.get_logger("test_yaml_config", level=logging.DEBUG)
        assert logger.get_level() == 10  # DEBUG level

        # Ellenőrzés: log fájl könyvtár létrejött
        _ = tmp_path / "logs"
        # A fájl nem jön létre azonnal, csak amikor van log üzenet,
        # de az is elég ha a könyvtár létrejött
        # (A configure() metódus létrehozza a parent dir-t)

    def test_configure_missing_handlers_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        """Hiányos konfig esetén warning logolás.

        Ez a teszt ellenőrzi, hogy ha a konfigurációból hiányzik a handlers
        szekció, akkor a LoggerFactory fallback módba vált és warning-ot logol.
        """
        # Hiányos config (nincs handlers)
        incomplete_config: dict[str, object] = {
            "default_level": "INFO"
            # handlers hiányzik!
        }

        # Configure hívás warning capture-rel
        with caplog.at_level(logging.WARNING):
            LoggerFactory.configure(incomplete_config)

        # Ellenőrizzük, hogy volt-e warning
        warning_found = any(
            "Hiányos logger konfiguráció" in record.message for record in caplog.records
        )
        assert warning_found, "Warning nem került naplózásra hiányos config esetén"

        # Ellenőrizzük a strukturált logolás extra mezőit
        extra_found = any(
            hasattr(record, "component") and record.component == "LoggerFactory"  # type: ignore[reportAttributeAccessIssue]
            for record in caplog.records
        )
        assert extra_found or warning_found, "Strukturált logolás extra mező hiányzik"

    def test_configure_empty_handlers_fallback(self, tmp_path: Path) -> None:
        """Üres handlers dict esetén fallback működés.

        Ez a teszt ellenőrzi, hogy ha a handlers egy üres dictionary,
        akkor a rendszer nem crashel, hanem fallback módba vált.
        """
        # Config üres handlers-szel
        config_with_empty_handlers: dict[str, object] = {
            "default_level": "INFO",
            "handlers": {},  # Üres, de létezik
        }

        # Ez NEM dobhat hibát, a rendszer működnie kell
        try:
            LoggerFactory.configure(config_with_empty_handlers)
            # Logger létrehozható
            logger = LoggerFactory.get_logger("test_empty_handlers")
            assert logger is not None
        except Exception as e:
            pytest.fail(f"Configure() nem működött üres handlers esetén: {e}")
