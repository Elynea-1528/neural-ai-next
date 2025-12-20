"""Training Dataset Generator modul.

Ez a modul felelős a különböző típusú tanulási adathalmazok generálásáért:
- Retraining Dataset: 1 év, heti frissítés
- Medium Dataset: 5 év, havi frissítés
- Deep Learning Dataset: 25 év, évi frissítés
- Validation Dataset: 6 hónap, soha nem kerül tanításba

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from dateutil.relativedelta import relativedelta

from neural_ai.collectors.mt5.error_handler import StorageError
from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
    DataWarehouseManager,
)


class TrainingDatasetGenerator:
    """Training Dataset Generator osztály.

    Felelős a tanulási adathalmazok generálásáért és kezeléséért.
    """

    def __init__(
        self,
        warehouse_manager: DataWarehouseManager,
        logger: logging.Logger | None = None,
    ):
        """Inicializálás.

        Args:
            warehouse_manager: DataWarehouseManager példány
            logger: Opcionális logger példány
        """
        self.warehouse_manager = warehouse_manager
        self.logger = logger or logging.getLogger(__name__)

        # Adathalmaz típusok konfigurációja
        self.dataset_types = {
            "retraining": {
                "description": "1 év, hetente frissül (gyors rátanuláshoz)",
                "years": 1,
                "update_frequency": "weekly",
                "use_case": "Rapid model adaptation, short-term pattern learning",
            },
            "medium": {
                "description": "5 év, havonta frissül (közepes tanuláshoz)",
                "years": 5,
                "update_frequency": "monthly",
                "use_case": "Medium-term pattern learning, production model training",
            },
            "deep_learning": {
                "description": "25 év, évente frissül (mélytanuláshoz)",
                "years": 25,
                "update_frequency": "yearly",
                "use_case": "Long-term pattern learning, deep neural network training",
            },
            "validation": {
                "description": "6 hónap, soha nem kerül tanításba",
                "months": 6,
                "update_frequency": "weekly",
                "use_case": "Model validation, backtesting, performance evaluation",
                "never_in_training": True,
            },
        }

        # Támogatott instrumentumok és időkeretek
        self.supported_instruments = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self.supported_timeframes = ["M1", "M5", "M15", "H1", "H4", "D1"]

        self.logger.info("TrainingDatasetGenerator initialized")

    def generate_dataset(
        self,
        dataset_type: str,
        symbols: list[str],
        timeframes: list[str],
        end_date: str | None = None,
        quality_threshold: float = 0.95,
        output_format: str = "parquet",
    ) -> dict[str, Any]:
        """Tanulási adathalmaz generálása.

        Args:
            dataset_type: Adathalmaz típusa (retraining, medium, deep_learning, validation)
            symbols: Instrumentumok listája
            timeframes: Időkeretek listája
            end_date: Befejezési dátum (opcionális, alapértelmezett: mai dátum)
            quality_threshold: Minimális minőségi küszöb
            output_format: Kimeneti formátum (parquet, csv)

        Returns:
            A generálás eredményét tartalmazó szótár
        """
        try:
            # Érvényesség ellenőrzés
            if dataset_type not in self.dataset_types:
                raise ValueError(f"Invalid dataset type: {dataset_type}")

            # Dátumok beállítása
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")

            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            dataset_config = self.dataset_types[dataset_type]

            # Kezdő dátum kiszámítása
            if "years" in dataset_config:
                start_dt = end_dt - relativedelta(years=dataset_config["years"])
            else:
                start_dt = end_dt - relativedelta(months=dataset_config["months"])

            start_date = start_dt.strftime("%Y-%m-%d")

            # Dataset ID generálás
            dataset_id = f"dataset_{dataset_type}_{start_dt.year}_{end_dt.year}"

            self.logger.info(f"Generating {dataset_type} dataset: {start_date} to {end_date}")

            # Adatok gyűjtése
            collected_data = {}
            total_records = 0

            for symbol in symbols:
                if symbol not in self.supported_instruments:
                    self.logger.warning(f"Unsupported instrument: {symbol}")
                    continue

                for timeframe in timeframes:
                    if timeframe not in self.supported_timeframes:
                        self.logger.warning(f"Unsupported timeframe: {timeframe}")
                        continue

                    # Adatok betöltése a warehouse-ból
                    try:
                        data = self._load_data_from_warehouse(
                            symbol=symbol,
                            timeframe=timeframe,
                            start_date=start_date,
                            end_date=end_date,
                        )

                        if data is not None and not data.empty:
                            # Minőségi szűrés
                            filtered_data = self._apply_quality_filters(
                                data=data, min_quality_score=quality_threshold
                            )

                            if not filtered_data.empty:
                                collected_data[f"{symbol}_{timeframe}"] = filtered_data
                                total_records += len(filtered_data)

                                self.logger.debug(
                                    f"Loaded {len(filtered_data)} records for {symbol} {timeframe}"
                                )

                    except Exception as e:
                        self.logger.error(f"Error loading data for {symbol} {timeframe}: {e}")

            if not collected_data:
                return {
                    "status": "no_data",
                    "message": "No valid data found for dataset generation",
                    "dataset_id": dataset_id,
                }

            # Adathalmaz mentése
            output_path = self._save_dataset(
                dataset_type=dataset_type,
                dataset_id=dataset_id,
                data=collected_data,
                output_format=output_format,
            )

            # Metadata mentése
            metadata = self._create_dataset_metadata(
                dataset_id=dataset_id,
                dataset_type=dataset_type,
                start_date=start_date,
                end_date=end_date,
                symbols=symbols,
                timeframes=timeframes,
                total_records=total_records,
                quality_threshold=quality_threshold,
            )

            self._save_dataset_metadata(dataset_id, metadata)

            result = {
                "status": "success",
                "message": "Training dataset generated successfully",
                "dataset_id": dataset_id,
                "dataset_type": dataset_type,
                "date_range": {"start": start_date, "end": end_date},
                "instruments": symbols,
                "timeframes": timeframes,
                "total_records": total_records,
                "output_path": str(output_path),
                "metadata": metadata,
            }

            self.logger.info(
                f"Dataset {dataset_id} generated successfully: {total_records} records"
            )

            return result

        except Exception as e:
            error_msg = f"Error generating dataset: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def _load_data_from_warehouse(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame | None:
        """Adatok betöltése a warehouse-ból.

        Args:
            symbol: Instrumentum szimbólum
            timeframe: Időkeret
            start_date: Kezdő dátum
            end_date: Befejezési dátum

        Returns:
            DataFrame az adatokkal vagy None
        """
        try:
            # Historical adatok betöltése
            historical_path = self.warehouse_manager.get_data_location(
                instrument=symbol, timeframe=timeframe, data_type="historical"
            )

            # Update adatok betöltése
            update_path = self.warehouse_manager.get_data_location(
                instrument=symbol, timeframe=timeframe, data_type="update"
            )

            dataframes = []

            # Historical fájl betöltése
            historical_file = historical_path / f"{symbol}_{timeframe}_2000_2025.parquet"
            if historical_file.exists():
                try:
                    df_historical = pd.read_parquet(historical_file)

                    # Dátum szűrés
                    df_historical["timestamp"] = pd.to_datetime(df_historical["time"], unit="s")
                    df_filtered = df_historical[
                        (df_historical["timestamp"] >= start_date)
                        & (df_historical["timestamp"] <= end_date)
                    ]

                    if not df_filtered.empty:
                        dataframes.append(df_filtered)

                except Exception as e:
                    self.logger.warning(f"Error reading historical file: {e}")

            # Update fájlok betöltése
            for update_file in update_path.glob("*.parquet"):
                try:
                    df_update = pd.read_parquet(update_file)

                    # Dátum szűrés
                    df_update["timestamp"] = pd.to_datetime(df_update["time"], unit="s")
                    df_filtered = df_update[
                        (df_update["timestamp"] >= start_date)
                        & (df_update["timestamp"] <= end_date)
                    ]

                    if not df_filtered.empty:
                        dataframes.append(df_filtered)

                except Exception as e:
                    self.logger.warning(f"Error reading update file {update_file}: {e}")

            if not dataframes:
                return None

            # Összesítés
            combined_df = pd.concat(dataframes, ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=["time"], keep="last")
            combined_df = combined_df.sort_values("time")

            return combined_df

        except Exception as e:
            self.logger.error(f"Error loading data from warehouse: {e}")
            return None

    def _apply_quality_filters(
        self, data: pd.DataFrame, min_quality_score: float = 0.95
    ) -> pd.DataFrame:
        """Minőségi szűrők alkalmazása.

        Args:
            data: Bemeneti DataFrame
            min_quality_score: Minimális minőségi küszöb

        Returns:
            Szűrt DataFrame
        """
        try:
            filtered_data = data.copy()

            # Hiányzó értékek eltávolítása
            filtered_data = filtered_data.dropna()

            # Duplikátumok eltávolítása
            filtered_data = filtered_data.drop_duplicates(subset=["time"], keep="last")

            # Idősor rendezés
            filtered_data = filtered_data.sort_values("time")

            # Alapvető validáció
            # OHLC ellenőrzés
            invalid_mask = (
                (filtered_data["high"] < filtered_data["low"])
                | (filtered_data["open"] > filtered_data["high"])
                | (filtered_data["open"] < filtered_data["low"])
                | (filtered_data["close"] > filtered_data["high"])
                | (filtered_data["close"] < filtered_data["low"])
                | (filtered_data["volume"] < 0)
            )

            filtered_data = filtered_data[~invalid_mask]

            # Minőségi pontszám számítása
            quality_score = len(filtered_data) / len(data) if len(data) > 0 else 0

            if quality_score < min_quality_score:
                self.logger.warning(
                    f"Quality score {quality_score:.2f} below threshold {min_quality_score}"
                )

            return filtered_data

        except Exception as e:
            self.logger.error(f"Error applying quality filters: {e}")
            return data

    def _save_dataset(
        self,
        dataset_type: str,
        dataset_id: str,
        data: dict[str, pd.DataFrame],
        output_format: str = "parquet",
    ) -> Path:
        """Adathalmaz mentése.

        Args:
            dataset_type: Adathalmaz típusa
            dataset_id: Adathalmaz azonosító
            data: Adatok szótára
            output_format: Kimeneti formátum

        Returns:
            A mentési útvonal
        """
        try:
            # Kimeneti mappa létrehozása
            output_dir = self.warehouse_manager.base_path / "training" / dataset_type
            output_dir.mkdir(parents=True, exist_ok=True)

            # Fájlok mentése
            for key, df in data.items():
                symbol, timeframe = key.split("_", 1)

                # Instrumentum mappa létrehozása
                instrument_dir = output_dir / symbol
                instrument_dir.mkdir(exist_ok=True)

                # Fájlnév generálás
                filename = f"{symbol}_{timeframe}_{dataset_type}.{output_format}"
                filepath = instrument_dir / filename

                # Mentés
                if output_format == "parquet":
                    df.to_parquet(
                        filepath,
                        engine="fastparquet",
                        compression="snappy",
                        index=False,
                    )
                elif output_format == "csv":
                    df.to_csv(filepath, index=False)
                else:
                    raise ValueError(f"Unsupported output format: {output_format}")

                self.logger.debug(f"Saved dataset file: {filepath}")

            return output_dir

        except Exception as e:
            error_msg = f"Error saving dataset: {e}"
            self.logger.error(error_msg)
            raise StorageError(error_msg)

    def _create_dataset_metadata(
        self,
        dataset_id: str,
        dataset_type: str,
        start_date: str,
        end_date: str,
        symbols: list[str],
        timeframes: list[str],
        total_records: int,
        quality_threshold: float,
    ) -> dict[str, Any]:
        """Adathalmaz metadata létrehozása.

        Args:
            dataset_id: Adathalmaz azonosító
            dataset_type: Adathalmaz típusa
            start_date: Kezdő dátum
            end_date: Befejezési dátum
            symbols: Instrumentumok listája
            timeframes: Időkeretek listája
            total_records: Összes rekordok száma
            quality_threshold: Minőségi küszöb

        Returns:
            Metadata szótár
        """
        dataset_config = self.dataset_types[dataset_type]

        metadata = {
            "dataset_id": dataset_id,
            "dataset_type": dataset_type,
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "date_range": {"start": start_date, "end": end_date},
            "instruments": symbols,
            "timeframes": timeframes,
            "quality_threshold": quality_threshold,
            "total_records": total_records,
            "description": dataset_config["description"],
            "update_frequency": dataset_config["update_frequency"],
            "use_case": dataset_config["use_case"],
            "features": [
                "timestamp",
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "symbol",
                "timeframe",
            ],
            "quality_notes": [
                "Missing values removed",
                "Duplicates removed",
                "Basic OHLC validation applied",
            ],
            "usage_notes": [],
        }

        if dataset_config.get("never_in_training"):
            metadata["usage_notes"].append(
                "NEVER use this dataset for training - only for validation and backtesting"
            )

        return metadata

    def _save_dataset_metadata(self, dataset_id: str, metadata: dict[str, Any]) -> None:
        """Adathalmaz metadata mentése.

        Args:
            dataset_id: Adathalmaz azonosító
            metadata: Metadata szótár
        """
        try:
            # Metadata mappa
            metadata_dir = self.warehouse_manager.base_path / "metadata"
            metadata_dir.mkdir(exist_ok=True)

            # Fájl mentése
            metadata_file = metadata_dir / f"{dataset_id}_metadata.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            # Training datasets metadata frissítése
            datasets_file = metadata_dir / "training_datasets.json"

            if datasets_file.exists():
                with open(datasets_file, encoding="utf-8") as f:
                    datasets_data = json.load(f)
            else:
                datasets_data = {
                    "last_updated": datetime.now().isoformat(),
                    "datasets": {},
                }

            datasets_data["datasets"][dataset_id] = metadata
            datasets_data["last_updated"] = datetime.now().isoformat()

            with open(datasets_file, "w", encoding="utf-8") as f:
                json.dump(datasets_data, f, indent=2)

            self.logger.debug(f"Saved metadata for dataset: {dataset_id}")

        except Exception as e:
            self.logger.error(f"Error saving dataset metadata: {e}")

    def get_dataset_status(self, dataset_id: str) -> dict[str, Any]:
        """Adathalmaz állapotának lekérdezése.

        Args:
            dataset_id: Adathalmaz azonosító

        Returns:
            Az adathalmaz állapotát tartalmazó szótár
        """
        try:
            # Metadata betöltése
            metadata_file = (
                self.warehouse_manager.base_path / "metadata" / f"{dataset_id}_metadata.json"
            )

            if not metadata_file.exists():
                return {
                    "status": "not_found",
                    "message": f"Dataset {dataset_id} not found",
                }

            with open(metadata_file, encoding="utf-8") as f:
                metadata = json.load(f)

            # Fájlok ellenőrzése
            dataset_type = metadata["dataset_type"]
            output_dir = self.warehouse_manager.base_path / "training" / dataset_type

            files_found = []
            total_size_bytes = 0

            for instrument in metadata["instruments"]:
                instrument_dir = output_dir / instrument

                if instrument_dir.exists():
                    for file_path in instrument_dir.glob(f"*_{dataset_type}.*"):
                        files_found.append(str(file_path))
                        total_size_bytes += file_path.stat().st_size

            result = {
                "status": "completed",
                "dataset_id": dataset_id,
                "dataset_type": dataset_type,
                "files": files_found,
                "total_size_bytes": total_size_bytes,
                "total_size_gb": total_size_bytes / (1024**3),
                "created_at": metadata["created_at"],
                "date_range": metadata["date_range"],
                "instruments": metadata["instruments"],
                "timeframes": metadata["timeframes"],
                "total_records": metadata["total_records"],
            }

            return result

        except Exception as e:
            error_msg = f"Error getting dataset status: {e}"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def list_datasets(self, dataset_type: str | None = None) -> dict[str, Any]:
        """Elérhető adathalmazok listázása.

        Args:
            dataset_type: Adathalmaz típusa (opcionális szűréshez)

        Returns:
            Az adathalmazokat tartalmazó szótár
        """
        try:
            # Metadata betöltése
            datasets_file = self.warehouse_manager.base_path / "metadata" / "training_datasets.json"

            if not datasets_file.exists():
                return {"status": "no_datasets", "message": "No datasets found"}

            with open(datasets_file, encoding="utf-8") as f:
                datasets_data = json.load(f)

            datasets = datasets_data["datasets"]

            # Szűrés adathalmaz típusra
            if dataset_type:
                datasets = {k: v for k, v in datasets.items() if v["dataset_type"] == dataset_type}

            result = {
                "status": "success",
                "total_datasets": len(datasets),
                "datasets": datasets,
                "last_updated": datasets_data["last_updated"],
            }

            return result

        except Exception as e:
            error_msg = f"Error listing datasets: {e}"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def get_dataset_info(self) -> dict[str, Any]:
        """Adathalmaz típusok információinak lekérdezése.

        Returns:
            Az adathalmaz típusok információit tartalmazó szótár
        """
        return {
            "status": "success",
            "dataset_types": self.dataset_types,
            "supported_instruments": self.supported_instruments,
            "supported_timeframes": self.supported_timeframes,
        }
