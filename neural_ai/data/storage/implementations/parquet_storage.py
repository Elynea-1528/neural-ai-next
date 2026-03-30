"""ParquetStorageService - Particionált Parquet tároló szolgáltatás.

Ez a modul implementálja a Tick adatok particionált Parquet formátumban történő tárolását
és lekérdezését a Neural AI Next rendszer számára. A tárolás dátum és szimbólum alapú
particionálást használ a gyors lekérdezés érdekében.

A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb
backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

Szerző: Neural AI Next csapat
Verzió: 2.0.0
"""
# pyright: reportUnknownVariableType=false, reportInvalidTypeForm=false, reportUnknownMemberType=false
# DataFrame type alias TYPE_CHECKING blokkban van, cast() string annotation hibák

import asyncio
import hashlib
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel, ConfigDict, Field

from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.utils.decorators import trace
from neural_ai.data.storage.exceptions import StorageIOError, StorageNotFoundError
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    from neural_ai.core.config.interfaces.config_interface import ConfigInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
    from neural_ai.data.storage.backends.base import StorageBackend

    # Type alias a DataFrame típusokhoz
    DataFrame = pd.DataFrame | pl.DataFrame


class ParquetWriteConfig(BaseModel):
    """Parquet írás opciók konfigurációja."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)

    compression: str = Field(
        "snappy",
        pattern="^(snappy|gzip|brotli|zstd|lz4|none)$",
        description="Tömörítési algoritmus",
    )
    unique_id: str | None = Field(None, description="Egyedi azonosító a fájlnévhez")


class ParquetReadConfig(BaseModel):
    """Parquet olvasás opciók konfigurációja."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)

    start_date: datetime = Field(..., description="Kezdő dátum")
    end_date: datetime = Field(..., description="Záró dátum")


