"""D01PriceProcessor - Alap adatok processzor."""

from typing import TYPE_CHECKING

import polars as pl

from neural_ai.processors.dimensions.base import BaseDimensionProcessor

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
        # Alapértelmezett config
        z_score_window = self.dim_config.get("z_score_window", 60)

        # Timeframe specifikus felülírás
        if timeframe:
            tf_configs = self.dim_config.get("timeframe_configs", {})
            for tf_key, tf_cfg in tf_configs.items():
                if tf_key.lower() == timeframe.lower():
                    z_score_window = tf_cfg.get("z_score_window", z_score_window)
                    break

        calc_shadows = self.dim_config.get("calc_shadows", True)

        self.logger.debug(
            f"D1 processzor futtatása: timeframe={timeframe}, window={z_score_window}"
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

        # Bid és ask adatok számítása spread alapján (ha nincs már bid)
        if "bid_open" not in df.columns:
            bid_open = pl.col("mid_open") - (pl.col("spread") / 2)
            bid_high = pl.col("mid_high") - (pl.col("spread") / 2)
            bid_low = pl.col("mid_low") - (pl.col("spread") / 2)
            bid_close = pl.col("mid_close") - (pl.col("spread") / 2)
        else:
            bid_open = pl.col("bid_open")
            bid_high = pl.col("bid_high")
            bid_low = pl.col("bid_low")
            bid_close = pl.col("bid_close")

        if "ask_open" not in df.columns:
            ask_open = pl.col("mid_open") + (pl.col("spread") / 2)
            ask_high = pl.col("mid_high") + (pl.col("spread") / 2)
            ask_low = pl.col("mid_low") + (pl.col("spread") / 2)
            ask_close = pl.col("mid_close") + (pl.col("spread") / 2)
        else:
            ask_open = pl.col("ask_open")
            ask_high = pl.col("ask_high")
            ask_low = pl.col("ask_low")
            ask_close = pl.col("ask_close")

        # Alap oszlopok kiválasztása
        columns = [
            "timestamp",
            # Bid adatok
            bid_open.alias("bid_open"),
            bid_high.alias("bid_high"),
            bid_low.alias("bid_low"),
            bid_close.alias("bid_close"),
            # Ask adatok
            ask_open.alias("ask_open"),
            ask_high.alias("ask_high"),
            ask_low.alias("ask_low"),
            ask_close.alias("ask_close"),
            # Mid adatok
            "mid_open", "mid_high", "mid_low", "mid_close",
            # Metadata
            "tick_volume", "spread", "real_volume",
            # Számított értékek
            log_return.alias("log_return"),
            rolling_z_score.alias("rolling_z_score"),
            upper_shadow.alias("upper_shadow"),
            lower_shadow.alias("lower_shadow"),
        ]

        # Bid és ask volume hozzáadása, ha rendelkezésre állnak
        if "bid_volume" in df.columns:
            columns.append(pl.col("bid_volume"))
        if "ask_volume" in df.columns:
            columns.append(pl.col("ask_volume"))

        return df.select(columns)

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 1 (D1 dimenzió)
        """
        return 1
