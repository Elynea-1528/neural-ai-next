#!/usr/bin/env python3
"""Direct download test script for A/B testing against system pipeline.

This script downloads .bi5 data directly from Dukascopy for a full day (00-23h)
and sums the total number of ticks for validation against the system pipeline.
"""

import asyncio
import lzma

import aiohttp

# KONFIGURÁCIÓ
SYMBOL = "EURUSD"
YEAR = 2024
MONTH = 1  # Február (0-tól indexelve a JForex szerint: 00 = Jan, 01 = Feb)
DAY = 14
BASE_URL = "https://datafeed.dukascopy.com/datafeed"  # Vagy a configban lévő URL


async def download_and_count_hour(session: aiohttp.ClientSession, hour: int) -> int:
    """Letölti és megszámolja a tick-eket egy adott órához.

    Args:
        session: HTTP session
        hour: Az óra (0-23)

    Returns:
        A tick-ek száma az adott órában
    """
    # URL összerakása
    url = f"{BASE_URL}/{SYMBOL}/{YEAR}/{MONTH:02d}/{DAY:02d}/{hour:02d}h_ticks.bi5"

    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()

                if len(content) == 0:
                    print(f"   Óra {hour:02d}: Üres fájl")
                    return 0

                try:
                    # Dekódolás
                    decompressed = lzma.decompress(content)

                    # Tick-ek számolása (12 bájt per tick)
                    count = len(decompressed) // 12

                    print(f"   Óra {hour:02d}: {count} tick")
                    return count

                except Exception as e:
                    print(f"   Óra {hour:02d}: Dekódolási hiba - {e}")
                    return 0
            else:
                print(f"   Óra {hour:02d}: Nincs adat (HTTP {response.status})")
                return 0

    except Exception as e:
        print(f"   Óra {hour:02d}: Hálózati hiba - {e}")
        return 0


async def test_full_day_download():
    """Letölti a teljes nap adatait (00-23h) és összegzi a tick-eket."""
    print("=" * 60)
    print("🧪 DIREKT LETÖLTŐ TESZT (CONTROL GROUP)")
    print("=" * 60)
    print(f"Cél: {SYMBOL} {YEAR}-{MONTH + 1:02d}-{DAY:02d} (teljes nap)")
    print(f"URL alap: {BASE_URL}")
    print("-" * 60)

    total_ticks = 0

    async with aiohttp.ClientSession() as session:
        # Minden óra letöltése (0-23)
        for hour in range(24):
            count = await download_and_count_hour(session, hour)
            total_ticks += count

    print("-" * 60)
    print(f"=== TOTAL TICKS FOR {YEAR}-{MONTH + 1:02d}-{DAY:02d}: {total_ticks} ===")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_full_day_download())
