#!/usr/bin/env python3
"""Egyszerű teszt szkript a .bi5 formátum detektáláshoz."""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.core import bootstrap_core


async def test_bi5_format(symbol: str, date_str: str) -> None:
    """Teszteljük a .bi5 formátum detektálást."""
    print(f"🧪 TESZT: {symbol} - {date_str}")
    print("=" * 60)

    # Rendszer inicializálása
    core = bootstrap_core()
    logger = core.logger
    event_bus = core.event_bus

    # EventBus indítása
    await event_bus.start()

    # Downloader létrehozása
    downloader = JForexFactory.create_downloader(
        config=core.config,
        logger=logger,
        event_bus=event_bus,
        storage=core.storage,
    )

    # Dátum parse-olása
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=UTC
    )

    print(f"📥 Letöltés indítása: {date.isoformat()}")
    print()

    # Letöltés óránként
    for hour in range(24):
        current_hour = date.replace(hour=hour)

        try:
            print(f"   ⏰ Óra: {hour:02d}:00")
            ticks = await downloader.download_tick_data(symbol, current_hour)

            if ticks:
                print(f"      ✅ {len(ticks)} tick letöltve")
            else:
                print("      ⚠️  Nincs adat")

        except Exception as e:
            print(f"      ❌ Hiba: {e}")

    print()
    print("=" * 60)
    print("✅ TESZT BEFEJEZVE")
    print()
    print("📊 Ellenőrizd a logfájlt a formátum detektálásról:")
    print("   grep 'bi5_format_detected' logs/neural_ai.log")
    print("   grep 'bi5_chunk_stats' logs/neural_ai.log")

    # Rendszer leállítása
    await downloader.close()
    await event_bus.stop()


def main() -> None:
    """Főprogram."""
    if len(sys.argv) != 3:
        print("Használat: python scripts/test_bi5_format.py <SYMBOL> <YYYY-MM-DD>")
        print("Példa: python scripts/test_bi5_format.py EURUSD 2008-06-04")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    date_str = sys.argv[2]

    try:
        asyncio.run(test_bi5_format(symbol, date_str))
    except KeyboardInterrupt:
        print("\n⚠️  Teszt megszakítva")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
