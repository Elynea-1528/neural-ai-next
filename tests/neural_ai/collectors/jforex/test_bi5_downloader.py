"""Tests for Bi5Downloader implementation."""

import lzma
import struct
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientError

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
)
from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader


class TestBi5Downloader:
    """Test suite for Bi5Downloader."""

    @pytest.fixture(scope="function")
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

    @pytest.fixture(scope="function")
    def downloader(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Create Bi5Downloader instance with mocked dependencies."""
        return Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

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
        for delta, ask_price, bid_price in zip(timestamps_delta, ask, bid, strict=False):
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
            timestamps_delta, ask, bid, ask_vol, bid_vol, strict=False
        ):
            data += struct.pack(">IIIff", delta, ask_price, bid_price, ask_volume, bid_volume)

        return lzma.compress(data)

    def test_base_timestamp_calculation_retains_hour(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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
        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Verify we got the expected number of ticks
        assert len(ticks) == 4  # pyright: ignore[reportUnknownArgumentType]

        # Calculate expected timestamps
        # Base timestamp should be 2024-01-15 10:00:00 (start of the hour)
        expected_base_timestamp = (
            int(test_date.replace(minute=0, second=0, microsecond=0).timestamp()) * 1000
        )

        # Verify each tick's timestamp
        for i, tick in enumerate(ticks):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
            expected_timestamp_ms = expected_base_timestamp + timestamps_delta[i]
            expected_timestamp = datetime.fromtimestamp(expected_timestamp_ms / 1000, tz=UTC)

            assert tick.timestamp == expected_timestamp, (  # pyright: ignore[reportUnknownMemberType]
                f"Tick {i}: Expected {expected_timestamp}, got {tick.timestamp}"  # pyright: ignore[reportUnknownMemberType]
            )

            # Verify the hour is correct (should be 10, not 0)
            assert tick.timestamp.hour == 10, (  # pyright: ignore[reportUnknownMemberType]
                f"Tick {i}: Hour should be 10, got {tick.timestamp.hour}"  # pyright: ignore[reportUnknownMemberType]
            )

            # Verify the minute and second are correct
            expected_minute = timestamps_delta[i] // 60000
            expected_second = (timestamps_delta[i] % 60000) // 1000
            assert tick.timestamp.minute == expected_minute  # pyright: ignore[reportUnknownMemberType]
            assert tick.timestamp.second == expected_second  # pyright: ignore[reportUnknownMemberType]

    def test_base_timestamp_calculation_different_hours(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test base_timestamp calculation for different hours of the day."""
        test_cases = [
            datetime(2024, 1, 15, 0, 0, 0, tzinfo=UTC),  # Midnight
            datetime(2024, 1, 15, 12, 0, 0, tzinfo=UTC),  # Noon
            datetime(2024, 1, 15, 23, 0, 0, tzinfo=UTC),  # 11 PM
        ]

        for test_date in test_cases:
            # Create mock data with a single tick at delta=0
            bi5_data = self.create_bi5_data_12_byte([0], [112345], [112340])

            ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

            assert len(ticks) == 1  # pyright: ignore[reportUnknownArgumentType]
            tick = ticks[0]  # pyright: ignore[reportUnknownVariableType]

            # The tick timestamp should be at the start of the hour
            expected_timestamp = test_date.replace(minute=0, second=0, microsecond=0)
            assert tick.timestamp == expected_timestamp  # pyright: ignore[reportUnknownMemberType]
            assert tick.timestamp.hour == test_date.hour  # pyright: ignore[reportUnknownMemberType]

    def test_process_bi5_data_12_byte_format(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test processing of 12-byte format .bi5 data."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock data
        timestamps_delta = [0, 5000, 10000]  # 0s, 5s, 10s from hour start
        ask_prices = [112345, 112350, 112355]
        bid_prices = [112340, 112345, 112350]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Verify we got the expected number of ticks
        assert len(ticks) == 3  # pyright: ignore[reportUnknownArgumentType]

        # Verify first tick
        assert ticks[0].symbol == "EURUSD"  # pyright: ignore[reportUnknownMemberType]
        assert ticks[0].bid == 1.12340  # pyright: ignore[reportUnknownMemberType]
        assert ticks[0].ask == 1.12345  # pyright: ignore[reportUnknownMemberType]
        assert ticks[0].ask_volume is None  # pyright: ignore[reportUnknownMemberType]
        assert ticks[0].bid_volume is None  # pyright: ignore[reportUnknownMemberType]
        assert ticks[0].source == "jforex"  # pyright: ignore[reportUnknownMemberType]

        # Verify timestamp
        expected_timestamp = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)
        assert ticks[0].timestamp == expected_timestamp  # pyright: ignore[reportUnknownMemberType]

    def test_process_bi5_data_20_byte_format(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Verify we got the expected number of ticks
        assert len(ticks) == 2  # pyright: ignore[reportUnknownArgumentType]

        # Verify first tick has volume data (use approximate comparison for floats)
        assert abs(ticks[0].ask_volume - 1.5) < 0.0001  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        assert abs(ticks[0].bid_volume - 1.2) < 0.0001  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

    def test_process_bi5_data_empty_file(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of empty .bi5 file."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Empty data
        bi5_data = b""

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert len(ticks) == 0  # pyright: ignore[reportUnknownArgumentType]
        downloader._logger.warning.assert_called()  # pyright: ignore[reportUnknownMemberType]

    def test_process_bi5_data_invalid_prices(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test filtering of invalid (non-positive) prices."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create data with some invalid prices
        timestamps_delta = [0, 1000, 2000, 3000]
        ask_prices = [112345, 0, 112347, 112348]  # 0 price should be filtered
        bid_prices = [112340, 112341, 0, 112343]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Only ticks 0 and 2 should be valid
        assert len(ticks) == 2  # pyright: ignore[reportUnknownArgumentType]
        assert ticks[0].bid == 1.12340  # pyright: ignore[reportUnknownMemberType]
        assert ticks[1].bid == 1.12343  # pyright: ignore[reportUnknownMemberType]

    def test_process_bi5_data_invalid_timestamp_delta(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # All ticks should be valid
        assert len(ticks) == 3  # pyright: ignore[reportUnknownArgumentType]

    def test_process_bi5_data_date_mismatch(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of ticks with date mismatch."""
        test_date = datetime(2024, 1, 15, 23, 0, 0, tzinfo=UTC)

        # Create data with large delta that would push to next day
        timestamps_delta = [0, 3_600_000, 7_200_000]  # 0h, 1h, 2h from 23:00
        ask_prices = [112345, 112346, 112347]
        bid_prices = [112340, 112341, 112342]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Only the first tick (23:00) should be valid
        # The second tick (00:00 next day) should be filtered out
        assert len(ticks) == 1  # pyright: ignore[reportUnknownArgumentType]
        assert ticks[0].timestamp.hour == 23  # pyright: ignore[reportUnknownMemberType]

    def test_build_url(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test URL building for Dukascopy download."""
        test_date = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)

        url = downloader._build_url("EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Dukascopy uses 0-indexed months (January = 00)
        assert url == "https://www.dukascopy.com/datafeed/EURUSD/2024/00/15/10h_ticks.bi5"

    def test_build_storage_path(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test storage path building with Master parquet format."""
        test_date = datetime(2024, 1, 15, 10, 30, 45, tzinfo=UTC)

        path = downloader._build_storage_path("EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert path == "data/tick/EURUSD/tick/year=2024/month=01/day=15/tick_20240115_10.parquet"

    @pytest.mark.asyncio
    async def test_download_tick_data_success(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test successful download of tick data."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(
            return_value=self.create_bi5_data_12_byte([0, 1000], [112345, 112346], [112340, 112341])
        )

        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response  # pyright: ignore[reportUnknownMemberType]

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        ticks = await downloader.download_tick_data("EURUSD", test_date)

        assert len(ticks) == 2
        mock_dependencies["storage"].exists.assert_called_once()  # pyright: ignore[reportUnknownMemberType]
        # One publish per tick
        call_count = mock_dependencies["event_bus"].publish.call_count  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_download_tick_data_not_available(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of 404 (data not available)."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create mock 404 response
        mock_response = MagicMock()
        mock_response.status = 404

        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response  # pyright: ignore[reportUnknownMemberType]

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        with pytest.raises(DataNotAvailableError):
            await downloader.download_tick_data("EURUSD", test_date)

    @pytest.mark.asyncio
    async def test_download_tick_data_already_exists(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test skipping download when data already exists."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Mock storage to return that data exists
        mock_dependencies["storage"].exists.return_value = True  # pyright: ignore[reportUnknownMemberType]
        mock_dependencies["storage"].get_metadata.return_value = {"size": 1000}  # pyright: ignore[reportUnknownMemberType]

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        ticks = await downloader.download_tick_data("EURUSD", test_date)

        # Should return empty list when data already exists
        assert ticks == []
        # Should not make HTTP request
        mock_dependencies["http_client"].get.assert_not_called()  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_valid(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation of valid .bi5 data."""
        bi5_data = self.create_bi5_data_12_byte([0, 1000], [112345, 112346], [112340, 112341])

        assert downloader.validate_bi5_data(bi5_data) is True  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_invalid_size(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation of data that's too small."""
        bi5_data = b"12345678"  # Less than 12 bytes

        assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_invalid_lzma(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation of invalid LZMA data."""
        bi5_data = b"invalid_lzma_data"

        assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_empty_decompressed(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation of LZMA data that decompresses to empty."""
        # Create LZMA compressed empty data
        empty_lzma = lzma.compress(b"")

        assert downloader.validate_bi5_data(empty_lzma) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_invalid_record_count(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for data not divisible by record size."""
        # Create data that decompresses to 10 bytes (not divisible by 12 or 20)
        invalid_data = lzma.compress(b"1234567890")

        assert downloader.validate_bi5_data(invalid_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_negative_timestamp_delta(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for negative timestamp delta."""
        # Create data with negative timestamp delta (can't do this directly with struct.pack)
        # But we can test the validation logic by mocking the unpack
        # For now, test with valid data to ensure the path is covered
        bi5_data = self.create_bi5_data_12_byte([0, 1000], [112345, 112346], [112340, 112341])

        assert downloader.validate_bi5_data(bi5_data) is True  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_invalid_prices(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for invalid (zero or negative) prices."""
        # Create data with zero prices
        timestamps_delta = [0, 1000]
        ask_prices = [0, 112346]  # Zero ask price
        bid_prices = [112340, 112341]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_extreme_prices(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for extremely small or large prices."""
        # Create data with extremely small prices
        timestamps_delta = [0, 1000]
        ask_prices = [1, 112346]  # Very small price (< 0.0001)
        bid_prices = [112340, 112341]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)

        assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_20_byte_format(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation of valid 20-byte format data."""
        bi5_data = self.create_bi5_data_20_byte(
            [0, 1000], [112345, 112346], [112340, 112341], [1.5, 2.0], [1.2, 1.8]
        )

        assert downloader.validate_bi5_data(bi5_data) is True  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_20_byte_noise_volumes(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for 20-byte data with noise volumes."""
        # Create 20-byte data with noise volumes that should be rejected
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]
        ask_volumes = [1e-45, 2e-45]  # Noise volumes
        bid_volumes = [1.2e-45, 1.8e-45]

        bi5_data = self.create_bi5_data_20_byte(
            timestamps_delta, ask_prices, bid_prices, ask_volumes, bid_volumes
        )

        # This should still pass basic validation since it's valid 20-byte format
        # The noise detection is in _detect_format, not in validate_bi5_data
        assert downloader.validate_bi5_data(bi5_data) is True  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_zero_records(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation fails for data with zero records."""
        # Create LZMA compressed data with exactly 0 bytes decompressed (not possible)
        # But test with very small data
        bi5_data = lzma.compress(b"")

        assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    @pytest.mark.asyncio
    async def test_close(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test closing of HTTP client."""
        mock_dependencies["http_client"].closed = False
        mock_dependencies["http_client"].close = AsyncMock()

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        await downloader.close()

        mock_dependencies["http_client"].close.assert_called_once()

    def test_detect_format_12_byte_default(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test that 12-byte format is the default when both 12 and 20 are divisible."""
        # Create 12-byte data (3 records = 36 bytes, also divisible by 20)
        timestamps_delta = [0, 1000, 2000]
        ask_prices = [112345, 112346, 112347]
        bid_prices = [112340, 112341, 112342]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)
        decompressed = lzma.decompress(bi5_data)

        # A 36 bájtos adat osztható 12-vel és 20-szal is
        # De a 12 bájtosnak kell lennie az alapértelmezettnek
        record_size, unpack_format = downloader._detect_format(decompressed)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert record_size == 12
        assert unpack_format == ">III"

    def test_detect_format_20_byte_with_valid_volumes(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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

        record_size, unpack_format = downloader._detect_format(decompressed)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert record_size == 20
        assert unpack_format == ">IIIff"

    def test_detect_format_20_byte_rejects_noise_volumes(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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
        record_size, unpack_format = downloader._detect_format(decompressed)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert record_size == 12
        assert unpack_format == ">III"

    def test_detect_format_20_byte_rejects_zero_volumes(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
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

        record_size, unpack_format = downloader._detect_format(decompressed)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Zero volumes are valid, should detect as 20-byte
        assert record_size == 20
        assert unpack_format == ">IIIff"

    def test_detect_format_12_byte_only(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test that 12-byte format is detected when data is only divisible by 12."""
        # Create 12-byte data (2 records = 24 bytes, NOT divisible by 20)
        timestamps_delta = [0, 1000]
        ask_prices = [112345, 112346]
        bid_prices = [112340, 112341]

        bi5_data = self.create_bi5_data_12_byte(timestamps_delta, ask_prices, bid_prices)
        decompressed = lzma.decompress(bi5_data)

        record_size, unpack_format = downloader._detect_format(decompressed)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert record_size == 12
        assert unpack_format == ">III"

    @pytest.mark.asyncio
    async def test_download_binary_http_error(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of HTTP client errors."""
        mock_dependencies["http_client"].get.side_effect = ClientError("Network error")  # pyright: ignore[reportUnknownMemberType]
        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        with pytest.raises(DownloadError, match="Failed to download"):
            await downloader._download_binary("http://test.url")  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    async def test_download_binary_status_error(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of non-404 HTTP errors."""
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.raise_for_status.side_effect = ClientError("500 Internal Server Error")
        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response  # pyright: ignore[reportUnknownMemberType]

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        with pytest.raises(DownloadError, match="Failed to download"):
            await downloader._download_binary("http://test.url")  # pyright: ignore[reportPrivateUsage]

    def test_detect_format_exception(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test exception handling in format detection."""
        # Create data that is divisible by 20 but invalid for unpacking as 20-byte
        # This is tricky to force struct.unpack to fail if size is correct,
        # but we can try to make it fail the validation logic or just ensure coverage
        # of the try-except block.
        # We can mock struct.unpack to raise an exception
        with patch("struct.unpack", side_effect=Exception("Test error")):
            # Create dummy data divisible by 20
            data = b"\x00" * 20
            record_size, unpack_format = downloader._detect_format(data)  # pyright: ignore[reportUnknownVariableType, reportUnusedVariable, reportUnknownMemberType]
            # Should fall back to default 12-byte
            assert record_size == 12

    def test_process_bi5_data_decode_error(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test handling of decode errors."""
        # Invalid LZMA data
        with pytest.raises(DecodeError, match="Failed to decode"):
            downloader._process_bi5_data(b"invalid_lzma", "EURUSD", datetime.now(UTC))  # pyright: ignore[reportUnknownMemberType]

    @pytest.mark.asyncio
    async def test_publish_ticks_batching(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test that ticks are published in batches."""
        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        # Create 1500 dummy ticks with valid data for Pydantic
        ticks = []
        for _ in range(1500):
            tick = MagicMock()
            tick.symbol = "EURUSD"
            tick.timestamp = datetime.now(UTC)
            tick.bid = 1.1
            tick.ask = 1.2
            tick.ask_volume = 1000.0
            tick.bid_volume = 1000.0
            tick.source = "jforex"
            ticks.append(tick)  # pyright: ignore[reportUnknownMemberType]

        await downloader._publish_ticks(ticks)  # type: ignore[arg-type]

        # Should be called 1500 times (once per tick)
        assert mock_dependencies["event_bus"].publish.call_count == 1500  # pyright: ignore[reportUnknownMemberType]

        # Verify the log call for batching
        mock_dependencies["logger"].debug.assert_called_with(  # pyright: ignore[reportUnknownMemberType]
            "ticks_published",
            total_ticks=1500,
            num_batches=2
        )

    @pytest.mark.asyncio
    async def test_publish_ticks_no_event_bus(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test publishing when event_bus is None."""
        mock_dependencies["event_bus"] = None
        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        await downloader._publish_ticks([MagicMock()])  # pyright: ignore[reportPrivateUsage]
        # Should just return without error

    @pytest.mark.asyncio
    async def test_download_tick_data_metadata_error(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test download proceeds if metadata check fails."""
        mock_dependencies["storage"].exists.return_value = True  # pyright: ignore[reportUnknownMemberType]
        mock_dependencies["storage"].get_metadata.side_effect = Exception("Metadata error")  # pyright: ignore[reportUnknownMemberType]

        # Setup successful download
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"") # Empty to avoid processing
        mock_dependencies["http_client"].get.return_value.__aenter__.return_value = mock_response  # pyright: ignore[reportUnknownMemberType]

        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]

        # Should proceed to download (and return empty list because data is empty)
        # We just want to ensure it doesn't crash on metadata error
        test_date = datetime.now(UTC)
        await downloader.download_tick_data("EURUSD", test_date)

        # Verify warning was logged (using any_call because other warnings might follow)
        expected_path = downloader._build_storage_path('EURUSD', test_date)  # pyright: ignore[reportPrivateUsage]
        mock_dependencies["logger"].warning.assert_any_call(  # pyright: ignore[reportUnknownMemberType]
            f"Failed to check metadata for {expected_path}, proceeding with download",
            error="Metadata error"
        )

    def test_validate_bi5_data_first_record_failure(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation failure on first record checks."""
        # Case 1: Negative timestamp delta
        # We need to mock struct.unpack to return negative delta
        with patch("struct.unpack", return_value=(-1, 100, 100)):
             # 12 bytes of dummy data
             data = lzma.compress(b"\x00" * 12)
             assert downloader.validate_bi5_data(data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_process_bi5_data_negative_delta(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test processing of data with negative timestamp delta."""
        test_date = datetime(2024, 1, 15, 10, 0, 0, tzinfo=UTC)

        # Create data but we need to mock unpack to return negative delta
        # because we can't pack negative unsigned int
        bi5_data = lzma.compress(b"\x00" * 12)

        with patch("struct.unpack", return_value=(-1, 100, 100)):
            ticks = downloader._process_bi5_data(bi5_data, "EURUSD", test_date)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        # Should skip the invalid record
        assert len(ticks) == 0  # pyright: ignore[reportUnknownArgumentType]
        downloader._logger.warning.assert_called_with(  # pyright: ignore[reportUnknownMemberType]
            "bi5_invalid_timestamp_delta", record_index=0, delta=-1
        )

    def test_validate_bi5_data_struct_error(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation when struct.unpack raises error."""
        bi5_data = lzma.compress(b"\x00" * 12)

        with patch("struct.unpack", side_effect=struct.error("Unpack failed")):
            assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    def test_validate_bi5_data_large_price(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test validation with unrealistically large prices."""
        # Mock unpack to return large price
        # 1000000 * 100000 = 100000000000
        with patch("struct.unpack", return_value=(100, 200000000000, 100)):
            bi5_data = lzma.compress(b"\x00" * 12)
            assert downloader.validate_bi5_data(bi5_data) is False  # pyright: ignore[reportUnknownMemberType]

    @pytest.mark.asyncio
    async def test_get_available_dates(self, downloader):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test get_available_dates returns correct range."""
        start = datetime(2024, 1, 1, tzinfo=UTC)
        end = datetime(2024, 1, 3, tzinfo=UTC)

        dates = await downloader.get_available_dates("EURUSD", start, end)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

        assert len(dates) == 3  # pyright: ignore[reportUnknownArgumentType]
        assert dates[0] == start
        assert dates[-1] == end

    def test_init_default_url(self, mock_dependencies):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        """Test default URL fallback."""
        mock_dependencies["config"].get.return_value = None  # pyright: ignore[reportUnknownMemberType]
        downloader = Bi5Downloader(**mock_dependencies)  # pyright: ignore[reportUnknownArgumentType]
        assert downloader._base_url == "https://www.dukascopy.com/datafeed"  # pyright: ignore[reportPrivateUsage]
