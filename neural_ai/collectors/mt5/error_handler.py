"""Error Handler for MT5 Collector.
================================

Provides comprehensive error handling and recovery mechanisms for the MT5 Collector system.

Features:
- Centralized error handling
- Error categorization and logging
- Recovery strategies
- Error reporting and alerting

Author: Neural AI Next Team
Date: 2025-12-15
"""

import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ErrorSeverity(Enum):
    """Error severity levels."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorCategory(Enum):
    """Error categories."""

    VALIDATION = "VALIDATION"
    NETWORK = "NETWORK"
    STORAGE = "STORAGE"
    CONFIGURATION = "CONFIGURATION"
    DATA_QUALITY = "DATA_QUALITY"
    SYSTEM = "SYSTEM"


class CollectorError(Exception):
    """Base exception class for MT5 Collector errors.

    Attributes:
        message: Error message
        category: Error category
        severity: Error severity
        details: Additional error details
    """

    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.timestamp = datetime.now()

        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        return (
            f"[{self.severity.value}] {self.category.value}: {self.message} "
            f"(Details: {self.details})"
        )


class ValidationError(CollectorError):
    """Validation-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.WARNING,
            details=details,
        )


class StorageError(CollectorError):
    """Storage-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            category=ErrorCategory.STORAGE,
            severity=ErrorSeverity.ERROR,
            details=details,
        )


class NetworkError(CollectorError):
    """Network-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.ERROR,
            details=details,
        )


class ConfigurationError(CollectorError):
    """Configuration-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.CRITICAL,
            details=details,
        )


class DataQualityError(CollectorError):
    """Data quality-related errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message,
            category=ErrorCategory.DATA_QUALITY,
            severity=ErrorSeverity.WARNING,
            details=details,
        )


