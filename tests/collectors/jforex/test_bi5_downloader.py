"""Tests for Bi5Downloader implementation."""

import lzma
import struct
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any

import pytest

from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader
from neural_ai.collectors.jforex.interfaces.tick_data import TickData
from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DownloadError,
    DecodeError,
    DataNotAvailableError
)


class MockBi5DataGenerator:
    """Mock .bi5 data generator for testing."""
    
    @staticmethod
    def generate_mock_bi5_data(
        symbol: str,
        date: datetime,
        num_ticks: int = 100
    ) -> bytes:
        """Generate mock .bi5 data for testing.
        
        Args:
            symbol: Trading symbol
            date: Date for which to generate data
            num_ticks: Number of ticks to generate
            
        Returns:
            LZMA compressed .bi5 binary data
        """
        # Base timestamp: start of the day in milliseconds
        base_timestamp = int(date.replace(
            hour=0, minute=0, second=0, microsecond=0
        ).timestamp()) * 1000
        
        # Generate mock tick data
        raw_data = bytearray()
        base_price = 1.10000  # EURUSD base price
        
        for i in range(num_ticks):
            # Timestamp delta (1 second intervals)
            timestamp_delta = i * 1000
            
            # Generate prices with small variations
            bid = base_price + (i * 0.00001)  # Slight upward trend
            ask = bid + 0.00010  # 1 pip spread
            
            # Convert to integer format (multiplied by 100,000)
            bid_int = int(bid * 100000)
            ask_int = int(ask * 100000)
            
            # Pack as big-endian: unsigned int, unsigned int, unsigned int
            raw_data.extend(struct.pack('>III', timestamp_delta, ask_int, bid_int))
        
        # LZMA compress
        compressed = lzma.compress(bytes(raw_data))
        
        return compressed


