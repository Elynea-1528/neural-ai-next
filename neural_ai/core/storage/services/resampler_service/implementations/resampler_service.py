"""ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása."""

from datetime import datetime
from typing import TYPE_CHECKING

import pandas as pd
import polars as pl

from neural_ai.core.storage.services.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)
from neural_ai.core.storage.services.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)

if TYPE_CHECKING:
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class ResamplerService(ResamplerInterface):
    """ResamplerService implementáció, amely tick adatokból hoz létre OHLCV gyertyákat.

    Ez a szolgáltatás felelős a tick adatok átalakításáért OHLCV (Open, High, Low, Close, Volume)
    gyertyákká a megadott időkeretben. A hatékonyság érdekében Polars-t használ.
    """

    def __init__(self, storage: "StorageInterface") -> None:
        """ResamplerService inicializálása.

        Args:
            storage: A tárolási interfész példány (Dependency Injection)
        """
        self._storage = storage

    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = '1m'
    ) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            start: A kezdő időpont
            end: A záró időpont
            timeframe: Az időkeret (alapértelmezett: '1m' - 1 perc)

        Returns:
            DataFrame: OHLCV gyertyákat tartalmazó DataFrame

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen
            DataLoadError: Ha hiba történik az adatok betöltése során
            ResamplingError: Ha hiba történik az átalakítás során
        """
        # Időkeret validálása
        self._validate_timeframe(timeframe)

        try:
            # Tick adatok betöltése a tárolóból
            tick_data = await self._load_tick_data(symbol, start, end)
        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(
                symbol=symbol,
                start=str(start),
                end=str(end),
                original_error=e
            ) from e

        try:
            # Átalakítás OHLCV gyertyákká
            ohlcv_data = self._convert_to_ohlcv(tick_data, timeframe)
            return ohlcv_data
        except Exception as e:
            raise ResamplingError(
                symbol=symbol,
                timeframe=timeframe,
                original_error=e
            ) from e

    def _validate_timeframe(self, timeframe: str) -> None:
        """Időkeret validálása.

        Args:
            timeframe: Az időkeret string

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen
        """
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W', '1M']
        if timeframe not in valid_timeframes:
            raise InvalidTimeframeError(timeframe)

    async def _load_tick_data(
        self,
        symbol: str,
        start: datetime,
        end: datetime
    ) -> pl.DataFrame:
        """Tick adatok betöltése a tárolóból.

        Args:
            symbol: A kereskedési szimbólum
            start: A kezdő időpont
            end: A záró időpont

        Returns:
            Polars DataFrame a tick adatokkal

        Raises:
            DataLoadError: Ha hiba történik a betöltés során
        """
        # FIXME: Ez egy ideiglenes implementáció
        # A valós implementációban a StorageInterface-en keresztül kell betölteni az adatokat
        # Jelenleg egy üres DataFrame-et adunk vissza a struktúra bemutatásához

        # Példa adatok létrehozása (ez a rész kerüljön lecserélésre a valós adatokra)
        import numpy as np
        date_range = pd.date_range(start=start, end=end, freq='1s')

        tick_data = pl.DataFrame({
            "timestamp": date_range,
            "bid": np.random.uniform(1.05, 1.10, len(date_range)),
            "ask": np.random.uniform(1.05, 1.10, len(date_range)),
            "volume": np.random.randint(1, 100, len(date_range))
        })

        return tick_data

    def _convert_to_ohlcv(
        self,
        tick_data: pl.DataFrame,
        timeframe: str
    ) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká.

        Args:
            tick_data: Polars DataFrame tick adatokkal
            timeframe: Az időkeret

        Returns:
            Pandas DataFrame OHLCV gyertyákkal
        """
        # Átlagár számítása (bid és ask átlaga)
        tick_data = tick_data.with_columns(
            price=(pl.col("bid") + pl.col("ask")) / 2
        )

        # Timestamp oszlop beállítása indexként
        tick_data = tick_data.sort("timestamp")

        # OHLCV aggregáció Polars group_by_dynamic használatával
        ohlcv = tick_data.group_by_dynamic(
            "timestamp",
            every=timeframe,
            period=timeframe
        ).agg([
            pl.col("price").first().alias("open"),
            pl.col("price").max().alias("high"),
            pl.col("price").min().alias("low"),
            pl.col("price").last().alias("close"),
            pl.col("volume").sum().alias("volume")
        ])

        # Polars DataFrame konvertálása Pandas DataFrame-re
        ohlcv_pandas = ohlcv.to_pandas()

        # Index beállítása timestamp-re
        ohlcv_pandas.set_index("timestamp", inplace=True)

        return ohlcv_pandas
