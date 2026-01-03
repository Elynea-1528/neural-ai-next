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

### `_detect_format`

Detect .bi5 record format dynamically.

        Args:
            decompressed: Decompressed .bi5 binary data

        Returns:
            Tuple of (record_size, unpack_format)

        Raises:
            DecodeError: If format detection fails
        
        Metódus működése:
        - Alapértelmezett: 12 bájtos formátum (timestamp_delta, ask, bid)
        - Heurisztika: ha a hossz osztható 20-szal, ellenőrizzük a 20 bájtos formátumot
        - Smart Check: elemzi az első néhány rekordot
          - Volume validáció: 0 és 100M között kell lennie
          - Delta validáció: 0 és 3,600,000 között kell lennie (max 1 óra)
        - Visszatérés a detektált formátummal (12 vagy 20 bájt)

### `_process_bi5_data`

Process and decode .bi5 binary data with dynamic format detection.

        Args:
            data: Raw .bi5 binary data (LZMA compressed)
            symbol: Trading symbol
            date: Date for which data was downloaded

        Returns:
            List of TickData objects

        Raises:
            DecodeError: If decompression or unpacking fails
        
        Metódus működése:
        - LZMA dekompresszió végrehajtása
        - Dinamikus formátumfelismerés a `_detect_format` metódussal
        - Bináris adatok feldolgozása (12 vagy 20 bájtos rekordok)
        - Ár konverzió (integer -> float, osztás 100000-rel)
        - Időbélyeg számítás (base_timestamp + delta)
        - Szűrés:
          - Ár szűrés: csak pozitív bid/ask árak (bid <= 0.0 or ask <= 0.0 esetén kihagyás)
          - Dátum validáció: timestamp_delta nem lehet negatív
          - Dátum egyezés: timestamp.date() == date.date()
        - Metrikák gyűjtése:
          - `total_records`: Összes feldolgozott rekord
          - `skipped_price`: Ár szűrés miatt kihagyott rekordok
          - `valid_ticks`: Érvényes tick-ek száma
          - `record_size`: Detektált rekord méret (12 vagy 20)
        - Statisztika logolás: `bi5_chunk_stats` (INFO szint)
        - Volume adatok logolása (ha 20 bájtos formátum)

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