class TestBi5Downloader:
    """Test suite for Bi5Downloader."""
    
    @pytest.fixture
    def mock_logger(self) -> MagicMock:
        """Create mock logger."""
        return MagicMock()
    
    @pytest.fixture
    def mock_event_bus(self) -> AsyncMock:
        """Create mock event bus."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_config(self) -> MagicMock:
        """Create mock config."""
        config = MagicMock()
        config.get.return_value = "https://test.dukascopy.com/datafeed"
        return config
    
    @pytest.fixture
    def mock_http_client(self) -> MagicMock:
        """Create mock HTTP client."""
        return MagicMock()
    
    @pytest.fixture
    def downloader(
        self,
        mock_logger: MagicMock,
        mock_event_bus: MagicMock,
        mock_config: MagicMock,
        mock_http_client: MagicMock
    ) -> Bi5Downloader:
        """Create Bi5Downloader instance for testing."""
        return Bi5Downloader(
            logger=mock_logger,
            event_bus=mock_event_bus,
            config=mock_config,
            http_client=mock_http_client
        )
    
    def test_init(
        self,
        mock_logger: MagicMock,
        mock_event_bus: MagicMock,
        mock_config: MagicMock,
        mock_http_client: MagicMock
    ) -> None:
        """Test Bi5Downloader initialization."""
        downloader = Bi5Downloader(
            logger=mock_logger,
            event_bus=mock_event_bus,
            config=mock_config,
            http_client=mock_http_client
        )
        
        assert downloader._logger == mock_logger
        assert downloader._event_bus == mock_event_bus
        assert downloader._config == mock_config
        assert downloader._http_client == mock_http_client
        assert downloader._base_url == "https://test.dukascopy.com/datafeed"
        mock_config.get.assert_called_once_with(
            "jforex.base_url",
            "https://www.dukascopy.com/datafeed"
        )
    
    def test_build_url(self, downloader: Bi5Downloader) -> None:
        """Test URL building for Dukascopy download."""
        date = datetime(2023, 12, 1, 10, 0, 0, tzinfo=timezone.utc)
        url = downloader._build_url("EURUSD", date)
        
        # Dukascopy uses 0-indexed months (11 for December)
        expected = (
            "https://test.dukascopy.com/datafeed/EURUSD/"
            "2023/11/01/10h_ticks.bi5"
        )
        assert url == expected
    
    def test_build_url_lowercase_symbol(self, downloader: Bi5Downloader) -> None:
        """Test URL building with lowercase symbol."""
        date = datetime(2023, 12, 1, 10, 0, 0, tzinfo=timezone.utc)
        url = downloader._build_url("eurusd", date)
        
        # Symbol should be uppercased
        assert "EURUSD" in url
    
    @pytest.mark.asyncio
    async def test_download_binary_success(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test successful binary download."""
        # Setup mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"test_data")
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_http_client.get.return_value = mock_response
        
        # Test download
        data = await downloader._download_binary("http://test.url")
        
        assert data == b"test_data"
        mock_http_client.get.assert_called_once_with("http://test.url")
        downloader._logger.debug.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_download_binary_404_error(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test 404 error handling (data not available)."""
        # Setup 404 response
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_http_client.get.return_value = mock_response
        
        # Test that DataNotAvailableError is raised
        with pytest.raises(DataNotAvailableError):
            await downloader._download_binary("http://test.url")
        
        downloader._logger.warning.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_download_binary_network_error(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test network error handling."""
        # Setup network error
        mock_http_client.get.side_effect = Exception("Network error")
        
        # Test that DownloadError is raised
        with pytest.raises(DownloadError):
            await downloader._download_binary("http://test.url")
        
        downloader._logger.error.assert_called_once()
    
    def test_process_bi5_data_success(self, downloader: Bi5Downloader) -> None:
        """Test successful .bi5 data processing."""
        # Generate mock data
        date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        mock_data = MockBi5DataGenerator.generate_mock_bi5_data(
            "EURUSD",
            date,
            num_ticks=10
        )
        
        # Process data
        ticks = downloader._process_bi5_data(mock_data, "EURUSD", date)
        
        # Verify results
        assert len(ticks) == 10
        assert all(isinstance(tick, TickData) for tick in ticks)
        assert ticks[0].symbol == "EURUSD"
        assert ticks[0].bid < ticks[0].ask  # Spread check
        assert ticks[0].timestamp.tzinfo == timezone.utc
        
        # Verify price progression
        for i in range(1, len(ticks)):
            assert ticks[i].bid > ticks[i-1].bid  # Upward trend
        
        downloader._logger.debug.assert_called_once()
    
    def test_process_bi5_data_corrupted(self, downloader: Bi5Downloader) -> None:
        """Test corrupted .bi5 data handling."""
        date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        # Invalid LZMA data
        corrupted_data = b"invalid_lzma_data"
        
        # Test that DecodeError is raised
        with pytest.raises(DecodeError):
            downloader._process_bi5_data(corrupted_data, "EURUSD", date)
        
        downloader._logger.error.assert_called_once()
    
    def test_validate_bi5_data_valid(self, downloader: Bi5Downloader) -> None:
        """Test validation of valid .bi5 data."""
        # Generate valid mock data
        date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        valid_data = MockBi5DataGenerator.generate_mock_bi5_data(
            "EURUSD",
            date,
            num_ticks=10
        )
        
        # Validate
        result = downloader.validate_bi5_data(valid_data)
        
        assert result is True
    
    def test_validate_bi5_data_too_small(self, downloader: Bi5Downloader) -> None:
        """Test validation of data that's too small."""
        # Data too small
        small_data = b"12345678"
        
        # Validate
        result = downloader.validate_bi5_data(small_data)
        
        assert result is False
        downloader._logger.warning.assert_called_once()
    
    def test_validate_bi5_data_invalid_records(self, downloader: Bi5Downloader) -> None:
        """Test validation of data with invalid record count."""
        # Create data that doesn't decompress to multiple of 12
        invalid_data = lzma.compress(b"12345678901")  # 11 bytes
        
        # Validate
        result = downloader.validate_bi5_data(invalid_data)
        
        assert result is False
        downloader._logger.warning.assert_called_once()
    
    def test_validate_bi5_data_corrupted(self, downloader: Bi5Downloader) -> None:
        """Test validation of corrupted LZMA data."""
        # Invalid LZMA data
        corrupted_data = b"invalid_lzma_data"
        
        # Validate
        result = downloader.validate_bi5_data(corrupted_data)
        
        assert result is False
        downloader._logger.error.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_publish_ticks_empty(self, downloader: Bi5Downloader) -> None:
        """Test publishing empty tick list."""
        await downloader._publish_ticks([])
        
        # Should not publish anything
        downloader._event_bus.publish.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_publish_ticks_single_batch(self, downloader: Bi5Downloader) -> None:
        """Test publishing ticks in single batch."""
        # Create mock ticks (less than batch size)
        date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        ticks = [
            TickData(
                timestamp=date + timedelta(seconds=i),
                symbol="EURUSD",
                bid=1.10000 + i * 0.00001,
                ask=1.10010 + i * 0.00001,
                source="jforex"
            )
            for i in range(5)
        ]
        
        # Publish
        await downloader._publish_ticks(ticks)
        
        # Should publish once
        downloader._event_bus.publish.assert_called_once()
        downloader._logger.debug.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_publish_ticks_multiple_batches(self, downloader: Bi5Downloader) -> None:
        """Test publishing ticks in multiple batches."""
        # Create mock ticks (more than batch size of 1000)
        date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        ticks = [
            TickData(
                timestamp=date + timedelta(seconds=i),
                symbol="EURUSD",
                bid=1.10000 + i * 0.00001,
                ask=1.10010 + i * 0.00001,
                source="jforex"
            )
            for i in range(2500)
        ]
        
        # Publish
        await downloader._publish_ticks(ticks)
        
        # Should publish 3 times (2500 / 1000 = 2.5, rounded up to 3)
        assert downloader._event_bus.publish.call_count == 3
        downloader._logger.debug.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_download_tick_data_success(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test successful tick data download."""
        # Setup mock data
        date = datetime(2023, 12, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_data = MockBi5DataGenerator.generate_mock_bi5_data(
            "EURUSD",
            date,
            num_ticks=50
        )
        
        # Setup mock HTTP response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=mock_data)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_http_client.get.return_value = mock_response
        
        # Download
        ticks = await downloader.download_tick_data("EURUSD", date)
        
        # Verify results
        assert len(ticks) == 50
        assert all(isinstance(tick, TickData) for tick in ticks)
        assert all(tick.symbol == "EURUSD" for tick in ticks)
        
        # Verify logging
        downloader._logger.info.assert_called()
        downloader._logger.debug.assert_called()
    
    @pytest.mark.asyncio
    async def test_download_tick_data_404_error(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test tick data download with 404 error."""
        # Setup 404 response
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_http_client.get.return_value = mock_response
        
        date = datetime(2023, 12, 25, 10, 0, 0, tzinfo=timezone.utc)  # Christmas
        
        # Test that DataNotAvailableError is raised
        with pytest.raises(DataNotAvailableError):
            await downloader.download_tick_data("EURUSD", date)
    
    @pytest.mark.asyncio
    async def test_download_tick_data_decode_error(
        self,
        downloader: Bi5Downloader,
        mock_http_client: MagicMock
    ) -> None:
        """Test tick data download with corrupted data."""
        # Setup response with corrupted data
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"corrupted_data")
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_http_client.get.return_value = mock_response
        
        date = datetime(2023, 12, 1, 10, 0, 0, tzinfo=timezone.utc)
        
        # Test that DecodeError is raised
        with pytest.raises(DecodeError):
            await downloader.download_tick_data("EURUSD", date)
    
    @pytest.mark.asyncio
    async def test_get_available_dates(self, downloader: Bi5Downloader) -> None:
        """Test getting available dates."""
        start_date = datetime(2023, 12, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_date = datetime(2023, 12, 3, 0, 0, 0, tzinfo=timezone.utc)
        
        dates = await downloader.get_available_dates("EURUSD", start_date, end_date)
        
        # Should return all dates in range
        assert len(dates) == 3
        assert dates[0] == start_date
        assert dates[1] == datetime(2023, 12, 2, 0, 0, 0, tzinfo=timezone.utc)
        assert dates[2] == end_date
    
    def test_tick_data_properties(self) -> None:
        """Test TickData computed properties."""
        tick = TickData(
            timestamp=datetime(2023, 12, 1, 10, 0, 0, tzinfo=timezone.utc),
            symbol="EURUSD",
            bid=1.10000,
            ask=1.10010,
            source="jforex"
        )
        
        # Test spread calculation
        assert tick.spread == 1.0  # 1 pip spread
        
        # Test mid price calculation
        assert tick.mid_price == 1.10005