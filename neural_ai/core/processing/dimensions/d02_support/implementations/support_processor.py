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

        # Config validáció
        if "swing_window" not in self.dim_config:
            self.logger.error("swing_window paraméter hiányzik a configból, default 5 használata")
            self.dim_config["swing_window"] = 5

    def _find_swing_points_close_open(self, df: pl.DataFrame) -> pl.DataFrame:
        """Swing pontok keresése záró/nyitó árak alapján.

        Kiszámolja a gyertya testének top és bottom értékeit mid_open és mid_close alapján,
        majd swing pontokat keres rajtuk gördülő maximum szukcesszióval.

        Args:
            df: Bemeneti Polars DataFrame

        Returns:
            pl.DataFrame: swing_high_body és swing_low_body oszlopokkal kiegészített DataFrame
        """
        min_candles = self.dim_config.get("min_candles")
        if min_candles is None:
            self.logger.warning("min_candles paraméter hiányzik a configból, default 5 használata")
            min_candles = 5
        min_candles = cast(int, min_candles)

        # Body definíció: gyertya testének top és bottom (mid_open és mid_close alapján)
        body_top = pl.max_horizontal("mid_open", "mid_close")
        body_bottom = pl.min_horizontal("mid_open", "mid_close")

        # Body swing pontok számítása
        swing_high_body = (
            pl.when(body_top == body_top.rolling_max(window_size=min_candles, center=True))
            .then(body_top)
            .otherwise(None)
        )

        swing_low_body = (
            pl.when(body_bottom == body_bottom.rolling_min(window_size=min_candles, center=True))
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
        min_candles = self.dim_config.get("min_candles")
        if min_candles is None:
            self.logger.warning("min_candles paraméter hiányzik a configból, default 5 használata")
            min_candles = 5
        min_candles = cast(int, min_candles)

        # Wick swing pontok számítása
        swing_high_wick = (
            pl.when(
                pl.col("high")
                == pl.col("high").rolling_max(
                    window_size=min_candles, center=True
                )
            )
            .then(pl.col("high"))
            .otherwise(None)
        )

        swing_low_wick = (
            pl.when(
                pl.col("low")
                == pl.col("low").rolling_min(
                    window_size=min_candles, center=True
                )
            )
            .then(pl.col("low"))
            .otherwise(None)
        )

        return df.with_columns([
            swing_high_wick.alias("swing_high_wick"),
            swing_low_wick.alias("swing_low_wick"),
        ])

    def _merge_levels(self, df: pl.DataFrame) -> pl.DataFrame:
        """Iteratív klaszterezés a swing szintek összevonására.

        Amíg vannak a merge_threshold-nél közelebbi szintpárok, addig ismétli
        a legkisebb távolságú pár megtalálását és összevonását súlyozott
        átlagolással.

        Args:
            df: Polars DataFrame price, weight, type oszlopokkal

        Returns:
            pl.DataFrame: Klaszterezett szintek DataFrame
        """
        if df.is_empty():
            return df

        if df.height > 5000:
            self.logger.warning(
                "Too many swing points for heavy clustering, skipping merge optimization"
            )
            return df

        level_merge = self.dim_config.get("level_merge")
        if level_merge is None:
            self.logger.warning(
                "level_merge paraméter hiányzik a configból, default 0.0005 használata"
            )
            level_merge = 0.0005
        threshold = cast(float, level_merge)

        while True:
            rows = df.to_dicts()
            prices = [r["price"] for r in rows]
            weights = [r["weight"] for r in rows]
            types = [r["type"] for r in rows]

            min_dist = float('inf')
            min_i, min_j = -1, -1

            # Keresd meg a legkisebb távolságú azonos típusú párt
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    if types[i] != types[j]:
                        continue
                    dist = abs(prices[i] - prices[j])
                    if dist <= threshold and dist < min_dist:
                        min_dist = dist
                        min_i, min_j = i, j

            if min_i == -1:
                break  # Nincs több összevonható pár

            # Egyesítés
            p1, w1 = prices[min_i], weights[min_i]
            p2, w2 = prices[min_j], weights[min_j]
            new_price = (p1 * w1 + p2 * w2) / (w1 + w2)
            new_weight = w1 + w2
            new_type = types[min_i]

            # Új lista létrehozása
            new_rows = []
            for idx, row in enumerate(rows):
                if idx not in (min_i, min_j):
                    new_rows.append(row)
            new_rows.append({"price": new_price, "weight": new_weight, "type": new_type})

            df = pl.DataFrame(new_rows)

        return df.sort("price")

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
        strength_window = self.dim_config.get("strength_window")
        if strength_window is None:
            self.logger.warning(
                "strength_window paraméter hiányzik a configból, default 10 használata"
            )
            strength_window = 10
        strength_window = cast(int, strength_window)
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
        min_touches = self.dim_config.get("min_touches")
        if min_touches is None:
            self.logger.warning("min_touches paraméter hiányzik a configból, default 1 használata")
            min_touches = 1
        min_touches = cast(int, min_touches)

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
        volume_confirmation = self.dim_config.get("volume_confirmation")
        if volume_confirmation is None:
            self.logger.warning(
                "volume_confirmation paraméter hiányzik a configból, default False használata"
            )
            volume_confirmation = False
        volume_confirmation = cast(bool, volume_confirmation)
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

        # Swing pontok gyűjtése DataFrame-ként
        swing_data = []
        for row in df.iter_rows(named=True):
            if row.get("swing_high_body") is not None:
                swing_data.append({
                    "price": row["swing_high_body"],
                    "weight": row["vf_high_body"],
                    "type": "high"
                })
            if row.get("swing_low_body") is not None:
                swing_data.append({
                    "price": row["swing_low_body"],
                    "weight": row["vf_low_body"],
                    "type": "low"
                })
            if row.get("swing_high_wick") is not None:
                swing_data.append({
                    "price": row["swing_high_wick"],
                    "weight": row["vf_high_wick"],
                    "type": "high"
                })
            if row.get("swing_low_wick") is not None:
                swing_data.append({
                    "price": row["swing_low_wick"],
                    "weight": row["vf_low_wick"],
                    "type": "low"
                })

        swings_df = pl.DataFrame(swing_data)

        # Szintek összevonása
        merged_df = self._merge_levels(swings_df)

        # Visszaalakítás list[dict]-ra a további feldolgozáshoz
        merged_levels = []
        for row in merged_df.to_dicts():
            level_type = "resistance" if row["type"] == "high" else "support"
            merged_levels.append({
                "price": row["price"],
                "touches": 1,
                "type": level_type,
                "volume_factor": row["weight"]
            })

        # Szintek erősségének számítása
        merged_levels = self._calculate_level_strength(merged_levels)

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
