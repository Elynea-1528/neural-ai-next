"""ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez a modul implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import polars as pl
from loguru import logger

from neural_ai.core.base.interfaces import StorageInterface
from neural_ai.core.base.singleton import SingletonMeta


class ParquetStorageService(StorageInterface, metaclass=SingletonMeta):
    """Particionált Parquet tároló szolgáltatás.

    Ez az osztály felelős a Tick adatok particionált Parquet formátumban történő
    tárolásáért és lekérdezéséért. A particionálás dátum és szimbólum alapú,
    ami lehetővé teszi a gyors és hatékony adatlekérdezést.

    Attributes:
        BASE_PATH: A tárolás alapútvonala
        engine: A Parquet engine ('fastparquet')
        compression: Tömörítési algoritmus ('snappy')
    """

    BASE_PATH = Path("/data/tick")

    def __init__(self) -> None:
        """Inicializálja a ParquetStorageService-t.

        Beállítja a Parquet engine-t és a tömörítési algoritmust.
        """
        self.engine = "fastparquet"
        self.compression = "snappy"
        logger.info("ParquetStorageService initialized")

    def _get_path(self, symbol: str, date: datetime) -> Path:
        """Elérési út generálása a megadott szimbólumhoz és dátumhoz.

        Args:
            symbol: A pénzpár szimbóluma (pl. 'EURUSD')
            date: A dátum

        Returns:
            A teljes elérési út a Parquet fájlhoz

        Example:
            >>> service = ParquetStorageService()
            >>> date = datetime(2023, 12, 23)
            >>> path = service._get_path('EURUSD', date)
            >>> print(path)
            /data/tick/EURUSD/tick/year=2023/month=12/day=23/data.parquet
        """
        return (
            self.BASE_PATH
            / symbol.upper()
            / "tick"
            / f"year={date.year}"
            / f"month={date.month:02d}"
            / f"day={date.day:02d}"
            / "data.parquet"
        )

    async def store_tick_data(self, symbol: str, data: pl.DataFrame, date: datetime) -> None:
        """Tick adatok tárolása particionált Parquet formátumban.

        Args:
            symbol: A pénzpár szimbóluma
            data: A Tick adatokat tartalmazó Polars DataFrame
            date: A dátum, ami alapján a particionálás történik

        Raises:
            ValueError: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

        Example:
            >>> import polars as pl
            >>> from datetime import datetime
            >>>
            >>> data = pl.DataFrame({
            ...     'timestamp': [datetime.now()],
            ...     'bid': [1.1000],
            ...     'ask': [1.1002],
            ...     'volume': [1000],
            ...     'source': ['jforex']
            ... })
            >>>
            >>> service = ParquetStorageService()
            >>> await service.store_tick_data('EURUSD', data, datetime.now())
        """
        if len(data) == 0:
            raise ValueError("Cannot store empty DataFrame")

        required_columns = ["timestamp", "bid", "ask"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        path = self._get_path(symbol, date)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Polars DataFrame -> Parquet
        data.write_parquet(str(path), compression=self.compression)

        logger.info(
            "Tick data stored successfully",
            symbol=symbol,
            date=date.isoformat(),
            rows=len(data),
            path=str(path),
            size_mb=path.stat().st_size / (1024 * 1024),
        )

    async def read_tick_data(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> pl.DataFrame:
        """Tick adatok olvasása dátumtartományból.

        Args:
            symbol: A pénzpár szimbóluma
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A Tick adatokat tartalmazó Polars DataFrame

        Example:
            >>> from datetime import datetime, timedelta
            >>>
            >>> service = ParquetStorageService()
            >>> start = datetime(2023, 12, 1)
            >>> end = datetime(2023, 12, 31)
            >>>
            >>> data = await service.read_tick_data('EURUSD', start, end)
            >>> print(f"Loaded {len(data)} ticks")
        """
        paths: list[Path] = []

        # Összes releváns fájl megtalálása
        current_date = start_date
        while current_date <= end_date:
            path = self._get_path(symbol, current_date)
            if path.exists():
                paths.append(path)
            current_date += timedelta(days=1)

        if not paths:
            logger.warning(
                "No data found for date range",
                symbol=symbol,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
            return pl.DataFrame()

        # Adatok betöltése párhuzamosan
        dfs = await asyncio.gather(*[self._read_parquet_async(path) for path in paths])

        # Összefűzés
        if dfs:
            result = pl.concat(dfs)

            # Dátum szerinti szűrés (pontosabb)
            result = result.filter(
                (pl.col("timestamp") >= start_date) & (pl.col("timestamp") <= end_date)
            )
        else:
            result = pl.DataFrame()

        logger.info(
            "Tick data loaded successfully",
            symbol=symbol,
            rows=len(result),
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            files_loaded=len(paths),
        )

        return result

    async def _read_parquet_async(self, path: Path) -> pl.DataFrame:
        """Aszinkron Parquet olvasás.

        Args:
            path: A Parquet fájl elérési útja

        Returns:
            A beolvasott Polars DataFrame
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, pl.read_parquet, str(path))

    async def get_available_dates(self, symbol: str) -> list[datetime]:
        """Elérhető dátumok lekérdezése egy adott szimbólumhoz.

        Args:
            symbol: A pénzpár szimbóluma

        Returns:
            Az elérhető dátumok listája

        Example:
            >>> service = ParquetStorageService()
            >>> dates = await service.get_available_dates('EURUSD')
            >>> print(f"Available dates: {len(dates)}")
        """
        symbol_path = self.BASE_PATH / symbol.upper() / "tick"

        if not symbol_path.exists():
            return []

        dates: list[datetime] = []
        for year_dir in symbol_path.glob("year=*"):
            year = int(year_dir.name.split("=")[1])
            for month_dir in year_dir.glob("month=*"):
                month = int(month_dir.name.split("=")[1])
                for day_dir in month_dir.glob("day=*"):
                    day = int(day_dir.name.split("=")[1])
                    dates.append(datetime(year, month, day))

        return sorted(dates)

    async def calculate_checksum(self, symbol: str, date: datetime) -> str:
        """Adatok checksum számítása integritás ellenőrzéshez.

        Args:
            symbol: A pénzpár szimbóluma
            date: A dátum

        Returns:
            A checksum SHA256 hash

        Example:
            >>> service = ParquetStorageService()
            >>> checksum = await service.calculate_checksum('EURUSD', datetime.now())
            >>> print(f"Checksum: {checksum}")
        """
        path = self._get_path(symbol, date)

        if not path.exists():
            return ""

        try:
            df = pl.read_parquet(str(path))
            # Csak a fontos oszlopok alapján
            data_str = df.select(["timestamp", "bid", "ask"]).to_csv()
            return hashlib.sha256(data_str.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate checksum: {e}")
            return ""

    async def verify_data_integrity(self, symbol: str, date: datetime) -> bool:
        """Adatintegritás ellenőrzése.

        Args:
            symbol: A pénzpár szimbóluma
            date: A dátum

        Returns:
            True ha az adatok integritása megfelelő, egyébként False

        Example:
            >>> service = ParquetStorageService()
            >>> is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
            >>> print(f"Data integrity: {is_valid}")
        """
        path = self._get_path(symbol, date)

        if not path.exists():
            return False

        try:
            # Parquet fájl ellenőrzése
            df = pl.read_parquet(str(path))

            # Alapvető ellenőrzések
            assert len(df) > 0, "Empty dataframe"
            assert "timestamp" in df.columns, "Missing timestamp column"
            assert "bid" in df.columns, "Missing bid column"
            assert "ask" in df.columns, "Missing ask column"

            # Rendezés ellenőrzése
            assert df["timestamp"].is_sorted(), "Data not sorted by timestamp"

            logger.info(
                "Data integrity verified", symbol=symbol, date=date.isoformat(), rows=len(df)
            )

            return True

        except Exception as e:
            logger.error(
                "Data integrity check failed", symbol=symbol, date=date.isoformat(), error=str(e)
            )
            return False

    async def get_storage_stats(self, symbol: str | None = None) -> dict[str, Any]:
        """Tárolási statisztikák lekérdezése.

        Args:
            symbol: Opcionális szimbólum szűréshez

        Returns:
            A statisztikákat tartalmazó dictionary

        Example:
            >>> service = ParquetStorageService()
            >>> stats = await service.get_storage_stats('EURUSD')
            >>> print(f"Total files: {stats['total_files']}")
        """
        stats = {"total_files": 0, "total_size_gb": 0.0, "symbols": {}}

        base_path = self.BASE_PATH
        if symbol:
            base_path = base_path / symbol.upper()

        if not base_path.exists():
            return stats

        # Fájlok felsorolása
        for parquet_file in base_path.rglob("*.parquet"):
            stats["total_files"] += 1
            stats["total_size_gb"] += parquet_file.stat().st_size

        stats["total_size_gb"] = stats["total_size_gb"] / (1024**3)

        # Szimbólumonkénti statisztikák
        for symbol_dir in base_path.iterdir():
            if symbol_dir.is_dir():
                symbol_name = symbol_dir.name
                symbol_stats = {"files": 0, "size_gb": 0.0}

                for parquet_file in symbol_dir.rglob("*.parquet"):
                    symbol_stats["files"] += 1
                    symbol_stats["size_gb"] += parquet_file.stat().st_size

                symbol_stats["size_gb"] = symbol_stats["size_gb"] / (1024**3)
                stats["symbols"][symbol_name] = symbol_stats

        return stats
