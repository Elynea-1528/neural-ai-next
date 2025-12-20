# Dead-Letter-Queue (DLQ) Documentation

## Overview

The Dead-Letter-Queue (DLQ) is a critical component for handling corrupted or failed data in the MT5 Collector system. It provides a robust mechanism for:

- **Structured logging** of all data processing failures
- **Retry capabilities** for transient failures
- **Statistics and monitoring** of failure patterns
- **Atomic write guarantees** for data integrity
- **File rotation** to prevent unlimited growth

## Architecture

### Components

```
DeadLetterQueue
├── dlq_directory: Path
├── max_file_size: int (100MB default)
├── current_file: Path
├── record_failure() - Atomically record a failure
├── get_failures() - Retrieve failed entries
├── get_statistics() - Get comprehensive stats
└── mark_as_processed() - Mark entry as processed
```

### Data Flow

```
[Data Processing] → [Failure Detected] → [DLQ.record_failure()]
                                                    ↓
                                            [JSONL File]
                                                    ↓
                                    [Structured Error Entry]
                                                    ↓
                            [Retry Mechanism / Manual Analysis]
```

## Usage

### Initialization

```python
from neural_ai.collectors.mt5 import DeadLetterQueue
from pathlib import Path

# Initialize DLQ
dlq_directory = Path("data/collectors/mt5/dlq")
dlq = DeadLetterQueue(dlq_directory, max_file_size_mb=100)
```

### Recording Failures

```python
from neural_ai.collectors.mt5.exceptions import MT5DataValidationError

# Record a retryable failure
error = MT5DataValidationError("Invalid tick data")
dlq.record_failure(
    data={'symbol': 'EURUSD', 'price': 1.1234},
    error=error,
    context={'timeframe': 'TICK', 'symbol': 'EURUSD'},
    retryable=True
)

# Record a non-retryable failure (permanent error)
error = MT5DataValidationError("Corrupted data structure")
dlq.record_failure(
    data={'symbol': 'GBPUSD'},
    error=error,
    context={'timeframe': 'H1'},
    retryable=False
)
```

### Retrieving Failures

```python
# Get all retryable failures
retryable_failures = dlq.get_failures(retryable_only=True)

# Get all failures (including non-retryable)
all_failures = dlq.get_failures(retryable_only=False)

# Get limited number of failures
recent_failures = dlq.get_failures(retryable_only=True, limit=10)
```

### Getting Statistics

```python
# Get comprehensive DLQ statistics
stats = dlq.get_statistics()

print(f"Total failures: {stats['total_entries']}")
print(f"Retryable: {stats['retryable_entries']}")
print(f"Non-retryable: {stats['non_retryable_entries']}")
print(f"Error types: {stats['error_types']}")
print(f"Oldest entry: {stats['oldest_entry']}")
print(f"Newest entry: {stats['newest_entry']}")
```

### Marking as Processed

```python
# Get failures
failures = dlq.get_failures(retryable_only=True)

# Process a failure
for failure in failures:
    # ... process the failure ...

    # Mark as processed
    dlq.mark_as_processed(failure['timestamp'])
```

## Integration with MT5Collector

### Automatic DLQ Recording

The MT5Collector automatically records failures to DLQ in several scenarios:

1. **Tick Data Processing Errors**
   ```python
   def _process_tick_data(self, symbol: str) -> None:
       try:
           # Process tick data
           ...
       except Exception as e:
           self._dlq.record_failure(
               data={'symbol': symbol},
               error=e,
               context={'timeframe': 'TICK', 'symbol': symbol},
               retryable=isinstance(e, (MT5ConnectionError, MT5TimeoutError))
           )
   ```

2. **Historical Data Fetch Errors**
   ```python
   def _fetch_historical_data(self, symbol: str, timeframe: int, start: int, end: int):
       try:
           # Fetch historical data
           ...
       except Exception as e:
           self._dlq.record_failure(
               data={'symbol': symbol, 'timeframe': timeframe, 'start': start, 'end': end},
               error=e,
               context={'timeframe': timeframe, 'symbol': symbol},
               retryable=isinstance(e, (MT5ConnectionError, MT5TimeoutError))
           )
           raise
   ```

### Retrying Failed Data

```python
# Retry processing failed data
collector = MT5Collector(config)
stats = collector.retry_failed_data(max_retries=3)

print(f"Total retried: {stats['total_retried']}")
print(f"Successful: {stats['successful']}")
print(f"Failed: {stats['failed']}")
print(f"Errors: {stats['errors']}")
```

### Monitoring DLQ Status

```python
# Get DLQ statistics
stats = collector.get_dlq_statistics()
print(f"DLQ Status: {stats}")

# Get connection status with DLQ info
status = collector.get_connection_status()
print(f"DLQ Info: {status['dlq']}")
```

## Integration with ErrorHandler

The ErrorHandler can also record errors to DLQ:

