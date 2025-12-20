"""Historical Data Manager for MT5 Collector.
==========================================

Ez a modul implementálja a historikus adatgyűjtés Python backendjét az MT5 Collector komponensben.

Felelősségek:
- Historikus adatkérések kezelése
- Job követés és státusz kezelés
- Adatok fogadása és validálása
- Adathézagok azonosítása
- Data Warehouse-ba történő tárolás

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

import json
import logging
import os
import sqlite3
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import HTTPException

from neural_ai.collectors.mt5.data_validator import DataValidator
from neural_ai.collectors.mt5.error_handler import (
    CollectorError,
    ErrorHandler,
    StorageError,
)
from neural_ai.collectors.mt5.implementations.storage.collector_storage import (
    CollectorStorage,
)


class HistoricalJobStatus(Enum):
    """Historikus adatgyűjtési job státuszok enumja."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class HistoricalJob:
    """Historikus adatgyűjtési feladat reprezentációja.

    Attribútumok:
        job_id: Egyedi job azonosító
        symbol: Pénznem szimbólum (pl. EURUSD)
        timeframe: Időkeret (pl. M1, H1)
        start_date: Kezdő dátum (ISO formátumban)
        end_date: Végdátum (ISO formátumban)
        batch_size: Kötegenkénti napok száma
        priority: Prioritás (low, normal, high)
        status: Job státusz
        progress: Haladás százalékban
        total_batches: Összes köteg száma
        completed_batches: Elkészült kötegek száma
        current_batch: Jelenlegi köteg száma
        errors: Hibaüzenetek listája
        warnings: Figyelmeztetések listája
        created_at: Létrehozás időpontja
        started_at: Indulás időpontja
        completed_at: Befejezés időpontja
        estimated_duration: Becsült időtartam
    """

    job_id: str
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    batch_size: int = 99000
    priority: str = "normal"
    status: HistoricalJobStatus = HistoricalJobStatus.QUEUED
    progress: float = 0.0
    total_batches: int = 0
    completed_batches: int = 0
    current_batch: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str | None = None
    completed_at: str | None = None
    estimated_duration: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Konvertálás szótárrá."""
        data = asdict(self)
        data["status"] = self.status.value
        return data

    def calculate_progress(self) -> float:
        """Haladás kiszámítása."""
        if self.total_batches == 0:
            return 0.0
        return round((self.completed_batches / self.total_batches) * 100, 2)


class HistoricalDataManager:
    """Fő historikus adatkezelő osztály.

    Felelősségek:
        - Historikus adatkérések kezelése
        - Job követés és státusz kezelés
        - Adatok fogadása és validálása
        - Adathézagok azonosítása
        - Data Warehouse-ba történő tárolás
    """

    def __init__(
        self,
        storage: CollectorStorage,
        validator: DataValidator,
        error_handler: ErrorHandler,
        logger: logging.Logger | None = None,
        db_path: str | None = None,
    ):
        """Inicializálás.

        Args:
            storage: CollectorStorage példány
            validator: DataValidator példány
            error_handler: ErrorHandler példány
            logger: Logger példány
            db_path: SQLite adatbázis elérési útja
        """
        self.storage = storage
        self.validator = validator
        self.error_handler = error_handler
        self.logger = logger or logging.getLogger(__name__)

        # Job tárolás (memóriában és/vagy SQLite-ben)
        self.jobs: dict[str, HistoricalJob] = {}
        self.db_path = db_path or "data/collectors/mt5/historical_jobs.db"
        self._init_database()

        # Szálbiztonság
        self._lock = threading.RLock()

        self.logger.info(f"{self.__class__.__name__} initialized")

    def _init_database(self) -> None:
        """Adatbázis inicializálása."""
        try:
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS historical_jobs (
                        job_id TEXT PRIMARY KEY,
                        symbol TEXT NOT NULL,
                        timeframe TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        batch_size INTEGER NOT NULL,
                        priority TEXT NOT NULL,
                        status TEXT NOT NULL,
                        progress REAL NOT NULL,
                        total_batches INTEGER NOT NULL,
                        completed_batches INTEGER NOT NULL,
                        current_batch INTEGER NOT NULL,
                        errors TEXT,
                        warnings TEXT,
                        created_at TEXT NOT NULL,
                        started_at TEXT,
                        completed_at TEXT,
                        estimated_duration TEXT
                    )
                """
                )
                conn.commit()

            self.logger.info(f"Database initialized: {self.db_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise StorageError(f"Database initialization failed: {e}")

    def request_historical_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str,
        end_date: str,
        batch_size: int = 99000,
        priority: str = "normal",
    ) -> dict[str, Any]:
        """Historikus adatkérés létrehozása.

        Args:
            symbol: Pénznem szimbólum
            timeframe: Időkeret
            start_date: Kezdő dátum (ISO formátum)
            end_date: Végdátum (ISO formátum)
            batch_size: Kötegenkénti napok száma
            priority: Prioritás (low, normal, high)

        Returns:
            Job információval tér vissza
        """
        try:
            # Validáció
            if not symbol:
                raise ValueError("Invalid symbol")

            if not timeframe:
                raise ValueError("Invalid timeframe")

            # Dátum validáció
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

            if start_dt >= end_dt:
                raise ValueError("Start date must be before end date")

            if batch_size <= 0:
                raise ValueError("Batch size must be positive")

            # Job létrehozása
            job_id = f"job_{uuid.uuid4().hex[:8]}"

            # Kötegek számának kiszámítása
            date_range_days = (end_dt - start_dt).days
            total_batches = (date_range_days + batch_size - 1) // batch_size

            # Becsült időtartam kiszámítása (átlagosan 5 perc per köteg)
            estimated_minutes = total_batches * 5
            if estimated_minutes < 60:
                estimated_duration = f"{estimated_minutes} minutes"
            else:
                estimated_duration = (
                    f"{estimated_minutes // 60} hours {estimated_minutes % 60} minutes"
                )

            job = HistoricalJob(
                job_id=job_id,
                symbol=symbol.upper(),
                timeframe=str(timeframe).upper(),
                start_date=start_date,
                end_date=end_date,
                batch_size=batch_size,
                priority=priority,
                status=HistoricalJobStatus.QUEUED,
                total_batches=total_batches,
                estimated_duration=estimated_duration,
            )

            # Mentés
            with self._lock:
                self.jobs[job_id] = job
                self._save_job_to_db(job)

            self.logger.info(
                f"Historical data job created: {job_id} "
                f"({symbol} {timeframe} from {start_date} to {end_date})"
            )

            # TODO: Küldés az MT5 EA-nak
            # self._send_request_to_ea(job)

            return {
                "job_id": job_id,
                "status": job.status.value,
                "estimated_duration": estimated_duration,
                "total_batches": total_batches,
                "message": "Historical data collection job created",
            }

        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            error = CollectorError(f"Failed to create historical data job: {e}")
            self.error_handler.handle_error(error)
            raise HTTPException(status_code=500, detail=str(e))

    def get_job_status(self, job_id: str) -> dict[str, Any]:
        """Job státusz lekérdezése.

        Args:
            job_id: Job azonosító

        Returns:
            Job státusz információ
        """
        try:
            with self._lock:
                job = self.jobs.get(job_id)
                if not job:
                    # Próbáljuk betölteni az adatbázisból
                    job = self._load_job_from_db(job_id)
                    if job:
                        self.jobs[job_id] = job

            if not job:
                raise HTTPException(status_code=404, detail="Job not found")

            # Haladás frissítése
            job.progress = job.calculate_progress()

            return {
                "job_id": job.job_id,
                "status": job.status.value,
                "progress": {
                    "completed_batches": job.completed_batches,
                    "total_batches": job.total_batches,
                    "percentage": job.progress,
                },
                "current_batch": {
                    "batch_number": job.current_batch,
                    "date_range": self._get_batch_date_range(job, job.current_batch),
                },
                "errors": job.errors,
                "warnings": job.warnings,
                "started_at": job.started_at,
                "estimated_completion": self._estimate_completion_time(job),
            }

        except HTTPException:
            raise
        except Exception as e:
            error = CollectorError(f"Failed to get job status: {e}")
            self.error_handler.handle_error(error)
            raise HTTPException(status_code=500, detail=str(e))

    def save_historical_data(self, job_id: str, data: dict[str, Any]) -> bool:
        """Historikus adatok mentése a helyes mappába.

        Args:
            job_id: Job azonosító
            data: Adatok szótára

        Returns:
            True ha sikeres, False ha sikertelen
        """
        try:
            # Job adatok lekérdezése
            job = self.get_job(job_id)
            if not job:
                self.logger.error(f"Job not found: {job_id}")
                return False

            symbol = job["symbol"]
            timeframe = job["timeframe"]

            # HELYES ÚTVONAL: data/warehouse/historical/
            base_path = "data/warehouse/historical"
            symbol_path = os.path.join(base_path, symbol)
            timeframe_path = os.path.join(symbol_path, timeframe)

            # Mappa létrehozása, ha nem létezik
            os.makedirs(timeframe_path, exist_ok=True)

            # Fájl neve: {start_date}_{end_date}.parquet
            start_date = job["start_date"].replace("-", "_")
            end_date = job["end_date"].replace("-", "_")
            filename = f"{start_date}_{end_date}.parquet"
            filepath = os.path.join(timeframe_path, filename)

            # Adatok konvertálása DataFrame-be
            import pandas as pd

            # Ellenőrizzük, hogy van-e adat
            if not data.get("bars") or len(data["bars"]) == 0:
                self.logger.warning(f"No bars to save for job {job_id}")
                return False

            bars = data["bars"]
            df = pd.DataFrame(bars)

            # Időbélyeg konvertálása
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)

            # Tárolás Parquet formátumban
            df.to_parquet(filepath, compression="snappy")

            self.logger.info(f"✅ Adatok elmentve: {filepath}")
            self.logger.info(f"   - {len(df)} bar")
            self.logger.info(f"   - {df['timestamp'].min()} - {df['timestamp'].max()}")

            # Job státusz frissítése completed-re
            self.update_job_status(job_id, "completed")

            # Job törlése a pending listából
            self.delete_job(job_id)
            self.logger.info(f"✅ Job törölve: {job_id}")

            return True

        except Exception as e:
            self.logger.error(f"Error saving historical data: {e}")
            return False

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        """Job lekérdezése."""
        with self._lock:
            job = self.jobs.get(job_id)
            if not job:
                job = self._load_job_from_db(job_id)
            if job:
                return job.to_dict()
        return None

    def update_job_status(self, job_id: str, status: str) -> bool:
        """Job státusz frissítése."""
        try:
            with self._lock:
                job = self.jobs.get(job_id)
                if not job:
                    job = self._load_job_from_db(job_id)
                if job:
                    job.status = HistoricalJobStatus(status)
                    self._save_job_to_db(job)
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating job status: {e}")
            return False

    def delete_job(self, job_id: str) -> bool:
        """Job törlése."""
        try:
            with self._lock:
                # Törlés a memóriából
                if job_id in self.jobs:
                    del self.jobs[job_id]

                # Törlés az adatbázisból
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("DELETE FROM historical_jobs WHERE job_id = ?", (job_id,))
                    conn.commit()

                return True
        except Exception as e:
            self.logger.error(f"Error deleting job: {e}")
            return False

    def collect_historical_data(
        self,
        job_id: str,
        batch_number: int,
        symbol: str,
        timeframe: str | int,
        date_range: dict[str, str],
        bars: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Historikus adatok fogadása az EA-tól.

        Args:
            job_id: Job azonosító
            batch_number: Köteg száma
            symbol: Pénznem szimbólum
            timeframe: Időkeret
            date_range: Dátumtartomány
            bars: OHLCV sorok listája

        Returns:
            Fogadás eredménye
        """
        job: HistoricalJob | None = None
        try:
            with self._lock:
                job = self.jobs.get(job_id)
                if not job:
                    job = self._load_job_from_db(job_id)
                    if job:
                        self.jobs[job_id] = job

            if not job:
                raise HTTPException(status_code=404, detail="Job not found")

            # Job státusz frissítése
            if job.status == HistoricalJobStatus.QUEUED:
                job.status = HistoricalJobStatus.IN_PROGRESS
                job.started_at = datetime.now().isoformat()

            # Adatok validálása
            valid_bars: list[dict[str, Any]] = []
            invalid_bars: list[dict[str, Any]] = []

            for bar in bars:
                # Szimbólum és időkeret hozzáadása
                bar["symbol"] = symbol
                # Konvertáljuk az időkeretet string-re, ha integer
                timeframe_str = str(timeframe) if isinstance(timeframe, int) else timeframe
                bar["timeframe"] = self._convert_timeframe_to_int(timeframe_str)

                # Validáció
                validation_result = self.validator.validate_ohlcv(bar)

                if validation_result.is_valid:
                    valid_bars.append(bar)
                else:
                    invalid_bars.append(bar)

                    # Hiba tárolása
                    self.storage.store_invalid_data(
                        data=bar,
                        data_type="ohlcv",
                        reason="; ".join(validation_result.errors),
                    )

            # Érvényes adatok mentése a HELYES mappába
            if valid_bars:
                ohlcv_data: dict[str, Any] = {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "bars": valid_bars,
                    "timestamp": int(datetime.now().timestamp()),
                }

                # Mentés a helyes útvonalra
                self.save_historical_data(job_id, ohlcv_data)

            # Job frissítése
            job.completed_batches = batch_number
            job.current_batch = batch_number + 1
            job.progress = job.calculate_progress()

            # Hibák és figyelmeztetések hozzáadása
            if invalid_bars:
                job.warnings.append(f"Batch {batch_number}: {len(invalid_bars)} invalid bars found")

            # Ellenőrizzük, hogy a job befejeződött-e
            if job.completed_batches >= job.total_batches:
                job.status = HistoricalJobStatus.COMPLETED
                job.completed_at = datetime.now().isoformat()

            # Mentés
            with self._lock:
                self._save_job_to_db(job)

            self.logger.info(
                f"Historical data batch received: {job_id} batch {batch_number} "
                f"({len(valid_bars)} valid, {len(invalid_bars)} invalid bars)"
            )

            return {
                "status": "success",
                "batch_number": batch_number,
                "bars_received": len(bars),
                "bars_stored": len(valid_bars),
                "message": "Batch stored successfully",
            }

        except HTTPException:
            raise
        except Exception as e:
            error = StorageError(f"Failed to collect historical data: {e}")
            self.error_handler.handle_error(error)

            # Hiba hozzáadása a job-hoz
            if job:
                job.errors.append(str(e))
                job.status = HistoricalJobStatus.FAILED
                with self._lock:
                    self._save_job_to_db(job)

            raise HTTPException(status_code=500, detail=str(e))

    def identify_data_gaps(
        self,
        symbol: str | None = None,
        timeframe: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Adathézagok azonosítása.

        Args:
            symbol: Pénznem szimbólum (opcionális)
            timeframe: Időkeret (opcionális)
            start_date: Kezdő dátum (opcionális)
            end_date: Végdátum (opcionális)

        Returns:
            Hézagok listája és elemzés
        """
        try:
            # Alapértelmezett dátumtartomány
            if not end_date:
                end_date = datetime.now().isoformat()
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).isoformat()

            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

            # Szimbólumok és időkeretek beállítása
            symbols = [symbol] if symbol else self.storage.supported_instruments
            timeframes = (
                [timeframe] if timeframe else list(self.storage.supported_timeframes.keys())
            )

            all_gaps: list[dict[str, Any]] = []
            total_missing_bars = 0

            # Hézagok keresése minden szimbólumra és időkeretre
            for sym in symbols:
                for tf in timeframes:
                    gaps = self._find_gaps_for_symbol_timeframe(sym, tf, start_dt, end_dt)
                    all_gaps.extend(gaps)
                    total_missing_bars += sum(gap["missing_bars"] for gap in gaps)

            return {
                "analysis_period": {"start": start_date, "end": end_date},
                "gaps": all_gaps,
                "total_gaps": len(all_gaps),
                "total_missing_bars": total_missing_bars,
            }

        except Exception as e:
            error = CollectorError(f"Failed to identify data gaps: {e}")
            self.error_handler.handle_error(error)
            raise HTTPException(status_code=500, detail=str(e))

    def _find_gaps_for_symbol_timeframe(
        self, symbol: str, timeframe: str, start_dt: datetime, end_dt: datetime
    ) -> list[dict[str, Any]]:
        """Hézagok keresése adott szimbólumra és időkeretre.

        Args:
            symbol: Pénznem szimbólum
            timeframe: Időkeret
            start_dt: Kezdő dátum
            end_dt: Végdátum

        Returns:
            Hézagok listája
        """
        gaps: list[dict[str, Any]] = []

        try:
            # Adatok betöltése a warehouse-ból
            warehouse_path = self.storage.get_data_warehouse_path(
                symbol=symbol, timeframe=timeframe, data_type="validated"
            )

            # Parquet fájl keresése
            parquet_file = warehouse_path / f"{symbol}_{timeframe}_ohlcv.parquet"

            if not parquet_file.exists():
                # Ha nincs adat, az egész tartomány hiányzik
                gaps.append(
                    {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                        "duration_minutes": int((end_dt - start_dt).total_seconds() / 60),
                        "missing_bars": int((end_dt - start_dt).total_seconds() / 60),
                    }
                )
                return gaps

            # Adatok betöltése
            df = pd.read_parquet(parquet_file, engine="fastparquet")

            if df.empty:
                return gaps

            # Időbélyegek rendezése
            df = df.sort_values("time")

            # Időkeret percekben
            tf_minutes = self._get_timeframe_minutes(timeframe)

            # Hézagok keresése
            for i in range(len(df) - 1):
                current_time = pd.to_datetime(df.iloc[i]["time"], unit="s")
                next_time = pd.to_datetime(df.iloc[i + 1]["time"], unit="s")

                expected_time = current_time + timedelta(minutes=tf_minutes)

                # Ha a következő időbélyeg nagyobb, mint az elvárt, akkor van hézag
                if next_time > expected_time + timedelta(minutes=tf_minutes):
                    gap_start = expected_time
                    gap_end = next_time - timedelta(minutes=tf_minutes)

                    gap_duration = (gap_end - gap_start).total_seconds() / 60
                    missing_bars = int(gap_duration / tf_minutes)

                    if missing_bars > 0:
                        gaps.append(
                            {
                                "symbol": symbol,
                                "timeframe": timeframe,
                                "start": gap_start.isoformat(),
                                "end": gap_end.isoformat(),
                                "duration_minutes": int(gap_duration),
                                "missing_bars": missing_bars,
                            }
                        )

        except Exception as e:
            self.logger.warning(f"Error finding gaps for {symbol} {timeframe}: {e}")

        return gaps

    def _save_job_to_db(self, job: HistoricalJob) -> None:
        """Job mentése adatbázisba."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO historical_jobs (
                        job_id, symbol, timeframe, start_date, end_date,
                        batch_size, priority, status, progress, total_batches,
                        completed_batches, current_batch, errors, warnings,
                        created_at, started_at, completed_at, estimated_duration
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        job.job_id,
                        job.symbol,
                        job.timeframe,
                        job.start_date,
                        job.end_date,
                        job.batch_size,
                        job.priority,
                        job.status.value,
                        job.progress,
                        job.total_batches,
                        job.completed_batches,
                        job.current_batch,
                        json.dumps(job.errors),
                        json.dumps(job.warnings),
                        job.created_at,
                        job.started_at,
                        job.completed_at,
                        job.estimated_duration,
                    ),
                )
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to save job to database: {e}")

    def _load_job_from_db(self, job_id: str) -> HistoricalJob | None:
        """Job betöltése adatbázisból."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT * FROM historical_jobs WHERE job_id = ?", (job_id,))
                row = cursor.fetchone()

                if row:
                    job = HistoricalJob(
                        job_id=row[0],
                        symbol=row[1],
                        timeframe=row[2],
                        start_date=row[3],
                        end_date=row[4],
                        batch_size=row[5],
                        priority=row[6],
                        status=HistoricalJobStatus(row[7]),
                        progress=row[8],
                        total_batches=row[9],
                        completed_batches=row[10],
                        current_batch=row[11],
                        errors=json.loads(row[12]) if row[12] else [],
                        warnings=json.loads(row[13]) if row[13] else [],
                        created_at=row[14],
                        started_at=row[15],
                        completed_at=row[16],
                        estimated_duration=row[17],
                    )
                    return job
        except Exception as e:
            self.logger.error(f"Failed to load job from database: {e}")

        return None

    def _get_batch_date_range(self, job: HistoricalJob, batch_number: int) -> str:
        """Köteg dátumtartományának lekérdezése."""
        try:
            start_dt = datetime.fromisoformat(job.start_date.replace("Z", "+00:00"))
            batch_start = start_dt + timedelta(days=(batch_number - 1) * job.batch_size)
            batch_end = min(
                batch_start + timedelta(days=job.batch_size),
                datetime.fromisoformat(job.end_date.replace("Z", "+00:00")),
            )
            return f"{batch_start.date()} to {batch_end.date()}"
        except Exception:
            return "Unknown"

    def _estimate_completion_time(self, job: HistoricalJob) -> str | None:
        """Befejezési idő becslése."""
        if job.status != HistoricalJobStatus.IN_PROGRESS:
            return None

        if job.completed_batches == 0 or not job.started_at:
            return None

        try:
            started_at = datetime.fromisoformat(job.started_at.replace("Z", "+00:00"))
            elapsed = (datetime.now() - started_at).total_seconds()

            if job.completed_batches > 0:
                time_per_batch = elapsed / job.completed_batches
                remaining_batches = job.total_batches - job.completed_batches
                remaining_time = time_per_batch * remaining_batches

                completion_time = datetime.now() + timedelta(seconds=remaining_time)
                return completion_time.isoformat()
        except Exception:
            pass

        return None

    def _convert_timeframe_to_int(self, timeframe: str) -> int:
        """Időkeret konvertálása int-re."""
        timeframe_map = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "H1": 16385,
            "H4": 16388,
            "D1": 16408,
        }
        return timeframe_map.get(timeframe.upper(), 16385)

    def _get_timeframe_minutes(self, timeframe: str) -> int:
        """Időkeret percekben."""
        timeframe_map = {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}
        return timeframe_map.get(timeframe.upper(), 60)

    def auto_start_historical_collection(self) -> dict[str, Any]:
        """Automatikus historikus adatgyűjtés indítása.

        Ellenőrzi, hogy vannak-e historikus adatok, és ha nincsenek,
        automatikusan elindítja a historikus adatgyűjtést minden
        támogatott instrumentumra és időkeretre.

        Returns:
            Indítási eredményekkel tér vissza
        """
        try:
            self.logger.info("Auto-start historikus adatgyűjtés ellenőrzése...")

            # Adatok ellenőrzése a Data Warehouse-ban
            missing_data = self._check_missing_historical_data()

            if not missing_data:
                self.logger.info("Minden historikus adat megtalálható, nincs szükség auto-startra")
                return {
                    "status": "no_action",
                    "message": "All historical data already exists",
                    "jobs_created": 0,
                }

            # Historikus job-ok létrehozása a hiányzó adatokra
            jobs_created = []

            for item in missing_data:
                self.logger.info(
                    f"Hiányzó historikus adatok: {item['symbol']} {item['timeframe']} "
                    f"({item['start_date']} - {item['end_date']})"
                )

                # Job létrehozása
                job_result = self.request_historical_data(
                    symbol=item["symbol"],
                    timeframe=item["timeframe"],
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                    batch_size=365,  # Alapértelmezett kötegméret
                    priority="normal",
                )

                jobs_created.append(job_result)

            self.logger.info(
                f"Auto-start historikus adatgyűjtés indítva: {len(jobs_created)} job létrehozva"
            )

            return {
                "status": "started",
                "message": f"Historical data collection started for {len(jobs_created)} instrument/timeframe combinations",
                "jobs_created": jobs_created,
                "total_jobs": len(jobs_created),
            }

        except Exception as e:
            error = CollectorError(f"Failed to auto-start historical collection: {e}")
            self.error_handler.handle_error(error)
            self.logger.error(f"Auto-start historikus adatgyűjtés sikertelen: {e}")

            return {"status": "error", "message": str(e), "jobs_created": []}

    def _check_missing_historical_data(self) -> list[dict[str, str]]:
        """Hiányzó historikus adatok ellenőrzése.

        Returns:
            Hiányzó adatok listája
        """
        missing_data = []

        try:
            # Alapértelmezett dátumtartomány (5 év)
            end_date = datetime.now().isoformat()
            start_date = (datetime.now() - timedelta(days=5 * 365)).isoformat()

            # Támogatott instrumentumok és időkeretek
            symbols = self.storage.supported_instruments
            timeframes = list(self.storage.supported_timeframes.keys())

            self.logger.debug(
                f"Hiányzó adatok ellenőrzése: {len(symbols)} instrumentum, {len(timeframes)} időkeret"
            )

            # Minden instrumentum/timeframe kombináció ellenőrzése
            for symbol in symbols:
                for timeframe in timeframes:
                    # Adatok ellenőrzése a warehouse-ban
                    warehouse_path = self.storage.get_data_warehouse_path(
                        symbol=symbol, timeframe=timeframe, data_type="validated"
                    )

                    # Parquet fájl ellenőrzése
                    parquet_file = warehouse_path / f"{symbol}_{timeframe}_ohlcv.parquet"

                    if not parquet_file.exists():
                        # Ha nincs adat, hozzáadjuk a hiányzókhoz
                        missing_data.append(
                            {
                                "symbol": symbol,
                                "timeframe": timeframe,
                                "start_date": start_date,
                                "end_date": end_date,
                                "reason": "no_data_file",
                            }
                        )
                    else:
                        # Ha van fájl, ellenőrizzük, hogy van-e benne adat
                        try:
                            import pandas as pd

                            df = pd.read_parquet(parquet_file, engine="fastparquet")

                            if df.empty or len(df) < 100:  # Kevesebb mint 100 sor
                                missing_data.append(
                                    {
                                        "symbol": symbol,
                                        "timeframe": timeframe,
                                        "start_date": start_date,
                                        "end_date": end_date,
                                        "reason": "insufficient_data",
                                        "current_rows": len(df),
                                    }
                                )
                        except Exception as e:
                            self.logger.warning(
                                f"Hiba a {symbol} {timeframe} adatfájl ellenőrzésénél: {e}"
                            )
                            missing_data.append(
                                {
                                    "symbol": symbol,
                                    "timeframe": timeframe,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "reason": "file_error",
                                }
                            )

        except Exception as e:
            self.logger.error(f"Hiba a hiányzó adatok ellenőrzésénél: {e}")

        return missing_data

    def start_historical_collection_for_all_instruments(self) -> dict[str, Any]:
        """Historikus adatgyűjtés indítása minden instrumentumra és időkeretre.

        Ez a metódus létrehozza a historikus job-okat az összes támogatott
        instrumentumra és időkeretre az elmúlt 5 év adataira.

        Returns:
            Indítási eredményekkel tér vissza
        """
        try:
            self.logger.info("Historikus adatgyűjtés indítása minden instrumentumra...")

            # Alapértelmezett dátumtartomány (5 év)
            end_date = datetime.now().isoformat()
            start_date = (datetime.now() - timedelta(days=5 * 365)).isoformat()

            # Támogatott instrumentumok és időkeretek
            symbols = self.storage.supported_instruments
            timeframes = list(self.storage.supported_timeframes.keys())

            jobs_created = []

            self.logger.info(
                f"Job-ok létrehozása: {len(symbols)} instrumentum × {len(timeframes)} időkeret"
            )

            # Job-ok létrehozása minden kombinációra
            for symbol in symbols:
                for timeframe in timeframes:
                    self.logger.debug(f"Job létrehozása: {symbol} {timeframe}")

                    job_result = self.request_historical_data(
                        symbol=symbol,
                        timeframe=timeframe,
                        start_date=start_date,
                        end_date=end_date,
                        batch_size=365,
                        priority="normal",
                    )

                    jobs_created.append(job_result)

            self.logger.info(f"Historikus adatgyűjtés indítva: {len(jobs_created)} job létrehozva")

            return {
                "status": "started",
                "message": f"Historical data collection started for {len(jobs_created)} combinations",
                "jobs_created": jobs_created,
                "total_jobs": len(jobs_created),
                "date_range": {"start": start_date, "end": end_date},
            }

        except Exception as e:
            error = CollectorError(f"Failed to start historical collection: {e}")
            self.error_handler.handle_error(error)
            self.logger.error(f"Historikus adatgyűjtés indítása sikertelen: {e}")

            return {"status": "error", "message": str(e), "jobs_created": []}

    def get_pending_jobs(self, limit: int = 1) -> list[dict[str, Any]]:
        """Lekérdezi a legrégebbi függőben lévő (pending/queued) historikus job-okat.

        Args:
            limit: Maximum ennyi job-ot ad vissza (alapértelmezett: 1)

        Returns:
            Függőben lévő job-ok listája
        """
        try:
            pending_jobs = []

            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT job_id, symbol, timeframe, start_date, end_date,
                           batch_size, priority, status, progress, total_batches,
                           completed_batches, current_batch, created_at
                    FROM historical_jobs
                    WHERE status = 'queued' OR status = 'pending'
                    ORDER BY created_at ASC
                    LIMIT ?
                    """,
                    (limit,),
                )

                rows = cursor.fetchall()

                for row in rows:
                    job_dict = {
                        "job_id": row["job_id"],
                        "symbol": row["symbol"],
                        "timeframe": row["timeframe"],
                        "start_date": row["start_date"],
                        "end_date": row["end_date"],
                        "batch_size": row["batch_size"],
                        "priority": row["priority"],
                        "status": row["status"],
                        "progress": row["progress"],
                        "total_batches": row["total_batches"],
                        "completed_batches": row["completed_batches"],
                        "current_batch": row["current_batch"],
                        "created_at": row["created_at"],
                    }
                    pending_jobs.append(job_dict)

            self.logger.info(f"Függőben lévő job-ok lekérdezve: {len(pending_jobs)} db")

            return pending_jobs

        except Exception as e:
            self.logger.error(f"Hiba a függőben lévő job-ok lekérdezésekor: {e}")
            return []