class ErrorHandler:
    """Centralized error handler for MT5 Collector.

    Responsibilities:
    - Log errors with appropriate severity
    - Categorize and track errors
    - Store error reports
    - Provide error recovery suggestions
    - Generate error statistics
    """

    def __init__(self, logger: logging.Logger | None = None):
        """Initialize the ErrorHandler.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

        # Error tracking
        self.error_stats: dict[str, Any] = {
            "total_errors": 0,
            "by_category": {},
            "by_severity": {},
            "recent_errors": [],
        }

        # Error storage
        self.error_log_dir = Path("logs")
        self.error_log_dir.mkdir(parents=True, exist_ok=True)
        self.error_log_file = self.error_log_dir / "collector_errors.jsonl"

    def handle_error(self, error: CollectorError) -> None:
        """Handle an error by logging and storing it.

        Args:
            error: CollectorError instance
        """
        # Update statistics
        self.error_stats["total_errors"] += 1

        category = error.category.value
        severity = error.severity.value

        self.error_stats["by_category"][category] = (
            self.error_stats["by_category"].get(category, 0) + 1
        )

        self.error_stats["by_severity"][severity] = (
            self.error_stats["by_severity"].get(severity, 0) + 1
        )

        # Keep recent errors (last 100)
        self.error_stats["recent_errors"].append(error.to_dict())
        if len(self.error_stats["recent_errors"]) > 100:
            self.error_stats["recent_errors"].pop(0)

        # Log error
        log_method = getattr(self.logger, error.severity.value.lower())
        log_method(str(error))

        # Store error to file
        self._store_error(error)

    def _store_error(self, error: CollectorError) -> None:
        """Store error to JSONL file.

        Args:
            error: CollectorError instance
        """
        try:
            with open(self.error_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(error.to_dict()) + "\n")
        except OSError as e:
            self.logger.exception(
                f"Failed to store error to file: {self.error_log_file}", stack_info=True
            )
            self.logger.error(f"Storage error: {e}")
        except Exception as e:
            self.logger.exception(
                f"Unexpected error while storing error: {self.error_log_file}",
                stack_info=True,
            )
            self.logger.error(f"Failed to store error: {e}")

    def get_error_report(self) -> dict[str, Any]:
        """Generate error statistics report.

        Returns:
            Dictionary containing error statistics
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "total_errors": self.error_stats["total_errors"],
            "by_category": self.error_stats["by_category"],
            "by_severity": self.error_stats["by_severity"],
            "recent_errors_count": len(self.error_stats["recent_errors"]),
        }

    def save_error_report(self, filepath: str) -> None:
        """Save error report to file.

        Args:
            filepath: Path to save the report
        """
        report = self.get_error_report()
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except OSError as e:
            self.logger.exception(
                f"Failed to save error report to file: {filepath}", stack_info=True
            )
            raise StorageError(
                f"Failed to save error report: {e}", details={"filepath": str(filepath)}
            )
        except Exception as e:
            self.logger.exception(
                f"Unexpected error while saving error report: {filepath}",
                stack_info=True,
            )
            raise StorageError(
                f"Failed to save error report: {e}", details={"filepath": str(filepath)}
            )

    def get_recovery_suggestion(self, error: CollectorError) -> str:
        """Get recovery suggestion for an error.

        Args:
            error: CollectorError instance

        Returns:
            Recovery suggestion message
        """
        suggestions = {
            ErrorCategory.VALIDATION: (
                "Check the data source for quality issues. "
                "Invalid data has been stored separately for analysis."
            ),
            ErrorCategory.STORAGE: (
                "Check disk space and file permissions. Ensure the data directory is accessible."
            ),
            ErrorCategory.NETWORK: (
                "Check network connectivity and MT5 Expert Advisor status. "
                "Verify that the EA is running and can reach the collector."
            ),
            ErrorCategory.CONFIGURATION: (
                "Review configuration files for errors. "
                "Check that all required settings are present and valid."
            ),
            ErrorCategory.DATA_QUALITY: (
                "Monitor data quality metrics. Consider implementing additional validation rules."
            ),
            ErrorCategory.SYSTEM: (
                "Check system resources and logs. "
                "Consider restarting the collector if the issue persists."
            ),
        }

        return suggestions.get(error.category, "Review system logs for details.")

    def reset_statistics(self) -> None:
        """Reset error statistics."""
        self.error_stats = {
            "total_errors": 0,
            "by_category": {},
            "by_severity": {},
            "recent_errors": [],
        }
        self.logger.info("Error statistics reset")

    def store_error_to_file(
        self,
        error: Exception,
        context: dict[str, Any] | None = None,
        collector: Any | None = None,
    ) -> None:
        """Store error to file and DLQ if available.

        Args:
            error: Exception to store
            context: Additional context information
            collector: Optional MT5Collector instance for DLQ integration
        """
        # Convert to CollectorError if not already
        if not isinstance(error, CollectorError):
            error = CollectorError(
                message=str(error),
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.ERROR,
                details=context or {},
            )

        # Handle error normally
        self.handle_error(error)

        # Also record to DLQ if collector is provided
        if collector and hasattr(collector, "_dlq"):
            try:
                collector._dlq.record_failure(
                    data=context or {},
                    error=error,
                    context={"source": "ErrorHandler"},
                    retryable=False,
                )
            except Exception as dlq_error:
                self.logger.error(f"Failed to record error to DLQ: {dlq_error}")


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Create error handler
    error_handler = ErrorHandler(logger=logger)

    # Test different error types
    print("\n=== Testing Validation Error ===")
    validation_error = ValidationError(
        "Invalid tick data received", details={"symbol": "EURUSD", "bid": -1.17500}
    )
    error_handler.handle_error(validation_error)
    print(f"Recovery suggestion: {error_handler.get_recovery_suggestion(validation_error)}")

    print("\n=== Testing Storage Error ===")
    storage_error = StorageError(
        "Failed to write data to file",
        details={"filepath": "/data/mt5/ticks.jsonl", "error": "Disk full"},
    )
    error_handler.handle_error(storage_error)
    print(f"Recovery suggestion: {error_handler.get_recovery_suggestion(storage_error)}")

    print("\n=== Testing Network Error ===")
    network_error = NetworkError(
        "Connection timeout from Expert Advisor",
        details={"host": "127.0.0.1", "port": 8000, "timeout": 30},
    )
    error_handler.handle_error(network_error)
    print(f"Recovery suggestion: {error_handler.get_recovery_suggestion(network_error)}")

    print("\n=== Testing Configuration Error ===")
    config_error = ConfigurationError(
        "Missing required configuration parameter",
        details={"parameter": "data_dir", "config_file": "collector_config.yaml"},
    )
    error_handler.handle_error(config_error)
    print(f"Recovery suggestion: {error_handler.get_recovery_suggestion(config_error)}")

    print("\n=== Testing Data Quality Error ===")
    data_quality_error = DataQualityError(
        "Large spread detected in tick data",
        details={"symbol": "EURUSD", "spread": 0.0015, "threshold": 0.001},
    )
    error_handler.handle_error(data_quality_error)
    print(f"Recovery suggestion: {error_handler.get_recovery_suggestion(data_quality_error)}")

    # Generate and print error report
    print("\n=== Error Report ===")
    report = error_handler.get_error_report()
    print(json.dumps(report, indent=2))

    # Save error report
    error_handler.save_error_report("logs/error_report.json")
    print("\nError report saved to: logs/error_report.json")
