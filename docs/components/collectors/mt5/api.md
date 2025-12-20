# MT5 Collector API Reference

## MT5Collector Class

### Core Methods

#### `initialize() -> bool`
Initialize MT5 connection with timeout and socket integrity check.

**Returns:** True if successful, False otherwise

**Timeout:** 30 seconds

#### `get_connection_status() -> Dict[str, Any]`
Get detailed connection status including socket integrity, circuit breaker, and DLQ.

**Returns:** Dictionary with connection information

**Example:**
```python
status = collector.get_connection_status()
print(status['socket_valid'])  # True/False
print(status['circuit_breaker'])  # Circuit breaker state
print(status['dlq'])  # DLQ statistics
```

#### `get_circuit_breaker_status() -> Dict[str, Any]`
Get circuit breaker state and statistics.

**Returns:** Dictionary with circuit breaker information

#### `get_dlq_statistics() -> Dict[str, Any]`
Get Dead-Letter-Queue statistics.

**Returns:** Dictionary with DLQ information

#### `retry_failed_data(max_retries: int = 3) -> Dict[str, Any]`
Retry processing failed data from DLQ.

**Args:**
- `max_retries`: Maximum number of retry attempts

**Returns:** Dictionary with retry statistics

### Data Collection Methods

#### `_fetch_historical_data(symbol: str, timeframe: int, start: int, end: int) -> Optional[pd.DataFrame]`
Fetch historical data with timeout, socket integrity check, and DLQ support.

**Timeout:** 60 seconds
**Retry:** Automatic with exponential backoff
**DLQ:** Failed data recorded for later retry

#### `_process_tick_data(symbol: str) -> None`
Process tick data with timeout, validation, and DLQ support.

**Timeout:** 10 seconds
**Retry:** Automatic with exponential backoff
**DLQ:** Failed data recorded for later retry

### Error Handling Methods

#### `_safe_mt5_call(func, *args, expected_type=None, retry_on_failure: bool = True, **kwargs)`
Wrapper for MT5 API calls with timeout, error handling, and retry logic.

**Features:**
- Socket integrity check
- Automatic reconnection
- Circuit breaker protection
- Heartbeat monitoring
- Response validation

#### `_check_socket_integrity() -> bool`
Check if the MT5 socket connection is still valid.

**Returns:** True if valid, False otherwise

#### `_reconnect(max_retries: int = 3) -> bool`
Attempt to reconnect to MT5 with exponential backoff.

**Returns:** True if successful, False otherwise

### Timeout Decorator

```python
@timeout(30)
def initialize(self) -> bool:
    # Method will timeout after 30 seconds
    pass
```

### Retry Decorator

```python
@retry_with_backoff(max_retries=3, base_delay=2.0)
def _fetch_historical_data(self, symbol: str, timeframe: int, start: int, end: int):
    # Method will retry with exponential backoff
    pass
```

## FastAPI Endpoints

### Health Check

#### GET /api/v1/ping
Health check endpoint for Expert Advisor connection testing.

**Response:**
```json
{
  "status": "ok",
  "message": "MT5 Collector is running"
}
```

