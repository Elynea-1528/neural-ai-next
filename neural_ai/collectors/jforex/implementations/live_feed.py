"""JForex Live Feed Implementation.

Ez a modul implementálja a JForex live adatfolyam fogadását ZMQ socketen keresztül
a Java Bridge-el (NeuralBridgeStrategy) való kommunikációhoz.
"""

import asyncio
import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, cast

import zmq
import zmq.asyncio

from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class JForexLiveFeed(ILiveFeed):
    """JForex live adatfolyam fogadó implementációja.

    Ez az osztály felelős a Java Bridge-el való ZMQ-alapú kommunikációért.
    A start() metódus indítja el a tick fogadást a 5555-ös porton, a stop() pedig
    leállítja azt.

    Attributes:
        logger: Logger példány a naplózásra
        event_bus: Event bus a piaci adatok publikálására
        config: Konfiguráció kezelő
        _running: Futási állapot jelzője
        _socket: ZMQ SUB socket a tick fogadásához
        _context: ZMQ context
        _listen_task: Aszinkron task a tick fogadásához
    """

    def __init__(
        self,
        logger: "LoggerInterface",
        event_bus: "EventBusInterface",
        config: "ConfigManagerInterface",
    ) -> None:
        """Inicializálja a JForexLiveFeed osztályt.

        Args:
            logger: Logger példány
            event_bus: Event bus példány
            config: Konfiguráció kezelő példány
        """
        self.logger = logger
        self.event_bus = event_bus
        self.config = config

        self._running = False
        self._socket: zmq.asyncio.Socket | None = None
        self._context: zmq.asyncio.Context | None = None
        self._listen_task: asyncio.Task[None] | None = None

        # Konfiguráció betöltése (Helyes útvonal: collectors -> jforex_live)
        try:
            # Először próbáljuk a namespaced helyen
            live_config = config.get("collectors", "jforex_live")

            # Ha ott nincs, próbáljuk a gyökérben (fallback)
            if not live_config:
                live_config = config.get("jforex_live")

            # Ha sehol nincs, üres dict
            if not live_config:
                live_config = {}
                self.logger.warning("jforex_live_config_missing - Using defaults (5555)")
            else:
                self.logger.debug(f"jforex_live_config_loaded - config: {live_config}")

        except (KeyError, ValueError, AttributeError):
            live_config = {}

        self._host: str = cast(str, live_config.get("host", "127.0.0.1"))
        self._tick_port: int = cast(int, live_config.get("tick_port", 5555))
        self._command_port: int = cast(int, live_config.get("command_port", 5556))

    async def start(self) -> None:
        """Indítja a live adatfolyam fogadását.

        Létrehozza a ZMQ SUB socketet, csatlakozik a megadott portra, és elindítja
        a háttérfolyamatot (_listen_loop) a tickek folyamatos fogadásához.

        Raises:
            LiveFeedError: Ha a csatlakozás vagy a fogadás során hiba történik.
        """
        if self._running:
            self.logger.warning("jforex_live_feed_already_running")
            return

        try:
            # ZMQ context létrehozása
            self._context = zmq.asyncio.Context()

            # SUB socket létrehozása
            self._socket = self._context.socket(zmq.SUB)

            # Csatlakozás a tick portra
            connection_string = f"tcp://{self._host}:{self._tick_port}"
            self._socket.connect(connection_string)

            # Feliratkozás minden üzenetre
            self._socket.setsockopt_string(zmq.SUBSCRIBE, "")

            # Futási állapot beállítása
            self._running = True

            # Háttérfolyamat indítása
            self._listen_task = asyncio.create_task(self._listen_loop())

            self.logger.info("jforex_live_feed_started", host=self._host, tick_port=self._tick_port)

        except Exception as e:
            self.logger.error(
                "jforex_live_feed_start_failed", error=str(e), host=self._host, port=self._tick_port
            )
            await self.stop()
            raise

    async def stop(self) -> None:
        """Leállítja a live adatfolyam fogadását.

        Megszünteti a ZMQ kapcsolatot és leállítja a háttérfolyamatot.
        """
        if not self._running:
            return

        self._running = False

        # Háttérfolyamat leállítása
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
            self._listen_task = None

        # Socket lezárása
        if self._socket:
            self._socket.close()
            self._socket = None

        # Context lezárása
        if self._context:
            self._context.term()
            self._context = None

        self.logger.info("jforex_live_feed_stopped")

    def is_running(self) -> bool:
        """Visszaadja, hogy a live feed jelenleg fut-e.

        Returns:
            bool: True, ha a feed fut, False egyébként.
        """
        return self._running

    async def _listen_loop(self) -> None:
        """Háttérfolyamat a tickek folyamatos fogadásához.

        Ez a metódus egy végtelen ciklusban vár a ZMQ socketre érkező üzenetekre,
        dekódolja a JSON adatokat, és továbbítja a `_process_tick_data` metódusnak
        a teljes feldolgozásért és publikálásért.
        """
        print(f"DEBUG: ZMQ Receiver Loop start on port {self._tick_port}")

        while self._running:
            try:
                if self._socket is None:
                    await asyncio.sleep(0.1)
                    continue

                # Blokkoló hívás
                message = await self._socket.recv_string()

                # JSON dekódolás
                tick_data = json.loads(message)

                # Tick adatok továbbítása a feldolgozó metódusnak
                await self._process_tick_data(tick_data)

            except asyncio.CancelledError:
                break
            except Exception as e:
                # DIAGNOSZTIKA: Mi a baj?
                import traceback

                print("!!! CRITICAL LIVE FEED ERROR !!!")
                traceback.print_exc()

                self.logger.error("jforex_live_feed_listen_loop_error", error=str(e))
                await asyncio.sleep(1)

    async def _process_tick_data(self, data: dict[str, object]) -> None:
        """Feldolgozza a tick adatokat és publikálja az EventBus-on.

        A `_listen_loop` metódusból kapja a már dekódolt JSON adatokat.
        A timestamp milliszekundumban érkezik, ezért osztani kell 1000-el.
        A bid/ask értékek már float-ként érkeznek, nem kell castolni.
        Az ask_volume és bid_volume mezőket kiolvassa a JSON-ből és hozzáadja az event-hez.

        Args:
            data: A tick adatok dictionary-ben (timestamp ms-ban, bid/ask float, ask_volume/bid_volume float)
        """
        try:
            # Timestamp konverziója ms-ből datetime objektummá
            ts_ms = data.get("timestamp")
            if isinstance(ts_ms, (int, float)):
                timestamp = datetime.fromtimestamp(ts_ms / 1000.0, tz=UTC)
            else:
                timestamp = datetime.now(UTC)

            # Volume értékek kiolvasása
            ask_vol = float(data.get("ask_volume", 0.0))
            bid_vol = float(data.get("bid_volume", 0.0))

            # MarketDataEvent létrehozása
            event = MarketDataEvent(
                symbol=str(data.get("symbol", "")),
                timestamp=timestamp,
                bid=float(data.get("bid", 0.0)),
                ask=float(data.get("ask", 0.0)),
                volume=(ask_vol + bid_vol) if (ask_vol or bid_vol) else None,
                ask_volume=ask_vol,
                bid_volume=bid_vol,
                source="jforex",
            )

            # Esemény publikálása
            await self.event_bus.publish("market_data", event)

            # Naplózás (csak debug módban)
            self.logger.debug(
                "jforex_live_feed_tick_received", symbol=event.symbol, bid=event.bid, ask=event.ask
            )

        except Exception as e:
            self.logger.error(
                "jforex_live_feed_process_tick_error",
                error=str(e),
                raw_message=str(data),
                exc_info=True,
            )
