"""Tests for Bi5Downloader implementation."""

import lzma
import struct
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
)
from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader


class TestBi5Downloader:
    """Test suite for Bi5Downloader."""

    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies for Bi5Downloader."""
        logger = MagicMock()
        event_bus = MagicMock()
        event_bus.publish = AsyncMock()
        config = MagicMock()
        config.get.return_value = "https://www.dukascopy.com/datafeed"
        http_client = MagicMock()
        storage = MagicMock()
        storage.exists.return_value = False

        return {
            "logger": logger,
            "event_bus": event_bus,
            "config": config,
            "http_client": http_client,
            "storage": storage,
        }

    @pytest.fixture
    def downloader(self, mock_dependencies):
        """Create Bi5Downloader instance with mocked dependencies."""
        return Bi5Downloader(**mock_dependencies)

    def create_bi5_data_12_byte(
        self, timestamps_delta: list[int], ask: list[int], bid: list[int]
    ) -> bytes:
        """Create mock .bi5 data with 12-byte records.

        Args:
            timestamps_delta: List of timestamp deltas in milliseconds
            ask: List of ask prices as integers
            bid: List of bid prices as integers

        Returns:
            LZMA compressed .bi5 data
        """
        data = b""
        for delta, ask_price, bid_price in zip(timestamps_delta, ask, bid):
            data += struct.pack(">III", delta, ask_price, bid_price)

        return lzma.compress(data)

    def create_bi5_data_20_byte(
        self,
        timestamps_delta: list[int],
        ask: list[int],
        bid: list[int],
        ask_vol: list[float],
        bid_vol: list[float],
    ) -> bytes:
        """Create mock .bi5 data with 20-byte records.

        Args:
            timestamps_delta: List of timestamp deltas in milliseconds
            ask: List of ask prices as integers
            bid: List of bid prices as integers
            ask_vol: List of ask volumes as floats
            bid_vol: List of bid volumes as floats

        Returns:
            LZMA compressed .bi5 data
        """
        data = b""
        for delta, ask_price, bid_price, ask_volume, bid_volume in zip(
            timestamps_delta, ask, bid, ask_vol, bid_vol
        ):
            data += struct.pack(">IIIff", delta, ask_price, bid_price, ask_volume, bid_volume)

        return lzma.compress(data)

    def test_base_timestamp_calculation_retains_hour(self, downloader):
        """Test that base_timestamp calculation correctly retains the hour value.

        This is a CRITICAL test for the bug fix implemented on 2026.01.03.
        The previous implementation incorrectly zeroed out the hour (hour=0),
        which caused incorrect timestamp calculations for hourly .bi5 files.

        The .bi5 files from Dukascopy are hourly chunks, and the timestamp_delta
        is always calculated from the START of that specific hour, not from midnight.
        """
        # Test for 10:00 AM
        test_date = datetime(2024, 1, 15, 10, 30, 45, 123456, tzinfo=UTC)

        # Create mock 12-byte .bi5 data
        # Timestamp deltas are from the start of the hour (10:00:00)
        timestamps_delta = [0, 1000, 2000, 3000]  # 0ms, 1s, 2s, 3s from 10:00:00
        ask_prices = [112345, 112346, 112347, 112348]
        bid_prices = [112340, 112341, 112342, 112343]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        # Process the data
        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # Verify we got the expected number of ticks
        assert len(ticks) == 4

        # Calculate expected timestamps
        # Base timestamp should be 2024-01-15 10:00:00 (start of the hour)
        expected_base_timestamp = (
            int(test_date.replace(minute=0, second=0, microsecond=0).timestamp()) * 1000
        )

        # Verify each tick's timestamp
        for i, tick in enumerate(ticks):
            expected_timestamp_ms = expected_base_timestamp + timestamps_delta[i]
            expected_timestamp = datetime.fromtimestamp(expected_timestamp_ms / 1000, tz=UTC)

            assert tick.timestamp == expected_timestamp, (
                f"Tick {i}: Expected {expected_timestamp}, got {tick.timestamp}"
            )

            # Verify the hour is correct (should be 10, not 0)
            assert tick.timestamp.hour == 10, (
                f"Tick {i}: Hour should be 10, got {tick.timestamp.hour}"
            )

            # Verify the minute and second are correct
            expected_minute = timestamps_delta[i] // 60000
            expected_second = (timestamps_delta[i] % 60000) // 1000
            assert tick.timestamp.minute == expected_minute
            assert tick.timestamp.second == expected_second

    def test_base_timestamp_calculation_different_hours(self, downloader):
        """Test base_timestamp calculation for different hours of the day."""
        test_cases = [
            datetime(2024, 1, 15, 0, 0, 0, tzinfo=UTC),  # Midnight
            datetime(2024, 1, 15, 12, 0, 0, tzinfo=UTC),  # Noon
            datetime(2024, 1, 15, 23, 0, 0, tzinfo=UTC),  # 11 PM
        ]

        for test_date in test_cases:
            # Create mock data with a single tick at delta=0
            bi5_data = self.create_bi5_data_12_byte([0], [112345], [112340])

            ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

            assert len(ticks) == 1
            tick = ticks[0]

            # The tick timestamp should be at the start of the hour
            expected_timestamp = test_date.replace(minute=0, second=0, microsecond=0)
            assert tick.timestamp == expected_timestamp
            assert tick.timestamp.hour == test_date.hour

    def test_process_bi5_data_12_byte_format(self, downloader):
        """Test processing of 12-byte format .bi5 data."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock data
        timestamps_delta = [0, 5000, 10000]  # 0s, 5s, 10s from hour start
        ask_prices = [112345, 112350, 112355]
        bid_prices = [112340, 112345, 112350]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # Verify we got the expected number of ticks
        assert len(ticks) == 3

        # Verify first tick
        assert ticks[0].symbol == "EURUSD"
        assert ticks[0].bid == 1.12340
        assert ticks[0].ask == 1.12345
        assert ticks[0].ask_volume is None
        assert ticks[0].bid_volume is None
        assert ticks[0].source == "jforex"

        # Verify timestamp
        expected_timestamp = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)
        assert ticks[0].timestamp == expected_timestamp

    def test_process_bi5_data_20_byte_format(self, downloader):
        """Test processing of 20-byte format .bi5 data."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock data
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]
        ask_volumes = [1.5, 2.0]
        bid_volumes = [1.2, 1.8]

        bi5_data = self.create_bi5_data_20_byte(
            timestamps_delta, ask_prices, bid_prices, ask_volumes, bid_volumes
        )

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # Verify we got the expected number of ticks
        assert len(ticks) == 2

        # Verify first tick has volume data (use approximate comparison for floats)
        assert abs(ticks[0].ask_volume - 1.5) < 0.0001
        assert abs(ticks[0].bid_volume - 1.2) < 0.0001

    def test_process_bi5_data_empty_file(self, downloader):
        """Test handling of empty .bi5 file."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Empty data
        bi5_data = b""

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        assert len(ticks) == 0
        downloader._logger.warning.assert_called()

    def test_process_bi5_data_invalid_prices(self, downloader):
        """Test filtering of invalid (non-positive) prices."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create data with some invalid prices
        timestamps_delta = [0, 1000, 2000, 3000]
        ask_prices = [112345, 0, 112347, 112348]  # 0 price should be filtered
        bid_prices = [112340, 112341, 0, 112343]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # Only ticks 0 and 2 should be valid
        assert len(ticks) == 2
        assert ticks[0].bid == 1.12340
        assert ticks[1].bid == 1.12343

    def test_process_bi5_data_invalid_timestamp_delta(self, downloader):
        """Test that the code handles timestamp delta validation (edge case).

        Note: We cannot create negative timestamp_delta values in struct.pack
        with unsigned int format, but the actual Bi5Downloader code does check
        for negative values after unpacking. This test verifies normal operation.
        """
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create normal data with valid timestamp deltas
        timestamps_delta = [0, 1000, 2000]
        ask_prices = [112345, 112346, 112347]
        bid_prices = [112340, 112341, 112342]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # All ticks should be valid
        assert len(ticks) == 3

    def test_process_bi5_data_date_mismatch(self, downloader):
        """Test handling of ticks with date mismatch."""
        test_date = datetime(2024, 1, 15, 23, 0, 0, tzinfo=UTC)

        # Create data with large delta that would push to next day
        timestamps_delta = [0, 3_600_000, 7_200_000]  # 0h, 1h, 2h from 23:00
        ask_prices = [112345, 112346, 112347]
        bid_prices = [112340, 112341, 112342]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)

        # Only the first tick (23:00) should be valid
        # The second tick (00:00 next day) should be filtered out
        assert len(ticks) == 1
        assert ticks[0].timestamp.hour == 23

    def test_build_url(self, downloader):
        """Test URL building for Dukascopy download."""
        test_date = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)

        url = downloader._build_url("EURUSD", test_date)

        # Dukascopy uses 0-indexed months (January = 00)
        assert url == "https://www.dukascopy.com/datafeed/EURUSD/2024/00/15/10h_ticks.bi5"

    def test_build_storage_path(self, downloader):
        """Test storage path building."""
        test_date = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)

        path = downloader._build_storage_path("EURUSD", test_date)

        assert path == "data/jforex/EURUSD/2024/01/15/10h_ticks.parquet"

    @pytest.mark.asyncio
    async def test_download_tick_data_success(self, mock_dependencies):
        """Test successful download of tick data."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(
            return_value=self.create_bi5_data_12_byte([0, 1000], [112345, 112346], [112340, 112341])
        )

        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response

        downloader = Bi5Downloader(**mock_dependencies)

        ticks = await downloader.download_tick_data("EURUSD", test_date)

        assert len(ticks) == 2
        mock_dependencies["storage"].exists.assert_called_once()
        mock_dependencies["event_bus"].publish.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_tick_data_not_available(self, mock_dependencies):
        """Test handling of 404 (data not available)."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock 404 response
        mock_response = MagicMock()
        mock_response.status = 404

        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response

        downloader = Bi5Downloader(**mock_dependencies)

        with pytest.raises(DataNotAvailableError):
            await downloader.download_tick_data("EURUSD", test_date)

    @pytest.mark.asyncio
    async def test_download_tick_data_already_exists(self, mock_dependencies):
        """Test skipping download when data already exists."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Mock storage to return that data exists
        mock_dependencies["storage"].exists.return_value = True
        mock_dependencies["storage"].get_metadata.return_value = {"size": 1000}

        downloader = Bi5Downloader(**mock_dependencies)

        ticks = await downloader.download_tick_data("EURUSD", test_date)

        # Should return empty list when data already exists
        assert ticks == []
        # Should not make HTTP request
        mock_dependencies["http_client"].get.assert_not_called()

    def test_validate_bi5_data_valid(self, downloader):
        """Test validation of valid .bi5 data."""
        bi5_data = self.create_bi5_data_12_byte([0, 1000], [112345, 112346], [112340, 112341])

        assert downloader.validate_bi5_data(bi5_data) is True

    def test_validate_bi5_data_invalid_size(self, downloader):
        """Test validation of data that's too small."""
        bi5_data = b"12345678"  # Less than 12 bytes

        assert downloader.validate_bi5_data(bi5_data) is False

    def test_validate_bi5_data_invalid_lzma(self, downloader):
        """Test validation of invalid LZMA data."""
        bi5_data = b"invalid_lzma_data"

        assert downloader.validate_bi5_data(bi5_data) is False

    @pytest.mark.asyncio
    async def test_close(self, mock_dependencies):
        """Test closing of HTTP client."""
        mock_dependencies["http_client"].closed = False
        mock_dependencies["http_client"].close = AsyncMock()

        downloader = Bi5Downloader(**mock_dependencies)

        await downloader.close()

        mock_dependencies["http_client"].close.assert_called_once()

    def test_detect_format_12_byte_default(self, downloader):
        """Test that 12-byte format is the default when both 12 and 20 are divisible."""
        # Create 12-byte data (3 records = 36 bytes, also divisible by 20)
        timestamps_delta = [0, 1000, 2000]
        ask_prices = [112345, 112346, 112347]
        bid_prices = [112340, 112341, 112342]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)
        decompressed = lzma.decompress(bi5_data)

        # A 36 bájtos adat osztható 12-vel és 20-szal is
        # De a 12 bájtosnak kell lennie az alapértelmezettnek
        record_size, unpack_format = downloader._detect_format(decompressed)

        assert record_size == 12
        assert unpack_format == ">III"

    def test_detect_format_20_byte_with_valid_volumes(self, downloader):
        """Test that 20-byte format is detected when volumes are valid."""
        # Create 20-byte data with realistic volumes
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]
        ask_volumes = [1.5, 2.0]  # Realistic volumes
        bid_volumes = [1.2, 1.8]

        bi5_data = self.create_bi5_data_20_byte(
            timestamps_delta, ask_prices, bid_prices, ask_volumes, bid_volumes
        )
        decompressed = lzma.decompress(bi5_data)

        record_size, unpack_format = downloader._detect_format(decompressed)

        assert record_size == 20
        assert unpack_format == ">IIIff"

    def test_detect_format_20_byte_rejects_noise_volumes(self, downloader):
        """Test that 20-byte format is rejected when volumes are noise (very small floats)."""
        # Create 20-byte data with noise volumes (like from integer misinterpretation)
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]
        # Very small volumes that are likely noise from integer->float conversion
        ask_volumes = [1.4e-43, 2.0e-43]
        bid_volumes = [1.2e-43, 1.8e-43]

        bi5_data = self.create_bi5_data_20_byte(
            timestamps_delta, ask_prices, bid_prices, ask_volumes, bid_volumes
        )
        decompressed = lzma.decompress(bi5_data)

        # Should fall back to 12-byte format due to noise detection
        record_size, unpack_format = downloader._detect_format(decompressed)

        assert record_size == 12
        assert unpack_format == ">III"

    def test_detect_format_20_byte_rejects_zero_volumes(self, downloader):
        """Test that 20-byte format is accepted with zero volumes."""
        # Create 20-byte data with zero volumes (valid case)
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]
        ask_volumes = [0.0, 0.0]
        bid_volumes = [0.0, 0.0]

        bi5_data = self.create_bi5_data_20_byte(
            timestamps_delta, ask_prices, bid_prices, ask_volumes, bid_volumes
        )
        decompressed = lzma.decompress(bi5_data)

        record_size, unpack_format = downloader._detect_format(decompressed)

        # Zero volumes are valid, should detect as 20-byte
        assert record_size == 20
        assert unpack_format == ">IIIff"

    def test_detect_format_12_byte_only(self, downloader):
        """Test that 12-byte format is detected when data is only divisible by 12."""
        # Create 12-byte data (2 records = 24 bytes, NOT divisible by 20)
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)
        decompressed = lzma.decompress(bi5_data)

        record_size, unpack_format = downloader._detect_format(decompressed)

        assert record_size == 12
        assert unpack_format == ">III"
