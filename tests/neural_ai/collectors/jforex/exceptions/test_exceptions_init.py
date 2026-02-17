"""Tests for JForex exceptions __init__.py exports."""

from neural_ai.collectors.jforex.exceptions import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
    JForexError,
)


class TestJForexExceptionsInit:
    """Test cases for JForex exceptions exports."""

    def test_jforexerror_exported(self) -> None:
        """Test that JForexError is exported."""
        assert JForexError is not None
        assert issubclass(JForexError, Exception)

    def test_downloaderror_exported(self) -> None:
        """Test that DownloadError is exported."""
        assert DownloadError is not None
        assert issubclass(DownloadError, JForexError)

    def test_decodeerror_exported(self) -> None:
        """Test that DecodeError is exported."""
        assert DecodeError is not None
        assert issubclass(DecodeError, JForexError)

    def test_datanotavailableerror_exported(self) -> None:
        """Test that DataNotAvailableError is exported."""
        assert DataNotAvailableError is not None
        assert issubclass(DataNotAvailableError, JForexError)

    def test_exception_instantiation(self) -> None:
        """Test that exceptions can be instantiated with messages."""
        download_error = DownloadError("Network error")
        decode_error = DecodeError("LZMA decompression failed")
        data_not_available_error = DataNotAvailableError("No data for weekend")

        assert str(download_error) == "Network error"
        assert str(decode_error) == "LZMA decompression failed"
        assert str(data_not_available_error) == "No data for weekend"
