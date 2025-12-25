"""EventBus factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az EventBus létrehozását a konfiguráció alapján.
A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk
egyszerű cseréjét.

Author: Neural AI Next Team
Version: 1.0.0
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.events.implementations.zeromq_bus import EventBus, EventBusConfig


class EventBusFactory:
    """EventBus factory osztály.

    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).
    """

    @staticmethod
    def create(config: "EventBusConfig | None" = None) -> "EventBus":
        """Létrehozza az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBus: Az EventBus példány

        Note:
            Jelenleg csak a ZeroMQ-s implementációt támogatja.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(config)

    @staticmethod
    async def create_and_start(config: "EventBusConfig | None" = None) -> "EventBus":
        """Létrehozza és elindítja az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBus: Az elindított EventBus példány
        """
        event_bus = EventBusFactory.create(config)
        await event_bus.start()
        return event_bus
