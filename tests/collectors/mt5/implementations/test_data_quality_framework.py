"""Unit tests for Data Quality Framework component.

Tests cover:
- 3-level validation system (basic, logical, statistical)
- Outlier detection methods (IQR, Z-Score, Moving Average)
- Quality metrics calculation
- Auto-correction functionality
- Quality reporting
- Quality tracking and trend analysis

Author: Neural AI Next Team
Date: 2025-12-17
"""

import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

from neural_ai.collectors.mt5.implementations.data_quality_framework import (
    DataCorrection,
    DataQualityFramework,
    IssueSeverity,
    OutlierDetector,
    QualityIssue,
    QualityMetrics,
)


class TestOutlierDetector(unittest.TestCase):
    """Test cases for OutlierDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.detector = OutlierDetector(logger=self.logger)

        # Test data with outliers
        self.data = pd.Series([1.0, 1.1, 1.2, 1.1, 1.3, 5.0, 1.2, 1.1, 1.15, 1.25])

    def test_detect_iqr(self):
        """Test IQR outlier detection."""
        outliers, stats = self.detector.detect_iqr(self.data, threshold=1.5)

        self.assertIsInstance(outliers, pd.Series)
        self.assertIsInstance(stats, dict)
        self.assertIn("method", stats)
        self.assertIn("outlier_count", stats)
        self.assertEqual(stats["method"], "IQR")

        # Check if outliers were detected
        self.assertGreater(stats["outlier_count"], 0)

    def test_detect_iqr_no_outliers(self):
        """Test IQR detection with no outliers."""
        clean_data = pd.Series([1.0, 1.1, 1.2, 1.1, 1.3, 1.2, 1.1, 1.15, 1.25])

        outliers, stats = self.detector.detect_iqr(clean_data, threshold=1.5)

        self.assertEqual(stats["outlier_count"], 0)

    def test_detect_z_score(self):
        """Test Z-Score outlier detection."""
        outliers, stats = self.detector.detect_z_score(self.data, threshold=3.0)

        self.assertIsInstance(outliers, pd.Series)
        self.assertIsInstance(stats, dict)
        self.assertIn("method", stats)
        self.assertIn("outlier_count", stats)
        self.assertEqual(stats["method"], "Z-Score")

    def test_detect_z_score_zero_std(self):
        """Test Z-Score detection with zero standard deviation."""
        constant_data = pd.Series([1.0, 1.0, 1.0, 1.0, 1.0])

        outliers, stats = self.detector.detect_z_score(constant_data, threshold=3.0)

        # Should return empty stats dict
        self.assertEqual(stats, {})

    def test_detect_moving_average(self):
        """Test Moving Average outlier detection."""
        outliers, stats = self.detector.detect_moving_average(self.data, window=3, threshold=2.0)

        self.assertIsInstance(outliers, pd.Series)
        self.assertIsInstance(stats, dict)
        self.assertIn("method", stats)
        self.assertIn("outlier_count", stats)
        self.assertEqual(stats["method"], "Moving Average")

    def test_detect_all_methods(self):
        """Test all detection methods."""
        results = self.detector.detect_all_methods(self.data)

        self.assertIsInstance(results, dict)
        self.assertIn("iqr", results)
        self.assertIn("z_score", results)
        self.assertIn("moving_average", results)

        # Check each method
        for _method, (outliers, stats) in results.items():
            self.assertIsInstance(outliers, pd.Series)
            self.assertIsInstance(stats, dict)


class TestQualityMetrics(unittest.TestCase):
    """Test cases for QualityMetrics class."""

    def setUp(self):
        """Set up test fixtures."""
        self.metrics = QualityMetrics()

    def test_initialization(self):
        """Test QualityMetrics initialization."""
        self.assertEqual(self.metrics.completeness, 0.0)
        self.assertEqual(self.metrics.accuracy, 0.0)
        self.assertEqual(self.metrics.consistency, 0.0)
        self.assertEqual(self.metrics.timeliness, 0.0)
        self.assertEqual(self.metrics.overall_score, 0.0)

    def test_calculate_overall(self):
        """Test overall score calculation."""
        self.metrics.completeness = 0.9
        self.metrics.accuracy = 0.8
        self.metrics.consistency = 0.7
        self.metrics.timeliness = 0.6

        overall = self.metrics.calculate_overall()

        # Expected: 0.9*0.3 + 0.8*0.3 + 0.7*0.2 + 0.6*0.2 = 0.77
        expected = 0.9 * 0.3 + 0.8 * 0.3 + 0.7 * 0.2 + 0.6 * 0.2
        self.assertEqual(overall, expected)
        self.assertEqual(self.metrics.overall_score, expected)

    def test_to_dict(self):
        """Test converting QualityMetrics to dictionary."""
        self.metrics.completeness = 0.9
        self.metrics.accuracy = 0.8
        self.metrics.consistency = 0.7
        self.metrics.timeliness = 0.6
        self.metrics.calculate_overall()

        metrics_dict = self.metrics.to_dict()

        self.assertIn("completeness", metrics_dict)
        self.assertIn("accuracy", metrics_dict)
        self.assertIn("consistency", metrics_dict)
        self.assertIn("timeliness", metrics_dict)
        self.assertIn("overall_score", metrics_dict)


class TestDataQualityFramework(unittest.TestCase):
    """Test cases for DataQualityFramework class."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.validator = Mock()
        self.framework = DataQualityFramework(validator=self.validator, logger=self.logger)

        # Test OHLCV data
        dates = pd.date_range(start="2025-01-01", end="2025-01-10", freq="H")
        self.ohlcv_data = pd.DataFrame(
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

        # Test tick data
        self.tick_data = pd.DataFrame(
            {
                "symbol": ["EURUSD"] * 100,
                "bid": np.random.normal(1.10, 0.001, 100),
                "ask": np.random.normal(1.1005, 0.001, 100),
                "time": [int(datetime.now().timestamp()) + i for i in range(100)],
            }
        )

    def test_initialization(self):
        """Test DataQualityFramework initialization."""
        self.assertEqual(self.framework.validator, self.validator)
        self.assertEqual(self.framework.logger, self.logger)
        self.assertIsNotNone(self.framework.outlier_detector)
        self.assertIsNotNone(self.framework.quality_history)
        self.assertIsNotNone(self.framework.corrections)
        self.assertIsNotNone(self.framework.issues)

    def test_validate_level_1_basic_ohlcv_valid(self):
        """Test Level 1 validation with valid OHLCV data."""
        is_valid, issues = self.framework.validate_level_1_basic(self.ohlcv_data, data_type="ohlcv")

        self.assertTrue(is_valid)
        self.assertIsInstance(issues, list)

    def test_validate_level_1_basic_missing_fields(self):
        """Test Level 1 validation with missing fields."""
        invalid_data = self.ohlcv_data.copy()
        invalid_data.drop(columns=["open", "high"], inplace=True)

        is_valid, issues = self.framework.validate_level_1_basic(invalid_data, data_type="ohlcv")

        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_validate_level_1_basic_invalid_types(self):
        """Test Level 1 validation with invalid data types."""
        invalid_data = self.ohlcv_data.copy()
        invalid_data["open"] = "invalid"

        is_valid, issues = self.framework.validate_level_1_basic(invalid_data, data_type="ohlcv")

        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_validate_level_1_basic_missing_values(self):
        """Test Level 1 validation with missing values."""
        invalid_data = self.ohlcv_data.copy()
        invalid_data.loc[0, "open"] = None

        is_valid, issues = self.framework.validate_level_1_basic(invalid_data, data_type="ohlcv")

        self.assertTrue(is_valid)  # Should pass but with warnings
        self.assertGreater(len(issues), 0)

    def test_validate_level_2_logical_ohlcv_valid(self):
        """Test Level 2 validation with valid OHLCV data."""
        is_valid, issues = self.framework.validate_level_2_logical(
            self.ohlcv_data, data_type="ohlcv"
        )

        self.assertTrue(is_valid)
        self.assertIsInstance(issues, list)

    def test_validate_level_2_logical_invalid_high_low(self):
        """Test Level 2 validation with high < low."""
        invalid_data = self.ohlcv_data.copy()
        invalid_data.loc[0, "high"] = 1.08
        invalid_data.loc[0, "low"] = 1.09

        is_valid, issues = self.framework.validate_level_2_logical(invalid_data, data_type="ohlcv")

        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_validate_level_2_logical_negative_volume(self):
        """Test Level 2 validation with negative volume."""
        invalid_data = self.ohlcv_data.copy()
        invalid_data.loc[0, "volume"] = -100

        is_valid, issues = self.framework.validate_level_2_logical(invalid_data, data_type="ohlcv")

        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_validate_level_2_logical_tick_invalid_bid_ask(self):
        """Test Level 2 validation with ask < bid."""
        invalid_data = self.tick_data.copy()
        invalid_data.loc[0, "ask"] = 1.09
        invalid_data.loc[0, "bid"] = 1.10

        is_valid, issues = self.framework.validate_level_2_logical(invalid_data, data_type="tick")

        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)

    def test_validate_level_3_statistical_ohlcv(self):
        """Test Level 3 validation with OHLCV data."""
        is_valid, issues = self.framework.validate_level_3_statistical(
            self.ohlcv_data, data_type="ohlcv"
        )

        self.assertTrue(is_valid)
        self.assertIsInstance(issues, list)

    def test_validate_level_3_statistical_with_outliers(self):
        """Test Level 3 validation with outliers."""
        invalid_data = self.ohlcv_data.copy()
        # Add outliers
        invalid_data.loc[0, "high"] = 2.0
        invalid_data.loc[1, "low"] = 0.5

        is_valid, issues = self.framework.validate_level_3_statistical(
            invalid_data, data_type="ohlcv"
        )

        self.assertTrue(is_valid)  # Outliers are warnings, not errors
        self.assertGreater(len(issues), 0)

    def test_validate_comprehensive(self):
        """Test comprehensive validation."""
        result = self.framework.validate_comprehensive(self.ohlcv_data, data_type="ohlcv")

        self.assertIn("timestamp", result)
        self.assertIn("data_type", result)
        self.assertIn("total_records", result)
        self.assertIn("validation_levels", result)
        self.assertIn("overall_status", result)
        self.assertIn("issues", result)
        self.assertIn("metrics", result)

    def test_auto_correct_data_ohlcv(self):
        """Test auto-correction with OHLCV data."""
        # Create data with errors
        invalid_data = self.ohlcv_data.copy()
        invalid_data.loc[0, "high"] = 1.08
        invalid_data.loc[0, "low"] = 1.09

        corrected_data, corrections = self.framework.auto_correct_data(
            invalid_data, data_type="ohlcv"
        )

        self.assertIsInstance(corrected_data, pd.DataFrame)
        self.assertIsInstance(corrections, list)

    def test_auto_correct_data_disabled(self):
        """Test auto-correction when disabled."""
        self.framework.config["auto_correction"]["enabled"] = False

        corrected_data, corrections = self.framework.auto_correct_data(
            self.ohlcv_data, data_type="ohlcv"
        )

        self.assertEqual(len(corrections), 0)
        self.assertEqual(len(corrected_data), len(self.ohlcv_data))

    def test_generate_quality_report_json(self):
        """Test generating quality report in JSON format."""
        with patch("builtins.open", create=True) as mock_open:
            self.framework.generate_quality_report("logs/test_report.json", format="json")

            mock_open.assert_called_once()

    def test_generate_quality_report_csv(self):
        """Test generating quality report in CSV format."""
        # Add some issues and corrections
        self.framework.issues.append(
            QualityIssue(
                severity=IssueSeverity.WARNING,
                category="test",
                description="Test issue",
            )
        )

        self.framework.corrections.append(
            DataCorrection(
                original_value=1.0,
                corrected_value=1.1,
                correction_method="test",
                reason="Test correction",
            )
        )

        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            self.framework.generate_quality_report("logs/test_report.csv", format="csv")

            # Should be called twice (issues and corrections)
            self.assertEqual(mock_to_csv.call_count, 2)

    def test_track_quality_trend(self):
        """Test tracking quality trend."""
        metrics = QualityMetrics()
        metrics.completeness = 0.9
        metrics.accuracy = 0.8
        metrics.consistency = 0.7
        metrics.timeliness = 0.6
        metrics.calculate_overall()

        self.framework.track_quality_trend("EURUSD", "H1", metrics)

        self.assertEqual(len(self.framework.quality_history), 1)

        # Check the tracked entry
        entry = self.framework.quality_history[0]
        self.assertEqual(entry["symbol"], "EURUSD")
        self.assertEqual(entry["timeframe"], "H1")
        self.assertIn("metrics", entry)

    def test_get_quality_summary(self):
        """Test getting quality summary."""
        # Add some history
        for i in range(10):
            metrics = QualityMetrics()
            metrics.completeness = 0.9 - i * 0.01
            metrics.accuracy = 0.8 - i * 0.01
            metrics.consistency = 0.7 - i * 0.01
            metrics.timeliness = 0.6 - i * 0.01
            metrics.calculate_overall()

            self.framework.track_quality_trend("EURUSD", "H1", metrics)

        summary = self.framework.get_quality_summary()

        self.assertIn("period", summary)
        self.assertIn("average_score", summary)
        self.assertIn("min_score", summary)
        self.assertIn("max_score", summary)
        self.assertIn("trend", summary)
        self.assertIn("total_issues", summary)
        self.assertIn("total_corrections", summary)

    def test_get_quality_summary_no_data(self):
        """Test getting quality summary with no data."""
        summary = self.framework.get_quality_summary()

        self.assertEqual(summary["status"], "no_data")
        self.assertIn("Nincs elérhető minőségadatok", summary["message"])


