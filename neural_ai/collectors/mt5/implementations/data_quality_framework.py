"""Data Quality Framework for MT5 Collector.
========================================

Komprehenzív adatminőség-ellenőrzési és validációs keretrendszer
a historikus adatokhoz.

Funkcionalitások:
- 3-szintű validációs rendszer (alap, logikai, statisztikai)
- Kiugró értékek detektálása (IQR, Z-score, moving average)
- Adatminőség-jelentés generálás (CSV/JSON formátumban)
- Automatikus javítási lehetőségek
- Minőségkövetés és trendanalízis

Author: Neural AI Next Team
Date: 2025-12-16
Version: 1.0.0
"""

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from neural_ai.collectors.mt5.data_validator import DataValidator


class ValidationLevel(Enum):
    """Validációs szintek enumja."""

    LEVEL_1_BASIC = "level_1_basic"
    LEVEL_2_LOGICAL = "level_2_logical"
    LEVEL_3_STATISTICAL = "level_3_statistical"


class IssueSeverity(Enum):
    """Probléma súlyossági szintek enumja."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class OutlierDetectionMethod(Enum):
    """Kiugró érték detektálási módszerek enumja."""

    IQR = "iqr"
    Z_SCORE = "z_score"
    MOVING_AVERAGE = "moving_average"


@dataclass
class QualityIssue:
    """Adatminőségi probléma reprezentációja."""

    severity: IssueSeverity
    category: str
    description: str
    count: int = 1
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Szótárrá konvertálás."""
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


