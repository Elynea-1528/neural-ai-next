import polars as pl

from neural_ai.core.processing.interfaces.time_alignment_interface import ITimeAlignmentService


class TimeAlignmentService(ITimeAlignmentService):
    """Időszinkronizációs szolgáltatás - tökéletes időskála biztosítása."""

    def reindex_to_grid(self, df: pl.DataFrame, timeframe: str) -> pl.DataFrame:
        """Tökéletes időskála generálása minden timeframe-re."""
        # Létrehozza az összes szükséges időpontot (pl. minden perc M1-nél)
        # Kezeli a tőzsde nyitvatartási időket
        full_range = pl.DataFrame(
            {
                "timestamp": pl.datetime_range(
                    df["timestamp"].min(), df["timestamp"].max(), interval=timeframe, eager=True
                )
            }
        )
        return full_range.join(df, on="timestamp", how="left")

    def market_hours_filter(self, df: pl.DataFrame) -> pl.DataFrame:
        """Hétvégék szűrése - csak H-P napok megtartása."""
        return df.filter(pl.col("timestamp").dt.weekday() < 6)

    def handle_gaps(self, df: pl.DataFrame, method: str = "forward_fill") -> pl.DataFrame:
        """Lyukak kezelése az adatokban - árak forward fill, volumenek 0."""
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
            return df
        elif method == "mask":
            return df.with_columns(
                pl.when(pl.col("close").is_null())
                .then(None)
                .otherwise(pl.col("close"))
                .alias("close")
            )
        else:
            raise ValueError(f"Ismeretlen method: {method}")
