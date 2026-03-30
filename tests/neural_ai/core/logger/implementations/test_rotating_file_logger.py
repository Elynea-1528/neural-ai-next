"""Unit tesztek a neural_ai.core.logger.implementations.rotating_file_logger modulhoz.

Ez a teszt ellenőrzi a RotatingFileLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Fájlba írás
3. Méret alapú rotáció
4. Idő alapú rotáció
5. LoggerInterface implementáció
"""

import logging
import tempfile
from pathlib import Path

from neural_ai.core.logger.implementations.rotating_file_logger import (
    RotatingFileLogger,
)


def test_rotating_file_logger_initialization() -> None:
    """Teszt: A RotatingFileLogger inicializálható."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = str(Path(tmpdir) / "test.log")

        # Act
        logger = RotatingFileLogger(name="test_logger", log_file=log_file)

        # Assert
        assert logger is not None
        assert logger.logger.name == "test_logger"


def test_rotating_file_logger_default_level() -> None:
    """Teszt: A RotatingFileLogger alapértelmezett log szintje INFO."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = str(Path(tmpdir) / "test.log")

        # Act
        logger = RotatingFileLogger(name="test_logger", log_file=log_file)

        # Assert
        assert logger.logger.level == logging.INFO


def test_rotating_file_logger_custom_level() -> None:
    """Teszt: A RotatingFileLogger egyedi log szinttel inicializálható."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = str(Path(tmpdir) / "test.log")

        # Act
        logger = RotatingFileLogger(
            name="test_logger", log_file=log_file, level=logging.DEBUG
        )

        # Assert
        assert logger.logger.level == logging.DEBUG


def test_rotating_file_logger_writes_to_file() -> None:
    """Teszt: A RotatingFileLogger fájlba ír."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"
        logger = RotatingFileLogger(name="test_logger", log_file=str(log_file))

        # Act
        logger.info("Test info message")

        # Assert
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test info message" in content


def test_rotating_file_logger_size_rotation() -> None:
    """Teszt: A RotatingFileLogger méret alapú rotációt végez."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"
        logger = RotatingFileLogger(
            name="test_logger",
            log_file=str(log_file),
            max_bytes=100,  # Kis méret a gyors rotációhoz
            backup_count=2,
            rotation_type="size",
        )

        # Act - Sok üzenet írása a rotáció kiváltásához
        for i in range(50):
            logger.info(f"Test message {i} with some extra text to fill the file")

        # Assert
        assert log_file.exists()


def test_rotating_file_logger_time_rotation() -> None:
    """Teszt: A RotatingFileLogger idő alapú rotációval inicializálható."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"

        # Act
        logger = RotatingFileLogger(
            name="test_logger",
            log_file=str(log_file),
            rotation_type="time",
            when="D",  # Napi rotáció
            backup_count=7,
        )

        # Assert
        assert logger is not None
        logger.info("Test message")
        assert log_file.exists()


def test_rotating_file_logger_multiple_messages() -> None:
    """Teszt: A RotatingFileLogger több üzenetet tud logolni."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / "test.log"
        logger = RotatingFileLogger(name="test_logger", log_file=str(log_file))

        # Act
        logger.info("Message 1")
        logger.warning("Message 2")
        logger.error("Message 3")

        # Assert
        content = log_file.read_text()
        assert "Message 1" in content
        assert "Message 2" in content
        assert "Message 3" in content
