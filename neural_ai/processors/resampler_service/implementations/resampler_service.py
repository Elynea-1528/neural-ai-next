"""ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása."""

from datetime import datetime
from typing import TYPE_CHECKING

import polars as pl

from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.processors.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplingError,
)
from neural_ai.processors.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


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
        self._logger: LoggerInterface = LoggerFactory.get_logger("resampler_service")

    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = "1m",
        return_type: str = "polars",
    ) -> pl.DataFrame:
        """Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            start: A kezdő időpont
            end: A záró időpont
            timeframe: Az időkeret (alapértelmezett: '1m' - 1 perc)
            return_type: A visszaadott DataFrame típusa ('pandas' vagy 'polars')

        Returns:
            pl.DataFrame: OHLCV gyertyákat tartalmazó Polars DataFrame

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
            # Átalakítás OHLCV gyertyákká (mindig Polars)
            ohlcv_data = self._convert_to_ohlcv(tick_data, timeframe)

            # Mindig Polars DataFrame visszaadása (Zero-Copy)
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
        valid_timeframes = ["tick", "1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"]
        if timeframe.lower() not in [tf.lower() for tf in valid_timeframes]:
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

    def _convert_to_ohlcv(self, tick_data: pl.DataFrame, timeframe: str) -> pl.DataFrame:
        """Tick adatok átalakítása kiterjesztett OHLCV gyertyákká.

        Args:
            tick_data: Polars DataFrame tick adatokkal
            timeframe: Az időkeret

        Returns:
            Polars DataFrame kiterjesztett gyertyákkal (Bid/Mid OHLC, Spread, Real/Tick Volume)
        """
        # Ellenőrizzük, hogy van-e adat
        if tick_data.is_empty():
            return pl.DataFrame(
                schema=[
                    "timestamp",
                    "mid_open",
                    "mid_high",
                    "mid_low",
                    "mid_close",
                    "bid_open",
                    "bid_high",
                    "bid_low",
                    "bid_close",
                    "spread",
                    "real_volume",
                    "tick_volume",
                    "bid_volume",
                    "ask_volume",
                ]
            )

        # Szükséges oszlopok ellenőrzése
        required_columns = ["timestamp", "bid", "ask", "bid_volume", "ask_volume"]
        missing_columns = [col for col in required_columns if col not in tick_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for OHLCV conversion: {missing_columns}")

        # Ha timeframe tick, akkor bypass aggregáció és enrich soronként
        if timeframe.lower() == "tick":
            mid_price = (pl.col("bid") + pl.col("ask")) / 2
            enriched_tick_data = tick_data.with_columns(
                mid_open=mid_price,
                mid_high=mid_price,
                mid_low=mid_price,
                mid_close=mid_price,
                bid_open=pl.col("bid"),
                bid_high=pl.col("bid"),
                bid_low=pl.col("bid"),
                bid_close=pl.col("bid"),
                spread=pl.col("ask") - pl.col("bid"),
                real_volume=pl.col("bid_volume") + pl.col("ask_volume"),
                tick_volume=pl.lit(1),
            )
            return enriched_tick_data

        # Volume oszlopok kezelése (csak bid_volume, ask_volume)
        volume_cols: list[str] = []
        if "bid_volume" in tick_data.columns:
            volume_cols.append("bid_volume")
        if "ask_volume" in tick_data.columns:
            volume_cols.append("ask_volume")

        # Mid ár számítása (bid és ask átlaga)
        tick_data = tick_data.with_columns(mid_price=(pl.col("bid") + pl.col("ask")) / 2)

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

        # Kiterjesztett aggregáció Polars group_by_dynamic használatával
        ohlcv = (
            tick_data.sort("timestamp")
            .group_by_dynamic("timestamp", every=polars_timeframe)
            .agg(
                [
                    # Mid OHLC (középár)
                    pl.col("mid_price").first().alias("mid_open"),
                    pl.col("mid_price").max().alias("mid_high"),
                    pl.col("mid_price").min().alias("mid_low"),
                    pl.col("mid_price").last().alias("mid_close"),
                    # Bid OHLC
                    pl.col("bid").first().alias("bid_open"),
                    pl.col("bid").max().alias("bid_high"),
                    pl.col("bid").min().alias("bid_low"),
                    pl.col("bid").last().alias("bid_close"),
                    # Spread: átlag (ask - bid)
                    (pl.col("ask") - pl.col("bid")).mean().alias("spread"),
                    # Real Volume: bid_volume + ask_volume összeg
                    (pl.col("bid_volume") + pl.col("ask_volume")).sum().alias("real_volume"),
                    # Tick Volume: tick szám
                    pl.len().alias("tick_volume"),
                ]
                + [pl.col(col).sum().alias(f"{col}_sum") for col in volume_cols]
            )
        )

        # Volume oszlopok átnevezése
        for col in volume_cols:
            if f"{col}_sum" in ohlcv.columns:
                ohlcv = ohlcv.rename({f"{col}_sum": col})

        # Natív Polars DataFrame visszaadás (Zero-Copy)
        return ohlcv
