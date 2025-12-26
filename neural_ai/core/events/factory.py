"""EventBus factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az EventBus létrehozását a konfiguráció alapján.
A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk
egyszerű cseréjét.

Author: Neural AI Next Team
Version: 1.0.0
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.implementations.zeromq_bus import EventBusConfig
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface


class EventBusFactory:
    """EventBus factory osztály.

    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).
    """

    @staticmethod
    def create(config: "EventBusConfig | None" = None) -> "EventBusInterface":
        """Létrehozza az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            Jelenleg csak a ZeroMQ-s implementációt támogatja.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(config)

    @staticmethod
    async def create_and_start(config: "EventBusConfig | None" = None) -> "EventBusInterface":
        """Létrehozza és elindítja az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az elindított EventBus példány
        """
        event_bus = EventBusFactory.create(config)
        await event_bus.start()
        return event_bus

    @staticmethod
    def create_from_config(config_manager: "ConfigManagerInterface") -> "EventBusInterface":
        """Létrehozza az EventBus példányt konfigurációkezelő alapján.

        Args:
            config_manager: Konfigurációkezelő, amelyből az EventBus beállításokat olvassuk

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            A metódus biztonságosan kezeli a konfiguráció hiányát,
            alapértelmezett értékeket használva.
        """
        from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig

        # Biztonságos lekérdezés (ha nincs szekció, üres dict)
        try:
            data = config_manager.get_section("event_bus")
        except (KeyError, ValueError):
            data = {}

        bus_config = EventBusConfig(
            pub_port=data.get("pub_port", 5555),
            sub_port=data.get("sub_port", 5556),
            use_inproc=data.get("use_inproc", False),
        )
        return EventBusFactory.create(bus_config)
