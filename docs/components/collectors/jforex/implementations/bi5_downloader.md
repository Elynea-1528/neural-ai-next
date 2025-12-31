# collectors/jforex/implementations/bi5_downloader.py

Bi5 Downloader Implementation.

## Osztályok

### `Bi5Downloader`

JForex Bi5 data downloader implementation.

    Downloads and decodes Dukascopy's native .bi5 tick data format.


## Függvények

### `__init__`

Initialize Bi5 downloader.

        Args:
            logger: Logger instance
            event_bus: Event bus for publishing market data
            config: Configuration manager
            http_client: HTTP client for downloads
            storage: Storage interface for data persistence

### `_build_url`

Build Dukascopy .bi5 download URL.

        Args:
            symbol: Trading symbol (e.g., 'EURUSD')
            date: Date for which to download data

        Returns:
            Complete download URL

### `_build_storage_path`

Build storage path for tick data.

        Args:
            symbol: Trading symbol
            date: Date for which to store data

        Returns:
            Storage path string

### `_download_binary`

Download binary .bi5 data from Dukascopy.

        Args:
            url: Complete download URL

        Returns:
            Raw .bi5 binary data

        Raises:
            DataNotAvailableError: If server returns 404 (weekend/holiday)
            DownloadError: If network error occurs

### `_process_bi5_data`

Process and decode .bi5 binary data.

        Args:
            data: Raw .bi5 binary data (LZMA compressed)
            symbol: Trading symbol
            date: Date for which data was downloaded

        Returns:
            List of TickData objects

        Raises:
            DecodeError: If decompression or unpacking fails

### `_publish_ticks`

Publish tick data to EventBus.

        Args:
            ticks: List of TickData objects to publish

### `download_tick_data`

Download and decode tick data.

        Args:
            symbol: Trading symbol
            date: Date for which to download data

        Returns:
            List of TickData objects

        Raises:
            DownloadError: If download fails
            DecodeError: If decoding fails
            DataNotAvailableError: If data not available

### `validate_bi5_data`

Validate .bi5 data integrity.

        Args:
            data: Raw .bi5 data bytes

        Returns:
            True if data is valid

### `get_available_dates`

Get list of available dates.

        Args:
            symbol: Trading symbol
            start_date: Start of date range
            end_date: End of date range

        Returns:
            List of datetime objects


---

**Forrásfájl:** [`collectors/jforex/implementations/bi5_downloader.py`](../../../neural_ai/collectors/jforex/implementations/bi5_downloader.py)
