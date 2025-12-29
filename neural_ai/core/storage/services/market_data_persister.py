"""MarketDataPersister szolgáltatás.

Ez a modul implementálja a MarketDataPersister osztályt, amely felelős
a bejövő market data eventek bufferezéséért és időzített mentéséért
a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
from collections import defaultdict
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, cast

import structlog

from neural_ai.core.events.interfaces.event_models import MarketDataEvent

if TYPE_CHECKING:
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

logger = structlog.get_logger()


class MarketDataPersister:
    """Market data eventeket bufferez és menti a tárolóba.

    Ez az osztály felelős azért, hogy a bejövő market data eventeket
    gyűjtse egy belső bufferbe, és amikor a buffer eléri a méretkorlátot
    vagy új óra kezdődik, akkor a buffert kiürítse és elmentse a
    Parquet tárolóba.

    Attributes:
        event_bus: Az EventBus interfész példánya
        storage: A Storage interfész példánya
        logger: A Logger interfész példánya
        buffer: A tick adatok buffere szimbólumonként csoportosítva
        buffer_size_limit: A buffer méretkorlátja (alapértelmezett: 10.000 tick)
        current_hour: Az aktuális óra az időzített flush-hoz
        running: A szolgáltatás futásállapota
    """

    def __init__(
        self,
        event_bus: "EventBusInterface",
        storage: "StorageInterface",
        logger: "LoggerInterface | None" = None,
        buffer_size_limit: int = 10_000,
    ) -> None:
        """Inicializálja a MarketDataPersister-t.

        Args:
            event_bus: Az EventBus interfész példánya
            storage: A Storage interfész példánya
            logger: A Logger interfész példánya (opcionális)
            buffer_size_limit: A buffer méretkorlátja tick-ekben
        """
        self.event_bus = event_bus
        self.storage = storage
        self.logger = logger if logger else structlog.get_logger()
        self.buffer_size_limit = buffer_size_limit
        
        # Buffer szimbólumonként csoportosítva
        self.buffer: dict[str, list[MarketDataEvent]] = defaultdict(list)
        self.current_hour = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        self.running = False
        
        self.logger.info(f"MarketDataPersister inicializálva, buffer_size_limit={buffer_size_limit}")

    async def start(self) -> None:
        """Elindítja a MarketDataPersister szolgáltatást.
        
        Feliratkozik a market_data topicra és elindítja a háttérfeladatot
        az időzített flush-hoz.
        """
        if self.running:
            self.logger.warning("MarketDataPersister már fut")
            return

        self.running = True
        
        # Feliratkozás a market_data topicra
        # Type cast to satisfy the interface
        from neural_ai.core.events.interfaces.event_bus_interface import EventCallback
        callback = cast(EventCallback, self.on_market_data)
        self.event_bus.subscribe("market_data", callback)
        
        self.logger.info("MarketDataPersister elindítva")
        
        # Háttérfeladat indítása időzített flush-hoz
        asyncio.create_task(self._periodic_flush_task())

    async def stop(self) -> None:
        """Leállítja a MarketDataPersister szolgáltatást.
        
        Kiüríti a maradék buffert és leiratkozik az eventekről.
        """
        if not self.running:
            return

        self.running = False
        
        # Leiratkozás
        # Type cast to satisfy the interface
        from neural_ai.core.events.interfaces.event_bus_interface import EventCallback
        callback = cast(EventCallback, self.on_market_data)
        self.event_bus.unsubscribe("market_data", callback)
        
        # Maradék buffer kiürítése
        await self._flush_all_buffers()
        
        self.logger.info("MarketDataPersister leállítva")

    async def on_market_data(self, event: MarketDataEvent) -> None:
        """Fogadja a market data eventeket és bufferezi őket.

        Args:
            event: A fogadott MarketDataEvent
        """
        symbol = event.symbol
        self.buffer[symbol].append(event)
        
        # Ellenőrizzük, hogy elértük-e a buffer méretkorlátot
        total_buffered = sum(len(events) for events in self.buffer.values())
        if total_buffered >= self.buffer_size_limit:
            self.logger.info(f"Buffer méretkorlát elérve, kiürítés indítása, total_buffered={total_buffered}")
            await self._flush_all_buffers()

    async def _periodic_flush_task(self) -> None:
        """Háttérfeladat az időzített buffer kiürítéshez.
        
        Minden órában ellenőrzi, hogy új óra kezdődött-e,
        és ha igen, kiüríti a buffert.
        """
        while self.running:
            try:
                await asyncio.sleep(60)  # Minden percben ellenőriz
                
                now = datetime.now(timezone.utc)
                current_hour = now.replace(minute=0, second=0, microsecond=0)
                
                if current_hour > self.current_hour:
                    # Új óra kezdődött, kiürítjük a buffert
                    self.logger.info(
                        f"Új óra kezdődött, buffer kiürítése, old_hour={self.current_hour}, new_hour={current_hour}"
                    )
                    await self._flush_all_buffers()
                    self.current_hour = current_hour
                    
            except Exception as e:
                self.logger.error(f"Hiba a periodikus flush során: {e}")

    async def _flush_all_buffers(self) -> None:
        """Kiüríti az összes buffert és elmenti a tárolóba.
        
        Szimbólumonként csoportosítva konvertálja DataFrame-é és menti.
        """
        if not any(self.buffer.values()):
            # Nincs mit kiüríteni
            return

        for symbol, events in self.buffer.items():
            if events:
                try:
                    await self._flush_symbol_buffer(symbol, events)
                except Exception as e:
                    self.logger.error(
                        f"Hiba a buffer kiürítésekor {symbol} szimbólumhoz: {e}"
                    )
        
        # Buffer ürítése
        self.buffer.clear()
        
        self.logger.info("Összes buffer kiürítve")

    async def _flush_symbol_buffer(self, symbol: str, events: list[MarketDataEvent]) -> None:
        """Kiüríti egy adott szimbólum bufferét.

        Args:
            symbol: A szimbólum neve
            events: A kiürítendő eventek listája
        """
        if not events:
            return

        # Eventek dátum szerinti csoportosítása
        events_by_date: dict[datetime, list[MarketDataEvent]] = defaultdict(list)
        
        for event in events:
            # Dátum kinyerése (csak dátum rész, óra-perc-másodperc nélkül)
            event_date = event.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            events_by_date[event_date].append(event)

        # Minden dátumhoz külön mentés
        for date, date_events in events_by_date.items():
            await self._save_events_to_storage(symbol, date_events, date)

    async def _save_events_to_storage(
        self,
        symbol: str,
        events: list[MarketDataEvent],
        date: datetime
    ) -> None:
        """Elmenti az eventeket a tárolóba.

        Args:
            symbol: A szimbólum neve
            events: Az elmentendő eventek listája
            date: A dátum, ami alapján a particionálás történik
        """
        if not events:
            return

        try:
            # DataFrame létrehozása az eventekből
            df = self._convert_events_to_dataframe(events)
            
            # Tárolás a Parquet tárolóban
            # Type cast to access store_tick_data if it exists
            from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService
            if isinstance(self.storage, ParquetStorageService):
                await self.storage.store_tick_data(symbol, df, date)  # type: ignore
            else:
                # Fallback: használjuk a save_dataframe metódust
                path = f"/data/tick/{symbol}/{date.strftime('%Y/%m/%d')}/data.parquet"
                kwargs: dict[str, Any] = {'symbol': symbol, 'date': date}
                self.storage.save_dataframe(df, path, **kwargs)
            
            self.logger.info(
                f"Tick adatok elmentve, symbol={symbol}, date={date.strftime('%Y-%m-%d')}, rows={len(events)}"
            )
            
        except Exception as e:
            self.logger.error(
                f"Hiba az adatok mentésekor, symbol={symbol}, date={date.strftime('%Y-%m-%d')}, error={str(e)}"
            )
            raise

    def _convert_events_to_dataframe(self, events: list[MarketDataEvent]) -> Any:
        """Konvertálja az eventeket DataFrame-é.

        Args:
            events: A konvertálandó eventek listája

        Returns:
            A konvertált DataFrame
        """
        try:
            import pandas as pd
            
            # Adatok előkészítése
            data: dict[str, list[Any]] = {
                'timestamp': [e.timestamp for e in events],
                'bid': [e.bid for e in events],
                'ask': [e.ask for e in events],
                'volume': [e.volume for e in events],
                'source': [e.source for e in events]
            }
            
            df = pd.DataFrame(data)
            
            # Rendezés időbélyeg szerint
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            return df
            
        except ImportError:
            # Ha pandas nincs telepítve, próbáljuk meg Polars-t
            try:
                import polars as pl
                
                data: dict[str, list[Any]] = {
                    'timestamp': [e.timestamp for e in events],
                    'bid': [e.bid for e in events],
                    'ask': [e.ask for e in events],
                    'volume': [e.volume for e in events],
                    'source': [e.source for e in events]
                }
                
                df = pl.DataFrame(data)
                df = df.sort('timestamp')
                
                return df
                
            except ImportError:
                raise RuntimeError("Sem pandas, sem polars nincs telepítve")