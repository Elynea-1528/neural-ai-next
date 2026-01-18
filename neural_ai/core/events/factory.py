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
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class EventBusFactory:
    """EventBus factory osztály.

    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).
    """

    def __init__(self, logger: "LoggerInterface", config_manager: "ConfigManagerInterface") -> None:
        """Inicializálja az EventBusFactory-t.

        Args:
            logger: Logger interfész a logoláshoz
            config_manager: Konfigurációkezelő interfész
        """
        self._logger = logger
        self._config_manager = config_manager
        self._logger.debug("EventBusFactory inicializálva", factory_id=id(self))

    def create(self, config: "EventBusConfig | None" = None) -> "EventBusInterface":
        """Létrehozza az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            Jelenleg csak a ZeroMQ-s implementációt támogatja.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(config, self._logger)

    async def create_and_start(self, config: "EventBusConfig | None" = None) -> "EventBusInterface":
        """Létrehozza és elindítja az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az elindított EventBus példány
        """
        event_bus = self.create(config)
        await event_bus.start()
        return event_bus

    @staticmethod
    def get_event_bus(logger: "LoggerInterface") -> "EventBusInterface":
        """Létrehozza az EventBus példányt alapértelmezett konfigurációval.

        Args:
            logger: Logger interfész

        Returns:
            EventBusInterface: Az EventBus példány
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(logger=logger)

    def create_from_config(self) -> "EventBusInterface":
        """Létrehozza az EventBus példányt konfigurációkezelő alapján.

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            A metódus biztonságosan kezeli a konfiguráció hiányát,
            alapértelmezett értékeket használva.
        """
        from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig

        self._logger.debug("EventBus létrehozása konfigurációból")
        # Biztonságos lekérdezés (ha nincs szekció, üres dict)
        try:
            data = self._config_manager.get_section("events")
            self._logger.debug("Konfigurációs adatok lekérdezve", data=data)
        except (KeyError, ValueError) as e:
            self._logger.warning(
                "Konfigurációs szekció hiányzik, alapértelmezett értékek használata", error=str(e)
            )
            data = {}

        bus_config = EventBusConfig(
            pub_port=data.get("pub_port", 5555),
            sub_port=data.get("sub_port", 5556),
            use_inproc=data.get("use_inproc", False),
        )
        self._logger.debug("EventBus konfiguráció létrehozva", config=bus_config)
        return self.create(bus_config)
