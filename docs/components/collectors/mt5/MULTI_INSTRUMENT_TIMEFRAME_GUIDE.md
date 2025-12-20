# Multi-Instrument and Multi-Timeframe MT5 Collector Guide

## Overview

This guide describes the enhanced MT5 Collector system that supports multiple instruments and timeframes for comprehensive financial data collection.

## Architecture

### Components

1. **Neural_AI_Next_Multi.mq5** - Enhanced Expert Advisor supporting multiple instruments and timeframes
2. **MT5Collector** - Python FastAPI server with validation and storage
3. **DataValidator** - Comprehensive data validation system
4. **ErrorHandler** - Robust error handling and recovery
5. **CollectorStorage** - Multi-format storage (JSONL for ticks, CSV for OHLCV)

## Supported Instruments

The system currently supports the following instruments:
- **EURUSD** - Euro/US Dollar
- **GBPUSD** - British Pound/US Dollar
- **USDJPY** - US Dollar/Japanese Yen
- **XAUUSD** - Gold/US Dollar

### Adding New Instruments

To add a new instrument, modify the `Instruments` input parameter in the Expert Advisor:

```mql5
input string Instruments = "EURUSD,GBPUSD,USDJPY,XAUUSD,NEWINSTRUMENT";
```

## Supported Timeframes

The system supports the following timeframes:
- **M1** - 1 Minute
- **M5** - 5 Minutes
- **M15** - 15 Minutes
- **H1** - 1 Hour
- **H4** - 4 Hours
- **D1** - Daily

### Timeframe Mappings

| Timeframe | MQL5 Constant | Integer Value |
| --------- | ------------- | ------------- |
| M1        | PERIOD_M1     | 1             |
| M5        | PERIOD_M5     | 5             |
| M15       | PERIOD_M15    | 15            |
| H1        | PERIOD_H1     | 60            |
| H4        | PERIOD_H4     | 240           |
| D1        | PERIOD_D1     | 1440          |

## Data Collection Strategy

### Three-Tier Approach

1. **Historical Data** (25 years)
   - Collected once during initial setup
   - Stored in CSV format for efficient access
   - Used for model training

2. **Update Data** (3-12 months)
   - Collected periodically to keep data current
   - Incremental updates to existing datasets
   - Validated against existing data

3. **Real-Time Data**
   - Continuous collection via Expert Advisor
   - Tick data (JSONL format)
   - OHLCV data (CSV format)
   - Immediate validation and storage

### Collection Frequency

- **Tick Data**: Every tick (real-time)
- **OHLCV Data**: Every 60 seconds (configurable)
- **Multi-Instrument**: Sequential collection with automatic error handling
- **Multi-Timeframe**: Parallel collection for each timeframe

## Data Storage Structure

### Directory Organization

```
data/
├── raw/
│   ├── EURUSD/
│   │   ├── M1/
│   │   │   ├── ticks.jsonl
│   │   │   └── ohlcv.csv
│   │   ├── M5/
│   │   ├── M15/
│   │   ├── H1/
│   │   ├── H4/
│   │   └── D1/
│   ├── GBPUSD/
│   ├── USDJPY/
│   └── XAUUSD/
├── invalid/
│   ├── EURUSD/
│   │   ├── M1/
│   │   │   └── rejected_ticks.jsonl
│   │   └── ...
│   └── ...
└── processed/
    └── ...
```

### File Formats

#### Tick Data (JSONL)
```json
{"symbol":"EURUSD","bid":1.17509,"ask":1.17524,"time":1765845540,"volume":1000000}
{"symbol":"EURUSD","bid":1.17508,"ask":1.17524,"time":1765845551,"volume":1000000}
```

#### OHLCV Data (CSV)
```csv
time,open,high,low,close,volume
1765845540,1.17509,1.17524,1.17508,1.17522,1000000
1765845600,1.17522,1.17530,1.17520,1.17528,1200000
```

## Expert Advisor Configuration

### Input Parameters

```mql5
input string FastAPI_Server = "http://localhost:8000"; // FastAPI server address
input int Update_Interval = 60;                        // Update interval in seconds
input bool Enable_HTTP_Logs = true;                    // Enable HTTP request logging

// Multi-instrument and multi-timeframe configuration
input string Instruments = "EURUSD,GBPUSD,USDJPY,XAUUSD"; // Comma-separated symbols
input string Timeframes = "M1,M5,M15,H1,H4,D1";          // Comma-separated timeframes
```

### Key Features

1. **Dynamic Instrument Parsing**
   - Automatically parses comma-separated instrument list
   - Validates each instrument before data collection
   - Continues collection even if one instrument fails

2. **Timeframe Conversion**
   - Converts string timeframes to MQL5 constants
   - Supports all standard MT5 timeframes
   - Handles invalid timeframe strings gracefully

3. **Sequential Data Collection**
   - Collects tick data for all instruments on every tick
   - Collects OHLCV data for all instrument/timeframe combinations periodically
   - Includes error handling for failed requests

4. **Configurable Logging**
   - Detailed HTTP request/response logging
   - Symbol-specific error messages
   - Connection status monitoring

## API Endpoints

### Tick Data Collection

**Endpoint**: `POST /api/v1/collect/tick`

