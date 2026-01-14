"""D02SupportProcessor - Support/Resistance szintek processzora."""

from typing import TYPE_CHECKING

import polars as pl

from neural_ai.core.processing.dimensions.base import BaseDimensionProcessor

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class D02SupportProcessor(BaseDimensionProcessor):
    """D2 - Support/Resistance szintek processzora.

    Feladata a support és resistance szintek azonosítása és számítása
    swing pontok alapján különböző timeframe-ekre.
    """

    def __init__(self, config: "ConfigManagerInterface", logger: "LoggerInterface") -> None:
        """Inicializálja a D2 processzort.

        Args:
            config: Konfigurációs menedzser interfész
            logger: Logger interfész
        """
        super().__init__(config, logger)

    def process(self, df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame:
        """Support/Resistance szintek számítása swing pontok alapján.

        Swing high és low pontokat keres különböző ablakméretekkel,
        majd ezek alapján számítja a support és resistance szinteket.

        Args:
            df: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
            timeframe: Időkeret ("H1", "H4", "D1"), default "H1"

        Returns:
            Polars DataFrame a support/resistance szintekkel kiegészítve
        """
        # Konfiguráció kiolvasása
        swing_window = self.dim_config.get("swing_window", 5)
        min_distance = self.dim_config.get("min_distance", 10)

        # Timeframe specifikus felülírás
        tf_configs = self.dim_config.get("timeframe_configs", {})
        for tf_key, tf_cfg in tf_configs.items():
            if tf_key.lower() == timeframe.lower():
                swing_window = tf_cfg.get("swing_window", swing_window)
                min_distance = tf_cfg.get("min_distance", min_distance)
                break

        self.logger.debug(f"D2 processzor futtatása: timeframe={timeframe}, window={swing_window}")

        # Swing pontok számítása
        swing_highs = (
            pl.when(pl.col("mid_high") == pl.col("mid_high").rolling_max(window_size=swing_window))
            .then(pl.col("mid_high"))
            .otherwise(None)
        )

        swing_lows = (
            pl.when(pl.col("mid_low") == pl.col("mid_low").rolling_min(window_size=swing_window))
            .then(pl.col("mid_low"))
            .otherwise(None)
        )

        # Support és resistance szintek aggregálása
        # Resistance: swing high-ok átlaga (felső szintek)
        resistance_levels = swing_highs.rolling_mean(window_size=min_distance * 2).alias(
            "resistance"
        )

        # Support: swing low-ok átlaga (alsó szintek)
        support_levels = swing_lows.rolling_mean(window_size=min_distance * 2).alias("support")

        # Swing pontok boolean flag-ek
        swing_high_flag = swing_highs.is_not_null().alias("swing_high")
        swing_low_flag = swing_lows.is_not_null().alias("swing_low")

        # Eredmény dataframe visszaadása az új oszlopokkal
        return df.with_columns(
            [
                swing_high_flag,
                swing_low_flag,
                resistance_levels,
                support_levels,
            ]
        )

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 2 (D2 dimenzió)
        """
        return 2