#### GET /api/v1/health
Comprehensive health check including connection status, circuit breaker, and DLQ.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-18T21:15:00Z",
  "version": "1.0.0",
  "connection_status": {
    "socket_valid": true,
    "circuit_breaker": {
      "state": "CLOSED",
      "failure_count": 0
    },
    "dlq": {
      "total_entries": 0,
      "retryable_entries": 0
    }
  }
}
```

### Real-Time Data Collection

#### POST /api/v1/collect/tick
Receive tick data from Expert Advisor with automatic validation and DLQ support.

**Request Body:**
```json
{
  "symbol": "EURUSD",
  "bid": 1.17509,
  "ask": 1.17524,
  "time": 1765845540,
  "volume": 1000000
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Tick data received and stored",
  "data": {
    "symbol": "EURUSD",
    "bid": 1.17509,
    "ask": 1.17524,
    "time": 1765845540,
    "volume": 1000000,
    "type": "tick",
    "received_at": "2025-12-18T21:15:00Z"
  }
}
```

**Response (Validation Error with DLQ):**
```json
{
  "status": "warning",
  "message": "Invalid tick data received and stored in DLQ",
  "errors": ["Bid price must be positive"],
  "dlq_reference": "dlq_12345"
}
```

#### POST /api/v1/collect/ohlcv
Receive OHLCV data from Expert Advisor with validation and DLQ support.

**Request Body:**
```json
{
  "symbol": "EURUSD",
  "timeframe": "16385",
  "timestamp": 1765845540,
  "bars": [
    {
      "time": 1765845540,
      "open": 1.17509,
      "high": 1.17524,
      "low": 1.17508,
      "close": 1.17522,
      "volume": 1000000
    }
  ]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "OHLCV data received and stored",
  "data": {
    "symbol": "EURUSD",
    "timeframe": "16385",
    "bars_count": 1
  }
}
```

### Historical Data Collection

#### POST /api/v1/historical/start
Start historical data collection with automatic gap detection.

**Query Parameters:**
- `auto_start` (bool, optional): Automatic start with gap detection. Default: `true`
- `symbol` (string, optional): Symbol (e.g., "EURUSD")
- `timeframe` (string, optional): Timeframe (e.g., "H1", "M15"). Default: "H1"
- `start_date` (string, optional): Start date (YYYY-MM-DD format)
- `end_date` (string, optional): End date (YYYY-MM-DD format)
- `batch_size` (int, optional): Batch size in days. Default: `365`
- `priority` (string, optional): Priority ("normal", "high", "low"). Default: "normal"

**Response (Automatic Mode):**
```json
{
  "status": "success",
  "message": "Historical data collection started",
  "mode": "auto_start",
  "jobs_created": 5,
  "missing_data": [
    {
      "symbol": "EURUSD",
      "timeframe": "H1",
      "start_date": "2020-01-01",
      "end_date": "2023-12-31"
    }
  ]
}
```

#### GET /api/v1/historical/poll
Poll for pending historical data requests (Expert Advisor compatibility).

**Response:**
```json
{
  "job_id": "job_12345",
  "symbol": "EURUSD",
  "timeframe": "H1",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "batch_size_days": 365
}
```

#### POST /api/v1/historical/collect
Receive historical data from Expert Advisor.

**Request Body:**
```json
{
  "job_id": "job_12345",
  "batch_number": 1,
  "symbol": "EURUSD",
  "timeframe": "H1",
  "date_range": {
    "start": "2023-01-01",
    "end": "2023-12-31"
  },
  "bars": [
    {
      "time": 1672531200,
      "open": 1.17509,
      "high": 1.17524,
      "low": 1.17508,
      "close": 1.17522,
      "volume": 1000000
    }
  ]
}
```

#### GET /api/v1/historical/status/{job_id}
Get historical job status.

**Response:**
```json
{
  "job_id": "job_12345",
  "status": "in_progress",
  "progress": 45,
  "total_batches": 10,
  "completed_batches": 4,
  "current_batch": 5
}
```

### Data Quality Endpoints

#### GET /api/v1/quality/metrics
Get data quality metrics.

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "total_validations": 1500,
    "valid_data": 1450,
    "invalid_data": 50,
    "quality_score": 0.967,
    "outliers_detected": 12,
    "corrections_applied": 8
  }
}
```

#### POST /api/v1/quality/report
Generate quality report.

**Request Body:**
```json
{
  "symbol": "EURUSD",
  "timeframe": "H1",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "format": "json",
  "include_corrections": true
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Quality report generated",
  "files": [
    "logs/quality_reports/quality_report_20251218_211500_EURUSD_H1.json"
  ],
  "output_path": "logs/quality_reports/quality_report_20251218_211500_EURUSD_H1.json"
}
```

### Data Warehouse Endpoints

#### GET /api/v1/warehouse/stats
Get Data Warehouse statistics.

**Response:**
```json
{
  "status": "success",
  "total_instruments": 4,
  "total_timeframes": 6,
  "total_files": 250,
  "total_size_gb": 2.5,
  "by_instrument": {
    "EURUSD": 100,
    "GBPUSD": 80,
    "USDJPY": 50,
    "XAUUSD": 20
  },
  "by_timeframe": {
    "M1": 50,
    "M5": 50,
    "M15": 40,
    "H1": 40,
    "H4": 40,
    "D1": 30
  }
}
```

#### POST /api/v1/warehouse/organize
Organize data to Data Warehouse.

**Request Body:**
```json
{
  "instrument": "EURUSD",
  "timeframe": "H1",
  "data_type": "validated"
}
```

#### POST /api/v1/warehouse/backup
Backup Warehouse data.

**Request Body:**
```json
{
  "backup_name": "backup_20251218",
  "instruments": "EURUSD,GBPUSD,USDJPY",
  "timeframes": "H1,H4,D1"
}
```

### Training Dataset Endpoints

#### POST /api/v1/training/generate
Generate training dataset.

