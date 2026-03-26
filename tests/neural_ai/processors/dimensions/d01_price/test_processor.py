"""Unit tesztek a D01PriceProcessor osztályhoz."""

from unittest.mock import MagicMock

import polars as pl
import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor


@pytest.fixture
def mock_config() -> MagicMock:
    """Mock ConfigManagerInterface fixture."""
    config = MagicMock(spec=ConfigManagerInterface)
    config.get.return_value = {
        "z_score_window": 60,
        "calc_shadows": True,
        "market_hours": {"enabled": False},
    }
    return config


@pytest.fixture
def mock_logger() -> MagicMock:
    """Mock LoggerInterface fixture."""
    return MagicMock(spec=LoggerInterface)


@pytest.fixture
def sample_ohlcv_data() -> pl.DataFrame:
    """Minta OHLCV adat fixture."""
    return pl.DataFrame(
        {
            "timestamp": pl.datetime_range(
                start=pl.datetime(2024, 1, 1, 0, 0),
                end=pl.datetime(2024, 1, 1, 0, 4),
                interval="1m",
                eager=True,
            ),
            "mid_open": [1.1000, 1.1010, 1.1020, 1.1030, 1.1040],
            "mid_high": [1.1015, 1.1025, 1.1035, 1.1045, 1.1055],
            "mid_low": [1.0995, 1.1005, 1.1015, 1.1025, 1.1035],
            "mid_close": [1.1010, 1.1020, 1.1030, 1.1040, 1.1050],
            "tick_volume": [100, 150, 200, 180, 220],
            "spread": [0.0002, 0.0002, 0.0002, 0.0002, 0.0002],
            "real_volume": [1000.0, 1500.0, 2000.0, 1800.0, 2200.0],
        }
    )


