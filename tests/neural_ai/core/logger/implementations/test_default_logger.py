"""Unit tesztek a neural_ai.core.logger.implementations.default_logger modulhoz.

Ez a teszt ellenőrzi a DefaultLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Log szintek (debug, info, warning, error, critical)
3. Structlog integráció
4. LoggerInterface implementáció
"""

import logging
from io import StringIO

from neural_ai.core.logger.implementations.default_logger import DefaultLogger


def test_default_logger_initialization() -> None:
    """Teszt: A DefaultLogger inicializálható."""
    # Arrange & Act
    logger = DefaultLogger(name="test_logger")

    # Assert
    assert logger is not None
    assert logger.logger.name == "test_logger"


def test_default_logger_default_level() -> None:
    """Teszt: A DefaultLogger alapértelmezett log szintje INFO."""
    # Arrange & Act
    logger = DefaultLogger(name="test_logger")

    # Assert
    assert logger.logger.level == logging.INFO


def test_default_logger_custom_level() -> None:
    """Teszt: A DefaultLogger egyedi log szinttel inicializálható."""
    # Arrange & Act
    logger = DefaultLogger(name="test_logger", level=logging.DEBUG)

    # Assert
    assert logger.logger.level == logging.DEBUG


def test_default_logger_info_message() -> None:
    """Teszt: A DefaultLogger info üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = DefaultLogger(name="test_logger")
    logger.logger.addHandler(handler)

    # Act
    logger.info("Test info message")

    # Assert
    output = stream.getvalue()
    assert "Test info message" in output


def test_default_logger_warning_message() -> None:
    """Teszt: A DefaultLogger warning üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = DefaultLogger(name="test_logger")
    logger.logger.addHandler(handler)

    # Act
    logger.warning("Test warning message")

    # Assert
    output = stream.getvalue()
    assert "Test warning message" in output


def test_default_logger_error_message() -> None:
    """Teszt: A DefaultLogger error üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = DefaultLogger(name="test_logger")
    logger.logger.addHandler(handler)

    # Act
    logger.error("Test error message")

    # Assert
    output = stream.getvalue()
    assert "Test error message" in output


def test_default_logger_debug_message() -> None:
    """Teszt: A DefaultLogger debug üzenetet tud logolni DEBUG szinten."""
    # Arrange
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = DefaultLogger(name="test_logger", level=logging.DEBUG)
    logger.logger.addHandler(handler)

    # Act
    logger.debug("Test debug message")

    # Assert
    output = stream.getvalue()
    assert "Test debug message" in output


def test_default_logger_critical_message() -> None:
    """Teszt: A DefaultLogger critical üzenetet tud logolni."""
    # Arrange
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    logger = DefaultLogger(name="test_logger")
    logger.logger.addHandler(handler)

    # Act
    logger.critical("Test critical message")

    # Assert
    output = stream.getvalue()
    assert "Test critical message" in output
