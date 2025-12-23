"""EventBus implementáció ZeroMQ-val és asyncio-val.

Ez a modul biztosítja az eseményvezérelt architektúra magját, lehetővé téve
a komponensek közötti laza csatolást Pub/Sub mintázattal.

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Optional

# Csak típusellenőrzéskor importáljuk, hogy elkerüljük a körkörös importot
if TYPE_CHECKING:
    from typing import Any

    import zmq
    import zmq.asyncio
    from pydantic import BaseModel


logger = logging.getLogger(__name__)

# Típus aliasok a jobb olvashatóság érdekében
EventCallback = Callable[["BaseModel"], "Any"]


@dataclass
class EventBusConfig:
    """EventBus konfiguráció.

    Attributes:
        zmq_context: ZeroMQ kontextus (opcionális, létrejön ha nincs megadva)
        pub_port: Publisher port (alapértelmezett: 5555)
        sub_port: Subscriber port (alapértelmezett: 5556)
        use_inproc: Használjon inproc transportot teszteléshez (alapértelmezett: False)
    """

    zmq_context: Optional["zmq.asyncio.Context"] = None
    pub_port: int = 5555
    sub_port: int = 5556
    use_inproc: bool = False


class EventBus:
    """ZeroMQ alapú aszinkron eseménybusz.

    Ez az osztály biztosítja az események közzétételét és feliratkozást
    a rendszer különböző komponensei számára. A ZeroMQ PUB/SUB mintázatot használja.

    A specifikációban említett asyncio.Queue-s megvalósítás helyett egyből
    ZeroMQ-t használunk a teljesítmény és a skálázhatóság érdekében.

    Attributes:
        config: Az EventBus konfigurációja
        _context: ZeroMQ kontextus
        _publisher: Publisher socket
        _subscribers: Feliratkozók szótára event_type -> callback lista
        _running: Futási állapot jelzője
    """

    def __init__(self, config: EventBusConfig | None = None) -> None:
        """Inicializálja az EventBus-t.

        Args:
            config: EventBus konfiguráció (opcionális)
        """
        self.config = config or EventBusConfig()

        # Importáljuk itt, hogy ne legyen kötelező függőség a használathoz
        try:
            import zmq.asyncio

            self._zmq = zmq
            self._zmq_asyncio = zmq.asyncio
        except ImportError as e:
            raise ImportError("ZeroMQ nincs telepítve. Telepítsd: pip install pyzmq") from e

        # Hozzuk létre a kontextust ha nincs megadva
        if self.config.zmq_context is None:
            self._context: zmq.asyncio.Context = self._zmq_asyncio.Context()
            self._own_context = True
        else:
            self._context = self.config.zmq_context
            self._own_context = False

        self._publisher: zmq.Socket | None = None
        self._subscribers: dict[str, list[EventCallback]] = {}
        self._running = False
        self._logger = logging.getLogger(self.__class__.__name__)

    async def start(self) -> None:
        """Elindítja az EventBus-t és létrehozza a socketeket."""
        if self._running:
            return

        self._logger.info("EventBus indítása...")

        # Publisher socket létrehozása
        self._publisher = self._context.socket(self._zmq.PUB)

        if self.config.use_inproc:
            # Inproc transport teszteléshez
            pub_url = "inproc://eventbus_pub"
        else:
            # TCP transport éles használathoz
            pub_url = f"tcp://*:{self.config.pub_port}"

        self._publisher.bind(pub_url)
        self._logger.info(f"Publisher bind-olva: {pub_url}")

        # Kis várakozás, hogy a bind teljesüljön
        await asyncio.sleep(0.1)

        self._running = True
        self._logger.info("EventBus elindítva")

    async def stop(self) -> None:
        """Leállítja az EventBus-t és felszabadítja az erőforrásokat."""
        if not self._running:
            return

        self._logger.info("EventBus leállítása...")
        self._running = False

        if self._publisher:
            self._publisher.close()
            self._publisher = None

        if self._own_context and self._context:
            self._context.term()

        self._logger.info("EventBus leállítva")

    async def publish(self, event_type: str, event: "BaseModel") -> None:
        """Esemény közzététele a buszon.

        Args:
            event_type: Az esemény típusa (pl. 'market_data', 'trade')
            event: Az esemény objektum (Pydantic BaseModel)

        Raises:
            RuntimeError: Ha az EventBus nincs elindítva
        """
        if not self._running:
            raise RuntimeError("EventBus nincs elindítva")

        if self._publisher is None:
            raise RuntimeError("Publisher socket nincs inicializálva")

        # Serializáljuk az eseményt JSON formátumba
        # A model_dump_json() automatikusan kezeli a datetime objektumokat
        event_dict = json.loads(event.model_dump_json())
        event_dict["_event_type"] = event_type
        event_dict["_timestamp"] = datetime.now(UTC).isoformat()

        message = json.dumps(event_dict).encode("utf-8")

        # Küldjük az eseményt a megfelelő témakörbe
        topic = event_type.encode("utf-8")
        await self._publisher.send_multipart([topic, message])

        self._logger.debug(f"Esemény közzétéve: {event_type}")

    def subscribe(self, event_type: str, callback: EventCallback) -> None:
        """Feliratkozás eseménytípusra.

        Args:
            event_type: Az esemény típusa, amire feliratkozunk
            callback: A callback függvény, amely az eseményt fogadja

        Note:
            A callback-nek aszinkronnak kell lennie (async def)
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._subscribers[event_type].append(callback)
        self._logger.info(f"Feliratkozás létrehozva: {event_type}")

    def unsubscribe(self, event_type: str, callback: EventCallback) -> None:
        """Leiratkozás eseménytípusról.

        Args:
            event_type: Az esemény típusa
            callback: A callback függvény, amelyet eltávolítunk
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                self._logger.info(f"Leiratkozás: {event_type}")

    async def _dispatch_event(self, event_type: str, event_data: dict[str, "Any"]) -> None:
        """Esemény továbbítása a feliratkozóknak.

        Args:
            event_type: Az esemény típusa
            event_data: Az esemény adatai
        """
        if event_type not in self._subscribers:
            return

        # Deserializáljuk az eseményt a megfelelő osztályba
        try:
            event = self._deserialize_event(event_type, event_data)
            if event is None:
                return

            # Hívjuk meg az összes feliratkozó callback-jét
            for callback in self._subscribers[event_type]:
                try:
                    await callback(event)
                except Exception as e:
                    self._logger.error(f"Hiba a callback végrehajtásakor: {e}", exc_info=True)
        except Exception as e:
            self._logger.error(f"Hiba az esemény deserializálásakor: {e}", exc_info=True)

    def _deserialize_event(
        self, event_type: str, event_data: dict[str, "Any"]
    ) -> Optional["BaseModel"]:
        """Deserializálja az eseményt a megfelelő Pydantic modellbe.

        Args:
            event_type: Az esemény típusa
            event_data: Az esemény adatai

        Returns:
            A deserializált esemény objektum vagy None ha hiba történt
        """
        # Importáljuk itt, hogy elkerüljük a körkörös importot
        from neural_ai.core.events.events import (
            MarketDataEvent,
            OrderEvent,
            PositionEvent,
            SignalEvent,
            SystemLogEvent,
            TradeEvent,
        )

        # Távolítsuk el a meta adatokat
        event_data = {k: v for k, v in event_data.items() if not k.startswith("_")}

        try:
            if event_type == "market_data":
                return MarketDataEvent(**event_data)
            elif event_type == "trade":
                return TradeEvent(**event_data)
            elif event_type == "signal":
                return SignalEvent(**event_data)
            elif event_type == "system_log":
                return SystemLogEvent(**event_data)
            elif event_type == "order":
                return OrderEvent(**event_data)
            elif event_type == "position":
                return PositionEvent(**event_data)
            else:
                self._logger.warning(f"Ismeretlen eseménytípus: {event_type}")
                return None
        except Exception as e:
            self._logger.error(f"Hiba az esemény deserializálásakor: {e}", exc_info=True)
            return None

    async def run_forever(self) -> None:
        """Eseménybusz örök futás (blokkoló).

        Ez a metódus egy végtelen ciklusban fogadja az eseményeket
        és továbbítja azokat a feliratkozóknak.

        Note:
            Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd
        """
        if not self._running:
            raise RuntimeError("EventBus nincs elindítva")

        # Subscriber socket létrehozása
        subscriber = self._context.socket(self._zmq.SUB)

        if self.config.use_inproc:
            sub_url = "inproc://eventbus_pub"
        else:
            sub_url = f"tcp://localhost:{self.config.pub_port}"

        subscriber.connect(sub_url)

        # Feliratkozás az összes témakörre
        subscriber.setsockopt(self._zmq.SUBSCRIBE, b"")

        self._logger.info(f"Subscriber csatlakozva: {sub_url}")

        try:
            while self._running:
                try:
                    # Várjunk egy eseményre (non-blocking)
                    msg = await asyncio.wait_for(subscriber.recv_multipart(), timeout=1.0)

                    if len(msg) >= 2:
                        topic = msg[0].decode("utf-8")
                        message = msg[1].decode("utf-8")

                        # Deserializáljuk az üzenetet
                        event_data = json.loads(message)

                        # Távolítsuk el a témakört az event_data-ból
                        event_type = event_data.pop("_event_type", topic)

                        # Továbbítjuk az eseményt
                        await self._dispatch_event(event_type, event_data)

                except TimeoutError:
                    # Időtúllépés, ellenőrizzük a futási állapotot
                    continue
                except Exception as e:
                    self._logger.error(f"Hiba az esemény fogadásakor: {e}", exc_info=True)

        finally:
            subscriber.close()
            self._logger.info("Subscriber lezárva")

    async def __aenter__(self) -> "EventBus":
        """Aszinkron context manager.

        Returns:
            Az EventBus példány
        """
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Aszinkron context manager lezárás.

        Args:
            exc_type: A kivétel típusa (ha volt kivétel)
            exc_val: A kivétel objektum (ha volt kivétel)
            exc_tb: A traceback objektum (ha volt kivétel)
        """
        await self.stop()
