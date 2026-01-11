"""D01PriceProcessor - Alap adatok processzor."""

from typing import TYPE_CHECKING

import polars as pl

from neural_ai.core.processing.dimensions.base import BaseDimensionProcessor

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class D01PriceProcessor(BaseDimensionProcessor):
    """D1 - Alap adatok (Base Data) processzor.

    Feladata az alap pénzügyi adatok biztosítása és validálása.
    Kiválasztja és visszaadja a timestamp, open, high, low, close,
    tick_volume, spread és real_volume oszlopokat.
    """

    def __init__(self, config: "ConfigManagerInterface", logger: "LoggerInterface") -> None:
        """Inicializálja a D1 processzort.

        Args:
            config: Konfigurációs menedzser interfész
            logger: Logger interfész
        """
        super().__init__(config, logger)

    def process(self, df: pl.DataFrame, timeframe: str = "1m") -> pl.DataFrame:
        """Polars Expr alapú dimenzió számítás matematikai transzformációkkal.

        Számítja a log return-ot, rolling Z-score-ot és árnyékokat (shadows).
        Adaptív logika: tick timeframe esetén különbözik az OHLC-tól.

        Args:
            df: Bemeneti Polars DataFrame (már time-aligned OHLCV adatok)
            timeframe: Időkeret ("tick", "1m", stb.), default "1m"

        Returns:
            Polars DataFrame az alap adatokkal és matematikai transzformációkkal
        """
        # Konfiguráció kiolvasása
        z_score_window = self.dim_config.get("z_score_window", 60)
        calc_shadows = self.dim_config.get("calc_shadows", True)

        self.logger.debug(
            f"D1 processzor konfiguráció: z_score_window={z_score_window}, "
            f"calc_shadows={calc_shadows}"
        )

        # Használjuk a bemeneti DataFrame meglévő mid_close oszlopát (Resampler biztosítja)
        # Log return: ln(mid_close / mid_close.shift(1))
        log_return = (pl.col("mid_close") / pl.col("mid_close").shift(1)).log()

        # Rolling Z-score: (log_return - rolling_mean) / rolling_std
        rolling_mean = log_return.rolling_mean(window_size=z_score_window)
        rolling_std = log_return.rolling_std(window_size=z_score_window)
        rolling_z_score = (log_return - rolling_mean) / rolling_std

        # Árnyékok számítása: csak akkor, ha calc_shadows és timeframe != "tick"
        if calc_shadows and timeframe != "tick":
            # Upper shadow: mid_high - max(mid_open, mid_close)
            upper_shadow = pl.col("mid_high") - pl.max_horizontal(
                pl.col("mid_open"), pl.col("mid_close")
            )
            # Lower shadow: min(mid_open, mid_close) - mid_low
            lower_shadow = pl.min_horizontal(pl.col("mid_open"), pl.col("mid_close")) - pl.col(
                "mid_low"
            )
        else:
            # Egyéb esetben None értékekkel töltjük
            upper_shadow = pl.lit(None).cast(pl.Float64)
            lower_shadow = pl.lit(None).cast(pl.Float64)

        # Alap oszlopok kiválasztása
        columns = [
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

        return df.select(columns)

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 1 (D1 dimenzió)
        """
        return 1