@dataclass
class DataCorrection:
    """Adatjavítás reprezentációja."""

    original_value: float
    corrected_value: float
    correction_method: str
    reason: str
    confidence: float = 1.0
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Szótárrá konvertálás."""
        return asdict(self)


@dataclass
class QualityMetrics:
    """Adatminőségi metrikák reprezentációja."""

    completeness: float = 0.0
    accuracy: float = 0.0
    consistency: float = 0.0
    timeliness: float = 0.0
    overall_score: float = 0.0

    def calculate_overall(self) -> float:
        """Összesített minőségi pontszám kiszámítása."""
        self.overall_score = (
            self.completeness * 0.3
            + self.accuracy * 0.3
            + self.consistency * 0.2
            + self.timeliness * 0.2
        )
        return self.overall_score

    def to_dict(self) -> dict[str, Any]:
        """Szótárrá konvertálás."""
        return asdict(self)


class OutlierDetector:
    """Kiugró értékek detektálására szolgáló osztály.

    Támogatott módszerek:
    - IQR (Interquartile Range)
    - Z-Score
    - Moving Average
    """

    def __init__(self, logger: logging.Logger | None = None):
        """Inicializálás.

        Args:
            logger: Logger példány
        """
        self.logger = logger or logging.getLogger(__name__)

    def detect_iqr(
        self, data: pd.Series, threshold: float = 1.5
    ) -> tuple[pd.Series, dict[str, Any]]:
        """IQR módszerrel történő kiugró értékek detektálása.

        Args:
            data: Adatsor
            threshold: Küszöbérték (alapértelmezett: 1.5)

        Returns:
            (kiugró értékek maszkja, statisztikák)
        """
        try:
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            outliers = (data < lower_bound) | (data > upper_bound)

            stats = {
                "method": "IQR",
                "threshold": threshold,
                "Q1": float(Q1),
                "Q3": float(Q3),
                "IQR": float(IQR),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outlier_count": int(outliers.sum()),
                "outlier_percentage": float((outliers.sum() / len(data)) * 100),
            }

            return outliers, stats

        except Exception as e:
            self.logger.error(f"IQR detection failed: {e}")
            return pd.Series([False] * len(data)), {}

    def detect_z_score(
        self, data: pd.Series, threshold: float = 3.0
    ) -> tuple[pd.Series, dict[str, Any]]:
        """Z-Score módszerrel történő kiugró értékek detektálása.

        Args:
            data: Adatsor
            threshold: Z-Score küszöbérték (alapértelmezett: 3.0)

        Returns:
            (kiugró értékek maszkja, statisztikák)
        """
        try:
            mean = data.mean()
            std = data.std()

            if std == 0:
                return pd.Series([False] * len(data)), {}

            z_scores = np.abs((data - mean) / std)
            outliers = z_scores > threshold

            stats = {
                "method": "Z-Score",
                "threshold": threshold,
                "mean": float(mean),
                "std": float(std),
                "outlier_count": int(outliers.sum()),
                "outlier_percentage": float((outliers.sum() / len(data)) * 100),
                "max_z_score": float(z_scores.max()),
            }

            return outliers, stats

        except Exception as e:
            self.logger.error(f"Z-Score detection failed: {e}")
            return pd.Series([False] * len(data)), {}

    def detect_moving_average(
        self, data: pd.Series, window: int = 20, threshold: float = 2.0
    ) -> tuple[pd.Series, dict[str, Any]]:
        """Moving Average módszerrel történő kiugró értékek detektálása.

        Args:
            data: Adatsor
            window: Mozgóátlag ablakméret
            threshold: Küszöbérték a szóráshoz képest

        Returns:
            (kiugró értékek maszkja, statisztikák)
        """
        try:
            ma = data.rolling(window=window, center=True).mean()
            std = data.rolling(window=window, center=True).std()

            # Szélső értékek kezelése
            ma = ma.fillna(method="bfill").fillna(method="ffill")
            std = std.fillna(method="bfill").fillna(method="ffill")

            upper_bound = ma + threshold * std
            lower_bound = ma - threshold * std

            outliers = (data < lower_bound) | (data > upper_bound)

            stats = {
                "method": "Moving Average",
                "window": window,
                "threshold": threshold,
                "outlier_count": int(outliers.sum()),
                "outlier_percentage": float((outliers.sum() / len(data)) * 100),
            }

            return outliers, stats

        except Exception as e:
            self.logger.error(f"Moving Average detection failed: {e}")
            return pd.Series([False] * len(data)), {}

    def detect_all_methods(
        self,
        data: pd.Series,
        iqr_threshold: float = 1.5,
        z_score_threshold: float = 3.0,
        ma_window: int = 20,
        ma_threshold: float = 2.0,
    ) -> dict[str, tuple[pd.Series, dict[str, Any]]]:
        """Összes módszerrel történő kiugró értékek detektálása.

        Returns:
            Módszerekhez tartozó eredmények szótára
        """
        results = {}

        results["iqr"] = self.detect_iqr(data, iqr_threshold)
        results["z_score"] = self.detect_z_score(data, z_score_threshold)
        results["moving_average"] = self.detect_moving_average(data, ma_window, ma_threshold)

        return results


class DataQualityFramework:
    """Adatminőség-keretrendszer fő osztálya.

    Felelősségek:
    - 3-szintű validáció végrehajtása
    - Kiugró értékek detektálása
    - Minőségjelentések generálása
    - Automatikus javítási lehetőségek
    - Minőségkövetés és trendanalízis
    """

    def __init__(
        self,
        validator: DataValidator | None = None,
        logger: logging.Logger | None = None,
    ):
        """Inicializálás.

        Args:
            validator: DataValidator példány
            logger: Logger példány
        """
        self.validator = validator or DataValidator(logger=logger)
        self.logger = logger or logging.getLogger(__name__)
        self.outlier_detector = OutlierDetector(logger=logger)

        # Minőségmetrikák nyomon követése
        self.quality_history: list[dict[str, Any]] = []
        self.corrections: list[DataCorrection] = []
        self.issues: list[QualityIssue] = []

        # Konfiguráció
        self.config = {
            "outlier_detection": {
                "iqr_threshold": 1.5,
                "z_score_threshold": 3.0,
                "ma_window": 20,
                "ma_threshold": 2.0,
            },
            "quality_thresholds": {
                "excellent": 95.0,
                "good": 85.0,
                "acceptable": 75.0,
                "poor": 60.0,
            },
            "auto_correction": {"enabled": True, "max_corrections_per_batch": 100},
        }

    def validate_level_1_basic(
        self, data: pd.DataFrame, data_type: str = "ohlcv"
    ) -> tuple[bool, list[QualityIssue]]:
        """Level 1 - Alap validálás: Adatstruktúra, típusok, kötelező mezők.

        Args:
            data: DataFrame az adatokkal
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            (validációs eredmény, problémák listája)
        """
        issues = []
        is_valid = True

        try:
            # Kötelező mezők ellenőrzése
            if data_type == "ohlcv":
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
            else:  # tick
                required_fields = ["symbol", "bid", "ask", "time"]

            missing_fields = [field for field in required_fields if field not in data.columns]

            if missing_fields:
                is_valid = False
                issues.append(
                    QualityIssue(
                        severity=IssueSeverity.CRITICAL,
                        category="missing_fields",
                        description=f"Hiányzó kötelező mezők: {', '.join(missing_fields)}",
                        count=len(missing_fields),
                    )
                )

            # Adattípusok ellenőrzése
            type_issues = []
            for col in data.columns:
                if data[col].isnull().all():
                    continue

                if col in ["open", "high", "low", "close", "bid", "ask"]:
                    if not pd.api.types.is_numeric_dtype(data[col]):
                        type_issues.append(col)
                elif col in ["time", "volume"]:
                    if not pd.api.types.is_integer_dtype(data[col]):
                        type_issues.append(col)

            if type_issues:
                issues.append(
                    QualityIssue(
                        severity=IssueSeverity.CRITICAL,
                        category="invalid_types",
                        description=f"Érvénytelen adattípusok: {', '.join(type_issues)}",
                        count=len(type_issues),
                    )
                )

            # Üres értékek ellenőrzése
            null_count = data.isnull().sum().sum()
            if null_count > 0:
                issues.append(
                    QualityIssue(
                        severity=IssueSeverity.WARNING,
                        category="missing_values",
                        description=f"Üres értékek találhatók: {null_count} db",
                        count=int(null_count),
                    )
                )

            return is_valid, issues

        except Exception as e:
            self.logger.error(f"Level 1 validation failed: {e}")
            issues.append(
                QualityIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="validation_error",
                    description=f"Validálási hiba: {str(e)}",
                )
            )
            return False, issues

    def validate_level_2_logical(
        self, data: pd.DataFrame, data_type: str = "ohlcv"
    ) -> tuple[bool, list[QualityIssue]]:
        """Level 2 - Logikai validálás: Ártartományok, időbélyegek, konzisztencia.

        Args:
            data: DataFrame az adatokkal
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            (validációs eredmény, problémák listája)
        """
        issues = []
        is_valid = True

        try:
            if data_type == "ohlcv":
                # OHLC kapcsolatok ellenőrzése
                ohlc_issues = 0

                # High >= Low
                invalid_high_low = (data["high"] < data["low"]).sum()
                if invalid_high_low > 0:
                    ohlc_issues += invalid_high_low
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.CRITICAL,
                            category="invalid_ohlc",
                            description=f"High < Low esetek: {invalid_high_low} db",
                            count=int(invalid_high_low),
                        )
                    )

                # High >= Open, High >= Close
                invalid_high_open = (data["high"] < data["open"]).sum()
                invalid_high_close = (data["high"] < data["close"]).sum()

                if invalid_high_open > 0 or invalid_high_close > 0:
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.WARNING,
                            category="suspicious_high",
                            description=f"High < Open/Close esetek: {invalid_high_open + invalid_high_close} db",
                            count=int(invalid_high_open + invalid_high_close),
                        )
                    )

                # Low <= Open, Low <= Close
                invalid_low_open = (data["low"] > data["open"]).sum()
                invalid_low_close = (data["low"] > data["close"]).sum()

                if invalid_low_open > 0 or invalid_low_close > 0:
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.WARNING,
                            category="suspicious_low",
                            description=f"Low > Open/Close esetek: {invalid_low_open + invalid_low_close} db",
                            count=int(invalid_low_open + invalid_low_close),
                        )
                    )

                # Volume ellenőrzés
                negative_volume = (data["volume"] < 0).sum()
                if negative_volume > 0:
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.CRITICAL,
                            category="invalid_volume",
                            description=f"Negatív volume értékek: {negative_volume} db",
                            count=int(negative_volume),
                        )
                    )

            else:  # tick
                # Bid-Ask kapcsolat ellenőrzése
                invalid_bid_ask = (data["ask"] < data["bid"]).sum()
                if invalid_bid_ask > 0:
                    is_valid = False
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.CRITICAL,
                            category="invalid_bid_ask",
                            description=f"Ask < Bid esetek: {invalid_bid_ask} db",
                            count=int(invalid_bid_ask),
                        )
                    )

                # Spread ellenőrzése
                spread = data["ask"] - data["bid"]
                max_spread_ratio = 0.01  # 1%
                large_spreads = (spread / data["bid"] > max_spread_ratio).sum()

                if large_spreads > 0:
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.WARNING,
                            category="large_spread",
                            description=f"Nagy spread értékek: {large_spreads} db",
                            count=int(large_spreads),
                        )
                    )

            # Időbélyeg ellenőrzése (kronológiai sorrend)
            if "time" in data.columns:
                time_diffs = data["time"].diff()
                negative_time_diffs = (time_diffs < 0).sum()

                if negative_time_diffs > 0:
                    issues.append(
                        QualityIssue(
                            severity=IssueSeverity.WARNING,
                            category="time_sequence",
                            description=f"Időbeli visszafordulások: {negative_time_diffs} db",
                            count=int(negative_time_diffs),
                        )
                    )

            return is_valid, issues

        except Exception as e:
            self.logger.error(f"Level 2 validation failed: {e}")
            issues.append(
                QualityIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="validation_error",
                    description=f"Validálási hiba: {str(e)}",
                )
            )
            return False, issues

    def validate_level_3_statistical(
        self, data: pd.DataFrame, data_type: str = "ohlcv"
    ) -> tuple[bool, list[QualityIssue]]:
        """Level 3 - Statisztikai validálás: Kiugró értékek, trendek, volatilitás.

        Args:
            data: DataFrame az adatokkal
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            (validációs eredmény, problémák listája)
        """
        issues = []
        is_valid = True

        try:
            if data_type == "ohlcv":
                # Kiugró értékek detektálása minden árfolyam mezőre
                price_columns = ["open", "high", "low", "close"]

                for col in price_columns:
                    if col not in data.columns:
                        continue

                    # Összes módszerrel történő detektálás
                    results = self.outlier_detector.detect_all_methods(data[col])

                    for method, (outliers, stats) in results.items():
                        outlier_count = int(outliers.sum())

                        if outlier_count > 0:
                            outlier_pct = (outlier_count / len(data)) * 100

                            severity = IssueSeverity.WARNING
                            if outlier_pct > 5:  # Több mint 5% kiugró érték
                                severity = IssueSeverity.CRITICAL

                            issues.append(
                                QualityIssue(
                                    severity=severity,
                                    category=f"outliers_{method}_{col}",
                                    description=f"Kiugró értékek ({method}): {outlier_count} db ({outlier_pct:.2f}%)",
                                    count=outlier_count,
                                    details=stats,
                                )
                            )

                # Volatilitás ellenőrzése
                if "close" in data.columns:
                    returns = data["close"].pct_change().dropna()

                    if len(returns) > 0:
                        vol_issues = 0

                        # Túl nagy volatilitás (napi > 10%)
                        high_vol = (np.abs(returns) > 0.10).sum()
                        if high_vol > 0:
                            vol_issues += high_vol
                            issues.append(
                                QualityIssue(
                                    severity=IssueSeverity.WARNING,
                                    category="high_volatility",
                                    description=f"Magas volatilitású periódusok: {high_vol} db",
                                    count=int(high_vol),
                                )
                            )

                        # Túl alacsony volatilitás (napi < 0.01%)
                        low_vol = (np.abs(returns) < 0.0001).sum()
                        if low_vol > len(returns) * 0.5:  # Több mint 50%
                            issues.append(
                                QualityIssue(
                                    severity=IssueSeverity.INFO,
                                    category="low_volatility",
                                    description=f"Alacsony volatilitású periódusok: {low_vol} db",
                                    count=int(low_vol),
                                )
                            )

            else:  # tick
                # Tick adatok statisztikai ellenőrzése
                if "bid" in data.columns and "ask" in data.columns:
                    spread = data["ask"] - data["bid"]

                    # Spread statisztikák
                    results = self.outlier_detector.detect_all_methods(spread)

                    for method, (outliers, stats) in results.items():
                        outlier_count = int(outliers.sum())

                        if outlier_count > 0:
                            issues.append(
                                QualityIssue(
                                    severity=IssueSeverity.WARNING,
                                    category=f"spread_outliers_{method}",
                                    description=f"Kiugró spread értékek ({method}): {outlier_count} db",
                                    count=outlier_count,
                                    details=stats,
                                )
                            )

            return is_valid, issues

        except Exception as e:
            self.logger.error(f"Level 3 validation failed: {e}")
            issues.append(
                QualityIssue(
                    severity=IssueSeverity.CRITICAL,
                    category="validation_error",
                    description=f"Validálási hiba: {str(e)}",
                )
            )
            return False, issues

    def validate_comprehensive(
        self, data: pd.DataFrame, data_type: str = "ohlcv"
    ) -> dict[str, Any]:
        """Komprehenzív validálás mindhárom szinten.

        Args:
            data: DataFrame az adatokkal
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            Validációs eredmények szótára
        """
        result = {
            "timestamp": datetime.now(UTC).isoformat(),
            "data_type": data_type,
            "total_records": len(data),
            "validation_levels": {},
            "overall_status": "passed",
            "issues": [],
            "metrics": QualityMetrics(),
        }

        # Level 1 - Alap validálás
        level1_valid, level1_issues = self.validate_level_1_basic(data, data_type)
        result["validation_levels"]["level_1_basic"] = {
            "status": "passed" if level1_valid else "failed",
            "issues_count": len(level1_issues),
        }
        result["issues"].extend([issue.to_dict() for issue in level1_issues])

        if not level1_valid:
            result["overall_status"] = "failed"
            return result

        # Level 2 - Logikai validálás
        level2_valid, level2_issues = self.validate_level_2_logical(data, data_type)
        result["validation_levels"]["level_2_logical"] = {
            "status": "passed" if level2_valid else "failed",
            "issues_count": len(level2_issues),
        }
        result["issues"].extend([issue.to_dict() for issue in level2_issues])

        if not level2_valid:
            result["overall_status"] = "failed"

        # Level 3 - Statisztikai validálás
        level3_valid, level3_issues = self.validate_level_3_statistical(data, data_type)
        result["validation_levels"]["level_3_statistical"] = {
            "status": "passed" if level3_valid else "failed",
            "issues_count": len(level3_issues),
        }
        result["issues"].extend([issue.to_dict() for issue in level3_issues])

        # Minőségi metrikák kiszámítása
        metrics = self._calculate_quality_metrics(result["issues"], len(data))
        result["metrics"] = metrics.to_dict()

        # Összesített állapot frissítése
        if metrics.overall_score < self.config["quality_thresholds"]["acceptable"]:
            result["overall_status"] = "failed"
        elif metrics.overall_score < self.config["quality_thresholds"]["good"]:
            result["overall_status"] = "warning"

        return result

    def _calculate_quality_metrics(
        self, issues: list[dict[str, Any]], total_records: int
    ) -> QualityMetrics:
        """Minőségi metrikák kiszámítása.

        Args:
            issues: Problémák listája
            total_records: Összes rekord száma

        Returns:
            QualityMetrics objektum
        """
        metrics = QualityMetrics()

        if total_records == 0:
            return metrics

        # Komplettesség (nincs hiányzó adat)
        missing_value_issues = [i for i in issues if i["category"] == "missing_values"]
        missing_count = sum(i["count"] for i in missing_value_issues)
        metrics.completeness = max(0.0, 100.0 - (missing_count / total_records * 100))

        # Pontosság (nincs kritikus hiba)
        critical_issues = [i for i in issues if i["severity"] == "critical"]
        critical_count = len(critical_issues)
        metrics.accuracy = max(0.0, 100.0 - (critical_count * 10))

        # Konzisztencia (nincs logikai hiba)
        logical_issues = [
            i
            for i in issues
            if i["category"] in ["invalid_ohlc", "invalid_bid_ask", "time_sequence"]
        ]
        logical_count = len(logical_issues)
        metrics.consistency = max(0.0, 100.0 - (logical_count * 5))

        # Időbeliség (nincs időbeli probléma)
        time_issues = [i for i in issues if "time" in i["category"]]
        time_count = len(time_issues)
        metrics.timeliness = max(0.0, 100.0 - (time_count * 2))

        # Összesített pontszám
        metrics.calculate_overall()

        return metrics

    def auto_correct_data(
        self, data: pd.DataFrame, data_type: str = "ohlcv"
    ) -> tuple[pd.DataFrame, list[DataCorrection]]:
        """Automatikus adatjavítás.

        Args:
            data: DataFrame az adatokkal
            data_type: Adattípus (ohlcv vagy tick)

        Returns:
            (javított DataFrame, javítások listája)
        """
        corrections = []

        if not self.config["auto_correction"]["enabled"]:
            return data, corrections

        corrected_data = data.copy()
        max_corrections = self.config["auto_correction"]["max_corrections_per_batch"]

        try:
            if data_type == "ohlcv":
                # High < Low javítása
                invalid_mask = corrected_data["high"] < corrected_data["low"]
                invalid_count = invalid_mask.sum()

                if invalid_count > 0 and invalid_count <= max_corrections:
                    for idx in corrected_data[invalid_mask].index:
                        original_high = corrected_data.loc[idx, "high"]
                        original_low = corrected_data.loc[idx, "low"]

                        # Csere ha szükséges
                        if original_high < original_low:
                            corrected_data.loc[idx, "high"] = original_low
                            corrected_data.loc[idx, "low"] = original_high

                            corrections.append(
                                DataCorrection(
                                    original_value=original_high,
                                    corrected_value=original_low,
                                    correction_method="swap_high_low",
                                    reason="High < Low korrekció",
                                    confidence=0.9,
                                )
                            )

                # Hiányzó értékek interpolációja
                for col in ["open", "high", "low", "close"]:
                    if col in corrected_data.columns:
                        null_count = corrected_data[col].isnull().sum()

                        if null_count > 0 and null_count <= max_corrections:
                            original_values = corrected_data[col].copy()
                            corrected_data[col] = corrected_data[col].interpolate(
                                method="linear", limit=max_corrections
                            )

                            # Javítások rögzítése
                            for idx in corrected_data[
                                corrected_data[col].notnull() & original_values.isnull()
                            ].index:
                                corrections.append(
                                    DataCorrection(
                                        original_value=float("nan"),
                                        corrected_value=float(corrected_data.loc[idx, col]),
                                        correction_method="interpolation",
                                        reason=f"Hiányzó {col} interpolációja",
                                        confidence=0.7,
                                    )
                                )

            else:  # tick
                # Ask < Bid javítása
                invalid_mask = corrected_data["ask"] < corrected_data["bid"]
                invalid_count = invalid_mask.sum()

                if invalid_count > 0 and invalid_count <= max_corrections:
                    for idx in corrected_data[invalid_mask].index:
                        original_ask = corrected_data.loc[idx, "ask"]
                        original_bid = corrected_data.loc[idx, "bid"]

                        # Csere ha szükséges
                        if original_ask < original_bid:
                            corrected_data.loc[idx, "ask"] = original_bid
                            corrected_data.loc[idx, "bid"] = original_ask

                            corrections.append(
                                DataCorrection(
                                    original_value=original_ask,
                                    corrected_value=original_bid,
                                    correction_method="swap_bid_ask",
                                    reason="Ask < Bid korrekció",
                                    confidence=0.9,
                                )
                            )

            # Javítások mentése
            self.corrections.extend(corrections)

            return corrected_data, corrections

        except Exception as e:
            self.logger.error(f"Auto-correction failed: {e}")
            return data, corrections

    def generate_quality_report(self, output_path: str, format: str = "json") -> None:
        """Minőségjelentés generálása.

        Args:
            output_path: Kimeneti fájl elérési útja
            format: Kimeneti formátum (json vagy csv)
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            report = {
                "generated_at": datetime.now(UTC).isoformat(),
                "total_issues": len(self.issues),
                "total_corrections": len(self.corrections),
                "quality_history": self.quality_history,
                "recent_issues": [issue.to_dict() for issue in self.issues[-100:]],  # Utolsó 100
                "recent_corrections": [
                    corr.to_dict() for corr in self.corrections[-100:]
                ],  # Utolsó 100
            }

            if format.lower() == "json":
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)

            elif format.lower() == "csv":
                # Problémák CSV-be
                if self.issues:
                    issues_df = pd.DataFrame([issue.to_dict() for issue in self.issues])
                    issues_path = output_path.parent / f"{output_path.stem}_issues.csv"
                    issues_df.to_csv(issues_path, index=False)

                # Javítások CSV-be
                if self.corrections:
                    corrections_df = pd.DataFrame([corr.to_dict() for corr in self.corrections])
                    corrections_path = output_path.parent / f"{output_path.stem}_corrections.csv"
                    corrections_df.to_csv(corrections_path, index=False)

            self.logger.info(f"Quality report saved to: {output_path}")

        except Exception as e:
            self.logger.error(f"Failed to generate quality report: {e}")

    def track_quality_trend(self, symbol: str, timeframe: str, metrics: QualityMetrics) -> None:
        """Minőség trend nyomon követése.

        Args:
            symbol: Pénznem szimbólum
            timeframe: Időkeret
            metrics: Minőségi metrikák
        """
        trend_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "symbol": symbol,
            "timeframe": timeframe,
            "metrics": metrics.to_dict(),
        }

        self.quality_history.append(trend_entry)

        # Trend analízis (utolsó 30 nap)
        recent_history = [
            h
            for h in self.quality_history[-30:]
            if h["symbol"] == symbol and h["timeframe"] == timeframe
        ]

        if len(recent_history) >= 7:
            scores = [h["metrics"]["overall_score"] for h in recent_history]
            trend = "improving" if scores[-1] > scores[0] else "declining"

            if trend == "declining":
                self.logger.warning(
                    f"Quality declining for {symbol} {timeframe}: "
                    f"{scores[0]:.2f} -> {scores[-1]:.2f}"
                )

    def get_quality_summary(self) -> dict[str, Any]:
        """Összesített minőségi összefoglaló.

        Returns:
            Minőségi összefoglaló szótára
        """
        if not self.quality_history:
            return {"status": "no_data", "message": "Nincs elérhető minőségadatok"}

        recent_history = self.quality_history[-30:]

        scores = [h["metrics"]["overall_score"] for h in recent_history]

        return {
            "period": "last_30_days",
            "average_score": float(np.mean(scores)),
            "min_score": float(np.min(scores)),
            "max_score": float(np.max(scores)),
            "trend": "improving" if scores[-1] > scores[0] else "declining",
            "total_issues": len(self.issues),
            "total_corrections": len(self.corrections),
            "last_update": recent_history[-1]["timestamp"],
        }


