"""Logger Factory tesztek - Mirror Test a factory.py-hoz.

Ez a teszt suite kiegészíti a test_logger_factory.py-t
valós config betöltéssel és edge case teszteléssel.
"""

import logging
from pathlib import Path
from typing import Any

import pytest
import yaml

from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.logger.factory import LoggerFactory


class TestLoggerFactoryRealConfig:
    """Valós YAML config tesztelése."""

    def test_configure_with_real_yaml_parsing(self, tmp_path: Path) -> None:
        """Valós YAML fájl betöltése és config alkalmazása."""
        # YAML fájl írása
        config_dir = tmp_path / "configs"
        config_dir.mkdir()

        logging_yaml = config_dir / "logging.yaml"
        logging_content = {
            "default_level": "INFO",
            "handlers": {
                "console": {"enabled": True, "level": "DEBUG", "colored": True},
                "file": {"enabled": False},
            },
            "loggers": {"neural_ai": {"level": "INFO", "propagate": True}},
        }
        logging_yaml.write_text(yaml.dump(logging_content), encoding="utf-8")

        # YAMLConfigManager használata
        config_manager = YAMLConfigManager()
        config_manager.load_directory(str(config_dir))
        logging_config = config_manager.get_section("logging")

        # LoggerFactory.configure() hívás
        LoggerFactory.configure(logging_config)

        # Logger működésének ellenőrzése
        logger = LoggerFactory.get_logger("test_real_config")
        assert logger.get_level() == logging.INFO

        # Ellenőrizzük, hogy a root logger megfelelően be lett-e állítva
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO

        # Ellenőrizzük, hogy van-e console handler
        has_console_handler = any(
            isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
            for h in root_logger.handlers
        )
        assert has_console_handler

    def test_configure_fallback_with_missing_handlers(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Hiányos config esetén fallback console handler + warning."""
        # Config NÉLKÜL 'handlers' kulcs
        incomplete_config: dict[str, Any] = {
            "default_level": "INFO",
            # "handlers": {...} HIÁNYZIK
            "loggers": {},
        }

        # LoggerFactory.configure() hívás
        LoggerFactory.configure(incomplete_config)

        # Warning log ellenőrzése (strukturált!)
        # A caplog elkapja a warningot, amit a fallback logger küld
        assert "Hiányos logger konfiguráció" in caplog.text

        # Ellenőrizzük, hogy a fallback handler beállította a console-t
        root_logger = logging.getLogger()
        has_console_handler = any(
            isinstance(h, logging.StreamHandler) for h in root_logger.handlers
        )
        assert has_console_handler

    def test_configure_fallback_warning_is_structured(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A fallback warning strukturált logolással történik."""
        # Ezt nehéz közvetlenül ellenőrizni a structlog miatt, de
        # megpróbálhatjuk elkapni a logging record-ot és megnézni az attribútumait

        incomplete_config: dict[str, Any] = {"default_level": "INFO", "loggers": {}}

        with caplog.at_level(logging.WARNING):
            LoggerFactory.configure(incomplete_config)

        # Keressük meg a releváns log rekordot
        warning_record = None
        for record in caplog.records:
            if "Hiányos logger konfiguráció" in record.message:
                warning_record = record
                break

        assert warning_record is not None
        # Az 'extra' mezők a record attribútumaiként jelennek meg
        assert hasattr(warning_record, "component")
        assert warning_record.component == "LoggerFactory"
        assert hasattr(warning_record, "issue")
        assert warning_record.issue == "missing_handlers_section"


class TestLoggerFactoryCoverage:
    """100%-os lefedettség biztosítása."""

    def test_all_branches_in_get_logger(self) -> None:
        """get_logger() minden ága le van fedve."""
        # Ez már részben fedett a test_logger_factory.py-ban,
        # de itt biztosíthatjuk a teljes lefedettséget

        # 1. Rotating logger without log_file
        with pytest.raises(ValueError, match="kötelező megadni a 'log_file' paramétert"):
            LoggerFactory.get_logger("bad_rotating", logger_type="rotating")

        # 2. Non-existent type falls back to default
        logger = LoggerFactory.get_logger("fallback_logger", logger_type="non_existent_type")
        # Ellenőrzés, hogy DefaultLogger lett-e
        # (Itt feltételezzük a DefaultLogger implementációt)
        assert logger.__class__.__name__ == "DefaultLogger"

    def test_configure_file_handler_creation(self, tmp_path: Path) -> None:
        """configure() file handler létrehozásának tesztelése."""
        log_file = tmp_path / "test.log"

        config: dict[str, Any] = {
            "default_level": "DEBUG",
            "handlers": {
                "file": {
                    "enabled": True,
                    "filename": str(log_file),
                    "level": "DEBUG",
                    "json_format": True,
                    "rotating": False,
                }
            },
        }

        LoggerFactory.configure(config)
        assert log_file.exists()

    def test_configure_rotating_file_handler(self, tmp_path: Path) -> None:
        """Rotating file handler létrehozásának tesztelése."""
        log_file = tmp_path / "rotating.log"

        config: dict[str, Any] = {
            "default_level": "DEBUG",
            "handlers": {
                "file": {
                    "enabled": True,
                    "filename": str(log_file),
                    "level": "INFO",
                    "rotating": True,
                    "max_bytes": 1024,
                    "backup_count": 3,
                }
            },
        }

        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a root logger-hez hozzáadódott a rotating handler
        root_logger = logging.getLogger()
        rotating_handlers = [
            h for h in root_logger.handlers
            if h.__class__.__name__ == "RotatingFileHandler"
        ]
        assert len(rotating_handlers) > 0

    def test_configure_trace_file_handler(self, tmp_path: Path) -> None:
        """Trace file handler létrehozásának tesztelése."""
        trace_file = tmp_path / "trace.log"

        config: dict[str, Any] = {
            "default_level": "DEBUG",
            "handlers": {
                "trace_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(trace_file),
                    "level": "DEBUG",
                    "encoding": "utf-8",
                    "maxBytes": 2048,
                    "backupCount": 2,
                }
            },
            "loggers": {
                "neural_ai.trace": {
                    "level": "DEBUG",
                    "propagate": False,
                }
            },
        }

        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a trace logger létrejött
        trace_logger = logging.getLogger("neural_ai.trace")
        assert trace_logger.level == logging.DEBUG
        assert not trace_logger.propagate

        # Ellenőrizzük, hogy van handler
        assert len(trace_logger.handlers) > 0

    def test_configure_trace_file_handler_non_rotating(self, tmp_path: Path) -> None:
        """Trace file handler nem-rotating változatának tesztelése."""
        trace_file = tmp_path / "trace_simple.log"

        config: dict[str, Any] = {
            "default_level": "DEBUG",
            "handlers": {
                "trace_file": {
                    "class": "logging.FileHandler",
                    "filename": str(trace_file),
                    "level": "INFO",
                    "encoding": "utf-8",
                }
            },
            "loggers": {
                "neural_ai.trace": {
                    "level": "INFO",
                    "propagate": True,
                }
            },
        }

        LoggerFactory.configure(config)

        # Ellenőrizzük, hogy a trace logger létrejött
        trace_logger = logging.getLogger("neural_ai.trace")
        assert trace_logger.level == logging.INFO
        assert trace_logger.propagate

    def test_schema_version_methods(self) -> None:
        """Schema version getter/setter tesztelése."""
        # Eredeti verzió mentése
        original_version = LoggerFactory.get_schema_version()

        # Új verzió beállítása
        LoggerFactory.set_schema_version("2.0.0")
        assert LoggerFactory.get_schema_version() == "2.0.0"

        # Visszaállítás
        LoggerFactory.set_schema_version(original_version)

    def test_clear_instances(self) -> None:
        """clear_instances() metódus tesztelése."""
        # Logger létrehozása
        logger1 = LoggerFactory.get_logger("test_clear_1")
        _ = LoggerFactory.get_logger("test_clear_2")

        # Cache törlése
        LoggerFactory.clear_instances()

        # Új logger létrehozása ugyanazzal a névvel
        logger3 = LoggerFactory.get_logger("test_clear_1")

        # Az új logger más példány kell legyen
        assert logger1 is not logger3

    def test_get_registered_types(self) -> None:
        """get_registered_types() metódus tesztelése."""
        types = LoggerFactory.get_registered_types()

        assert isinstance(types, list)
        assert "default" in types
        assert "colored" in types
        assert "rotating" in types

    def test_is_logger_registered(self) -> None:
        """is_logger_registered() metódus tesztelése."""
        assert LoggerFactory.is_logger_registered("default") is True
        assert LoggerFactory.is_logger_registered("colored") is True
        assert LoggerFactory.is_logger_registered("rotating") is True
        assert LoggerFactory.is_logger_registered("non_existent") is False
