# MT5 Collector Component

## Overview

The MT5 Collector is a production-ready data collection component with advanced reliability features:

- **Hard-Timeout Mechanism:** Signal-based timeout for all MT5 API calls
- **Socket Integrity Check:** Periodic validation of MT5 connection
- **Automatic Reconnection:** Exponential backoff reconnection strategy
- **Circuit Breaker:** Prevents cascading failures
- **Dead-Letter-Queue (DLQ):** Handles corrupted or failed data
- **Atomic Write Storage:** Guarantees data integrity
- **Exponential Backoff:** Intelligent retry mechanism
- **Heartbeat Monitoring:** Proactive connection maintenance

## Quick Start

```python
from neural_ai.collectors.mt5.implementations.mt5_collector import MT5Collector

# Initialize collector
collector = MT5Collector()

# Check connection status
status = collector.get_connection_status()
print(f"Socket valid: {status['socket_valid']}")
print(f"Circuit breaker: {status['circuit_breaker']['state']}")
print(f"DLQ entries: {status['dlq']['total_entries']}")

# Retry failed data
retry_stats = collector.retry_failed_data(max_retries=3)
print(f"Retried: {retry_stats['total_retried']}, Successful: {retry_stats['successful']}")
```

## Key Features

### Multi-Instrument Support
- EURUSD, GBPUSD, USDJPY, XAUUSD
- Easy extension to additional instruments

### Multi-Timeframe Support
- M1, M5, M15, H1, H4, D1
- Configurable timeframe mappings

### Real-Time Data Collection
- Tick data collection with validation
- OHLCV data collection with quality checks
- Automatic invalid data handling

### Historical Data Collection
- 25+ years of historical data
- Automatic gap detection and filling
- Batch processing for large datasets
- Progress tracking and status monitoring

### Data Quality Framework
- 3-level validation (basic, logical, statistical)
- Outlier detection (IQR, Z-Score, Moving Average)
- Automatic data correction
- Quality metrics and reporting

### Data Warehouse Integration
- Hierarchical data organization
- Automatic data movement and merging
- Backup and restore functionality
- Integrity validation

### Training Dataset Generation
- 4 dataset types (retraining, medium, deep_learning, validation)
- Quality filtering
- Multiple output formats (CSV, Parquet)
- Metadata management

## Architecture

### Component Structure

```
neural_ai/collectors/mt5/
├── exceptions.py                          # Exception classes
├── data_validator.py                      # Data validation with quality framework
├── dlq.py                                 # Dead-Letter-Queue implementation
├── error_handler.py                       # Error handling and recovery
├── interfaces/
│   ├── collector_interface.py            # Main interface
│   ├── data_validator_interface.py       # Validator interface
│   └── storage_interface.py              # Storage interface
├── implementations/
│   ├── mt5_collector.py                  # Main collector with reliability features
│   ├── data_quality_framework.py         # Comprehensive quality framework
│   ├── historical_data_manager.py        # Historical data management
│   ├── training_dataset_generator.py     # Training dataset generation
│   ├── collector_factory.py              # Factory pattern
│   └── storage/
│       ├── collector_storage.py          # Storage implementation
│       └── data_warehouse_manager.py     # Data warehouse management
└── validators/
    ├── tick_validator.py                 # Tick validator
    └── ohlcv_validator.py                # OHLCV validator
```

### Data Flow

1. **Expert Advisor** (in MT5) collects data
2. **FastAPI Server** receives data via HTTP POST requests
3. **DataValidator** validates incoming data with quality framework
4. **CollectorStorage** stores data in Data Warehouse
5. **ErrorHandler** manages errors with recovery strategies
6. **DLQ** handles corrupted data for later retry
7. **Circuit Breaker** prevents cascading failures

## Reliability Features

### Hard-Timeout Mechanism

Every MT5 API call has a configurable timeout:
- `initialize()`: 30 seconds
- `_fetch_historical_data()`: 60 seconds
- `_process_tick_data()`: 10 seconds

```python
@timeout(30)
def initialize(self) -> bool:
    # Method will timeout after 30 seconds
    pass
```

### Socket Integrity Check

The collector periodically checks if the MT5 socket connection is valid:

```python
if collector._check_socket_integrity():
    # Connection is valid
    pass
else:
    # Attempt reconnection
    collector._reconnect()
```

**Check Frequency:**
- Every 60 seconds (heartbeat)
- Before every MT5 API call
- On connection errors

### Circuit Breaker

