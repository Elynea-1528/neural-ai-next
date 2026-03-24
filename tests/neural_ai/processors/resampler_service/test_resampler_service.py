"""ResamplerService unit tesztek - 100% coverage cél."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import polars as pl
import pytest

from neural_ai.processors.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)
from neural_ai.processors.resampler_service.implementations.resampler_service import (
    ResamplerService,
)


class TestResamplerServiceInitialization:
    """ResamplerService inicializálás tesztek."""

    def test_init_success(self, mock_storage: MagicMock, mock_logger: MagicMock) -> None:
        """Teszt: Sikeres inicializálás függőségekkel."""
        # Arrange & Act
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Assert
        assert resampler._storage == mock_storage
        assert resampler._logger == mock_logger


class TestResamplerServiceValidateTimeframe:
    """ResamplerService _validate_timeframe tesztek."""

    @pytest.mark.parametrize(
        "timeframe",
        ["tick", "1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"],
    )
    def test_validate_timeframe_valid(
        self, mock_storage: MagicMock, mock_logger: MagicMock, timeframe: str
    ) -> None:
        """Teszt: Érvényes timeframe-ek validálása."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act & Assert (nem dob hibát)
        resampler._validate_timeframe(timeframe)

    @pytest.mark.parametrize(
        "timeframe",
        ["2m", "10m", "invalid", "1s", ""],
    )
    def test_validate_timeframe_invalid(
        self, mock_storage: MagicMock, mock_logger: MagicMock, timeframe: str
    ) -> None:
        """Teszt: Érvénytelen timeframe-ek elutasítása."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act & Assert
        with pytest.raises(InvalidTimeframeError):
            resampler._validate_timeframe(timeframe)


class TestResamplerServiceLoadTickData:
    """ResamplerService _load_tick_data tesztek."""

    @pytest.mark.asyncio
    async def test_load_tick_data_success(
        self, mock_storage: MagicMock, mock_logger: MagicMock, sample_tick_df: pl.DataFrame
    ) -> None:
        """Teszt: Sikeres tick adat betöltés."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act
        result = await resampler._load_tick_data(symbol, start, end)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 1000
        mock_storage.read_tick_data.assert_called_once_with(symbol, start, end)

    @pytest.mark.asyncio
    async def test_load_tick_data_empty(
        self, mock_storage_empty: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Üres adat betöltés (warning log)."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage_empty, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act
        result = await resampler._load_tick_data(symbol, start, end)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0
        mock_logger.warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_tick_data_no_method(
        self, mock_storage_no_method: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Storage nem támogatja a read_tick_data metódust."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage_no_method, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(DataLoadError):
            await resampler._load_tick_data(symbol, start, end)

    @pytest.mark.asyncio
    async def test_load_tick_data_storage_exception(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Storage kivételt dob betöltéskor."""
        # Arrange
        mock_storage.read_tick_data = AsyncMock(side_effect=RuntimeError("Storage error"))
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(DataLoadError):
            await resampler._load_tick_data(symbol, start, end)


class TestResamplerServiceConvertToOHLCV:
    """ResamplerService _convert_to_ohlcv tesztek."""

    def test_convert_to_ohlcv_empty_dataframe(
        self, mock_storage: MagicMock, mock_logger: MagicMock, empty_tick_df: pl.DataFrame
    ) -> None:
        """Teszt: Üres DataFrame kezelése."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act
        result = resampler._convert_to_ohlcv(empty_tick_df, "1m")

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0
        expected_columns = [
            "timestamp",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "bid_open",
            "bid_high",
            "bid_low",
            "bid_close",
            "spread",
            "real_volume",
            "tick_volume",
            "bid_volume",
            "ask_volume",
        ]
        assert result.columns == expected_columns

    def test_convert_to_ohlcv_missing_columns(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Hiányzó oszlopok kezelése."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        invalid_df = pl.DataFrame({
            "timestamp": [datetime(2024, 1, 1)],
            "bid": [1.1000],
        })

        # Act & Assert
        with pytest.raises(ValueError, match="Missing required columns"):
            resampler._convert_to_ohlcv(invalid_df, "1m")

    def test_convert_to_ohlcv_tick_timeframe(
        self, mock_storage: MagicMock, mock_logger: MagicMock, sample_tick_df: pl.DataFrame
    ) -> None:
        """Teszt: Tick timeframe (bypass aggregáció)."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act
        result = resampler._convert_to_ohlcv(sample_tick_df, "tick")

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 1000  # Nincs aggregáció
        assert "mid_open" in result.columns
        assert "mid_close" in result.columns
        assert "spread" in result.columns
        assert "tick_volume" in result.columns
        # Tick volume mindig 1
        assert result["tick_volume"][0] == 1

    @pytest.mark.parametrize(
        "timeframe,expected_min_bars",
        [
            ("1m", 16),  # 1000 seconds / 60 = ~17 bars
            ("5m", 3),  # 1000 seconds / 300 = ~3 bars
            ("15m", 1),  # 1000 seconds / 900 = ~1 bar
        ],
    )
    def test_convert_to_ohlcv_different_timeframes(
        self,
        mock_storage: MagicMock,
        mock_logger: MagicMock,
        sample_tick_df: pl.DataFrame,
        timeframe: str,
        expected_min_bars: int,
    ) -> None:
        """Teszt: Különböző timeframe-ek aggregációja."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act
        result = resampler._convert_to_ohlcv(sample_tick_df, timeframe)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) >= expected_min_bars
        assert "mid_open" in result.columns
        assert "mid_high" in result.columns
        assert "mid_low" in result.columns
        assert "mid_close" in result.columns
        assert "bid_open" in result.columns
        assert "spread" in result.columns
        assert "real_volume" in result.columns
        assert "tick_volume" in result.columns

    def test_convert_to_ohlcv_1m_aggregation(
        self, mock_storage: MagicMock, mock_logger: MagicMock, sample_tick_df: pl.DataFrame
    ) -> None:
        """Teszt: 1m aggregáció részletes ellenőrzés."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)

        # Act
        result = resampler._convert_to_ohlcv(sample_tick_df, "1m")

        # Assert
        assert len(result) > 0
        # Ellenőrizzük az első gyertya értékeit (Polars row access)
        first_row = result.row(0, named=True)
        assert first_row["mid_open"] is not None
        assert first_row["mid_high"] >= first_row["mid_low"]
        assert first_row["bid_high"] >= first_row["bid_low"]
        assert first_row["spread"] > 0
        assert first_row["real_volume"] > 0
        assert first_row["tick_volume"] > 0


class TestResamplerServiceResample:
    """ResamplerService resample tesztek (fő metódus)."""

    @pytest.mark.asyncio
    async def test_resample_success_polars(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Sikeres resample Polars visszatérési típussal."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act
        result = await resampler.resample(
            symbol=symbol, start=start, end=end, timeframe="1m", return_type="polars"
        )

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_resample_success_pandas(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Sikeres resample Pandas visszatérési típussal."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act
        result = await resampler.resample(
            symbol=symbol, start=start, end=end, timeframe="1m", return_type="pandas"
        )

        # Assert
        # Pandas DataFrame ellenőrzés
        assert hasattr(result, "index")  # Pandas DataFrame jellemző
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_resample_invalid_timeframe(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Érvénytelen timeframe elutasítása."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(InvalidTimeframeError):
            await resampler.resample(
                symbol=symbol, start=start, end=end, timeframe="invalid"
            )

    @pytest.mark.asyncio
    async def test_resample_invalid_return_type(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Érvénytelen return_type elutasítása."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(ResamplingError):
            await resampler.resample(
                symbol=symbol, start=start, end=end, timeframe="1m", return_type="invalid"
            )

    @pytest.mark.asyncio
    async def test_resample_data_load_error(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Adat betöltési hiba kezelése."""
        # Arrange
        mock_storage.read_tick_data = AsyncMock(side_effect=RuntimeError("Storage error"))
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(DataLoadError):
            await resampler.resample(symbol=symbol, start=start, end=end, timeframe="1m")

    @pytest.mark.asyncio
    async def test_resample_conversion_error(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Konverziós hiba kezelése."""
        # Arrange
        # Hibás adatot ad vissza a storage (hiányzó oszlopok)
        invalid_df = pl.DataFrame({
            "timestamp": [datetime(2024, 1, 1)],
            "bid": [1.1000],
        })
        mock_storage.read_tick_data = AsyncMock(return_value=invalid_df)
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act & Assert
        with pytest.raises(ResamplingError):
            await resampler.resample(symbol=symbol, start=start, end=end, timeframe="1m")

    @pytest.mark.asyncio
    async def test_resample_default_timeframe(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Alapértelmezett timeframe (1m)."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)

        # Act
        result = await resampler.resample(symbol=symbol, start=start, end=end)

        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_resample_all_timeframes(
        self, mock_storage: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszt: Minden támogatott timeframe működik."""
        # Arrange
        resampler = ResamplerService(storage=mock_storage, logger=mock_logger)
        symbol = "EURUSD"
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 2)
        timeframes = ["tick", "1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"]

        # Act & Assert
        for timeframe in timeframes:
            result = await resampler.resample(
                symbol=symbol, start=start, end=end, timeframe=timeframe
            )
            assert isinstance(result, pl.DataFrame)
            assert len(result) >= 0  # Lehet üres is (pl. 1M esetén)
