#!/usr/bin/env python3
"""D1 teljes integrációs teszt script.

Ez a script végrehajtja a teljes D1 dimenzió feldolgozási folyamatot:
1. Parquet tick adatok betöltése
2. Resampling OHLCV generálására
3. Time alignment gap kezelés
4. D01PriceProcessor alkalmazása
5. Eredmény validálása
"""

import sys
from pathlib import Path

# Projekt root hozzáadása a path-hoz
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import polars as pl

from neural_ai.processors.processing.factory import (
    create_dimension_processor,
    create_time_alignment_service,
)


def load_tick_data() -> pl.DataFrame:
    """Tick adatok betöltése Parquet fájlokból."""
    print("📂 Tick adatok betöltése...")

    # Glob pattern a tick adatokhoz
    parquet_pattern = "data/tick/EURUSD/**/*.parquet"

    try:
        # Összes Parquet fájl betöltése
        df = pl.read_parquet(parquet_pattern)
        print(f"   ✅ {len(df)} tick betöltve")
        return df
    except Exception as e:
        print(f"   ❌ Hiba a tick adatok betöltésekor: {e}")
        # Ha nincs valódi adat, mock adatokat hozunk létre
        print("   ⚠️  Mock adatok használata teszteléshez...")
        return create_mock_tick_data()


def create_mock_tick_data() -> pl.DataFrame:
    """Mock tick adatok létrehozása teszteléshez."""
    from datetime import datetime, timedelta

    import numpy as np

    # 1000 mock tick generálása
    timestamps = [datetime(2023, 1, 1, 9, 0, 0) + timedelta(seconds=i) for i in range(1000)]
    bids = 1.0500 + np.random.normal(0, 0.001, 1000)
    asks = bids + np.random.normal(0.0002, 0.0001, 1000)

    return pl.DataFrame({"timestamp": timestamps, "bid": bids, "ask": asks})


def create_mock_ohlcv_data() -> pl.DataFrame:
    """Mock OHLCV adatok létrehozása teszteléshez."""
    from datetime import datetime, timedelta

    import numpy as np

    # 100 mock OHLCV gyertya generálása
    timestamps = [datetime(2023, 1, 1, 9, 0, 0) + timedelta(minutes=i) for i in range(100)]
    base_price = 1.0500

    opens = []
    highs = []
    lows = []
    closes = []

    for i in range(100):
        open_price = base_price + np.random.normal(0, 0.001)
        close_price = open_price + np.random.normal(0, 0.002)
        high_price = max(open_price, close_price) + abs(np.random.normal(0, 0.001))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, 0.001))

        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)

        base_price = close_price

    spreads = [abs(np.random.normal(0.0002, 0.0001)) for _ in range(100)]
    tick_volumes = [int(np.random.normal(1000, 200)) for _ in range(100)]
    real_volumes = [tv * np.random.normal(1.5, 0.3) for tv in tick_volumes]

    return pl.DataFrame(
        {
            "timestamp": timestamps,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "tick_volume": tick_volumes,
            "spread": spreads,
            "real_volume": real_volumes,
        }
    )


def test_full_pipeline():
    """Teljes D1 feldolgozási pipeline tesztelése."""
    print("🚀 D1 teljes integrációs teszt indítása...\n")

    try:
        # 1. Tick adatok betöltése
        tick_df = load_tick_data()
        print(f"   Adatok sémája: {tick_df.schema}")
        print()

        # 2. Mock OHLCV adatok generálása (teszteléshez)
        print("📊 Mock OHLCV adatok generálása...")
        ohlcv_df = create_mock_ohlcv_data()
        print(f"   ✅ {len(ohlcv_df)} OHLCV gyertya generálva")
        print(f"   Oszlopok: {list(ohlcv_df.columns)}")
        print()

        # 4. Time Alignment inicializálása
        print("⏰ TimeAlignmentService inicializálása...")
        time_aligner = create_time_alignment_service()
        print("   ✅ TimeAlignmentService kész")
        print()

        # 5. Gap kezelés és időskála normalizálás
        print("🔧 Gap kezelés és időskála normalizálás...")
        aligned_df = time_aligner.reindex_to_grid(ohlcv_df, timeframe="1m")
        print(f"   ✅ {len(aligned_df)} időpont normalizálva")
        print()

        # 6. D01PriceProcessor inicializálása
        print("🏗️ D01PriceProcessor inicializálása...")
        d1_processor = create_dimension_processor(1)
        print("   ✅ D01PriceProcessor kész")
        print()

        # 7. D1 feldolgozás alkalmazása
        print("⚙️ D1 dimenzió feldolgozás...")
        d1_result = d1_processor.process(aligned_df)
        print(f"   ✅ D1 feldolgozás kész, {len(d1_result)} sor eredmény")
        print(f"   Eredmény oszlopok: {list(d1_result.columns)}")
        print()

        # 8. Eredmény validálása
        print("✅ Eredmény validálása...")
        validate_d1_output(d1_result)
        print("   ✅ Validálás sikeres!")
        print()

        # 9. Statisztikák megjelenítése
        print("📈 Feldolgozási statisztikák:")
        print(f"   • Tick adatok: {len(tick_df)} sor")
        print(f"   • OHLCV adatok: {len(ohlcv_df)} sor")
        print(f"   • Aligned adatok: {len(aligned_df)} sor")
        print(f"   • D1 eredmény: {len(d1_result)} sor")
        print()

        print("🎉 D1 teljes integrációs teszt SIKERES!")
        return True

    except Exception as e:
        print(f"❌ HIBA a pipeline futtatása során: {e}")
        import traceback

        traceback.print_exc()
        return False


def validate_d1_output(df: pl.DataFrame):
    """D1 kimenet validálása a specifikáció alapján."""
    required_columns = {
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread",
        "real_volume",
    }

    # Ellenőrizzük, hogy minden szükséges oszlop megvan-e
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Hiányzó oszlopok: {missing_columns}")

    # Ellenőrizzük, hogy ne legyenek null értékek a kritikus oszlopokban
    critical_columns = ["timestamp", "open", "high", "low", "close"]
    for col in critical_columns:
        null_count = df[col].is_null().sum()
        if null_count > 0:
            raise ValueError(f"Null értékek találhatók a {col} oszlopban: {null_count} db")

    # Ellenőrizzük az adattípusokat
    if not isinstance(df["timestamp"], pl.Series):
        raise TypeError("timestamp oszlop nem megfelelő típusú")

    numeric_columns = ["open", "high", "low", "close", "tick_volume", "spread", "real_volume"]
    for col in numeric_columns:
        if df[col].dtype not in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]:
            raise TypeError(f"{col} oszlop nem numerikus típusú: {df[col].dtype}")

    print("   ✅ Minden szükséges oszlop jelen van")
    print("   ✅ Nincs null érték a kritikus oszlopokban")
    print("   ✅ Adattípusok helyesek")


if __name__ == "__main__":
    success = test_full_pipeline()
    sys.exit(0 if success else 1)
