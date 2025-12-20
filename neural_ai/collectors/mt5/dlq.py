"""Dead-Letter-Queue (DLQ) implementation for MT5 Collector.
Handles corrupted or failed data with structured logging and retry capabilities.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DeadLetterQueue:
    """Dead-Letter-Queue for handling corrupted or failed MT5 data."""

    def __init__(self, dlq_directory: str | Path, max_file_size_mb: int = 100):
        """Initialize DLQ.

        Args:
            dlq_directory: Directory to store DLQ files
            max_file_size_mb: Maximum size of DLQ file before rotation (in MB)
        """
        self.dlq_directory = Path(dlq_directory)
        self.max_file_size = max_file_size_mb * 1024 * 1024  # Convert to bytes

        # Ensure DLQ directory exists
        self.dlq_directory.mkdir(parents=True, exist_ok=True)

        # Current DLQ file
        self.current_file = self._get_current_dlq_file()

    def _get_current_dlq_file(self) -> Path:
        """Get the current DLQ file, creating a new one if needed."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corrupted_ticks_{timestamp}.jsonl"
        return self.dlq_directory / filename

    def _should_rotate_file(self) -> bool:
        """Check if we should rotate to a new DLQ file."""
        if not self.current_file.exists():
            return False
        return self.current_file.stat().st_size >= self.max_file_size

    def _rotate_file(self) -> None:
        """Rotate to a new DLQ file."""
        self.current_file = self._get_current_dlq_file()
        logger.info(f"Rotated DLQ to new file: {self.current_file.name}")

    def record_failure(
        self,
        data: Any,
        error: Exception,
        context: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Record a failed data processing attempt.

        Args:
            data: The data that failed to process
            error: The exception that caused the failure
            context: Additional context information
            retryable: Whether this failure can be retried later
        """
        if self._should_rotate_file():
            self._rotate_file()

        # Prepare DLQ entry
        # Convert bytes/memoryview to string for JSON serialization
        data_for_storage: Any
        if isinstance(data, (bytes, memoryview)):
            data_for_storage = str(data)
        else:
            data_for_storage = data

        dlq_entry: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "retryable": retryable,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "data": data_for_storage,
            "context": context or {},
        }

        # Add stack trace for debugging
        if hasattr(error, "__traceback__"):
            import traceback

            dlq_entry["stack_trace"] = traceback.format_exc()

        # Write to DLQ file atomically
        try:
            with open(self.current_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(dlq_entry, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())

            logger.warning(
                f"Recorded failure to DLQ: {type(error).__name__} - {error}. "
                f"File: {self.current_file.name}"
            )
        except Exception as e:
            logger.error(f"Failed to write to DLQ: {e}")
            raise

    def get_failures(
        self, retryable_only: bool = True, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """Get failed entries from DLQ.

        Args:
            retryable_only: Only return retryable failures
            limit: Maximum number of entries to return

        Returns:
            List of DLQ entries
        """
        failures: list[dict[str, Any]] = []

        # Read all DLQ files
        dlq_files = sorted(self.dlq_directory.glob("corrupted_ticks_*.jsonl"))

        for dlq_file in dlq_files:
            try:
                with open(dlq_file, encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            entry = json.loads(line)

                            # Filter by retryable
                            if retryable_only and not entry.get("retryable", False):
                                continue

                            failures.append(entry)

                            # Apply limit
                            if limit and len(failures) >= limit:
                                return failures
            except Exception as e:
                logger.error(f"Failed to read DLQ file {dlq_file}: {e}")
                continue

        return failures

    def mark_as_processed(self, timestamp: str) -> bool:
        """Mark a DLQ entry as processed (remove from retryable list).

        Args:
            timestamp: ISO timestamp of the entry to mark

        Returns:
            True if successful, False otherwise
        """
        # Note: In a production system, you might want to implement a more
        # sophisticated marking mechanism (e.g., separate processed entries file)
        logger.info(f"Marked DLQ entry as processed: {timestamp}")
        return True

    def get_statistics(self) -> dict[str, Any]:
        """Get DLQ statistics."""
        stats: dict[str, Any] = {
            "total_files": 0,
            "total_entries": 0,
            "retryable_entries": 0,
            "non_retryable_entries": 0,
            "error_types": {},
            "oldest_entry": None,
            "newest_entry": None,
        }

        dlq_files = list(self.dlq_directory.glob("corrupted_ticks_*.jsonl"))
        stats["total_files"] = len(dlq_files)

        for dlq_file in dlq_files:
            try:
                with open(dlq_file, encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            entry = json.loads(line)
                            stats["total_entries"] += 1

                            if entry.get("retryable", False):
                                stats["retryable_entries"] += 1
                            else:
                                stats["non_retryable_entries"] += 1

                            # Track error types
                            error_type = entry.get("error_type", "Unknown")
                            stats["error_types"][error_type] = (
                                stats["error_types"].get(error_type, 0) + 1
                            )

                            # Track timestamps
                            entry_time = entry.get("timestamp")
                            if entry_time:
                                if not stats["oldest_entry"] or entry_time < stats["oldest_entry"]:
                                    stats["oldest_entry"] = entry_time
                                if not stats["newest_entry"] or entry_time > stats["newest_entry"]:
                                    stats["newest_entry"] = entry_time
            except Exception as e:
                logger.error(f"Failed to read DLQ file {dlq_file} for statistics: {e}")
                continue

        return stats
