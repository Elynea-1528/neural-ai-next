"""Unit tests for Historical Data Manager component.

Tests cover:
- Historical data request creation
- Job status tracking
- Data collection and validation
- Data gap identification
- Job management (CRUD operations)
- Database operations

Author: Neural AI Next Team
Date: 2025-12-17
"""

import shutil
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from fastapi import HTTPException

from neural_ai.collectors.mt5.data_validator import DataValidator
from neural_ai.collectors.mt5.error_handler import ErrorHandler
from neural_ai.collectors.mt5.implementations.historical_data_manager import (
    HistoricalDataManager,
    HistoricalJob,
    HistoricalJobStatus,
)
from neural_ai.collectors.mt5.implementations.storage.collector_storage import (
    CollectorStorage,
)


class TestHistoricalDataManager(unittest.TestCase):
    """Test cases for HistoricalDataManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Mock dependencies
        self.storage = Mock(spec=CollectorStorage)
        self.validator = Mock(spec=DataValidator)
        self.error_handler = Mock(spec=ErrorHandler)
        self.logger = Mock()

        # Create manager instance
        db_path = Path(self.temp_dir) / "historical_jobs.db"
        self.manager = HistoricalDataManager(
            storage=self.storage,
            validator=self.validator,
            error_handler=self.error_handler,
            logger=self.logger,
            db_path=str(db_path),
        )

        # Test data
        self.symbol = "EURUSD"
        self.timeframe = "H1"
        self.start_date = "2025-01-01"
        self.end_date = "2025-01-31"

        self.valid_bar = {
            "time": int(datetime.now().timestamp()),
            "open": 1.17450,
            "high": 1.17550,
            "low": 1.17400,
            "close": 1.17500,
            "volume": 1000,
        }

    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test HistoricalDataManager initialization."""
        self.assertEqual(self.manager.storage, self.storage)
        self.assertEqual(self.manager.validator, self.validator)
        self.assertEqual(self.manager.error_handler, self.error_handler)
        self.assertEqual(self.manager.logger, self.logger)
        self.assertIsNotNone(self.manager.jobs)
        self.assertIsNotNone(self.manager._lock)

    def test_request_historical_data_valid(self):
        """Test creating valid historical data request."""
        result = self.manager.request_historical_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_date=self.start_date,
            end_date=self.end_date,
            batch_size=365,
            priority="normal",
        )

        self.assertIn("job_id", result)
        self.assertIn("status", result)
        self.assertIn("estimated_duration", result)
        self.assertIn("total_batches", result)
        self.assertIn("message", result)

        # Check if job was created
        job_id = result["job_id"]
        self.assertIn(job_id, self.manager.jobs)

        # Check job details
        job = self.manager.jobs[job_id]
        self.assertEqual(job.symbol, self.symbol.upper())
        self.assertEqual(job.timeframe, self.timeframe.upper())
        self.assertEqual(job.status, HistoricalJobStatus.QUEUED)

    def test_request_historical_data_invalid_symbol(self):
        """Test creating historical data request with invalid symbol."""
        with self.assertRaises(HTTPException) as context:
            self.manager.request_historical_data(
                symbol="",
                timeframe=self.timeframe,
                start_date=self.start_date,
                end_date=self.end_date,
            )

        self.assertEqual(context.exception.status_code, 400)

    def test_request_historical_data_invalid_timeframe(self):
        """Test creating historical data request with invalid timeframe."""
        with self.assertRaises(HTTPException) as context:
            self.manager.request_historical_data(
                symbol=self.symbol,
                timeframe="",
                start_date=self.start_date,
                end_date=self.end_date,
            )

        self.assertEqual(context.exception.status_code, 400)

    def test_request_historical_data_invalid_dates(self):
        """Test creating historical data request with invalid dates."""
        with self.assertRaises(HTTPException) as context:
            self.manager.request_historical_data(
                symbol=self.symbol,
                timeframe=self.timeframe,
                start_date="2025-01-31",
                end_date="2025-01-01",
            )

        self.assertEqual(context.exception.status_code, 400)

    def test_request_historical_data_invalid_batch_size(self):
        """Test creating historical data request with invalid batch size."""
        with self.assertRaises(HTTPException) as context:
            self.manager.request_historical_data(
                symbol=self.symbol,
                timeframe=self.timeframe,
                start_date=self.start_date,
                end_date=self.end_date,
                batch_size=-1,
            )

        self.assertEqual(context.exception.status_code, 400)

    def test_get_job_status_existing_job(self):
        """Test getting status of existing job."""
        # Create a job first
        result = self.manager.request_historical_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        job_id = result["job_id"]
        status = self.manager.get_job_status(job_id)

        self.assertIn("job_id", status)
        self.assertIn("status", status)
        self.assertIn("progress", status)
        self.assertIn("current_batch", status)
        self.assertIn("errors", status)
        self.assertIn("warnings", status)

    def test_get_job_status_non_existing_job(self):
        """Test getting status of non-existing job."""
        with self.assertRaises(HTTPException) as context:
            self.manager.get_job_status("non_existing_job")

        self.assertEqual(context.exception.status_code, 404)

    def test_collect_historical_data_valid(self):
        """Test collecting historical data."""
        # Create a job first
        result = self.manager.request_historical_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        job_id = result["job_id"]

        # Mock validator
        self.validator.validate_ohlcv.return_value.is_valid = True

        # Collect data
        collect_result = self.manager.collect_historical_data(
            job_id=job_id,
            batch_number=1,
            symbol=self.symbol,
            timeframe=self.timeframe,
            date_range={"start": "2025-01-01", "end": "2025-01-07"},
            bars=[self.valid_bar],
        )

        self.assertIn("status", collect_result)
        self.assertIn("batch_number", collect_result)
        self.assertIn("bars_received", collect_result)
        self.assertIn("bars_stored", collect_result)
        self.assertEqual(collect_result["status"], "success")

    def test_collect_historical_data_invalid_bars(self):
        """Test collecting historical data with invalid bars."""
        # Create a job first
        result = self.manager.request_historical_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        job_id = result["job_id"]

        # Mock validator to return invalid result
        self.validator.validate_ohlcv.return_value.is_valid = False

        # Collect data
        collect_result = self.manager.collect_historical_data(
            job_id=job_id,
            batch_number=1,
            symbol=self.symbol,
            timeframe=self.timeframe,
            date_range={"start": "2025-01-01", "end": "2025-01-07"},
            bars=[self.valid_bar],
        )

        self.assertEqual(collect_result["status"], "success")
        self.assertEqual(collect_result["bars_stored"], 0)

    def test_collect_historical_data_non_existing_job(self):
        """Test collecting data for non-existing job."""
        with self.assertRaises(HTTPException) as context:
            self.manager.collect_historical_data(
                job_id="non_existing_job",
                batch_number=1,
                symbol=self.symbol,
                timeframe=self.timeframe,
                date_range={"start": "2025-01-01", "end": "2025-01-07"},
                bars=[self.valid_bar],
            )

        self.assertEqual(context.exception.status_code, 404)

    def test_identify_data_gaps(self):
        """Test identifying data gaps."""
        # Mock storage
        self.storage.supported_instruments = ["EURUSD", "GBPUSD"]
        self.storage.supported_timeframes = {"M1": 1, "H1": 16385}

        # Mock the _find_gaps_for_symbol_timeframe method
        with patch.object(self.manager, "_find_gaps_for_symbol_timeframe") as mock_find_gaps:
            mock_find_gaps.return_value = []

            result = self.manager.identify_data_gaps(
                symbol=self.symbol,
                timeframe=self.timeframe,
                start_date=self.start_date,
                end_date=self.end_date,
            )

        self.assertIn("analysis_period", result)
        self.assertIn("gaps", result)
        self.assertIn("total_gaps", result)
        self.assertIn("total_missing_bars", result)

    def test_historical_job_creation(self):
        """Test HistoricalJob creation."""
        job = HistoricalJob(
            job_id="test_job",
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
            batch_size=365,
            priority="normal",
        )

        self.assertEqual(job.job_id, "test_job")
        self.assertEqual(job.symbol, "EURUSD")
        self.assertEqual(job.timeframe, "H1")
        self.assertEqual(job.status, HistoricalJobStatus.QUEUED)
        self.assertEqual(job.progress, 0.0)

    def test_historical_job_calculate_progress(self):
        """Test HistoricalJob progress calculation."""
        job = HistoricalJob(
            job_id="test_job",
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
            total_batches=10,
            completed_batches=5,
        )

        progress = job.calculate_progress()

        self.assertEqual(progress, 50.0)

    def test_historical_job_to_dict(self):
        """Test converting HistoricalJob to dictionary."""
        job = HistoricalJob(
            job_id="test_job",
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
        )

        job_dict = job.to_dict()

        self.assertIn("job_id", job_dict)
        self.assertIn("symbol", job_dict)
        self.assertIn("timeframe", job_dict)
        self.assertIn("status", job_dict)
        self.assertIn("progress", job_dict)

    def test_historical_job_status_enum(self):
        """Test HistoricalJobStatus enum values."""
        self.assertEqual(HistoricalJobStatus.QUEUED.value, "queued")
        self.assertEqual(HistoricalJobStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(HistoricalJobStatus.COMPLETED.value, "completed")
        self.assertEqual(HistoricalJobStatus.FAILED.value, "failed")
        self.assertEqual(HistoricalJobStatus.CANCELLED.value, "cancelled")

    def test_convert_timeframe_to_int(self):
        """Test timeframe conversion to integer."""
        result = self.manager._convert_timeframe_to_int("H1")
        self.assertEqual(result, 16385)

        result = self.manager._convert_timeframe_to_int("M1")
        self.assertEqual(result, 1)

    def test_get_timeframe_minutes(self):
        """Test getting timeframe in minutes."""
        result = self.manager._get_timeframe_minutes("H1")
        self.assertEqual(result, 60)

        result = self.manager._get_timeframe_minutes("M1")
        self.assertEqual(result, 1)

    def test_get_batch_date_range(self):
        """Test getting batch date range."""
        job = HistoricalJob(
            job_id="test_job",
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
            batch_size=7,
        )

        date_range = self.manager._get_batch_date_range(job, 1)

        self.assertIsInstance(date_range, str)
        self.assertIn("to", date_range)

    def test_estimate_completion_time(self):
        """Test estimating completion time."""
        job = HistoricalJob(
            job_id="test_job",
            symbol="EURUSD",
            timeframe="H1",
            start_date="2025-01-01",
            end_date="2025-01-31",
            total_batches=10,
            completed_batches=5,
            status=HistoricalJobStatus.IN_PROGRESS,
            started_at=datetime.now().isoformat(),
        )

        completion_time = self.manager._estimate_completion_time(job)

        # Should return a string or None
        if completion_time is not None:
            self.assertIsInstance(completion_time, str)

    def test_database_operations(self):
        """Test database operations."""
        # Create a job
        result = self.manager.request_historical_data(
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        job_id = result["job_id"]
        job = self.manager.jobs[job_id]

        # Save job to database
        self.manager._save_job_to_db(job)

        # Load job from database
        loaded_job = self.manager._load_job_from_db(job_id)

        self.assertIsNotNone(loaded_job)
        self.assertEqual(loaded_job.job_id, job.job_id)
        self.assertEqual(loaded_job.symbol, job.symbol)
        self.assertEqual(loaded_job.timeframe, job.timeframe)


if __name__ == "__main__":
    unittest.main()
