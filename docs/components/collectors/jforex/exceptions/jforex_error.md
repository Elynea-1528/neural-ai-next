# collectors/jforex/exceptions/jforex_error.py

JForex Collector Exceptions.

## Osztályok

### `JForexError`

Base exception for all JForex Collector errors.

### `DownloadError`

Raised when data download fails.
    
    This includes network errors, server errors, and timeout issues.

### `DecodeError`

Raised when .bi5 data decoding fails.
    
    This includes LZMA decompression errors and struct unpacking errors.

### `DataNotAvailableError`

Raised when data is not available for the requested date.
    
    This typically occurs on weekends, holidays, or when the market was closed.


---

**Forrásfájl:** [`collectors/jforex/exceptions/jforex_error.py`](../../../neural_ai/collectors/jforex/exceptions/jforex_error.py)
