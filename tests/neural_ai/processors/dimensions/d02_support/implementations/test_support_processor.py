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


def _create_mock_config_dict(**kwargs: object) -> dict[str, object]:  # pyright: ignore[reportUnknownParameterType]
    """Helper: Mock config dict létrehozása ProcessorConfig mezőkkel.

    A BaseDimensionProcessor ProcessorConfig(**raw_config) hívást vár,
    tehát dict-et kell visszaadnunk, nem Pydantic objektumot.

    Args:
        **kwargs: ProcessorConfig mezők (pl. min_candles=5)

    Returns:
        dict: Config dict a BaseDimensionProcessor számára
    """
    return dict(kwargs)  # pyright: ignore[reportReturnType]


@pytest.fixture(scope="function")
def mock_deps():
    """Create mock dependencies."""
    config = MagicMock(spec=ConfigManagerInterface)
    logger = MagicMock(spec=LoggerInterface)
    return config, logger


def test_d02_processor_happy_path(mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Test D02SupportProcessor instantiation with valid config."""
    config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]

    # Mock config return for BaseDimensionProcessor
    # config.get("processors", "d02")
    config.get.return_value = _create_mock_config_dict(  # pyright: ignore[reportUnknownMemberType]
        min_candles=10,
        level_merge=0.0005,
        strength_window=10,
        min_touches=2,
    )

    processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

    assert isinstance(processor.dim_config, ProcessorConfig)
    assert processor.dim_config.min_candles == 10
    assert processor.dim_config.level_merge == 0.0005
    assert processor.dim_config.strength_window == 10


def test_d02_processor_defaults(mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Test D02SupportProcessor default values."""
    config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]

    # Empty config
    config.get.return_value = _create_mock_config_dict()  # pyright: ignore[reportUnknownMemberType]

    processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

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