class TestD01PriceProcessorInitialization:
    """D01PriceProcessor inicializálás tesztjei."""

    def test_init_success(self, mock_config: MagicMock, mock_logger: MagicMock) -> None:
        """Sikeres inicializálás tesztje."""
        # Arrange & Act
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Assert
        assert processor.config == mock_config
        assert processor.logger == mock_logger
        assert processor.dimension_id == 1

    def test_dimension_id_property(self, mock_config: MagicMock, mock_logger: MagicMock) -> None:
        """Dimenzió ID property tesztje."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        dim_id = processor.dimension_id

        # Assert
        assert dim_id == 1
        assert isinstance(dim_id, int)


class TestD01PriceProcessorProcess:
    """D01PriceProcessor process metódus tesztjei."""

    def test_process_happy_path(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Process metódus normál működés tesztje."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == len(sample_ohlcv_data)
        assert "timestamp" in result.columns
        assert "log_return" in result.columns
        assert "rolling_z_score" in result.columns
        assert "upper_shadow" in result.columns
        assert "lower_shadow" in result.columns

    def test_process_calculates_log_return(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Log return számítás tesztje."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "log_return" in result.columns
        # Első sor None (nincs előző érték)
        assert result["log_return"][0] is None or result["log_return"][0] != result["log_return"][0]
        # Második sortól van érték
        assert result["log_return"][1] is not None

    def test_process_calculates_bid_ask_from_spread(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Bid/Ask számítás spread alapján tesztje."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "bid_open" in result.columns
        assert "bid_close" in result.columns
        assert "ask_open" in result.columns
        assert "ask_close" in result.columns

        # Ellenőrizzük a számítást: bid = mid - spread/2
        expected_bid_close = sample_ohlcv_data["mid_close"][0] - (
            sample_ohlcv_data["spread"][0] / 2
        )
        assert abs(result["bid_close"][0] - expected_bid_close) < 1e-6

    def test_process_calculates_shadows_for_ohlc(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Árnyékok számítása OHLC timeframe esetén."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "upper_shadow" in result.columns
        assert "lower_shadow" in result.columns
        # Nem None értékek (OHLC timeframe)
        assert result["upper_shadow"][0] is not None

    def test_process_no_shadows_for_tick_timeframe(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Árnyékok NEM számítása tick timeframe esetén."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="tick")

        # Assert
        assert "upper_shadow" in result.columns
        assert "lower_shadow" in result.columns
        # None értékek (tick timeframe)
        assert result["upper_shadow"][0] is None

    def test_process_with_custom_z_score_window(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Egyedi Z-score ablak használata."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 30,
            "calc_shadows": True,
            "market_hours": {"enabled": False},
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "rolling_z_score" in result.columns
        # Ellenőrizzük, hogy a logger debug hívódott
        mock_logger.debug.assert_called()

    def test_process_with_timeframe_specific_config(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Timeframe specifikus konfiguráció használata."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 60,
            "calc_shadows": True,
            "market_hours": {"enabled": False},
            "timeframe_configs": {"1m": {"z_score_window": 20}},
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "rolling_z_score" in result.columns
        assert len(result) == len(sample_ohlcv_data)

    def test_process_preserves_existing_bid_ask_columns(
        self, mock_config: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Meglévő bid/ask oszlopok megőrzése."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)
        data_with_bid_ask = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 0, 0),
                    end=pl.datetime(2024, 1, 1, 0, 2),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000, 1.1010, 1.1020],
                "mid_high": [1.1015, 1.1025, 1.1035],
                "mid_low": [1.0995, 1.1005, 1.1015],
                "mid_close": [1.1010, 1.1020, 1.1030],
                "bid_open": [1.0999, 1.1009, 1.1019],
                "bid_high": [1.1014, 1.1024, 1.1034],
                "bid_low": [1.0994, 1.1004, 1.1014],
                "bid_close": [1.1009, 1.1019, 1.1029],
                "ask_open": [1.1001, 1.1011, 1.1021],
                "ask_high": [1.1016, 1.1026, 1.1036],
                "ask_low": [1.0996, 1.1006, 1.1016],
                "ask_close": [1.1011, 1.1021, 1.1031],
                "tick_volume": [100, 150, 200],
                "spread": [0.0002, 0.0002, 0.0002],
                "real_volume": [1000.0, 1500.0, 2000.0],
            }
        )

        # Act
        result = processor.process(data_with_bid_ask, timeframe="1m")

        # Assert
        assert "bid_open" in result.columns
        assert "ask_open" in result.columns
        # Ellenőrizzük, hogy az eredeti értékek megmaradtak
        assert result["bid_open"][0] == 1.0999


class TestD01PriceProcessorEdgeCases:
    """D01PriceProcessor edge case tesztek."""

    def test_process_with_empty_dataframe(
        self, mock_config: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Üres DataFrame kezelése."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)
        empty_df = pl.DataFrame(
            {
                "timestamp": [],
                "mid_open": [],
                "mid_high": [],
                "mid_low": [],
                "mid_close": [],
                "tick_volume": [],
                "spread": [],
                "real_volume": [],
            }
        )

        # Act
        result = processor.process(empty_df, timeframe="1m")

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0

    def test_process_with_single_row(
        self, mock_config: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Egyetlen sor kezelése."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)
        single_row_df = pl.DataFrame(
            {
                "timestamp": [pl.datetime(2024, 1, 1, 0, 0)],
                "mid_open": [1.1000],
                "mid_high": [1.1015],
                "mid_low": [1.0995],
                "mid_close": [1.1010],
                "tick_volume": [100],
                "spread": [0.0002],
                "real_volume": [1000.0],
            }
        )

        # Act
        result = processor.process(single_row_df, timeframe="1m")

        # Assert
        assert len(result) == 1
        assert "log_return" in result.columns
        # Első sor log_return None (nincs előző érték)
        assert result["log_return"][0] is None or result["log_return"][0] != result["log_return"][0]

    def test_process_with_calc_shadows_disabled(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Árnyék számítás kikapcsolva."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 60,
            "calc_shadows": False,
            "market_hours": {"enabled": False},
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "upper_shadow" in result.columns
        assert "lower_shadow" in result.columns
        # None értékek (calc_shadows = False)
        assert result["upper_shadow"][0] is None


class TestD01PriceProcessorMarketHours:
    """D01PriceProcessor market hours szűrés tesztjei."""

    def test_process_with_market_hours_disabled(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Market hours szűrés kikapcsolva."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 60,
            "calc_shadows": True,
            "market_hours": {"enabled": False},
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert len(result) == len(sample_ohlcv_data)
        # Logger info NEM hívódott (market hours disabled)
        mock_logger.info.assert_not_called()

    def test_process_with_market_hours_enabled_no_filtering(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Market hours szűrés bekapcsolva, de nincs szűrés (minden adat market hours-ban)."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 60,
            "calc_shadows": True,
            "market_hours": {
                "enabled": True,
                "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "hours": ["00:00", "23:59"],
                "timezone": "UTC",
                "log_filtering": True,
            },
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert len(result) == len(sample_ohlcv_data)

    def test_process_with_market_hours_logging_triggered(
        self, mock_config: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Market hours szűrés logging aktiválása hétvégi adatokkal."""
        # Arrange
        mock_config.get.return_value = {
            "z_score_window": 60,
            "calc_shadows": True,
            "market_hours": {
                "enabled": True,
                "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "hours": ["09:00", "17:00"],
                "timezone": "UTC",
                "log_filtering": True,
            },
        }
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Hétvégi adatok (szombat)
        weekend_data = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 6, 8, 0),  # Szombat 08:00
                    end=pl.datetime(2024, 1, 6, 8, 4),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000, 1.1010, 1.1020, 1.1030, 1.1040],
                "mid_high": [1.1015, 1.1025, 1.1035, 1.1045, 1.1055],
                "mid_low": [1.0995, 1.1005, 1.1015, 1.1025, 1.1035],
                "mid_close": [1.1010, 1.1020, 1.1030, 1.1040, 1.1050],
                "tick_volume": [100, 150, 200, 180, 220],
                "spread": [0.0002, 0.0002, 0.0002, 0.0002, 0.0002],
                "real_volume": [1000.0, 1500.0, 2000.0, 1800.0, 2200.0],
            }
        )

        # Act
        result = processor.process(weekend_data, timeframe="1m")

        # Assert
        assert len(result) == len(weekend_data)
        # Logger info hívódott (market hours outside)
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        assert "Market hours szűrés eredménye" in call_args[0]


