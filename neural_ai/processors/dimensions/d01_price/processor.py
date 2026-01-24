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

        # Market Hours szűrés és logolás
        market_hours_config = self.dim_config.get("market_hours", {})
        if market_hours_config.get("enabled", False):
            enabled_weekdays = market_hours_config.get(
                "weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            )
            hours_range = market_hours_config.get("hours", ["00:00", "23:59"])
            market_hours_config.get("timezone", "UTC")

            # Számoljuk a market hours-on kívüli sorokat
            total_rows = len(df)
            if total_rows > 0:
                # Polars expr a market hours ellenőrzéshez
                weekday_expr = (
                    pl.col("timestamp")
                    .dt.weekday()
                    .replace_strict(
                        {
                            1: "Monday",
                            2: "Tuesday",
                            3: "Wednesday",
                            4: "Thursday",
                            5: "Friday",
                            6: "Saturday",
                            7: "Sunday",
                        }
                    )
                    .is_in(enabled_weekdays)
                )

                # Óra és perc ellenőrzés
                start_hour, start_min = map(int, hours_range[0].split(":"))
                end_hour, end_min = map(int, hours_range[1].split(":"))
                start_time_minutes = start_hour * 60 + start_min
                end_time_minutes = end_hour * 60 + end_min

                time_minutes = pl.col("timestamp").dt.hour() * 60 + pl.col("timestamp").dt.minute()
                time_in_range = (time_minutes >= start_time_minutes) & (
                    time_minutes <= end_time_minutes
                )

                market_hours_mask = weekday_expr & time_in_range
                outside_market_hours_count = (
                    df.select((~market_hours_mask).sum().alias("outside")).select("outside").item()
                )

                if outside_market_hours_count > 0 and market_hours_config.get(
                    "log_filtering", False
                ):
                    self.logger.info(
                        "Market hours szűrés eredménye",
                        total_rows=total_rows,
                        outside_market_hours=outside_market_hours_count,
                        timeframe=timeframe,
                        symbol="N/A",  # TODO: symbol hozzáadása ha elérhető
                    )

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
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            # Metadata
            "tick_volume",
            "spread",
            "real_volume",
            # Számított értékek
            log_return.alias("log_return"),
            rolling_z_score.alias("rolling_z_score"),
            upper_shadow.alias("upper_shadow"),
            lower_shadow.alias("lower_shadow"),
        ]

        # Eredeti tick oszlopok hozzáadása, ha rendelkezésre állnak (tick timeframe esetén)
        if "bid" in df.columns:
            columns.append(pl.col("bid"))
        if "ask" in df.columns:
            columns.append(pl.col("ask"))
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
