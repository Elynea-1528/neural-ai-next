"""Unit tests for Error Handler component.

Tests cover:
- Error creation and categorization
- Error handling and logging
- Error statistics tracking
- Recovery suggestions
- Error storage and reporting

Author: Neural AI Next Team
Date: 2025-12-17
"""

import unittest
from unittest.mock import Mock, patch

from neural_ai.collectors.mt5.error_handler import (
    CollectorError,
    ConfigurationError,
    DataQualityError,
    ErrorCategory,
    ErrorHandler,
    ErrorSeverity,
    NetworkError,
    StorageError,
    ValidationError,
)


class TestErrorHandler(unittest.TestCase):
    """Test cases for ErrorHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.error_handler = ErrorHandler(logger=self.logger)

        # Reset statistics before each test
        self.error_handler.reset_statistics()

    def test_collector_error_creation(self):
        """Test creating a basic CollectorError."""
        error = CollectorError(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
        )

        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.category, ErrorCategory.VALIDATION)
        self.assertEqual(error.severity, ErrorSeverity.ERROR)
        self.assertIsNotNone(error.timestamp)

    def test_collector_error_to_dict(self):
        """Test converting CollectorError to dictionary."""
        error = CollectorError(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            details={"key": "value"},
        )

        error_dict = error.to_dict()

        self.assertIn("message", error_dict)
        self.assertIn("category", error_dict)
        self.assertIn("severity", error_dict)
        self.assertIn("details", error_dict)
        self.assertIn("timestamp", error_dict)
        self.assertEqual(error_dict["message"], "Test error")

    def test_collector_error_str(self):
        """Test string representation of CollectorError."""
        error = CollectorError(
            message="Test error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
        )

        error_str = str(error)

        self.assertIn("Test error", error_str)
        self.assertIn("VALIDATION", error_str)
        self.assertIn("ERROR", error_str)

    def test_validation_error_creation(self):
        """Test creating a ValidationError."""
        error = ValidationError(message="Validation failed", details={"field": "price"})

        self.assertEqual(error.message, "Validation failed")
        self.assertEqual(error.category, ErrorCategory.VALIDATION)
        self.assertEqual(error.severity, ErrorSeverity.WARNING)

    def test_storage_error_creation(self):
        """Test creating a StorageError."""
        error = StorageError(message="Storage failed", details={"file": "data.csv"})

        self.assertEqual(error.message, "Storage failed")
        self.assertEqual(error.category, ErrorCategory.STORAGE)
        self.assertEqual(error.severity, ErrorSeverity.ERROR)

    def test_network_error_creation(self):
        """Test creating a NetworkError."""
        error = NetworkError(message="Connection failed", details={"host": "127.0.0.1"})

        self.assertEqual(error.message, "Connection failed")
        self.assertEqual(error.category, ErrorCategory.NETWORK)
        self.assertEqual(error.severity, ErrorSeverity.ERROR)

    def test_configuration_error_creation(self):
        """Test creating a ConfigurationError."""
        error = ConfigurationError(message="Config invalid", details={"param": "missing"})

        self.assertEqual(error.message, "Config invalid")
        self.assertEqual(error.category, ErrorCategory.CONFIGURATION)
        self.assertEqual(error.severity, ErrorSeverity.CRITICAL)

    def test_data_quality_error_creation(self):
        """Test creating a DataQualityError."""
        error = DataQualityError(message="Quality issue", details={"score": 0.5})

        self.assertEqual(error.message, "Quality issue")
        self.assertEqual(error.category, ErrorCategory.DATA_QUALITY)
        self.assertEqual(error.severity, ErrorSeverity.WARNING)

    def test_handle_error(self):
        """Test handling an error."""
        error = ValidationError(message="Test validation error")

        self.error_handler.handle_error(error)

        # Check if statistics were updated
        self.assertEqual(self.error_handler.error_stats["total_errors"], 1)
        self.assertEqual(self.error_handler.error_stats["by_category"]["VALIDATION"], 1)
        self.assertEqual(self.error_handler.error_stats["by_severity"]["WARNING"], 1)

        # Check if error was added to recent errors
        self.assertEqual(len(self.error_handler.error_stats["recent_errors"]), 1)

        # Check if logger was called
        self.logger.warning.assert_called_once()

    def test_handle_multiple_errors(self):
        """Test handling multiple errors."""
        errors = [
            ValidationError(message="Error 1"),
            StorageError(message="Error 2"),
            NetworkError(message="Error 3"),
        ]

        for error in errors:
            self.error_handler.handle_error(error)

        # Check statistics
        self.assertEqual(self.error_handler.error_stats["total_errors"], 3)
        self.assertEqual(self.error_handler.error_stats["by_category"]["VALIDATION"], 1)
        self.assertEqual(self.error_handler.error_stats["by_category"]["STORAGE"], 1)
        self.assertEqual(self.error_handler.error_stats["by_category"]["NETWORK"], 1)

    def test_recent_errors_limit(self):
        """Test that recent errors list is limited."""
        # Add more than 100 errors
        for i in range(110):
            error = ValidationError(message=f"Error {i}")
            self.error_handler.handle_error(error)

        # Check that only 100 errors are kept
        self.assertEqual(len(self.error_handler.error_stats["recent_errors"]), 100)

    @patch("builtins.open", create=True)
    def test_store_error(self, mock_open):
        """Test storing error to file."""
        error = ValidationError(message="Test error")

        self.error_handler._store_error(error)

        # Check if file was opened for writing
        mock_open.assert_called_once()

        # Check if write was called
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_once()

    def test_get_error_report(self):
        """Test generating error report."""
        # Add some errors
        self.error_handler.handle_error(ValidationError(message="Error 1"))
        self.error_handler.handle_error(StorageError(message="Error 2"))

        report = self.error_handler.get_error_report()

        self.assertIn("timestamp", report)
        self.assertIn("total_errors", report)
        self.assertIn("by_category", report)
        self.assertIn("by_severity", report)
        self.assertIn("recent_errors_count", report)

        self.assertEqual(report["total_errors"], 2)
        self.assertEqual(report["recent_errors_count"], 2)

    @patch("builtins.open", create=True)
    def test_save_error_report(self, mock_open):
        """Test saving error report to file."""
        filepath = "logs/test_error_report.json"

        self.error_handler.save_error_report(filepath)

        # Check if file was opened for writing
        mock_open.assert_called_once()

    def test_get_recovery_suggestion_validation(self):
        """Test getting recovery suggestion for validation error."""
        error = ValidationError(message="Validation failed")

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Check the data source", suggestion)

    def test_get_recovery_suggestion_storage(self):
        """Test getting recovery suggestion for storage error."""
        error = StorageError(message="Storage failed")

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Check disk space", suggestion)

    def test_get_recovery_suggestion_network(self):
        """Test getting recovery suggestion for network error."""
        error = NetworkError(message="Network failed")

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Check network connectivity", suggestion)

    def test_get_recovery_suggestion_configuration(self):
        """Test getting recovery suggestion for configuration error."""
        error = ConfigurationError(message="Config failed")

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Review configuration files", suggestion)

    def test_get_recovery_suggestion_data_quality(self):
        """Test getting recovery suggestion for data quality error."""
        error = DataQualityError(message="Quality failed")

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Monitor data quality metrics", suggestion)

    def test_get_recovery_suggestion_system(self):
        """Test getting recovery suggestion for system error."""
        error = CollectorError(message="System failed", category=ErrorCategory.SYSTEM)

        suggestion = self.error_handler.get_recovery_suggestion(error)

        self.assertIsInstance(suggestion, str)
        self.assertIn("Check system resources", suggestion)

    def test_reset_statistics(self):
        """Test resetting error statistics."""
        # Add some errors
        self.error_handler.handle_error(ValidationError(message="Error 1"))
        self.error_handler.handle_error(StorageError(message="Error 2"))

        # Reset statistics
        self.error_handler.reset_statistics()

        # Check if statistics are reset
        self.assertEqual(self.error_handler.error_stats["total_errors"], 0)
        self.assertEqual(len(self.error_handler.error_stats["by_category"]), 0)
        self.assertEqual(len(self.error_handler.error_stats["by_severity"]), 0)
        self.assertEqual(len(self.error_handler.error_stats["recent_errors"]), 0)

        # Check if logger was called
        self.logger.info.assert_called_with("Error statistics reset")

    def test_error_severity_enum(self):
        """Test ErrorSeverity enum values."""
        self.assertEqual(ErrorSeverity.INFO.value, "INFO")
        self.assertEqual(ErrorSeverity.WARNING.value, "WARNING")
        self.assertEqual(ErrorSeverity.ERROR.value, "ERROR")
        self.assertEqual(ErrorSeverity.CRITICAL.value, "CRITICAL")

    def test_error_category_enum(self):
        """Test ErrorCategory enum values."""
        self.assertEqual(ErrorCategory.VALIDATION.value, "VALIDATION")
        self.assertEqual(ErrorCategory.NETWORK.value, "NETWORK")
        self.assertEqual(ErrorCategory.STORAGE.value, "STORAGE")
        self.assertEqual(ErrorCategory.CONFIGURATION.value, "CONFIGURATION")
        self.assertEqual(ErrorCategory.DATA_QUALITY.value, "DATA_QUALITY")
        self.assertEqual(ErrorCategory.SYSTEM.value, "SYSTEM")

    def test_error_handler_initialization(self):
        """Test ErrorHandler initialization."""
        # Test with custom logger
        custom_logger = Mock()
        handler = ErrorHandler(logger=custom_logger)

        self.assertEqual(handler.logger, custom_logger)
        self.assertIsNotNone(handler.error_log_dir)
        self.assertIsNotNone(handler.error_log_file)

        # Test with default logger
        handler = ErrorHandler()
        self.assertIsNotNone(handler.logger)

    def test_error_log_directory_creation(self):
        """Test that error log directory is created."""
        handler = ErrorHandler()

        # Check if directory exists or can be created
        self.assertTrue(handler.error_log_dir.exists() or handler.error_log_dir.parent.exists())


if __name__ == "__main__":
    unittest.main()
