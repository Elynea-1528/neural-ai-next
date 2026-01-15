"""D02SupportProcessor unit tesztek."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import numpy as np
import polars as pl
import pytest

from neural_ai.core.processing.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)


class TestD02SupportProcessor:
    """D02SupportProcessor unit teszt osztály."""

    @pytest.fixture
    def processor(self) -> D02SupportProcessor:
        """D02SupportProcessor példány fixture."""
        # Mock config és logger létrehozása
        mock_config = MagicMock()
        mock_config.get.return_value = {
            "swing_window": 5,
            "min_distance": 10,
            "volume_confirmation": True
        }
        mock_logger = MagicMock()
        return D02SupportProcessor(mock_config, mock_logger)

    @pytest.fixture
    def sample_ohlcv_data(self) -> pl.DataFrame:
        """Mint OHLCV adatok fixture swing pontok teszteléséhez."""
        # 50 mock OHLCV rekord swing pontok generálásához
        timestamps = [datetime(2023, 1, 1, 9, 0, 0) + timedelta(minutes=i) for i in range(50)]
        base_price = 1.0500

        data = []
        for i, ts in enumerate(timestamps):
            # Swing minták létrehozása: magasabb alacsonyabb periódusok
            if i < 10:  # Első szakasz: emelkedő trend
                open_price = base_price + i * 0.0005
                close_price = open_price + 0.0003
                high_price = close_price + 0.0002
                low_price = open_price - 0.0001
            elif i < 25:  # Második szakasz: csökkenő trend
                open_price = base_price - (i - 10) * 0.0004
                close_price = open_price - 0.0002
                high_price = open_price + 0.0001
                low_price = close_price - 0.0003
            else:  # Harmadik szakasz: oldalazó
                open_price = base_price + np.random.normal(0, 0.0002)
                close_price = open_price + np.random.normal(0, 0.0001)
                high_price = max(open_price, close_price) + abs(np.random.normal(0, 0.0001))
                low_price = min(open_price, close_price) - abs(np.random.normal(0, 0.0001))

            data.append(
                {
                    "timestamp": ts,
                    "open": open_price,
                    "high": high_price + 0.001,  # Teljes high magasabb
                    "low": low_price - 0.001,  # Teljes low alacsonyabb
                    "close": close_price,
                    "mid_open": open_price,
                    "mid_high": high_price,
                    "mid_low": low_price,
                    "mid_close": close_price,
                    "tick_volume": int(np.random.normal(1000, 200)),
                    "spread": abs(np.random.normal(0.0002, 0.0001)),
                    "real_volume": np.random.normal(1500, 300),
                }
            )

            base_price = close_price

        return pl.DataFrame(data)

    def test_dimension_id(self, processor: D02SupportProcessor):
        """Teszteli a dimension_id property-t."""
        assert processor.dimension_id == 2

    def test_process_valid_data(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a process metódust érvényes adatokkal."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük az eredmény típusát
        assert isinstance(result, pl.DataFrame)

        # Ellenőrizzük az új oszlopokat
        expected_new_columns = {
            "swing_high_body",
            "swing_low_body",
            "swing_high_wick",
            "swing_low_wick",
        }
        assert all(col in result.columns for col in expected_new_columns)

        # Ellenőrizzük, hogy az eredeti oszlopok megmaradtak
        original_columns = {
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
        }
        assert all(col in result.columns for col in original_columns)

        # Ellenőrizzük a sorok számát
        assert len(result) == len(sample_ohlcv_data)

    def test_process_swing_high_body_detection(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a body swing high pontok helyes detektálását."""
        result = processor.process(sample_ohlcv_data)

        # Swing high body Float vagy None lehet
        assert result["swing_high_body"].dtype in [pl.Float32, pl.Float64]

        # Legalább egy swing high pontnak kell lennie (a minta adatokban)
        assert result["swing_high_body"].drop_nulls().len() > 0

    def test_process_swing_low_body_detection(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a body swing low pontok helyes detektálását."""
        result = processor.process(sample_ohlcv_data)

        # Swing low body Float vagy None lehet
        assert result["swing_low_body"].dtype in [pl.Float32, pl.Float64]

        # Legalább egy swing low pontnak kell lennie
        assert result["swing_low_body"].drop_nulls().len() > 0

    def test_process_swing_high_wick_detection(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a wick swing high pontok helyes detektálását."""
        result = processor.process(sample_ohlcv_data)

        # Swing high wick Float vagy None lehet
        assert result["swing_high_wick"].dtype in [pl.Float32, pl.Float64]

        # Legalább egy swing high pontnak kell lennie (a minta adatokban)
        assert result["swing_high_wick"].drop_nulls().len() > 0

    def test_process_swing_low_wick_detection(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a wick swing low pontok helyes detektálását."""
        result = processor.process(sample_ohlcv_data)

        # Swing low wick Float vagy None lehet
        assert result["swing_low_wick"].dtype in [pl.Float32, pl.Float64]

        # Legalább egy swing low pontnak kell lennie
        assert result["swing_low_wick"].drop_nulls().len() > 0

    def test_process_empty_dataframe(self, processor: D02SupportProcessor):
        """Teszteli a process metódust üres DataFrame-mel."""
        empty_df = pl.DataFrame(
            schema={
                "timestamp": pl.Datetime,
                "open": pl.Float64,
                "high": pl.Float64,
                "low": pl.Float64,
                "close": pl.Float64,
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

        # Új oszlopok jelen kell legyenek
        expected_columns = {
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "swing_high_body",
            "swing_low_body",
            "swing_high_wick",
            "swing_low_wick",
            "swing_high",
            "swing_low",
            "support_levels",
            "resistance_levels",
        }
        assert set(result.columns) == expected_columns

    def test_process_missing_columns_raises_error(self, processor: D02SupportProcessor):
        """Teszteli, hogy hiányzó oszlopok esetén ColumnNotFoundError-t dob."""
        # Hiányzó oszlopok (mid_high és high)
        incomplete_df = pl.DataFrame(
            {
                "timestamp": [datetime(2023, 1, 1, 9, 0, 0)],
                "open": [1.0500],
                # high hiányzik
                "low": [1.0480],
                "close": [1.0510],
                "mid_open": [1.0500],
                # mid_high hiányzik
                "mid_low": [1.0480],
                "mid_close": [1.0510],
                "tick_volume": [1000],
                "spread": [0.0002],
                "real_volume": [1500.0],
            }
        )

        # Polars ColumnNotFoundError-t dob hiányzó oszlopokra
        with pytest.raises(pl.exceptions.ColumnNotFoundError):
            processor.process(incomplete_df)

    def test_process_order_preserved(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli, hogy a sorok sorrendje megmarad."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük, hogy a timestamp oszlop sorrendje azonos
        assert result["timestamp"].equals(sample_ohlcv_data["timestamp"])

    def test_process_data_types_preserved(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli, hogy az adattípusok megmaradnak."""
        result = processor.process(sample_ohlcv_data)

        # Ellenőrizzük a fontos adattípusokat
        assert result["timestamp"].dtype == pl.Datetime
        assert result["open"].dtype in [pl.Float32, pl.Float64]
        assert result["high"].dtype in [pl.Float32, pl.Float64]
        assert result["low"].dtype in [pl.Float32, pl.Float64]
        assert result["close"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_open"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_high"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_low"].dtype in [pl.Float32, pl.Float64]
        assert result["mid_close"].dtype in [pl.Float32, pl.Float64]
        assert result["tick_volume"].dtype in [pl.Int32, pl.Int64]
        assert result["spread"].dtype in [pl.Float32, pl.Float64]
        assert result["real_volume"].dtype in [pl.Float32, pl.Float64]

        # Új oszlopok típusai
        assert result["swing_high_body"].dtype in [pl.Float32, pl.Float64]
        assert result["swing_low_body"].dtype in [pl.Float32, pl.Float64]
        assert result["swing_high_wick"].dtype in [pl.Float32, pl.Float64]
        assert result["swing_low_wick"].dtype in [pl.Float32, pl.Float64]

    def test_confirm_with_volume_enabled(
        self, processor: D02SupportProcessor, sample_ohlcv_data: pl.DataFrame
    ):
        """Teszteli a _confirm_with_volume metódust volume_confirmation True esetén."""
        # Swing mask: első 10 sor True, többi False
        swing_mask = pl.col("timestamp").cum_count() <= 10

        expr = processor._confirm_with_volume(sample_ohlcv_data, swing_mask)

        # Alkalmazzuk az expr-t a df-re
        result_df = sample_ohlcv_data.with_columns(volume_multiplier=expr)

        # Ellenőrizzük, hogy az első 10 sorban különböző értékek vannak (1.0 vagy 1.2)
        first_10 = result_df.head(10)["volume_multiplier"].to_list()
        others = result_df.slice(10)["volume_multiplier"].to_list()

        # Első 10-ben lehet 1.2 vagy 1.0 attól függően, hogy teljesül-e a feltétel
        assert all(v in [1.0, 1.2] for v in first_10)
        # Többi mindig 1.0 (swing_mask False)
        assert all(v == 1.0 for v in others)

    def test_confirm_with_volume_disabled(self, processor: D02SupportProcessor):
        """Teszteli a _confirm_with_volume metódust volume_confirmation False esetén."""
        # Mock config módosítása volume_confirmation False-ra
        processor.dim_config = {"volume_confirmation": False}

        df = pl.DataFrame({"real_volume": [1000, 2000, 3000]})
        swing_mask = pl.lit(True)

        expr = processor._confirm_with_volume(df, swing_mask)

        # Alkalmazzuk
        result_df = df.with_columns(volume_multiplier=expr)

        # Mindig 1.0 kell legyen
        assert all(result_df["volume_multiplier"] == 1.0)

    def test_merge_levels_empty_swings(self, processor: D02SupportProcessor):
        """Teszteli a _merge_levels metódust üres swing listával."""
        result = processor._merge_levels([])

        assert result == []

    def test_merge_levels_single_swing_high(self, processor: D02SupportProcessor):
        """Teszteli a _merge_levels metódust egyetlen high swing-gel."""
        swings = [{"price": 1.0500, "volume": 1000.0, "type": "high"}]
        result = processor._merge_levels(swings)

        expected = [{"price": 1.0500, "touches": 1, "type": "resistance", "strength": 1.0}]

        assert result == expected

    def test_merge_levels_single_swing_low(self, processor: D02SupportProcessor):
        """Teszteli a _merge_levels metódust egyetlen low swing-gel."""
        swings = [{"price": 1.0480, "volume": 1000.0, "type": "low"}]
        result = processor._merge_levels(swings)

        expected = [{"price": 1.0480, "touches": 1, "type": "support", "strength": 1.0}]

        assert result == expected

    def test_merge_levels_multiple_swings_no_merge(self, processor: D02SupportProcessor):
        """Teszteli a _merge_levels metódust több swing-gel, amelyek nem kerülnek összevonásra."""
        swings = [
            {"price": 1.0500, "volume": 1000.0, "type": "high"},
            {"price": 1.0520, "volume": 1000.0, "type": "high"},
            # Távolabb mint level_merge (0.0005)
            {"price": 1.0480, "volume": 1000.0, "type": "low"},
        ]
        result = processor._merge_levels(swings)

        expected = [
            {"price": 1.0480, "touches": 1, "type": "support", "strength": 1.0},
            {"price": 1.0500, "touches": 1, "type": "resistance", "strength": 1.0},
            {"price": 1.0520, "touches": 1, "type": "resistance", "strength": 1.0},
        ]

        assert result == expected

    def test_merge_levels_merge_close_swings(self, processor: D02SupportProcessor):
        """Teszteli a _merge_levels metódust közel lévő swing-ek összevonásával."""
        swings = [
            {"price": 1.0500, "volume": 1000.0, "type": "high"},
            {"price": 1.0502, "volume": 2000.0, "type": "high"},  # Közel, össze kell vonni
        ]
        result = processor._merge_levels(swings)

        # Súlyozott átlag számítása
        expected_price = (1.0500 * 1000 + 1.0502 * 2000) / 3000

        assert len(result) == 1
        assert result[0]["touches"] == 2
        assert result[0]["type"] == "resistance"
        assert result[0]["strength"] == 2.0
        assert abs(result[0]["price"] - expected_price) < 1e-6

    def test_merge_levels_sorted_by_price(self, processor: D02SupportProcessor):
        """Teszteli, hogy a swing-ek ár szerint rendezettek maradnak."""
        swings = [
            {"price": 1.0520, "volume": 1000.0, "type": "high"},
            {"price": 1.0480, "volume": 1000.0, "type": "low"},
            {"price": 1.0500, "volume": 1000.0, "type": "high"},
        ]
        result = processor._merge_levels(swings)

        # Rendezve kell lenni ár szerint
        prices = [level["price"] for level in result]
        assert prices == sorted(prices)
