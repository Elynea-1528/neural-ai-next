import asyncio
import lzma
import struct

import aiohttp

# KONFIGURÁCIÓ
SYMBOL = "EURUSD"
YEAR = 2024
MONTH = 0  # Január (0-tól indexelve a JForex szerint)
DAY = 4
HOUR = 10
BASE_URL = "https://datafeed.dukascopy.com/datafeed"


async def test_direct_download():
    # 1. URL Összerakása (A kódod logikája szerint)
    # Figyelem: A hónap itt 00-11, a nap 01-31
    url = f"{BASE_URL}/{SYMBOL}/{YEAR}/{MONTH:02d}/{DAY:02d}/{HOUR:02d}h_ticks.bi5"

    print("--- DIREKT TESZT ---")
    print(f"Cél: {SYMBOL} {YEAR}-{MONTH + 1:02d}-{DAY:02d} {HOUR}:00")
    print(f"URL: {url}")
    print("-" * 30)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                print(f"HTTP Státusz: {response.status}")

                if response.status == 200:
                    content = await response.read()
                    print(f"Letöltött méret: {len(content)} bájt")

                    if len(content) == 0:
                        print("❌ A fájl üres!")
                        return

                    try:
                        # 2. Dekódolás
                        decompressed = lzma.decompress(content)
                        print(f"Kicsomagolt méret: {len(decompressed)} bájt")

                        # 3. Első tick kiolvasása
                        # Formátum: >III (timestamp_delta, ask_int, bid_int)
                        count = len(decompressed) // 12
                        print(f"Tickek száma: {count}")

                        if count > 0:
                            first_record = decompressed[0:12]
                            td, ask, bid = struct.unpack(">III", first_record)
                            print(f"Első Tick RAW: {td}, {ask}, {bid}")
                            print(f"Első Tick ÁR: Ask={ask / 100000:.5f}, Bid={bid / 100000:.5f}")
                            print("✅ SIKER: Az adatok validak és olvashatók.")

                    except Exception as e:
                        print(f"❌ Dekódolási hiba: {e}")
                else:
                    print("❌ Nem 200 OK a válasz.")

        except Exception as e:
            print(f"❌ Hálózati hiba: {e}")


if __name__ == "__main__":
    asyncio.run(test_direct_download())
