"""Data Validator Interface.
========================

Defines the interface for data validation components in the MT5 Collector system.

This interface ensures consistent validation behavior across different
data validator implementations, supporting both tick and OHLCV data validation.

Author: Neural AI Next Team
Date: 2025-12-15
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Result of data validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    quality_score: float = 1.0

    def add_error(self, error: str) -> None:
        """Add a validation error."""
        self.errors.append(error)
        self.is_valid = False
        self.quality_score = max(0.0, self.quality_score - 0.2)

    def add_warning(self, warning: str) -> None:
        """Add a validation warning."""
        self.warnings.append(warning)
        self.quality_score = max(0.0, self.quality_score - 0.05)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "quality_score": self.quality_score,
        }


class DataValidatorInterface(ABC):
    """Interface for data validation components.

    Responsibilities:
    - Validate tick data for correctness and quality
    - Validate OHLCV data for correctness and quality
    - Track validation statistics
    - Generate validation reports
    - Handle validation errors and warnings
    """

    @abstractmethod
    def validate_tick(self, tick_data: dict[str, Any]) -> ValidationResult:
        """Validate tick data.

        Args:
            tick_data: Dictionary containing tick data with keys:
                - symbol (str): Instrument symbol
                - bid (float): Bid price
                - ask (float): Ask price
                - time (int): Unix timestamp

        Returns:
            ValidationResult: Result containing validation status, errors, warnings, and quality score
        """
        pass

    @abstractmethod
    def validate_ohlcv(self, ohlcv_data: dict[str, Any]) -> ValidationResult:
        """Validate OHLCV data.

        Args:
            ohlcv_data: Dictionary containing OHLCV data with keys:
                - symbol (str): Instrument symbol
                - timeframe (int): Timeframe identifier
                - time (int): Unix timestamp
                - open (float): Open price
                - high (float): High price
                - low (float): Low price
                - close (float): Close price
                - volume (int): Volume

        Returns:
            ValidationResult: Result containing validation status, errors, warnings, and quality score
        """
        pass

    @abstractmethod
    def get_validation_report(self) -> dict[str, Any]:
        """Generate a validation statistics report.

        Returns:
            Dictionary containing validation statistics including:
                - total_validated: Total number of data points validated
                - total_valid: Number of valid data points
                - total_errors: Number of validation errors
                - total_warnings: Number of validation warnings
                - quality_scores: Quality scores by data type
        """
        pass

    @abstractmethod
    def save_validation_report(self, filepath: str) -> None:
        """Save validation report to a file.

        Args:
            filepath: Path to save the report (typically JSON format)
        """
        pass

    @abstractmethod
    def reset_statistics(self) -> None:
        """Reset validation statistics to zero."""
        pass