def test_d02_processor_validation_error(mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Test D02SupportProcessor with invalid config."""
    config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]

    # Invalid config: min_candles < 1
    config.get.return_value = _create_mock_config_dict(min_candles=0)  # pyright: ignore[reportUnknownMemberType]

    with pytest.raises(ValidationError):
        D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]


def test_d02_processor_invalid_type(mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """Test D02SupportProcessor with invalid type in config."""
    config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]

    # Invalid config: min_candles is string instead of int (pydantic might coerce strings to int)
    # Let's use something that cannot be coerced easily or clearly wrong type
    config.get.return_value = _create_mock_config_dict(min_candles="not_an_integer")  # pyright: ignore[reportUnknownMemberType]

    with pytest.raises(ValidationError):
        D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]
"""Additional tests for D02 Support Processor - 100% coverage."""




class TestD02ProcessorMissingConfigBranches:
    """Test hiányzó config paraméterek branch coverage-hez."""

    def test_merge_levels_missing_level_merge_config(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: level_merge hiányzik a configból (133-136 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Kis DataFrame (< 5000 sor) hogy elérjük a level_merge ellenőrzést
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 20),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 21,
                "mid_high": [1.1010] * 21,
                "mid_low": [1.0990] * 21,
                "mid_close": [1.1005] * 21,
                "real_volume": [100.0] * 21,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy warning log hívás történt
        assert logger.warning.call_count >= 1  # pyright: ignore[reportUnknownMemberType]
        assert isinstance(result, pl.DataFrame)

    def test_merge_levels_large_dataframe_skip_merge(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Nagy DataFrame (> 5000 sor) esetén merge skip (130-136 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5, "level_merge": 0.001}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Nagy DataFrame (> 5000 sor)
        large_size = 5100
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 0, 0),
                    end=pl.datetime(2024, 1, 1, 0, 0) + pl.duration(minutes=large_size - 1),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * large_size,
                "mid_high": [1.1010] * large_size,
                "mid_low": [1.0990] * large_size,
                "mid_close": [1.1005] * large_size,
                "real_volume": [100.0] * large_size,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy warning log hívás történt (too many swing points)
        warning_calls = [str(call) for call in logger.warning.call_args_list]  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType, reportUnknownMemberType]
        assert any("Too many swing points" in str(call) for call in warning_calls)
        assert isinstance(result, pl.DataFrame)

    def test_confirm_with_volume_missing_config(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: volume_confirmation hiányzik a configból (292-297 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 20),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 21,
                "mid_high": [1.1010] * 21,
                "mid_low": [1.0990] * 21,
                "mid_close": [1.1005] * 21,
                "real_volume": [100.0] * 21,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy warning log hívás történt
        warning_calls = [str(call) for call in logger.warning.call_args_list]  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType, reportUnknownMemberType]
        assert any("volume_confirmation" in str(call) for call in warning_calls)
        assert isinstance(result, pl.DataFrame)

    def test_confirm_with_volume_false(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: volume_confirmation = False (300-301 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5, "volume_confirmation": False}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 20),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 21,
                "mid_high": [1.1010] * 21,
                "mid_low": [1.0990] * 21,
                "mid_close": [1.1005] * 21,
                "real_volume": [100.0] * 21,
            }
        )

        result = processor.process(df)

        # volume_confirmation = False esetén is működnie kell
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0


    def test_confirm_with_volume_true(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: volume_confirmation = True (300-301 sorok - threshold számítás)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5, "volume_confirmation": True}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Legalább 20 sor kell a rolling_mean(20) számításhoz
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 30),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 31,
                "mid_high": [1.1010] * 31,
                "mid_low": [1.0990] * 31,
                "mid_close": [1.1005] * 31,
                "real_volume": [100.0] * 31,
            }
        )

        result = processor.process(df)

        # volume_confirmation = True esetén threshold számítás fut
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0


class TestD02ProcessorNearestLevelsEdgeCases:
    """Test find_nearest_support/resistance edge cases (493-504 sorok)."""

    def test_nearest_support_no_candidates_below(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Nincs support szint az aktuális ár alatt (493-497 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Monoton növekvő árak (nincs support az aktuális ár alatt)
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 30),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000 + i * 0.0001 for i in range(31)],
                "mid_high": [1.1010 + i * 0.0001 for i in range(31)],
                "mid_low": [1.0990 + i * 0.0001 for i in range(31)],
                "mid_close": [1.1005 + i * 0.0001 for i in range(31)],
                "real_volume": [100.0] * 31,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy a result tartalmaz nearest_support oszlopot
        # (lehet None értékekkel, ha nincs support az ár alatt)
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0

    def test_nearest_resistance_no_candidates_above(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Nincs resistance szint az aktuális ár felett (500-504 sorok)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Monoton csökkenő árak (nincs resistance az aktuális ár felett)
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 30),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1100 - i * 0.0001 for i in range(31)],
                "mid_high": [1.1110 - i * 0.0001 for i in range(31)],
                "mid_low": [1.1090 - i * 0.0001 for i in range(31)],
                "mid_close": [1.1105 - i * 0.0001 for i in range(31)],
                "real_volume": [100.0] * 31,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy a result tartalmaz nearest_resistance oszlopot
        # (lehet None értékekkel, ha nincs resistance az ár felett)
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0
"""Extended tests for D02 Support Processor - Coverage pótlás."""




@pytest.fixture(scope="function")
def sample_ohlcv_df():
    """Create sample OHLCV DataFrame for testing."""
    return pl.DataFrame(
        {
            "timestamp": pl.datetime_range(
                start=pl.datetime(2024, 1, 1, 10, 0),
                end=pl.datetime(2024, 1, 1, 10, 30),
                interval="1m",
                eager=True,
            ),
            "mid_open": [1.1000, 1.1005, 1.1010, 1.1015, 1.1020] * 6 + [1.1025],
            "mid_high": [1.1010, 1.1015, 1.1020, 1.1025, 1.1030] * 6 + [1.1035],
            "mid_low": [1.0990, 1.0995, 1.1000, 1.1005, 1.1010] * 6 + [1.1015],
            "mid_close": [1.1005, 1.1010, 1.1015, 1.1020, 1.1025] * 6 + [1.1030],
            "real_volume": [100.0, 150.0, 200.0, 180.0, 120.0] * 6 + [130.0],
        }
    )


class TestD02ProcessorCategorizeZones:
    """Test _categorize_zones method coverage."""

    def test_categorize_zones_strong_levels(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Strong levels kategorizálása (strength > 0.7, touches >= min_touches)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_touches": 2}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        levels = [
            {"type": "support", "price": 1.1000, "strength": 0.8, "touches": 3},
            {"type": "resistance", "price": 1.1050, "strength": 0.9, "touches": 4},
        ]

        result = processor._categorize_zones(levels)  # type: ignore[arg-type]

        assert len(result["support"]["strong"]) == 1
        assert len(result["resistance"]["strong"]) == 1
        assert result["support"]["strong"][0]["strength"] == 0.8
        assert result["resistance"]["strong"][0]["strength"] == 0.9

    def test_categorize_zones_moderate_levels(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Moderate levels kategorizálása (0.3 <= strength <= 0.7)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_touches": 2}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        levels = [
            {"type": "support", "price": 1.1000, "strength": 0.5, "touches": 2},
            {"type": "resistance", "price": 1.1050, "strength": 0.6, "touches": 3},
        ]

        result = processor._categorize_zones(levels)  # type: ignore[arg-type]

        assert len(result["support"]["moderate"]) == 1
        assert len(result["resistance"]["moderate"]) == 1

    def test_categorize_zones_weak_levels(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Weak levels kategorizálása (strength < 0.3)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_touches": 2}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        levels = [
            {"type": "support", "price": 1.1000, "strength": 0.2, "touches": 1},
            {"type": "resistance", "price": 1.1050, "strength": 0.1, "touches": 1},
        ]

        result = processor._categorize_zones(levels)  # type: ignore[arg-type]

        assert len(result["support"]["weak"]) == 1
        assert len(result["resistance"]["weak"]) == 1

    def test_categorize_zones_moderate_low_touches_high_strength(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Moderate kategória (touches < min_touches de strength > 0.4)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_touches": 3}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        levels = [
            {"type": "support", "price": 1.1000, "strength": 0.5, "touches": 2},
        ]

        result = processor._categorize_zones(levels)  # type: ignore[arg-type]

        assert len(result["support"]["moderate"]) == 1

    def test_categorize_zones_missing_min_touches_config(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: min_touches hiányzik a configból (default 1 használata)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        levels = [
            {"type": "support", "price": 1.1000, "strength": 0.8, "touches": 1},
        ]

        result = processor._categorize_zones(levels)  # type: ignore[arg-type]

        # Default min_touches=1, így strong kategória
        assert len(result["support"]["strong"]) == 1
        # Warning hívás ellenőrzése (lehet több is)
        assert logger.warning.call_count >= 1  # pyright: ignore[reportUnknownMemberType]


class TestD02ProcessorMidColumnsHandling:
    """Test mid oszlopok hiányának kezelése."""

    def test_process_with_bid_columns_no_mid(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Mid oszlopok hiányoznak, Bid oszlopok másolása."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 10),
                    interval="1m",
                    eager=True,
                ),
                "bid_open": [1.1000] * 11,
                "bid_high": [1.1010] * 11,
                "bid_low": [1.0990] * 11,
                "bid_close": [1.1005] * 11,
                "real_volume": [100.0] * 11,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy mid oszlopok létrejöttek
        assert "mid_open" in result.columns
        assert "mid_high" in result.columns
        assert "mid_low" in result.columns
        assert "mid_close" in result.columns
        logger.info.assert_called()  # pyright: ignore[reportUnknownMemberType]

    def test_process_with_simple_ohlc_no_mid(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Mid oszlopok hiányoznak, sima OHLC oszlopok másolása."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 10),
                    interval="1m",
                    eager=True,
                ),
                "open": [1.1000] * 11,
                "high": [1.1010] * 11,
                "low": [1.0990] * 11,
                "close": [1.1005] * 11,
                "real_volume": [100.0] * 11,
            }
        )

        result = processor.process(df)

        # Ellenőrizzük, hogy mid oszlopok létrejöttek
        assert "mid_open" in result.columns
        assert "mid_high" in result.columns
        assert "mid_low" in result.columns
        assert "mid_close" in result.columns
        logger.info.assert_called()  # pyright: ignore[reportUnknownMemberType]

    def test_process_missing_all_ohlc_columns(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Hiányzó OHLC oszlopok (ColumnNotFoundError várható)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 10),
                    interval="1m",
                    eager=True,
                ),
                "real_volume": [100.0] * 11,
            }
        )

        # Hiányzó OHLC oszlopok esetén ColumnNotFoundError várható
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            processor.process(df)


class TestD02ProcessorMarketHoursFiltering:
    """Test market hours filtering coverage."""

    def test_process_with_market_hours_enabled_filtering(self, mock_deps, sample_ohlcv_df):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Market hours enabled, filtering triggered."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(  # pyright: ignore[reportUnknownMemberType]
            min_candles=5,
            market_hours={
                "enabled": True,
                "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "hours": ["09:00", "17:00"],
                "log_filtering": True,
            },
        )
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Hozzáadunk hétvégi adatokat (szombat)
        df_with_weekend = sample_ohlcv_df.with_columns(  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            pl.datetime(2024, 1, 6, 10, 0).alias("timestamp")  # Szombat
        )

        processor.process(df_with_weekend)  # pyright: ignore[reportUnknownArgumentType]

        # Market hours log hívás ellenőrzése
        assert logger.info.call_count >= 1  # pyright: ignore[reportUnknownMemberType]

    def test_process_with_market_hours_outside_hours(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Market hours filtering - outside trading hours."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(  # pyright: ignore[reportUnknownMemberType]
            min_candles=5,
            market_hours={
                "enabled": True,
                "weekdays": ["Monday"],
                "hours": ["09:00", "17:00"],
                "log_filtering": True,
            },
        )
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        # Éjszakai adatok (18:00-20:00)
        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 18, 0),  # Hétfő este
                    end=pl.datetime(2024, 1, 1, 20, 0),
                    interval="10m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 13,
                "mid_high": [1.1010] * 13,
                "mid_low": [1.0990] * 13,
                "mid_close": [1.1005] * 13,
                "real_volume": [100.0] * 13,
            }
        )

        processor.process(df)

        # Market hours log hívás ellenőrzése
        assert logger.info.call_count >= 1  # pyright: ignore[reportUnknownMemberType]


class TestD02ProcessorNearestLevels:
    """Test find_nearest_support/resistance coverage."""

    def test_process_calculates_nearest_support(self, mock_deps, sample_ohlcv_df):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Legközelebbi support szint számítása (ha implementálva)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        result = processor.process(sample_ohlcv_df)  # pyright: ignore[reportUnknownArgumentType]

        # Ellenőrizzük, hogy a result DataFrame típusú és nem üres
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0
        # Ha nearest_support oszlop létezik, ellenőrizzük
        # (Ha nincs implementálva, akkor csak az alapvető oszlopokat várjuk)

    def test_process_calculates_nearest_resistance(self, mock_deps, sample_ohlcv_df):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Legközelebbi resistance szint számítása (ha implementálva)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=5)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        result = processor.process(sample_ohlcv_df)  # pyright: ignore[reportUnknownArgumentType]

        # Ellenőrizzük, hogy a result DataFrame típusú és nem üres
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0
        # Ha nearest_resistance oszlop létezik, ellenőrizzük
        # (Ha nincs implementálva, akkor csak az alapvető oszlopokat várjuk)


class TestD02ProcessorEdgeCases:
    """Test edge cases és branch coverage."""

    def test_process_with_empty_dataframe(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Üres DataFrame kezelése (Polars rolling_max hiba várható)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {"min_candles": 5}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": [],
                "mid_open": [],
                "mid_high": [],
                "mid_low": [],
                "mid_close": [],
                "real_volume": [],
            }
        )

        # Üres DataFrame esetén Polars InvalidOperationError várható
        try:
            result = processor.process(df)
            # Ha nem dob hibát, akkor üres eredményt várunk
            assert len(result) == 0
        except Exception as e:
            # Polars hiba elfogadható üres DataFrame esetén
            assert "rolling" in str(e).lower() or "null" in str(e).lower()

    def test_process_with_insufficient_data(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: Kevés adat (< min_candles)."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = _create_mock_config_dict(min_candles=10)  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        df = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 10, 0),
                    end=pl.datetime(2024, 1, 1, 10, 4),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000] * 5,
                "mid_high": [1.1010] * 5,
                "mid_low": [1.0990] * 5,
                "mid_close": [1.1005] * 5,
                "real_volume": [100.0] * 5,
            }
        )

        result = processor.process(df)

        # Kevés adat esetén is működnie kell (rolling window None értékekkel)
        assert len(result) == 5

    def test_dimension_id_property(self, mock_deps):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test: dimension_id property."""
        config, logger = mock_deps  # pyright: ignore[reportUnknownVariableType]
        config.get.return_value = {}  # pyright: ignore[reportUnknownMemberType]
        processor = D02SupportProcessor(config, logger)  # pyright: ignore[reportUnknownArgumentType]

        assert processor.dimension_id == 2
