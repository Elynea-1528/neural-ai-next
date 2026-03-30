"""Unit tesztek a D01PriceProcessor osztályhoz."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

import polars as pl

from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor


class TestD01PriceProcessor:
    """Tesztek a D01PriceProcessor osztályhoz."""

    def test_processor_initialization(self) -> None:
        """Ellenőrzi, hogy a processzor inicializálható."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()

        # Act
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Assert
        assert processor is not None
        assert processor.dimension_id == 1

    def test_dimension_id_is_one(self) -> None:
        """Ellenőrzi, hogy a dimension_id 1."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        dim_id = processor.dimension_id

        # Assert
        assert dim_id == 1

    def test_process_with_basic_dataframe(self) -> None:
        """Ellenőrzi a process metódust alapvető DataFrame-mel."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [
                    datetime(2024, 3, 20, 10, 0, tzinfo=UTC),
                    datetime(2024, 3, 20, 10, 1, tzinfo=UTC),
                    datetime(2024, 3, 20, 10, 2, tzinfo=UTC),
                ],
                "mid_open": [1.08500, 1.08510, 1.08520],
                "mid_high": [1.08520, 1.08530, 1.08540],
                "mid_low": [1.08490, 1.08500, 1.08510],
                "mid_close": [1.08510, 1.08520, 1.08530],
                "tick_volume": [100, 150, 120],
                "spread": [0.00020, 0.00020, 0.00020],
                "real_volume": [1000000, 1500000, 1200000],
            }
        )

        # Act
        result = processor.process(df)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert "timestamp" in result.columns
        assert "bid_open" in result.columns
        assert "ask_open" in result.columns
        assert "log_return" in result.columns
        assert "rolling_z_score" in result.columns

    def test_process_calculates_bid_ask_from_mid_and_spread(self) -> None:
        """Ellenőrzi, hogy a bid/ask értékek helyesen számítódnak."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [datetime(2024, 3, 20, 10, 0, tzinfo=UTC)],
                "mid_open": [1.08500],
                "mid_high": [1.08520],
                "mid_low": [1.08490],
                "mid_close": [1.08510],
                "tick_volume": [100],
                "spread": [0.00020],
                "real_volume": [1000000],
            }
        )

        # Act
        result = processor.process(df)

        # Assert
        bid_open = result["bid_open"][0]
        ask_open = result["ask_open"][0]
        assert abs(bid_open - 1.08490) < 0.00001  # mid - spread/2
        assert abs(ask_open - 1.08510) < 0.00001  # mid + spread/2

    def test_process_with_custom_z_score_window(self) -> None:
        """Ellenőrzi a process metódust egyedi z_score_window-val."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {"z_score_window": 30}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [
                    datetime(2024, 3, 20, 10, i, tzinfo=UTC) for i in range(50)
                ],
                "mid_open": [1.08500 + i * 0.00001 for i in range(50)],
                "mid_high": [1.08520 + i * 0.00001 for i in range(50)],
                "mid_low": [1.08490 + i * 0.00001 for i in range(50)],
                "mid_close": [1.08510 + i * 0.00001 for i in range(50)],
                "tick_volume": [100] * 50,
                "spread": [0.00020] * 50,
                "real_volume": [1000000] * 50,
            }
        )

        # Act
        result = processor.process(df)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert "rolling_z_score" in result.columns

    def test_process_with_tick_timeframe(self) -> None:
        """Ellenőrzi a process metódust tick timeframe-mel."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {"calc_shadows": True}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [datetime(2024, 3, 20, 10, 0, tzinfo=UTC)],
                "mid_open": [1.08500],
                "mid_high": [1.08520],
                "mid_low": [1.08490],
                "mid_close": [1.08510],
                "tick_volume": [100],
                "spread": [0.00020],
                "real_volume": [1000000],
                "bid": [1.08490],
                "ask": [1.08510],
            }
        )

        # Act
        result = processor.process(df, timeframe="tick")

        # Assert
        assert isinstance(result, pl.DataFrame)
        # Tick timeframe esetén az árnyékok None-ok
        assert result["upper_shadow"][0] is None
        assert result["lower_shadow"][0] is None

    def test_process_calculates_shadows_for_non_tick_timeframe(self) -> None:
        """Ellenőrzi, hogy az árnyékok számítódnak nem-tick timeframe esetén."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {"calc_shadows": True}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [datetime(2024, 3, 20, 10, 0, tzinfo=UTC)],
                "mid_open": [1.08500],
                "mid_high": [1.08530],
                "mid_low": [1.08480],
                "mid_close": [1.08520],
                "tick_volume": [100],
                "spread": [0.00020],
                "real_volume": [1000000],
            }
        )

        # Act
        result = processor.process(df, timeframe="1m")

        # Assert
        assert result["upper_shadow"][0] is not None
        assert result["lower_shadow"][0] is not None

    def test_process_with_existing_bid_ask_columns(self) -> None:
        """Ellenőrzi, hogy a meglévő bid/ask oszlopokat használja."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [datetime(2024, 3, 20, 10, 0, tzinfo=UTC)],
                "mid_open": [1.08500],
                "mid_high": [1.08520],
                "mid_low": [1.08490],
                "mid_close": [1.08510],
                "bid_open": [1.08480],
                "bid_high": [1.08500],
                "bid_low": [1.08470],
                "bid_close": [1.08490],
                "ask_open": [1.08520],
                "ask_high": [1.08540],
                "ask_low": [1.08510],
                "ask_close": [1.08530],
                "tick_volume": [100],
                "spread": [0.00020],
                "real_volume": [1000000],
            }
        )

        # Act
        result = processor.process(df)

        # Assert
        assert result["bid_open"][0] == 1.08480
        assert result["ask_open"][0] == 1.08520

    def test_process_logs_debug_message(self) -> None:
        """Ellenőrzi, hogy a process metódus naplóz."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = D01PriceProcessor(mock_config, mock_logger)

        df = pl.DataFrame(
            {
                "timestamp": [datetime(2024, 3, 20, 10, 0, tzinfo=UTC)],
                "mid_open": [1.08500],
                "mid_high": [1.08520],
                "mid_low": [1.08490],
                "mid_close": [1.08510],
                "tick_volume": [100],
                "spread": [0.00020],
                "real_volume": [1000000],
            }
        )

        # Act
        processor.process(df, timeframe="5m")

        # Assert
        mock_logger.debug.assert_called()
