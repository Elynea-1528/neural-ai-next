"""ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez a modul implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb
backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

Author: Neural AI Next Team
Version: 2.0.0
"""

import asyncio
import hashlib
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import structlog

from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.storage.exceptions import StorageError, StorageIOError, StorageNotFoundError
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.backends.base import StorageBackend
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


logger = structlog.get_logger()


class ParquetStorageService(StorageInterface, metaclass=SingletonMeta):
    """Particionált Parquet tároló szolgáltatás backend selectorral.

    Ez az osztály felelős a Tick adatok particionált Parquet formátumban történő
    tárolásáért és lekérdezéséért. A particionálás dátum és szimbólum alapú,
    ami lehetővé teszi a gyors és hatékony adatlekérdezést.

    A szolgáltatás automatikusan detektálja a hardver képességeket és kiválasztja
    a legoptimálisabb tárolási backend-et:
    - PolarsBackend: AVX2 támogatással gyorsabb feldolgozás
    - PandasBackend: Kompatibilitási mód régebbi CPU-khoz

    Attributes:
        BASE_PATH: A tárolás alapútvonala
        engine: A Parquet engine ('fastparquet' vagy 'polars')
        compression: Tömörítési algoritmus ('snappy')
        backend: A kiválasztott tárolási backend
    """

    def __init__(
        self,
        base_path: str | Path | None = None,
        compression: str = "snappy",
        hardware: "HardwareInterface | None" = None,
        logger: "LoggerInterface | None" = None,  # <--- EZ HIÁNYZOTT
        **kwargs: Any,                            # <--- ÉS EZ A BIZTONSÁGÉRT
    ) -> None:
        """Inicializálja a ParquetStorageService-t backend selectorral.

        A hardver detekció alapján kiválasztja a megfelelő tárolási backend-et.
        Ha az AVX2 utasításkészlet elérhető, a PolarsBackend-et használja,
        egyébként a PandasBackend-et kompatibilitási módban.

        Args:
            base_path: Az alapútvonal a tároláshoz (opcionális)
            compression: A tömörítési algoritmus (alapértelmezett: 'snappy')
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális)
            logger: A naplózásért felelős interfész (opcionális)
            **kwargs: További opcionális paraméterek
        """
        self.BASE_PATH = Path(base_path) if base_path else Path("/data/tick")
        self.engine = "fastparquet"
        self.compression = compression
        self.backend: StorageBackend
        self.logger = logger  # <--- Elmentjük

        # Dependency Injection a HardwareInterface-hez
        if hardware is None:
            from neural_ai.core.utils.factory import HardwareFactory

            self.hardware = HardwareFactory.get_hardware_interface()
        else:
            self.hardware = hardware

        # Hardver detekció és backend kiválasztás
        self._select_backend()
        
        # Logolás a saját loggerrel (ha van), vagy a globálissal
        log_msg = f"ParquetStorageService initialized with {self.backend.name} backend"
        if self.logger:
            self.logger.info(log_msg)
        else:
            structlog.get_logger().info(log_msg)

    def _select_backend(self) -> None:
        """Backend kiválasztása hardver detekció alapján.

        Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért
        a hardver képességek alapján. Külön metódusba van kiszervezve,
        hogy a tesztek könnyen mockolhassák.
        """
        if self.hardware.has_avx2():
            from neural_ai.core.storage.backends.polars_backend import PolarsBackend

            self.backend = PolarsBackend()
            self.engine = "polars"
            logger.info(
                "AVX2 support detected. Using PolarsBackend for accelerated data processing."
            )
        else:
            from neural_ai.core.storage.backends.pandas_backend import PandasBackend

            self.backend = PandasBackend()
            self.engine = "fastparquet"
            logger.warning("Legacy CPU detected. Running in Compatibility Mode with PandasBackend.")

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

    async def store_tick_data(self, symbol: str, data: Any, date: datetime) -> None:
        """Tick adatok tárolása particionált Parquet formátumban.

        Args:
            symbol: A pénzpár szimbóluma
            data: A Tick adatokat tartalmazó DataFrame
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

        # Adatok tárolása a kiválasztott backend-en keresztül
        self.backend.write(data, str(path), compression=self.compression)

        logger.info(
            "Tick data stored successfully",
            symbol=symbol,
            date=date.isoformat(),
            rows=len(data),
            path=str(path),
            size_mb=path.stat().st_size / (1024 * 1024),
            backend=self.backend.name,
        )

    async def read_tick_data(self, symbol: str, start_date: datetime, end_date: datetime) -> Any:
        """Tick adatok olvasása dátumtartományból.

        Args:
            symbol: A pénzpár szimbóluma
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A Tick adatokat tartalmazó DataFrame

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
            # Üres DataFrame visszaadása a backend típusának megfelelően
            if self.engine == "polars":
                import polars as pl

                return pl.DataFrame()
            else:
                import pandas as pd

                return pd.DataFrame()

        # Adatok betöltése párhuzamosan a backend-en keresztül
        dfs = await asyncio.gather(*[self._read_parquet_async(path) for path in paths])

        # Összefűzés
        if dfs:
            result = self._concat_dataframes(dfs)

            # Dátum szerinti szűrés (pontosabb)
            result = self._filter_by_timestamp(result, start_date, end_date)
        else:
            if self.engine == "polars":
                import polars as pl

                result = pl.DataFrame()
            else:
                import pandas as pd

                result = pd.DataFrame()

        logger.info(
            "Tick data loaded successfully",
            symbol=symbol,
            rows=len(result),
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            files_loaded=len(paths),
            backend=self.backend.name,
        )

        return result

    async def _read_parquet_async(self, path: Path) -> Any:
        """Aszinkron Parquet olvasás.

        Args:
            path: A Parquet fájl elérési útja

        Returns:
            A beolvasott DataFrame
        """
        loop = asyncio.get_event_loop()
        return cast(
            "pd.DataFrame | pl.DataFrame",
            await loop.run_in_executor(None, self.backend.read, str(path)),
        )

    def _concat_dataframes(self, dfs: list[Any]) -> Any:
        """DataFrame-ek összefűzése a backend típusának megfelelően.

        Args:
            dfs: Az összefűzendő DataFrame-ek listája

        Returns:
            Az összefűzött DataFrame
        """
        if self.engine == "polars":
            import polars as pl

            return pl.concat(dfs)
        else:
            import pandas as pd

            return pd.concat(dfs, ignore_index=True)

    def _filter_by_timestamp(
        self,
        data: Any,
        start_date: datetime,
        end_date: datetime,
    ) -> Any:
        """DataFrame szűrése időbélyeg alapján.

        Args:
            data: A szűrendő DataFrame
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A szűrt DataFrame
        """
        if self.engine == "polars":
            import polars as pl

            pl_data = cast(pl.DataFrame, data)
            # A filter metódus a Polars DataFrame-et adja vissza
            return pl_data.filter(
                (pl.col("timestamp") >= start_date) & (pl.col("timestamp") <= end_date)
            )
        else:
            import pandas as pd

            pd_data = cast(pd.DataFrame, data)
            # A pandas filter más, itt a boolean indexelést használjuk
            mask = (pd_data["timestamp"] >= start_date) & (pd_data["timestamp"] <= end_date)
            return pd_data[mask]

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
            df = self.backend.read(str(path))
            # Csak a fontos oszlopok alapján
            if self.engine == "polars":
                import polars as pl

                pl_df = cast(pl.DataFrame, df)
                data_str = pl_df.select(["timestamp", "bid", "ask"]).write_csv()
            else:
                import pandas as pd

                pd_df = cast(pd.DataFrame, df)
                data_str = pd_df[["timestamp", "bid", "ask"]].to_csv(index=False)
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
            # Parquet fájl ellenőrzése a backend-en keresztül
            df = self.backend.read(str(path))

            # Alapvető ellenőrzések
            assert len(df) > 0, "Empty dataframe"
            assert "timestamp" in df.columns, "Missing timestamp column"
            assert "bid" in df.columns, "Missing bid column"
            assert "ask" in df.columns, "Missing ask column"

            # Rendezés ellenőrzése
            if self.engine == "polars":
                import polars as pl

                pl_df = cast(pl.DataFrame, df)
                # Egyszerűbb ellenőrzés: csak azt nézzük, hogy a timestamp oszlop monoton növekvő-e
                # A Polars Series-nek nincs is_monotonic_increasing property-je, ezért
                # összehasonlítjuk az eredetit a rendezett változattal
                sorted_timestamp = pl_df["timestamp"].sort()
                is_sorted = (pl_df["timestamp"] == sorted_timestamp).all()
                assert is_sorted, "Data not sorted by timestamp"
            else:
                import pandas as pd

                pd_df = cast(pd.DataFrame, df)
                assert pd_df["timestamp"].is_monotonic_increasing, "Data not sorted by timestamp"

            logger.info(
                "Data integrity verified",
                symbol=symbol,
                date=date.isoformat(),
                rows=len(df),
                backend=self.backend.name,
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

    # --- StorageInterface Implementáció ---

    def save_dataframe(self, df: "pd.DataFrame", path: str, **kwargs: Any) -> None:
        """DataFrame mentése a megadott útvonalra.
        
        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        A ParquetStorageService saját store_tick_data metódusát használja.
        """
        from datetime import datetime
        
        # Alapértelmezett dátum a mai nap
        date = kwargs.get('date', datetime.now())
        symbol = kwargs.get('symbol', 'DEFAULT')
        
        # Aszinkron hívás szinkron wrapper-ben
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Ha már fut egy loop, akkor task-ként indítjuk
                task = loop.create_task(self.store_tick_data(symbol, df, date))
                # Várakozás a task befejezésére
                while not task.done():
                    pass
            else:
                # Ha nincs futó loop, akkor futtatjuk
                loop.run_until_complete(self.store_tick_data(symbol, df, date))
        except RuntimeError:
            # Ha nincs event loop, létrehozunk egyet
            asyncio.run(self.store_tick_data(symbol, df, date))

    def load_dataframe(self, path: str, **kwargs: Any) -> "pd.DataFrame":
        """DataFrame betöltése a megadott útvonalról.
        
        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        from datetime import datetime, timedelta
        
        # Dátumtartomány kinyerése a path-ból vagy kwargs-ból
        start_date = kwargs.get('start_date', datetime.now() - timedelta(days=1))
        end_date = kwargs.get('end_date', datetime.now())
        symbol = kwargs.get('symbol', 'DEFAULT')
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Ha már fut egy loop, akkor task-ként indítjuk
                task = loop.create_task(self.read_tick_data(symbol, start_date, end_date))
                # Várakozás a task befejezésére
                while not task.done():
                    pass
                result = task.result()
            else:
                # Ha nincs futó loop, akkor futtatjuk
                result = loop.run_until_complete(self.read_tick_data(symbol, start_date, end_date))
        except RuntimeError:
            # Ha nincs event loop, létrehozunk egyet
            result = asyncio.run(self.read_tick_data(symbol, start_date, end_date))
        
        # Konvertálás pandas DataFrame-re ha szükséges
        if not isinstance(result, pd.DataFrame):
            try:
                import polars as pl
                if isinstance(result, pl.DataFrame):
                    result = result.to_pandas()
            except ImportError:
                pass
        
        return result

    def save_object(self, obj: object, path: str, **kwargs: Any) -> None:
        """Objektum mentése a megadott útvonalra.
        
        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        import pickle
        full_path = self._get_full_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'wb') as f:
            pickle.dump(obj, f)

    def load_object(self, path: str, **kwargs: Any) -> object:
        """Objektum betöltése a megadott útvonalról.
        
        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        import pickle
        full_path = self._get_full_path(path)
        with open(full_path, 'rb') as f:
            return pickle.load(f)

    def exists(self, path: str) -> bool:
        """Ellenőrzi, hogy az útvonal létezik-e."""
        return self._get_full_path(path).exists()

    def get_metadata(self, path: str) -> dict[str, Any]:
        """Fájl vagy könyvtár metaadatainak lekérdezése."""
        full_path = self._get_full_path(path)
        if not full_path.exists():
            from neural_ai.core.storage.exceptions import StorageNotFoundError
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")
        
        stat = full_path.stat()
        return {
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "accessed": datetime.fromtimestamp(stat.st_atime),
            "is_file": full_path.is_file(),
            "is_dir": full_path.is_dir(),
        }

    def delete(self, path: str) -> None:
        """Fájl vagy könyvtár törlése."""
        from neural_ai.core.storage.exceptions import StorageNotFoundError
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")
        
        if full_path.is_file():
            full_path.unlink()
        else:
            import shutil
            shutil.rmtree(full_path)

    def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]:
        """Könyvtár tartalmának listázása."""
        from neural_ai.core.storage.exceptions import StorageNotFoundError, StorageIOError
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Könyvtár nem található: {full_path}")
        if not full_path.is_dir():
            raise StorageIOError(f"Az útvonal nem könyvtár: {full_path}")
        
        pattern = pattern or "*"
        return list(full_path.glob(pattern))

    def _get_full_path(self, path: str | Path) -> Path:
        """Segédfüggvény az útvonal feloldásához."""
        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj
        return self.BASE_PATH / path_obj
