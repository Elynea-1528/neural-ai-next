"""Bi5 Downloader Implementation."""

import lzma
import struct
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
)
from neural_ai.collectors.jforex.interfaces.tick_data import TickData

if TYPE_CHECKING:
    import aiohttp
    from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
    from neural_ai.collectors.jforex.interfaces.tick_data import TickData
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.collectors.jforex.exceptions.jforex_error import (
        DataNotAvailableError,
        DecodeError,
        DownloadError,
    )


class Bi5Downloader:
    """JForex Bi5 data downloader implementation.

    Downloads and decodes Dukascopy's native .bi5 tick data format.
    """

    def __init__(
        self,
        logger: "LoggerInterface",
        event_bus: "EventBusInterface",
        config: "ConfigManagerInterface",
        http_client: "aiohttp.ClientSession",
    ):
        """Initialize Bi5 downloader.

        Args:
            logger: Logger instance
            event_bus: Event bus for publishing market data
            config: Configuration manager
            http_client: HTTP client for downloads
        """
        self._logger = logger
        self._event_bus = event_bus
        self._config = config
        self._http_client = http_client
        self._base_url = config.get("jforex.base_url", "https://www.dukascopy.com/datafeed")
        if not self._base_url:
            self._base_url = "https://www.dukascopy.com/datafeed"
            self._logger.warning("jforex_base_url_not_set", _message="Using default Dukascopy URL")

    def _build_url(self, symbol: str, date: datetime) -> str:
        """Build Dukascopy .bi5 download URL.

        Args:
            symbol: Trading symbol (e.g., 'EURUSD')
            date: Date for which to download data

        Returns:
            Complete download URL
        """
        # Dukascopy uses 0-indexed months (00-11)
        year = date.year
        month = date.month - 1  # Convert to 0-indexed
        day = date.day
        hour = date.hour

        # Format: {BASE_URL}/{SYMBOL}/{YEAR}/{MONTH_00}/{DAY_00}/{HOUR_00}h_ticks.bi5
        url = (
            f"{self._base_url}/{symbol.upper()}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
        )

        return url

    async def _download_binary(self, url: str) -> bytes:
        """Download binary .bi5 data from Dukascopy.

        Args:
            url: Complete download URL

        Returns:
            Raw .bi5 binary data

        Raises:
            DataNotAvailableError: If server returns 404 (weekend/holiday)
            DownloadError: If network error occurs
        """
        try:
            async with self._http_client.get(url) as response:
                if response.status == 404:
                    self._logger.warning("bi5_data_not_available", url=url, reason="404_not_found")
                    raise DataNotAvailableError(f"No data available at {url}")

                response.raise_for_status()
                data = await response.read()

                self._logger.debug("bi5_download_success", url=url, size_bytes=len(data))

                return data

        except aiohttp.ClientError as e:
            self._logger.error("bi5_download_failed", url=url, error=str(e))
            raise DownloadError(f"Failed to download {url}: {e}") from e

    def _process_bi5_data(self, data: bytes, symbol: str, date: datetime) -> list["TickData"]:
        """Process and decode .bi5 binary data.

        Args:
            data: Raw .bi5 binary data (LZMA compressed)
            symbol: Trading symbol
            date: Date for which data was downloaded

        Returns:
            List of TickData objects

        Raises:
            DecodeError: If decompression or unpacking fails
        """
        # Check for empty file before attempting decompression
        if not data or len(data) == 0:
            self._logger.warning("bi5_empty_file_received", symbol=symbol, date=date.isoformat())
            return []  # Return empty list instead of crashing
        
        try:
            # LZMA decompression
            decompressed = lzma.decompress(data)

            # Process records (12 bytes each: 4 bytes timestamp_delta + 4 bytes ask + 4 bytes bid)
            record_size = 12
            num_records = len(decompressed) // record_size

            # Base timestamp: start of the day in milliseconds
            base_timestamp = (
                int(date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()) * 1000
            )

            ticks: list[TickData] = []

            for i in range(num_records):
                offset = i * record_size
                record = decompressed[offset : offset + record_size]

                # Big-endian unpack: unsigned int, unsigned int, unsigned int
                # Dukascopy stores prices as integers (multiplied by 100,000)
                timestamp_delta, ask_int, bid_int = struct.unpack(">III", record)
                
                # Convert integer prices to floats
                ask = ask_int / 100000.0
                bid = bid_int / 100000.0

                # Skip records with invalid prices (0.0, negative, or unreasonable)
                if bid <= 0.0 or ask <= 0.0 or bid > 100.0 or ask > 100.0:
                    self._logger.warning(
                        "bi5_invalid_price_skipped",
                        symbol=symbol,
                        record_index=i,
                        bid=bid,
                        ask=ask
                    )
                    continue

                # Calculate actual timestamp
                timestamp_ms = base_timestamp + timestamp_delta
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)

                # Create TickData object
                tick = TickData(
                    timestamp=timestamp,
                    symbol=symbol.upper(),
                    bid=round(bid, 5),  # Forex prices to 5 decimal places
                    ask=round(ask, 5),
                    source="jforex",
                )

                ticks.append(tick)

            self._logger.debug(
                "bi5_decode_success", symbol=symbol, date=date.isoformat(), num_ticks=len(ticks)
            )

            return ticks

        except (lzma.LZMAError, struct.error) as e:
            self._logger.error(
                "bi5_decode_failed", symbol=symbol, date=date.isoformat(), error=str(e)
            )
            raise DecodeError(f"Failed to decode .bi5 data: {e}") from e

    async def _publish_ticks(self, ticks: list["TickData"]) -> None:
        """Publish tick data to EventBus.

        Args:
            ticks: List of TickData objects to publish
        """
        if not ticks:
            return

        # Import MarketDataEvent here to avoid circular imports
        from neural_ai.core.events.interfaces.event_models import MarketDataEvent

        # Publish in batches of 1000 to avoid overwhelming the bus
        batch_size = 1000
        for i in range(0, len(ticks), batch_size):
            batch = ticks[i : i + batch_size]

            # Convert TickData to MarketDataEvent
            events = [
                MarketDataEvent(
                    symbol=tick.symbol,
                    timestamp=tick.timestamp,
                    bid=tick.bid,
                    ask=tick.ask,
                    volume=None,  # JForex .bi5 doesn't include volume
                    source=tick.source,
                )
                for tick in batch
            ]

            # Publish batch
            await self._event_bus.publish("market_data", events)

        self._logger.debug(
            "ticks_published",
            total_ticks=len(ticks),
            num_batches=(len(ticks) + batch_size - 1) // batch_size,
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True
    )
    async def download_tick_data(self, symbol: str, date: datetime) -> list["TickData"]:
        """Download and decode tick data.

        Args:
            symbol: Trading symbol
            date: Date for which to download data

        Returns:
            List of TickData objects

        Raises:
            DownloadError: If download fails
            DecodeError: If decoding fails
            DataNotAvailableError: If data not available
        """
        self._logger.info("download_started", symbol=symbol, date=date.isoformat())

        # Build URL
        url = self._build_url(symbol, date)

        # Download binary data
        binary_data = await self._download_binary(url)

        # Process and decode data
        ticks = self._process_bi5_data(binary_data, symbol, date)

        # Publish to EventBus
        await self._publish_ticks(ticks)

        self._logger.info(
            "download_completed", symbol=symbol, date=date.isoformat(), num_ticks=len(ticks)
        )

        return ticks

    def validate_bi5_data(self, data: bytes) -> bool:
        """Validate .bi5 data integrity.

        Args:
            data: Raw .bi5 data bytes

        Returns:
            True if data is valid
        """
        # Check minimum size
        if len(data) < 12:
            self._logger.warning("bi5_invalid_size", size=len(data), expected_min=12)
            return False

        # Try LZMA decompression
        try:
            decompressed = lzma.decompress(data)

            # Check if decompressed size is divisible by record size (12 bytes)
            if len(decompressed) % 12 != 0:
                self._logger.warning(
                    "bi5_invalid_record_count", decompressed_size=len(decompressed)
                )
                return False

            return True

        except lzma.LZMAError as e:
            self._logger.error("bi5_lzma_decompress_failed", error=str(e))
            return False

    async def get_available_dates(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> list[datetime]:
        """Get list of available dates.

        Args:
            symbol: Trading symbol
            start_date: Start of date range
            end_date: End of date range

        Returns:
            List of datetime objects
        """
        # Placeholder implementation: returns all dates in range
        # In production, this would probe the server for actual availability
        from datetime import timedelta

        dates: list[datetime] = []
        current = start_date

        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)

        return dates