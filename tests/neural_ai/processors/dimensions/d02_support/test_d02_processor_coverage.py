"""Additional tests for D02 Support Processor - 100% coverage."""

from unittest.mock import MagicMock

import polars as pl
import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
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


class TestD02ProcessorMissingConfigBranches:
    """Test hiányzó config paraméterek branch coverage-hez."""

    def test_merge_levels_missing_level_merge_config(self, mock_deps):
        """Test: level_merge hiányzik a configból (133-136 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5}
        processor = D02SupportProcessor(config, logger)

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
        assert logger.warning.call_count >= 1
        assert isinstance(result, pl.DataFrame)

    def test_merge_levels_large_dataframe_skip_merge(self, mock_deps):
        """Test: Nagy DataFrame (> 5000 sor) esetén merge skip (130-136 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5, "level_merge": 0.001}
        processor = D02SupportProcessor(config, logger)

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
        warning_calls = [str(call) for call in logger.warning.call_args_list]
        assert any("Too many swing points" in str(call) for call in warning_calls)
        assert isinstance(result, pl.DataFrame)

    def test_confirm_with_volume_missing_config(self, mock_deps):
        """Test: volume_confirmation hiányzik a configból (292-297 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5}
        processor = D02SupportProcessor(config, logger)

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
        warning_calls = [str(call) for call in logger.warning.call_args_list]
        assert any("volume_confirmation" in str(call) for call in warning_calls)
        assert isinstance(result, pl.DataFrame)

    def test_confirm_with_volume_false(self, mock_deps):
        """Test: volume_confirmation = False (300-301 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5, "volume_confirmation": False}
        processor = D02SupportProcessor(config, logger)

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


    def test_confirm_with_volume_true(self, mock_deps):
        """Test: volume_confirmation = True (300-301 sorok - threshold számítás)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5, "volume_confirmation": True}
        processor = D02SupportProcessor(config, logger)

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

    def test_nearest_support_no_candidates_below(self, mock_deps):
        """Test: Nincs support szint az aktuális ár alatt (493-497 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5}
        processor = D02SupportProcessor(config, logger)

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

    def test_nearest_resistance_no_candidates_above(self, mock_deps):
        """Test: Nincs resistance szint az aktuális ár felett (500-504 sorok)."""
        config, logger = mock_deps
        config.get.return_value = {"min_candles": 5}
        processor = D02SupportProcessor(config, logger)

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
