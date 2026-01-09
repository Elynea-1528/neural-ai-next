"""ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása."""

from datetime import datetime
from typing import TYPE_CHECKING

import pandas as pd
import polars as pl
import structlog

from neural_ai.core.processing.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)
from neural_ai.core.processing.resampler_service.interfaces.resampler_interface import (
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
        self._logger = structlog.get_logger()

    async def resample(
        self, symbol: str, start: datetime, end: datetime, timeframe: str = "1m"
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
                symbol=symbol, start=str(start), end=str(end), original_error=e
            ) from e

        try:
            # Átalakítás OHLCV gyertyákká
            ohlcv_data = self._convert_to_ohlcv(tick_data, timeframe)
            return ohlcv_data
        except Exception as e:
            raise ResamplingError(symbol=symbol, timeframe=timeframe, original_error=e) from e

    def _validate_timeframe(self, timeframe: str) -> None:
        """Időkeret validálása.

        Args:
            timeframe: Az időkeret string

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen
        """
        valid_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"]
        if timeframe not in valid_timeframes:
            raise InvalidTimeframeError(timeframe)

    async def _load_tick_data(self, symbol: str, start: datetime, end: datetime) -> pl.DataFrame:
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
        try:
            # Tick adatok betöltése a StorageInterface-en keresztül
            # Dinamikusan hívjuk meg a read_tick_data metódust
            read_method = getattr(self._storage, "read_tick_data", None)
            if read_method is None:
                raise DataLoadError(
                    symbol=symbol,
                    start=str(start),
                    end=str(end),
                    original_error=AttributeError("Storage does not support read_tick_data method"),
                )
            tick_data = await read_method(symbol, start, end)

            # Ellenőrizzük, hogy kaptunk-e adatot
            if tick_data is None or len(tick_data) == 0:
                self._logger.warning(
                    "No tick data found for the specified range",
                    symbol=symbol,
                    start=start.isoformat(),
                    end=end.isoformat(),
                )
                return pl.DataFrame()

            return tick_data
        except Exception as e:
            raise DataLoadError(
                symbol=symbol, start=str(start), end=str(end), original_error=e
            ) from e

    def _convert_to_ohlcv(self, tick_data: pl.DataFrame, timeframe: str) -> pd.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká Polars group_by_dynamic használatával.

        Args:
            tick_data: Polars DataFrame tick adatokkal
            timeframe: Az időkeret

        Returns:
            Pandas DataFrame OHLCV gyertyákkal
        """
        # Ellenőrizzük, hogy van-e adat
        if tick_data.is_empty():
            return pd.DataFrame(
                columns=["open", "high", "low", "close", "volume", "bid_volume", "ask_volume"]
            )

        # Szükséges oszlopok ellenőrzése
        required_columns = ["timestamp", "bid", "ask"]
        missing_columns = [col for col in required_columns if col not in tick_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for OHLCV conversion: {missing_columns}")

        # Volume oszlopok kezelése (lehet volume, bid_volume, ask_volume)
        volume_cols = []
        if "volume" in tick_data.columns:
            volume_cols.append("volume")
        if "bid_volume" in tick_data.columns:
            volume_cols.append("bid_volume")
        if "ask_volume" in tick_data.columns:
            volume_cols.append("ask_volume")

        # Átlagár számítása (bid és ask átlaga)
        tick_data = tick_data.with_columns(price=(pl.col("bid") + pl.col("ask")) / 2)

        # Időkeret konvertálása Polars formátumba
        timeframe_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1D": "1d",
            "1W": "1w",
            "1M": "1mo",
        }
        polars_timeframe = timeframe_map.get(timeframe, "1m")

        # OHLCV aggregáció Polars group_by_dynamic használatával
        # A timestamp oszlopot használjuk időalapú csoportosításhoz
        ohlcv = (
            tick_data.sort("timestamp")
            .group_by_dynamic("timestamp", every=polars_timeframe)
            .agg(
                [
                    pl.col("price").first().alias("open"),
                    pl.col("price").max().alias("high"),
                    pl.col("price").min().alias("low"),
                    pl.col("price").last().alias("close"),
                ]
                + [pl.col(col).sum().alias(f"{col}_sum") for col in volume_cols]
            )
        )

        # Oszlopnevek normalizálása
        ohlcv = ohlcv.rename(
            {
                "timestamp": "timestamp",
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
            }
        )

        # Volume oszlopok átnevezése
        for col in volume_cols:
            if f"{col}_sum" in ohlcv.columns:
                if col == "volume":
                    ohlcv = ohlcv.rename({f"{col}_sum": "volume"})
                elif col == "bid_volume":
                    ohlcv = ohlcv.rename({f"{col}_sum": "bid_volume"})
                elif col == "ask_volume":
                    ohlcv = ohlcv.rename({f"{col}_sum": "ask_volume"})

        # Konvertálás Pandas DataFrame-re és timestamp beállítása indexként
        result_df = ohlcv.to_pandas()
        if not result_df.empty:
            result_df.index = pd.to_datetime(result_df["timestamp"])
            result_df = result_df.drop("timestamp", axis=1)
        return result_df
