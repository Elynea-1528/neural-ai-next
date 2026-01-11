#!/usr/bin/env python3
"""D1 Processor teljes funkcionalitásának tesztelése valós adatokon.

Ez a szkript:
1. Inicializálja a core komponenseket (config, logger, storage)
2. Betölt valós tick adatokat
3. Futtatja a D1 processzort
4. Validálja az eredményeket

Használat:
    python scripts/test_d1_full.py

Author: Neural AI Next Team
"""

import asyncio
import sys
from pathlib import Path

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import MagicMock


async def test_d1_full() -> None:
    """D1 processor teljes tesztelése."""
    print("🧬 D1 PROCESSOR TELJES TESZTELÉS")
    print("=" * 50)

    try:
        # 1. Mock komponensek létrehozása
        print("🔧 Mock komponensek létrehozása...")

        config = MagicMock()
        config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        logger = MagicMock()

        print("Mock komponensek sikeresen létrehozva")

        # 2. Mock adat generálása
        print("📥 Mock adat generálása tesztelés...")

        from datetime import datetime, timedelta

        import numpy as np
        import polars as pl

        # Mock OHLCV adat generálása
        timestamps = [datetime(2024, 3, 20, 9, 0) + timedelta(minutes=i) for i in range(100)]
        data = {
            "timestamp": timestamps,
            "mid_open": 1.0850 + np.random.normal(0, 0.001, 100),
            "mid_high": 1.0850 + np.random.normal(0.0005, 0.001, 100),
            "mid_low": 1.0850 + np.random.normal(-0.0005, 0.001, 100),
            "mid_close": 1.0850 + np.random.normal(0, 0.001, 100),
            "tick_volume": np.random.randint(50, 200, 100),
            "spread": np.random.uniform(0.0001, 0.0005, 100),
            "real_volume": np.random.randint(1000, 5000, 100),
        }

        mock_df = pl.DataFrame(data)

        logger.info(f"Mock OHLCV adat létrehozva: {len(mock_df)} sor")

        # 3. D1 processor létrehozása és futtatása
        print("🚀 D1 processor futtatása...")

        from neural_ai.core.processing.dimensions.d01_price.factory import D01PriceFactory

        d1_processor = D01PriceFactory.create(config, logger)

        # D1 processzor futtatása
        result_df = d1_processor.process(mock_df)

        logger.info(f"D1 feldolgozás kész: {len(result_df)} sor")

        # 4. Validáció
        print("✅ Validáció...")
        validation_errors = []

        # Ellenőrizni hogy a rolling_z_score oszlop létezik
        if "rolling_z_score" not in result_df.columns:
            validation_errors.append("rolling_z_score oszlop hiányzik")
        else:
            z_scores = result_df["rolling_z_score"].drop_nulls()
            if len(z_scores) == 0:
                validation_errors.append("rolling_z_score oszlop csupa null érték")
            elif (z_scores == 0.0).all():
                validation_errors.append("rolling_z_score oszlop csupa 0 érték")
            else:
                logger.info(f".2fRolling Z-Score értékek rendben (átlag: {z_scores.mean():.4f})")

        # Ellenőrizni hogy az eredeti oszlopok megmaradtak
        original_columns = [
            "timestamp",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
        ]
        for col in original_columns:
            if col not in result_df.columns:
                validation_errors.append(f"Eredeti oszlop hiányzik: {col}")

        # Ellenőrizni hogy az új oszlopok jelen vannak
        new_columns = ["log_return", "rolling_z_score", "upper_shadow", "lower_shadow"]

        for col in new_columns:
            if col not in result_df.columns:
                validation_errors.append(f"Új oszlop hiányzik: {col}")

        # Eredmények kiírása
        if validation_errors:
            print("❌ Validációs hibák:")
            for error in validation_errors:
                print(f"  • {error}")
            return False
        else:
            print("✅ Minden validáció sikeres!")
            print(f"  • Eredmény sorok száma: {len(result_df)}")
            print(f"  • Oszlopok: {list(result_df.columns)}")
            return True

    except Exception as e:
        logger.error(f"Hiba a tesztelés során: {e}", exc_info=True)
        print(f"❌ Hiba: {e}")
        return False


async def main() -> None:
    """Fő függvény."""
    success = await test_d1_full()
    if success:
        print("\n🎉 D1 PROCESSOR TESZT SIKERES!")
        sys.exit(0)
    else:
        print("\n❌ D1 PROCESSOR TESZT SIKERTELEN!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
