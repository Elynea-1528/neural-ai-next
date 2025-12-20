"""Data Warehouse Manager modul.

Ez a modul felelős a Data Warehouse hierarchikus adatszervezéséért és
adatműveletekért, beleértve az adatok mozgatását, merge-elését, archiválását
és törlését a különböző mappák között.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

import json
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from neural_ai.collectors.mt5.error_handler import StorageError


class DataWarehouseManager:
    """Data Warehouse Manager osztály.

    Felelős a Data Warehouse hierarchikus adatszervezéséért:
    - historical/: 25 év állandó adat
    - update/: 3-12 hónap, évente merge-elődik
    - realtime/: Jelenlegi 30 nap
    - validated/: Minőségellenőrzött adatok
    """

    def __init__(self, base_path: str = "data", logger: logging.Logger | None = None):
        """Inicializálás.

        Args:
            base_path: Alap útvonal az adattároláshoz
            logger: Opcionális logger példány
        """
        self.base_path = Path(base_path)
        self.logger = logger or logging.getLogger(__name__)

        # Data Warehouse struktúra definíció
        self.warehouse_structure = {
            "warehouse": {
                "historical": {
                    "description": "25 év állandó adat",
                    "retention": "permanent",
                },
                "update": {
                    "description": "3-12 hónap, évente merge-elődik",
                    "retention": "1_year",
                },
                "realtime": {"description": "Jelenlegi 30 nap", "retention": "30_days"},
                "validated": {
                    "description": "Minőségellenőrzött adatok",
                    "retention": "permanent",
                },
            },
            "training": {
                "retraining": {
                    "description": "1 év, hetente frissül",
                    "retention": "permanent",
                },
                "medium": {
                    "description": "5 év, havonta frissül",
                    "retention": "permanent",
                },
                "deep_learning": {
                    "description": "25 év, évente frissül",
                    "retention": "permanent",
                },
                "validation": {
                    "description": "6 hónap, soha nem kerül tanításba",
                    "retention": "permanent",
                },
            },
        }

        # Támogatott instrumentumok és időkeretek
        self.supported_instruments = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.supported_timeframes = ["M1", "M5", "M15", "H1", "H4", "D1"]

        # Inicializálás
        self._initialize_warehouse_structure()

        self.logger.info(f"DataWarehouseManager initialized: {self.base_path}")

    def _initialize_warehouse_structure(self) -> None:
        """Data Warehouse struktúra inicializálása.

        Létrehozza a szükséges könyvtárszerkezetet, ha az nem létezik.
        """
        try:
            # Warehouse struktúra létrehozása
            for category, subdirs in self.warehouse_structure.items():
                category_path = self.base_path / category

                for subdir, _config in subdirs.items():
                    subdir_path = category_path / subdir
                    subdir_path.mkdir(parents=True, exist_ok=True)

                    # Instrumentum és timeframe mappák létrehozása
                    for instrument in self.supported_instruments:
                        instrument_path = subdir_path / instrument
                        instrument_path.mkdir(exist_ok=True)

                        # Csak warehouse mappákban hozzuk létre a timeframe mappákat
                        if category == "warehouse" and subdir in [
                            "historical",
                            "update",
                            "realtime",
                            "validated",
                        ]:
                            for timeframe in self.supported_timeframes:
                                (instrument_path / timeframe).mkdir(exist_ok=True)

            # Metadata mappa létrehozása
            metadata_path = self.base_path / "metadata"
            metadata_path.mkdir(exist_ok=True)

            # Metadata fájlok inicializálása
            self._initialize_metadata_files(metadata_path)

            self.logger.info("Data warehouse structure initialized successfully")

        except Exception as e:
            error_msg = f"Error initializing warehouse structure: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def _initialize_metadata_files(self, metadata_path: Path) -> None:
        """Metadata fájlok inicializálása.

        Args:
            metadata_path: Metadata mappa útvonala
        """
        # Instruments metadata
        instruments_file = metadata_path / "instruments.json"
        if not instruments_file.exists():
            instruments_data = {
                "EURUSD": {
                    "name": "Euro vs US Dollar",
                    "digits": 5,
                    "point": 0.00001,
                    "lot_size": 100000,
                },
                "GBPUSD": {
                    "name": "British Pound vs US Dollar",
                    "digits": 5,
                    "point": 0.00001,
                    "lot_size": 100000,
                },
                "USDJPY": {
                    "name": "US Dollar vs Japanese Yen",
                    "digits": 3,
                    "point": 0.001,
                    "lot_size": 100000,
                },
                "XAUUSD": {
                    "name": "Gold vs US Dollar",
                    "digits": 2,
                    "point": 0.01,
                    "lot_size": 100,
                },
            }
            with open(instruments_file, "w", encoding="utf-8") as f:
                json.dump(instruments_data, f, indent=2)

        # Timeframes metadata
        timeframes_file = metadata_path / "timeframes.json"
        if not timeframes_file.exists():
            timeframes_data = {
                "M1": {"name": "1 Minute", "minutes": 1},
                "M5": {"name": "5 Minutes", "minutes": 5},
                "M15": {"name": "15 Minutes", "minutes": 15},
                "H1": {"name": "1 Hour", "minutes": 60},
                "H4": {"name": "4 Hours", "minutes": 240},
                "D1": {"name": "1 Day", "minutes": 1440},
            }
            with open(timeframes_file, "w", encoding="utf-8") as f:
                json.dump(timeframes_data, f, indent=2)

        # Data quality metadata
        quality_file = metadata_path / "data_quality.json"
        if not quality_file.exists():
            quality_data = {
                "last_updated": datetime.now().isoformat(),
                "quality_metrics": {},
            }
            with open(quality_file, "w", encoding="utf-8") as f:
                json.dump(quality_data, f, indent=2)

        # Collection jobs metadata
        jobs_file = metadata_path / "collection_jobs.json"
        if not jobs_file.exists():
            jobs_data = {"last_updated": datetime.now().isoformat(), "jobs": {}}
            with open(jobs_file, "w", encoding="utf-8") as f:
                json.dump(jobs_data, f, indent=2)

        # Training datasets metadata
        datasets_file = metadata_path / "training_datasets.json"
        if not datasets_file.exists():
            datasets_data = {"last_updated": datetime.now().isoformat(), "datasets": {}}
            with open(datasets_file, "w", encoding="utf-8") as f:
                json.dump(datasets_data, f, indent=2)

        # Gaps metadata
        gaps_file = metadata_path / "gaps.json"
        if not gaps_file.exists():
            gaps_data = {"last_updated": datetime.now().isoformat(), "gaps": []}
            with open(gaps_file, "w", encoding="utf-8") as f:
                json.dump(gaps_data, f, indent=2)

    def move_data(
        self,
        source_path: str,
        destination_path: str,
        instrument: str,
        timeframe: str | None = None,
    ) -> dict[str, Any]:
        """Adatok mozgatása a különböző mappák között.

        Args:
            source_path: Forrás útvonal (pl. 'warehouse/realtime')
            destination_path: Cél útvonal (pl. 'warehouse/update')
            instrument: Instrumentum szimbólum
            timeframe: Időkeret (opcionális)

        Returns:
            A művelet eredményét tartalmazó szótár
        """
        try:
            # Útvonalak ellenőrzése
            source_dir = self.base_path / source_path / instrument
            dest_dir = self.base_path / destination_path / instrument

            if timeframe:
                source_dir = source_dir / timeframe
                dest_dir = dest_dir / timeframe

            if not source_dir.exists():
                raise StorageError(f"Source directory does not exist: {source_dir}")

            dest_dir.mkdir(parents=True, exist_ok=True)

            # Fájlok mozgatása
            moved_files = []
            for file_path in source_dir.iterdir():
                if file_path.is_file():
                    dest_file = dest_dir / file_path.name
                    shutil.move(str(file_path), str(dest_file))
                    moved_files.append(file_path.name)

            result = {
                "status": "success",
                "message": f"Data moved from {source_path} to {destination_path}",
                "instrument": instrument,
                "timeframe": timeframe,
                "files_moved": moved_files,
                "files_count": len(moved_files),
            }

            self.logger.info(
                f"Moved {len(moved_files)} files for {instrument} "
                f"{timeframe or ''} from {source_path} to {destination_path}"
            )

            return result

        except Exception as e:
            error_msg = f"Error moving data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def merge_update_to_historical(self, instrument: str, timeframe: str) -> dict[str, Any]:
        """Update mappa adatainak merge-elése a historical mappába.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret

        Returns:
            A merge művelet eredményét tartalmazó szótár
        """
        try:
            update_dir = self.base_path / "warehouse" / "update" / instrument / timeframe
            historical_dir = self.base_path / "warehouse" / "historical" / instrument / timeframe

            if not update_dir.exists():
                return {
                    "status": "no_data",
                    "message": f"No update data found for {instrument} {timeframe}",
                }

            # Update fájlok betöltése
            update_dataframes = []
            for file_path in update_dir.glob("*.parquet"):
                try:
                    df = pd.read_parquet(file_path)
                    update_dataframes.append(df)
                except Exception as e:
                    self.logger.warning(f"Error reading {file_path}: {e}")

            if not update_dataframes:
                return {
                    "status": "no_data",
                    "message": "No valid data found in update directory",
                }

            # Összesített update adatok
            update_df = pd.concat(update_dataframes, ignore_index=True)
            update_df = update_df.drop_duplicates(subset=["time"], keep="last")
            update_df = update_df.sort_values("time")

            # Historical fájl betöltése
            historical_file = historical_dir / f"{instrument}_{timeframe}_2000_2025.parquet"

            if historical_file.exists():
                # Meglévő adatok betöltése és merge
                historical_df = pd.read_parquet(historical_file)

                # Duplikátumok eltávolítása és merge
                combined_df = pd.concat([historical_df, update_df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=["time"], keep="last")
                combined_df = combined_df.sort_values("time")
            else:
                combined_df = update_df

            # Mentés
            combined_df.to_parquet(
                historical_file, engine="fastparquet", compression="snappy", index=False
            )

            # Update mappa kiürítése
            for file_path in update_dir.glob("*.parquet"):
                file_path.unlink()

            result = {
                "status": "success",
                "message": "Update data merged to historical",
                "instrument": instrument,
                "timeframe": timeframe,
                "historical_records": len(combined_df),
                "update_records": len(update_df),
                "merged_at": datetime.now().isoformat(),
            }

            self.logger.info(
                f"Merged update data to historical for {instrument} {timeframe}: "
                f"{len(update_df)} records added"
            )

            return result

        except Exception as e:
            error_msg = f"Error merging update to historical: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def archive_data(
        self,
        source_path: str,
        archive_name: str,
        instrument: str,
        timeframe: str | None = None,
    ) -> dict[str, Any]:
        """Adatok archiválása.

        Args:
            source_path: Forrás útvonal
            archive_name: Archívum neve
            instrument: Instrumentum szimbólum
            timeframe: Időkeret (opcionális)

        Returns:
            Az archiválás eredményét tartalmazó szótár
        """
        try:
            source_dir = self.base_path / source_path / instrument
            if timeframe:
                source_dir = source_dir / timeframe

            if not source_dir.exists():
                raise StorageError(f"Source directory does not exist: {source_dir}")

            # Archívum mappa létrehozása
            archive_dir = self.base_path / "archive" / archive_name / instrument
            if timeframe:
                archive_dir = archive_dir / timeframe
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Fájlok másolása
            archived_files = []
            for file_path in source_dir.iterdir():
                if file_path.is_file():
                    dest_file = archive_dir / file_path.name
                    shutil.copy2(str(file_path), str(dest_file))
                    archived_files.append(file_path.name)

            result = {
                "status": "success",
                "message": f"Data archived to {archive_name}",
                "instrument": instrument,
                "timeframe": timeframe,
                "files_archived": archived_files,
                "files_count": len(archived_files),
                "archive_path": str(archive_dir),
            }

            self.logger.info(
                f"Archived {len(archived_files)} files for {instrument} "
                f"{timeframe or ''} to {archive_name}"
            )

            return result

        except Exception as e:
            error_msg = f"Error archiving data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def cleanup_old_data(self, source_path: str, retention_days: int = 30) -> dict[str, Any]:
        """Régi adatok törlése.

        Args:
            source_path: Forrás útvonal
            retention_days: Megtartási időtartam napokban

        Returns:
            A tisztítás eredményét tartalmazó szótár
        """
        try:
            source_dir = self.base_path / source_path

            if not source_dir.exists():
                return {
                    "status": "no_data",
                    "message": f"Source directory does not exist: {source_dir}",
                }

            cutoff_date = datetime.now() - timedelta(days=retention_days)
            deleted_files = []

            # Rekurzív fájl keresés
            for file_path in source_dir.rglob("*.parquet"):
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)

                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        deleted_files.append(str(file_path.relative_to(self.base_path)))
                    except Exception as e:
                        self.logger.warning(f"Error deleting {file_path}: {e}")

            result = {
                "status": "success",
                "message": f"Cleaned up old data (>{retention_days} days)",
                "deleted_files": deleted_files,
                "files_count": len(deleted_files),
                "cutoff_date": cutoff_date.isoformat(),
            }

            self.logger.info(f"Cleaned up {len(deleted_files)} old files from {source_path}")

            return result

        except Exception as e:
            error_msg = f"Error cleaning up old data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def get_warehouse_stats(self) -> dict[str, Any]:
        """Data Warehouse statisztikák lekérdezése.

        Returns:
            A statisztikákat tartalmazó szótár
        """
        try:
            stats = {
                "timestamp": datetime.now().isoformat(),
                "warehouse": {},
                "training": {},
                "total_size_bytes": 0,
                "total_files": 0,
            }

            # Warehouse statisztikák
            for category in ["warehouse", "training"]:
                category_path = self.base_path / category

                if not category_path.exists():
                    continue

                for subdir in category_path.iterdir():
                    if subdir.is_dir():
                        subdir_stats = self._calculate_directory_stats(subdir)
                        stats[category][subdir.name] = subdir_stats
                        stats["total_size_bytes"] += subdir_stats["size_bytes"]
                        stats["total_files"] += subdir_stats["file_count"]

            # Méret formázása
            stats["total_size_gb"] = stats["total_size_bytes"] / (1024**3)
            stats["total_size_mb"] = stats["total_size_bytes"] / (1024**2)

            return stats

        except Exception as e:
            error_msg = f"Error getting warehouse stats: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def _calculate_directory_stats(self, directory: Path) -> dict[str, Any]:
        """Könyvtár statisztikáinak kiszámítása.

        Args:
            directory: Könyvtár útvonala

        Returns:
            A statisztikákat tartalmazó szótár
        """
        file_count = 0
        size_bytes = 0
        instruments = {}
        timeframes = {}

        for file_path in directory.rglob("*"):
            if file_path.is_file():
                file_count += 1
                size_bytes += file_path.stat().st_size

                # Instrumentum és timeframe statisztikák
                for instrument in self.supported_instruments:
                    if instrument in file_path.name:
                        instruments[instrument] = instruments.get(instrument, 0) + 1

                for timeframe in self.supported_timeframes:
                    if timeframe in file_path.name:
                        timeframes[timeframe] = timeframes.get(timeframe, 0) + 1

        return {
            "file_count": file_count,
            "size_bytes": size_bytes,
            "size_mb": size_bytes / (1024**2),
            "size_gb": size_bytes / (1024**3),
            "instruments": instruments,
            "timeframes": timeframes,
        }

    def validate_data_integrity(
        self, instrument: str, timeframe: str, location: str = "warehouse/historical"
    ) -> dict[str, Any]:
        """Adatintegritás ellenőrzése.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret
            location: Adatok helye

        Returns:
            Az ellenőrzés eredményét tartalmazó szótár
        """
        try:
            data_dir = self.base_path / location / instrument / timeframe

            if not data_dir.exists():
                return {
                    "status": "no_data",
                    "message": f"No data found at {location}/{instrument}/{timeframe}",
                }

            issues = []
            warnings = []

            # Parquet fájlok ellenőrzése
            for file_path in data_dir.glob("*.parquet"):
                try:
                    df = pd.read_parquet(file_path)

                    # Alapvető ellenőrzések
                    if df.empty:
                        issues.append(f"Empty file: {file_path.name}")
                        continue

                    # Kötelező oszlopok ellenőrzése
                    required_columns = [
                        "time",
                        "open",
                        "high",
                        "low",
                        "close",
                        "volume",
                    ]
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        issues.append(f"Missing columns in {file_path.name}: {missing_columns}")
                        continue

                    # Duplikátumok ellenőrzése
                    duplicates = df.duplicated(subset=["time"]).sum()
                    if duplicates > 0:
                        warnings.append(
                            f"Found {duplicates} duplicate timestamps in {file_path.name}"
                        )

                    # Idősor rendezettség ellenőrzése
                    if not df["time"].is_monotonic_increasing:
                        warnings.append(f"Timestamps not sorted in {file_path.name}")

                    # Érvénytelen értékek ellenőrzése
                    null_count = df[required_columns].isnull().sum().sum()
                    if null_count > 0:
                        issues.append(f"Found {null_count} null values in {file_path.name}")

                except Exception as e:
                    issues.append(f"Error reading {file_path.name}: {str(e)}")

            result = {
                "status": "completed",
                "instrument": instrument,
                "timeframe": timeframe,
                "location": location,
                "issues_found": len(issues),
                "warnings_found": len(warnings),
                "issues": issues,
                "warnings": warnings,
                "is_valid": len(issues) == 0,
            }

            if issues:
                self.logger.warning(
                    f"Data integrity check found {len(issues)} issues for {instrument} {timeframe}"
                )
            else:
                self.logger.info(f"Data integrity check passed for {instrument} {timeframe}")

            return result

        except Exception as e:
            error_msg = f"Error validating data integrity: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def backup_data(
        self,
        source_path: str,
        backup_name: str,
        instruments: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Adatok biztonsági mentése.

        Args:
            source_path: Forrás útvonal
            backup_name: Biztonsági mentés neve
            instruments: Instrumentumok listája (opcionális)
            timeframes: Időkeretek listája (opcionális)

        Returns:
            A biztonsági mentés eredményét tartalmazó szótár
        """
        try:
            source_dir = self.base_path / source_path
            backup_dir = self.base_path / "backup" / backup_name

            if not source_dir.exists():
                raise StorageError(f"Source directory does not exist: {source_dir}")

            backup_dir.mkdir(parents=True, exist_ok=True)

            # Szűrés instrumentumokra és időkeretekre
            target_instruments = instruments or self.supported_instruments
            target_timeframes = timeframes or self.supported_timeframes

            backed_up_files = []

            for instrument in target_instruments:
                instrument_source = source_dir / instrument

                if not instrument_source.exists():
                    continue

                for timeframe in target_timeframes:
                    timeframe_source = instrument_source / timeframe

                    if not timeframe_source.exists():
                        continue

                    # Cél útvonal létrehozása
                    backup_instrument = backup_dir / instrument / timeframe
                    backup_instrument.mkdir(parents=True, exist_ok=True)

                    # Fájlok másolása
                    for file_path in timeframe_source.glob("*"):
                        if file_path.is_file():
                            dest_file = backup_instrument / file_path.name
                            shutil.copy2(str(file_path), str(dest_file))
                            backed_up_files.append(str(file_path))

            result = {
                "status": "success",
                "message": f"Backup created: {backup_name}",
                "backup_path": str(backup_dir),
                "files_backed_up": len(backed_up_files),
                "instruments": target_instruments,
                "timeframes": target_timeframes,
            }

            self.logger.info(f"Created backup {backup_name} with {len(backed_up_files)} files")

            return result

        except Exception as e:
            error_msg = f"Error creating backup: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def restore_data(
        self,
        backup_name: str,
        target_path: str,
        instruments: list[str] | None = None,
        timeframes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Adatok visszaállítása biztonsági mentésből.

        Args:
            backup_name: Biztonsági mentés neve
            target_path: Cél útvonal
            instruments: Instrumentumok listája (opcionális)
            timeframes: Időkeretek listája (opcionális)

        Returns:
            A visszaállítás eredményét tartalmazó szótár
        """
        try:
            backup_dir = self.base_path / "backup" / backup_name
            target_dir = self.base_path / target_path

            if not backup_dir.exists():
                raise StorageError(f"Backup does not exist: {backup_dir}")

            target_dir.mkdir(parents=True, exist_ok=True)

            # Szűrés instrumentumokra és időkeretekre
            target_instruments = instruments or self.supported_instruments
            target_timeframes = timeframes or self.supported_timeframes

            restored_files = []

            for instrument in target_instruments:
                backup_instrument = backup_dir / instrument

                if not backup_instrument.exists():
                    continue

                for timeframe in target_timeframes:
                    backup_timeframe = backup_instrument / timeframe

                    if not backup_timeframe.exists():
                        continue

                    # Cél útvonal létrehozása
                    target_instrument = target_dir / instrument / timeframe
                    target_instrument.mkdir(parents=True, exist_ok=True)

                    # Fájlok másolása
                    for file_path in backup_timeframe.glob("*"):
                        if file_path.is_file():
                            dest_file = target_instrument / file_path.name
                            shutil.copy2(str(file_path), str(dest_file))
                            restored_files.append(str(file_path))

            result = {
                "status": "success",
                "message": f"Data restored from backup: {backup_name}",
                "restored_to": target_path,
                "files_restored": len(restored_files),
                "instruments": target_instruments,
                "timeframes": target_timeframes,
            }

            self.logger.info(f"Restored {len(restored_files)} files from backup {backup_name}")

            return result

        except Exception as e:
            error_msg = f"Error restoring data: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def get_data_location(
        self, instrument: str, timeframe: str, data_type: str = "historical"
    ) -> Path:
        """Adatok helyének lekérdezése.

        Args:
            instrument: Instrumentum szimbólum
            timeframe: Időkeret
            data_type: Adattípus (historical, update, realtime, validated)

        Returns:
            Az adatok útvonala
        """
        if data_type not in ["historical", "update", "realtime", "validated"]:
            raise ValueError(f"Invalid data type: {data_type}")

        return self.base_path / "warehouse" / data_type / instrument / timeframe