class TestD01PriceProcessorTickColumns:
    """D01PriceProcessor tick oszlopok kezelése tesztjei."""

    def test_process_with_tick_columns(
        self, mock_config: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Tick oszlopok hozzáadása, ha rendelkezésre állnak."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)
        tick_data = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    start=pl.datetime(2024, 1, 1, 0, 0),
                    end=pl.datetime(2024, 1, 1, 0, 2),
                    interval="1m",
                    eager=True,
                ),
                "mid_open": [1.1000, 1.1010, 1.1020],
                "mid_high": [1.1015, 1.1025, 1.1035],
                "mid_low": [1.0995, 1.1005, 1.1015],
                "mid_close": [1.1010, 1.1020, 1.1030],
                "tick_volume": [100, 150, 200],
                "spread": [0.0002, 0.0002, 0.0002],
                "real_volume": [1000.0, 1500.0, 2000.0],
                "bid": [1.0999, 1.1009, 1.1019],
                "ask": [1.1001, 1.1011, 1.1021],
                "bid_volume": [50, 75, 100],
                "ask_volume": [50, 75, 100],
            }
        )

        # Act
        result = processor.process(tick_data, timeframe="tick")

        # Assert
        assert "bid" in result.columns
        assert "ask" in result.columns
        assert "bid_volume" in result.columns
        assert "ask_volume" in result.columns
        assert result["bid"][0] == 1.0999
        assert result["ask"][0] == 1.1001

    def test_process_without_tick_columns(
        self, mock_config: MagicMock, mock_logger: MagicMock, sample_ohlcv_data: pl.DataFrame
    ) -> None:
        """Tick oszlopok hiánya nem okoz hibát."""
        # Arrange
        processor = D01PriceProcessor(mock_config, mock_logger)

        # Act
        result = processor.process(sample_ohlcv_data, timeframe="1m")

        # Assert
        assert "bid" not in result.columns
        assert "ask" not in result.columns
        assert "bid_volume" not in result.columns
        assert "ask_volume" not in result.columns
