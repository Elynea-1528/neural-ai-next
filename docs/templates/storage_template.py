"""Template for Neural-AI-Next storage components.

This file contains a storage component template that handles
storing and managing different types of data.
"""

import datetime as dt
import json
import os
from typing import Any, Protocol, cast

import pandas as pd
from pandas import DataFrame

from neural_ai.core.logger import LoggerInterface
from neural_ai.core.logger.implementations import LoggerFactory


class StorageInterface(Protocol):
    """Interface for storage implementations."""

    def save_raw_data(
        self, data: DataFrame, symbol: str, timeframe: str, overwrite: bool = False
    ) -> bool:
        """Save raw data.

        Args:
            data: Data to save in DataFrame format
            symbol: Symbol (e.g., 'EURUSD')
            timeframe: Timeframe (e.g., 'M1', 'H1', 'D1')
            overwrite: If True, overwrites existing data

        Returns:
            bool: True if save was successful

        Raises:
            StorageError: When storage operation fails
        """
        ...

    def load_raw_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
        columns: list[str] | None = None,
    ) -> DataFrame:
        """Load raw data.

        Args:
            symbol: Symbol (e.g., 'EURUSD')
            timeframe: Timeframe (e.g., 'M1', 'H1', 'D1')
            start_date: Start date for filtering
            end_date: End date for filtering
            columns: Columns to load

        Returns:
            pd.DataFrame: Loaded data

        Raises:
            DataNotFoundError: When data is not found
            StorageError: When other storage error occurs
        """
        ...


class StorageError(Exception):
    """Base exception for storage operations."""


class DataNotFoundError(StorageError):
    """Exception raised when requested data is not found."""


class InvalidFormatError(StorageError):
    """Exception raised when format is not supported."""


