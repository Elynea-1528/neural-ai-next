#!/usr/bin/env python3
"""Feature Pipeline teszt szkript.

Ez a szkript végigmegy a teljes feature pipeline-on:
1. Storage-ból adat betöltés
2. Resampler futtatása (Mid OHLC generálás)
3. Time Alignment futtatása (Hétvége szűrés)
4. D1 Processor futtatása (Z-Score számítás)
5. Eredmények ellenőrzése

Használat:
    python scripts/test_feature_pipeline.py

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.core import bootstrap_core
from neural_ai.core.processing.factory import (
    create_dimension_processor,
    create_time_alignment_service,
)
from neural_ai.core.processing.resampler_service.implementations.resampler_service import (
    ResamplerService,
)


async def main() -> None:
    """Fő teszt folyamat."""
    print("=" * 60)
    print("🧠 NEURAL AI NEXT - FEATURE PIPELINE TEST")
    print("=" * 60)
    print()

    try:
        # Core inicializálása
        print("⏳ Rendszer inicializálása...")
        core = bootstrap_core()
        if core.storage is None:
            print("❌ Storage nem érhető el")
            return
        storage = core.storage
        resampler = ResamplerService(storage)
        time_alignment = create_time_alignment_service()
        d1_processor = create_dimension_processor(1)
        print("✅ Core komponensek inicializálva")
        print()

        # 1. Adat betöltés storage-ból
        print("📥 1. lépés: Adat betöltés storage-ból")
        symbol = "EURUSD"
        start = datetime(2024, 3, 20, tzinfo=UTC)
        end = datetime(2024, 3, 20, tzinfo=UTC)

        tick_data = await storage.read_tick_data(symbol, start, end)
        if tick_data is None or tick_data.is_empty():
            print("❌ Nincs elérhető tick adat")
            return

        print(f"✅ {len(tick_data)} tick rekord betöltve")
        print(f"   Oszlopok: {list(tick_data.columns)}")
        print("   Első 3 sor:")
        print(tick_data.head(3))
        print()

        # Ellenőrzés: nincs volume oszlop a forrásban
        if "volume" in tick_data.columns:
            print("❌ HIBA: Volume oszlop jelen van a forrásban!")
            return
        print("✅ Volume oszlop nincs jelen a forrásban")
        print()

        # 2. Resampler futtatása
        print("🔄 2. lépés: Resampler futtatása (Mid OHLC generálás)")
        ohlc_data = await resampler.resample(
            symbol, start, end, timeframe="1m", return_type="polars"
        )

        if ohlc_data is None or ohlc_data.is_empty():
            print("❌ Resampler hiba")
            return

        print(f"✅ {len(ohlc_data)} OHLC rekord generálva")
        print(f"   Oszlopok: {list(ohlc_data.columns)}")
        print("   Első 3 sor:")
        print(ohlc_data.head(3))
        print()

        # 3. Time Alignment futtatása
        print("⏳ 3. lépés: Time Alignment futtatása (Hétvége szűrés)")

        # Hétvége szűrés
        aligned_data = time_alignment.market_hours_filter(ohlc_data)

        # Gap kezelés
        aligned_data = time_alignment.handle_gaps(aligned_data)

        if aligned_data is None or aligned_data.is_empty():
            print("❌ Time Alignment hiba")
            return

        print(f"✅ {len(aligned_data)} rekord időszinkronizálva (hétvégék szűrve)")
        print(f"   Oszlopok: {list(aligned_data.columns)}")
        print("   Első 3 sor:")
        print(aligned_data.head(3))
        print()

        # 4. D1 Processor futtatása
        print("🧮 4. lépés: D1 Processor futtatása (Z-Score számítás)")
        final_data = d1_processor.process(aligned_data)

        if final_data is None or final_data.is_empty():
            print("❌ D1 Processor hiba")
            return

        print(f"✅ {len(final_data)} rekord feldolgozva (Z-Score hozzáadva)")
        print(f"   Oszlopok: {list(final_data.columns)}")
        print("   Első 5 sor:")
        print(final_data.head(5))
        print()

        # 5. Eredmények ellenőrzése
        print("🔍 5. lépés: Eredmények ellenőrzése")

        # Z-Score jelen van
        if "rolling_z_score" not in final_data.columns:
            print("❌ HIBA: rolling_z_score oszlop hiányzik!")
            return

        # Z-Score értékek ellenőrzése
        z_scores = final_data["rolling_z_score"].drop_nulls()
        if z_scores.is_empty():
            print("❌ HIBA: Nincs érvényes Z-Score érték!")
            return

        print(f"✅ Z-Score oszlop jelen van, {len(z_scores)} érvényes érték")
        print(".4f.4f.4f")

        # Mid_close jelen van
        if "mid_close" not in final_data.columns:
            print("❌ HIBA: mid_close oszlop hiányzik!")
            return

        print("✅ Mid_close oszlop jelen van")
        print()

        # Sikeres befejezés
        print("=" * 60)
        print("🎉 FEATURE PIPELINE TEST SIKERES!")
        print("=" * 60)
        print("✅ Nincs volume oszlop a forrásban")
        print("✅ Z-Score oszlop hozzáadva a kimenetben")
        print("✅ Pipeline teljes refaktorálása helyesen működik")

    except Exception as e:
        print(f"❌ Hiba a teszt során: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Teszt megszakítva")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        sys.exit(1)
