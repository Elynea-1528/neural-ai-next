"""Unit tests for Data Validator component.

Tests cover:
- Tick data validation (valid, invalid, edge cases)
- OHLCV data validation (valid, invalid, edge cases)
- Validation statistics and reporting
- Data Quality Framework integration
- Batch validation
- Auto-correction functionality

Author: Neural AI Next Team
Date: 2025-12-17
"""

import unittest
from datetime import UTC, datetime
from unittest.mock import Mock, patch

import pandas as pd

from neural_ai.collectors.mt5.data_validator import DataValidator
from neural_ai.collectors.mt5.interfaces.data_validator_interface import (
    ValidationResult,
)


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = DataValidator(logger=Mock(), enable_quality_framework=False)

        # Valid tick data
        self.valid_tick = {
            "symbol": "EURUSD",
            "bid": 1.17500,
            "ask": 1.17505,
            "time": int(datetime.now(UTC).timestamp()),
        }

        # Valid OHLCV data
        self.valid_ohlcv = {
            "symbol": "EURUSD",
            "timeframe": 16385,
            "time": int(datetime.now(UTC).timestamp()),
            "open": 1.17450,
            "high": 1.17550,
            "low": 1.17400,
            "close": 1.17500,
            "volume": 1000,
        }

    def test_validate_tick_valid_data(self):
        """Test validation of valid tick data."""
        result = self.validator.validate_tick(self.valid_tick)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(result.quality_score, 1.0)

    def test_validate_tick_missing_required_field(self):
        """Test validation of tick data with missing required field."""
        invalid_tick = self.valid_tick.copy()
        del invalid_tick["symbol"]

        result = self.validator.validate_tick(invalid_tick)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Missing required field", result.errors[0])

    def test_validate_tick_invalid_bid_price(self):
        """Test validation of tick data with invalid bid price."""
        invalid_tick = self.valid_tick.copy()
        invalid_tick["bid"] = -1.17500

        result = self.validator.validate_tick(invalid_tick)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Bid price", result.errors[0])

    def test_validate_tick_ask_less_than_bid(self):
        """Test validation of tick data where ask < bid."""
        invalid_tick = self.valid_tick.copy()
        invalid_tick["ask"] = 1.17495
        invalid_tick["bid"] = 1.17500

        result = self.validator.validate_tick(invalid_tick)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Ask price", result.errors[0])

    def test_validate_tick_large_spread_warning(self):
        """Test validation of tick data with large spread."""
        invalid_tick = self.valid_tick.copy()
        invalid_tick["bid"] = 1.17000
        invalid_tick["ask"] = 1.18000

        result = self.validator.validate_tick(invalid_tick)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)
        self.assertIn("Large spread", result.warnings[0])

    def test_validate_tick_timestamp_drift_warning(self):
        """Test validation of tick data with timestamp drift."""
        invalid_tick = self.valid_tick.copy()
        invalid_tick["time"] = int(datetime.now(UTC).timestamp()) - 600

        result = self.validator.validate_tick(invalid_tick)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)
        self.assertIn("Timestamp drift", result.warnings[0])

    def test_validate_ohlcv_valid_data(self):
        """Test validation of valid OHLCV data."""
        result = self.validator.validate_ohlcv(self.valid_ohlcv)

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(result.quality_score, 1.0)

    def test_validate_ohlcv_missing_required_field(self):
        """Test validation of OHLCV data with missing required field."""
        invalid_ohlcv = self.valid_ohlcv.copy()
        del invalid_ohlcv["open"]

        result = self.validator.validate_ohlcv(invalid_ohlcv)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Missing required field", result.errors[0])

    def test_validate_ohlcv_high_less_than_low(self):
        """Test validation of OHLCV data where high < low."""
        invalid_ohlcv = self.valid_ohlcv.copy()
        invalid_ohlcv["high"] = 1.17300
        invalid_ohlcv["low"] = 1.17500

        result = self.validator.validate_ohlcv(invalid_ohlcv)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("High price", result.errors[0])

    def test_validate_ohlcv_negative_volume(self):
        """Test validation of OHLCV data with negative volume."""
        invalid_ohlcv = self.valid_ohlcv.copy()
        invalid_ohlcv["volume"] = -100

        result = self.validator.validate_ohlcv(invalid_ohlcv)

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("Volume", result.errors[0])

    def test_validate_ohlcv_suspicious_high_warning(self):
        """Test validation of OHLCV data with suspicious high price."""
        invalid_ohlcv = self.valid_ohlcv.copy()
        invalid_ohlcv["high"] = 1.17400  # Lower than open
        invalid_ohlcv["open"] = 1.17500

        result = self.validator.validate_ohlcv(invalid_ohlcv)

        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.warnings), 0)
        self.assertIn("High price", result.warnings[0])

    def test_get_validation_report(self):
        """Test generation of validation report."""
        # Validate some data first
        self.validator.validate_tick(self.valid_tick)
        self.validator.validate_ohlcv(self.valid_ohlcv)

        report = self.validator.get_validation_report()

        self.assertIn("timestamp", report)
        self.assertIn("total_validated", report)
        self.assertIn("total_valid", report)
        self.assertIn("tick_data", report)
        self.assertIn("ohlcv_data", report)
        self.assertIn("overall_quality_score", report)

        self.assertEqual(report["total_validated"], 2)
        self.assertEqual(report["total_valid"], 2)

    def test_reset_statistics(self):
        """Test resetting validation statistics."""
        # Validate some data first
        self.validator.validate_tick(self.valid_tick)

        # Reset statistics
        self.validator.reset_statistics()

        # Check if statistics are reset
        self.assertEqual(self.validator.validation_stats["total_ticks"], 0)
        self.assertEqual(self.validator.validation_stats["valid_ticks"], 0)

    @patch("neural_ai.collectors.mt5.data_validator.pd.DataFrame")
    def test_validate_batch_without_quality_framework(self, mock_dataframe):
        """Test batch validation without quality framework enabled."""
        data = [self.valid_ohlcv, self.valid_ohlcv]

        result = self.validator.validate_batch(data, data_type="ohlcv")

        self.assertEqual(result["status"], "error")
        self.assertIn("Data Quality Framework not enabled", result["message"])

    @patch("neural_ai.collectors.mt5.data_validator.pd.DataFrame")
    def test_validate_batch_with_quality_framework(self, mock_dataframe):
        """Test batch validation with quality framework enabled."""
        # Enable quality framework
        self.validator.enable_quality_framework = True
        self.validator.quality_framework = Mock()
        self.validator.quality_framework.validate_comprehensive.return_value = {
            "overall_status": "passed",
            "metrics": {"overall_score": 0.95},
        }

        data = [self.valid_ohlcv, self.valid_ohlcv]

        result = self.validator.validate_batch(data, data_type="ohlcv")

        self.assertEqual(result["overall_status"], "passed")

    @patch("neural_ai.collectors.mt5.data_validator.pd.DataFrame")
    def test_auto_correct_batch_without_quality_framework(self, mock_dataframe):
        """Test auto-correction without quality framework enabled."""
        data = [self.valid_ohlcv, self.valid_ohlcv]

        corrected_data, corrections = self.validator.auto_correct_batch(data, data_type="ohlcv")

        self.assertEqual(len(corrections), 0)
        self.assertEqual(len(corrected_data), len(data))

    @patch("neural_ai.collectors.mt5.data_validator.pd.DataFrame")
    def test_auto_correct_batch_with_quality_framework(self, mock_dataframe):
        """Test auto-correction with quality framework enabled."""
        # Enable quality framework
        self.validator.enable_quality_framework = True
        self.validator.quality_framework = Mock()
        self.validator.quality_framework.auto_correct_data.return_value = (
            pd.DataFrame([self.valid_ohlcv, self.valid_ohlcv]),
            [{"correction": "test"}],
        )

        data = [self.valid_ohlcv, self.valid_ohlcv]

        corrected_data, corrections = self.validator.auto_correct_batch(data, data_type="ohlcv")

        self.assertEqual(len(corrections), 1)

    def test_get_quality_metrics_without_framework(self):
        """Test getting quality metrics without framework enabled."""
        metrics = self.validator.get_quality_metrics()

        self.assertIsNone(metrics)

    def test_get_quality_metrics_with_framework(self):
        """Test getting quality metrics with framework enabled."""
        # Enable quality framework
        self.validator.enable_quality_framework = True
        self.validator.quality_framework = Mock()
        self.validator.quality_framework.quality_history = [
            {
                "metrics": {
                    "completeness": 0.95,
                    "accuracy": 0.90,
                    "consistency": 0.85,
                    "timeliness": 0.80,
                    "overall_score": 0.88,
                }
            }
        ]

        metrics = self.validator.get_quality_metrics()

        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.completeness, 0.95)
        self.assertEqual(metrics.overall_score, 0.88)

    @patch("neural_ai.collectors.mt5.data_validator.json.dump")
    def test_save_validation_report(self, mock_json_dump):
        """Test saving validation report to file."""
        filepath = "logs/test_validation_report.json"

        self.validator.save_validation_report(filepath)

        mock_json_dump.assert_called_once()

    def test_validation_result_add_error(self):
        """Test adding error to validation result."""
        result = ValidationResult(is_valid=True)

        result.add_error("Test error")

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Test error", result.errors)
        self.assertLess(result.quality_score, 1.0)

    def test_validation_result_add_warning(self):
        """Test adding warning to validation result."""
        result = ValidationResult(is_valid=True)

        result.add_warning("Test warning")

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.warnings), 1)
        self.assertIn("Test warning", result.warnings)
        self.assertLess(result.quality_score, 1.0)

    def test_validation_result_to_dict(self):
        """Test converting validation result to dictionary."""
        result = ValidationResult(is_valid=True)
        result.add_error("Error 1")
        result.add_warning("Warning 1")

        result_dict = result.to_dict()

        self.assertIn("is_valid", result_dict)
        self.assertIn("errors", result_dict)
        self.assertIn("warnings", result_dict)
        self.assertIn("quality_score", result_dict)
        self.assertEqual(result_dict["is_valid"], False)


if __name__ == "__main__":
    unittest.main()
