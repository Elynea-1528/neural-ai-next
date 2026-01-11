#!/usr/bin/env python3
"""Tick Pipeline validációs szkript.

Ez a szkript:
1. Inicializálja a core komponenseket (config, logger, storage)
2. Betölt mock tick adatokat
3. Futtatja a Resampler-t "tick" timeframe-mal
4. Validálja a resample eredményeket
5. Futtatja a D1 processzort "tick" timeframe-mal
6. Validálja a D1 eredményeket

Használat:
    python scripts/test_tick_pipeline.py

Author: Neural AI Next Team
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock

if TYPE_CHECKING:
    from neural_ai.core.processing.resampler_service.interfaces.resampler_interface import (
        ResamplerInterface,
    )


async def validate_tick_pipeline() -> bool:
    """Tick pipeline teljes validációja.

    Returns:
        bool: Sikeres-e a validáció
    """
    import pandas as pd
    import polars as pl

    from neural_ai.core.processing.factory import create_dimension_processor
    from neural_ai.core.processing.resampler_service.factory import ResamplerServiceFactory

    print("🧬 TICK PIPELINE VALIDÁCIÓ")
    print("=" * 50)

    try:
        # 1. Mock komponensek létrehozása
        print("🔧 Mock komponensek létrehozása...")

        config = MagicMock()
        config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        logger = MagicMock()
        storage = MagicMock()

        print("✅ Mock komponensek sikeresen létrehozva")

        # 2. Mock tick adat generálása
        print("📥 Mock tick adat generálása teszteléshez...")

        # 10 másodperc adatok 1 másodperces frekvenciával

        date_range = pd.date_range(
            start=datetime(2024, 1, 1, 12, 0, 0), end=datetime(2024, 1, 1, 12, 0, 10), freq="1s"
        )

        tick_df = pl.DataFrame(
            {
                "timestamp": date_range,
                "bid": [1.05 + i * 0.001 for i in range(len(date_range))],
                "ask": [1.051 + i * 0.001 for i in range(len(date_range))],
                "bid_volume": [50 + i * 5 for i in range(len(date_range))],
                "ask_volume": [50 + i * 5 for i in range(len(date_range))],
            }
        )

        logger.info(f"Mock tick adat létrehozva: {len(tick_df)} sor")

        # Mock storage read_tick_data metódus
        from unittest.mock import AsyncMock

        storage.read_tick_data = AsyncMock(return_value=tick_df)

        # 3. Resampler létrehozása és futtatása "tick" timeframe-mal
        print("🚀 Resampler futtatása 'tick' timeframe-mal...")

        resampler: ResamplerInterface = ResamplerServiceFactory.create(storage=storage)

        start = datetime(2024, 1, 1, 12, 0, 0)
        end = datetime(2024, 1, 1, 12, 0, 10)

        resampled_df = await resampler.resample(
            symbol="EURUSD", start=start, end=end, timeframe="tick", return_type="polars"
        )

        logger.info(f"Resample kész: {len(resampled_df)} sor")

        # 4. Resample eredmény validáció
        print("✅ Resample eredmény validáció...")
        validation_errors = []

        # Sorok száma megegyezik-e
        if len(resampled_df) != len(tick_df):
            validation_errors.append(
                f"Sorok száma nem egyezik: bemenet {len(tick_df)}, kimenet {len(resampled_df)}"
            )

        # Új oszlopok jelen vannak-e (mid_close)
        required_new_columns = ["mid_close", "spread", "tick_volume"]
        for col in required_new_columns:
            if col not in resampled_df.columns:
                validation_errors.append(f"Új oszlop hiányzik: {col}")

        # Tick volume minden sorban 1
        if "tick_volume" in resampled_df.columns:
            if not (resampled_df["tick_volume"] == 1).all():
                validation_errors.append("Tick volume nem minden sorban 1")

        if not validation_errors:
            print("✅ Resample validáció sikeres!")
            print(f"  • Sorok száma: {len(resampled_df)} (megegyezik a bemenettel)")
            print(f"  • Új oszlopok: {required_new_columns}")

        # 5. D1 processor létrehozása és futtatása "tick" timeframe-mal
        print("🚀 D1 processor futtatása 'tick' timeframe-mal...")

        d1_processor = create_dimension_processor(1, config, logger)

        d1_result_df = d1_processor.process(resampled_df, timeframe="tick")

        logger.info(f"D1 feldolgozás kész: {len(d1_result_df)} sor")

        # 6. D1 eredmény validáció
        print("✅ D1 eredmény validáció...")

        # Log_return megléte
        if "log_return" not in d1_result_df.columns:
            validation_errors.append("log_return oszlop hiányzik")

        # Shadows None kell legyenek tick esetében
        if "upper_shadow" in d1_result_df.columns:
            if not d1_result_df["upper_shadow"].is_null().all():
                validation_errors.append("Upper shadow nem None tick timeframe esetén")

        if "lower_shadow" in d1_result_df.columns:
            if not d1_result_df["lower_shadow"].is_null().all():
                validation_errors.append("Lower shadow nem None tick timeframe esetén")

        # Eredmények kiírása
        if validation_errors:
            print("❌ Validációs hibák:")
            for error in validation_errors:
                print(f"  • {error}")
            return False
        else:
            print("✅ D1 validáció sikeres!")
            print(f"  • Sorok száma: {len(d1_result_df)}")
            print(f"  • Oszlopok: {list(d1_result_df.columns)}")
            return True

    except Exception as e:
        logger.error(f"Hiba a validáció során: {e}", exc_info=True)
        print(f"❌ Hiba: {e}")
        return False


async def main() -> None:
    """Fő függvény."""
    success = await validate_tick_pipeline()
    if success:
        print("\n🎉 TICK PIPELINE VALIDÁCIÓ SIKERES!")
        sys.exit(0)
    else:
        print("\n❌ TICK PIPELINE VALIDÁCIÓ SIKERTELEN!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