```python
from neural_ai.collectors.mt5.error_handler import ErrorHandler

error_handler = ErrorHandler(logger=logger)

# Store error to both ErrorHandler and DLQ
error_handler.store_error_to_file(
    error=exception,
    context={'symbol': 'EURUSD', 'operation': 'data_processing'},
    collector=mt5_collector_instance
)
```

## File Format

### JSONL Structure

Each DLQ entry is stored as a JSON line:

```json
{
  "timestamp": "2025-12-18T19:30:00.123456",
  "retryable": true,
  "error_type": "MT5DataValidationError",
  "error_message": "Invalid tick data received",
  "data": {
    "symbol": "EURUSD",
    "price": 1.1234
  },
  "context": {
    "timeframe": "TICK",
    "symbol": "EURUSD"
  },
  "stack_trace": "Traceback (most recent call last)..."
}
```

### File Naming Convention

```
corrupted_ticks_YYYYMMDD_HHMMSS.jsonl
```

Example: `corrupted_ticks_20251218_193000.jsonl`

## File Rotation

The DLQ automatically rotates files when they reach the maximum size:

- **Default max size**: 100MB
- **Configurable**: `DeadLetterQueue(dlq_directory, max_file_size_mb=50)`
- **Rotation strategy**: New file created with current timestamp

## Error Types

### Retryable Errors

These errors are marked as `retryable=True` and can be automatically retried:

- `MT5ConnectionError` - Network connectivity issues
- `MT5TimeoutError` - Request timeout issues
- `MT5SocketError` - Socket communication issues

### Non-Retryable Errors

These errors are marked as `retryable=False` and require manual intervention:

- `MT5DataValidationError` - Corrupted or invalid data
- `ConfigurationError` - Configuration issues
- `StorageError` - Storage system errors

## Best Practices

### 1. Regular Monitoring

```python
# Monitor DLQ regularly
stats = collector.get_dlq_statistics()
if stats['total_entries'] > 100:
    # Alert: High failure rate
    send_alert("High DLQ failure rate detected")
```

### 2. Scheduled Retry

```python
# Schedule retry during off-peak hours
import schedule

def retry_failed_data_job():
    stats = collector.retry_failed_data(max_retries=3)
    logger.info(f"Retry job completed: {stats}")

schedule.every().day.at("02:00").do(retry_failed_data_job)
```

### 3. Error Analysis

```python
# Analyze error patterns
stats = collector.get_dlq_statistics()
error_types = stats['error_types']

for error_type, count in error_types.items():
    if count > 50:
        logger.warning(f"High frequency of {error_type}: {count} occurrences")
```

### 4. Cleanup Old Entries

```python
# Periodically clean up old non-retryable entries
import os
from datetime import datetime, timedelta

dlq_files = list(dlq_directory.glob('corrupted_ticks_*.jsonl'))
for file in dlq_files:
    file_time = datetime.fromtimestamp(file.stat().st_mtime)
    if datetime.now() - file_time > timedelta(days=30):
        # Archive or delete old files
        archive_file(file)
```

## Configuration

### DLQ Directory Structure

```
data/
├── collectors/
│   └── mt5/
│       ├── raw/
│       │   ├── ticks/
│       │   ├── ohlcv/
│       │   └── dlq/              # DLQ files
│       │       ├── corrupted_ticks_20251218_193000.jsonl
│       │       └── corrupted_ticks_20251218_200000.jsonl
│       └── processed/
└── warehouse/
```

### Environment Variables

```bash
# DLQ Configuration
DLQ_MAX_FILE_SIZE_MB=100
DLQ_RETENTION_DAYS=30
DLQ_RETRY_ENABLED=true
```

## Troubleshooting

### Issue: DLQ files not created

**Symptoms**: No DLQ files in the expected directory

**Solutions**:
1. Check directory permissions: `ls -la data/collectors/mt5/raw/dlq/`
2. Verify DLQ initialization: Check logs for "Dead-Letter-Queue initialized"
3. Test DLQ manually: `dlq.record_failure({'test': 'data'}, Exception("test"))`

### Issue: High DLQ entry count

**Symptoms**: `stats['total_entries']` is very high

**Solutions**:
1. Analyze error types: `stats['error_types']`
2. Check for systemic issues: Review recent changes
3. Implement rate limiting: Add backoff for repeated failures
4. Review data sources: Check MT5 connection quality

### Issue: Retry not working

**Symptoms**: `retry_failed_data()` returns 0 successful retries

**Solutions**:
1. Verify retryable flag: Check `retryable=True` in failures
2. Check error types: Only network errors are retryable by default
3. Review retry logic: Add logging to `_process_tick_data()`
4. Test manually: Call `_process_tick_data(symbol)` directly

## API Reference

### DeadLetterQueue Class

#### `__init__(dlq_directory: str | Path, max_file_size_mb: int = 100)`

Initialize the DeadLetterQueue.

