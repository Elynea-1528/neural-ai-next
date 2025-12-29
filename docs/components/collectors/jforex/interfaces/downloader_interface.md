# collectors/jforex/interfaces/downloader_interface.py

JForex Downloader Interface Definition.

## Osztályok

### `IJForexDownloader`

Interface for JForex .bi5 data downloader.
    
    This interface defines the contract for downloading and processing
    Dukascopy's native .bi5 tick data format.


## Függvények

### `download_tick_data`

Download and decode tick data for a specific symbol and date.
        
        Args:
            symbol: Trading symbol (e.g., 'EURUSD', 'GBPUSD')
            date: Date for which to download data
            
        Returns:
            List of TickData objects containing bid/ask prices
            
        Raises:
            DownloadError: If download fails (network issues, server errors)
            DecodeError: If data decoding fails (corrupted file)
            DataNotAvailableError: If data is not available (weekend, holiday)

### `get_available_dates`

Get list of dates with available data for a symbol.
        
        Args:
            symbol: Trading symbol
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of datetime objects for dates with available data

### `validate_bi5_data`

Validate .bi5 data integrity.
        
        Args:
            data: Raw .bi5 data bytes
            
        Returns:
            True if data is valid, False otherwise


---

**Forrásfájl:** [`collectors/jforex/interfaces/downloader_interface.py`](../../../neural_ai/collectors/jforex/interfaces/downloader_interface.py)
