"""Collector Storage Module.
========================

Extended storage implementation for MT5 Collector with support for:
- CSV format storage
- Multi-timeframe data organization
- Multi-instrument data organization
- Data warehouse structure integration
- Automatic data organization and quality management

Author: Neural AI Team
Date: 2025-12-16
Version: 2.0.0
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from neural_ai.collectors.mt5.error_handler import StorageError

try:
    import fastparquet

    PARQUET_AVAILABLE = True
except ImportError:
    PARQUET_AVAILABLE = False


class CollectorStorage:
    """Extended storage for MT5 Collector with CSV, Parquet and multi-instrument support.

    Features:
    - JSONL format for tick data (append-only, efficient)
    - CSV format for OHLCV data (structured, queryable)
    - Parquet format for OHLCV data (compressed, fast querying)
    - Multi-instrument support (EURUSD, GBPUSD, USDJPY, XAUUSD)
    - Multi-timeframe support (M1, M5, M15, H1, H4, D1)
    - Data warehouse structure integration
    """

    def __init__(
        self,
        base_path: str = "data",
        logger: logging.Logger | None = None,
        use_parquet: bool = True,
        enable_warehouse_integration: bool = True,
    ):
        """Initialize CollectorStorage.

        Args:
            base_path: Base path for data storage
            logger: Optional logger instance
            use_parquet: Whether to use Parquet format when available
            enable_warehouse_integration: Enable automatic Data Warehouse integration
        """
        self.base_path = Path(base_path)
        self.logger = logger or logging.getLogger(__name__)
        self.use_parquet = use_parquet and PARQUET_AVAILABLE
        self.enable_warehouse_integration = enable_warehouse_integration

        # Create base directories
        self.base_path.mkdir(parents=True, exist_ok=True)
        (self.base_path / "collectors" / "mt5").mkdir(parents=True, exist_ok=True)

        # Supported instruments and timeframes
        self.supported_instruments = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.supported_timeframes = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "H1": 16385,
            "H4": 16388,
            "D1": 16408,
        }

        # Data Warehouse Manager inicializálása
        if self.enable_warehouse_integration:
            try:
                from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
                    DataWarehouseManager,
                )

                self.warehouse_manager = DataWarehouseManager(
                    base_path=str(self.base_path), logger=self.logger
                )
                self.logger.info("Data Warehouse Manager integration: ENABLED")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Data Warehouse Manager: {e}")
                self.enable_warehouse_integration = False

        self.logger.info(f"CollectorStorage initialized: {self.base_path}")
        if self.use_parquet:
            self.logger.info("Parquet format support: ENABLED (fastparquet)")
        else:
            self.logger.info("Parquet format support: DISABLED (using CSV)")

    def store_tick(self, tick_data: dict[str, Any]) -> None:
        """Store tick data in JSONL format.

        Args:
            tick_data: Dictionary containing tick data
        """
        try:
            symbol = tick_data["symbol"]

            # Validate symbol
            if symbol not in self.supported_instruments:
                self.logger.warning(f"Unsupported instrument: {symbol}")
                return

            # Prepare data
            data = {
                "symbol": symbol,
                "bid": tick_data["bid"],
                "ask": tick_data["ask"],
                "time": tick_data["time"],
                "timestamp": datetime.now().isoformat(),
            }

            # Store in raw data directory
            filepath = self.base_path / "collectors" / "mt5" / "raw" / f"{symbol}_ticks.jsonl"
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Append to JSONL file
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")

            self.logger.debug(f"Tick stored: {symbol} at {data['timestamp']}")

        except Exception as e:
            self.logger.error(f"Error storing tick data: {e}")
            raise

    def store_ohlcv(self, ohlcv_data: dict[str, Any]) -> None:
        """Store OHLCV data in CSV or Parquet format.

        Args:
            ohlcv_data: Dictionary containing OHLCV data
        """
        try:
            symbol = ohlcv_data["symbol"]
            timeframe = ohlcv_data["timeframe"]

            # Validate symbol
            if symbol not in self.supported_instruments:
                self.logger.warning(f"Unsupported instrument: {symbol}")
                return

            # Get timeframe name
            tf_name = None
            for name, tf_id in self.supported_timeframes.items():
                if tf_id == timeframe:
                    tf_name = name
                    break

            if tf_name is None:
                self.logger.warning(f"Unsupported timeframe: {timeframe}")
                return

            # Use Parquet if available and enabled, otherwise use CSV
            if self.use_parquet:
                self._store_ohlcv_parquet(symbol, tf_name, ohlcv_data)
            else:
                self._store_ohlcv_csv(symbol, tf_name, ohlcv_data)

            self.logger.debug(
                f"OHLCV stored: {symbol} {tf_name} "
                f"({len(ohlcv_data.get('bars', []))} bars) "
                f"[{'Parquet' if self.use_parquet else 'CSV'}]"
            )

        except Exception as e:
            self.logger.error(f"Error storing OHLCV data: {e}")
            raise

    def store_invalid_data(self, data: dict[str, Any], data_type: str, reason: str) -> None:
        """Store invalid data separately for analysis.

        Args:
            data: Invalid data
            data_type: Type of data (tick, ohlcv)
            reason: Reason for invalidity
        """
        try:
            symbol = data.get("symbol", "UNKNOWN")

            # Add invalidity reason
            invalid_data = data.copy()
            invalid_data["invalid_reason"] = reason
            invalid_data["timestamp"] = datetime.now().isoformat()

            # Store in invalid data directory
            filepath = (
                self.base_path
                / "collectors"
                / "mt5"
                / "invalid"
                / f"{symbol}_{data_type}_invalid.jsonl"
            )
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Append to JSONL file
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(invalid_data) + "\n")

            self.logger.warning(f"Invalid {data_type} data stored: {symbol} - {reason}")

        except Exception as e:
            self.logger.error(f"Error storing invalid data: {e}")
            raise

    def get_data_warehouse_path(
        self, symbol: str, timeframe: str | None = None, data_type: str = "raw"
    ) -> Path:
        """Get path for data warehouse structure.

        Args:
            symbol: Instrument symbol
            timeframe: Timeframe (M1, M5, etc.) or None for ticks
            data_type: Type of data (raw, processed, validated)

        Returns:
            Path object for the specified location
        """
        path = self.base_path / "warehouse" / data_type / symbol

        if timeframe:
            path = path / timeframe

        path.mkdir(parents=True, exist_ok=True)
        return path

    def store_to_warehouse(
        self, data: dict[str, Any], data_type: str = "raw", validated: bool = False
    ) -> None:
        """Store data in warehouse structure.

        Args:
            data: Data to store
            data_type: Type of data (raw, processed, validated)
            validated: Whether the data has been validated
        """
        try:
            symbol = data.get("symbol", "UNKNOWN")
            timeframe = data.get("timeframe")

            # Convert timeframe ID to name if present
            tf_name = None
            if timeframe:
                for name, tf_id in self.supported_timeframes.items():
                    if tf_id == timeframe:
                        tf_name = name
                        break

            # Get warehouse path
            warehouse_path = self.get_data_warehouse_path(
                symbol=symbol,
                timeframe=tf_name,
                data_type="validated" if validated else data_type,
            )

            # Store based on data type
            if "bars" in data:  # OHLCV data
                filepath = warehouse_path / f"{symbol}_{tf_name}_ohlcv.csv"
                self._store_ohlcv_to_warehouse(data, filepath)
            else:  # Tick data
                filepath = warehouse_path / f"{symbol}_ticks.jsonl"
                self._store_tick_to_warehouse(data, filepath)

            self.logger.debug(
                f"Data stored to warehouse: {symbol} {tf_name or 'ticks'} ({data_type})"
            )

        except Exception as e:
            self.logger.error(f"Error storing to warehouse: {e}")
            raise

    def _store_tick_to_warehouse(self, data: dict[str, Any], filepath: Path) -> None:
        """Store tick data to warehouse."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

    def _store_ohlcv_csv(self, symbol: str, tf_name: str, ohlcv_data: dict[str, Any]) -> None:
        """Store OHLCV data in CSV format."""
        filepath = self.base_path / "collectors" / "mt5" / f"{symbol}_{tf_name}_ohlcv.csv"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        write_header = not filepath.exists()

        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if write_header:
                writer.writerow(["timestamp", "time", "open", "high", "low", "close", "volume"])

            for bar in ohlcv_data.get("bars", []):
                writer.writerow(
                    [
                        datetime.now().isoformat(),
                        bar.get("time", ""),
                        bar.get("open", ""),
                        bar.get("high", ""),
                        bar.get("low", ""),
                        bar.get("close", ""),
                        bar.get("volume", ""),
                    ]
                )

    def _store_ohlcv_parquet(self, symbol: str, tf_name: str, ohlcv_data: dict[str, Any]) -> None:
        """Store OHLCV data in Parquet format."""
        import pandas as pd

        filepath = self.base_path / "collectors" / "mt5" / f"{symbol}_{tf_name}_ohlcv.parquet"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Prepare data for DataFrame
        rows = []
        for bar in ohlcv_data.get("bars", []):
            rows.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "time": bar.get("time", 0),
                    "open": bar.get("open", 0.0),
                    "high": bar.get("high", 0.0),
                    "low": bar.get("low", 0.0),
                    "close": bar.get("close", 0.0),
                    "volume": bar.get("volume", 0),
                }
            )

        if not rows:
            return

        # Create DataFrame
        df_new = pd.DataFrame(rows)

        # Append to existing Parquet file or create new one
        if filepath.exists():
            try:
                # Read existing data
                df_existing = pd.read_parquet(filepath, engine="fastparquet")
                # Concatenate
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                # Remove duplicates based on time column
                df_combined = df_combined.drop_duplicates(subset=["time"], keep="last")
                # Write back
                df_combined.to_parquet(
                    filepath, engine="fastparquet", compression="snappy", index=False
                )
            except Exception as e:
                self.logger.warning(f"Error reading existing Parquet file, creating new: {e}")
                df_new.to_parquet(filepath, engine="fastparquet", compression="snappy", index=False)
        else:
            # Create new Parquet file
            df_new.to_parquet(filepath, engine="fastparquet", compression="snappy", index=False)

    def _store_ohlcv_to_warehouse(self, data: dict[str, Any], filepath: Path) -> None:
        """Store OHLCV data to warehouse."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Use Parquet for warehouse if available, otherwise CSV
        if self.use_parquet and filepath.suffix != ".parquet":
            filepath = filepath.with_suffix(".parquet")
            self._store_ohlcv_parquet(
                data.get("symbol", "UNKNOWN"),
                str(data.get("timeframe", "UNKNOWN")),
                data,
            )
        else:
            filepath = filepath.with_suffix(".csv")
            write_header = not filepath.exists()

            with open(filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                if write_header:
                    writer.writerow(["timestamp", "time", "open", "high", "low", "close", "volume"])

                for bar in data.get("bars", []):
                    writer.writerow(
                        [
                            datetime.now().isoformat(),
                            bar.get("time", ""),
                            bar.get("open", ""),
                            bar.get("high", ""),
                            bar.get("low", ""),
                            bar.get("close", ""),
                            bar.get("volume", ""),
                        ]
                    )

    def get_storage_stats(self) -> dict[str, Any]:
        """Get storage statistics.

        Returns:
            Dictionary containing storage statistics
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "parquet_enabled": self.use_parquet,
            "total_files": 0,
            "by_instrument": {},
            "by_timeframe": {},
            "by_format": {"csv": 0, "parquet": 0, "jsonl": 0},
            "total_size_bytes": 0,
        }

        # Count files and sizes
        mt5_path = self.base_path / "collectors" / "mt5"
        if mt5_path.exists():
            for file_path in mt5_path.rglob("*"):
                if file_path.is_file():
                    stats["total_files"] += 1
                    stats["total_size_bytes"] += file_path.stat().st_size

                    # Count by format
                    if file_path.suffix == ".csv":
                        stats["by_format"]["csv"] += 1
                    elif file_path.suffix == ".parquet":
                        stats["by_format"]["parquet"] += 1
                    elif file_path.suffix == ".jsonl":
                        stats["by_format"]["jsonl"] += 1

                    # Count by instrument
                    filename = file_path.name
                    for instrument in self.supported_instruments:
                        if instrument in filename:
                            stats["by_instrument"][instrument] = (
                                stats["by_instrument"].get(instrument, 0) + 1
                            )

                    # Count by timeframe
                    for timeframe in self.supported_timeframes:
                        if timeframe in filename:
                            stats["by_timeframe"][timeframe] = (
                                stats["by_timeframe"].get(timeframe, 0) + 1
                            )

        return stats

    # ===== DATA WAREHOUSE INTEGRATION METHODS =====

    def organize_data_to_warehouse(
        self,
        instrument: str,
        timeframe: str | None = None,
        data_type: str = "validated",
    ) -> dict[str, Any]:
        """Adatok szervezése a Data Warehouse-ba.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret (opcionális)
            data_type: Adattípus (raw, validated, historical, update, realtime)

        Returns:
            A szervezés eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            # Forrás útvonal
            source_path = self.base_path / "collectors" / "mt5" / "raw"

            if timeframe:
                # OHLCV adatok
                if self.use_parquet:
                    source_pattern = f"{instrument}_{timeframe}_ohlcv.parquet"
                else:
                    source_pattern = f"{instrument}_{timeframe}_ohlcv.csv"

                source_files = list(source_path.glob(source_pattern))
            else:
                # Tick adatok
                source_pattern = f"{instrument}_ticks.jsonl"
                source_files = list(source_path.glob(source_pattern))

            if not source_files:
                return {
                    "status": "no_data",
                    "message": f"No data found for {instrument} {timeframe or 'ticks'}",
                }

            # Cél útvonal a warehouse-ban
            if data_type in ["raw", "validated"]:
                dest_path = f"warehouse/{data_type}/{instrument}"
            else:
                dest_path = f"warehouse/{data_type}/{instrument}"
                if timeframe:
                    dest_path += f"/{timeframe}"

            # Adatok mozgatása
            result = self.warehouse_manager.move_data(
                source_path="collectors/mt5/raw",
                destination_path=dest_path,
                instrument=instrument,
                timeframe=timeframe,
            )

            self.logger.info(
                f"Data organized to warehouse: {instrument} {timeframe or 'ticks'} -> {data_type}"
            )

            return result

        except Exception as e:
            error_msg = f"Error organizing data to warehouse: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def auto_organize_validated_data(self) -> dict[str, Any]:
        """Validált adatok automatikus szervezése a warehouse-ba.

        Returns:
            A szervezés eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            organized_count = 0
            results = {}

            # Tick adatok szervezése
            for instrument in self.supported_instruments:
                result = self.organize_data_to_warehouse(
                    instrument=instrument, data_type="validated"
                )
                results[f"{instrument}_ticks"] = result
                if result.get("status") == "success":
                    organized_count += 1

            # OHLCV adatok szervezése
            for instrument in self.supported_instruments:
                for timeframe in self.supported_timeframes:
                    result = self.organize_data_to_warehouse(
                        instrument=instrument,
                        timeframe=timeframe,
                        data_type="validated",
                    )
                    results[f"{instrument}_{timeframe}"] = result
                    if result.get("status") == "success":
                        organized_count += 1

            return {
                "status": "success",
                "message": f"Auto-organized {organized_count} data sources",
                "results": results,
                "organized_count": organized_count,
            }

        except Exception as e:
            error_msg = f"Error in auto-organize: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def cleanup_old_raw_data(self, retention_days: int = 30) -> dict[str, Any]:
        """Régi nyers adatok törlése.

        Args:
            retention_days: Megtartási időtartam napokban

        Returns:
            A tisztítás eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            result = self.warehouse_manager.cleanup_old_data(
                source_path="collectors/mt5/raw", retention_days=retention_days
            )

            self.logger.info(f"Cleaned up old raw data (>{retention_days} days)")

            return result

        except Exception as e:
            error_msg = f"Error cleaning up old raw data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def get_warehouse_stats(self) -> dict[str, Any]:
        """Data Warehouse statisztikák lekérdezése.

        Returns:
            A statisztikákat tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            stats = self.warehouse_manager.get_warehouse_stats()

            return stats

        except Exception as e:
            error_msg = f"Error getting warehouse stats: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def validate_warehouse_integrity(
        self, instrument: str, timeframe: str, location: str = "warehouse/historical"
    ) -> dict[str, Any]:
        """Warehouse adatok integritásának ellenőrzése.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret
            location: Adatok helye

        Returns:
            Az ellenőrzés eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            result = self.warehouse_manager.validate_data_integrity(
                instrument=instrument, timeframe=timeframe, location=location
            )

            return result

        except Exception as e:
            error_msg = f"Error validating warehouse integrity: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def backup_warehouse_data(
        self,
        backup_name: str,
        instruments: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Warehouse adatok biztonsági mentése.

        Args:
            backup_name: Biztonsági mentés neve
            instruments: Instrumentumok listája (opcionális)
            timeframes: Időkeretek listája (opcionális)

        Returns:
            A biztonsági mentés eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            result = self.warehouse_manager.backup_data(
                source_path="warehouse",
                backup_name=backup_name,
                instruments=instruments,
                timeframes=timeframes,
            )

            self.logger.info(f"Warehouse backup created: {backup_name}")

            return result

        except Exception as e:
            error_msg = f"Error backing up warehouse data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def merge_update_to_historical(self, instrument: str, timeframe: str) -> dict[str, Any]:
        """Update adatok merge-elése historical-ba.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret

        Returns:
            A merge művelet eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            result = self.warehouse_manager.merge_update_to_historical(
                instrument=instrument, timeframe=timeframe
            )

            self.logger.info(f"Merged update to historical: {instrument} {timeframe}")

            return result

        except Exception as e:
            error_msg = f"Error merging update to historical: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def schedule_warehouse_maintenance(self) -> dict[str, Any]:
        """Warehouse karbantartási feladatok ütemezése.

        Returns:
            A karbantartás eredményét tartalmazó szótár
        """
        try:
            if not hasattr(self, "warehouse_manager"):
                return {
                    "status": "disabled",
                    "message": "Data Warehouse Manager not initialized",
                }

            results = {}

            # 1. Régi nyers adatok törlése (30 napnál régebbi)
            results["cleanup_raw"] = self.cleanup_old_raw_data(retention_days=30)

            # 2. Update adatok merge-elése historical-ba
            for instrument in self.supported_instruments:
                for timeframe in self.supported_timeframes:
                    merge_result = self.merge_update_to_historical(
                        instrument=instrument, timeframe=timeframe
                    )
                    results[f"merge_{instrument}_{timeframe}"] = merge_result

            # 3. Validált adatok szervezése
            results["organize_validated"] = self.auto_organize_validated_data()

            # 4. Integritás ellenőrzés
            integrity_results = {}
            for instrument in self.supported_instruments:
                for timeframe in self.supported_timeframes:
                    integrity_result = self.validate_warehouse_integrity(
                        instrument=instrument, timeframe=timeframe
                    )
                    integrity_results[f"{instrument}_{timeframe}"] = integrity_result

            results["integrity_check"] = integrity_results

            return {
                "status": "success",
                "message": "Warehouse maintenance completed",
                "results": results,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            error_msg = f"Error in warehouse maintenance: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)
