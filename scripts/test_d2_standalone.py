#!/usr/bin/env python3
"""D2 Support Processor standalone teszt script.

Ez a script közvetlenül teszteli a D02SupportProcessor-t a teljes rendszer megkerülése nélkül.
Bootstrap-peli a core komponenseket, majd betölti és feldolgozza az adatokat.

Használat:
    python scripts/test_d2_standalone.py

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

import polars as pl

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.core import bootstrap_core
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.processors.dimensions.d02_support.factory import D02SupportFactory
from neural_ai.processors.resampler_service.factory import ResamplerServiceFactory

if TYPE_CHECKING:
    pass


async def run_d2_test() -> None:
    """D2 Support Processor standalone teszt futtatása.

    A teszt a következő lépéseket hajtja végre:
    1. Core komponensek inicializálása
    2. Tick adatok betöltése az adatbázisból
    3. Adatok átalakítása H1 OHLCV gyertyákká
    4. D2 Support Processor futtatása
    5. Eredmények kiírása konzolra
    """
    print("🚀 D2 Support Processor Standalone Teszt Indítása...")
    print()

    # 1. Core komponensek inicializálása
    print("⏳ 1. Core komponensek inicializálása...")
    try:
        core = bootstrap_core()
        print("   ✅ Core komponensek inicializálva")
    except Exception as e:
        print(f"   ❌ Hiba a core inicializálásakor: {e}")
        return

    # 2. Tick adatok betöltése
    print("⏳ 2. Tick adatok betöltése...")
    symbol = "EURUSD"
    start_date = datetime(2023, 1, 1, tzinfo=UTC)
    end_date = datetime(2023, 1, 2, tzinfo=UTC)

    try:
        # Castoljuk a storage-t ParquetStorageService-ra
        storage = cast(ParquetStorageService, core.storage)
        df = await storage.read_tick_data(symbol, start_date, end_date)
        if df.is_empty():
            print("   ❌ Nincs elérhető tick adat a megadott időtartományban")
            return
        print(f"   ✅ {len(df)} tick rekord betöltve")
    except Exception as e:
        print(f"   ❌ Hiba az adatok betöltésekor: {e}")
        return

    # 3. Adatok átalakítása H1 OHLCV gyertyákká
    print("⏳ 3. Adatok resample-olása H1 timeframe-re...")
    try:
        if not core.storage:
            raise RuntimeError("Storage nincs inicializálva")
        if not core.logger:
            raise RuntimeError("Logger nincs inicializálva")

        resampler = ResamplerServiceFactory.create(core.storage, core.logger)
        # Privát metódus használata - csak teszt célból
        ohlcv: pl.DataFrame = resampler._convert_to_ohlcv(df, "1h")  # type: ignore

        # OHLCV adatok transzformálása a processor számára
        # A processor "high" és "low" oszlopokat vár a wick swingekhez
        ohlcv = ohlcv.with_columns(
            high=pl.col("bid_high"),
            low=pl.col("bid_low"),
            open=pl.col("bid_open"),
            close=pl.col("bid_close"),
        )

        print(f"   ✅ {len(ohlcv)} H1 gyertya létrehozva")
    except Exception as e:
        print(f"   ❌ Hiba a resample-oláskor: {e}")
        return

    # 4. D2 Support Processor futtatása és új függvények ellenőrzése
    print("⏳ 4. D2 Support Processor futtatása...")
    try:
        if not core.config:
            raise RuntimeError("Config nincs inicializálva")
        if not core.logger:
            raise RuntimeError("Logger nincs inicializálva")

        processor = D02SupportFactory.create(core.config, core.logger)

        # Ellenőrizzük, hogy az új függvények léteznek
        assert hasattr(processor, "_find_swing_points_close_open"), (
            "Hiányzó _find_swing_points_close_open függvény"
        )
        assert hasattr(processor, "_find_swing_points_high_low"), (
            "Hiányzó _find_swing_points_high_low függvény"
        )
        assert hasattr(processor, "_merge_levels"), "Hiányzó _merge_levels függvény"
        print("   ✅ Új függvények ellenőrizve")

        result: pl.DataFrame = processor.process(ohlcv, timeframe="H1")  # type: ignore[call-arg]
        print("   ✅ D2 processor sikeresen lefutott")
    except Exception as e:
        print(f"   ❌ Hiba a processor futtatásakor: {e}")
        return

    # 5. Diagnosztika és eredmények kiírása
    print()
    print("=" * 60)
    print("📊 TESZT EREDMÉNYEK")
    print("=" * 60)

    # Oszlopok listája
    print("📋 Eredmény oszlopok:")
    for i, col in enumerate(result.columns, 1):
        print(f"{i:2d}. {col}")
    print()

    # Swing pontok számlálása
    swing_high_body_count = result["swing_high_body"].drop_nulls().len()
    swing_low_body_count = result["swing_low_body"].drop_nulls().len()
    swing_high_wick_count = result["swing_high_wick"].drop_nulls().len()
    swing_low_wick_count = result["swing_low_wick"].drop_nulls().len()

    print("🎯 Swing pontok:")
    print(f"   Swing High Body: {swing_high_body_count}")
    print(f"   Swing Low Body: {swing_low_body_count}")
    print(f"   Swing High Wick: {swing_high_wick_count}")
    print(f"   Swing Low Wick: {swing_low_wick_count}")
    print()

    # Első 5 sor swing pontokkal
    swing_rows = result.filter(
        pl.col("swing_high_body").is_not_null()
        | pl.col("swing_low_body").is_not_null()
        | pl.col("swing_high_wick").is_not_null()
        | pl.col("swing_low_wick").is_not_null()
    ).head(5)

    if len(swing_rows) > 0:
        print("📈 Első 5 swing ponttal rendelkező sor:")
        print(swing_rows)
    else:
        print("⚠️  Nincs swing pont az adatokban")

    print()
    print("✅ Teszt sikeresen befejezve!")


async def main() -> None:
    """Főprogram belépési pont."""
    print("=" * 60)
    print("🧠 NEURAL AI NEXT - D2 SUPPORT PROCESSOR STANDALONE TEST")
    print("=" * 60)
    print()

    try:
        await run_d2_test()
    except KeyboardInterrupt:
        print()
        print("⚠️  Teszt megszakítva a felhasználó által")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
