"""Tests for D02 Support Exceptions - 100% coverage."""

from neural_ai.processors.dimensions.d02_support.exceptions.support_error import (
    SupportError,
    SupportResistanceLevelError,
    SwingPointCalculationError,
    TimeframeConfigurationError,
)


def test_support_error_basic():
    """Test: SupportError alapvető használat."""
    error = SupportError("Test error message")
    assert str(error) == "Test error message"
    assert isinstance(error, Exception)
    assert error.error_code is None


def test_support_error_with_error_code():
    """Test: SupportError hibakóddal."""
    error = SupportError("Test error", error_code="TEST_ERROR")
    assert str(error) == "Test error"
    assert error.error_code == "TEST_ERROR"


def test_swing_point_calculation_error():
    """Test: SwingPointCalculationError használat."""
    error = SwingPointCalculationError("Swing point error")
    assert str(error) == "Swing point error"
    assert isinstance(error, SupportError)
    assert error.error_code == "SWING_POINT_CALCULATION_ERROR"
    assert error.window_size is None
    assert error.column_name is None


def test_swing_point_calculation_error_with_details():
    """Test: SwingPointCalculationError részletekkel."""
    error = SwingPointCalculationError(
        "Swing point error", window_size=5, column_name="mid_high"
    )
    assert str(error) == "Swing point error"
    assert error.window_size == 5
    assert error.column_name == "mid_high"
    assert error.error_code == "SWING_POINT_CALCULATION_ERROR"


def test_support_resistance_level_error():
    """Test: SupportResistanceLevelError használat."""
    error = SupportResistanceLevelError("Level error")
    assert str(error) == "Level error"
    assert isinstance(error, SupportError)
    assert error.error_code == "SUPPORT_RESISTANCE_LEVEL_ERROR"
    assert error.level_type is None
    assert error.aggregation_method is None


def test_support_resistance_level_error_with_details():
    """Test: SupportResistanceLevelError részletekkel."""
    error = SupportResistanceLevelError(
        "Level error", level_type="support", aggregation_method="mean"
    )
    assert str(error) == "Level error"
    assert error.level_type == "support"
    assert error.aggregation_method == "mean"
    assert error.error_code == "SUPPORT_RESISTANCE_LEVEL_ERROR"


def test_timeframe_configuration_error():
    """Test: TimeframeConfigurationError használat."""
    error = TimeframeConfigurationError("Config error")
    assert str(error) == "Config error"
    assert isinstance(error, SupportError)
    assert error.error_code == "TIMEFRAME_CONFIGURATION_ERROR"
    assert error.timeframe is None
    assert error.config_key is None


def test_timeframe_configuration_error_with_details():
    """Test: TimeframeConfigurationError részletekkel."""
    error = TimeframeConfigurationError(
        "Config error", timeframe="H1", config_key="swing_window"
    )
    assert str(error) == "Config error"
    assert error.timeframe == "H1"
    assert error.config_key == "swing_window"
    assert error.error_code == "TIMEFRAME_CONFIGURATION_ERROR"


def test_exception_hierarchy():
    """Test: Exception hierarchia ellenőrzése."""
    swing_error = SwingPointCalculationError("Swing")
    level_error = SupportResistanceLevelError("Level")
    config_error = TimeframeConfigurationError("Config")

    assert isinstance(swing_error, SupportError)
    assert isinstance(level_error, SupportError)
    assert isinstance(config_error, SupportError)

    assert isinstance(swing_error, Exception)
    assert isinstance(level_error, Exception)
    assert isinstance(config_error, Exception)
