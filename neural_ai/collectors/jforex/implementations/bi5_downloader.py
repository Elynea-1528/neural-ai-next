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
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.tick_data import TickData

if TYPE_CHECKING:
    import aiohttp

    from neural_ai.collectors.jforex.exceptions.jforex_error import (
        DataNotAvailableError,
        DecodeError,
        DownloadError,
    )
    from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
    from neural_ai.collectors.jforex.interfaces.tick_data import TickData
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class Bi5Downloader(IJForexDownloader):
    """JForex Bi5 data downloader implementation.

    Downloads and decodes Dukascopy's native .bi5 tick data format.
    """

    def __init__(
        self,
        logger: "LoggerInterface",
        event_bus: "EventBusInterface | None",
        config: "ConfigManagerInterface",
        http_client: "aiohttp.ClientSession",
        storage: "StorageInterface",
    ):
        """Initialize Bi5 downloader.

        Args:
            logger: Logger instance
            event_bus: Event bus for publishing market data
            config: Configuration manager
            http_client: HTTP client for downloads
            storage: Storage interface for data persistence
        """
        self._logger = logger
        self._event_bus = event_bus
        self._config = config
        self._http_client = http_client
        self._storage = storage
        self._base_url = config.get("jforex", "base_url") or "https://www.dukascopy.com/datafeed"
        if not self._base_url:
            self._base_url = "https://www.dukascopy.com/datafeed"
            self._logger.warning("jforex_base_url_not_set: Using default Dukascopy URL")

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

    def _build_storage_path(self, symbol: str, date: datetime) -> str:
        """Build storage path for tick data.

        Args:
            symbol: Trading symbol
            date: Date for which to store data

        Returns:
            Storage path string
        """
        # Format: data/tick/{SYMBOL}/tick/year={YYYY}/month={MM}/day={DD}/
        # tick_{YYYYMMDD}_{HH}.parquet
        path = (
            f"data/tick/{symbol.upper()}/tick/"
            f"year={date.year}/month={date.month:02d}/day={date.day:02d}/"
            f"tick_{date.strftime('%Y%m%d')}_{date.strftime('%H')}.parquet"
        )
        return path

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
                    self._logger.warning(
                        f"bi5_data_not_available: {url}", url=url, reason="404_not_found"
                    )
                    raise DataNotAvailableError(f"No data available at {url}")

                response.raise_for_status()
                data = await response.read()

                self._logger.debug("bi5_download_success", url=url, size_bytes=len(data))

                return data

        except aiohttp.ClientError as e:
            self._logger.error("bi5_download_failed", url=url, error=str(e))
            raise DownloadError(f"Failed to download {url}: {e}") from e

    def _detect_format(self, decompressed: bytes) -> tuple[int, str]:
        """Detect .bi5 record format dynamically.

        Analyzes the decompressed data to determine if it uses 12-byte or 20-byte records.
        Uses heuristics to distinguish between the two formats.

        Args:
            decompressed: Decompressed .bi5 binary data

        Returns:
            Tuple of (record_size, unpack_format)

        Raises:
            DecodeError: If format detection fails
        """
        # Alapértelmezett: 12 bájtos formátum (timestamp_delta, ask, bid)
        record_size = 12
        unpack_format = ">III"

        # Ha osztható 20-szal, megvizsgáljuk, hogy TÉNYLEG volumen-e
        if len(decompressed) % 20 == 0:
            is_valid_20 = False
            try:
                # Megnézzük az első rekordot
                # >IIIff = Delta(int), Ask(int), Bid(int), AskVol(float), BidVol(float)
                _, _, _, ask_vol, bid_vol = struct.unpack(">IIIff", decompressed[0:20])

                # ZAJ SZŰRÉS: (A manuális_letöltő.py-ból másolva)
                # Egy valódi volumen float nem lehet extrém kicsi (pl 1e-40), hacsak nem nulla.
                # És nem lehet extrém nagy sem.
                valid_ask_vol = (ask_vol == 0) or (0.001 < ask_vol < 1000000000)
                valid_bid_vol = (bid_vol == 0) or (0.001 < bid_vol < 1000000000)

                if valid_ask_vol and valid_bid_vol:
                    is_valid_20 = True
            except Exception:
                pass

            if is_valid_20:
                record_size = 20
                unpack_format = ">IIIff"

        self._logger.info(
            "bi5_format_detected",
            record_size=record_size,
            unpack_format=unpack_format,
            total_bytes=len(decompressed),
        )

        return record_size, unpack_format

    def _process_bi5_data(self, data: bytes, symbol: str, date: datetime) -> list["TickData"]:
        """Process and decode .bi5 binary data with dynamic format detection.

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

            # Dinamikus formátumfelismerés
            record_size, unpack_format = self._detect_format(decompressed)
            num_records = len(decompressed) // record_size

            # Base timestamp: start of the HOUR in milliseconds
            # A .bi5 fájlban lévő delta mindig az adott óra elejétől számítódik
            # A manuális_letöltő.py-ból: date.replace(minute=0, second=0, microsecond=0)
            base_timestamp = int(date.replace(minute=0, second=0, microsecond=0).timestamp()) * 1000

            ticks: list[TickData] = []

            # Metrikaváltozók a statisztikákhoz
            total_records = 0
            skipped_price = 0
            valid_ticks = 0

            # Inicializáljuk a volume változókat, hogy elkerüljük a Pylance hibát
            ask_vol = 0.0
            bid_vol = 0.0

            for i in range(num_records):
                total_records += 1

                offset = i * record_size
                record = decompressed[offset : offset + record_size]

                # Dinamikus unpakolás a detektált formátum alapján
                if record_size == 20:
                    # 20 bájtos formátum: delta, ask, bid, ask_vol, bid_vol
                    # A manuális_letöltő.py-ból: delta, ask_int, bid_int, ask_vol, bid_vol
                    timestamp_delta, ask_int, bid_int, ask_vol, bid_vol = struct.unpack(
                        unpack_format, record
                    )

                    # Logoljuk a volume adatokat, ha érdekesek
                    if i < 5:  # Csak az első 5 rekordot logoljuk
                        self._logger.debug(
                            "bi5_20_byte_record_detected",
                            record_index=i,
                            ask_volume=ask_vol,
                            bid_volume=bid_vol,
                        )

                else:
                    # 12 bájtos formátum: delta, ask, bid
                    timestamp_delta, ask_int, bid_int = struct.unpack(unpack_format, record)
                    ask_vol = 0.0
                    bid_vol = 0.0

                # Convert integer prices to floats
                ask = ask_int / 100000.0
                bid = bid_int / 100000.0

                # Ár szűrés: csak a nullánál nagyobb árakat fogadjuk el
                if bid <= 0.0 or ask <= 0.0:
                    skipped_price += 1
                    continue

                # Dátum validáció: a timestamp_delta nem lehet negatív
                if timestamp_delta < 0:
                    self._logger.warning(
                        "bi5_invalid_timestamp_delta", record_index=i, delta=timestamp_delta
                    )
                    continue

                # Calculate actual timestamp
                timestamp_ms = base_timestamp + timestamp_delta
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)

                # Dátum validáció: a timestamp a kért dátum napján belül kell legyen
                # Megengedjük, hogy az óra végén lévő tick-ek a következő órába essenek
                if timestamp.date() != date.date():
                    self._logger.warning(
                        "bi5_date_mismatch",
                        record_index=i,
                        expected=date.date().isoformat(),
                        actual=(
                            f"{timestamp.date().isoformat()} "
                            f"{timestamp.hour:02d}:{timestamp.minute:02d}"
                        ),
                    )
                    continue

                # Create TickData object
                tick = TickData(
                    timestamp=timestamp,
                    symbol=symbol.upper(),
                    bid=round(bid, 5),  # Forex prices to 5 decimal places
                    ask=round(ask, 5),
                    ask_volume=ask_vol if record_size == 20 else None,
                    bid_volume=bid_vol if record_size == 20 else None,
                    source="jforex",
                )

                ticks.append(tick)
                valid_ticks += 1

            # Statisztika logolása
            self._logger.info(
                "bi5_chunk_stats",
                symbol=symbol,
                date=date.isoformat(),
                total=total_records,
                valid=valid_ticks,
                price_skip=skipped_price,
                record_size=record_size,
            )

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
        if not ticks or not self._event_bus:
            # Ha nincs EventBus (Direct Storage Mode), egyszerűen visszatérünk
            return

        self._logger.info(f"_publish_ticks: {len(ticks)} tick publikálása")

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
                    volume=(tick.ask_volume + tick.bid_volume)
                    if (tick.ask_volume is not None and tick.bid_volume is not None)
                    else None,
                    ask_volume=tick.ask_volume,
                    bid_volume=tick.bid_volume,
                    source=tick.source,
                )
                for tick in batch
            ]

            # Publish each event individually
            for event in events:
                await self._event_bus.publish("market_data", event)

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

        # Build storage path and check if data already exists
        storage_path = self._build_storage_path(symbol, date)

        if self._storage.exists(storage_path):
            # Get metadata to check if file is not empty
            try:
                metadata = self._storage.get_metadata(storage_path)
                file_size = metadata.get("size", 0)

                if file_size > 0:
                    self._logger.info(
                        "data_already_exists",
                        message=f"Data already exists at {storage_path}, skipping download",
                        path=storage_path,
                        size=file_size,
                    )
                    return []  # Return empty list to indicate skip

            except Exception as e:
                self._logger.warning(
                    "metadata_check_failed",
                    message=(
                        f"Failed to check metadata for {storage_path}, proceeding with download"
                    ),
                    error=str(e),
                )

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

    async def close(self) -> None:
        """Bezárja a HTTP klienst.

        Ez a metódus biztosítja, hogy a letöltés végén ne maradjanak
        nyitott kapcsolatok, ami a 'Unclosed client session' hibát okozná.
        """
        if self._http_client and not self._http_client.closed:
            await self._http_client.close()
            self._logger.debug("http_client_closed")
