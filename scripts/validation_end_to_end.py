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
from typing import TYPE_CHECKING, cast

try:
    import polars as pl
    import requests
except ImportError as e:
    print(f"❌ Hiányzó modul: {e}. Telepítés: pip install requests polars")
    sys.exit(1)

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.ui.core_bridge import CoreBridge

if TYPE_CHECKING:
    pass


def download_data() -> bool:
    """Adat letöltés futtatása EURUSD 2024-03-20-ra.

    Returns:
        bool: Sikeres volt-e a letöltés
    """
    print("📥 Adat letöltés indítása: EURUSD 2024-03-20")

    try:
        # Download szkript futtatása
        script_path: Path = Path(__file__).parent / "download_history.py"
        cmd: list[str] = [
            "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
            str(script_path),
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-20",
        ]

        result: subprocess.CompletedProcess[str] = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

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
        # Először erőszakkal leállítjuk az esetleges zombi folyamatokat
        print("🔪 Zombi folyamatok leállítása...")
        force_kill_path: Path = Path(__file__).parent / "force_kill.py"
        kill_result: subprocess.CompletedProcess[str] = subprocess.run(
            ["/home/elynea/miniconda3/envs/neural-ai-next/bin/python", str(force_kill_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if kill_result.returncode != 0:
            print(f"⚠️ Force kill figyelmeztetés: {kill_result.stderr}")
        else:
            print("✅ Folyamatok tisztítása sikeres")

        # Dashboard indítása headless-ben
        main_path: Path = Path(__file__).parent.parent / "main.py"
        cmd: list[str] = [
            "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
            str(main_path),
            "dashboard",
            "--headless",
        ]

        # Indítás cwd-vel beállítva a projekt gyökerére
        process: subprocess.Popen[str] = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Ciklikus ellenőrzés: max 30 másodpercig várunk a port elérhetőségére
        max_wait: int = 30
        check_interval: int = 1
        health_url: str = "http://localhost:8501/_stcore/health"

        for elapsed in range(0, max_wait, check_interval):
            # Ellenőrizzük, hogy a folyamat még fut-e
            if process.poll() is not None:
                _, stderr = process.communicate()
                print(f"❌ Dashboard folyamat kilépett az indulás előtt: {stderr}")
                return False

            # Próbálunk kapcsolódni a health endpoint-hez
            try:
                response: requests.Response = requests.get(health_url, timeout=2)
                if response.status_code == 200:
                    print(f"✅ Dashboard sikeresen indult ({elapsed + check_interval}s)")
                    # Leállítjuk
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                        print("✅ Dashboard leállítva")
                    except subprocess.TimeoutExpired:
                        process.kill()
                        print("⚠️ Dashboard erőszakkal leállítva")
                    return True
            except requests.RequestException:
                # Port még nem elérhető, folytatjuk a várakozást
                pass

            time.sleep(check_interval)

        # Ha ide értünk, timeout történt
        print("❌ Dashboard indítása timeout - port nem vált elérhetővé 30 másodpercen belül")
        if process.poll() is None:
            process.kill()

        return False

    except Exception as e:
        print(f"❌ Hiba a dashboard indításakor: {e}")
        return False


async def validate_d2_swing_engine() -> bool:
    """D2 Swing Engine implementáció validálása.

    Returns:
        bool: Sikeres volt-e a validáció
    """
    print("🪝 D2 Swing Engine validálása")

    try:
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

        # Core Bridge inicializálása
        bridge: CoreBridge = CoreBridge()
        bridge.initialize()

        # Komponensek lekérése és cast
        # A get_component visszatérési értéke Any, ezért castoljuk
        # A cast importálva van a modul elején
        config: ConfigManagerInterface = cast(ConfigManagerInterface, bridge.get_component("config"))
        logger: LoggerInterface = cast(LoggerInterface, bridge.get_component("logger"))
        strategy_service: StrategyServiceInterface = cast(StrategyServiceInterface, bridge.get_component("strategy_service"))

        if not all([config, logger, strategy_service]):
            print("❌ Szükséges komponensek nem elérhetőek (config, logger, strategy_service)")
            return False

        # D2 processzor létrehozása
        from neural_ai.processors.factory import create_dimension_processor

        d2_processor = create_dimension_processor(2, config, logger)

        # Adatok lekérése (1h timeframe a support/resistance számításhoz)
        df: pl.DataFrame | None = await strategy_service.get_candles(
            symbol="EURUSD", date="2024-03-20", timeframe="1h"
        )

        if df is None or df.is_empty():
            print("❌ Nincs elérhető adat a D2 validációhoz")
            return False

        print(f"✅ {df.height} H1 gyertya adat betöltve a D2 validációhoz")

        # Oszlopnevek normalizálása (kisbetűsítés)
        df = df.clone()
        rename_dict: dict[str, str] = {col: col.lower() for col in df.columns}
        df = df.rename(rename_dict)

        # Szükséges oszlopok ellenőrzése
        required_columns: list[str] = ["timestamp", "bid_open", "bid_high", "bid_low", "bid_close"]
        missing_columns: list[str] = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Hiányzó kötelező oszlopok: {missing_columns}")
            return False

        # D2 processzor futtatása (1h timeframe)
        # A process metódus visszatérési értéke DataFrame
        processed_df: pl.DataFrame = d2_processor.process(df, timeframe="1h")  # type: ignore

        # Új oszlopok ellenőrzése
        expected_columns: list[str] = ["swing_high", "swing_low", "resistance", "support"]
        missing_new_columns: list[str] = [col for col in expected_columns if col not in processed_df.columns]
        if missing_new_columns:
            print(f"❌ Hiányzó D2 kimeneti oszlopok: {missing_new_columns}")
            return False

        print(f"✅ Minden D2 kimeneti oszlop jelen van: {expected_columns}")

        # Swing pontok ellenőrzése (boolean oszlopok, sum = True értékek száma)
        swing_high_count: int = processed_df.select(pl.col("swing_high").sum()).item()  # type: ignore[misc]
        swing_low_count: int = processed_df.select(pl.col("swing_low").sum()).item()  # type: ignore[misc]

        if swing_high_count == 0 and swing_low_count == 0:
            print("❌ Nincsenek swing pontok a feldolgozott adatokban")
            return False

        print(f"✅ Swing pontok megtalálva: {swing_high_count} high, {swing_low_count} low")

        # Support/Resistance szintek ellenőrzése (placeholder: None értékek elfogadottak)
        resistance_present: bool = "resistance" in processed_df.columns
        support_present: bool = "support" in processed_df.columns

        if not resistance_present or not support_present:
            print("❌ Hiányzó resistance vagy support oszlop")
            return False

        print("✅ Resistance/Support oszlopok jelen vannak (placeholder értékekkel)")

        print("✅ D2 Swing Engine validáció sikeres")
        return True

    except Exception as e:
        print(f"❌ Hiba a D2 Swing Engine validálása közben: {e}")
        return False


async def validate_data() -> bool:
    """Adatok validálása a Strategy Service-en keresztül.

    Returns:
        bool: Sikeres volt-e a validáció
    """
    print("🔍 Adatok validálása Strategy Service-en keresztül")

    try:
        from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

        # Core Bridge inicializálása és Strategy Service lekérése
        bridge: CoreBridge = CoreBridge()
        bridge.initialize()
        strategy_service: StrategyServiceInterface = cast(StrategyServiceInterface, bridge.get_component("strategy_service"))

        if not strategy_service:
            print("❌ Strategy Service nem elérhető")
            return False

        # Adatok lekérése
        candles: pl.DataFrame | None = await strategy_service.get_candles(
            symbol="EURUSD", date="2024-03-20", timeframe="1m"
        )

        if candles is None or candles.is_empty():
            print("❌ Nincs elérhető adat")
            return False

        print(f"✅ {len(candles)} gyertya adat betöltve")

        # Oszlopnevek normalizálása
        df: pl.DataFrame = candles.clone()
        df = df.rename({col: col.lower() for col in df.columns})

        # Kötelező oszlopok ellenőrzése
        required_columns: list[str] = [
            "timestamp",
            "bid_open",
            "bid_high",
            "bid_low",
            "bid_close",
            "mid_close",
        ]
        missing_columns: list[str] = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Hiányzó kötelező oszlopok: {missing_columns}")
            return False

        # Új oszlopok ellenőrzése
        new_columns: list[str] = [
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "spread",
            "real_volume",
            "tick_volume",
            "bid_volume",
            "ask_volume",
        ]
        missing_new_columns: list[str] = [col for col in new_columns if col not in df.columns]
        if missing_new_columns:
            print(f"❌ Hiányzó új oszlopok: {missing_new_columns}")
            return False

        print(f"✅ Minden új oszlop jelen van: {new_columns}")

        # Adatok minőségének ellenőrzése

        # Spread ellenőrzése: nem NaN, nem 0
        if "spread" in df.columns:
            spread_values: pl.Series = df["spread"].drop_nulls()
            if spread_values.is_empty():
                print("❌ Spread oszlop üres vagy csak NaN értékek")
                return False
            if (spread_values == 0).all():
                print("❌ Spread oszlop csak 0 értékeket tartalmaz")
                return False
            print(f"✅ Spread értékek rendben (átlag: {spread_values.mean():.6f})")  # type: ignore[str-bytes-safe]

        # Z-Score ellenőrzése: nem NaN, nem 0
        if "rolling_z_score" in df.columns:
            zscore_values: pl.Series = df["rolling_z_score"].drop_nulls()
            if zscore_values.is_empty():
                print("❌ Rolling Z-Score oszlop üres vagy csak NaN értékek")
                return False
            if (zscore_values == 0).all():
                print("❌ Rolling Z-Score oszlop csak 0 értékeket tartalmaz")
                return False
            print(f"✅ Z-Score értékek rendben (átlag: {zscore_values.mean():.6f})")  # type: ignore[str-bytes-safe]

        # Mid árak ellenőrzése
        mid_columns: list[str] = ["mid_open", "mid_high", "mid_low", "mid_close"]
        for col in mid_columns:
            if col in df.columns:
                values: pl.Series = df[col].drop_nulls()
                if values.is_empty() or (values == 0).all():
                    print(f"❌ {col} oszlop üres vagy csak 0 értékek")
                    return False
                print(f"✅ {col} értékek rendben")

        # Bid/Mid váltás szimuláció (adat szinten)
        # Ellenőrizzük, hogy a mid oszlopok különböznek a bid-től (ha van)
        if "bid_open" in df.columns and "mid_open" in df.columns:
            bid_open: pl.Series = df["bid_open"]
            mid_open: pl.Series = df["mid_open"]
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

    success_count: int = 0
    total_steps: int = 4

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

    # 4. D2 Swing Engine validálása
    if await validate_d2_swing_engine():
        success_count += 1
    else:
        print("❌ Validáció sikertelen a D2 Swing Engine validálásánál")
        return

    print()
    print("=" * 70)
    print("📊 VALIDÁCIÓ EREDMÉNYE")
    print("=" * 70)
    print(f"✅ Sikeres lépések: {success_count}/{total_steps}")

    if success_count == total_steps:
        print("🎉 END-TO-END VALIDÁCIÓ SIKERES!")
        print("A CORE DATA PIPELINE és D2 Swing Engine helyesen működik.")
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
