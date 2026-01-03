"""ResamplerService tesztek."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import polars as pl
import pytest

from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)
from neural_ai.core.processing.resampler_service.factory import ResamplerServiceFactory
from neural_ai.core.processing.resampler_service.implementations.resampler_service import (
    ResamplerService,
)
from neural_ai.core.processing.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)


class TestResamplerService:
    """ResamplerService tesztek."""

    @pytest.fixture
    def mock_storage(self) -> MagicMock:
        """Mock StorageInterface létrehozása."""
        return MagicMock()

    @pytest.fixture
    def resampler(self, mock_storage: MagicMock) -> ResamplerService:
        """ResamplerService példány létrehozása."""
        return ResamplerService(storage=mock_storage)

    @pytest.fixture
    def sample_tick_data(self) -> pl.DataFrame:
        """Minta tick adatok létrehozása."""
        # 10 másodperc adatok 1 másodperces frekvenciával
        date_range = pd.date_range(
            start=datetime(2024, 1, 1, 12, 0, 0), end=datetime(2024, 1, 1, 12, 0, 10), freq="1s"
        )

        return pl.DataFrame(
            {
                "timestamp": date_range,
                "bid": [1.05 + i * 0.001 for i in range(len(date_range))],
                "ask": [1.051 + i * 0.001 for i in range(len(date_range))],
                "volume": [100 + i * 10 for i in range(len(date_range))],
            }
        )

    @pytest.mark.asyncio
    async def test_resample_valid_timeframe(
        self, resampler: ResamplerService, sample_tick_data: pl.DataFrame
    ):
        """Teszt érvényes időkerettel."""
        # Mock a _load_tick_data metódust
        resampler._load_tick_data = AsyncMock(return_value=sample_tick_data)

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        result = await resampler.resample(symbol="EURUSD", start=start, end=end, timeframe="1m")

        # Ellenőrzés
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns

    @pytest.mark.asyncio
    async def test_resample_invalid_timeframe(self, resampler: ResamplerService):
        """Teszt érvénytelen időkerettel."""
        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        with pytest.raises(InvalidTimeframeError):
            await resampler.resample(symbol="EURUSD", start=start, end=end, timeframe="invalid")

    @pytest.mark.asyncio
    async def test_resample_data_load_error(self, resampler: ResamplerService):
        """Teszt adatok betöltési hibájával."""
        # Mock a _load_tick_data metódust, hogy dobjon kivételt
        resampler._load_tick_data = AsyncMock(side_effect=Exception("Betöltési hiba"))

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        with pytest.raises(DataLoadError):
            await resampler.resample(symbol="EURUSD", start=start, end=end, timeframe="1m")

    @pytest.mark.asyncio
    async def test_resample_resampling_error(
        self, resampler: ResamplerService, sample_tick_data: pl.DataFrame
    ):
        """Teszt átalakítási hibával."""
        # Mock a _load_tick_data metódust
        resampler._load_tick_data = AsyncMock(return_value=sample_tick_data)

        # Mock a _convert_to_ohlcv metódust, hogy dobjon kivételt
        resampler._convert_to_ohlcv = MagicMock(side_effect=Exception("Átalakítási hiba"))

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        with pytest.raises(ResamplingError):
            await resampler.resample(symbol="EURUSD", start=start, end=end, timeframe="1m")

    @pytest.mark.asyncio
    async def test_resample_different_timeframes(
        self, resampler: ResamplerService, sample_tick_data: pl.DataFrame
    ):
        """Teszt különböző időkeretekkel."""
        resampler._load_tick_data = AsyncMock(return_value=sample_tick_data)

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        timeframes = ["1m", "5m", "15m", "1h"]

        for timeframe in timeframes:
            result = await resampler.resample(
                symbol="EURUSD", start=start, end=end, timeframe=timeframe
            )

            assert isinstance(result, pd.DataFrame)
            assert len(result.columns) == 5  # OHLCV

    def test_validate_timeframe_valid(self, resampler: ResamplerService):
        """Teszt érvényes időkeret validálását."""
        valid_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"]

        for timeframe in valid_timeframes:
            # Nem dob kivételt
            resampler._validate_timeframe(timeframe)

    def test_validate_timeframe_invalid(self, resampler: ResamplerService):
        """Teszt érvénytelen időkeret validálását."""
        with pytest.raises(InvalidTimeframeError):
            resampler._validate_timeframe("invalid_timeframe")

    def test_convert_to_ohlcv(self, resampler: ResamplerService, sample_tick_data: pl.DataFrame):
        """Teszt OHLCV átalakítást."""
        result = resampler._convert_to_ohlcv(sample_tick_data, "1m")

        # Ellenőrzés
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert all(col in result.columns for col in ["open", "high", "low", "close", "volume"])
        assert result.index.name == "timestamp" or result.index.name is None

    def test_convert_to_ohlcv_empty_data(self, resampler: ResamplerService):
        """Teszt üres adatokkal."""
        # Üres DataFrame létrehozása megfelelő sémával
        empty_data = pl.DataFrame(
            {
                "timestamp": pl.Series([], dtype=pl.Datetime),
                "bid": pl.Series([], dtype=pl.Float64),
                "ask": pl.Series([], dtype=pl.Float64),
                "volume": pl.Series([], dtype=pl.Int64),
            }
        )

        result = resampler._convert_to_ohlcv(empty_data, "1m")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_resample_ohlcv_calculation(
        self, resampler: ResamplerService, sample_tick_data: pl.DataFrame
    ):
        """Teszt OHLCV számítás helyességét."""
        resampler._load_tick_data = AsyncMock(return_value=sample_tick_data)

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        result = await resampler.resample(symbol="EURUSD", start=start, end=end, timeframe="1m")

        # Ellenőrzés, hogy az OHLCV értékek logikailag helyesek-e
        for _, row in result.iterrows():
            assert row["high"] >= row["low"], "High nem lehet kisebb mint Low"
            assert row["open"] >= row["low"], "Open nem lehet kisebb mint Low"
            assert row["close"] >= row["low"], "Close nem lehet kisebb mint Low"
            assert row["high"] >= row["open"], "High nem lehet kisebb mint Open"
            assert row["high"] >= row["close"], "High nem lehet kisebb mint Close"
            assert row["volume"] >= 0, "Volume nem lehet negatív"


class TestResamplerServiceFactory:
    """ResamplerServiceFactory tesztek."""

    def test_create(self):
        """Teszt ResamplerService létrehozását."""
        mock_storage = MagicMock()
        resampler = ResamplerServiceFactory.create(storage=mock_storage)

        assert isinstance(resampler, ResamplerInterface)
        assert isinstance(resampler, ResamplerService)

    @patch("neural_ai.core.processing.resampler_service.factory.DIContainer")
    @patch("neural_ai.core.storage.factory.StorageFactory.get_storage")
    def test_get_instance(self, mock_get_storage: MagicMock, mock_container_class: MagicMock):
        """Teszt ResamplerService példány lekérését."""
        # Mock a DI konténert
        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        # Mock a get metódust, hogy dobjon kivételt (nincs regisztrálva)
        mock_container.get.side_effect = Exception("Nincs regisztrálva")

        # Mock a storage factory-t
        mock_storage = MagicMock()
        mock_get_storage.return_value = mock_storage

        # Teszt
        resampler = ResamplerServiceFactory.get_instance()

        assert isinstance(resampler, ResamplerInterface)
        mock_container.register.assert_called_once()

    @patch("neural_ai.core.processing.resampler_service.factory.DIContainer")
    def test_get_instance_cached(self, mock_container_class: MagicMock):
        """Teszt gyorsítótárazott példány lekérését."""
        # Mock a DI konténert
        mock_container = MagicMock()
        mock_container_class.return_value = mock_container

        # Mock a get metódust, hogy visszaadjon egy példányt
        mock_resampler = MagicMock()
        mock_container.get.return_value = mock_resampler

        # Teszt
        resampler = ResamplerServiceFactory.get_instance()

        assert resampler == mock_resampler
        mock_container.register.assert_not_called()


class TestResamplerErrorHierarchy:
    """ResamplerError hierarchia tesztek."""

    def test_resampler_error_creation(self):
        """Teszt ResamplerError létrehozását."""
        from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
            ResamplerError,
        )

        error = ResamplerError(
            message="Teszt hiba",
            details="Részletes információk",
            original_error=ValueError("Eredeti hiba"),
        )

        assert str(error) == "Teszt hiba"
        assert error.details == "Részletes információk"
        assert error.component == "ResamplerService"
        assert isinstance(error.original_error, ValueError)

    def test_data_load_error_creation(self):
        """Teszt DataLoadError létrehozását."""
        original_error = OSError("Fájl nem található")

        error = DataLoadError(
            symbol="EURUSD",
            start="2024-01-01 12:00:00",
            end="2024-01-01 13:00:00",
            original_error=original_error,
        )

        assert "EURUSD" in str(error)
        assert error.details is not None
        assert "2024-01-01 12:00:00" in error.details
        assert error.original_error == original_error

    def test_resampling_error_creation(self):
        """Teszt ResamplingError létrehozását."""
        original_error = RuntimeError("Feldolgozási hiba")

        error = ResamplingError(symbol="EURUSD", timeframe="1m", original_error=original_error)

        assert "EURUSD" in str(error)
        assert error.details is not None
        assert "1m" in error.details
        assert error.original_error == original_error

    def test_invalid_timeframe_error_creation(self):
        """Teszt InvalidTimeframeError létrehozását."""
        error = InvalidTimeframeError("invalid_tf")

        assert "invalid_tf" in str(error)
        assert error.details is not None
        assert "Pandas offset formátum" in error.details