**Parameters**:
- `dlq_directory`: Directory to store DLQ files
- `max_file_size_mb`: Maximum size of DLQ file before rotation (default: 100MB)

#### `record_failure(data: Any, error: Exception, context: Optional[Dict[str, Any]] = None, retryable: bool = True) -> None`

Record a failed data processing attempt.

**Parameters**:
- `data`: The data that failed to process
- `error`: The exception that caused the failure
- `context`: Additional context information
- `retryable`: Whether this failure can be retried later

#### `get_failures(retryable_only: bool = True, limit: Optional[int] = None) -> List[Dict[str, Any]]`

Get failed entries from DLQ.

**Parameters**:
- `retryable_only`: Only return retryable failures (default: True)
- `limit`: Maximum number of entries to return

**Returns**: List of DLQ entries

#### `get_statistics() -> Dict[str, Any]`

Get DLQ statistics.

**Returns**: Dictionary containing:
- `total_entries`: Total number of entries
- `retryable_entries`: Number of retryable entries
- `non_retryable_entries`: Number of non-retryable entries
- `error_types`: Dictionary of error types and their counts
- `oldest_entry`: Timestamp of oldest entry
- `newest_entry`: Timestamp of newest entry

#### `mark_as_processed(timestamp: str) -> bool`

Mark a DLQ entry as processed.

**Parameters**:
- `timestamp`: ISO timestamp of the entry to mark

**Returns**: True if successful, False otherwise

### MT5Collector DLQ Methods

#### `retry_failed_data(max_retries: int = 3) -> Dict[str, Any]`

Retry processing failed data from DLQ.

**Parameters**:
- `max_retries`: Maximum number of retry attempts

**Returns**: Statistics about retry attempts

#### `get_dlq_statistics() -> Dict[str, Any]`

Get DLQ statistics.

**Returns**: Dictionary containing DLQ statistics

## Examples

### Complete Workflow Example

```python
from neural_ai.collectors.mt5 import MT5Collector, DeadLetterQueue
from neural_ai.collectors.mt5.exceptions import MT5DataValidationError
from pathlib import Path

# Initialize collector
config = {"config_path": "configs/collector_config.yaml"}
collector = MT5Collector(config)

# Monitor DLQ status
status = collector.get_connection_status()
print(f"DLQ Status: {status['dlq']}")

# Simulate a failure
try:
    # Process data that fails
    collector._process_tick_data("EURUSD")
except Exception as e:
    print(f"Error: {e}")

# Check DLQ for failures
stats = collector.get_dlq_statistics()
print(f"Failures recorded: {stats['total_entries']}")

# Retry failed data
if stats['retryable_entries'] > 0:
    retry_stats = collector.retry_failed_data(max_retries=3)
    print(f"Retry results: {retry_stats}")

# Get detailed failure information
failures = collector._dlq.get_failures(retryable_only=True)
for failure in failures:
    print(f"Failure: {failure['error_type']} - {failure['error_message']}")
    print(f"Context: {failure['context']}")
    print(f"Timestamp: {failure['timestamp']}")
```

## Performance Considerations

### Memory Usage

- DLQ entries are written to disk immediately (no in-memory buffering)
- `get_failures()` loads entries into memory (use `limit` parameter for large datasets)
- Typical entry size: ~1-2KB

### Disk Usage

- Default max file size: 100MB per file
- File rotation prevents unlimited growth
- Old files should be archived or deleted periodically

### I/O Performance

- Atomic writes with `fsync()` ensure data integrity
- JSONL format allows efficient streaming reads
- File rotation is a fast operation (just creating new file)

## Security Considerations

### File Permissions

```bash
# Recommended permissions
chmod 750 data/collectors/mt5/raw/dlq/
chmod 640 data/collectors/mt5/raw/dlq/*.jsonl
```

### Data Sensitivity

- DLQ files may contain sensitive financial data
- Implement access controls for DLQ directory
- Consider encryption for sensitive environments
- Regular cleanup of old files

### Audit Trail

- All failures are logged with timestamps
- Stack traces are preserved for debugging
- Context information helps trace failure sources
- Statistics provide overview of system health

## Version History

- **v1.0.0** (2025-12-18): Initial DLQ implementation
  - Basic DLQ functionality
  - Atomic write guarantees
  - File rotation
  - Retry mechanism
  - Statistics collection

## Support

For issues or questions about DLQ:

1. Check the logs: `logs/collectors/mt5/mt5_collector.log`
2. Review DLQ statistics: `collector.get_dlq_statistics()`
3. Check file permissions: `ls -la data/collectors/mt5/raw/dlq/`
4. Review error types: `stats['error_types']`

## Related Documentation

- [MT5 Collector Overview](README.md)
- [Error Handling Guide](../error_handling.md)
- [Data Quality Framework](DATA_QUALITY_FRAMEWORK.md)
- [Historical Data Collection](HISTORICAL_DATA_COLLECTION.md)
