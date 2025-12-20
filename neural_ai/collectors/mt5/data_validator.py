"""Data Validator for MT5 Collector.
==================================

Validates tick and OHLCV data for quality, consistency, and correctness.

Responsibilities:
- Validate data types and ranges
- Check for missing or invalid values
- Detect data anomalies and outliers
- Verify timestamp consistency
- Track data quality metrics
- Generate validation reports
- Integrate with Data Quality Framework

Author: Neural AI Next Team
Date: 2025-12-16
Version: 2.0.0
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

# DataQualityFramework import moved to methods to avoid circular import
from neural_ai.collectors.mt5.interfaces.data_validator_interface import (
    DataValidatorInterface,
    ValidationResult,
)


class DataValidator(DataValidatorInterface):
    """Validates financial market data (ticks and OHLCV) for quality and consistency.

    Validation rules:
    - Tick data: symbol, bid/ask prices, timestamp, spread
    - OHLCV data: symbol, OHLC prices, volume, timestamp, timeframe
    - Price validation: positive values, reasonable ranges
    - Time validation: chronological order, reasonable timestamps
    - Spread validation: reasonable bid-ask spread
    - Volume validation: non-negative values

    Extended with Data Quality Framework integration for comprehensive validation.
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        enable_quality_framework: bool = True,
    ):
        """Initialize the DataValidator.

        Args:
            logger: Optional logger instance for validation logs
            enable_quality_framework: Enable Data Quality Framework integration
        """
        self.logger = logger or logging.getLogger(__name__)

        # Validation configuration
        self.min_price = 0.00001  # Minimum valid price
        self.max_price = 1000000.0  # Maximum valid price
        self.max_spread_ratio = 0.01  # Maximum spread ratio (1%)
        self.max_timestamp_drift_seconds = 300  # 5 minutes

        # Data quality tracking
        self.validation_stats = {
            "total_ticks": 0,
            "valid_ticks": 0,
            "total_ohlcv": 0,
            "valid_ohlcv": 0,
            "total_errors": 0,
            "total_warnings": 0,
        }

        # Data Quality Framework integration (lazy import)
        self.enable_quality_framework = enable_quality_framework
        self._quality_framework = None
        self._quality_framework_initialized = False
        self._quality_framework_mock = None  # For testing purposes

    def validate_tick(self, tick_data: dict[str, Any]) -> ValidationResult:
        """Validate tick data.

        Args:
            tick_data: Dictionary containing tick data
                Required keys: symbol, bid, ask, time

        Returns:
            ValidationResult with validation status and issues
        """
        result = ValidationResult(is_valid=True)
        self.validation_stats["total_ticks"] += 1

        # Check required fields
        required_fields = ["symbol", "bid", "ask", "time"]
        for field_name in required_fields:
            if field_name not in tick_data:
                result.add_error(f"Missing required field: {field_name}")
                return result

        symbol = tick_data["symbol"]
        bid = tick_data["bid"]
        ask = tick_data["ask"]
        timestamp = tick_data["time"]

        # Validate symbol
        if not isinstance(symbol, str) or not symbol:
            result.add_error(f"Invalid symbol: {symbol}")

        # Validate bid price
        if not isinstance(bid, (int, float)):
            result.add_error(f"Bid price must be numeric: {bid}")
        elif bid < self.min_price or bid > self.max_price:
            result.add_error(f"Bid price out of valid range: {bid}")

        # Validate ask price
        if not isinstance(ask, (int, float)):
            result.add_error(f"Ask price must be numeric: {ask}")
        elif ask < self.min_price or ask > self.max_price:
            result.add_error(f"Ask price out of valid range: {ask}")

        # Validate bid-ask relationship
        if isinstance(bid, (int, float)) and isinstance(ask, (int, float)):
            if ask < bid:
                result.add_error(f"Ask price ({ask}) is less than bid price ({bid})")
            else:
                spread = ask - bid
                spread_ratio = spread / bid if bid > 0 else 0

                if spread_ratio > self.max_spread_ratio:
                    result.add_warning(
                        f"Large spread detected: {spread:.5f} ({spread_ratio:.4%}) for {symbol}"
                    )

        # Validate timestamp
        if not isinstance(timestamp, int):
            result.add_error(f"Timestamp must be integer: {timestamp}")
        else:
            # Check if timestamp is reasonable (not too far in past/future)
            current_time = int(datetime.now(UTC).timestamp())
            time_drift = abs(current_time - timestamp)

            if time_drift > self.max_timestamp_drift_seconds:
                result.add_warning(
                    f"Timestamp drift detected: {time_drift} seconds "
                    f"(timestamp: {timestamp}, current: {current_time})"
                )

        # Update statistics
        if result.is_valid:
            self.validation_stats["valid_ticks"] += 1
        else:
            self.validation_stats["total_errors"] += len(result.errors)

        if result.warnings:
            self.validation_stats["total_warnings"] += len(result.warnings)

        return result

    def validate_ohlcv(self, ohlcv_data: dict[str, Any]) -> ValidationResult:
        """Validate OHLCV data.

        Args:
            ohlcv_data: Dictionary containing OHLCV data
                Required keys: symbol, timeframe, time, open, high, low, close, volume

        Returns:
            ValidationResult with validation status and issues
        """
        result = ValidationResult(is_valid=True)
        self.validation_stats["total_ohlcv"] += 1

        # Check required fields
        required_fields = [
            "symbol",
            "timeframe",
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
        for field_name in required_fields:
            if field_name not in ohlcv_data:
                result.add_error(f"Missing required field: {field_name}")
                return result

        symbol = ohlcv_data["symbol"]
        timeframe = ohlcv_data["timeframe"]
        timestamp = ohlcv_data["time"]
        open_price = ohlcv_data["open"]
        high_price = ohlcv_data["high"]
        low_price = ohlcv_data["low"]
        close_price = ohlcv_data["close"]
        volume = ohlcv_data["volume"]

        # Validate symbol
        if not isinstance(symbol, str) or not symbol:
            result.add_error(f"Invalid symbol: {symbol}")

        # Validate timeframe
        if not isinstance(timeframe, int):
            result.add_error(f"Timeframe must be integer: {timeframe}")

        # Validate timestamp
        if not isinstance(timestamp, int):
            result.add_error(f"Timestamp must be integer: {timestamp}")
        else:
            # Check if timestamp is reasonable
            current_time = int(datetime.now(UTC).timestamp())
            time_drift = abs(current_time - timestamp)

            if time_drift > self.max_timestamp_drift_seconds:
                result.add_warning(
                    f"Timestamp drift detected: {time_drift} seconds "
                    f"(timestamp: {timestamp}, current: {current_time})"
                )

        # Validate OHLC prices
        prices = {
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
        }

        for price_name, price_value in prices.items():
            if not isinstance(price_value, (int, float)):
                result.add_error(f"{price_name.capitalize()} price must be numeric: {price_value}")
            elif price_value < self.min_price or price_value > self.max_price:
                result.add_error(
                    f"{price_name.capitalize()} price out of valid range: {price_value}"
                )

        # Validate OHLC relationship (only if all prices are valid)
        if all(isinstance(p, (int, float)) for p in prices.values()):
            if high_price < low_price:
                result.add_error(f"High price ({high_price}) is less than low price ({low_price})")

            if high_price < open_price:
                result.add_warning(
                    f"High price ({high_price}) is less than open price ({open_price})"
                )

            if high_price < close_price:
                result.add_warning(
                    f"High price ({high_price}) is less than close price ({close_price})"
                )

            if low_price > open_price:
                result.add_warning(
                    f"Low price ({low_price}) is greater than open price ({open_price})"
                )

            if low_price > close_price:
                result.add_warning(
                    f"Low price ({low_price}) is greater than close price ({close_price})"
                )

        # Validate volume
        if not isinstance(volume, (int, float)):
            result.add_error(f"Volume must be numeric: {volume}")
        elif volume < 0:
            result.add_error(f"Volume cannot be negative: {volume}")

        # Update statistics
        if result.is_valid:
            self.validation_stats["valid_ohlcv"] += 1
        else:
            self.validation_stats["total_errors"] += len(result.errors)

        if result.warnings:
            self.validation_stats["total_warnings"] += len(result.warnings)

        return result

    def get_validation_report(self) -> dict[str, Any]:
        """Generate a validation statistics report.

        Returns:
            Dictionary containing validation statistics
        """
        total_validated = (
            self.validation_stats["total_ticks"] + self.validation_stats["total_ohlcv"]
        )

        total_valid = self.validation_stats["valid_ticks"] + self.validation_stats["valid_ohlcv"]

        tick_quality = (
            self.validation_stats["valid_ticks"] / self.validation_stats["total_ticks"]
            if self.validation_stats["total_ticks"] > 0
            else 1.0
        )

        ohlcv_quality = (
            self.validation_stats["valid_ohlcv"] / self.validation_stats["total_ohlcv"]
            if self.validation_stats["total_ohlcv"] > 0
            else 1.0
        )

        overall_quality = total_valid / total_validated if total_validated > 0 else 1.0

        report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "total_validated": total_validated,
            "total_valid": total_valid,
            "total_errors": self.validation_stats["total_errors"],
            "total_warnings": self.validation_stats["total_warnings"],
            "tick_data": {
                "total": self.validation_stats["total_ticks"],
                "valid": self.validation_stats["valid_ticks"],
                "quality_score": tick_quality,
            },
            "ohlcv_data": {
                "total": self.validation_stats["total_ohlcv"],
                "valid": self.validation_stats["valid_ohlcv"],
                "quality_score": ohlcv_quality,
            },
            "overall_quality_score": overall_quality,
        }

        # Data Quality Framework report hozzáadása
        if self.quality_framework:
            quality_summary = self.quality_framework.get_quality_summary()
            report["quality_framework"] = quality_summary

        return report

    def save_validation_report(self, filepath: str) -> None:
        """Save validation report to a JSON file.

        Args:
            filepath: Path to save the report
        """
        report = self.get_validation_report()
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        if self.logger:
            self.logger.info(f"Validation report saved to: {filepath}")

    def reset_statistics(self) -> None:
        """Reset validation statistics."""
        self.validation_stats = {
            "total_ticks": 0,
            "valid_ticks": 0,
            "total_ohlcv": 0,
            "valid_ohlcv": 0,
            "total_errors": 0,
            "total_warnings": 0,
        }
        if self.logger:
            self.logger.info("Validation statistics reset")

    def validate_batch(
        self, data: list[dict[str, Any]], data_type: str = "ohlcv"
    ) -> dict[str, Any]:
        """Kötegelt adatok validálása Data Quality Frameworkkel.

        Args:
            data: Validálandó adatok listája
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            Validációs eredmények szótára
        """
        if not self._get_quality_framework():
            return {"status": "error", "message": "Data Quality Framework not enabled"}

        try:
            # Adatok konvertálása DataFrame-be
            df = pd.DataFrame(data)

            # Komprehenzív validálás
            result = self._quality_framework.validate_comprehensive(df, data_type)

            # Statisztikák frissítése
            if data_type == "ohlcv":
                self.validation_stats["total_ohlcv"] += len(data)
                if result["overall_status"] == "passed":
                    self.validation_stats["valid_ohlcv"] += len(data)
            else:  # tick
                self.validation_stats["total_ticks"] += len(data)
                if result["overall_status"] == "passed":
                    self.validation_stats["valid_ticks"] += len(data)

            return result

        except Exception as e:
            self.logger.error(f"Batch validation failed: {e}")
            return {"status": "error", "message": str(e)}

    def _get_quality_framework(self):
        """Lazy initialization of Data Quality Framework to avoid circular imports."""
        # Allow mocking for testing
        if self._quality_framework_mock is not None:
            return self._quality_framework_mock

        if not self.enable_quality_framework:
            return None

        if not self._quality_framework_initialized:
            try:
                from neural_ai.collectors.mt5.implementations.data_quality_framework import (
                    DataQualityFramework,
                )

                self._quality_framework = DataQualityFramework(validator=self, logger=self.logger)
                self.logger.info("Data Quality Framework integration enabled")
            except ImportError as e:
                self.logger.warning(f"Failed to import DataQualityFramework: {e}")
                self._quality_framework = None
            self._quality_framework_initialized = True

        return self._quality_framework

    @property
    def quality_framework(self):
        """Property accessor for quality framework with lazy initialization."""
        return self._get_quality_framework()

    @quality_framework.setter
    def quality_framework(self, value):
        """Setter for testing purposes - allows mocking."""
        self._quality_framework_mock = value

    def get_quality_metrics(self):
        """Minőségi metrikák lekérdezése.

        Returns:
            QualityMetrics objektum vagy None
        """
        if not self._get_quality_framework():
            return None

        # Utolsó minőségmetrikák lekérdezése
        if self._quality_framework.quality_history:
            last_entry = self._quality_framework.quality_history[-1]
            metrics_dict = last_entry["metrics"]

            # Lazy import
            from neural_ai.collectors.mt5.implementations.data_quality_framework import (
                QualityMetrics,
            )

            metrics = QualityMetrics()
            metrics.completeness = metrics_dict["completeness"]
            metrics.accuracy = metrics_dict["accuracy"]
            metrics.consistency = metrics_dict["consistency"]
            metrics.timeliness = metrics_dict["timeliness"]
            metrics.overall_score = metrics_dict["overall_score"]

            return metrics

        return None

    def generate_quality_report(self, output_path: str, format: str = "json") -> None:
        """Minőségjelentés generálása.

        Args:
            output_path: Kimeneti fájl elérési útja
            format: Kimeneti formátum (json vagy csv)
        """
        if not self._get_quality_framework():
            self.logger.warning("Data Quality Framework not enabled, cannot generate report")
            return

        self._quality_framework.generate_quality_report(output_path, format)

    def auto_correct_batch(
        self, data: list[dict[str, Any]], data_type: str = "ohlcv"
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Kötegelt adatok automatikus javítása.

        Args:
            data: Javítandó adatok listája
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            (javított adatok, javítások listája)
        """
        if not self._get_quality_framework():
            self.logger.warning("Data Quality Framework not enabled, cannot auto-correct")
            return data, []

        try:
            # Adatok konvertálása DataFrame-be
            df = pd.DataFrame(data)

            # Automatikus javítás
            corrected_df, corrections = self._quality_framework.auto_correct_data(df, data_type)

            # DataFrame visszakonvertálása listává
            corrected_data = corrected_df.to_dict("records")

            # Javítások szótárrá konvertálása
            corrections_list = [corr.to_dict() for corr in corrections]

            if corrections:
                self.logger.info(f"Auto-corrected {len(corrections)} issues in batch")

            return corrected_data, corrections_list

        except Exception as e:
            self.logger.error(f"Auto-correction failed: {e}")
            return data, []

    def track_quality(self, symbol: str, timeframe: str) -> None:
        """Minőség nyomon követése adott szimbólumra és időkeretre.

        Args:
            symbol: Pénznem szimbólum
            timeframe: Időkeret
        """
        if not self._get_quality_framework():
            return

        metrics = self.get_quality_metrics()
        if metrics:
            self._quality_framework.track_quality_trend(symbol, timeframe, metrics)


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Create validator
    validator = DataValidator(logger=logger)

    # Test valid tick data
    print("\n=== Testing Valid Tick Data ===")
    valid_tick = {
        "symbol": "EURUSD",
        "bid": 1.17500,
        "ask": 1.17505,
        "time": 1765841400,
    }
    result = validator.validate_tick(valid_tick)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")

    # Test invalid tick data (negative bid)
    print("\n=== Testing Invalid Tick Data (Negative Bid) ===")
    invalid_tick = {
        "symbol": "EURUSD",
        "bid": -1.17500,
        "ask": 1.17505,
        "time": 1765841400,
    }
    result = validator.validate_tick(invalid_tick)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Errors: {result.errors}")

    # Test invalid tick data (ask < bid)
    print("\n=== Testing Invalid Tick Data (Ask < Bid) ===")
    invalid_tick2 = {
        "symbol": "EURUSD",
        "bid": 1.17505,
        "ask": 1.17500,
        "time": 1765841400,
    }
    result = validator.validate_tick(invalid_tick2)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Errors: {result.errors}")

    # Test tick with large spread
    print("\n=== Testing Tick with Large Spread ===")
    large_spread_tick = {
        "symbol": "EURUSD",
        "bid": 1.17000,
        "ask": 1.18000,
        "time": 1765841400,
    }
    result = validator.validate_tick(large_spread_tick)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Warnings: {result.warnings}")

    # Test valid OHLCV data
    print("\n=== Testing Valid OHLCV Data ===")
    valid_ohlcv = {
        "symbol": "EURUSD",
        "timeframe": 16385,
        "time": 1765841400,
        "open": 1.17450,
        "high": 1.17550,
        "low": 1.17400,
        "close": 1.17500,
        "volume": 1000,
    }
    result = validator.validate_ohlcv(valid_ohlcv)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")

    # Test invalid OHLCV data (high < low)
    print("\n=== Testing Invalid OHLCV Data (High < Low) ===")
    invalid_ohlcv = {
        "symbol": "EURUSD",
        "timeframe": 16385,
        "time": 1765841400,
        "open": 1.17500,
        "high": 1.17400,
        "low": 1.17550,
        "close": 1.17450,
        "volume": 1000,
    }
    result = validator.validate_ohlcv(invalid_ohlcv)
    print(f"Valid: {result.is_valid}")
    print(f"Quality Score: {result.quality_score:.2f}")
    print(f"Errors: {result.errors}")

    # Generate and print validation report
    print("\n=== Validation Report ===")
    report = validator.get_validation_report()
    print(json.dumps(report, indent=2))

    # Save validation report
    validator.save_validation_report("logs/validation_report.json")
