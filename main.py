"""Neural AI Next - Fő indító szkript.

Ez a modul tartalmazza az alkalmazás fő belépési pontját, amely felelős a core
komponensek inicializálásáért és az alkalmazás életciklusának kezeléséért.

A szkript követi a Dependency Injection (DI) elvet, kizárólag interfészeken
keresztül kommunikál a komponensekkel, és a CoreComponents bundle-t használja
a szolgáltatások eléréséhez.
"""

import asyncio
import sys
from contextlib import suppress
from typing import TYPE_CHECKING

from neural_ai.core import bootstrap_core

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.services.market_data_persister import MarketDataPersister


async def main() -> None:
    """Fő alkalmazás belépési pont.

    Ez a függvény felelős az alkalmazás teljes életciklusáért:
    1. Core komponensek inicializálása
    2. Szolgáltatások indítása (event bus, adatbázis)
    3. Örök futás biztosítása, amíg le nem állítják
    4. Hiba kezelése és naplózása

    Raises:
        SystemExit: Ha kritikus hiba történik az alkalmazás indítása során.
    """
    # Core komponensek inicializálása típusos változóval
    components: CoreComponents = bootstrap_core()
    
    # Komponensek lekérése
    logger: LoggerInterface | None = components.logger
    event_bus: EventBusInterface | None = components.event_bus
    database: DatabaseManager | None = components.database
    live_feed: ILiveFeed | None = components.live_feed
    persister: MarketDataPersister | None = components.persister

    try:
        if logger is not None:
            logger.info("Rendszer indítása", extra={"version": "0.5.0"})

        # Szolgáltatások indítása
        if event_bus is not None:
            await event_bus.start()

        if database is not None:
            await database.initialize()
        
        # Adatmentő szolgálat indítása (Hogy ne vesszen el az adat!)
        if persister:
            await persister.start()
            if logger: logger.info("✅ MarketDataPersister elindítva")

        # Live feed indítása (ha elérhető)
        if live_feed is not None:
            await live_feed.start()
            if logger is not None:
                logger.info("✅ JForex Live Feed elindítva")

        if logger is not None:
            logger.info("Rendszer fut, eseményekre vár")

        # Örök futás (amíg nem jön Ctrl+C)
        # A suppress elnyeli a CancelledError-t leálláskor
        with suppress(asyncio.CancelledError):
            await asyncio.Event().wait()
    
    finally:
        # Szolgáltatások leállítása fordított sorrendben
        if logger is not None:
            logger.info("Rendszer leállítása...")

        # ELŐSZÖR a Persistert állítjuk le, hogy kiírja a buffert!
        if persister:
            await persister.stop()
            if logger: logger.info("✅ MarketDataPersister leállítva (Buffer kiírva)")
        
        if live_feed is not None:
            await live_feed.stop()
            if logger is not None:
                logger.info("✅ JForex Live Feed leállítva")
        
        if event_bus is not None:
            await event_bus.stop()
            if logger is not None:
                logger.info("✅ EventBus leállítva")
        
        if logger is not None:
            logger.info("✅ Rendszer leállítva")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ez kapja el a Ctrl+C-t a legfelső szinten
        pass
    except Exception as e:
        # Globális hiba kezelése
        print(f"CRITICAL SYSTEM ERROR: {e}")
        sys.exit(1)
    finally:
        print("\n🛑 Rendszer leállítva.")
