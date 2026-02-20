# neural_ai/collectors/jforex/implementations/bi5_downloader.py

Bi5 Downloader Implementation.

## Importok

```python
import lzma
import struct
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
import aiohttp
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from neural_ai.collectors.jforex.exceptions.jforex_error import DataNotAvailableError
# ... és még 10 import
```

## Osztály: `Bi5Downloader(IJForexDownloader)`

JForex Bi5 adat letöltő implementáció.

Letölti és dekódolja a Dukascopy natív .bi5 tick adat formátumát.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', event_bus: 'EventBusInterface | None', config: 'ConfigManagerInterface', http_client: 'aiohttp.ClientSession', storage: 'StorageInterface')
```

Initialize Bi5 downloader.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): Logger instance
- **`event_bus`** (`'EventBusInterface | None'`): Event bus for publishing market data
- **`config`** (`'ConfigManagerInterface'`): Configuration manager
- **`http_client`** (`'aiohttp.ClientSession'`): HTTP client for downloads
- **`storage`** (`'StorageInterface'`): Storage interface for data persistence

#### `_build_url()`

```python
def _build_url(self, symbol: str, date: datetime) -> str
```

Build Dukascopy .bi5 download URL.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Trading symbol (e.g., 'EURUSD')
- **`date`** (`datetime`): Date for which to download data

**Visszatérési érték:**

- Típus: `str`
- Complete download URL

#### `_build_storage_path()`

```python
def _build_storage_path(self, symbol: str, date: datetime) -> str
```

Build storage path for tick data.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Trading symbol
- **`date`** (`datetime`): Date for which to store data

**Visszatérési érték:**

- Típus: `str`
- Storage path string

#### `_download_binary()`

```python
async def _download_binary(self, url: str) -> bytes
```

Download binary .bi5 data from Dukascopy.

**Paraméterek:**

- **`self`**
- **`url`** (`str`): Complete download URL

**Visszatérési érték:**

- Típus: `bytes`
- Raw .bi5 binary data

**Kivételek:**

- **`DataNotAvailableError`**: If server returns 404 (weekend/holiday)
- **`DownloadError`**: If network error occurs

#### `_detect_format()`

```python
def _detect_format(self, decompressed: bytes) -> tuple[int, str]
```

Detect .bi5 record format dynamically. Analyzes the decompressed data to determine if it uses 12-byte or 20-byte records. Uses heuristics to distinguish between the two formats.

**Paraméterek:**

- **`self`**
- **`decompressed`** (`bytes`): Decompressed .bi5 binary data

**Visszatérési érték:**

- Típus: `tuple[int, str]`
- Tuple of (record_size, unpack_format)

**Kivételek:**

- **`DecodeError`**: If format detection fails

#### `_process_bi5_data()`

```python
def _process_bi5_data(self, data: bytes, symbol: str, date: datetime) -> list['TickData']
```

Process and decode .bi5 binary data with dynamic format detection.

**Paraméterek:**

- **`self`**
- **`data`** (`bytes`): Raw .bi5 binary data (LZMA compressed)
- **`symbol`** (`str`): Trading symbol
- **`date`** (`datetime`): Date for which data was downloaded

**Visszatérési érték:**

- Típus: `list['TickData']`
- List of TickData objects

**Kivételek:**

- **`DecodeError`**: If decompression or unpacking fails

#### `_publish_ticks()`

```python
async def _publish_ticks(self, ticks: list['TickData']) -> None
```

Publish tick data to EventBus.

**Paraméterek:**

- **`self`**
- **`ticks`** (`list['TickData']`): List of TickData objects to publish

**Visszatérési érték:**

- Típus: `None`

#### `download_tick_data()`

```python
async def download_tick_data(self, symbol: str, date: datetime) -> list['TickData']
```

Download and decode tick data.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Trading symbol
- **`date`** (`datetime`): Date for which to download data

**Visszatérési érték:**

- Típus: `list['TickData']`
- List of TickData objects

**Kivételek:**

- **`DownloadError`**: If download fails
- **`DecodeError`**: If decoding fails
- **`DataNotAvailableError`**: If data not available

#### `validate_bi5_data()`

```python
def validate_bi5_data(self, data: bytes) -> bool
```

Validate .bi5 data integrity with comprehensive checks. Performs full validation including LZMA decompression, format detection, record structure validation, and price/timestamp sanity checks.

**Paraméterek:**

- **`self`**
- **`data`** (`bytes`): Raw .bi5 data bytes

**Visszatérési érték:**

- Típus: `bool`
- True if data is valid, False otherwise

#### `get_available_dates()`

```python
async def get_available_dates(self, symbol: str, start_date: datetime, end_date: datetime) -> list[datetime]
```

Get list of available dates.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Trading symbol
- **`start_date`** (`datetime`): Start of date range
- **`end_date`** (`datetime`): End of date range

**Visszatérési érték:**

- Típus: `list[datetime]`
- List of datetime objects

#### `close()`

```python
async def close(self) -> None
```

Bezárja a HTTP klienst. Ez a metódus biztosítja, hogy a letöltés végén ne maradjanak nyitott kapcsolatok, ami a 'Unclosed client session' hibát okozná.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/collectors/jforex/implementations/bi5_downloader.py`](../../neural_ai/collectors/jforex/implementations/bi5_downloader.py)
