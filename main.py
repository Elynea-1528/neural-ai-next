#!/usr/bin/env python3
"""Neural AI Next - Fő indító szkript.

Ez a szkript inicializálja a teljes kereskedési ökoszisztémát
az új bootstrap_core függvény használatával.
"""

import asyncio

from neural_ai.core import bootstrap_core


async def main():
    """Fő alkalmazás belépési pont."""
    # Core komponensek inicializálása
    components = bootstrap_core()

    # EventBus indítása
    await components.event_bus.start()

    # Adatbázis inicializálása
    await components.database.initialize()

    # Örök futás
    await asyncio.Event().wait()


if __name__ == "__main__":
    """Entry point."""
    asyncio.run(main())
