"""JForex Downloader Interface Definition."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.tick_data import TickData


class IJForexDownloader(ABC):
    """Interface for JForex .bi5 data downloader.

    This interface defines the contract for downloading and processing
    Dukascopy's native .bi5 tick data format.
    """

    @abstractmethod
    async def download_tick_data(self, symbol: str, date: datetime) -> list["TickData"]:
        """Download and decode tick data for a specific symbol and date.

        Args:
            symbol: Trading symbol (e.g., 'EURUSD', 'GBPUSD')
            date: Date for which to download data

        Returns:
            List of TickData objects containing bid/ask prices

        Raises:
            DownloadError: If download fails (network issues, server errors)
            DecodeError: If data decoding fails (corrupted file)
            DataNotAvailableError: If data is not available (weekend, holiday)
        """
        pass

    @abstractmethod
    async def get_available_dates(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> list[datetime]:
        """Get list of dates with available data for a symbol.

        Args:
            symbol: Trading symbol
            start_date: Start of date range
            end_date: End of date range

        Returns:
            List of datetime objects for dates with available data
        """
        pass

    @abstractmethod
    def validate_bi5_data(self, data: bytes) -> bool:
        """Validate .bi5 data integrity.

        Args:
            data: Raw .bi5 data bytes

        Returns:
            True if data is valid, False otherwise
        """
        pass
