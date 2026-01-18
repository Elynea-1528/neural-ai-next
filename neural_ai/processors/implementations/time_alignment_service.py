"""Időszinkronizációs szolgáltatás implementáció."""

from typing import TYPE_CHECKING

import polars as pl

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.interfaces.time_alignment_interface import ITimeAlignmentService

if TYPE_CHECKING:
    pass


class TimeAlignmentService(ITimeAlignmentService):
    """Időszinkronizációs szolgáltatás - tökéletes időskála biztosítása.

    Ez az osztály biztosítja az időszinkronizációs műveleteket, mint a rácsra
    indexelés és lyukak kezelése az adatokban.
    """

    def __init__(self, logger: LoggerInterface) -> None:
        """Időszinkronizációs szolgáltatás inicializálása.

        Args:
            logger: A naplózási interfész a műveletek naplózásához.
        """
        self._logger = logger

    def reindex_to_grid(self, df: pl.DataFrame, timeframe: str) -> pl.DataFrame:
        """Tökéletes időskála generálása minden timeframe-re.

        Létrehozza az összes szükséges időpontot a megadott timeframe alapján,
        és kitölti a hiányzó értékeket.

        Args:
            df: A bemeneti DataFrame időbélyegekkel.
            timeframe: Az időintervallum (pl. '1m', '5m').

        Returns:
            pl.DataFrame: Az újragridelt DataFrame.
        """
        if timeframe.lower() == "tick":
            self._logger.info(
                "Tick adatoknál nincs rács és gap-fill szükséges.",
                extra={"timeframe": timeframe, "rows": len(df)},
            )
            return df  # Tick adaton nincs rács és nincs gap-fill

        # Biztosítjuk, hogy a timestamp oszlop datetime típusú legyen (epoch-ból)
        df_datetime = df.with_columns(pl.from_epoch(pl.col("timestamp").cast(pl.Int64)))

        # Létrehozza az összes szükséges időpontot (pl. minden perc M1-nél)
        full_range = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    df_datetime["timestamp"].min(),
                    df_datetime["timestamp"].max(),
                    interval=timeframe,
                    eager=True,
                )
            }
        )
        result = full_range.join(df_datetime, on="timestamp", how="left")
        self._logger.info(
            "Időskála újragridelve.",
            extra={"timeframe": timeframe, "original_rows": len(df), "new_rows": len(result)},
        )
        return result

    def market_hours_filter(self, df: pl.DataFrame) -> pl.DataFrame:
        """Hétvégék szűrése - csak H-P napok megtartása, kivétel vasárnap >=21 UTC.

        Args:
            df: A bemeneti DataFrame időbélyegekkel.

        Returns:
            pl.DataFrame: A szűrt DataFrame piaci órákban.
        """
        original_count = len(df)
        # Cast timestamp to datetime if needed
        df = df.with_columns(pl.from_epoch(pl.col("timestamp").cast(pl.Int64)))
        weekday = pl.col("timestamp").dt.weekday()
        hour = pl.col("timestamp").dt.hour()
        filtered_df = df.filter((weekday <= 5) | ((weekday == 7) & (hour >= 21)))
        filtered_count = len(filtered_df)
        self._logger.info(
            "Piaci órák szerinti szűrés alkalmazva.",
            extra={"original_count": original_count, "filtered_count": filtered_count},
        )
        return filtered_df

    def handle_gaps(
        self, df: pl.DataFrame, timeframe: str, method: str = "forward_fill"
    ) -> pl.DataFrame:
        """Lyukak kezelése az adatokban - árak forward fill, volumenek 0.

        Args:
            df: A bemeneti DataFrame lyukakkal.
            timeframe: Az időintervallum.
            method: A lyukkezelési módszer ('forward_fill' vagy 'mask').

        Returns:
            pl.DataFrame: A lyukak nélküli DataFrame.

        Raises:
            ValueError: Ha ismeretlen method van megadva.
        """
        if timeframe.lower() == "tick":
            self._logger.info(
                "Tick adatoknál nincs lyukkezelés szükséges.",
                extra={"timeframe": timeframe, "rows": len(df)},
            )
            return df  # Tick adaton nincs rács és nincs gap-fill
        if method == "forward_fill":
            # Áraknál forward fill
            price_cols = [
                "open",
                "high",
                "low",
                "close",
                "mid_open",
                "mid_high",
                "mid_low",
                "mid_close",
            ]
            df = df.with_columns(
                [
                    pl.col(col).fill_null(strategy="forward")
                    for col in price_cols
                    if col in df.columns
                ]
            )
            # Volumeneknél 0
            volume_cols = ["tick_volume", "real_volume", "ask_volume", "bid_volume"]
            df = df.with_columns(
                [pl.col(col).fill_null(0) for col in volume_cols if col in df.columns]
            )
            # Spread és egyéb null-ok forward fill
            df = df.fill_null(strategy="forward")
            self._logger.info(
                "Lyukak kezelése forward_fill módszerrel.",
                extra={"timeframe": timeframe, "method": method, "rows": len(df)},
            )
            return df
        elif method == "mask":
            df = df.with_columns(
                pl.when(pl.col("close").is_null())
                .then(None)
                .otherwise(pl.col("close"))
                .alias("close")
            )
            self._logger.info(
                "Lyukak kezelése mask módszerrel.",
                extra={"timeframe": timeframe, "method": method, "rows": len(df)},
            )
            return df
        else:
            self._logger.error(
                "Ismeretlen lyukkezelési method.",
                extra={"method": method},
            )
            raise ValueError(f"Ismeretlen method: {method}")
