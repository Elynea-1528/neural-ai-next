"""JForex Collector Exceptions."""


class JForexError(Exception):
    """Base exception for all JForex Collector errors."""

    pass


class DownloadError(JForexError):
    """Raised when data download fails.

    This includes network errors, server errors, and timeout issues.
    """

    pass


class DecodeError(JForexError):
    """Raised when .bi5 data decoding fails.

    This includes LZMA decompression errors and struct unpacking errors.
    """

    pass


class DataNotAvailableError(JForexError):
    """Raised when data is not available for the requested date.

    This typically occurs on weekends, holidays, or when the market was closed.
    """

    pass
