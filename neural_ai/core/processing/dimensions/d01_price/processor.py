"""D01PriceProcessor - Alap adatok processzor."""

from typing import TYPE_CHECKING

import polars as pl

from neural_ai.core.processing.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    pass


class D01PriceProcessor(IDimensionProcessor):
    """D1 - Alap adatok (Base Data) processzor.

    Feladata az alap pénzügyi adatok biztosítása és validálása.
    Kiválasztja és visszaadja a timestamp, open, high, low, close,
    tick_volume, spread és real_volume oszlopokat.
    """

    def process(self, df: pl.DataFrame) -> pl.DataFrame:
        """Polars Expr alapú dimenzió számítás matematikai transzformációkkal.

        Számítja a log return-ot, rolling Z-score-ot és árnyékokat (shadows).

        Args:
            df: Bemeneti Polars DataFrame (már time-aligned OHLCV adatok)

        Returns:
            Polars DataFrame az alap adatokkal és matematikai transzformációkkal
        """
        # Használjuk a bemeneti DataFrame meglévő mid_close oszlopát (Resampler biztosítja)
        # Log return: ln(mid_close / mid_close.shift(1))
        log_return = (pl.col("mid_close") / pl.col("mid_close").shift(1)).log()

        # Rolling Z-score: (log_return - log_return.rolling_mean(60)) / log_return.rolling_std(60)
        rolling_mean = log_return.rolling_mean(window_size=60)
        rolling_std = log_return.rolling_std(window_size=60)
        rolling_z_score = (log_return - rolling_mean) / rolling_std

        # Shadows: Árnyékok mérete
        # Upper shadow: mid_high - max(mid_open, mid_close)
        upper_shadow = pl.col("mid_high") - pl.max_horizontal(
            pl.col("mid_open"), pl.col("mid_close")
        )
        # Lower shadow: min(mid_open, mid_close) - mid_low
        lower_shadow = pl.min_horizontal(pl.col("mid_open"), pl.col("mid_close")) - pl.col(
            "mid_low"
        )

        return df.select(
            [
                "timestamp",
                "mid_open",
                "mid_high",
                "mid_low",
                "mid_close",
                "tick_volume",
                "spread",
                "real_volume",
                log_return.alias("log_return"),
                rolling_z_score.alias("rolling_z_score"),
                upper_shadow.alias("upper_shadow"),
                lower_shadow.alias("lower_shadow"),
            ]
        )

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 1 (D1 dimenzió)
        """
        return 1