**Request Body**:
```json
{
  "symbol": "EURUSD",
  "bid": 1.17509,
  "ask": 1.17524,
  "time": 1765845540,
  "volume": 1000000
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Tick data stored successfully",
  "validation_result": {
    "is_valid": true,
    "quality_score": 1.0,
    "warnings": []
  }
}
```

### OHLCV Data Collection

**Endpoint**: `POST /api/v1/collect/ohlcv`

**Request Body**:
```json
{
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
}
```

**Response**:
```json
{
  "status": "success",
  "message": "OHLCV data stored successfully",
  "validation_result": {
    "is_valid": true,
    "quality_score": 1.0,
    "warnings": []
  }
}
```

### Error Reporting

**Endpoint**: `GET /api/v1/errors/report`

**Response**:
```json
{
  "timestamp": "2025-12-15T23:39:28.063875",
  "total_errors": 0,
  "by_category": {},
  "by_severity": {},
  "recent_errors_count": 0
}
```

## Data Validation

### Tick Data Validation Rules

1. **Symbol Validation**
   - Must be a supported instrument
   - Must match the EA configuration

2. **Price Validation**
   - Bid must be > 0
   - Ask must be > 0
   - Ask must be >= Bid
   - Spread must be within reasonable limits

3. **Time Validation**
   - Timestamp must not be in the future
   - Timestamp must be within 24 hours of current time

4. **Volume Validation**
   - Volume must be >= 0
   - Volume must be within reasonable limits

### OHLCV Data Validation Rules

1. **Bar Structure Validation**
   - Open, High, Low, Close must all be > 0
   - High must be >= Open, High, Low, Close
   - Low must be <= Open, High, Low, Close

2. **Time Series Validation**
   - Bars must be in chronological order
   - No gaps larger than 2x timeframe interval
   - No duplicate timestamps

3. **Volume Validation**
   - Volume must be >= 0
   - Volume spikes must be investigated

## Error Handling

### Error Categories

1. **ValidationError** - Data validation failures
2. **StorageError** - File system or database errors
3. **NetworkError** - HTTP communication failures
4. **ConfigurationError** - Configuration issues
5. **DataQualityError** - Data quality concerns
6. **SystemError** - System-level errors

### Recovery Strategies

- **ValidationError**: Log and store in invalid data directory
- **StorageError**: Retry with exponential backoff
- **NetworkError**: Queue data and retry when connection restored
- **ConfigurationError**: Use default values and alert administrator
- **DataQualityError**: Flag data and continue collection
- **SystemError**: Log critical error and attempt graceful degradation

## Compilation and Installation

### Compiling the Expert Advisor

```bash
# Make the compilation script executable
chmod +x scripts/compile_multi_expert.sh

# Compile the Expert Advisor
./scripts/compile_multi_expert.sh
```

### Installing in MetaTrader 5

1. Copy the generated `Neural_AI_Next_Multi.ex5` file to your MT5 Experts directory
2. Restart MT5 or refresh the Navigator window
3. Attach the EA to a chart
4. Configure the input parameters
5. Enable automated trading

### Configuration Example

```
FastAPI Server: http://localhost:8000
Update Interval: 60
Enable HTTP Logs: true
Instruments: EURUSD,GBPUSD,USDJPY,XAUUSD
Timeframes: M1,M5,M15,H1,H4,D1
```

## Monitoring and Maintenance

### Log Files

- **Console Logs**: Real-time colored output (INFO level)
- **File Logs**: Detailed rotating logs (DEBUG level)
- **Error Logs**: Comprehensive error tracking

### Data Quality Monitoring

- Monitor validation statistics
- Review invalid data regularly
- Check error reports for patterns
- Validate data completeness

### Performance Optimization

- Adjust update interval based on data volume
- Monitor storage space usage
- Optimize validation rules
- Review network latency

## Troubleshooting

### Common Issues

1. **Connection Failures**
   - Verify FastAPI server is running
   - Check firewall settings
   - Validate server URL

2. **Compilation Errors**
   - Ensure MQL5 syntax is correct
   - Check MetaEditor installation
   - Verify Wine configuration

3. **Data Collection Issues**
   - Check instrument availability in MT5
   - Verify timeframe support
   - Review error logs

4. **Storage Issues**
   - Check disk space
   - Verify file permissions
   - Review storage configuration

### Getting Help

- Review the error logs in `/logs/collector_error.log`
- Check the error report at `GET /api/v1/errors/report`
- Consult the main project documentation
- Review the DataValidator and ErrorHandler documentation

## Future Enhancements

1. **Additional Data Sources**
   - Support for other brokers
   - Integration with additional data providers
   - Historical data import tools

2. **Advanced Features**
   - Real-time data quality scoring
   - Automated data cleaning
   - Machine learning-based anomaly detection

3. **Performance Improvements**
   - Parallel data collection
   - Caching mechanisms
   - Database optimization

4. **Monitoring Enhancements**
   - Web-based dashboard
   - Real-time alerts
   - Performance metrics

## Conclusion

The Multi-Instrument and Multi-Timeframe MT5 Collector provides a robust, scalable solution for comprehensive financial data collection. With support for multiple instruments, timeframes, and comprehensive validation, it forms the foundation for the Neural AI Next trading system.

For more information, refer to:
- [Logger Implementation Guide](LOGGER_IMPLEMENTATION.md)
- [Data Validator Documentation](../data_validator.py)
- [Error Handler Documentation](../error_handler.py)
- [Collector Storage Documentation](../storage/collector_storage.py)
