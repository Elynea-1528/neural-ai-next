"""Tests for Dead-Letter-Queue functionality.

This module contains comprehensive tests for the DLQ (Dead-Letter-Queue)
implementation, ensuring proper handling of corrupted or failed data.

Author: Neural AI Team
Date: 2025-12-18
"""

import shutil
import tempfile
from datetime import datetime

import pytest

from neural_ai.collectors.mt5.dlq import DeadLetterQueue
from neural_ai.collectors.mt5.exceptions import MT5DataValidationError


class TestDeadLetterQueue:
    """Test suite for DeadLetterQueue class."""

    @pytest.fixture
    def dlq(self):
        """Create a temporary DLQ for testing."""
        temp_dir = tempfile.mkdtemp()
        dlq = DeadLetterQueue(temp_dir, max_file_size_mb=1)
        yield dlq
        shutil.rmtree(temp_dir)

    def test_initialization(self, dlq):
        """Test DLQ initialization."""
        assert dlq.dlq_directory.exists()
        assert dlq.dlq_directory.is_dir()
        assert dlq.max_file_size == 1024 * 1024  # 1MB in bytes

    def test_record_failure(self, dlq):
        """Test recording a failure to DLQ."""
        error = MT5DataValidationError("Test validation error")
        data = {"symbol": "EURUSD", "price": 1.1234}
        context = {"timeframe": "M1"}

        dlq.record_failure(data, error, context, retryable=True)

        failures = dlq.get_failures(retryable_only=True)
        assert len(failures) == 1
        assert failures[0]["error_type"] == "MT5DataValidationError"
        assert failures[0]["data"]["symbol"] == "EURUSD"
        assert failures[0]["retryable"] is True
        assert "timestamp" in failures[0]

    def test_record_non_retryable_failure(self, dlq):
        """Test recording a non-retryable failure."""
        error = MT5DataValidationError("Permanent validation error")
        data = {"symbol": "GBPUSD", "price": 1.2500}
        context = {"timeframe": "H1"}

        dlq.record_failure(data, error, context, retryable=False)

        failures = dlq.get_failures(retryable_only=False)
        assert len(failures) == 1
        assert failures[0]["retryable"] is False

        # Should not appear in retryable-only query
        retryable_failures = dlq.get_failures(retryable_only=True)
        assert len(retryable_failures) == 0

    def test_get_failures_with_limit(self, dlq):
        """Test getting failures with limit."""
        # Record multiple failures
        for i in range(5):
            error = MT5DataValidationError(f"Error {i}")
            dlq.record_failure({"data": i}, error, retryable=True)

        # Get limited failures
        failures = dlq.get_failures(retryable_only=True, limit=3)
        assert len(failures) == 3

    def test_get_statistics(self, dlq):
        """Test DLQ statistics."""
        # Record some failures
        for i in range(3):
            error = MT5DataValidationError(f"Error {i}")
            dlq.record_failure({"data": i}, error, retryable=True)

        # Record a non-retryable failure
        error = MT5DataValidationError("Permanent error")
        dlq.record_failure({"data": "permanent"}, error, retryable=False)

        stats = dlq.get_statistics()

        assert stats["total_entries"] == 4
        assert stats["retryable_entries"] == 3
        assert stats["non_retryable_entries"] == 1
        assert "MT5DataValidationError" in stats["error_types"]
        assert stats["error_types"]["MT5DataValidationError"] == 4
        assert stats["oldest_entry"] is not None
        assert stats["newest_entry"] is not None

    def test_mark_as_processed(self, dlq):
        """Test marking a DLQ entry as processed."""
        error = MT5DataValidationError("Test error")
        dlq.record_failure({"data": "test"}, error, retryable=True)

        failures = dlq.get_failures(retryable_only=True)
        timestamp = failures[0]["timestamp"]

        result = dlq.mark_as_processed(timestamp)
        assert result is True

    def test_file_rotation(self, dlq):
        """Test DLQ file rotation."""
        # Record many failures to trigger rotation
        large_data = {"data": "x" * 10000}  # 10KB per entry

        for i in range(150):  # Should trigger rotation around 100 entries
            error = MT5DataValidationError(f"Error {i}")
            dlq.record_failure(large_data, error, retryable=True)

        # Check if multiple files were created
        dlq_files = list(dlq.dlq_directory.glob("corrupted_ticks_*.jsonl"))
        assert len(dlq_files) >= 1  # At least one file should exist

        # Verify all entries are accessible
        failures = dlq.get_failures(retryable_only=True)
        assert len(failures) == 150

    def test_context_preservation(self, dlq):
        """Test that context is preserved in DLQ entries."""
        error = MT5DataValidationError("Context test error")
        data = {"symbol": "USDJPY"}
        context = {
            "timeframe": "M5",
            "symbol": "USDJPY",
            "timestamp": 1234567890,
            "custom_field": "custom_value",
        }

        dlq.record_failure(data, error, context, retryable=True)

        failures = dlq.get_failures(retryable_only=True)
        assert len(failures) == 1
        assert failures[0]["context"] == context

    def test_error_message_preservation(self, dlq):
        """Test that error messages are preserved."""
        error_message = "This is a detailed error message with special chars: áéíóöőüű"
        error = MT5DataValidationError(error_message)

        dlq.record_failure({"data": "test"}, error, retryable=True)

        failures = dlq.get_failures(retryable_only=True)
        assert len(failures) == 1
        assert failures[0]["error_message"] == error_message

    def test_empty_dlq_statistics(self, dlq):
        """Test statistics for empty DLQ."""
        stats = dlq.get_statistics()

        assert stats["total_entries"] == 0
        assert stats["retryable_entries"] == 0
        assert stats["non_retryable_entries"] == 0
        assert stats["error_types"] == {}
        assert stats["oldest_entry"] is None
        assert stats["newest_entry"] is None

    def test_timestamp_format(self, dlq):
        """Test that timestamps are in ISO format."""
        error = MT5DataValidationError("Timestamp test")
        dlq.record_failure({"data": "test"}, error, retryable=True)

        failures = dlq.get_failures(retryable_only=True)
        timestamp = failures[0]["timestamp"]

        # Should be valid ISO format
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Invalid ISO format timestamp: {timestamp}")


