"""MarketDataPersister szolgáltatás.

Ez a modul implementálja a MarketDataPersister osztályt, amely felelős
a bejövő market data eventek bufferezéséért és időzített mentéséért
a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
from collections import defaultdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast

from neural_ai.core.config.interfaces.types import IngestionConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent

if TYPE_CHECKING:
    from neural_ai.core.events.interfaces.event_bus_interface import (
        EventBusInterface,
    )
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


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
        logger: "LoggerInterface",
        config: IngestionConfig,
    ) -> None:
        """Inicializálja a MarketDataPersister-t.

        Args:
            event_bus: Az EventBus interfész példánya
            storage: A Storage interfész példánya
            logger: A Logger interfész példánya
            config: Az ingestion konfiguráció
        """
        self.event_bus = event_bus
        self.storage = storage
        self.logger = logger
        self.config = config
        self.buffer_size_limit = config.buffer_size_limit or 10_000
        self.flush_interval_minutes = config.flush_interval_minutes or 60

        # Buffer szimbólumonként csoportosítva
        self.buffer: dict[str, list[MarketDataEvent]] = defaultdict(list)
        self.current_hour = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
        self.running = False

        self.logger.info(
            "MarketDataPersister inicializálva",
            extra={
                "buffer_size_limit": self.buffer_size_limit,
                "flush_interval_minutes": self.flush_interval_minutes,
            },
        )

    async def start(self) -> None:
        """Elindítja a MarketDataPersister szolgáltatást.

        Feliratkozás a market_data topicra és elindítja a háttérfeladatot
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
        self.logger.info("✅ MarketDataPersister feliratkozva a market_data topicra")

        self.logger.info("MarketDataPersister elindítva")

        # Háttérfeladat indítása időzített flush-hoz
        asyncio.create_task(self._periodic_flush_task())

        # EventBus fogyasztó task indítása
        asyncio.create_task(self.event_bus.run_forever())

    async def stop(self) -> None:
        """Leállítja a MarketDataPersister szolgáltatást.

        Kiüríti a maradék buffert és leiratkozik az eventekről.
        """
        if not self.running:
            self.logger.warning("MarketDataPersister már leállt vagy nem is futott")
            return

        self.running = False

        self.logger.info("MarketDataPersister leállítás indítása...")

        # Először leiratkozás, hogy ne jöjjenek új eventek
        from neural_ai.core.events.interfaces.event_bus_interface import EventCallback

        callback = cast(EventCallback, self.on_market_data)
        self.event_bus.unsubscribe("market_data", callback)
        self.logger.info("Leiratkozva a market_data topicról")

        # Várunk 2 másodpercet, hogy a ZMQ-nak legyen ideje kiüríteni a bejövő csövet
        await asyncio.sleep(2.0)
        self.logger.info("ZMQ buffer kiürítési idő letelt")

        # Maradék buffer kiürítése (FONTOS: védett try-except blokk!)
        buffer_before = {k: len(v) for k, v in self.buffer.items() if v}
        self.logger.info("Maradék buffer kiürítése", extra={"buffer_before": buffer_before})

        try:
            await self._flush_all_buffers()
        except Exception as e:
            self.logger.error("Hiba a buffer kiürítésekor", extra={"error": str(e)})
            # Fontos: még hiba esetén is folytatjuk, hogy a többi leállítási lépés lefusson

        # Ellenőrizzük, hogy tényleg kiürült-e a buffer
        buffer_after = {k: len(v) for k, v in self.buffer.items() if v}
        total_remaining = sum(buffer_after.values())

        if total_remaining > 0:
            self.logger.warning(
                "Buffer kiürítése után maradt event a bufferben",
                extra={
                    "total_remaining": total_remaining,
                    "before": sum(buffer_before.values()),
                    "after": total_remaining,
                },
            )
        else:
            self.logger.info(
                "Buffer sikeresen kiürítve",
                extra={"before": sum(buffer_before.values()), "after": 0},
            )

        self.logger.info("MarketDataPersister leállítva")

    async def on_market_data(self, event: MarketDataEvent | list[MarketDataEvent]) -> None:
        """Fogadja a market data eventeket (vagy batch listát) és bufferezi őket.

        Args:
            event: Egy MarketDataEvent VAGY MarketDataEvent-ek listája.
        """
        self.logger.info("on_market_data called", extra={"event_type": str(type(event))})
        new_events: list[MarketDataEvent] = []

        # 1. ESET: Lista (Batch) érkezett
        if isinstance(event, list):
            # Type check: ensure all items are MarketDataEvent
            for item in event:
                if hasattr(item, "symbol"):
                    new_events.append(item)  # item is MarketDataEvent

        # 2. ESET: Egyetlen Event érkezett
        elif hasattr(event, "symbol"):  # Pydantic model check
            new_events = [event]  # event is MarketDataEvent

        else:
            self.logger.warning("unknown_event_format", extra={"event_type": str(type(event))})
            return

        if not new_events:
            return

        # Adatok hozzáadása a bufferhez
        for ev in new_events:
            # Biztonsági ellenőrzés, ha a listában nem eventek lennének
            if not hasattr(ev, "symbol"):
                continue
            self.buffer[ev.symbol].append(ev)

        # Buffer méret ellenőrzése
        total_buffered = sum(len(events) for events in self.buffer.values())

        # Logolás (de csak okosan, nem dumpoljuk a teljes listát!)
        self.logger.debug(
            "market_data_received",
            extra={"count": len(new_events), "total_buffered": total_buffered},
        )

        if total_buffered >= self.buffer_size_limit:
            self.logger.info(
                "Buffer méretkorlát elérve, kiürítés indítása",
                extra={"total_buffered": total_buffered},
            )
            await self._flush_all_buffers()

    async def _periodic_flush_task(self) -> None:
        """Háttérfeladat az időzített buffer kiürítéshez.

        Minden órában ellenőrzi, hogy új óra kezdődött-e,
        és ha igen, kiüríti a buffert.
        """
        while self.running:
            try:
                await asyncio.sleep(60)  # Minden percben ellenőriz

                now = datetime.now(UTC)
                current_hour = now.replace(minute=0, second=0, microsecond=0)

                if current_hour > self.current_hour:
                    # Új óra kezdődött, kiürítjük a buffert
                    self.logger.info(
                        "Új óra kezdődött, buffer kiürítése",
                        extra={
                            "old_hour": self.current_hour.isoformat(),
                            "new_hour": current_hour.isoformat(),
                        },
                    )
                    await self._flush_all_buffers()
                    self.current_hour = current_hour

            except Exception as e:
                self.logger.error("Hiba a periodikus flush során", extra={"error": str(e)})

    async def _flush_all_buffers(self) -> None:
        """Kiüríti az összes buffert és elmenti a tárolóba.

        Szimbólumonként csoportosítva konvertálja DataFrame-é és menti.
        """
        buffer_keys = list(self.buffer.keys())
        self.logger.info("_flush_all_buffers called", extra={"buffer_keys": buffer_keys})

        # Részletes buffer állapot logolása
        buffer_stats = {symbol: len(events) for symbol, events in self.buffer.items() if events}
        self.logger.info("Buffer statisztika", extra={"buffer_stats": buffer_stats})

        if not any(self.buffer.values()):
            # Nincs mit kiüríteni
            self.logger.info("Nincs mit kiüríteni, a buffer üres")
            return

        total_saved = 0
        for symbol, events in self.buffer.items():
            if events:
                try:
                    event_count = len(events)
                    self.logger.info(
                        "Buffer kiürítése szimbólumhoz",
                        extra={"symbol": symbol, "event_count": event_count},
                    )
                    await self._flush_symbol_buffer(symbol, events)
                    total_saved += event_count
                    self.logger.info(
                        "Szimbólum buffer kiürítve",
                        extra={"symbol": symbol, "events_saved": event_count},
                    )
                except Exception as e:
                    self.logger.error(
                        "Hiba a buffer kiürítésekor szimbólumhoz",
                        extra={"symbol": symbol, "error": str(e)},
                    )

        # Buffer ürítése
        self.buffer.clear()

        self.logger.info("Összes buffer kiürítve", extra={"total_saved": total_saved})

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
        self, symbol: str, events: list[MarketDataEvent], date: datetime
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
            from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService

            if isinstance(self.storage, ParquetStorageService):
                row_count = len(df)
                self.logger.info(
                    "Tárolás ParquetStorageService-be",
                    extra={"symbol": symbol, "date": date.isoformat(), "row_count": row_count},
                )
                await self.storage.store_tick_data(symbol, df, date)
            else:
                # Fallback: használjuk a save_dataframe metódust
                row_count = len(df)
                self.logger.info(
                    "Tárolás save_dataframe-mal",
                    extra={"symbol": symbol, "date": date.isoformat(), "row_count": row_count},
                )
                path = f"/data/tick/{symbol}/{date.strftime('%Y/%m/%d')}/data.parquet"
                kwargs: dict[str, Any] = {"symbol": symbol, "date": date}
                self.storage.save_dataframe(df, path, **kwargs)

            self.logger.info(
                "Tick adatok elmentve",
                extra={"symbol": symbol, "date": date.strftime("%Y-%m-%d"), "rows": len(events)},
            )

        except Exception as e:
            import traceback

            self.logger.error(
                "Hiba az adatok mentésekor",
                extra={
                    "symbol": symbol,
                    "date": date.strftime("%Y-%m-%d"),
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                },
            )
            raise

    def _convert_events_to_dataframe(self, events: list[MarketDataEvent]) -> Any:
        """Konvertálja az eventeket DataFrame-é.

        Args:
            events: A konvertálandó eventek listája

        Returns:
            A konvertált DataFrame
        """
        # Ellenőrizzük, hogy a storage melyik backend-et használja
        from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService

        if isinstance(self.storage, ParquetStorageService):
            # Ha Polars backend-et használunk, akkor Polars DataFrame-et hozunk létre
            if self.storage.engine == "polars":
                try:
                    import polars as pl

                    polars_data: dict[str, list[Any]] = {
                        "timestamp": [e.timestamp for e in events],
                        "bid": [e.bid for e in events],
                        "ask": [e.ask for e in events],
                        "volume": [e.volume for e in events],
                        "source": [e.source for e in events],
                    }

                    df = pl.DataFrame(polars_data)
                    df = df.sort("timestamp")

                    return df

                except ImportError as err:
                    raise RuntimeError(
                        "Polars nincs telepítve, de a Polars backend van kiválasztva"
                    ) from err
            else:
                # Ha Pandas backend-et használunk, akkor Pandas DataFrame-et hozunk létre
                try:
                    import pandas as pd

                    pandas_data: dict[str, list[Any]] = {
                        "timestamp": [e.timestamp for e in events],
                        "bid": [e.bid for e in events],
                        "ask": [e.ask for e in events],
                        "volume": [e.volume for e in events],
                        "source": [e.source for e in events],
                    }

                    df = pd.DataFrame(pandas_data)
                    df = df.sort_values("timestamp").reset_index(drop=True)

                    return df

                except ImportError as err:
                    raise RuntimeError(
                        "Pandas nincs telepítve, de a Pandas backend van kiválasztva"
                    ) from err
        else:
            # Ha nem ParquetStorageService-t használunk, akkor
            # alapértelmezésként Pandas-t használunk
            try:
                import pandas as pd

                default_pandas_data: dict[str, list[Any]] = {
                    "timestamp": [e.timestamp for e in events],
                    "bid": [e.bid for e in events],
                    "ask": [e.ask for e in events],
                    "volume": [e.volume for e in events],
                    "source": [e.source for e in events],
                }

                df = pd.DataFrame(default_pandas_data)
                df = df.sort_values("timestamp").reset_index(drop=True)

                return df

            except ImportError:
                # Ha pandas nincs, próbáljuk polars-t
                try:
                    import polars as pl

                    fallback_polars_data: dict[str, list[Any]] = {
                        "timestamp": [e.timestamp for e in events],
                        "bid": [e.bid for e in events],
                        "ask": [e.ask for e in events],
                        "volume": [e.volume for e in events],
                        "source": [e.source for e in events],
                    }

                    df = pl.DataFrame(fallback_polars_data)
                    df = df.sort("timestamp")

                    return df

                except ImportError as err:
                    raise RuntimeError("Sem pandas, sem polars nincs telepítve") from err
