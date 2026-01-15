"""D02SupportProcessor - Support/Resistance szintek processzora."""

from typing import TYPE_CHECKING, cast

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

        Swing pontokat keres high és low értékeken gördülő maximum szukcesszióval.

        Args:
            df: Bemeneti Polars DataFrame

        Returns:
            pl.DataFrame: swing_high_wick és swing_low_wick oszlopokkal kiegészített DataFrame
        """
        swing_window = self.dim_config.get("swing_window", 5)

        # Wick swing pontok számítása
        swing_high_wick = (
            pl.when(
                pl.col("high")
                == pl.col("high").rolling_max(
                    window_size=swing_window, center=True
                )
            )
            .then(pl.col("high"))
            .otherwise(None)
        )

        swing_low_wick = (
            pl.when(
                pl.col("low")
                == pl.col("low").rolling_min(
                    window_size=swing_window, center=True
                )
            )
            .then(pl.col("low"))
            .otherwise(None)
        )

        return df.with_columns([
            swing_high_wick.alias("swing_high_wick"),
            swing_low_wick.alias("swing_low_wick"),
        ])

    def _merge_levels(
        self, swings: list[dict[str, float | str]]
    ) -> list[dict[str, float | int | str]]:
        """Szintek összevonása swing pontok alapján súlyozott átlagolással.

        A swing pontokat ár szerint rendezi, majd iteratívan összevonja azokat,
        amelyek a level_merge távolságon belül vannak. Az összevonás során
        súlyozott átlagot számol az árak és volumen faktorok alapján, és összeadja
        az érintéseket (touches).

        Args:
            swings: Swing pontok listája, ahol minden dict tartalmazza:
                - "price": float (ár)
                - "volume_factor": float (volumen faktor)
                - "type": str ("high" vagy "low")

        Returns:
            list[dict[str, float | int | str]]: Összevont szintek listája
                [{"price": float, "touches": int, "type": "support"|"resistance",
                "strength": float}]
        """
        if not swings:
            return []

        # Konfiguráció betöltése
        level_merge = cast(float, self.dim_config.get("level_merge", 0.0005))

        # Rendezés ár szerint
        sorted_swings = sorted(swings, key=lambda x: cast(float, x["price"]))

        merged_levels: list[dict[str, float | int | str]] = []

        for swing in sorted_swings:
            price = cast(float, swing["price"])
            volume_factor = cast(float, swing.get("volume_factor", 1.0))
            swing_type = cast(str, swing["type"])

            # Type mapping: high -> resistance, low -> support
            level_type = "resistance" if swing_type == "high" else "support"

            # Keresés, hogy van-e már közel hasonló árú szint
            found = False
            for level in merged_levels:
                level_price = cast(float, level["price"])
                level_touches = cast(int, level["touches"])
                level_volume_factor = cast(float, level["volume_factor"])
                if abs(level_price - price) <= level_merge:
                    # Súlyozott átlag az áraknak
                    total_volume_factor = level_volume_factor + volume_factor
                    new_price = (level_price * level_volume_factor +
                                 price * volume_factor) / total_volume_factor
                    level["price"] = new_price
                    level["touches"] = level_touches + 1
                    level["volume_factor"] = total_volume_factor
                    level["strength"] = float(level["touches"])  # Strength = touches
                    found = True
                    break

            if not found:
                merged_levels.append({
                    "price": price,
                    "touches": 1,
                    "type": level_type,
                    "strength": 1.0,
                    "volume_factor": volume_factor  # Tároljuk a volume_factor-t az összevonáshoz
                })

        # Eltávolítjuk a volume_factor-t a visszatérésből, mert nem része a specifikációnak
        for level in merged_levels:
            del level["volume_factor"]

        return merged_levels

    def _calculate_level_strength(
        self, levels: list[dict[str, float | int | str]]
    ) -> list[dict[str, float | int | str]]:
        """Szintek erősségének számítása.

        Minden szinthez kiszámolja a strength értéket az érintések, súly és
        volumen tényező alapján, majd normalizálja 0-1 közé.

        Args:
            levels: Szintek listája dict-ekkel, amelyek tartalmazzák 'touches' és
                opcionálisan 'volume_factor'.

        Returns:
            list[dict[str, float | int | str]]: Frissített szintek listája
                'strength' kulccsal.
        """
        base_weight = 0.1
        strength_window = cast(int, self.dim_config.get("strength_window", 10))
        # Használjuk a strength_window-t base_weight módosítására
        base_weight /= strength_window

        # Frissített szintek listája
        updated_levels: list[dict[str, float | int | str]] = []

        for level in levels:
            touches = cast(int, level.get("touches", 1))
            volume_factor = cast(float, level.get("volume_factor", 1.0))
            strength = (touches * base_weight) * volume_factor
            level["strength"] = strength
            updated_levels.append(level)

        # Normalizálás 0-1 közé a teljes listában
        if updated_levels:
            max_strength = max(cast(float, level["strength"]) for level in updated_levels)
            if max_strength > 0:
                for level in updated_levels:
                    level["strength"] = cast(float, level["strength"]) / max_strength

        return updated_levels

    def _categorize_zones(
        self,
        levels: list[dict[str, str | float | int]]
    ) -> dict[str, dict[str, list[dict[str, str | float | int]]]]:
        """Szintek kategorizálása strength és touches alapján.

        A szinteket erősíti support és resistance kategóriákba, majd minden kategóriában
        további alcsoportokba: strong, moderate, weak.

        Args:
            levels: Szintek listája dict-ekkel, melyek tartalmazzák 'strength',
                'touches', 'type' stb.

        Returns:
            dict: Kategorizált szintek struktúrája:
                {
                    "support": {"strong": [...], "moderate": [...], "weak": [...]},
                    "resistance": {"strong": [...], "moderate": [...], "weak": [...]}
                }
        """
        min_touches = cast(int, self.dim_config.get("min_touches", 1))

        result: dict[str, dict[str, list[dict[str, str | float | int]]]] = {
            "support": {"strong": [], "moderate": [], "weak": []},
            "resistance": {"strong": [], "moderate": [], "weak": []}
        }

        for level in levels:
            strength = cast(float, level["strength"])
            touches = cast(int, level["touches"])
            level_type = cast(str, level["type"])

            if strength > 0.7 and touches >= min_touches:
                category = "strong"
            elif 0.3 <= strength <= 0.7 or (touches < min_touches and strength > 0.4):
                category = "moderate"
            else:
                category = "weak"

            result[level_type][category].append(level)

        return result

    def _confirm_with_volume(self, df: pl.DataFrame, swing_mask: pl.Expr) -> pl.Expr:
        """Swing pontok megerősítése volumen alapján.

        Ellenőrzi, hogy a swing pontokon a real_volume nagyobb-e a mozgóátlagnál.
        Ha volume_confirmation false, mindig 1.0-s szorzót ad vissza.

        Args:
            df: Bemeneti Polars DataFrame (nem használt, de konzisztenciáért)
            swing_mask: Swing pontokat jelölő kifejezés

        Returns:
            pl.Expr: Szorzó kifejezés (1.2 ha megerősített, 1.0 ha nem)
        """
        volume_confirmation = cast(dict, self.dim_config).get("volume_confirmation", False)
        if not volume_confirmation:
            return pl.lit(1.0)

        threshold = pl.col("real_volume").rolling_mean(window_size=20) * 1.5
        return (
            pl.when(swing_mask & (pl.col("real_volume") > threshold))
            .then(1.2)
            .otherwise(1.0)
        )

    def process(self, df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame:
        """Support/Resistance szintek számítása swing pontok alapján.

        Detektálja a swingeket Body és Wick alapján, gyűjti őket listába VolumeFactor-ral,
        futtatja a szintek összevonását, erősség számítását és kategorizálását.
        Idősoros vetítés minden gyertyánál a legközelebbi support/resistance-hez.

        Args:
            df: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
            timeframe: Időkeret ("H1", "H4", "D1"), default "H1"

        Returns:
            Polars DataFrame frissített oszlopokkal: swing_high_body, swing_low_body,
            swing_high_wick, swing_low_wick, nearest_resistance, nearest_support,
            resistance_strength, support_strength.
        """
        self.logger.debug(f"D2 processzor futtatása: timeframe={timeframe}")

        # Swing pontok keresése záró/nyitó árak alapján
        df = self._find_swing_points_close_open(df)

        # Swing pontok keresése high/low értékeken
        df = self._find_swing_points_high_low(df)

        # Volume factor számítása minden swing típushoz
        high_body_mask = pl.col("swing_high_body").is_not_null()
        low_body_mask = pl.col("swing_low_body").is_not_null()
        high_wick_mask = pl.col("swing_high_wick").is_not_null()
        low_wick_mask = pl.col("swing_low_wick").is_not_null()

        df = df.with_columns([
            self._confirm_with_volume(df, high_body_mask).alias("vf_high_body"),
            self._confirm_with_volume(df, low_body_mask).alias("vf_low_body"),
            self._confirm_with_volume(df, high_wick_mask).alias("vf_high_wick"),
            self._confirm_with_volume(df, low_wick_mask).alias("vf_low_wick"),
        ])

        # Swing pontok gyűjtése list[dict]-ként
        swings = []
        for row in df.iter_rows(named=True):
            timestamp = row["timestamp"]
            if row.get("swing_high_body") is not None:
                swings.append({
                    "timestamp": timestamp,
                    "price": row["swing_high_body"],
                    "type": "high",
                    "volume_factor": row["vf_high_body"]
                })
            if row.get("swing_low_body") is not None:
                swings.append({
                    "timestamp": timestamp,
                    "price": row["swing_low_body"],
                    "type": "low",
                    "volume_factor": row["vf_low_body"]
                })
            if row.get("swing_high_wick") is not None:
                swings.append({
                    "timestamp": timestamp,
                    "price": row["swing_high_wick"],
                    "type": "high",
                    "volume_factor": row["vf_high_wick"]
                })
            if row.get("swing_low_wick") is not None:
                swings.append({
                    "timestamp": timestamp,
                    "price": row["swing_low_wick"],
                    "type": "low",
                    "volume_factor": row["vf_low_wick"]
                })

        # Szintek összevonása
        merged_levels = self._merge_levels(swings)

        # Szintek erősségének számítása
        merged_levels = self._calculate_level_strength(merged_levels)

        # Szintek kategorizálása
        self._categorize_zones(merged_levels)

        # Support és resistance szintek kinyerése
        support_levels = [level for level in merged_levels if level["type"] == "support"]
        resistance_levels = [level for level in merged_levels if level["type"] == "resistance"]

        # Mapping price -> strength
        support_dict = {level["price"]: level["strength"] for level in support_levels}
        resistance_dict = {level["price"]: level["strength"] for level in resistance_levels}

        # Függvények nearest számításhoz
        def find_nearest_support(close: float) -> tuple[float | None, float | None]:
            candidates = [p for p in support_dict if p <= close]
            if not candidates:
                return None, None
            nearest_price = max(candidates)
            return nearest_price, support_dict[nearest_price]

        def find_nearest_resistance(close: float) -> tuple[float | None, float | None]:
            candidates = [p for p in resistance_dict if p >= close]
            if not candidates:
                return None, None
            nearest_price = min(candidates)
            return nearest_price, resistance_dict[nearest_price]

        # Oszlopok hozzáadása
        nearest_support_expr = pl.col("close").map_elements(
            lambda c: find_nearest_support(c)[0], return_dtype=pl.Float64
        ).alias("nearest_support")
        support_strength_expr = pl.col("close").map_elements(
            lambda c: find_nearest_support(c)[1], return_dtype=pl.Float64
        ).alias("support_strength")
        nearest_resistance_expr = pl.col("close").map_elements(
            lambda c: find_nearest_resistance(c)[0], return_dtype=pl.Float64
        ).alias("nearest_resistance")
        resistance_strength_expr = pl.col("close").map_elements(
            lambda c: find_nearest_resistance(c)[1], return_dtype=pl.Float64
        ).alias("resistance_strength")

        df = df.with_columns([
            nearest_support_expr,
            support_strength_expr,
            nearest_resistance_expr,
            resistance_strength_expr,
        ])

        # Ideiglenes oszlopok eltávolítása
        return df.drop(["vf_high_body", "vf_low_body", "vf_high_wick", "vf_low_wick"])

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 2 (D2 dimenzió)
        """
        return 2