class TestQualityIssue(unittest.TestCase):
    """Test cases for QualityIssue class."""

    def test_quality_issue_creation(self):
        """Test QualityIssue creation."""
        issue = QualityIssue(
            severity=IssueSeverity.WARNING,
            category="test_category",
            description="Test issue",
            count=5,
            details={"key": "value"},
        )

        self.assertEqual(issue.severity, IssueSeverity.WARNING)
        self.assertEqual(issue.category, "test_category")
        self.assertEqual(issue.description, "Test issue")
        self.assertEqual(issue.count, 5)
        self.assertEqual(issue.details["key"], "value")

    def test_quality_issue_to_dict(self):
        """Test converting QualityIssue to dictionary."""
        issue = QualityIssue(severity=IssueSeverity.ERROR, category="test", description="Test")

        issue_dict = issue.to_dict()

        self.assertIn("severity", issue_dict)
        self.assertIn("category", issue_dict)
        self.assertIn("description", issue_dict)
        self.assertEqual(issue_dict["severity"], "ERROR")


class TestDataCorrection(unittest.TestCase):
    """Test cases for DataCorrection class."""

    def test_data_correction_creation(self):
        """Test DataCorrection creation."""
        correction = DataCorrection(
            original_value=1.0,
            corrected_value=1.1,
            correction_method="interpolation",
            reason="Missing value",
            confidence=0.9,
        )

        self.assertEqual(correction.original_value, 1.0)
        self.assertEqual(correction.corrected_value, 1.1)
        self.assertEqual(correction.correction_method, "interpolation")
        self.assertEqual(correction.reason, "Missing value")
        self.assertEqual(correction.confidence, 0.9)

    def test_data_correction_to_dict(self):
        """Test converting DataCorrection to dictionary."""
        correction = DataCorrection(
            original_value=1.0,
            corrected_value=1.1,
            correction_method="test",
            reason="Test",
        )

        correction_dict = correction.to_dict()

        self.assertIn("original_value", correction_dict)
        self.assertIn("corrected_value", correction_dict)
        self.assertIn("correction_method", correction_dict)
        self.assertIn("reason", correction_dict)


if __name__ == "__main__":
    unittest.main()
