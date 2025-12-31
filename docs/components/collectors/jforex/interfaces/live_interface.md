# collectors/jforex/interfaces/live_interface.py

Live Feed Interface for JForex Live Data Collection.

Ez az interfész definiálja a JForex live adatfolyam fogadásához szükséges metódusokat.
Az implementációk ezt az interfészt használják a ZMQ-alapú tick fogadáshoz.

## Osztályok

### `ILiveFeed`

Absztrakt osztály a JForex live adatfolyam kezeléséhez.
    
    Ez az interfész felelős a Java Bridge-el (NeuralBridgeStrategy) való kommunikációért
    ZMQ socketeken keresztül. A start() metódus indítja el a tick fogadást, a stop() pedig
    leállítja azt.


## Függvények

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


---

**Forrásfájl:** [`collectors/jforex/interfaces/live_interface.py`](../../../neural_ai/collectors/jforex/interfaces/live_interface.py)