**Request Body:**
```json
{
  "dataset_type": "retraining",
  "symbols": ["EURUSD", "GBPUSD"],
  "timeframes": ["H1", "H4"],
  "date_range": {
    "start": "2020-01-01",
    "end": "2023-12-31"
  },
  "quality_threshold": 0.95,
  "output_format": "parquet"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Training dataset generation started",
  "dataset_id": "dataset_12345",
  "estimated_completion": "2025-12-18T22:00:00Z"
}
```

#### GET /api/v1/training/status/{dataset_id}
Get training dataset status.

**Response:**
```json
{
  "dataset_id": "dataset_12345",
  "status": "completed",
  "progress": 100,
  "output_files": [
    "data/training/retraining/dataset_12345.parquet"
  ],
  "size_mb": 150.5
}
```

### Error Handling Endpoints

#### GET /api/v1/errors/report
Get error statistics report.

**Response:**
```json
{
  "timestamp": "2025-12-18T21:15:00Z",
  "total_errors": 3,
  "by_category": {
    "ValidationError": 2,
    "StorageError": 1
  },
  "by_severity": {
    "WARNING": 2,
    "ERROR": 1
  },
  "recent_errors_count": 1
}
```

#### GET /api/v1/validation/report
Get validation statistics.

**Response:**
```json
{
  "timestamp": "2025-12-18T21:15:00Z",
  "total_validations": 1500,
  "valid_data": 1450,
  "invalid_data": 50,
  "by_instrument": {
    "EURUSD": 1000,
    "GBPUSD": 300,
    "USDJPY": 200
  },
  "by_data_type": {
    "tick": 1200,
    "ohlcv": 300
  }
}
```

### Storage Statistics

#### GET /api/v1/storage/stats
Get storage statistics.

**Response:**
```json
{
  "timestamp": "2025-12-18T21:15:00Z",
  "base_path": "data/collectors/mt5",
  "total_files": 250,
  "by_instrument": {
    "EURUSD": 100,
    "GBPUSD": 80,
    "USDJPY": 50,
    "XAUUSD": 20
  },
  "by_timeframe": {
    "M1": 50,
    "M5": 50,
    "H1": 50,
    "D1": 50
  },
  "total_size_bytes": 10485760
}
```

## Reliability Features

### Circuit Breaker Status

The circuit breaker has three states:
- **CLOSED:** Normal operation, requests pass through
- **OPEN:** Failures detected, rejecting requests
- **HALF_OPEN:** Testing recovery, allowing limited requests

**Example:**
```python
cb_status = collector.get_circuit_breaker_status()
print(f"State: {cb_status['state']}")
print(f"Failure count: {cb_status['failure_count']}")
print(f"Last failure: {cb_status['last_failure_time']}")
```

### Dead-Letter-Queue (DLQ)

The DLQ handles corrupted or failed data with retry capability.

**Example:**
```python
dlq_stats = collector.get_dlq_statistics()
print(f"Total failures: {dlq_stats['total_entries']}")
print(f"Retryable: {dlq_stats['retryable_entries']}")
print(f"Error types: {dlq_stats['error_types']}")

# Retry failed data
retry_stats = collector.retry_failed_data(max_retries=3)
print(f"Retried: {retry_stats['total_retried']}")
print(f"Successful: {retry_stats['successful']}")
print(f"Failed: {retry_stats['failed']}")
```

### Connection Status

Comprehensive connection monitoring with socket integrity check.

**Example:**
```python
status = collector.get_connection_status()
print(f"Socket valid: {status['socket_valid']}")
print(f"Terminal connected: {status['terminal_info']['connected']}")
print(f"Last heartbeat: {status['last_heartbeat']}")
print(f"Circuit breaker: {status['circuit_breaker']['state']}")
print(f"DLQ entries: {status['dlq']['total_entries']}")
```

## Error Codes

### 200 OK
Request successfully processed.

### 400 Bad Request
Invalid request format or parameters.

### 500 Internal Server Error
Server-side error occurred.

### 503 Service Unavailable
Circuit breaker is OPEN, service temporarily unavailable.

## Rate Limiting

- **Maximum requests per minute:** 1000
- **Maximum requests per second:** 100

## Monitoring

Monitor the collector in real-time:

```python
# Get comprehensive status
status = collector.get_connection_status()

# Monitor circuit breaker
cb_status = collector.get_circuit_breaker_status()

# Check DLQ
dlq_stats = collector.get_dlq_statistics()

# Quality metrics
quality = collector.get_quality_metrics()
```

## Related Documentation

- [MT5 Collector README](README.md)
- [Reliability Features](RELIABILITY_FEATURES.md)
- [Design Specification](design_spec.md)
- [Data Quality Framework](DATA_QUALITY_FRAMEWORK.md)
- [Historical Data Collection](HISTORICAL_DATA_COLLECTION.md)
