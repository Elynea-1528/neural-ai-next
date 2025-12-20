"""Unit tests for MT5 Collector component.

Tests cover:
- Collector initialization and configuration
- MT5 connection management
- Real-time data collection (tick and OHLCV)
- Historical data collection
- Data validation and quality checks
- Error handling and recovery
- Data storage operations
- Multi-instrument and multi-timeframe support
- Collector lifecycle management

Author: Neural AI Next Team
Date: 2025-12-17
"""

import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

from neural_ai.collectors.mt5.error_handler import (
    NetworkError,
    StorageError,
)
from neural_ai.collectors.mt5.implementations.mt5_collector import MT5Collector


class TestMT5Collector(unittest.TestCase):
    """Test cases for MT5Collector class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Mock logger
        self.logger = Mock()

        # Mock error handler
        self.error_handler = Mock()

        # Mock data validator
        self.data_validator = Mock()
        self.data_validator.validate_tick_data.return_value = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {},
        }
        self.data_validator.validate_ohlcv_data.return_value = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {},
        }

        # Mock storage
        self.storage = Mock()
        self.storage.save_tick_data.return_value = {
            "status": "success",
            "saved_records": 100,
        }
        self.storage.save_ohlcv_data.return_value = {
            "status": "success",
            "saved_records": 100,
        }

        # Mock data warehouse
        self.data_warehouse = Mock()

        # Mock historical data manager
        self.historical_manager = Mock()
        self.historical_manager.create_historical_request.return_value = {
            "status": "success",
            "job_id": "job123",
        }
        self.historical_manager.get_job_status.return_value = {
            "status": "completed",
            "progress": 100,
        }

        # Mock data quality framework
        self.quality_framework = Mock()
        self.quality_framework.validate_data.return_value = {
            "is_valid": True,
            "quality_score": 0.95,
        }

        # Mock training dataset generator
        self.dataset_generator = Mock()

        # Test configuration
        self.test_config = {
            "collector_type": "mt5",
            "mt5": {
                "server": "DemoServer",
                "login": 123456,
                "password": "password123",
                "timeout": 30,
                "max_retries": 3,
            },
            "instruments": ["EURUSD", "GBPUSD"],
            "timeframes": ["H1", "H4"],
            "data_types": ["tick", "ohlcv"],
            "storage": {"base_path": self.temp_dir, "formats": ["parquet", "csv"]},
        }

        # Test data
        dates = pd.date_range(start="2025-01-01", end="2025-01-10", freq="H")
        self.test_tick_data = pd.DataFrame(
            {
                "timestamp": [int(d.timestamp()) for d in dates],
                "bid": np.random.normal(1.10, 0.001, len(dates)),
                "ask": np.random.normal(1.11, 0.001, len(dates)),
                "volume": np.random.randint(100, 1000, len(dates)),
            }
        )

        self.test_ohlcv_data = pd.DataFrame(
            {
                "timestamp": [int(d.timestamp()) for d in dates],
                "open": np.random.normal(1.10, 0.001, len(dates)),
                "high": np.random.normal(1.11, 0.001, len(dates)),
                "low": np.random.normal(1.09, 0.001, len(dates)),
                "close": np.random.normal(1.105, 0.001, len(dates)),
                "volume": np.random.randint(100, 1000, len(dates)),
            }
        )

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_initialization(self, mock_mt5):
        """Test MT5Collector initialization."""
        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
            data_warehouse=self.data_warehouse,
            historical_manager=self.historical_manager,
            quality_framework=self.quality_framework,
            dataset_generator=self.dataset_generator,
        )

        self.assertEqual(collector.config, self.test_config)
        self.assertEqual(collector.logger, self.logger)
        self.assertEqual(collector.error_handler, self.error_handler)
        self.assertEqual(collector.data_validator, self.data_validator)
        self.assertEqual(collector.storage, self.storage)
        self.assertEqual(collector.data_warehouse, self.data_warehouse)
        self.assertEqual(collector.historical_manager, self.historical_manager)
        self.assertEqual(collector.quality_framework, self.quality_framework)
        self.assertEqual(collector.dataset_generator, self.dataset_generator)

        # Check configuration extraction
        self.assertEqual(collector.server, "DemoServer")
        self.assertEqual(collector.login, 123456)
        self.assertEqual(collector.password, "password123")
        self.assertEqual(collector.timeout, 30)
        self.assertEqual(collector.max_retries, 3)
        self.assertEqual(collector.instruments, ["EURUSD", "GBPUSD"])
        self.assertEqual(collector.timeframes, ["H1", "H4"])
        self.assertEqual(collector.data_types, ["tick", "ohlcv"])

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_initialization_default_values(self, mock_mt5):
        """Test MT5Collector initialization with default values."""
        config = {
            "collector_type": "mt5",
            "mt5": {"server": "DemoServer", "login": 123456},
        }

        collector = MT5Collector(
            config=config, logger=self.logger, error_handler=self.error_handler
        )

        # Check default values
        self.assertEqual(collector.timeout, 60)
        self.assertEqual(collector.max_retries, 5)
        self.assertEqual(collector.instruments, ["EURUSD"])
        self.assertEqual(collector.timeframes, ["H1"])
        self.assertEqual(collector.data_types, ["tick"])

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_connect_success(self, mock_mt5):
        """Test successful connection to MT5."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )

        result = collector.connect()

        self.assertTrue(result)
        self.assertTrue(collector.is_connected)
        mock_mt5.initialize.assert_called_once_with(
            server="DemoServer", login=123456, password="password123", timeout=30
        )
        mock_mt5.login.assert_called_once_with(123456)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_connect_initialize_failure(self, mock_mt5):
        """Test connection failure during initialization."""
        mock_mt5.initialize.return_value = False

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )

        with self.assertRaises(NetworkError):
            collector.connect()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_connect_login_failure(self, mock_mt5):
        """Test connection failure during login."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = False

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )

        with self.assertRaises(NetworkError):
            collector.connect()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_disconnect(self, mock_mt5):
        """Test disconnecting from MT5."""
        mock_mt5.shutdown.return_value = True

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )
        collector.is_connected = True

        result = collector.disconnect()

        self.assertTrue(result)
        self.assertFalse(collector.is_connected)
        mock_mt5.shutdown.assert_called_once()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_disconnect_not_connected(self, mock_mt5):
        """Test disconnecting when not connected."""
        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )
        collector.is_connected = False

        result = collector.disconnect()

        self.assertTrue(result)
        mock_mt5.shutdown.assert_not_called()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_tick_data_success(self, mock_mt5):
        """Test successful tick data collection."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_ticks_from.return_value = [
            {"time": 1704067200, "bid": 1.1000, "ask": 1.1002, "volume": 1000},
            {"time": 1704067260, "bid": 1.1001, "ask": 1.1003, "volume": 1200},
        ]

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_tick_data(
            instrument="EURUSD",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("collected_records", result)
        self.assertIn("validation_result", result)
        self.assertIn("storage_result", result)
        mock_mt5.copy_ticks_from.assert_called_once()
        self.data_validator.validate_tick_data.assert_called_once()
        self.storage.save_tick_data.assert_called_once()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_tick_data_validation_failure(self, mock_mt5):
        """Test tick data collection with validation failure."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_ticks_from.return_value = [
            {"time": 1704067200, "bid": 1.1000, "ask": 1.1002, "volume": 1000}
        ]

        self.data_validator.validate_tick_data.return_value = {
            "is_valid": False,
            "errors": ["Invalid bid price"],
            "warnings": [],
            "statistics": {},
        }

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_tick_data(
            instrument="EURUSD",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        # Assert
        self.assertEqual(result["status"], "validation_failed")
        self.assertIn("validation_errors", result)
        self.storage.save_tick_data.assert_not_called()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_tick_data_storage_failure(self, mock_mt5):
        """Test tick data collection with storage failure."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_ticks_from.return_value = [
            {"time": 1704067200, "bid": 1.1000, "ask": 1.1002, "volume": 1000}
        ]

        self.storage.save_tick_data.side_effect = StorageError("Storage error")

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_tick_data(
            instrument="EURUSD",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        # Assert
        self.assertEqual(result["status"], "storage_failed")
        self.assertIn("error", result)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_ohlcv_data_success(self, mock_mt5):
        """Test successful OHLCV data collection."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_rates_from.return_value = [
            {
                "time": 1704067200,
                "open": 1.1000,
                "high": 1.1010,
                "low": 1.0990,
                "close": 1.1005,
                "volume": 1000,
            },
            {
                "time": 1704070800,
                "open": 1.1005,
                "high": 1.1015,
                "low": 1.0995,
                "close": 1.1010,
                "volume": 1200,
            },
        ]

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_ohlcv_data(
            instrument="EURUSD",
            timeframe="H1",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("collected_records", result)
        self.assertIn("validation_result", result)
        self.assertIn("storage_result", result)
        mock_mt5.copy_rates_from.assert_called_once()
        self.data_validator.validate_ohlcv_data.assert_called_once()
        self.storage.save_ohlcv_data.assert_called_once()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_realtime_data(self, mock_mt5):
        """Test real-time data collection."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.symbol_info_tick.return_value = {
            "time": 1704067200,
            "bid": 1.1000,
            "ask": 1.1002,
            "volume": 1000,
        }

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_realtime_data(instrument="EURUSD", data_type="tick")

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("collected_records", result)
        mock_mt5.symbol_info_tick.assert_called_once_with("EURUSD")

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_historical_data(self, mock_mt5):
        """Test historical data collection."""
        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            historical_manager=self.historical_manager,
        )

        # Execute
        result = collector.collect_historical_data(
            instrument="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("job_id", result)
        self.historical_manager.create_historical_request.assert_called_once_with(
            instrument="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_collect_batch_data(self, mock_mt5):
        """Test batch data collection for multiple instruments."""
        # Setup
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_ticks_from.return_value = [
            {"time": 1704067200, "bid": 1.1000, "ask": 1.1002, "volume": 1000}
        ]

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        # Execute
        result = collector.collect_batch_data(
            instruments=["EURUSD", "GBPUSD"],
            timeframes=["H1"],
            data_types=["tick"],
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertIn("total_collected", result)
        self.assertIn("instruments", result)
        self.assertIn("errors", result)
        self.assertGreater(result["total_collected"], 0)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_get_collector_status(self, mock_mt5):
        """Test getting collector status."""
        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )
        collector.is_connected = True
        collector.last_collection_time = datetime.now()
        collector.total_records_collected = 1000

        status = collector.get_collector_status()

        self.assertEqual(status["collector_type"], "mt5")
        self.assertTrue(status["is_connected"])
        self.assertIn("last_collection_time", status)
        self.assertEqual(status["total_records_collected"], 1000)
        self.assertIn("configuration", status)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_validate_instrument(self, mock_mt5):
        """Test instrument validation."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.symbol_select.return_value = True
        mock_mt5.symbol_info.return_value = {"name": "EURUSD"}

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )
        collector.connect()

        result = collector.validate_instrument("EURUSD")

        self.assertTrue(result["is_valid"])
        self.assertIn("instrument_info", result)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_validate_instrument_invalid(self, mock_mt5):
        """Test instrument validation for invalid instrument."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.symbol_select.return_value = False

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        )
        collector.connect()

        result = collector.validate_instrument("INVALID")

        self.assertFalse(result["is_valid"])
        self.assertIn("error", result)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_get_data_quality_report(self, mock_mt5):
        """Test getting data quality report."""
        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            quality_framework=self.quality_framework,
        )

        self.quality_framework.get_quality_report.return_value = {
            "overall_score": 0.95,
            "metrics": {},
            "recommendations": [],
        }

        report = collector.get_data_quality_report()

        self.assertEqual(report["overall_score"], 0.95)
        self.assertIn("metrics", report)
        self.quality_framework.get_quality_report.assert_called_once()

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_retry_mechanism(self, mock_mt5):
        """Test retry mechanism for failed operations."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True

        # First two calls fail, third succeeds
        mock_mt5.copy_ticks_from.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            [{"time": 1704067200, "bid": 1.1000, "ask": 1.1002, "volume": 1000}],
        ]

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        result = collector.collect_tick_data(
            instrument="EURUSD",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(mock_mt5.copy_ticks_from.call_count, 3)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_retry_mechanism_exhausted(self, mock_mt5):
        """Test retry mechanism exhaustion."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.copy_ticks_from.side_effect = Exception("Network error")

        collector = MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
            data_validator=self.data_validator,
            storage=self.storage,
        )
        collector.connect()

        result = collector.collect_tick_data(
            instrument="EURUSD",
            start_time=datetime(2025, 1, 1),
            end_time=datetime(2025, 1, 2),
        )

        self.assertEqual(result["status"], "failed")
        self.assertEqual(mock_mt5.copy_ticks_from.call_count, 3)

    @patch("neural_ai.collectors.mt5.implementations.mt5_collector.mt5")
    def test_context_manager(self, mock_mt5):
        """Test using collector as context manager."""
        mock_mt5.initialize.return_value = True
        mock_mt5.login.return_value = True
        mock_mt5.shutdown.return_value = True

        with MT5Collector(
            config=self.test_config,
            logger=self.logger,
            error_handler=self.error_handler,
        ) as collector:
            self.assertTrue(collector.is_connected)

        # Should be disconnected after exiting context
        self.assertFalse(collector.is_connected)
        mock_mt5.shutdown.assert_called_once()


if __name__ == "__main__":
    unittest.main()
