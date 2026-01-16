"""D01PriceProcessor unit tesztek."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import numpy as np
import polars as pl
import pytest

from neural_ai.processors.processing.dimensions.d01_price.processor import D01PriceProcessor


class TestD01PriceProcessor:
    """D01PriceProcessor unit teszt osztály."""

    @pytest.fixture
    def processor(self) -> D01PriceProcessor:
        """D01PriceProcessor példány fixture."""
        # Mock config és logger létrehozása
        mock_config = MagicMock()
        mock_config.get.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_logger = MagicMock()
        return D01PriceProcessor(mock_config, mock_logger)

    @pytest.fixture
    def sample_ohlcv_data(self) -> pl.DataFrame:
        """Mint OHLCV adatok fixture."""
        # 100 mock OHLCV rekord (nagyobb dataset a rolling Z-score-hoz)
        timestamps = [datetime(2023, 1, 1, 9, 0, 0) + timedelta(minutes=i) for i in range(100)]
        base_price = 1.0500

        data = []
        for ts in timestamps:
            open_price = base_price + np.random.normal(0, 0.001)
            close_price = open_price + np.random.normal(0, 0.002)
            high_price = max(open_price, close_price) + abs(np.random.normal(0, 0.001))
            low_price = min(open_price, close_price) - abs(np.random.normal(0, 0.001))

            # Bid árak (spread figyelembevételével)
            spread = abs(np.random.normal(0.0002, 0.0001))
            bid_open = open_price - spread / 2
            bid_high = high_price - spread / 2
            bid_low = low_price - spread / 2
            bid_close = close_price - spread / 2

            data.append(
                {
                    "timestamp": ts,
                    "bid_open": bid_open,
                    "bid_high": bid_high,
                    "bid_low": bid_low,
                    "bid_close": bid_close,
                    "mid_open": open_price,
                    "mid_high": high_price,
                    "mid_low": low_price,
                    "mid_close": close_price,
                    "tick_volume": int(np.random.normal(1000, 200)),
                    "spread": spread,
                    "real_volume": np.random.normal(1500, 300),
                }
            )

            base_price = close_price

        return pl.DataFrame(data)

    def test_dimension_id(self, processor: D01PriceProcessor):
        """Teszteli a dimension_id property-t."""
        assert processor.dimension_id == 1

    def test_process_valid_data(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a process metódust érvényes adatokkal."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük az eredmény típusát
        assert isinstance(result, pl.DataFrame)

        # Ellenőrizzük az oszlopokat
        expected_columns = {
            "timestamp",
            "bid_open", "bid_high", "bid_low", "bid_close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "log_return",
            "rolling_z_score",
            "upper_shadow",
            "lower_shadow",
        }
        assert set(result.columns) == expected_columns

        # Ellenőrizzük a sorok számát
        assert len(result) == len(sample_ohlcv_data)

        # Ellenőrizzük, hogy az adatok változatlanok (csak szelektálás)
        assert result["timestamp"].equals(sample_ohlcv_data["timestamp"])
        assert result["mid_open"].equals(sample_ohlcv_data["mid_open"])
        assert result["mid_high"].equals(sample_ohlcv_data["mid_high"])
        assert result["mid_low"].equals(sample_ohlcv_data["mid_low"])
        assert result["mid_close"].equals(sample_ohlcv_data["mid_close"])
        assert result["tick_volume"].equals(sample_ohlcv_data["tick_volume"])
        assert result["spread"].equals(sample_ohlcv_data["spread"])
        assert result["real_volume"].equals(sample_ohlcv_data["real_volume"])

    def test_process_empty_dataframe(self, processor: D01PriceProcessor):
        """Teszteli a process metódust üres DataFrame-mel."""
        empty_df = pl.DataFrame(
            schema={
                "timestamp": pl.Datetime,
                "bid_open": pl.Float64,
                "bid_high": pl.Float64,
                "bid_low": pl.Float64,
                "bid_close": pl.Float64,
                "mid_open": pl.Float64,
                "mid_high": pl.Float64,
                "mid_low": pl.Float64,
                "mid_close": pl.Float64,
                "tick_volume": pl.Int64,
                "spread": pl.Float64,
                "real_volume": pl.Float64,
            }
        )

        result = processor.process(empty_df)

        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0
        expected_columns = {
            "timestamp",
            "bid_open", "bid_high", "bid_low", "bid_close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "log_return",
            "rolling_z_score",
            "upper_shadow",
            "lower_shadow",
        }
        assert set(result.columns) == expected_columns

    def test_process_missing_columns_raises_error(self, processor: D01PriceProcessor):
        """Teszteli, hogy hiányzó oszlopok esetén ColumnNotFoundError-t dob."""
        # Hiányzó bid_close és mid_close oszlop
        incomplete_df = pl.DataFrame(
            {
                "timestamp": [datetime(2023, 1, 1, 9, 0, 0)],
                "bid_open": [1.0499],
                "bid_high": [1.0519],
                "bid_low": [1.0479],
                # bid_close és mid_close hiányzik
                "mid_open": [1.0500],
                "mid_high": [1.0520],
                "mid_low": [1.0480],
                "tick_volume": [1000],
                "spread": [0.0002],
                "real_volume": [1500.0],
            }
        )

        # Polars select ColumnNotFoundError-t dob hiányzó oszlopokra
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            processor.process(incomplete_df)

    def test_process_extra_columns_ignored(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli, hogy extra oszlopok figyelmen kívül maradnak."""
        # Extra oszlop hozzáadása
        data_with_extra = sample_ohlcv_data.with_columns(extra_col=pl.lit("extra"))

        result = processor.process(data_with_extra)

        # Csak a szükséges oszlopok maradnak (és az újak)
        expected_columns = {
            "timestamp",
            "bid_open", "bid_high", "bid_low", "bid_close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "log_return",
            "rolling_z_score",
            "upper_shadow",
            "lower_shadow",
        }
        assert set(result.columns) == expected_columns
        assert "extra_col" not in result.columns

    def test_process_data_types_preserved(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli, hogy az adattípusok megmaradnak."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük a fontos adattípusokat
        assert result["timestamp"].dtype == pl.Datetime
        assert result["mid_open"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_high"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_low"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_close"].dtype in [pl.Float32, pl.Float64]
        assert result["tick_volume"].dtype in [pl.Int32, pl.Int64]
        assert result["spread"].dtype in [pl.Float32, pl.Float64]
        assert result["real_volume"].dtype in [pl.Float32, pl.Float64]

    def test_process_order_preserved(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli, hogy a sorok sorrendje megmarad."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük, hogy a timestamp oszlop sorrendje azonos
        assert result["timestamp"].equals(sample_ohlcv_data["timestamp"])

    def test_process_tick_timeframe_shadows_none(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a process metódust tick timeframe-mal, ahol shadows None."""
        result = processor.process(sample_ohlcv_data, timeframe="tick")

        # Ellenőrizzük az eredmény típusát
        assert isinstance(result, pl.DataFrame)

        # Oszlopok azonosak, kivéve hogy shadows None
        expected_columns = {
            "timestamp",
            "bid_open", "bid_high", "bid_low", "bid_close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "log_return",
            "rolling_z_score",
            "upper_shadow",
            "lower_shadow",
        }
        assert set(result.columns) == expected_columns

        # Shadows None kell legyenek
        assert result["upper_shadow"].is_null().all()
        assert result["lower_shadow"].is_null().all()

        # Egyéb adatok megmaradnak
        assert result["timestamp"].equals(sample_ohlcv_data["timestamp"])
        assert result["mid_close"].equals(sample_ohlcv_data["mid_close"])

    def test_process_ohlc_timeframe_with_shadows(
        self, processor: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a process metódust OHLC timeframe-mal calc_shadows=True."""
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Shadows nem None
        assert not result["upper_shadow"].is_null().all()
        assert not result["lower_shadow"].is_null().all()

    @pytest.fixture
    def processor_no_shadows(self) -> D01PriceProcessor:
        """D01PriceProcessor példány fixture calc_shadows=False."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"z_score_window": 60, "calc_shadows": False}
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": False}
        mock_logger = MagicMock()
        return D01PriceProcessor(mock_config, mock_logger)

    def test_process_ohlc_timeframe_no_shadows(
        self, processor_no_shadows: D01PriceProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a process metódust OHLC timeframe-mal calc_shadows=False."""
        result = processor_no_shadows.process(sample_ohlcv_data, timeframe="1m")

        # Shadows None
        assert result["upper_shadow"].is_null().all()
        assert result["lower_shadow"].is_null().all()