class TestDeadLetterQueueIntegration:
    """Integration tests for DLQ with real scenarios."""

    @pytest.fixture
    def dlq(self):
        """Create a temporary DLQ for integration testing."""
        temp_dir = tempfile.mkdtemp()
        dlq = DeadLetterQueue(temp_dir, max_file_size_mb=10)
        yield dlq
        shutil.rmtree(temp_dir)

    def test_multiple_error_types(self, dlq):
        """Test handling multiple error types."""
        from neural_ai.collectors.mt5.exceptions import (
            MT5ConnectionError,
            MT5DataValidationError,
            MT5TimeoutError,
        )

        errors = [
            MT5DataValidationError("Validation failed"),
            MT5ConnectionError("Connection lost"),
            MT5TimeoutError("Request timed out"),
            MT5DataValidationError("Another validation error"),
        ]

        for error in errors:
            dlq.record_failure(
                {"symbol": "EURUSD"}, error, context={"timeframe": "M1"}, retryable=True
            )

        stats = dlq.get_statistics()

        assert stats["total_entries"] == 4
        assert stats["error_types"]["MT5DataValidationError"] == 2
        assert stats["error_types"]["MT5ConnectionError"] == 1
        assert stats["error_types"]["MT5TimeoutError"] == 1

    def test_high_volume_failures(self, dlq):
        """Test handling high volume of failures."""
        num_failures = 1000

        for i in range(num_failures):
            error = MT5DataValidationError(f"Error {i}")
            dlq.record_failure(
                {"symbol": f"SYMBOL_{i % 10}", "price": i},
                error,
                context={"batch": i // 100},
                retryable=(i % 2 == 0),  # Alternate retryable
            )

        stats = dlq.get_statistics()

        assert stats["total_entries"] == num_failures
        assert stats["retryable_entries"] == num_failures // 2
        assert stats["non_retryable_entries"] == num_failures // 2

        # Verify all entries are retrievable
        all_failures = dlq.get_failures(retryable_only=False)
        assert len(all_failures) == num_failures

        retryable_only = dlq.get_failures(retryable_only=True)
        assert len(retryable_only) == num_failures // 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