The circuit breaker prevents cascading failures:

- **CLOSED:** Normal operation
- **OPEN:** Failures detected, rejecting requests
- **HALF_OPEN:** Testing if service recovered

```python
cb_status = collector.get_circuit_breaker_status()
print(f"State: {cb_status['state']}")
print(f"Failure count: {cb_status['failure_count']}")
```

**Configuration:**
- `failure_threshold`: 5 consecutive failures
- `recovery_timeout`: 60 seconds in OPEN state

### Dead-Letter-Queue (DLQ)

The DLQ handles corrupted or failed data:

```python
dlq_stats = collector.get_dlq_statistics()
print(f"Total failures: {dlq_stats['total_entries']}")
print(f"Retryable: {dlq_stats['retryable_entries']}")
print(f"Error types: {dlq_stats['error_types']}")

# Retry failed data
retry_stats = collector.retry_failed_data(max_retries=3)
print(f"Retried: {retry_stats['total_retried']}, Successful: {retry_stats['successful']}")
```

**Features:**
- Atomic write guarantees
- File rotation (100MB limit)
- Retryable/non-retryable classification
- Comprehensive statistics

### Exponential Backoff

The retry mechanism uses exponential backoff with jitter:

```python
@retry_with_backoff(max_retries=3, base_delay=2.0)
def fetch_data(self):
    # Will retry up to 3 times with exponential backoff
    pass
```

**Configuration:**
- `base_delay`: 1.0 second
- `max_delay`: 60.0 seconds
- `max_retries`: 5 attempts
- `jitter`: True (prevents thundering herd)

### Heartbeat Monitoring

Periodic health checks maintain connection integrity:

```python
def _heartbeat_check(self) -> None:
    if time.time() - self._last_heartbeat > 60:
        if not self._check_socket_integrity():
            self._reconnect()
        self._last_heartbeat = time.time()
```

**Check Frequency:** Every 60 seconds

## Installation

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Neural AI Core components

### Installation Steps

1. **Install dependencies:**
```bash
pip install fastapi uvicorn
```

2. **Configure settings:**
```yaml
# configs/collector_config.yaml
logger:
  type: "colored"
  level: "INFO"

storage:
  base_path: "data/collectors/mt5"
  format: "csv"
```

3. **Start server:**
```bash
python scripts/run_collector.py
```

4. **Start GUI (optional):**
```bash
python main.py
```

## Usage

### Basic Usage

```python
from neural_ai.collectors.mt5 import CollectorFactory
from neural_ai.core.config import ConfigManagerFactory

# Load configuration
config = ConfigManagerFactory.get_manager("configs/collector_config.yaml")

# Create collector
collector = CollectorFactory.get_collector("mt5", config)

# Start server
await collector.start_server(host="0.0.0.0", port=8000)
```

### API Endpoints

#### Send Tick Data

```bash
curl -X POST "http://localhost:8000/api/v1/collect/tick" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "bid": 1.17509,
    "ask": 1.17524,
    "time": 1765845540,
    "volume": 1000000
  }'
```

#### Send OHLCV Data

```bash
curl -X POST "http://localhost:8000/api/v1/collect/ohlcv" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "timeframe": 16385,
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
  }'
```

#### Start Historical Collection

```bash
curl -X POST "http://localhost:8000/api/v1/historical/start?auto_start=true"
```

#### Get Connection Status

```bash
curl "http://localhost:8000/api/v1/health"
```

## Configuration

### Logger Configuration

```yaml
logger:
  type: "colored"              # Logger type
  level: "INFO"                # Log level
  file_logger:
    type: "rotating"           # File logger type
    log_file: "logs/mt5_collector.log"
    rotation_type: "time"      # Rotation type
    when: "midnight"           # Rotation time
    backup_count: 7            # Backup file count
```

### Storage Configuration

```yaml
storage:
  base_path: "data/collectors/mt5"
  raw_path: "raw"
  validated_path: "validated"
  invalid_path: "invalid"
  formats:
    tick: "jsonl"
    ohlcv: "csv"
```

### Reliability Configuration

```yaml
reliability:
  timeout:
    initialize: 30             # seconds
    fetch_historical: 60       # seconds
    process_tick: 10           # seconds
  circuit_breaker:
    failure_threshold: 5       # consecutive failures
    recovery_timeout: 60       # seconds
  retry:
    max_retries: 3
    base_delay: 1.0           # seconds
    max_delay: 60.0           # seconds
    jitter: true
  dlq:
    max_file_size_mb: 100
    rotation_enabled: true
```

