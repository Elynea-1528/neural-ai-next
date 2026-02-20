# tests/neural_ai/collectors/jforex/test_bi5_downloader.py

Tests for Bi5Downloader implementation.

## Importok

```python
import lzma
import struct
from datetime import UTC
from datetime import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from aiohttp import ClientError
from neural_ai.collectors.jforex.exceptions.jforex_error import DataNotAvailableError
# ... és még 3 import
```

## Osztály: `TestBi5Downloader`

Test suite for Bi5Downloader.

### Metódusok

#### `mock_dependencies()`

```python
def mock_dependencies(self)
```

Create mock dependencies for Bi5Downloader.

**Paraméterek:**

- **`self`**

#### `downloader()`

```python
def downloader(self, mock_dependencies)
```

Create Bi5Downloader instance with mocked dependencies.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `create_bi5_data_12_byte()`

```python
def create_bi5_data_12_byte(self, timestamps_delta: list[int], ask: list[int], bid: list[int]) -> bytes
```

Create mock .bi5 data with 12-byte records.

**Paraméterek:**

- **`self`**
- **`timestamps_delta`** (`list[int]`): List of timestamp deltas in milliseconds
- **`ask`** (`list[int]`): List of ask prices as integers
- **`bid`** (`list[int]`): List of bid prices as integers

**Visszatérési érték:**

- Típus: `bytes`
- LZMA compressed .bi5 data

#### `create_bi5_data_20_byte()`

```python
def create_bi5_data_20_byte(self, timestamps_delta: list[int], ask: list[int], bid: list[int], ask_vol: list[float], bid_vol: list[float]) -> bytes
```

Create mock .bi5 data with 20-byte records.

**Paraméterek:**

- **`self`**
- **`timestamps_delta`** (`list[int]`): List of timestamp deltas in milliseconds
- **`ask`** (`list[int]`): List of ask prices as integers
- **`bid`** (`list[int]`): List of bid prices as integers
- **`ask_vol`** (`list[float]`): List of ask volumes as floats
- **`bid_vol`** (`list[float]`): List of bid volumes as floats

**Visszatérési érték:**

- Típus: `bytes`
- LZMA compressed .bi5 data

#### `test_base_timestamp_calculation_retains_hour()`

```python
def test_base_timestamp_calculation_retains_hour(self, downloader)
```

Test that base_timestamp calculation correctly retains the hour value. This is a CRITICAL test for the bug fix implemented on 2026.01.03. The previous implementation incorrectly zeroed out the hour (hour=0), which caused incorrect timestamp calculations for hourly .bi5 files. The .bi5 files from Dukascopy are hourly chunks, and the timestamp_delta is always calculated from the START of that specific hour, not from midnight.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_base_timestamp_calculation_different_hours()`

```python
def test_base_timestamp_calculation_different_hours(self, downloader)
```

Test base_timestamp calculation for different hours of the day.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_12_byte_format()`

```python
def test_process_bi5_data_12_byte_format(self, downloader)
```

Test processing of 12-byte format .bi5 data.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_20_byte_format()`

```python
def test_process_bi5_data_20_byte_format(self, downloader)
```

Test processing of 20-byte format .bi5 data.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_empty_file()`

```python
def test_process_bi5_data_empty_file(self, downloader)
```

Test handling of empty .bi5 file.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_invalid_prices()`

```python
def test_process_bi5_data_invalid_prices(self, downloader)
```

Test filtering of invalid (non-positive) prices.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_invalid_timestamp_delta()`

```python
def test_process_bi5_data_invalid_timestamp_delta(self, downloader)
```

Test that the code handles timestamp delta validation (edge case). Note: We cannot create negative timestamp_delta values in struct.pack with unsigned int format, but the actual Bi5Downloader code does check for negative values after unpacking. This test verifies normal operation.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_date_mismatch()`

```python
def test_process_bi5_data_date_mismatch(self, downloader)
```

Test handling of ticks with date mismatch.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_build_url()`

```python
def test_build_url(self, downloader)
```

Test URL building for Dukascopy download.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_build_storage_path()`

```python
def test_build_storage_path(self, downloader)
```

Test storage path building with Master parquet format.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_download_tick_data_success()`

```python
async def test_download_tick_data_success(self, mock_dependencies)
```

Test successful download of tick data.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_download_tick_data_not_available()`

```python
async def test_download_tick_data_not_available(self, mock_dependencies)
```

Test handling of 404 (data not available).

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_download_tick_data_already_exists()`

```python
async def test_download_tick_data_already_exists(self, mock_dependencies)
```

Test skipping download when data already exists.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_validate_bi5_data_valid()`

```python
def test_validate_bi5_data_valid(self, downloader)
```

Test validation of valid .bi5 data.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_invalid_size()`

