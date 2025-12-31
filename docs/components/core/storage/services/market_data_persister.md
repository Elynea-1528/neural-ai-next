# core/storage/services/market_data_persister.py

MarketDataPersister szolgáltatás.

Ez a modul implementálja a MarketDataPersister osztályt, amely felelős
a bejövő market data eventek bufferezéséért és időzített mentéséért
a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0

## Osztályok

### `MarketDataPersister`

Market data eventeket bufferez és menti a tárolóba.

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


## Függvények

### `__init__`

Inicializálja a MarketDataPersister-t.

        Args:
            event_bus: Az EventBus interfész példánya
            storage: A Storage interfész példánya
            logger: A Logger interfész példánya (opcionális)
            buffer_size_limit: A buffer méretkorlátja tick-ekben

### `start`

Elindítja a MarketDataPersister szolgáltatást.
        
        Feliratkozás a market_data topicra és elindítja a háttérfeladatot
        az időzített flush-hoz.

### `stop`

Leállítja a MarketDataPersister szolgáltatást.
        
        Kiüríti a maradék buffert és leiratkozik az eventekről.

### `on_market_data`

Fogadja a market data eventeket (vagy batch listát) és bufferezi őket.

        Args:
            event: Egy MarketDataEvent VAGY MarketDataEvent-ek listája.

### `_periodic_flush_task`

Háttérfeladat az időzített buffer kiürítéshez.
        
        Minden órában ellenőrzi, hogy új óra kezdődött-e,
        és ha igen, kiüríti a buffert.

### `_flush_all_buffers`

Kiüríti az összes buffert és elmenti a tárolóba.
        
        Szimbólumonként csoportosítva konvertálja DataFrame-é és menti.

### `_flush_symbol_buffer`

Kiüríti egy adott szimbólum bufferét.

        Args:
            symbol: A szimbólum neve
            events: A kiürítendő eventek listája

### `_save_events_to_storage`

Elmenti az eventeket a tárolóba.

        Args:
            symbol: A szimbólum neve
            events: Az elmentendő eventek listája
            date: A dátum, ami alapján a particionálás történik

### `_convert_events_to_dataframe`

Konvertálja az eventeket DataFrame-é.

        Args:
            events: A konvertálandó eventek listája

        Returns:
            A konvertált DataFrame


---

**Forrásfájl:** [`core/storage/services/market_data_persister.py`](../../../neural_ai/core/storage/services/market_data_persister.py)
