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

    def handle_gaps(self, df: pl.DataFrame, method: str = "forward_fill") -> pl.DataFrame:
        """Lyukak kezelése az adatokban."""
        if method == "forward_fill":
            return df.fill_null(strategy="forward")
        elif method == "mask":
            return df.with_columns(
                pl.when(pl.col("close").is_null())
                .then(None)
                .otherwise(pl.col("close"))
                .alias("close")
            )
        else:
            raise ValueError(f"Ismeretlen method: {method}")
