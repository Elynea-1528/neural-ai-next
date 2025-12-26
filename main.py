"""Neural AI Next - Fő indító szkript."""

import asyncio
import sys
from contextlib import suppress

from neural_ai.core import bootstrap_core


async def main():
    """Fő alkalmazás belépési pont."""
    try:
        # Core komponensek inicializálása
        components = bootstrap_core()
        logger = components.logger

        if logger:
            logger.info("system_starting", version="0.5.0")

        # Szolgáltatások indítása
        if components.event_bus:
            await components.event_bus.start()

        if components.database:
            await components.database.initialize()

        if logger:
            logger.info("system_running_waiting_for_events")

        # Örök futás (amíg nem jön Ctrl+C)
        # A suppress elnyeli a CancelledError-t leálláskor
        with suppress(asyncio.CancelledError):
            await asyncio.Event().wait()

    except Exception as e:
        # Ha van logger, oda írjuk, ha nincs, print
        if "logger" in locals() and logger:
            logger.critical("system_crash", error=str(e))
        else:
            print(f"CRITICAL SYSTEM ERROR: {e}")
        sys.exit(1)
    finally:
        print("\n🛑 Rendszer leállítva.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ez kapja el a Ctrl+C-t a legfelső szinten
        pass
