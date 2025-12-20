"""Unit tests for Data Warehouse Manager component.

Tests cover:
- Warehouse structure initialization
- Data movement between locations
- Data merging (update to historical)
- Data archiving
- Data cleanup
- Warehouse statistics
- Data integrity validation
- Backup and restore operations

Author: Neural AI Next Team
Date: 2025-12-17
"""

import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import numpy as np
import pandas as pd

from neural_ai.collectors.mt5.error_handler import StorageError
from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
    DataWarehouseManager,
)


class TestDataWarehouseManager(unittest.TestCase):
    """Test cases for DataWarehouseManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Mock logger
        self.logger = Mock()

        # Create warehouse manager
        self.warehouse = DataWarehouseManager(base_path=self.temp_dir, logger=self.logger)

        # Test data
        dates = pd.date_range(start="2025-01-01", end="2025-01-10", freq="H")
        self.test_data = pd.DataFrame(
            {
                "time": [int(d.timestamp()) for d in dates],
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

    def test_initialization(self):
        """Test DataWarehouseManager initialization."""
        self.assertEqual(self.warehouse.base_path, Path(self.temp_dir))
        self.assertEqual(self.warehouse.logger, self.logger)
        self.assertIsNotNone(self.warehouse.warehouse_structure)
        self.assertIsNotNone(self.warehouse.supported_instruments)
        self.assertIsNotNone(self.warehouse.supported_timeframes)

    def test_warehouse_structure_creation(self):
        """Test warehouse structure creation."""
        # Check if base directories were created
        for category in ["warehouse", "training"]:
            category_path = self.warehouse.base_path / category
            self.assertTrue(category_path.exists())

            # Check subdirectories
            for subdir in self.warehouse.warehouse_structure[category]:
                subdir_path = category_path / subdir
                self.assertTrue(subdir_path.exists())

    def test_metadata_files_creation(self):
        """Test metadata files creation."""
        metadata_path = self.warehouse.base_path / "metadata"

        # Check if metadata files exist
        expected_files = [
            "instruments.json",
            "timeframes.json",
            "data_quality.json",
            "collection_jobs.json",
            "training_datasets.json",
            "gaps.json",
        ]

        for filename in expected_files:
            file_path = metadata_path / filename
            self.assertTrue(file_path.exists())

    def test_move_data(self):
        """Test moving data between locations."""
        # Create source data
        source_dir = self.warehouse.base_path / "warehouse" / "realtime" / "EURUSD" / "H1"
        source_dir.mkdir(parents=True, exist_ok=True)

        test_file = source_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Move data
        result = self.warehouse.move_data(
            source_path="warehouse/realtime",
            destination_path="warehouse/update",
            instrument="EURUSD",
            timeframe="H1",
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("files_moved", result)
        self.assertGreater(len(result["files_moved"]), 0)

        # Check if file was moved
        dest_dir = self.warehouse.base_path / "warehouse" / "update" / "EURUSD" / "H1"
        self.assertTrue(dest_dir.exists())

    def test_move_data_source_not_exists(self):
        """Test moving data when source doesn't exist."""
        with self.assertRaises(StorageError):
            self.warehouse.move_data(
                source_path="warehouse/nonexistent",
                destination_path="warehouse/update",
                instrument="EURUSD",
                timeframe="H1",
            )

    def test_merge_update_to_historical(self):
        """Test merging update data to historical."""
        # Create update data
        update_dir = self.warehouse.base_path / "warehouse" / "update" / "EURUSD" / "H1"
        update_dir.mkdir(parents=True, exist_ok=True)

        update_file = update_dir / "update_data.parquet"
        self.test_data.to_parquet(update_file, engine="fastparquet", compression="snappy")

        # Merge
        result = self.warehouse.merge_update_to_historical(instrument="EURUSD", timeframe="H1")

        self.assertEqual(result["status"], "success")
        self.assertIn("historical_records", result)
        self.assertIn("update_records", result)

        # Check if historical file was created
        historical_file = (
            self.warehouse.base_path
            / "warehouse"
            / "historical"
            / "EURUSD"
            / "H1"
            / "EURUSD_H1_2000_2025.parquet"
        )
        self.assertTrue(historical_file.exists())

    def test_merge_update_to_historical_no_data(self):
        """Test merging when no update data exists."""
        result = self.warehouse.merge_update_to_historical(instrument="GBPUSD", timeframe="H1")

        self.assertEqual(result["status"], "no_data")
        self.assertIn("No update data found", result["message"])

    def test_archive_data(self):
        """Test archiving data."""
        # Create source data
        source_dir = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        source_dir.mkdir(parents=True, exist_ok=True)

        test_file = source_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Archive
        result = self.warehouse.archive_data(
            source_path="warehouse/historical",
            archive_name="test_archive",
            instrument="EURUSD",
            timeframe="H1",
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("files_archived", result)
        self.assertGreater(len(result["files_archived"]), 0)

        # Check if archive was created
        archive_dir = self.warehouse.base_path / "archive" / "test_archive" / "EURUSD" / "H1"
        self.assertTrue(archive_dir.exists())

    def test_cleanup_old_data(self):
        """Test cleaning up old data."""
        # Create old data file
        source_dir = self.warehouse.base_path / "warehouse" / "realtime" / "EURUSD" / "H1"
        source_dir.mkdir(parents=True, exist_ok=True)

        test_file = source_dir / "old_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Make file old by modifying its timestamp
        old_time = datetime.now().timestamp() - (40 * 24 * 60 * 60)  # 40 days ago
        import os

        os.utime(test_file, (old_time, old_time))

        # Cleanup
        result = self.warehouse.cleanup_old_data(
            source_path="warehouse/realtime", retention_days=30
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("deleted_files", result)

    def test_cleanup_old_data_no_data(self):
        """Test cleanup when source doesn't exist."""
        result = self.warehouse.cleanup_old_data(
            source_path="warehouse/nonexistent", retention_days=30
        )

        self.assertEqual(result["status"], "no_data")

    def test_get_warehouse_stats(self):
        """Test getting warehouse statistics."""
        # Create some test data
        historical_dir = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        historical_dir.mkdir(parents=True, exist_ok=True)

        test_file = historical_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Get stats
        stats = self.warehouse.get_warehouse_stats()

        self.assertIn("timestamp", stats)
        self.assertIn("warehouse", stats)
        self.assertIn("training", stats)
        self.assertIn("total_size_bytes", stats)
        self.assertIn("total_files", stats)
        self.assertGreater(stats["total_files"], 0)

    def test_validate_data_integrity_valid(self):
        """Test validating data integrity with valid data."""
        # Create valid data
        historical_dir = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        historical_dir.mkdir(parents=True, exist_ok=True)

        test_file = historical_dir / "EURUSD_H1_2000_2025.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Validate
        result = self.warehouse.validate_data_integrity(
            instrument="EURUSD", timeframe="H1", location="warehouse/historical"
        )

        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["issues_found"], 0)

    def test_validate_data_integrity_invalid(self):
        """Test validating data integrity with invalid data."""
        # Create invalid data (empty DataFrame)
        historical_dir = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        historical_dir.mkdir(parents=True, exist_ok=True)

        test_file = historical_dir / "EURUSD_H1_2000_2025.parquet"
        empty_data = pd.DataFrame()
        empty_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Validate
        result = self.warehouse.validate_data_integrity(
            instrument="EURUSD", timeframe="H1", location="warehouse/historical"
        )

        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["issues_found"], 0)

    def test_validate_data_integrity_no_data(self):
        """Test validating data integrity when no data exists."""
        result = self.warehouse.validate_data_integrity(
            instrument="GBPUSD", timeframe="H1", location="warehouse/historical"
        )

        self.assertEqual(result["status"], "no_data")
        self.assertIn("No data found", result["message"])

    def test_backup_data(self):
        """Test backing up data."""
        # Create test data
        historical_dir = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        historical_dir.mkdir(parents=True, exist_ok=True)

        test_file = historical_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Backup
        result = self.warehouse.backup_data(
            source_path="warehouse/historical",
            backup_name="test_backup",
            instruments=["EURUSD"],
            timeframes=["H1"],
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("backup_path", result)
        self.assertGreater(result["files_backed_up"], 0)

        # Check if backup was created
        backup_dir = self.warehouse.base_path / "backup" / "test_backup"
        self.assertTrue(backup_dir.exists())

    def test_backup_data_source_not_exists(self):
        """Test backing up data when source doesn't exist."""
        with self.assertRaises(StorageError):
            self.warehouse.backup_data(
                source_path="warehouse/nonexistent", backup_name="test_backup"
            )

    def test_restore_data(self):
        """Test restoring data from backup."""
        # Create backup first
        backup_dir = self.warehouse.base_path / "backup" / "test_backup" / "EURUSD" / "H1"
        backup_dir.mkdir(parents=True, exist_ok=True)

        test_file = backup_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Restore
        result = self.warehouse.restore_data(
            backup_name="test_backup",
            target_path="warehouse/restored",
            instruments=["EURUSD"],
            timeframes=["H1"],
        )

        self.assertEqual(result["status"], "success")
        self.assertIn("restored_to", result)
        self.assertGreater(result["files_restored"], 0)

        # Check if data was restored
        restored_dir = self.warehouse.base_path / "warehouse" / "restored" / "EURUSD" / "H1"
        self.assertTrue(restored_dir.exists())

    def test_restore_data_backup_not_exists(self):
        """Test restoring data when backup doesn't exist."""
        with self.assertRaises(StorageError):
            self.warehouse.restore_data(
                backup_name="nonexistent_backup", target_path="warehouse/restored"
            )

    def test_get_data_location(self):
        """Test getting data location."""
        location = self.warehouse.get_data_location(
            instrument="EURUSD", timeframe="H1", data_type="historical"
        )

        expected = self.warehouse.base_path / "warehouse" / "historical" / "EURUSD" / "H1"
        self.assertEqual(location, expected)

    def test_get_data_location_invalid_type(self):
        """Test getting data location with invalid type."""
        with self.assertRaises(ValueError):
            self.warehouse.get_data_location(
                instrument="EURUSD", timeframe="H1", data_type="invalid"
            )

    def test_supported_instruments(self):
        """Test supported instruments."""
        expected = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.assertEqual(self.warehouse.supported_instruments, expected)

    def test_supported_timeframes(self):
        """Test supported timeframes."""
        expected = ["M1", "M5", "M15", "H1", "H4", "D1"]
        self.assertEqual(self.warehouse.supported_timeframes, expected)

    def test_calculate_directory_stats(self):
        """Test calculating directory statistics."""
        # Create test data
        test_dir = self.warehouse.base_path / "test_dir" / "EURUSD" / "H1"
        test_dir.mkdir(parents=True, exist_ok=True)

        test_file = test_dir / "test_data.parquet"
        self.test_data.to_parquet(test_file, engine="fastparquet", compression="snappy")

        # Calculate stats
        stats = self.warehouse._calculate_directory_stats(test_dir.parent.parent)

        self.assertIn("file_count", stats)
        self.assertIn("size_bytes", stats)
        self.assertIn("instruments", stats)
        self.assertIn("timeframes", stats)
        self.assertGreater(stats["file_count"], 0)
        self.assertGreater(stats["size_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