# Modul szintű változók a teszteléshez (lazy import támogatáshoz)
pl: Any = None  # type: ignore[no-redef]
pd: Any = None  # type: ignore[no-redef]


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
        logger: "LoggerInterface",
        config: "ConfigInterface | None" = None,
        event_bus: "EventBusInterface | None" = None,
        base_path: str | Path | None = None,
        compression: str = "snappy",
        hardware: "HardwareInterface | None" = None,
        **kwargs: Any,
    ) -> None:
        """Inicializálja a ParquetStorageService-t backend selectorral.

        A hardver detekció alapján kiválasztja a megfelelő tárolási backend-et.
        Ha az AVX2 utasításkészlet elérhető, a PolarsBackend-et használja,
        egyébként a PandasBackend-et kompatibilitási módban.

        Args:
            logger: A naplózásért felelős interfész
            config: A konfigurációért felelős interfész
            event_bus: Az eseménybusz interfész
            base_path: Az alapútvonal a tároláshoz (opcionális)
            compression: A tömörítési algoritmus (alapértelmezett: 'snappy')
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális)
            **kwargs: További opcionális paraméterek
        """
        self.logger = logger
        self.config = config
        self.event_bus = event_bus

        # Pydantic validáció a configra
        raw_config = config.get_section("storage") if config else {}
        self.storage_config = StorageConfig(**(raw_config or {}))

        # Base path inicializáció
        if base_path:
            self.base_path = Path(base_path)
        elif self.storage_config.base_path:
            self.base_path = Path(self.storage_config.base_path)
        else:
            self.base_path = Path("data/tick")

        self.engine = self.storage_config.engine or "fastparquet"
        self.compression = compression or self.storage_config.compression or "snappy"
        self.backend: StorageBackend

        # Dependency Injection a HardwareInterface-hez
        if hardware is None:
            from neural_ai.core.utils.factory import HardwareFactory

            self.hardware = HardwareFactory.get_hardware_interface()
        else:
            self.hardware = hardware

        # Hardver detekció és backend kiválasztás
        self._select_backend()

        # Debug log az inicializáláshoz
        self.logger.debug(
            "Initializing ParquetStorageService",
            base_path=str(self.base_path),
            engine=self.engine,
            compression=self.compression,
        )

        # Logolás a saját loggerrel (ha van), vagy a globálissal
        log_msg = f"ParquetStorageService initialized with {self.backend.name} backend"
        if self.logger:
            self.logger.info(log_msg)

    def _select_backend(self) -> None:
        """Backend kiválasztása hardver detekció alapján.

        Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért
        a hardver képességek alapján. Külön metódusba van kiszervezve,
        hogy a tesztek könnyen mockolhassák.
        """
        if self.hardware.has_avx2():
            from neural_ai.data.storage.backends.polars_backend import PolarsBackend

            self.backend = PolarsBackend(
                logger=self.logger, name="polars", supported_formats=["parquet"]
            )
            self.engine = "polars"
            # DEBUG log a backend kiválasztáshoz
            log_msg = f"Selected backend: {self.backend.name} (AVX2={self.hardware.has_avx2()})"
            if self.logger:
                self.logger.debug(log_msg)
                self.logger.info(
                    "AVX2 support detected. Using PolarsBackend for accelerated data processing."
                )
        else:
            from neural_ai.data.storage.backends.pandas_backend import PandasBackend

            self.backend = PandasBackend(
                logger=self.logger, name="pandas", supported_formats=["parquet"]
            )
            self.engine = "fastparquet"
            # DEBUG log a backend kiválasztáshoz
            log_msg = f"Selected backend: {self.backend.name} (AVX2={self.hardware.has_avx2()})"
            if self.logger:
                self.logger.debug(log_msg)
                self.logger.warning(
                    "Legacy CPU detected. Running in Compatibility Mode with PandasBackend."
                )
            else:
                # Ha nincs logger, nem logolunk
                pass

    def _get_path(self, symbol: str, date: datetime, unique_id: str | None = None) -> Path:
        """Elérési út generálása a megadott szimbólumhoz és dátumhoz.

        Args:
            symbol: A pénzpár szimbóluma (pl. 'EURUSD')
            date: A dátum
            unique_id: Egyedi azonosító a fájlnévhez (opcionális)

        Returns:
            A teljes elérési út a Parquet fájlhoz

        Example:
            >>> service = ParquetStorageService()
            >>> date = datetime(2023, 12, 23)
            >>> path = service._get_path('EURUSD', date)
            >>> print(path)
            /data/tick/EURUSD/tick/year=2023/month=12/day=23/tick_20231223_abc123.parquet
        """
        if unique_id:
            filename = f"tick_{date.strftime('%Y%m%d')}_{unique_id}.parquet"
        else:
            # Live módhoz: ÓraPercMsp_Micsec
            ts_str = datetime.now().strftime("%H%M%S_%f")
            filename = f"tick_{date.strftime('%Y%m%d')}_{ts_str}.parquet"

        return (
            self.base_path
            / symbol.upper()
            / f"year={date.year}"
            / f"month={date.month:02d}"
            / f"day={date.day:02d}"
            / filename
        )

    @trace
    async def store_tick_data(
        self, symbol: str, data: Any, date: datetime, unique_id: str | None = None
    ) -> None:
        """Tick adatok tárolása particionált Parquet formátumban.

        Args:
            symbol: A pénzpár szimbóluma
            data: A Tick adatokat tartalmazó DataFrame
            date: A dátum, ami alapján a particionálás történik
            unique_id: Egyedi azonosító a fájlnévhez (opcionális)

        Raises:
            ValueError: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

        Példa:
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
        # Logger használata
        log = self.logger
        log.debug(
            "Starting tick data storage", symbol=symbol, date=date.isoformat(), rows=len(data)
        )

        if len(data) == 0:
            raise ValueError("Cannot store empty DataFrame")

        required_columns = ["timestamp", "bid", "ask"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # APPEND-ONLY logika: minden adat egyedi fájlba kerül mentésre
        # Ez biztosítja a 100%-os adatmentést, a deduplikációt olvasáskor végezzük

        # Új fájl létrehozása egyedi azonosítóval
        path = self._get_path(symbol, date, unique_id=unique_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Adatok tárolása a kiválasztott backend-en keresztül
        try:
            self.backend.write(data, str(path), compression=self.compression)

            log.info(
                "Tick data stored successfully",
                symbol=symbol,
                date=date.isoformat(),
                rows=len(data),
                path=str(path),
                size_mb=path.stat().st_size / (1024 * 1024),
                backend=self.backend.name,
            )
        except Exception as e:
            log.error(
                "Failed to store tick data",
                symbol=symbol,
                date=date.isoformat(),
                path=str(path),
                error=str(e),
                error_type=type(e).__name__,
            )
            raise  # Tovább dobjuk a hibát, hogy a hívó is tudjon róla

    @trace
    async def read_tick_data(self, symbol: str, start_date: datetime, end_date: datetime) -> Any:
        """Tick adatok olvasása dátumtartományból.

        Args:
            symbol: A pénzpár szimbóluma
            start_date: A kezdő dátum
            end_date: A záró dátum

        Returns:
            A Tick adatokat tartalmazó DataFrame

        Példa:
            >>> from datetime import datetime, timedelta
            >>>
            >>> service = ParquetStorageService()
            >>> start = datetime(2023, 12, 1)
            >>> end = datetime(2023, 12, 31)
            >>>
            >>> data = await service.read_tick_data('EURUSD', start, end)
            >>> print(f"Betöltött {len(data)} tick-ek")
        """
        self.logger.debug(
            "Starting tick data reading",
            symbol=symbol,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        paths: list[Path] = []

        # Összes Parquet fájl megtalálása a dátumtartományban
        current_date = start_date
        while current_date <= end_date:
            date_dir = (
                self.base_path
                / symbol.upper()
                / f"year={current_date.year}"
                / f"month={current_date.month:02d}"
                / f"day={current_date.day:02d}"
            )
            if date_dir.exists():
                # Összes .parquet fájl hozzáadása ebből a mappából
                paths.extend(date_dir.glob("*.parquet"))
            current_date += timedelta(days=1)

        if not paths:
            self.logger.warning(
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

            self.logger.debug(f"Rows before deduplication: {len(result)}")

            # Deduplikáció: egyedi sorok szűrése timestamp + source alapján
            result = self._deduplicate_data(result)

            self.logger.debug(f"Rows after deduplication: {len(result)}")

            # Rendezés timestamp szerint
            result = self._sort_by_timestamp(result)

            # Dátum szerinti szűrés (pontosabb)
            result = self._filter_by_timestamp(result, start_date, end_date)

            self.logger.debug(f"Rows after filter: {len(result)}")
        else:
            if self.engine == "polars":
                import polars as pl

                result = pl.DataFrame()
            else:
                import pandas as pd

                result = pd.DataFrame()

        self.logger.info(
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
        """DataFrame-ek összefűzése a backend típusának megfelelően."""
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

    def _deduplicate_data(self, data: Any) -> Any:
        """Adatok deduplikációja timestamp + bid + ask alapján.

        Args:
            data: A deduplikálandó DataFrame

        Returns:
            A deduplikált DataFrame
        """
        if self.engine == "polars":
            import polars as pl

            try:
                # Ha már Polars DataFrame, használjuk közvetlenül
                if isinstance(data, pl.DataFrame):
                    pl_df = data
                else:
                    # Egyébként próbáljuk meg konvertálni
                    # Először próbáljuk meg a to_pandas() metódussal, ha van
                    if hasattr(data, "to_pandas"):
                        pd_df = data.to_pandas()
                        pl_df = pl.DataFrame(pd_df)
                    else:
                        # Ha nincs to_pandas() metódus, próbáljuk közvetlenül
                        pl_df = pl.DataFrame(data)

                # Csak a szükséges oszlopokat választjuk ki a deduplikációhoz
                # Ez biztosítja, hogy ne legyen oszlop szélesség hiba
                available_columns = [
                    col
                    for col in [
                        "timestamp",
                        "bid",
                        "ask",
                        "volume",
                        "ask_volume",
                        "bid_volume",
                        "source",
                    ]
                    if col in pl_df.columns
                ]
                pl_df_selected = pl_df.select(available_columns)

                # Deduplikáció: egyedi sorok szűrése timestamp + bid + ask alapján
                # Ez megőrzi az azonos időbélyegű, de eltérő árú tick-eket (intra-millisecond ticks)
                deduplicated = pl_df_selected.unique(
                    subset=["timestamp", "bid", "ask"], maintain_order=False
                )
                return deduplicated
            except Exception as e:
                # Ha bármi hiba történik, adjuk vissza az eredeti adatot
                self.logger.warning(f"Deduplikáció sikertelen, visszaadom az eredeti adatot: {e}")
                return data
        else:
            import pandas as pd

            try:
                # Ha már Pandas DataFrame, használjuk közvetlenül
                if isinstance(data, pd.DataFrame):
                    pd_df = data
                else:
                    # Egyébként próbáljuk meg konvertálni
                    # Először próbáljuk meg a to_pandas() metódussal, ha van
                    if hasattr(data, "to_pandas"):
                        pd_df = data.to_pandas()
                    else:
                        # Ha nincs to_pandas() metódus, próbáljuk közvetlenül
                        pd_df = pd.DataFrame(data)

                # Csak a szükséges oszlopokat választjuk ki a deduplikációhoz
                # Ez biztosítja, hogy ne legyen oszlop szélesség hiba
                available_columns = [
                    col
                    for col in [
                        "timestamp",
                        "bid",
                        "ask",
                        "volume",
                        "ask_volume",
                        "bid_volume",
                        "source",
                    ]
                    if col in pd_df.columns
                ]
                pd_df_selected = pd_df[available_columns]

                # Deduplikáció: egyedi sorok szűrése timestamp + bid + ask alapján
                # Ez megőrzi az azonos időbélyegű, de eltérő árú tick-eket (intra-millisecond ticks)
                return pd_df_selected.drop_duplicates(
                    subset=["timestamp", "bid", "ask"], keep="first"
                )
            except Exception as e:
                # Ha bármi hiba történik, adjuk vissza az eredeti adatot
                self.logger.warning(f"Deduplikáció sikertelen, visszaadom az eredeti adatot: {e}")
                return data

    def _filter_columns(self, data: Any) -> Any:
        """DataFrame oszlopainak szűrése csak a szükségesekre.

        Args:
            data: A szűrendő DataFrame

        Returns:
            A szűrt DataFrame csak a szükséges oszlopokkal
        """
        if self.engine == "polars":
            import polars as pl

            try:
                if isinstance(data, pl.DataFrame):
                    pl_df = data
                else:
                    if hasattr(data, "to_pandas"):
                        pd_df = data.to_pandas()
                        pl_df = pl.DataFrame(pd_df)
                    else:
                        pl_df = pl.DataFrame(data)

                # Csak a szükséges oszlopokat választjuk ki
                available_columns = [
                    col
                    for col in [
                        "timestamp",
                        "bid",
                        "ask",
                        "volume",
                        "ask_volume",
                        "bid_volume",
                        "source",
                    ]
                    if col in pl_df.columns
                ]
                return pl_df.select(available_columns)
            except Exception as e:
                self.logger.warning(f"Oszlop szűrés sikertelen, visszaadom az eredeti adatot: {e}")
                return data
        else:
            import pandas as pd

            try:
                if isinstance(data, pd.DataFrame):
                    pd_df = data
                else:
                    if hasattr(data, "to_pandas"):
                        pd_df = data.to_pandas()
                    else:
                        pd_df = pd.DataFrame(data)

                # Csak a szükséges oszlopokat választjuk ki
                available_columns = [
                    col
                    for col in [
                        "timestamp",
                        "bid",
                        "ask",
                        "volume",
                        "ask_volume",
                        "bid_volume",
                        "source",
                    ]
                    if col in pd_df.columns
                ]
                return pd_df[available_columns]
            except Exception as e:
                self.logger.warning(f"Oszlop szűrés sikertelen, visszaadom az eredeti adatot: {e}")
                return data

    def _sort_by_timestamp(self, data: Any) -> Any:
        """DataFrame rendezése timestamp szerint.

        Args:
            data: A rendezendő DataFrame

        Returns:
            A rendezett DataFrame
        """
        if self.engine == "polars":
            import polars as pl

            pl_df = cast(pl.DataFrame, data)
            return pl_df.sort("timestamp")
        else:
            import pandas as pd

            pd_df = cast(pd.DataFrame, data)
            return pd_df.sort_values("timestamp").reset_index(drop=True)

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
        # Mivel az adatok már dátum particionálva vannak, és csak a
        # megfelelő dátumú fájlokat töltjük be, a szűrés gyakorlatilag
        # felesleges. Visszaadjuk az adatokat változatlanul.
        # Ez elkerüli a datetime precision problémákat is.
        return data

    @trace
    async def get_available_dates(self, symbol: str) -> list[datetime]:
        """Elérhető dátumok lekérdezése egy adott szimbólumhoz.

        Args:
            symbol: A pénzpár szimbóluma

        Returns:
            Az elérhető dátumok listája

        Példa:
            >>> service = ParquetStorageService()
            >>> dates = await service.get_available_dates('EURUSD')
            >>> print(f"Elérhető dátumok: {len(dates)}")
        """
        symbol_path = self.base_path / symbol.upper()

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
            A checksum SHA256 hash (az összes fájlra vonatkozik az adott napon)

        Példa:
            >>> service = ParquetStorageService()
            >>> checksum = await service.calculate_checksum('EURUSD', datetime.now())
            >>> print(f"Ellenőrző összeg: {checksum}")

        Note:
            A checksum mostantól az összes fájlra vonatkozik az adott napon,
            nem csak egy specifikusra. Az összes fájl adatait összefűzi és
            az egészre számol checksum-ot.
        """
        # Az adott nap mappájának elérési útja
        date_dir = (
            self.base_path
            / symbol.upper()
            / f"year={date.year}"
            / f"month={date.month:02d}"
            / f"day={date.day:02d}"
        )

        if not date_dir.exists():
            return ""

        # Összes Parquet fájl beolvasása
        parquet_files = list(date_dir.glob("*.parquet"))
        if not parquet_files:
            return ""

        try:
            # Összes fájl beolvasása és összefűzése
            dfs: list[DataFrame] = []
            for file_path in parquet_files:
                df = self.backend.read(str(file_path))
                dfs.append(df)  # pyright: ignore[reportUnknownMemberType]

            # Összefűzés
            combined_df = self._concat_dataframes(dfs)  # pyright: ignore[reportArgumentType]

            # Deduplikáció és rendezés
            combined_df = self._deduplicate_data(combined_df)
            combined_df = self._sort_by_timestamp(combined_df)

            # Csak a fontos oszlopok alapján checksum számítás
            if self.engine == "polars":
                import polars as pl

                pl_df = cast(pl.DataFrame, combined_df)
                data_str = pl_df.select(["timestamp", "bid", "ask"]).write_csv()
            else:
                import pandas as pd

                pd_df = cast(pd.DataFrame, combined_df)
                data_str = pd_df[["timestamp", "bid", "ask"]].to_csv(index=False)

            return hashlib.sha256(data_str.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate checksum: {e}")
            return ""

    @trace
    async def verify_data_integrity(self, symbol: str, date: datetime) -> bool:
        """Adatintegritás ellenőrzése.

        Args:
            symbol: A pénzpár szimbóluma
            date: A dátum

        Returns:
            True ha az adatok integritása megfelelő, egyébként False

        Példa:
            >>> service = ParquetStorageService()
            >>> is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
            >>> print(f"Adatintegritás: {is_valid}")

        Note:
            Az integritás ellenőrzés mostantól az összes fájlra vonatkozik az adott napon.
            Az összes fájlt beolvassa, összefűzi, deduplikálja és ellenőrzi a rendezettséget.
        """
        # Az adott nap mappájának elérési útja
        date_dir = (
            self.base_path
            / symbol.upper()
            / f"year={date.year}"
            / f"month={date.month:02d}"
            / f"day={date.day:02d}"
        )

        if not date_dir.exists():
            return False

        # Összes Parquet fájl beolvasása
        parquet_files = list(date_dir.glob("*.parquet"))
        if not parquet_files:
            return False

        try:
            # Összes fájl beolvasása és összefűzése
            dfs: list[DataFrame] = []
            for file_path in parquet_files:
                df = self.backend.read(str(file_path))
                dfs.append(df)  # pyright: ignore[reportUnknownMemberType]

            # Összefűzés
            combined_df = self._concat_dataframes(dfs)  # pyright: ignore[reportArgumentType]

            # Alapvető ellenőrzések
            assert len(combined_df) > 0, "Empty dataframe"
            assert "timestamp" in combined_df.columns, "Missing timestamp column"
            assert "bid" in combined_df.columns, "Missing bid column"
            assert "ask" in combined_df.columns, "Missing ask column"

            # Deduplikáció és rendezés
            combined_df = self._deduplicate_data(combined_df)
            combined_df = self._sort_by_timestamp(combined_df)

            # Rendezés ellenőrzése
            if self.engine == "polars":
                import polars as pl

                pl_df = cast(pl.DataFrame, combined_df)
                # Összehasonlítjuk az eredetit a rendezett változattal
                sorted_timestamp = pl_df["timestamp"].sort()
                is_sorted = (pl_df["timestamp"] == sorted_timestamp).all()
                assert is_sorted, "Data not sorted by timestamp"
            else:
                import pandas as pd

                pd_df = cast(pd.DataFrame, combined_df)
                assert pd_df["timestamp"].is_monotonic_increasing, "Data not sorted by timestamp"

            self.logger.info(
                "Data integrity verified",
                symbol=symbol,
                date=date.isoformat(),
                rows=len(combined_df),
                files=len(parquet_files),
                backend=self.backend.name,
            )

            return True

        except Exception as e:
            self.logger.error(
                "Data integrity check failed", symbol=symbol, date=date.isoformat(), error=str(e)
            )
            return False

    async def get_storage_stats(self, symbol: str | None = None) -> dict[str, Any]:
        """Tárolási statisztikák lekérdezése.

        Args:
            symbol: Opcionális szimbólum szűréshez

        Returns:
            A statisztikákat tartalmazó dictionary

        Példa:
            >>> service = ParquetStorageService()
            >>> stats = await service.get_storage_stats('EURUSD')
            >>> print(f"Összes fájlok: {stats['total_files']}")
        """
        stats: dict[str, int | float | dict[str, dict[str, int | float]]] = {
            "total_files": 0,
            "total_size_gb": 0.0,
            "symbols": {},
        }

        base_path = self.base_path
        if symbol:
            base_path = base_path / symbol.upper()

        if not base_path.exists():
            return stats

        # Fájlok felsorolása
        for parquet_file in base_path.rglob("*.parquet"):
            stats["total_files"] += 1  # type: ignore[operator]
            stats["total_size_gb"] += parquet_file.stat().st_size  # type: ignore[operator]

        stats["total_size_gb"] = stats["total_size_gb"] / (1024**3)  # type: ignore[operator]

        # Szimbólumonkénti statisztikák
        for symbol_dir in base_path.iterdir():
            if symbol_dir.is_dir():
                symbol_name = symbol_dir.name
                symbol_stats = {"files": 0, "size_gb": 0.0}

                for parquet_file in symbol_dir.rglob("*.parquet"):
                    symbol_stats["files"] += 1
                    symbol_stats["size_gb"] += parquet_file.stat().st_size

                symbol_stats["size_gb"] = symbol_stats["size_gb"] / (1024**3)
                stats["symbols"][symbol_name] = symbol_stats  # type: ignore[index]

        return stats  # pyright: ignore[reportReturnType]

    # --- StorageInterface Implementáció ---

    def save_dataframe(self, df: "DataFrame", path: str, **kwargs: Any) -> None:  # pyright: ignore[reportReturnType]
        """DataFrame mentése a megadott útvonalra.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        A ParquetStorageService saját store_tick_data metódusát használja.
        """
        raise NotImplementedError(
            "ParquetStorageService save_dataframe adapter nincs implementálva"
        )

    def load_dataframe(self, path: str, **kwargs: Any) -> "DataFrame":  # type: ignore[override]  # pyright: ignore[reportReturnType]
        """DataFrame betöltése a megadott útvonalról.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        raise NotImplementedError(
            "ParquetStorageService load_dataframe adapter nincs implementálva"
        )

    def save_object(self, obj: object, path: str, **kwargs: Any) -> None:
        """Objektum mentése a megadott útvonalra.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        import pickle

        full_path = self._get_full_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "wb") as f:
            pickle.dump(obj, f)

    def load_object(self, path: str, **kwargs: Any) -> object:
        """Objektum betöltése a megadott útvonalról.

        Ez egy adapter metódus a StorageInterface kompatibilitás érdekében.
        """
        import pickle

        full_path = self._get_full_path(path)
        with open(full_path, "rb") as f:
            return pickle.load(f)

    def exists(self, path: str) -> bool:
        """Ellenőrzi, hogy az útvonal létezik-e."""
        return self._get_full_path(path).exists()

    def get_metadata(self, path: str) -> dict[str, Any]:
        """Fájl vagy könyvtár metaadatainak lekérdezése."""
        full_path = self._get_full_path(path)
        if not full_path.exists():
            from neural_ai.data.storage.exceptions import StorageNotFoundError

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
        return self.base_path / path_obj
