#!/usr/bin/env python3
"""
JForex Live Feed Bridge Test Script.

Ez a szkript teszteli a JForex Live Feed bekötését a rendszerbe anélkül,
hogy a teljes main.py alkalmazás elindulna.

Működés:
1. Bootstrap-el inicializálja a core komponenseket
2. Ellenőrzi, hogy a live feed elérhető-e
3. Ha igen, elindítja a live feed-et
4. Feliratkozik a market_data eseményre és kiírja a konzolra a bejövő tick-eket
5. 60 másodpercig fut, majd leállítja a live feed-et
"""

import asyncio
import sys
from datetime import datetime
from typing import TYPE_CHECKING

# Importok a projekt gyökeréből
sys.path.insert(0, '.')

from neural_ai.core import bootstrap_core

if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


async def test_live_feed():
    """Fő teszt függvény a Live Feed bekötéséhez."""
    
    print("=" * 80)
    print("🚀 JFOREX LIVE FEED BRIDGE TEST")
    print("=" * 80)
    print()
    
    # 1. Bootstrap inicializálása
    print("⏳ 1. Core komponensek inicializálása...")
    try:
        components = bootstrap_core()
        print("   ✅ Bootstrap sikeres")
    except Exception as e:
        print(f"   ❌ Bootstrap hiba: {e}")
        return
    
    # 2. Komponensek lekérése
    logger: LoggerInterface | None = components.logger
    event_bus: EventBusInterface | None = components.event_bus
    live_feed: ILiveFeed | None = components.live_feed
    
    # 3. Live feed ellenőrzése
    print("\n⏳ 2. Live Feed ellenőrzése...")
    if live_feed is None:
        print("   ⚠️  Live Feed nincs konfigurálva vagy nincs engedélyezve")
        print("   ℹ️  Ellenőrizd a configs/collectors.yaml fájlt!")
        return
    else:
        print("   ✅ Live Feed elérhető")
    
    # 4. Event bus ellenőrzése
    if event_bus is None:
        print("   ❌ EventBus nincs elérhető")
        return
    else:
        print("   ✅ EventBus elérhető")
    
    # 5. Eseménykezelő definiálása
    tick_count = 0
    
    async def on_market_data(event):
        """Fogadja és feldolgozza a market data eseményeket."""
        nonlocal tick_count
        tick_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"   📊 [{timestamp}] Tick #{tick_count}: {event.symbol} - "
              f"Bid: {event.bid_price:.5f}, Ask: {event.ask_price:.5f}")
    
    # 6. Feliratkozás az eseményre
    print("\n⏳ 3. Feliratkozás a market_data eseményre...")
    try:
        event_bus.subscribe("market_data", on_market_data)
        print("   ✅ Feliratkozva a market_data eseményre")
    except Exception as e:
        print(f"   ❌ Hiba a feliratkozáskor: {e}")
        return
    
    # 7. Live feed indítása
    print("\n⏳ 4. Live Feed indítása...")
    try:
        await live_feed.start()
        print("   ✅ Live Feed elindítva")
        if logger is not None:
            logger.info("Live Feed teszt indítva")
    except Exception as e:
        print(f"   ❌ Hiba a Live Feed indításkor: {e}")
        return
    
    # 8. Teszt futása 60 másodpercig
    print("\n⏳ 5. Teszt futtatása 60 másodpercig...")
    print("   ℹ️  Nyomj Ctrl+C-t a korai leállításhoz")
    print()
    
    try:
        for i in range(60):
            await asyncio.sleep(1)
            if i % 10 == 9:
                print(f"   ⏱️  {i+1} másodperc eltelt ({tick_count} tick fogadva)")
    except KeyboardInterrupt:
        print("\n   ⚠️  Felhasználói leállítás (Ctrl+C)")
    
    # 9. Statisztika kiírása
    print("\n" + "=" * 80)
    print("📊 TESZT STATISZTIKA")
    print("=" * 80)
    print(f"   Összes tick száma: {tick_count}")
    print(f"   Átlagos tick/másodperc: {tick_count/60:.2f}")
    print()
    
    # 10. Live feed leállítása
    print("⏳ 6. Live Feed leállítása...")
    try:
        await live_feed.stop()
        print("   ✅ Live Feed leállítva")
        if logger is not None:
            logger.info("Live Feed teszt leállítva")
    except Exception as e:
        print(f"   ❌ Hiba a Live Feed leállításkor: {e}")
    
    print("\n✅ TESZT VÉGE")
    print("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(test_live_feed())
    except KeyboardInterrupt:
        print("\n🛑 Teszt leállítva a felhasználó által")
    except Exception as e:
        print(f"\n❌ VÁRATLAN HIBA: {e}")
        sys.exit(1)