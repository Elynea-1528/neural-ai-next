"""Tesztek a LoggerFactory osztályhoz."""

import tempfile
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerFactory:
    """LoggerFactory osztály tesztjei."""

    def setup_method(self) -> None:
        """Tesztelés előtti beállítások."""
        # Tiszta gyorsítótár minden teszt előtt
        LoggerFactory._instances.clear()

    def test_register_logger(self) -> None:
        """Teszteli az új logger típus regisztrálását."""
        # Előkészítés
        mock_logger_class = Mock(spec=LoggerInterface)

        # Végrehajtás
        LoggerFactory.register_logger("mock", mock_logger_class)

        # Ellenőrzés
        assert "mock" in LoggerFactory._logger_types
        assert LoggerFactory._logger_types["mock"] is mock_logger_class

    def test_get_logger_default(self) -> None:
        """Teszteli az alapértelmezett logger létrehozását."""
        # Végrehajtás
        logger = LoggerFactory.get_logger("test_logger")

        # Ellenőrzés
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")
        assert "test_logger" in LoggerFactory._instances

    def test_get_logger_cached(self) -> None:
        """Teszteli a gyorsítótárazott logger visszaadását."""
        # Előkészítés
        logger1 = LoggerFactory.get_logger("cached_test")

        # Végrehajtás
        logger2 = LoggerFactory.get_logger("cached_test")

        # Ellenőrzés
        assert logger1 is logger2

    def test_get_logger_with_kwargs(self) -> None:
        """Teszteli a logger létrehozását extra paraméterekkel."""
        # Végrehajtás
        logger = LoggerFactory.get_logger("kwargs_test", custom_param="value")

        # Ellenőrzés
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")

    def test_get_logger_invalid_type_fallback(self) -> None:
        """Teszteli az érvénytelen típus esetén történő visszaesést."""
        # Végrehajtás
        logger = LoggerFactory.get_logger("fallback_test", logger_type="invalid_type")

        # Ellenőrzés
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")
        assert "fallback_test" in LoggerFactory._instances

    def test_get_logger_colored(self) -> None:
        """Teszteli a színes logger létrehozását."""
        # Végrehajtás
        logger = LoggerFactory.get_logger("colored_test", logger_type="colored")

        # Ellenőrzés
        assert isinstance(logger, LoggerInterface)

    def test_get_logger_rotating(self) -> None:
        """Teszteli a rotating file logger létrehozását."""
        # Végrehajtás
        logger = LoggerFactory.get_logger(
            "rotating_test",
            logger_type="rotating",
            log_file="/tmp/rotating_test.log",
            max_bytes=1000000,
            backup_count=5,
        )

        # Ellenőrzés
        assert isinstance(logger, LoggerInterface)

    def test_configure_basic(self) -> None:
        """Teszteli az alap logger konfigurációt."""
        # Előkészítés
        config = {
            "default_level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S",
        }

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés (nincs kivétel)

    def test_configure_with_console_handler(self) -> None:
        """Teszteli a konfigurációt console handlerrel."""
        # Előkészítés
        config = {
            "default_level": "DEBUG",
            "handlers": {"console": {"enabled": True, "level": "INFO"}},
        }

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés (nincs kivétel)

    def test_configure_with_file_handler(self) -> None:
        """Teszteli a konfigurációt file handlerrel."""
        # Előkészítés
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_filename = temp_file.name

        config = {
            "default_level": "DEBUG",
            "handlers": {"file": {"enabled": True, "filename": temp_filename, "level": "DEBUG"}},
        }

        try:
            # Végrehajtás
            LoggerFactory.configure(config)

            # Ellenőrzés (nincs kivétel)
        finally:
            # Tisztítás
            import os

            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_configure_with_both_handlers(self) -> None:
        """Teszteli a konfigurációt mindkét handlerrel."""
        # Előkészítés
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_filename = temp_file.name

        config = {
            "default_level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "handlers": {
                "console": {"enabled": True, "level": "INFO"},
                "file": {"enabled": True, "filename": temp_filename, "level": "DEBUG"},
            },
        }

        try:
            # Végrehajtás
            LoggerFactory.configure(config)

            # Ellenőrzés (nincs kivétel)
        finally:
            # Tisztítás
            import os

            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_configure_file_handler_no_filename(self) -> None:
        """Teszteli a file handler konfigurációt fájlnév nélkül."""
        # Előkészítés
        config = {"handlers": {"file": {"enabled": True, "level": "DEBUG"}}}

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés (nincs kivétel, mert a kód ellenőrzi a fájlnév hiányát)

    def test_configure_disabled_handlers(self) -> None:
        """Teszteli a letiltott handlereket."""
        # Előkészítés
        config = {"handlers": {"console": {"enabled": False}, "file": {"enabled": False}}}

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés (nincs kivétel)

    def test_logger_types_initialization(self) -> None:
        """Teszteli a logger típusok inicializálását."""
        # Ellenőrzés
        assert "default" in LoggerFactory._logger_types
        assert "colored" in LoggerFactory._logger_types
        assert "rotating" in LoggerFactory._logger_types

        # Típus ellenőrzés - csak a colored és rotating implementálják az interfészt
        assert "colored" in LoggerFactory._logger_types
        assert "rotating" in LoggerFactory._logger_types
        assert issubclass(LoggerFactory._logger_types["colored"], LoggerInterface)
        assert issubclass(LoggerFactory._logger_types["rotating"], LoggerInterface)

    def test_instances_cache_management(self) -> None:
        """Teszteli a példányok gyorsítótár kezelését."""
        # Előkészítés
        logger1 = LoggerFactory.get_logger("cache_test_1")
        logger2 = LoggerFactory.get_logger("cache_test_2")

        # Ellenőrzés
        assert len(LoggerFactory._instances) == 2
        assert "cache_test_1" in LoggerFactory._instances
        assert "cache_test_2" in LoggerFactory._instances
        assert LoggerFactory._instances["cache_test_1"] is logger1
        assert LoggerFactory._instances["cache_test_2"] is logger2

    @patch("logging.basicConfig")
    def test_configure_calls_basic_config(self, mock_basic_config: Mock) -> None:
        """Teszteli, hogy a configure meghívja a logging.basicConfig-ot."""
        # Előkészítés
        config = {"default_level": "INFO"}

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés
        mock_basic_config.assert_called_once()

    @patch("logging.getLogger")
    @patch("logging.StreamHandler")
    def test_configure_console_handler_creation(
        self, mock_stream_handler: Mock, mock_get_logger: Mock
    ) -> None:
        """Teszteli a console handler létrehozását."""
        # Előkészítés
        config = {"handlers": {"console": {"enabled": True, "level": "INFO"}}}

        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_handler = Mock()
        mock_stream_handler.return_value = mock_handler

        # Végrehajtás
        LoggerFactory.configure(config)

        # Ellenőrzés
        mock_stream_handler.assert_called_once()
        mock_logger.addHandler.assert_called_once_with(mock_handler)

    def test_configure_invalid_log_level_handled(self) -> None:
        """Teszteli az érvénytelen log szint kezelését."""
        # Előkészítés
        config = {
            "default_level": "INVALID_LEVEL",
            "handlers": {"console": {"enabled": True, "level": "ALSO_INVALID"}},
        }

        # Végrehajtás és ellenőrzés
        # A getattr AttributeError-t dob, ha nem találja a szintet
        # A kódunk most már elkapja és kezeli ezt
        with pytest.raises(AttributeError):
            LoggerFactory.configure(config)

    def test_get_logger_with_special_characters_in_name(self) -> None:
        """Teszteli a logger létrehozását speciális karaktereket tartalmazó névvel."""
        # Végrehajtás
        logger = LoggerFactory.get_logger("test-logger.123")

        # Ellenőrzés
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")
        assert "test-logger.123" in LoggerFactory._instances

    def test_multiple_loggers_different_types(self) -> None:
        """Teszteli a különböző típusú loggerek egyidejű létrehozását."""
        # Végrehajtás
        default_logger = LoggerFactory.get_logger("multi_test_default", logger_type="default")
        colored_logger = LoggerFactory.get_logger("multi_test_colored", logger_type="colored")
        rotating_logger = LoggerFactory.get_logger(
            "multi_test_rotating", logger_type="rotating", log_file="/tmp/multi_test_rotating.log"
        )

        # Ellenőrzés
        assert hasattr(default_logger, "debug")
        assert hasattr(colored_logger, "debug")
        assert hasattr(rotating_logger, "debug")
        assert len(LoggerFactory._instances) == 3

    def test_register_logger_overwrites_existing(self) -> None:
        """Teszteli, hogy a register_logger felülírja a meglévő típust."""
        # Előkészítés
        original_class = LoggerFactory._logger_types["default"]
        new_class = Mock(spec=LoggerInterface)

        # Végrehajtás
        LoggerFactory.register_logger("default", new_class)

        # Ellenőrzés
        assert LoggerFactory._logger_types["default"] is new_class
        assert LoggerFactory._logger_types["default"] is not original_class
