"""Unit tests for Collector Storage component.

Tests cover:
- Tick data storage (JSONL format)
- OHLCV data storage (CSV and Parquet formats)
- Invalid data storage
- Data warehouse integration
- Storage statistics
- Multi-instrument and multi-timeframe support

Author: Neural AI Next Team
Date: 2025-12-17
"""

import json
import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from neural_ai.collectors.mt5.implementations.storage.collector_storage import (
    CollectorStorage,
)


class TestCollectorStorage(unittest.TestCase):
    """Test cases for CollectorStorage class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.logger = Mock()

        # Create storage instance
        self.storage = CollectorStorage(
            base_path=self.temp_dir,
            logger=self.logger,
            use_parquet=False,  # Use CSV for simpler testing
            enable_warehouse_integration=False,
        )

        # Test data
        self.tick_data = {
            "symbol": "EURUSD",
            "bid": 1.17500,
            "ask": 1.17505,
            "time": int(datetime.now().timestamp()),
        }

        self.ohlcv_data = {
            "symbol": "EURUSD",
            "timeframe": 16385,
            "bars": [
                {
                    "time": int(datetime.now().timestamp()),
                    "open": 1.17450,
                    "high": 1.17550,
                    "low": 1.17400,
                    "close": 1.17500,
                    "volume": 1000,
                }
            ],
        }

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test CollectorStorage initialization."""
        self.assertEqual(self.storage.base_path, Path(self.temp_dir))
        self.assertEqual(self.storage.logger, self.logger)
        self.assertFalse(self.storage.use_parquet)
        self.assertIsNotNone(self.storage.supported_instruments)
        self.assertIsNotNone(self.storage.supported_timeframes)

    def test_store_tick_valid(self):
        """Test storing valid tick data."""
        self.storage.store_tick(self.tick_data)

        # Check if file was created
        filepath = Path(self.temp_dir) / "collectors" / "mt5" / "raw" / "EURUSD_ticks.jsonl"
        self.assertTrue(filepath.exists())

        # Check file content
        with open(filepath) as f:
            line = f.readline()
            data = json.loads(line)

        self.assertEqual(data["symbol"], "EURUSD")
        self.assertEqual(data["bid"], 1.17500)
        self.assertEqual(data["ask"], 1.17505)

    def test_store_tick_unsupported_instrument(self):
        """Test storing tick data for unsupported instrument."""
        invalid_tick = self.tick_data.copy()
        invalid_tick["symbol"] = "UNSUPPORTED"

        self.storage.store_tick(invalid_tick)

        # Check if warning was logged
        self.logger.warning.assert_called_once()

    def test_store_ohlcv_csv(self):
        """Test storing OHLCV data in CSV format."""
        self.storage.store_ohlcv(self.ohlcv_data)

        # Check if file was created
        filepath = Path(self.temp_dir) / "collectors" / "mt5" / "EURUSD_H1_ohlcv.csv"
        self.assertTrue(filepath.exists())

    @patch(
        "neural_ai.collectors.mt5.implementations.storage.collector_storage.PARQUET_AVAILABLE",
        True,
    )
    def test_store_ohlcv_parquet(self):
        """Test storing OHLCV data in Parquet format."""
        # Create storage with Parquet enabled
        storage = CollectorStorage(
            base_path=self.temp_dir,
            logger=self.logger,
            use_parquet=True,
            enable_warehouse_integration=False,
        )

        storage.store_ohlcv(self.ohlcv_data)

        # Check if file was created
        filepath = Path(self.temp_dir) / "collectors" / "mt5" / "EURUSD_H1_ohlcv.parquet"
        self.assertTrue(filepath.exists())

    def test_store_ohlcv_unsupported_instrument(self):
        """Test storing OHLCV data for unsupported instrument."""
        invalid_ohlcv = self.ohlcv_data.copy()
        invalid_ohlcv["symbol"] = "UNSUPPORTED"

        self.storage.store_ohlcv(invalid_ohlcv)

        # Check if warning was logged
        self.logger.warning.assert_called_once()

    def test_store_ohlcv_unsupported_timeframe(self):
        """Test storing OHLCV data for unsupported timeframe."""
        invalid_ohlcv = self.ohlcv_data.copy()
        invalid_ohlcv["timeframe"] = 99999

        self.storage.store_ohlcv(invalid_ohlcv)

        # Check if warning was logged
        self.logger.warning.assert_called_once()

    def test_store_invalid_data(self):
        """Test storing invalid data."""
        self.storage.store_invalid_data(
            data=self.tick_data, data_type="tick", reason="Invalid price"
        )

        # Check if file was created
        filepath = (
            Path(self.temp_dir) / "collectors" / "mt5" / "invalid" / "EURUSD_tick_invalid.jsonl"
        )
        self.assertTrue(filepath.exists())

        # Check file content
        with open(filepath) as f:
            line = f.readline()
            data = json.loads(line)

        self.assertEqual(data["symbol"], "EURUSD")
        self.assertEqual(data["invalid_reason"], "Invalid price")

    def test_get_data_warehouse_path(self):
        """Test getting data warehouse path."""
        path = self.storage.get_data_warehouse_path(
            symbol="EURUSD", timeframe="H1", data_type="validated"
        )

        expected_path = Path(self.temp_dir) / "warehouse" / "validated" / "EURUSD" / "H1"
        self.assertEqual(path, expected_path)

        # Test without timeframe
        path = self.storage.get_data_warehouse_path(symbol="EURUSD", data_type="raw")

        expected_path = Path(self.temp_dir) / "warehouse" / "raw" / "EURUSD"
        self.assertEqual(path, expected_path)

    def test_store_to_warehouse_ohlcv(self):
        """Test storing OHLCV data to warehouse."""
        self.storage.store_to_warehouse(data=self.ohlcv_data, data_type="raw", validated=True)

        # Check if file was created in warehouse
        filepath = (
            Path(self.temp_dir)
            / "warehouse"
            / "validated"
            / "EURUSD"
            / "H1"
            / "EURUSD_H1_ohlcv.csv"
        )
        self.assertTrue(filepath.exists())

    def test_store_to_warehouse_tick(self):
        """Test storing tick data to warehouse."""
        self.storage.store_to_warehouse(data=self.tick_data, data_type="raw", validated=False)

        # Check if file was created in warehouse
        filepath = Path(self.temp_dir) / "warehouse" / "raw" / "EURUSD" / "EURUSD_ticks.jsonl"
        self.assertTrue(filepath.exists())

    def test_get_storage_stats(self):
        """Test getting storage statistics."""
        # Store some data first
        self.storage.store_tick(self.tick_data)
        self.storage.store_ohlcv(self.ohlcv_data)

        stats = self.storage.get_storage_stats()

        self.assertIn("timestamp", stats)
        self.assertIn("base_path", stats)
        self.assertIn("parquet_enabled", stats)
        self.assertIn("total_files", stats)
        self.assertIn("by_instrument", stats)
        self.assertIn("by_timeframe", stats)
        self.assertIn("by_format", stats)
        self.assertIn("total_size_bytes", stats)

    def test_supported_instruments(self):
        """Test supported instruments."""
        expected = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.assertEqual(self.storage.supported_instruments, expected)

    def test_supported_timeframes(self):
        """Test supported timeframes."""
        expected = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "H1": 16385,
            "H4": 16388,
            "D1": 16408,
        }
        self.assertEqual(self.storage.supported_timeframes, expected)

    def test_organize_data_to_warehouse_without_warehouse_manager(self):
        """Test organizing data without warehouse manager."""
        result = self.storage.organize_data_to_warehouse(
            instrument="EURUSD", timeframe="H1", data_type="validated"
        )

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_auto_organize_validated_data_without_warehouse_manager(self):
        """Test auto-organize without warehouse manager."""
        result = self.storage.auto_organize_validated_data()

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_get_warehouse_stats_without_warehouse_manager(self):
        """Test getting warehouse stats without warehouse manager."""
        result = self.storage.get_warehouse_stats()

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_validate_warehouse_integrity_without_warehouse_manager(self):
        """Test validating warehouse integrity without warehouse manager."""
        result = self.storage.validate_warehouse_integrity(instrument="EURUSD", timeframe="H1")

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_backup_warehouse_data_without_warehouse_manager(self):
        """Test backing up warehouse data without warehouse manager."""
        result = self.storage.backup_warehouse_data(backup_name="test_backup")

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_merge_update_to_historical_without_warehouse_manager(self):
        """Test merging update to historical without warehouse manager."""
        result = self.storage.merge_update_to_historical(instrument="EURUSD", timeframe="H1")

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])

    def test_schedule_warehouse_maintenance_without_warehouse_manager(self):
        """Test scheduling warehouse maintenance without warehouse manager."""
        result = self.storage.schedule_warehouse_maintenance()

        self.assertEqual(result["status"], "disabled")
        self.assertIn("Data Warehouse Manager not initialized", result["message"])


if __name__ == "__main__":
    unittest.main()