## Data Structure

### Tick Data (JSONL)

```json
{"symbol":"EURUSD","bid":1.17509,"ask":1.17524,"time":1765845540,"volume":1000000}
```

### OHLCV Data (CSV)

```csv
time,open,high,low,close,volume
1765845540,1.17509,1.17524,1.17508,1.17522,1000000
```

## Error Handling

The component uses the following exception classes:

- `CollectorError` - Base exception
- `ConnectionError` - Connection errors
- `DataFetchError` - Data fetch errors
- `ValidationError` - Validation errors
- `StorageError` - Storage errors
- `ConfigurationError` - Configuration errors
- `MT5ConnectionError` - MT5 specific connection errors
- `MT5TimeoutError` - MT5 timeout errors
- `MT5SocketError` - MT5 socket errors

## Testing

### Unit Tests

```bash
pytest tests/collectors/mt5/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v
```

**Result:** 5/5 tests passed

### DLQ Tests

```bash
pytest tests/collectors/mt5/test_dlq.py -v
```

### Mock MT5 Testing

Use the Mock MT5 for testing without actual MT5 installation:

```python
from tests.integration.mock_mt5 import MockMT5
from tests.integration.mt5_bridge import MT5Bridge

# Create mock MT5
mock_mt5 = MockMT5()
mock_mt5.initialize()

# Create bridge
bridge = MT5Bridge(mock_mt5, storage)

# Test data flow
stats = bridge.fetch_and_store_historical_data('EURUSD', 60, 0, 100)
assert stats['fetched'] == 100
assert stats['stored'] == 100
```

## GUI Usage

The project includes a complete GUI for MT5 Collector monitoring and control.

### Main GUI

Start the GUI:

```bash
python main.py
```

#### Available Functions

1. **Control Panel**
   - Start Collector: Start real-time data collection
   - Stop Collector: Stop data collection
   - Start Historical: Start 25-year historical data collection

2. **Status Panel**
   - Collector status: Display data collector status
   - Historical status: Display historical collection status

3. **Data Structure**
   - Hierarchical tree structure for data folder
   - Display file size and modification date
   - Auto-refresh every 5 seconds

4. **Log Viewer**
   - Real-time log display
   - Display last 100 lines
   - Auto-refresh every 2 seconds

5. **Data Information**
   - Check data status
   - Display tick and OHLCV file counts
   - Check Data Warehouse contents

6. **Menu Bar**
   - File → Open Data Folder: Open data folder
   - Tools → Start Historical Collection: Start historical collection
   - Tools → View Logs: View log files
   - Tools → Check Data Status: Check data status
   - Help → About: System information

### Log Viewer

Start independent log viewer:

```bash
python scripts/log_viewer.py
```

#### Functions

- Independent log file viewing
- Real-time log updates (every 1 second)
- Delete and refresh log files
- Open log file in external editor
- Display last update time

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

# Storage statistics
storage_stats = collector.get_storage_stats()
```

## Performance

- **Lazy Loading:** Components loaded only when needed
- **Thread-Safe:** RLock-based synchronization
- **Memory Efficient:** Minimal memory footprint
- **Fast Recovery:** Automatic reconnection and retry

## Troubleshooting

### Common Issues

1. **Connection Error:**
   - Check if FastAPI server is running
   - Check firewall settings
   - Verify network connectivity

2. **Data Validation Error:**
   - Check data format
   - Review log files for detailed error information
   - Check DLQ for failed data

3. **Storage Error:**
   - Check disk space
   - Verify write permissions
   - Check Data Warehouse integrity

4. **Circuit Breaker OPEN:**
   - Check MT5 connection
   - Review error logs
   - Wait for recovery timeout
   - Manually reset if needed

## Related Documentation

- [API Reference](api.md)
- [Reliability Features](RELIABILITY_FEATURES.md)
- [Design Specification](design_spec.md)
- [Data Quality Framework](DATA_QUALITY_FRAMEWORK.md)
- [Historical Data Collection](HISTORICAL_DATA_COLLECTION.md)
- [Data Warehouse Guide](DATA_WAREHOUSE_AND_TRAINING_DATASETS.md)
- [Development Checklist](development_checklist.md)
- [Changelog](CHANGELOG.md)

## License

MIT License - see LICENSE file for details.

---

**Document Version:** 1.2
**Last Updated:** 2025-12-18
**Developer:** Neural AI Next Team
