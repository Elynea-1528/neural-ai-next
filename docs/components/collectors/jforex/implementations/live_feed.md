# collectors/jforex/implementations/live_feed.py

JForex Live Feed Implementation.

Ez a modul implementálja a JForex live adatfolyam fogadását ZMQ socketen keresztül
a Java Bridge-el (NeuralBridgeStrategy) való kommunikációhoz.

## Osztályok

### `JForexLiveFeed`

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


## Függvények

### `__init__`

Inicializálja a JForexLiveFeed osztályt.
        
        Args:
            logger: Logger példány
            event_bus: Event bus példány
            config: Konfiguráció kezelő példány

### `start`

Indítja a live adatfolyam fogadását.
        
        Létrehozza a ZMQ SUB socketet, csatlakozik a megadott portra, és elindítja
        a háttérfolyamatot (_listen_loop) a tickek folyamatos fogadásához.
        
        Raises:
            LiveFeedError: Ha a csatlakozás vagy a fogadás során hiba történik.

### `stop`

Leállítja a live adatfolyam fogadását.
        
        Megszünteti a ZMQ kapcsolatot és leállítja a háttérfolyamatot.

### `is_running`

Visszaadja, hogy a live feed jelenleg fut-e.
        
        Returns:
            bool: True, ha a feed fut, False egyébként.

### `_listen_loop`

Háttérfolyamat a tickek folyamatos fogadásához.
        
        Ez a metódus egy végtelen ciklusban vár a ZMQ socketre érkező üzenetekre,
        dekódolja a JSON adatokat, és továbbítja a `_process_tick_data` metódusnak
        a teljes feldolgozásért és publikálásért.

### `_process_tick_data`

Feldolgozza a tick adatokat és publikálja az EventBus-on.

        A `_listen_loop` metódusból kapja a már dekódolt JSON adatokat.
        A timestamp milliszekundumban érkezik, ezért osztani kell 1000-el.
        A bid/ask értékek már float-ként érkeznek, nem kell castolni.
        Az ask_volume és bid_volume mezőket kiolvassa a JSON-ből és hozzáadja az event-hez.

        Args:
            data: A tick adatok dictionary-ben (timestamp ms-ban, bid/ask float, ask_volume/bid_volume float)


---

**Forrásfájl:** [`collectors/jforex/implementations/live_feed.py`](../../../neural_ai/collectors/jforex/implementations/live_feed.py)
