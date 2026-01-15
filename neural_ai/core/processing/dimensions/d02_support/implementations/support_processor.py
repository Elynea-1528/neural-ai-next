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

        # Body definíció: gyertya testének top és bottom (mid_open és mid_close alapján)
        body_top = pl.max_horizontal("mid_open", "mid_close")
        body_bottom = pl.min_horizontal("mid_open", "mid_close")

        # Body swing pontok számítása (középső rész: body_top, body_bottom)
        swing_high_body = (
            pl.when(body_top == body_top.rolling_max(window_size=swing_window, center=True))
            .then(body_top)
            .otherwise(None)
        )

        swing_low_body = (
            pl.when(body_bottom == body_bottom.rolling_min(window_size=swing_window, center=True))
            .then(body_bottom)
            .otherwise(None)
        )

        # Wick swing pontok számítása (teljes rész: high, low)
        swing_high_wick = (
            pl.when(
                pl.col("high") == pl.col("high").rolling_max(window_size=swing_window, center=True)
            )
            .then(pl.col("high"))
            .otherwise(None)
        )

        swing_low_wick = (
            pl.when(
                pl.col("low") == pl.col("low").rolling_min(window_size=swing_window, center=True)
            )
            .then(pl.col("low"))
            .otherwise(None)
        )

        # Eredmény dataframe visszaadása a swing pontokkal (konkrét árak vagy None)
        return df.with_columns(
            [
                swing_high_body.alias("swing_high_body"),
                swing_low_body.alias("swing_low_body"),
                swing_high_wick.alias("swing_high_wick"),
                swing_low_wick.alias("swing_low_wick"),
            ]
        )

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 2 (D2 dimenzió)
        """
        return 2
