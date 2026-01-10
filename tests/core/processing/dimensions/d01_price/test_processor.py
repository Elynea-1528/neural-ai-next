"""D01PriceProcessor unit tesztek."""

from datetime import datetime, timedelta

import numpy as np
import polars as pl
import pytest

from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor


class TestD01PriceProcessor:
    """D01PriceProcessor unit teszt osztály."""

    @pytest.fixture
    def processor(self) -> D01PriceProcessor:
        """D01PriceProcessor példány fixture."""
        return D01PriceProcessor()

    @pytest.fixture
    def sample_ohlcv_data(self) -> pl.DataFrame:
        """Mint OHLCV adatok fixture."""
        # 10 mock OHLCV rekord
        timestamps = [datetime(2023, 1, 1, 9, 0, 0) + timedelta(minutes=i) for i in range(10)]
        base_price = 1.0500

        data = []
        for ts in timestamps:
            open_price = base_price + np.random.normal(0, 0.001)
            close_price = open_price + np.random.normal(0, 0.002)
            high_price = max(open_price, close_price) + abs(np.random.normal(0, 0.001))
            low_price = min(open_price, close_price) - abs(np.random.normal(0, 0.001))

            data.append(
                {
                    "timestamp": ts,
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "tick_volume": int(np.random.normal(1000, 200)),
                    "spread": abs(np.random.normal(0.0002, 0.0001)),
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
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread",
            "real_volume",
        }
        assert set(result.columns) == expected_columns

        # Ellenőrizzük a sorok számát
        assert len(result) == len(sample_ohlcv_data)

        # Ellenőrizzük, hogy az adatok változatlanok (csak szelektálás)
        assert result["timestamp"].equals(sample_ohlcv_data["timestamp"])
        assert result["open"].equals(sample_ohlcv_data["open"])
        assert result["high"].equals(sample_ohlcv_data["high"])
        assert result["low"].equals(sample_ohlcv_data["low"])
        assert result["close"].equals(sample_ohlcv_data["close"])
        assert result["tick_volume"].equals(sample_ohlcv_data["tick_volume"])
        assert result["spread"].equals(sample_ohlcv_data["spread"])
        assert result["real_volume"].equals(sample_ohlcv_data["real_volume"])

    def test_process_empty_dataframe(self, processor: D01PriceProcessor):
        """Teszteli a process metódust üres DataFrame-mel."""
        empty_df = pl.DataFrame(
            schema={
                "timestamp": pl.Datetime,
                "open": pl.Float64,
                "high": pl.Float64,
                "low": pl.Float64,
                "close": pl.Float64,
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
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread",
            "real_volume",
        }
        assert set(result.columns) == expected_columns

    def test_process_missing_columns_raises_error(self, processor: D01PriceProcessor):
        """Teszteli, hogy hiányzó oszlopok esetén ColumnNotFoundError-t dob."""
        # Hiányzó spread oszlop
        incomplete_df = pl.DataFrame(
            {
                "timestamp": [datetime(2023, 1, 1, 9, 0, 0)],
                "open": [1.0500],
                "high": [1.0520],
                "low": [1.0480],
                "close": [1.0510],
                "tick_volume": [1000],
                "real_volume": [1500.0],
                # spread hiányzik
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

        # Csak a szükséges oszlopok maradnak
        expected_columns = {
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread",
            "real_volume",
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
        assert result["open"].dtype in [pl.Float32, pl.Float64]
        assert result["high"].dtype in [pl.Float32, pl.Float64]
        assert result["low"].dtype in [pl.Float32, pl.Float64]
        assert result["close"].dtype in [pl.Float32, pl.Float64]
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
