"""
JForex Live Feed Implementation.

Ez a modul implementálja a JForex live adatfolyam fogadását ZMQ socketen keresztül
a Java Bridge-el (NeuralBridgeStrategy) való kommunikációhoz.
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import zmq
import zmq.asyncio

from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class JForexLiveFeed(ILiveFeed):
    """
    JForex live adatfolyam fogadó implementációja.
    
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
        config: "ConfigManagerInterface"
    ) -> None:
        """
        Inicializálja a JForexLiveFeed osztályt.
        
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
        self._listen_task: asyncio.Task | None = None
        
        # Konfiguráció betöltése
        try:
            live_config = config.get("jforex_live", {}) or {}
        except (KeyError, ValueError, AttributeError):
            live_config = {}
        
        self._host = live_config.get("host", "127.0.0.1")
        self._tick_port = live_config.get("tick_port", 5555)
        self._command_port = live_config.get("command_port", 5556)
    
    async def start(self) -> None:
        """
        Indítja a live adatfolyam fogadását.
        
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
            
            self.logger.info(
                "jforex_live_feed_started",
                host=self._host,
                tick_port=self._tick_port
            )
            
        except Exception as e:
            self.logger.error(
                "jforex_live_feed_start_failed",
                error=str(e),
                host=self._host,
                port=self._tick_port
            )
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """
        Leállítja a live adatfolyam fogadását.
        
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
        """
        Visszaadja, hogy a live feed jelenleg fut-e.
        
        Returns:
            bool: True, ha a feed fut, False egyébként.
        """
        return self._running
    
    async def _listen_loop(self) -> None:
        """
        Háttérfolyamat a tickek folyamatos fogadásához.
        
        Ez a metódus egy végtelen ciklusban vár a ZMQ socketre érkező üzenetekre,
        dekódolja a JSON adatokat, és létrehozza a MarketDataEvent-et, majd
        publikálja az EventBus-on.
        """
        print(f"DEBUG: ZMQ Receiver Loop start on port {self._tick_port}")
        
        while self._running:
            try:
                if self._socket is None:
                    await asyncio.sleep(0.1)
                    continue
                    
                # Blokkoló hívás
                message = await self._socket.recv_string()
                
                # 1. DIAGNOSZTIKA: Mit kaptunk?
                # print(f"DEBUG RAW RECV: {message}") # Kommentezve: konzol szemetelés elkerülése

                # JSON dekódolás
                tick_data = json.loads(message)

                # 2. KONVERZIÓ
                # JForex timestamp ms-ben jön, Python sec-et vár
                ts_ms = tick_data.get("timestamp")
                if ts_ms:
                    timestamp = datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
                else:
                    timestamp = datetime.now(timezone.utc)

                # 3. EVENT LÉTREHOZÁS
                from neural_ai.core.events.interfaces.event_models import MarketDataEvent
                event = MarketDataEvent(
                    symbol=tick_data["symbol"],
                    timestamp=timestamp,
                    bid=float(tick_data["bid"]),
                    ask=float(tick_data["ask"]),
                    volume=None,
                    source="jforex"
                )

                # 4. PUBLIKÁLÁS
                if self.event_bus:
                    await self.event_bus.publish("market_data", event)
                    # print(f"DEBUG: Published {event.symbol}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                # 5. DIAGNOSZTIKA: Mi a baj?
                import traceback
                print("!!! CRITICAL LIVE FEED ERROR !!!")
                traceback.print_exc()
                
                self.logger.error("jforex_live_feed_listen_loop_error", error=str(e))
                await asyncio.sleep(1)
    
    async def _process_tick_data(self, data: dict) -> None:
        """
        Feldolgozza a tick adatokat és publikálja az EventBus-on.
        
        Args:
            data: A tick adatok dictionary-ben
        """
        try:
            # MarketDataEvent létrehozása
            event = MarketDataEvent(
                symbol=data.get("symbol", ""),
                timestamp=datetime.fromisoformat(data.get("timestamp", "")),
                bid=float(data.get("bid", 0.0)),
                ask=float(data.get("ask", 0.0)),
                volume=int(data.get("volume", 0)) if data.get("volume") else None,
                source="jforex"
            )
            
            # Esemény publikálása
            await self.event_bus.publish("market_data", event)
            
            # Naplózás (csak debug módban)
            self.logger.debug(
                "jforex_live_feed_tick_received",
                symbol=event.symbol,
                bid=event.bid,
                ask=event.ask
            )
            
        except Exception as e:
            self.logger.error(
                "jforex_live_feed_process_tick_error: error=%s, raw_message=%s",
                str(e),
                str(data),
                exc_info=True  # Teljes traceback kiírása
            )