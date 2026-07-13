"""EventBus factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az EventBus létrehozását a konfiguráció alapján.
A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk
egyszerű cseréjét.

FONTOS: Ez a factory mindig ÚJ EventBus példányokat hoz létre (nem singleton).
Az EventBus context manager-ként használható, így biztosítva a clean shutdown-t.

Author: Neural AI Next Team
Version: 2.0.0
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.events.implementations.zeromq_bus import EventBusConfig
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class EventBusFactory:
    """EventBus factory - mindig ÚJ példányt hoz létre (nem singleton).

    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).

    KRITIKUS: A factory NEM singleton-okat gyárt! Minden hívás új EventBus
    példányt hoz létre, amely context manager-ként használható a clean
    shutdown biztosítására.

    Attributes:
        _logger: Logger interfész (opcionális)
    """

    def __init__(self, logger: "LoggerInterface | None" = None) -> None:
        """Factory inicializálása logger-rel.

        Args:
            logger: Logger interfész a logoláshoz (opcionális)
        """
        self._logger = logger

    async def create_and_start(
        self, config: "EventBusConfig | None" = None
    ) -> "EventBusInterface":
        """Létrehoz, elindít és visszaad egy EventBus példányt.

        Context manager használat:
            async with await factory.create_and_start(config) as bus:
                await bus.publish("event", data)

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            Elindított EventBus példány (context manager)

        Note:
            Jelenleg csak a ZeroMQ-s implementációt támogatja.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        bus = EventBus(config, self._logger)
        await bus.start()
        return bus

    def create(self, config: "EventBusConfig | None" = None) -> "EventBusInterface":
        """ÚJ EventBus példány létrehozása (nem singleton, nem elindítva).

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBus példány (még nincs elindítva)

        Note:
            A metódus NEM indítja el az EventBus-t. Használd a `create_and_start()`
            metódust, ha azonnal el akarod indítani, vagy hívd meg manuálisan
            a `start()` metódust az EventBus példányon.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(config, self._logger)

    @staticmethod
    def get_event_bus(logger: "LoggerInterface | None" = None) -> "EventBusInterface":
        """Egyszerű EventBus létrehozás (nem singleton).

        Args:
            logger: Logger instance (opcionális)

        Returns:
            EventBus példány (még nincs elindítva)

        Note:
            Ez a metódus NEM singleton! Minden hívás új példányt ad vissza.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus

        return EventBus(logger=logger)
