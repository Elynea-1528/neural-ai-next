"""Tests for D02 Support Processor."""

from unittest.mock import MagicMock

import polars as pl
import pytest
from pydantic import ValidationError

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.types import ProcessorConfig
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)


@pytest.fixture
def mock_deps():
    """Create mock dependencies."""
    config = MagicMock(spec=ConfigManagerInterface)
    logger = MagicMock(spec=LoggerInterface)
    return config, logger


def test_d02_processor_happy_path(mock_deps):
    """Test D02SupportProcessor instantiation with valid config."""
    config, logger = mock_deps

    # Mock config return for BaseDimensionProcessor
    # config.get("processors", "d02")
    config.get.return_value = {
        "min_candles": 10,
        "level_merge": 0.0005,
        "strength_window": 10,
        "min_touches": 2,
    }

    processor = D02SupportProcessor(config, logger)

    assert isinstance(processor.dim_config, ProcessorConfig)
    assert processor.dim_config.min_candles == 10
    assert processor.dim_config.level_merge == 0.0005
    assert processor.dim_config.strength_window == 10


def test_d02_processor_defaults(mock_deps):
    """Test D02SupportProcessor default values."""
    config, logger = mock_deps

    # Empty config
    config.get.return_value = {}

    processor = D02SupportProcessor(config, logger)

    assert isinstance(processor.dim_config, ProcessorConfig)
    # Fields are optional in Pydantic model, so they should be None
    assert processor.dim_config.min_candles is None

    # Create a dummy DataFrame for process
    # We need enough rows for rolling windows (default min_candles=5)
    df = pl.DataFrame(
        {
            "timestamp": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "mid_open": [1.0] * 10,
            "mid_high": [1.1] * 10,
            "mid_low": [0.9] * 10,
            "mid_close": [1.0] * 10,
            "real_volume": [100.0] * 10,
        }
    )

    # Add datetime column for market hours check compatibility
    df = df.with_columns(pl.datetime(2024, 1, 1).alias("timestamp"))

    # Run process to verify defaults don't crash
    result = processor.process(df)

    # Check if key columns are present
    assert "swing_high_body" in result.columns
    assert "swing_low_body" in result.columns
    assert "nearest_support" in result.columns
    assert "nearest_resistance" in result.columns


def test_d02_processor_validation_error(mock_deps):
    """Test D02SupportProcessor with invalid config."""
    config, logger = mock_deps

    # Invalid config: min_candles < 1
    config.get.return_value = {"min_candles": 0}

    with pytest.raises(ValidationError):
        D02SupportProcessor(config, logger)


def test_d02_processor_invalid_type(mock_deps):
    """Test D02SupportProcessor with invalid type in config."""
    config, logger = mock_deps

    # Invalid config: min_candles is string instead of int (pydantic might coerce strings to int)
    # Let's use something that cannot be coerced easily or clearly wrong type
    config.get.return_value = {"min_candles": "not_an_integer"}

    with pytest.raises(ValidationError):
        D02SupportProcessor(config, logger)
