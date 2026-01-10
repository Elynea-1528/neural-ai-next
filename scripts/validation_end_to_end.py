#!/usr/bin/env python3
"""End-to-End validációs szkript a CORE DATA PIPELINE teljes refaktorálásának ellenőrzésére.

Ez a szkript végrehajtja az összes szükséges lépést a pipeline validálására:
1. Adat letöltés egy napra (EURUSD 2024-03-20)
2. Dashboard indításának ellenőrzése
3. Adatok ellenőrzése a Strategy Service-en keresztül
4. Új oszlopok (mid_open, mid_close, spread, rolling_z_score) validálása

Használat:
    python scripts/validation_end_to_end.py

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.ui.services.strategy_service import StrategyService

if TYPE_CHECKING:
    from pandas import DataFrame


def download_data() -> bool:
    """Adat letöltés futtatása EURUSD 2024-03-20-ra.

    Returns:
        bool: Sikeres volt-e a letöltés
    """
    print("📥 Adat letöltés indítása: EURUSD 2024-03-20")

    try:
        # Download szkript futtatása
        cmd = [
            "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
            "scripts/download_history.py",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-20",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print("✅ Adat letöltés sikeres")
            return True
        else:
            print(f"❌ Adat letöltés sikertelen: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Adat letöltés timeout")
        return False
    except Exception as e:
        print(f"❌ Hiba az adat letöltésekor: {e}")
        return False


def test_dashboard_startup() -> bool:
    """Dashboard indításának tesztelése.

    Returns:
        bool: Sikeres volt-e az indítás
    """
    print("🖥️ Dashboard indítás tesztelése (headless mód)")

    try:
        # Dashboard indítása headless-ben
        cmd = [
            "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
            "main.py",
            "dashboard",
            "--headless",
        ]

        # Indítás 10 másodperces timeout-al
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Várunk 5 másodpercet az indulásra
        time.sleep(5)

        # Ellenőrizzük, hogy még fut-e
        if process.poll() is None:
            print("✅ Dashboard sikeresen indult")
            # Leállítjuk
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Dashboard leállítva")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️ Dashboard erőszakkal leállítva")
            return True
        else:
            _, stderr = process.communicate()
            print(f"❌ Dashboard indítása sikertelen: {stderr}")
            return False

    except Exception as e:
        print(f"❌ Hiba a dashboard indításakor: {e}")
        return False


async def validate_data() -> bool:
    """Adatok validálása a Strategy Service-en keresztül.

    Returns:
        bool: Sikeres volt-e a validáció
    """
    print("🔍 Adatok validálása Strategy Service-en keresztül")

    try:
        # Strategy Service példányosítása
        strategy_service = StrategyService()

        # Adatok lekérése
        candles: DataFrame = await strategy_service.get_candles(
            symbol="EURUSD", date="2024-03-20", timeframe="1m"
        )

        if candles is None or candles.empty:
            print("❌ Nincs elérhető adat")
            return False

        print(f"✅ {len(candles)} gyertya adat betöltve")

        # Oszlopnevek normalizálása
        df = candles.copy()
        df.columns = [col.lower() for col in df.columns]

        # Kötelező oszlopok ellenőrzése
        required_columns = ["timestamp", "open", "high", "low", "close"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Hiányzó kötelező oszlopok: {missing_columns}")
            return False

        # Új oszlopok ellenőrzése
        new_columns = ["mid_open", "mid_high", "mid_low", "mid_close", "spread", "rolling_z_score"]
        missing_new_columns = [col for col in new_columns if col not in df.columns]
        if missing_new_columns:
            print(f"❌ Hiányzó új oszlopok: {missing_new_columns}")
            return False

        print(f"✅ Minden új oszlop jelen van: {new_columns}")

        # Adatok minőségének ellenőrzése

        # Spread ellenőrzése: nem NaN, nem 0
        if "spread" in df.columns:
            spread_values = df["spread"].dropna()
            if spread_values.empty:
                print("❌ Spread oszlop üres vagy csak NaN értékek")
                return False
            if (spread_values == 0).all():
                print("❌ Spread oszlop csak 0 értékeket tartalmaz")
                return False
            print(f"✅ Spread értékek rendben (átlag: {spread_values.mean():.6f})")

        # Z-Score ellenőrzése: nem NaN, nem 0
        if "rolling_z_score" in df.columns:
            zscore_values = df["rolling_z_score"].dropna()
            if zscore_values.empty:
                print("❌ Rolling Z-Score oszlop üres vagy csak NaN értékek")
                return False
            if (zscore_values == 0).all():
                print("❌ Rolling Z-Score oszlop csak 0 értékeket tartalmaz")
                return False
            print(f"✅ Z-Score értékek rendben (átlag: {zscore_values.mean():.6f})")

        # Mid árak ellenőrzése
        mid_columns = ["mid_open", "mid_high", "mid_low", "mid_close"]
        for col in mid_columns:
            if col in df.columns:
                values = df[col].dropna()
                if values.empty or (values == 0).all():
                    print(f"❌ {col} oszlop üres vagy csak 0 értékek")
                    return False
                print(f"✅ {col} értékek rendben")

        # Bid/Mid váltás szimuláció (adat szinten)
        # Ellenőrizzük, hogy a mid oszlopok különböznek a bid-től (ha van)
        if "open" in df.columns and "mid_open" in df.columns:
            bid_open = df["open"]
            mid_open = df["mid_open"]
            if (bid_open == mid_open).all():
                print("⚠️ Figyelem: bid_open és mid_open azonos értékek (ez lehet normális)")
            else:
                print("✅ Bid és Mid árak különböznek")

        print("✅ Minden adat validáció sikeres")
        return True

    except Exception as e:
        print(f"❌ Hiba az adatok validálása közben: {e}")
        return False


async def main() -> None:
    """Fő validációs folyamat."""
    print("=" * 70)
    print("🧠 NEURAL AI NEXT - END-TO-END VALIDÁCIÓ")
    print("=" * 70)
    print()

    success_count = 0
    total_steps = 3

    # 1. Adat letöltés
    if download_data():
        success_count += 1
    else:
        print("❌ Validáció sikertelen az adat letöltésnél")
        return

    # 2. Dashboard indítás tesztelése
    if test_dashboard_startup():
        success_count += 1
    else:
        print("❌ Validáció sikertelen a dashboard indításnál")
        return

    # 3. Adatok validálása
    if await validate_data():
        success_count += 1
    else:
        print("❌ Validáció sikertelen az adatok validálásánál")
        return

    print()
    print("=" * 70)
    print("📊 VALIDÁCIÓ EREDMÉNYE")
    print("=" * 70)
    print(f"✅ Sikeres lépések: {success_count}/{total_steps}")

    if success_count == total_steps:
        print("🎉 END-TO-END VALIDÁCIÓ SIKERES!")
        print("A CORE DATA PIPELINE teljes refaktorálása helyesen működik.")
    else:
        print("❌ Validáció részben vagy teljesen sikertelen.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Validáció megszakítva")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        sys.exit(1)
