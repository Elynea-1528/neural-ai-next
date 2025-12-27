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
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


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

    # Logger komponens lekérése és típusos cast
    logger: LoggerInterface | None = components.logger

    if logger is not None:
        logger.info("Rendszer indítása", extra={"version": "0.5.0"})

    # Szolgáltatások indítása
    event_bus: EventBusInterface | None = components.event_bus
    if event_bus is not None:
        await event_bus.start()

    database: DatabaseManager | None = components.database
    if database is not None:
        await database.initialize()

    if logger is not None:
        logger.info("Rendszer fut, eseményekre vár")

    # Örök futás (amíg nem jön Ctrl+C)
    # A suppress elnyeli a CancelledError-t leálláskor
    with suppress(asyncio.CancelledError):
        await asyncio.Event().wait()


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
