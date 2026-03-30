"""Tests for Processor Factory."""

from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)
from neural_ai.processors.factory import create_dimension_processor
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor


def test_create_dimension_processor_happy_path():
    """Test create_dimension_processor with valid config."""
    mock_config = MagicMock(spec=ConfigManagerInterface)
    mock_logger = MagicMock(spec=LoggerInterface)

    # Valid config setup for ProcessorsConfig
    # The factory calls ProcessorsConfig(processors=config.get("processors") or {})
    mock_config.get.side_effect = (
        lambda section, key=None: {"d02": {"min_candles": 5, "level_merge": 0.0005}}  # pyright: ignore[reportUnknownLambdaType]
        if section == "processors"
        else {}
    )

    # We need to ensure that when the factory imports the module dynamically, it works.
    # Since we are in the same environment, it should find the real class.

    # However, BaseDimensionProcessor.__init__ also calls config.get("processors", "d02")
    # So our side_effect needs to handle that too.
    def config_get_side_effect(section, key=None):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        if section == "processors":
            if key == "d02":
                return {"min_candles": 5, "level_merge": 0.0005}
            return {"d02": {"min_candles": 5, "level_merge": 0.0005}}
        return {}  # pyright: ignore[reportUnknownVariableType]

    mock_config.get.side_effect = config_get_side_effect

    processor = create_dimension_processor(2, mock_config, mock_logger)

    assert isinstance(processor, IDimensionProcessor)
    assert isinstance(processor, D02SupportProcessor)
    assert processor.dimension_id == 2


def test_create_dimension_processor_validation_error():
    """Test create_dimension_processor with invalid config."""
    mock_config = MagicMock(spec=ConfigManagerInterface)
    mock_logger = MagicMock(spec=LoggerInterface)

    # Invalid config: min_candles is negative (must be >= 1)
    def config_get_side_effect(section, key=None):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        if section == "processors":
            return {"d02": {"min_candles": -5}}
        return {}  # pyright: ignore[reportUnknownVariableType]

    mock_config.get.side_effect = config_get_side_effect

    with pytest.raises(ValidationError):
        create_dimension_processor(2, mock_config, mock_logger)


def test_create_dimension_processor_invalid_id():
    """Test create_dimension_processor with unknown dimension ID."""
    mock_config = MagicMock(spec=ConfigManagerInterface)
    mock_logger = MagicMock(spec=LoggerInterface)

    with pytest.raises(ValueError, match="Ismeretlen dimenzió ID"):
        create_dimension_processor(999, mock_config, mock_logger)