```python
def test_validate_bi5_data_invalid_size(self, downloader)
```

Test validation of data that's too small.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_invalid_lzma()`

```python
def test_validate_bi5_data_invalid_lzma(self, downloader)
```

Test validation of invalid LZMA data.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_empty_decompressed()`

```python
def test_validate_bi5_data_empty_decompressed(self, downloader)
```

Test validation of LZMA data that decompresses to empty.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_invalid_record_count()`

```python
def test_validate_bi5_data_invalid_record_count(self, downloader)
```

Test validation fails for data not divisible by record size.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_negative_timestamp_delta()`

```python
def test_validate_bi5_data_negative_timestamp_delta(self, downloader)
```

Test validation fails for negative timestamp delta.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_invalid_prices()`

```python
def test_validate_bi5_data_invalid_prices(self, downloader)
```

Test validation fails for invalid (zero or negative) prices.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_extreme_prices()`

```python
def test_validate_bi5_data_extreme_prices(self, downloader)
```

Test validation fails for extremely small or large prices.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_20_byte_format()`

```python
def test_validate_bi5_data_20_byte_format(self, downloader)
```

Test validation of valid 20-byte format data.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_20_byte_noise_volumes()`

```python
def test_validate_bi5_data_20_byte_noise_volumes(self, downloader)
```

Test validation fails for 20-byte data with noise volumes.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_zero_records()`

```python
def test_validate_bi5_data_zero_records(self, downloader)
```

Test validation fails for data with zero records.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_close()`

```python
async def test_close(self, mock_dependencies)
```

Test closing of HTTP client.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_detect_format_12_byte_default()`

```python
def test_detect_format_12_byte_default(self, downloader)
```

Test that 12-byte format is the default when both 12 and 20 are divisible.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_detect_format_20_byte_with_valid_volumes()`

```python
def test_detect_format_20_byte_with_valid_volumes(self, downloader)
```

Test that 20-byte format is detected when volumes are valid.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_detect_format_20_byte_rejects_noise_volumes()`

```python
def test_detect_format_20_byte_rejects_noise_volumes(self, downloader)
```

Test that 20-byte format is rejected when volumes are noise (very small floats).

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_detect_format_20_byte_rejects_zero_volumes()`

```python
def test_detect_format_20_byte_rejects_zero_volumes(self, downloader)
```

Test that 20-byte format is accepted with zero volumes.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_detect_format_12_byte_only()`

```python
def test_detect_format_12_byte_only(self, downloader)
```

Test that 12-byte format is detected when data is only divisible by 12.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_download_binary_http_error()`

```python
async def test_download_binary_http_error(self, mock_dependencies)
```

Test handling of HTTP client errors.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_download_binary_status_error()`

```python
async def test_download_binary_status_error(self, mock_dependencies)
```

Test handling of non-404 HTTP errors.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_detect_format_exception()`

```python
def test_detect_format_exception(self, downloader)
```

Test exception handling in format detection.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_decode_error()`

```python
def test_process_bi5_data_decode_error(self, downloader)
```

Test handling of decode errors.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_publish_ticks_batching()`

```python
async def test_publish_ticks_batching(self, mock_dependencies)
```

Test that ticks are published in batches.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_publish_ticks_no_event_bus()`

```python
async def test_publish_ticks_no_event_bus(self, mock_dependencies)
```

Test publishing when event_bus is None.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_download_tick_data_metadata_error()`

```python
async def test_download_tick_data_metadata_error(self, mock_dependencies)
```

Test download proceeds if metadata check fails.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

#### `test_validate_bi5_data_first_record_failure()`

```python
def test_validate_bi5_data_first_record_failure(self, downloader)
```

Test validation failure on first record checks.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_process_bi5_data_negative_delta()`

```python
def test_process_bi5_data_negative_delta(self, downloader)
```

Test processing of data with negative timestamp delta.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_struct_error()`

```python
def test_validate_bi5_data_struct_error(self, downloader)
```

Test validation when struct.unpack raises error.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_validate_bi5_data_large_price()`

```python
def test_validate_bi5_data_large_price(self, downloader)
```

Test validation with unrealistically large prices.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_get_available_dates()`

```python
async def test_get_available_dates(self, downloader)
```

Test get_available_dates returns correct range.

**Paraméterek:**

- **`self`**
- **`downloader`**

#### `test_init_default_url()`

```python
def test_init_default_url(self, mock_dependencies)
```

Test default URL fallback.

**Paraméterek:**

- **`self`**
- **`mock_dependencies`**

---

**Forrásfájl:** [`tests/neural_ai/collectors/jforex/test_bi5_downloader.py`](../../tests/neural_ai/collectors/jforex/test_bi5_downloader.py)
