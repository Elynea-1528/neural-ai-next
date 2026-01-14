"""D02Support kivételek unit tesztek."""

from neural_ai.core.processing.dimensions.d02_support.exceptions.support_error import (
    SupportError,
    SupportResistanceLevelError,
    SwingPointCalculationError,
    TimeframeConfigurationError,
)


class TestSupportExceptions:
    """Support kivételek unit teszt osztály."""

    def test_support_error_creation(self):
        """Teszteli a SupportError létrehozását."""
        error = SupportError("Test error", "TEST_CODE")

        assert str(error) == "Test error"
        assert error.error_code == "TEST_CODE"

    def test_support_error_without_code(self):
        """Teszteli a SupportError létrehozását hibakód nélkül."""
        error = SupportError("Test error")

        assert str(error) == "Test error"
        assert error.error_code is None

    def test_swing_point_calculation_error(self):
        """Teszteli a SwingPointCalculationError létrehozását."""
        error = SwingPointCalculationError("Swing calculation failed", 5, "mid_high")

        assert str(error) == "Swing calculation failed"
        assert error.error_code == "SWING_POINT_CALCULATION_ERROR"
        assert error.window_size == 5
        assert error.column_name == "mid_high"

    def test_support_resistance_level_error(self):
        """Teszteli a SupportResistanceLevelError létrehozását."""
        error = SupportResistanceLevelError("Level calculation failed", "support", "rolling_mean")

        assert str(error) == "Level calculation failed"
        assert error.error_code == "SUPPORT_RESISTANCE_LEVEL_ERROR"
        assert error.level_type == "support"
        assert error.aggregation_method == "rolling_mean"

    def test_timeframe_configuration_error(self):
        """Teszteli a TimeframeConfigurationError létrehozását."""
        error = TimeframeConfigurationError("Config invalid", "H4", "swing_window")

        assert str(error) == "Config invalid"
        assert error.error_code == "TIMEFRAME_CONFIGURATION_ERROR"
        assert error.timeframe == "H4"
        assert error.config_key == "swing_window"

    def test_exception_inheritance(self):
        """Teszteli, hogy az összes kivétel örökli a SupportError-t."""
        swing_error = SwingPointCalculationError("test")
        level_error = SupportResistanceLevelError("test")
        config_error = TimeframeConfigurationError("test")

        assert isinstance(swing_error, SupportError)
        assert isinstance(level_error, SupportError)
        assert isinstance(config_error, SupportError)
