"""RotatingFileLogger tesztek.

Ez a modul a RotatingFileLogger implementáció tesztjeit tartalmazza.
"""

import gzip
import logging
import shutil
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterator

import pytest

from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger


class TestRotatingFileLogger:
    """RotatingFileLogger tesztek."""

    @pytest.fixture(autouse=False)  # type: ignore
    def test_dir(self) -> Iterator[Path]:
        """Létrehoz egy teszt könyvtárat."""
        test_dir = Path("test_logs")
        test_dir.mkdir(exist_ok=True)
        yield test_dir
        shutil.rmtree(test_dir)

    @pytest.fixture(autouse=False)  # type: ignore
    def logger(self, test_dir: Path) -> RotatingFileLogger:
        """Létrehoz egy logger objektumot."""
        log_file = test_dir / "test.log"
        return RotatingFileLogger(
            name="test_logger", filename=str(log_file), max_bytes=1024, backup_count=3  # 1KB
        )

    def test_initialization(self, test_dir: Path) -> None:
        """Teszteli a logger inicializálását."""
        log_file = test_dir / "init_test.log"
        logger = RotatingFileLogger("test_init", str(log_file))

        # pylint: disable=protected-access
        assert isinstance(logger._logger, logging.Logger)
        assert logger._logger.name == "test_init"
        assert log_file.parent.exists()
        assert len(logger._logger.handlers) > 0
        assert isinstance(logger._logger.handlers[0], RotatingFileHandler)

    def test_log_directory_creation(self, test_dir: Path) -> None:
        """Teszteli a log könyvtár automatikus létrehozását."""
        nested_dir = test_dir / "nested" / "logs"
        log_file = nested_dir / "test.log"

        RotatingFileLogger("test_dir", str(log_file))
        assert nested_dir.exists()

    def test_size_based_rotation(self, logger: RotatingFileLogger, test_dir: Path) -> None:
        """Teszteli a méret alapú log rotációt."""
        # Nagy mennyiségű adat írása
        large_data = "x" * 512  # 512 byte
        for i in range(5):  # Több mint 1KB adat
            logger.info(f"{large_data} - {i}")

        log_files = list(test_dir.glob("test.log*"))
        assert len(log_files) > 1  # Eredeti + legalább egy rotált fájl

    def test_time_based_rotation(self, test_dir: Path) -> None:
        """Teszteli az idő alapú log rotációt."""
        log_file = test_dir / "time_test.log"
        logger = RotatingFileLogger(
            name="time_test",
            filename=str(log_file),
            rotation_type="time",
            when="S",  # Másodpercenkénti rotáció a teszthez
            backup_count=2,
        )

        # Logolás különböző időpontokban
        logger.info("First message")
        time.sleep(1.1)  # Várunk egy másodpercet
        logger.info("Second message")

        log_files = list(test_dir.glob("time_test.log*"))
        assert len(log_files) > 1

    def test_backup_count_limit(self, logger: RotatingFileLogger, test_dir: Path) -> None:
        """Teszteli a backup fájlok számának korlátját."""
        # Több rotációt kiváltó mennyiségű adat írása
        large_data = "x" * 512
        for i in range(10):
            logger.info(f"{large_data} - {i}")

        log_files = list(test_dir.glob("test.log*"))
        assert len(log_files) <= 4  # Eredeti + 3 backup

    def test_compression(self, test_dir: Path) -> None:
        """Teszteli a log fájlok tömörítését."""
        # Log fájlok létrehozása
        for i in range(3):
            with open(test_dir / f"test.log.{i}", "w", encoding="utf-8") as f:
                f.write(f"Test log content {i}")

        # Tömörítés
        RotatingFileLogger.compress_old_logs(str(test_dir))

        # Ellenőrzés
        compressed_files = list(test_dir.glob("*.gz"))
        assert len(compressed_files) > 0

        # Tömörített tartalom ellenőrzése
        with gzip.open(compressed_files[0], "rt") as f:
            content = f.read()
            assert "Test log content" in content

    def test_custom_format(self, test_dir: Path) -> None:
        """Teszteli az egyéni formátum beállítását."""
        log_file = test_dir / "format_test.log"
        format_str = "%(levelname)s - %(message)s"
        logger = RotatingFileLogger("format_test", str(log_file), format_str=format_str)

        test_message = "Test message"
        logger.info(test_message)

        with open(log_file, encoding="utf-8") as f:
            content = f.read()
            assert "INFO - Test message" in content

    def test_log_levels(self, logger: RotatingFileLogger, test_dir: Path) -> None:
        """Teszteli a különböző log szinteket."""
        log_file = test_dir / "test.log"

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        with open(log_file, encoding="utf-8") as f:
            content = f.read()
            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content
            assert "Critical message" in content
