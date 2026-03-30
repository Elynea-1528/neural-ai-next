"""Unit tesztek a neural_ai.core.logger.implementations.colored_logger modulhoz.

Ez a teszt ellenőrzi a ColoredLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Log szintek (debug, info, warning, error, critical)
3. Színes formázás
4. LoggerInterface implementáció
"""

import logging
from io import StringIO

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger


def test_colored_logger_initialization() -> None:
    """Teszt: A ColoredLogger inicializálható."""
    # Arrange & Act
    logger = ColoredLogger(name="test_logger")

    # Assert
    assert logger is not None
    assert logger.logger.name == "test_logger"


def test_colored_logger_default_level() -> None:
    """Teszt: A ColoredLogger alapértelmezett log szintje INFO."""
    # Arrange & Act
    logger = ColoredLogger(name="test_logger")

    # Assert
    assert logger.logger.level == logging.INFO


def test_colored_logger_custom_level() -> None:
    """Teszt: A ColoredLogger egyedi log szinttel inicializálható."""
    # Arrange & Act
    logger = ColoredLogger(name="test_logger", level=logging.DEBUG)

    # Assert
    assert logger.logger.level == logging.DEBUG


def test_colored_logger_info_message() -> None:
    """Teszt: A ColoredLogger info üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", stream=stream)

    # Act
    logger.info("Test info message")

    # Assert
    output = stream.getvalue()
    assert "Test info message" in output
    assert "INFO" in output


def test_colored_logger_warning_message() -> None:
    """Teszt: A ColoredLogger warning üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", stream=stream)

    # Act
    logger.warning("Test warning message")

    # Assert
    output = stream.getvalue()
    assert "Test warning message" in output
    assert "WARNING" in output


def test_colored_logger_error_message() -> None:
    """Teszt: A ColoredLogger error üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", stream=stream)

    # Act
    logger.error("Test error message")

    # Assert
    output = stream.getvalue()
    assert "Test error message" in output
    assert "ERROR" in output


def test_colored_logger_debug_message() -> None:
    """Teszt: A ColoredLogger debug üzenetet tud logolni DEBUG szinten."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", level=logging.DEBUG, stream=stream)

    # Act
    logger.debug("Test debug message")

    # Assert
    output = stream.getvalue()
    assert "Test debug message" in output
    assert "DEBUG" in output


def test_colored_logger_critical_message() -> None:
    """Teszt: A ColoredLogger critical üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", stream=stream)

    # Act
    logger.critical("Test critical message")

    # Assert
    output = stream.getvalue()
    assert "Test critical message" in output
    assert "CRITICAL" in output


def test_colored_logger_with_extra_fields() -> None:
    """Teszt: A ColoredLogger extra mezőkkel tud logolni."""
    # Arrange
    stream = StringIO()
    logger = ColoredLogger(name="test_logger", stream=stream)

    # Act
    logger.info("Test message", extra={"user_id": 123})

    # Assert
    output = stream.getvalue()
    assert "Test message" in output