# Példa használat
if __name__ == "__main__":
    # Logger beállítása
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Framework létrehozása
    framework = DataQualityFramework(logger=logger)

    # Tesztadatok létrehozása
    print("\n=== Tesztadatok generálása ===")
    dates = pd.date_range(start="2025-01-01", end="2025-01-31", freq="H")
    data = pd.DataFrame(
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

    # Szándékosan hibák bevezetése
    data.loc[10, "high"] = 0.5  # Túl alacsony high
    data.loc[20, "low"] = 2.0  # Túl magas low
    data.loc[30, "volume"] = -100  # Negatív volume

    print(f"Tesztadatok létrehozva: {len(data)} sor")

    # Komprehenzív validálás
    print("\n=== Komprehenzív validálás ===")
    result = framework.validate_comprehensive(data, data_type="ohlcv")

    print(f"Összesített állapot: {result['overall_status']}")
    print(f"Minőségi pontszám: {result['metrics']['overall_score']:.2f}")
    print(f"Problémák száma: {len(result['issues'])}")

    # Problémák listázása
    print("\n=== Problémák ===")
    for issue in result["issues"][:5]:  # Első 5 probléma
        print(f"- [{issue['severity']}] {issue['category']}: {issue['description']}")

    # Automatikus javítás
    print("\n=== Automatikus javítás ===")
    corrected_data, corrections = framework.auto_correct_data(data, data_type="ohlcv")
    print(f"Javítások száma: {len(corrections)}")

    # Minőségjelentés generálása
    print("\n=== Minőségjelentés generálása ===")
    framework.generate_quality_report("logs/quality_report.json", format="json")
    framework.generate_quality_report("logs/quality_report.csv", format="csv")
    print("Jelentések elmentve")
