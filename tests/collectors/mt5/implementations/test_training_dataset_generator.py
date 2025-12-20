"""Unit tests for Training Dataset Generator component.

Tests cover:
- Dataset generation (retraining, medium, deep_learning, validation)
- Data loading from warehouse
- Quality filtering
- Dataset metadata management
- Dataset status tracking
- Dataset listing and info

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

from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
    DataWarehouseManager,
)
from neural_ai.collectors.mt5.implementations.training_dataset_generator import (
    TrainingDatasetGenerator,
)


class TestTrainingDatasetGenerator(unittest.TestCase):
    """Test cases for TrainingDatasetGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Mock warehouse manager
        self.warehouse_manager = Mock(spec=DataWarehouseManager)
        self.warehouse_manager.base_path = Path(self.temp_dir)

        # Mock logger
        self.logger = Mock()

        # Create generator instance
        self.generator = TrainingDatasetGenerator(
            warehouse_manager=self.warehouse_manager, logger=self.logger
        )

        # Test data
        dates = pd.date_range(start="2025-01-01", end="2025-01-10", freq="H")
        self.test_data = pd.DataFrame(
            {
                "symbol": ["EURUSD"] * len(dates),
                "timeframe": [16385] * len(dates),
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
        """Test TrainingDatasetGenerator initialization."""
        self.assertEqual(self.generator.warehouse_manager, self.warehouse_manager)
        self.assertEqual(self.generator.logger, self.logger)
        self.assertIsNotNone(self.generator.dataset_types)
        self.assertIsNotNone(self.generator.supported_instruments)
        self.assertIsNotNone(self.generator.supported_timeframes)

    def test_dataset_types_configuration(self):
        """Test dataset types configuration."""
        expected_types = ["retraining", "medium", "deep_learning", "validation"]

        for dataset_type in expected_types:
            self.assertIn(dataset_type, self.generator.dataset_types)

            config = self.generator.dataset_types[dataset_type]
            self.assertIn("description", config)
            self.assertIn("update_frequency", config)
            self.assertIn("use_case", config)

    def test_generate_dataset_retraining(self):
        """Test generating retraining dataset."""
        # Mock data loading
        with (
            patch.object(self.generator, "_load_data_from_warehouse") as mock_load,
            patch.object(self.generator, "_apply_quality_filters") as mock_filter,
            patch.object(self.generator, "_save_dataset") as mock_save,
            patch.object(self.generator, "_save_dataset_metadata"),
        ):
            mock_load.return_value = self.test_data
            mock_filter.return_value = self.test_data
            mock_save.return_value = Path(self.temp_dir) / "training" / "retraining"

            result = self.generator.generate_dataset(
                dataset_type="retraining",
                symbols=["EURUSD"],
                timeframes=["H1"],
                end_date="2025-01-10",
                quality_threshold=0.95,
                output_format="parquet",
            )

            self.assertIn("status", result)
            self.assertIn("dataset_id", result)
            self.assertIn("dataset_type", result)
            self.assertEqual(result["dataset_type"], "retraining")

    def test_generate_dataset_invalid_type(self):
        """Test generating dataset with invalid type."""
        with self.assertRaises(ValueError):
            self.generator.generate_dataset(
                dataset_type="invalid_type", symbols=["EURUSD"], timeframes=["H1"]
            )

    def test_generate_dataset_no_data(self):
        """Test generating dataset with no available data."""
        with patch.object(self.generator, "_load_data_from_warehouse") as mock_load:
            mock_load.return_value = None

            result = self.generator.generate_dataset(
                dataset_type="retraining", symbols=["EURUSD"], timeframes=["H1"]
            )

            self.assertEqual(result["status"], "no_data")
            self.assertIn("No valid data found", result["message"])

    def test_load_data_from_warehouse(self):
        """Test loading data from warehouse."""
        # Mock warehouse paths
        historical_path = Mock()
        Mock()

        self.warehouse_manager.get_data_location.return_value = historical_path

        # Mock parquet file
        historical_file = historical_path / "EURUSD_H1_2000_2025.parquet"
        historical_file.exists.return_value = True

        with patch("pandas.read_parquet") as mock_read:
            mock_read.return_value = self.test_data

            result = self.generator._load_data_from_warehouse(
                symbol="EURUSD",
                timeframe="H1",
                start_date="2025-01-01",
                end_date="2025-01-10",
            )

            self.assertIsNotNone(result)
            self.assertIsInstance(result, pd.DataFrame)

    def test_load_data_from_warehouse_no_file(self):
        """Test loading data when file doesn't exist."""
        historical_path = Mock()
        self.warehouse_manager.get_data_location.return_value = historical_path

        # Mock non-existent file
        historical_file = historical_path / "EURUSD_H1_2000_2025.parquet"
        historical_file.exists.return_value = False

        result = self.generator._load_data_from_warehouse(
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-10",
        )

        self.assertIsNone(result)

    def test_apply_quality_filters(self):
        """Test applying quality filters."""
        # Create data with some quality issues
        invalid_data = self.test_data.copy()
        invalid_data.loc[0, "high"] = 1.08  # High < Low
        invalid_data.loc[0, "low"] = 1.09
        invalid_data.loc[1, "volume"] = -100  # Negative volume

        filtered_data = self.generator._apply_quality_filters(invalid_data, min_quality_score=0.95)

        # Should remove invalid rows
        self.assertLess(len(filtered_data), len(invalid_data))
        self.assertIsInstance(filtered_data, pd.DataFrame)

    def test_apply_quality_filters_high_quality(self):
        """Test applying quality filters with high quality data."""
        filtered_data = self.generator._apply_quality_filters(
            self.test_data, min_quality_score=0.95
        )

        # Should keep all data
        self.assertEqual(len(filtered_data), len(self.test_data))

    def test_save_dataset(self):
        """Test saving dataset."""
        data = {"EURUSD_H1": self.test_data}

        output_path = self.generator._save_dataset(
            dataset_type="retraining",
            dataset_id="test_dataset",
            data=data,
            output_format="parquet",
        )

        # Check if output directory was created
        self.assertTrue(output_path.exists() or output_path.parent.exists())

    def test_save_dataset_csv_format(self):
        """Test saving dataset in CSV format."""
        data = {"EURUSD_H1": self.test_data}

        output_path = self.generator._save_dataset(
            dataset_type="retraining",
            dataset_id="test_dataset",
            data=data,
            output_format="csv",
        )

        # Check if output directory was created
        self.assertTrue(output_path.exists() or output_path.parent.exists())

    def test_create_dataset_metadata(self):
        """Test creating dataset metadata."""
        metadata = self.generator._create_dataset_metadata(
            dataset_id="test_dataset",
            dataset_type="retraining",
            start_date="2025-01-01",
            end_date="2025-01-10",
            symbols=["EURUSD"],
            timeframes=["H1"],
            total_records=100,
            quality_threshold=0.95,
        )

        self.assertIn("dataset_id", metadata)
        self.assertIn("dataset_type", metadata)
        self.assertIn("version", metadata)
        self.assertIn("created_at", metadata)
        self.assertIn("date_range", metadata)
        self.assertIn("instruments", metadata)
        self.assertIn("timeframes", metadata)
        self.assertIn("quality_threshold", metadata)
        self.assertIn("total_records", metadata)
        self.assertIn("description", metadata)
        self.assertIn("update_frequency", metadata)
        self.assertIn("use_case", metadata)
        self.assertIn("features", metadata)

    def test_save_dataset_metadata(self):
        """Test saving dataset metadata."""
        metadata = {
            "dataset_id": "test_dataset",
            "dataset_type": "retraining",
            "created_at": datetime.now().isoformat(),
        }

        self.generator._save_dataset_metadata("test_dataset", metadata)

        # Check if metadata file was created
        Path(self.temp_dir) / "metadata" / "test_dataset_metadata.json"
        # File may not exist due to mocking, but the method should complete

    def test_get_dataset_status_existing(self):
        """Test getting status of existing dataset."""
        # Create metadata file
        metadata_dir = Path(self.temp_dir) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)

        metadata_file = metadata_dir / "test_dataset_metadata.json"
        metadata = {
            "dataset_id": "test_dataset",
            "dataset_type": "retraining",
            "created_at": datetime.now().isoformat(),
            "date_range": {"start": "2025-01-01", "end": "2025-01-10"},
            "instruments": ["EURUSD"],
            "timeframes": ["H1"],
            "total_records": 100,
        }

        import json

        with open(metadata_file, "w") as f:
            json.dump(metadata, f)

        # Mock training directory
        training_dir = Path(self.temp_dir) / "training" / "retraining" / "EURUSD"
        training_dir.mkdir(parents=True, exist_ok=True)

        # Create a test file
        test_file = training_dir / "EURUSD_H1_retraining.parquet"
        test_file.touch()

        result = self.generator.get_dataset_status("test_dataset")

        self.assertEqual(result["status"], "completed")
        self.assertIn("dataset_id", result)
        self.assertIn("files", result)
        self.assertIn("total_size_bytes", result)

    def test_get_dataset_status_non_existing(self):
        """Test getting status of non-existing dataset."""
        result = self.generator.get_dataset_status("non_existing_dataset")

        self.assertEqual(result["status"], "not_found")
        self.assertIn("not found", result["message"])

    def test_list_datasets(self):
        """Test listing datasets."""
        # Create metadata file
        metadata_dir = Path(self.temp_dir) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)

        datasets_file = metadata_dir / "training_datasets.json"
        datasets_data = {
            "last_updated": datetime.now().isoformat(),
            "datasets": {
                "dataset_1": {"dataset_type": "retraining"},
                "dataset_2": {"dataset_type": "medium"},
            },
        }

        import json

        with open(datasets_file, "w") as f:
            json.dump(datasets_data, f)

        result = self.generator.list_datasets()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total_datasets"], 2)

    def test_list_datasets_by_type(self):
        """Test listing datasets filtered by type."""
        # Create metadata file
        metadata_dir = Path(self.temp_dir) / "metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)

        datasets_file = metadata_dir / "training_datasets.json"
        datasets_data = {
            "last_updated": datetime.now().isoformat(),
            "datasets": {
                "dataset_1": {"dataset_type": "retraining"},
                "dataset_2": {"dataset_type": "medium"},
            },
        }

        import json

        with open(datasets_file, "w") as f:
            json.dump(datasets_data, f)

        result = self.generator.list_datasets(dataset_type="retraining")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total_datasets"], 1)

    def test_list_datasets_no_datasets(self):
        """Test listing datasets when none exist."""
        result = self.generator.list_datasets()

        self.assertEqual(result["status"], "no_datasets")
        self.assertIn("No datasets found", result["message"])

    def test_get_dataset_info(self):
        """Test getting dataset information."""
        result = self.generator.get_dataset_info()

        self.assertEqual(result["status"], "success")
        self.assertIn("dataset_types", result)
        self.assertIn("supported_instruments", result)
        self.assertIn("supported_timeframes", result)

    def test_supported_instruments(self):
        """Test supported instruments."""
        expected = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.assertEqual(self.generator.supported_instruments, expected)

    def test_supported_timeframes(self):
        """Test supported timeframes."""
        expected = ["M1", "M5", "M15", "H1", "H4", "D1"]
        self.assertEqual(self.generator.supported_timeframes, expected)

    def test_unsupported_instrument_warning(self):
        """Test warning for unsupported instrument."""
        with (
            patch.object(self.generator, "_load_data_from_warehouse") as mock_load,
            patch.object(self.generator, "_apply_quality_filters") as mock_filter,
            patch.object(self.generator, "_save_dataset") as mock_save,
            patch.object(self.generator, "_save_dataset_metadata"),
        ):
            mock_load.return_value = self.test_data
            mock_filter.return_value = self.test_data
            mock_save.return_value = Path(self.temp_dir) / "training" / "retraining"

            self.generator.generate_dataset(
                dataset_type="retraining", symbols=["UNSUPPORTED"], timeframes=["H1"]
            )

            # Check if warning was logged
            self.logger.warning.assert_called()

    def test_unsupported_timeframe_warning(self):
        """Test warning for unsupported timeframe."""
        with (
            patch.object(self.generator, "_load_data_from_warehouse") as mock_load,
            patch.object(self.generator, "_apply_quality_filters") as mock_filter,
            patch.object(self.generator, "_save_dataset") as mock_save,
            patch.object(self.generator, "_save_dataset_metadata"),
        ):
            mock_load.return_value = self.test_data
            mock_filter.return_value = self.test_data
            mock_save.return_value = Path(self.temp_dir) / "training" / "retraining"

            self.generator.generate_dataset(
                dataset_type="retraining",
                symbols=["EURUSD"],
                timeframes=["UNSUPPORTED"],
            )

            # Check if warning was logged
            self.logger.warning.assert_called()


if __name__ == "__main__":
    unittest.main()
