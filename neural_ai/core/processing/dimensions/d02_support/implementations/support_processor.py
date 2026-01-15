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

    def _find_swing_points_close_open(self, df: pl.DataFrame) -> pl.DataFrame:
        """Swing pontok keresése záró/nyitó árak alapján.

        Kiszámolja a gyertya testének top és bottom értékeit mid_open és mid_close alapján,
        majd swing pontokat keres rajtuk gördülő maximum szukcesszióval.

        Args:
            df: Bemeneti Polars DataFrame

        Returns:
            pl.DataFrame: swing_high_body és swing_low_body oszlopokkal kiegészített DataFrame
        """
        swing_window = self.dim_config.get("swing_window", 5)

        # Body definíció: gyertya testének top és bottom (mid_open és mid_close alapján)
        body_top = pl.max_horizontal("mid_open", "mid_close")
        body_bottom = pl.min_horizontal("mid_open", "mid_close")

        # Body swing pontok számítása
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

        return df.with_columns([
            swing_high_body.alias("swing_high_body"),
            swing_low_body.alias("swing_low_body"),
        ])

    def _find_swing_points_high_low(self, df: pl.DataFrame) -> pl.DataFrame:
        """Swing pontok keresése high/low értékeken.

        Swing pontokat keres bid_high és bid_low értékeken gördülő maximum szukcesszióval.

        Args:
            df: Bemeneti Polars DataFrame

        Returns:
            pl.DataFrame: swing_high_wick és swing_low_wick oszlopokkal kiegészített DataFrame
        """
        swing_window = self.dim_config.get("swing_window", 5)

        # Wick swing pontok számítása
        swing_high_wick = (
            pl.when(
                pl.col("bid_high") == pl.col("bid_high").rolling_max(window_size=swing_window, center=True)
            )
            .then(pl.col("bid_high"))
            .otherwise(None)
        )

        swing_low_wick = (
            pl.when(
                pl.col("bid_low") == pl.col("bid_low").rolling_min(window_size=swing_window, center=True)
            )
            .then(pl.col("bid_low"))
            .otherwise(None)
        )

        return df.with_columns([
            swing_high_wick.alias("swing_high_wick"),
            swing_low_wick.alias("swing_low_wick"),
        ])

    def _merge_levels(self, df: pl.DataFrame) -> pl.DataFrame:
        """Szintek összevonása swing pontok alapján.

        Placeholder implementáció: egyszerűen visszaadja a swing high értékeket resistance oszlopban.
        Később ide kerül a súlyozott átlagolás logikája.

        Args:
            df: Bemeneti Polars DataFrame swing pontokkal

        Returns:
            pl.DataFrame: resistance oszloppal kiegészített DataFrame
        """
        # Placeholder: swing high-ok visszaadása resistance-ként
        resistance = pl.coalesce("swing_high_body", "swing_high_wick")

        return df.with_columns(resistance.alias("resistance"))

    def process(self, df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame:
        """Support/Resistance szintek számítása swing pontok alapján.

        Sorban meghívja a privát függvényeket: swing pontok keresése záró/nyitó és high/low alapján,
        majd szintek összevonása. A részeredményeket hozzáadja a DataFrame-hez.

        Args:
            df: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
            timeframe: Időkeret ("H1", "H4", "D1"), default "H1"

        Returns:
            Polars DataFrame a support/resistance szintekkel kiegészítve
        """
        self.logger.debug(f"D2 processzor futtatása: timeframe={timeframe}")

        # Swing pontok keresése záró/nyitó árak alapján
        df = self._find_swing_points_close_open(df)

        # Swing pontok keresése high/low értékeken
        df = self._find_swing_points_high_low(df)

        # Szintek összevonása
        df = self._merge_levels(df)

        # Végső aggregáció és UI által várt oszlopok hozzáadása
        return df.with_columns([
            # Egyszerűsített swing high/low aggregáció
            pl.coalesce("swing_high_body", "swing_high_wick").alias("swing_high"),
            pl.coalesce("swing_low_body", "swing_low_wick").alias("swing_low"),
            # Placeholder support szintek (None egyelőre)
            pl.lit(None).cast(pl.Float64).alias("support"),
        ])

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 2 (D2 dimenzió)
        """
        return 2
