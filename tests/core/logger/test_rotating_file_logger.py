"""Rotáló fájl logger tesztek."""

import logging
import shutil
import time
from pathlib import Path
from typing import Generator

import pytest

from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger


@pytest.fixture
def test_dir() -> Generator[Path, None, None]:
    """Teszt könyvtár fixture."""
    test_path = Path("test_logs")
    if not test_path.exists():
        test_path.mkdir()
    yield test_path
    # Cleanup
    if test_path.exists():
        shutil.rmtree(test_path)


class TestRotatingFileLogger:
    """RotatingFileLogger tesztosztály."""

    def test_initialization(self, test_dir: Path) -> None:
        """Teszteli a logger inicializálását."""
        log_file = test_dir / "init_test.log"
        logger = RotatingFileLogger(name="test_init", log_file=str(log_file))
        assert logger.logger.name == "test_init"
        assert logger.get_level() == logging.INFO

    def test_size_based_rotation(self, test_dir: Path) -> None:
        """Teszteli a méret alapú rotációt."""
        log_file = test_dir / "size_test.log"
        max_bytes = 50  # Nagyon kis méret a gyors rotációhoz
        logger = RotatingFileLogger(
            name="size_test",
            log_file=str(log_file),
            max_bytes=max_bytes,
            backup_count=3,
            format="%(message)s",  # Egyszerű formátum a kiszámítható méretért
        )

        # Nagy üzenetek írása a rotáció kiváltásához
        messages = ["x" * max_bytes for _ in range(3)]
        for msg in messages:
            logger.info(msg)
            # Kényszerített flush a fájlba
            for handler in logger.logger.handlers:
                handler.flush()

        # Ellenőrizzük a backup fájlokat
        assert log_file.exists()
        assert (log_file.parent / f"{log_file.name}.1").exists()
        assert (log_file.parent / f"{log_file.name}.2").exists()

    def test_time_based_rotation(self, test_dir: Path) -> None:
        """Teszteli az idő alapú rotációt."""
        log_file = test_dir / "time_test.log"
        logger = RotatingFileLogger(
            name="time_test",
            log_file=str(log_file),
            rotation_type="time",
            when="S",  # Másodpercenkénti rotáció
            backup_count=2,
        )

        logger.info("First message")
        time.sleep(1.1)  # Várunk egy másodpercet
        logger.info("Second message")

        # Gyorsítótár ürítése
        for handler in logger.logger.handlers:
            handler.flush()

        # Ellenőrizzük a fájlokat
        log_files = list(test_dir.glob("time_test.log*"))
        assert len(log_files) > 1

    def test_backup_count_limit(self, test_dir: Path) -> None:
        """Teszteli a backup fájlok számának korlátozását."""
        log_file = test_dir / "backup_test.log"
        backup_count = 2
        logger = RotatingFileLogger(
            name="backup_test",
            log_file=str(log_file),
            max_bytes=50,
            backup_count=backup_count,
            format="%(message)s",
        )

        # Több rotáció kiváltása
        for i in range(5):
            logger.info("x" * 100)
            # Kényszerített flush minden üzenet után
            for handler in logger.logger.handlers:
                handler.flush()

        # Ellenőrizzük a backup fájlok számát
        backup_files = list(test_dir.glob("backup_test.log.*"))
        assert len(backup_files) <= backup_count

    def test_log_levels(self, test_dir: Path) -> None:
        """Teszteli a különböző log szinteket."""
        log_file = test_dir / "levels_test.log"
        logger = RotatingFileLogger(
            name="levels_test",
            log_file=str(log_file),
            level=logging.DEBUG,
        )

        test_messages = {
            "debug": "Debug message",
            "info": "Info message",
            "warning": "Warning message",
            "error": "Error message",
            "critical": "Critical message",
        }

        # Minden szinten logolunk
        logger.debug(test_messages["debug"])
        logger.info(test_messages["info"])
        logger.warning(test_messages["warning"])
        logger.error(test_messages["error"])
        logger.critical(test_messages["critical"])

        # Gyorsítótár ürítése
        for handler in logger.logger.handlers:
            handler.flush()

        # Ellenőrizzük a log fájl tartalmát
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            for message in test_messages.values():
                assert message in content

    def test_invalid_rotation_type(self, test_dir: Path) -> None:
        """Teszteli érvénytelen rotációs típus kezelését."""
        log_file = test_dir / "invalid_test.log"
        with pytest.raises(ValueError, match="Invalid rotation_type"):
            RotatingFileLogger(
                name="invalid_test",
                log_file=str(log_file),
                rotation_type="invalid",
            )

    def test_log_dir_creation(self, test_dir: Path) -> None:
        """Teszteli a log könyvtár automatikus létrehozását."""
        nested_dir = test_dir / "nested" / "path"
        log_file = nested_dir / "nested_test.log"

        logger = RotatingFileLogger(name="nested_test", log_file=str(log_file))
        logger.info("Test message")

        # Gyorsítótár ürítése
        for handler in logger.logger.handlers:
            handler.flush()

        assert log_file.exists()
        assert log_file.parent.exists()

    def test_missing_log_file(self, test_dir: Path) -> None:
        """Teszteli a log_file paraméter hiányának kezelését."""
        with pytest.raises(ValueError, match="log_file parameter is required"):
            RotatingFileLogger(name="test_missing")