class StorageImplementation:
    """Storage template implementation."""

    def __init__(self, config: dict[str, Any], logger: LoggerInterface | None = None) -> None:
        """Initialize storage template.

        Args:
            config: Configuration settings
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)

        # Read configuration values
        self.base_path = config.get("base_path", "data")
        self.format = config.get("format", "csv")

        # Create base directory
        os.makedirs(self.base_path, exist_ok=True)

    def _get_path(self, symbol: str, timeframe: str, data_type: str = "raw") -> str:
        """Generate file path.

        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            data_type: Data type (raw, processed)

        Returns:
            str: File path

        Raises:
            InvalidFormatError: When format is not supported
        """
        if data_type == "raw":
            directory = os.path.join(self.base_path, "raw", symbol, timeframe)
        else:
            directory = os.path.join(self.base_path, "processed", data_type, symbol, timeframe)

        os.makedirs(directory, exist_ok=True)

        if self.format == "csv":
            filename = "data.csv"
        elif self.format == "hdf":
            filename = "data.h5"
        elif self.format == "json":
            filename = "data.json"
        else:
            raise InvalidFormatError(f"Unsupported format: {self.format}")

        return os.path.join(directory, filename)

    def save_raw_data(
        self, data: DataFrame, symbol: str, timeframe: str, overwrite: bool = False
    ) -> bool:
        """Save raw data.

        Args:
            data: Data to save in DataFrame format
            symbol: Symbol (e.g., 'EURUSD')
            timeframe: Timeframe (e.g., 'M1', 'H1', 'D1')
            overwrite: If True, overwrites existing data

        Returns:
            bool: True if save was successful

        Raises:
            StorageError: When storage operation fails
        """
        try:
            path = self._get_path(symbol, timeframe, "raw")

            if self.format == "csv":
                data.to_csv(path)
            elif self.format == "hdf":
                data.to_hdf(path, key="data", mode="w")
            elif self.format == "json":
                data.to_json(path, orient="records", date_format="iso")

            self.logger.info(f"Raw data saved: {symbol} {timeframe}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving raw data: {str(e)}")
            raise StorageError(f"Data save error: {str(e)}") from e

    def load_raw_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
        columns: list[str] | None = None,
    ) -> DataFrame:
        """Load raw data.

        Args:
            symbol: Symbol (e.g., 'EURUSD')
            timeframe: Timeframe (e.g., 'M1', 'H1', 'D1')
            start_date: Start date for filtering
            end_date: End date for filtering
            columns: Columns to load

        Returns:
            pd.DataFrame: Loaded data

        Raises:
            DataNotFoundError: When data is not found
            StorageError: When other storage error occurs
        """
        try:
            path = self._get_path(symbol, timeframe, "raw")

            if not os.path.exists(path):
                raise DataNotFoundError(f"No data found for: {symbol} {timeframe}")

            if self.format == "csv":
                data: DataFrame = pd.read_csv(path, index_col=0, parse_dates=True)
            elif self.format == "hdf":
                data = cast(DataFrame, pd.read_hdf(path, key="data"))
            elif self.format == "json":
                data = pd.read_json(path, orient="records", convert_dates=True)

            if start_date is not None or end_date is not None:
                data = self._filter_by_date(data, start_date, end_date)

            if columns is not None:
                data = cast(DataFrame, data[columns])

            self.logger.info(f"Raw data loaded: {symbol} {timeframe}")
            return data

        except DataNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Error loading raw data: {str(e)}")
            raise StorageError(f"Data load error: {str(e)}") from e

    def _filter_by_date(
        self,
        data: DataFrame,
        start_date: str | dt.datetime | None,
        end_date: str | dt.datetime | None,
    ) -> DataFrame:
        """Filter DataFrame by date.

        Args:
            data: DataFrame to filter
            start_date: Start date
            end_date: End date

        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        filtered_data = data

        if start_date is not None:
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date)
            filtered_data = cast(DataFrame, filtered_data[filtered_data.index >= start_date])

        if end_date is not None:
            if isinstance(end_date, str):
                end_date = pd.to_datetime(end_date)
            filtered_data = cast(DataFrame, filtered_data[filtered_data.index <= end_date])

        return filtered_data

    def has_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
    ) -> bool:
        """Check if data exists for given symbol and timeframe.

        Args:
            symbol: Symbol (e.g., 'EURUSD')
            timeframe: Timeframe (e.g., 'M1', 'H1', 'D1')
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            bool: True if data exists, False otherwise
        """
        path = self._get_path(symbol, timeframe, "raw")
        if not os.path.exists(path):
            return False

        if start_date is None and end_date is None:
            return True

        return self._check_date_range_exists(path, start_date, end_date)

    def _check_date_range_exists(
        self,
        path: str,
        start_date: str | dt.datetime | None,
        end_date: str | dt.datetime | None,
    ) -> bool:
        """Check if given date range exists in file.

        Args:
            path: File path
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            bool: True if date range exists, False otherwise
        """
        try:
            if self.format == "csv":
                df = cast(
                    DataFrame,
                    pd.read_csv(path, index_col=0, parse_dates=True, usecols=[0]),
                )
                min_date = df.index.min()
                max_date = df.index.max()
            elif self.format == "hdf":
                store = pd.HDFStore(path, mode="r")
                try:
                    min_date = store.select("data", start=0, stop=1).index.min()
                    max_date = store.select("data", start=-1, stop=None).index.max()
                finally:
                    store.close()
            else:  # json
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
                df.index = pd.to_datetime(df.index)
                min_date = df.index.min()
                max_date = df.index.max()

            if isinstance(start_date, str):
                start_date = pd.Timestamp(start_date)
            if isinstance(end_date, str):
                end_date = pd.Timestamp(end_date)

            if start_date is not None and max_date < start_date:
                return False
            if end_date is not None and min_date > end_date:
                return False

            return True

        except Exception as e:
            self.logger.warning(f"Error checking date range: {str(e)}")
            return False
