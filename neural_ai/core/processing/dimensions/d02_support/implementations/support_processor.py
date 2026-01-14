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
        """Support/Resistance szintek számítása swing pontok alapján body és wick számára.

        Swing high és low pontokat keres különböző ablakméretekkel body (középső)
        és wick (teljes) részeire, majd ezek alapján számítja a külön support és
        resistance szinteket.

        Args:
            df: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
            timeframe: Időkeret ("H1", "H4", "D1"), default "H1"

        Returns:
            Polars DataFrame a support/resistance szintekkel kiegészítve (8 új oszlop)
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

        # Body swing pontok számítása (középső rész: mid_high, mid_low)
        swing_high_body = (
            pl.when(pl.col("mid_high") == pl.col("mid_high").rolling_max(window_size=swing_window))
            .then(pl.col("mid_high"))
            .otherwise(None)
        )

        swing_low_body = (
            pl.when(pl.col("mid_low") == pl.col("mid_low").rolling_min(window_size=swing_window))
            .then(pl.col("mid_low"))
            .otherwise(None)
        )

        # Wick swing pontok számítása (teljes rész: high, low)
        swing_high_wick = (
            pl.when(pl.col("high") == pl.col("high").rolling_max(window_size=swing_window))
            .then(pl.col("high"))
            .otherwise(None)
        )

        swing_low_wick = (
            pl.when(pl.col("low") == pl.col("low").rolling_min(window_size=swing_window))
            .then(pl.col("low"))
            .otherwise(None)
        )

        # Aggregált szintek body számára
        resistance_body = swing_high_body.rolling_mean(window_size=min_distance * 2).alias(
            "resistance_body"
        )
        support_body = swing_low_body.rolling_mean(window_size=min_distance * 2).alias(
            "support_body"
        )

        # Aggregált szintek wick számára
        resistance_wick = swing_high_wick.rolling_mean(window_size=min_distance * 2).alias(
            "resistance_wick"
        )
        support_wick = swing_low_wick.rolling_mean(window_size=min_distance * 2).alias(
            "support_wick"
        )

        # Swing pontok boolean flag-ek
        swing_high_body_flag = swing_high_body.is_not_null().alias("swing_high_body")
        swing_low_body_flag = swing_low_body.is_not_null().alias("swing_low_body")
        swing_high_wick_flag = swing_high_wick.is_not_null().alias("swing_high_wick")
        swing_low_wick_flag = swing_low_wick.is_not_null().alias("swing_low_wick")

        # Eredmény dataframe visszaadása az új oszlopokkal
        return df.with_columns(
            [
                swing_high_body_flag,
                swing_low_body_flag,
                swing_high_wick_flag,
                swing_low_wick_flag,
                resistance_body,
                support_body,
                resistance_wick,
                support_wick,
            ]
        )

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 2 (D2 dimenzió)
        """
        return 2
