"""Tests for D02 Support Factory - 100% coverage."""

from unittest.mock import MagicMock

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d02_support.factory import D02SupportFactory
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)


def test_d02_factory_create():
    """Test: Factory létrehozza a D02SupportProcessor példányt."""
    config = MagicMock(spec=ConfigManagerInterface)
    logger = MagicMock(spec=LoggerInterface)

    processor = D02SupportFactory.create(config, logger)

    assert isinstance(processor, D02SupportProcessor)
    assert processor.dimension_id == 2  # D02 = 2


def test_d02_factory_create_with_config():
    """Test: Factory config paraméterekkel."""
    config = MagicMock(spec=ConfigManagerInterface)
    logger = MagicMock(spec=LoggerInterface)
    config.get.return_value = {"min_candles": 10, "level_merge": 0.001}

    processor = D02SupportFactory.create(config, logger)

    assert isinstance(processor, D02SupportProcessor)
    assert processor.dimension_id == 2  # D02 = 2
