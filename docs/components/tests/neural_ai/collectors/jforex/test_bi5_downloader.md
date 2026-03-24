# 🧪 Teszt: tests/neural_ai/collectors/jforex/test_bi5_downloader.py

**Tesztelt modul:** [`neural_ai/collectors/jforex/bi5_downloader.py`](../../neural_ai/collectors/jforex/bi5_downloader.py)

Tests for Bi5Downloader implementation.

## Teszt Osztály: `TestBi5Downloader`

Test suite for Bi5Downloader.

### ✓ `test_base_timestamp_calculation_retains_hour()`

Test that base_timestamp calculation correctly retains the hour value. This is a CRITICAL test for the bug fix implemented on 2026.01.03. The previous implementation incorrectly zeroed out the hour (hour=0), which caused incorrect timestamp calculations for hourly .bi5 files. The .bi5 files from Dukascopy are hourly chunks, and the timestamp_delta is always calculated from the START of that specific hour, not from midnight.

### ✓ `test_base_timestamp_calculation_different_hours()`

Test base_timestamp calculation for different hours of the day.

### ✓ `test_process_bi5_data_12_byte_format()`

Test processing of 12-byte format .bi5 data.

### ✓ `test_process_bi5_data_20_byte_format()`

Test processing of 20-byte format .bi5 data.

### ✓ `test_process_bi5_data_empty_file()`

Test handling of empty .bi5 file.

### ✓ `test_process_bi5_data_invalid_prices()`

Test filtering of invalid (non-positive) prices.

### ✓ `test_process_bi5_data_invalid_timestamp_delta()`

Test that the code handles timestamp delta validation (edge case). Note: We cannot create negative timestamp_delta values in struct.pack with unsigned int format, but the actual Bi5Downloader code does check for negative values after unpacking. This test verifies normal operation.

### ✓ `test_process_bi5_data_date_mismatch()`

Test handling of ticks with date mismatch.

### ✓ `test_build_url()`

Test URL building for Dukascopy download.

### ✓ `test_build_storage_path()`

Test storage path building with Master parquet format.

### ✓ `test_download_tick_data_success()`

Test successful download of tick data.

### ✓ `test_download_tick_data_not_available()`

Test handling of 404 (data not available).

### ✓ `test_download_tick_data_already_exists()`

Test skipping download when data already exists.

### ✓ `test_validate_bi5_data_valid()`

Test validation of valid .bi5 data.

### ✓ `test_validate_bi5_data_invalid_size()`

Test validation of data that's too small.

### ✓ `test_validate_bi5_data_invalid_lzma()`

Test validation of invalid LZMA data.

### ✓ `test_validate_bi5_data_empty_decompressed()`

Test validation of LZMA data that decompresses to empty.

### ✓ `test_validate_bi5_data_invalid_record_count()`

Test validation fails for data not divisible by record size.

### ✓ `test_validate_bi5_data_negative_timestamp_delta()`

Test validation fails for negative timestamp delta.

### ✓ `test_validate_bi5_data_invalid_prices()`

Test validation fails for invalid (zero or negative) prices.

### ✓ `test_validate_bi5_data_extreme_prices()`

Test validation fails for extremely small or large prices.

### ✓ `test_validate_bi5_data_20_byte_format()`

Test validation of valid 20-byte format data.

### ✓ `test_validate_bi5_data_20_byte_noise_volumes()`

Test validation fails for 20-byte data with noise volumes.

### ✓ `test_validate_bi5_data_zero_records()`

Test validation fails for data with zero records.

### ✓ `test_close()`

Test closing of HTTP client.

### ✓ `test_detect_format_12_byte_default()`

Test that 12-byte format is the default when both 12 and 20 are divisible.

### ✓ `test_detect_format_20_byte_with_valid_volumes()`

Test that 20-byte format is detected when volumes are valid.

### ✓ `test_detect_format_20_byte_rejects_noise_volumes()`

Test that 20-byte format is rejected when volumes are noise (very small floats).

### ✓ `test_detect_format_20_byte_rejects_zero_volumes()`

Test that 20-byte format is accepted with zero volumes.

### ✓ `test_detect_format_12_byte_only()`

Test that 12-byte format is detected when data is only divisible by 12.

### ✓ `test_download_binary_http_error()`

Test handling of HTTP client errors.

### ✓ `test_download_binary_status_error()`

Test handling of non-404 HTTP errors.

### ✓ `test_detect_format_exception()`

Test exception handling in format detection.

### ✓ `test_process_bi5_data_decode_error()`

Test handling of decode errors.

### ✓ `test_publish_ticks_batching()`

Test that ticks are published in batches.

### ✓ `test_publish_ticks_no_event_bus()`

Test publishing when event_bus is None.

### ✓ `test_download_tick_data_metadata_error()`

Test download proceeds if metadata check fails.

### ✓ `test_validate_bi5_data_first_record_failure()`

Test validation failure on first record checks.

### ✓ `test_process_bi5_data_negative_delta()`

Test processing of data with negative timestamp delta.

### ✓ `test_validate_bi5_data_struct_error()`

Test validation when struct.unpack raises error.

### ✓ `test_validate_bi5_data_large_price()`

Test validation with unrealistically large prices.

### ✓ `test_get_available_dates()`

Test get_available_dates returns correct range.

### ✓ `test_init_default_url()`

Test default URL fallback.

---

**Teszt fájl:** [`tests/neural_ai/collectors/jforex/test_bi5_downloader.py`](../../tests/neural_ai/collectors/jforex/test_bi5_downloader.py)

**Tesztelt modul:** [`neural_ai/collectors/jforex/bi5_downloader.py`](../../neural_ai/collectors/jforex/bi5_downloader.py)
