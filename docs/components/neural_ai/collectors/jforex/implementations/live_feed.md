# neural_ai/collectors/jforex/implementations/live_feed.py

JForex Live Feed Implementation.

Ez a modul implementálja a JForex live adatfolyam fogadását ZMQ socketen keresztül
a Java Bridge-el (NeuralBridgeStrategy) való kommunikációhoz.

## Importok

```python
import asyncio
import json
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import cast
import zmq
import zmq.asyncio
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
# ... és még 4 import
```

## Osztály: `JForexLiveFeed(ILiveFeed)`

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

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', event_bus: 'EventBusInterface', config: 'ConfigManagerInterface') -> None
```

Inicializálja a JForexLiveFeed osztályt.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): Logger példány
- **`event_bus`** (`'EventBusInterface'`): Event bus példány
- **`config`** (`'ConfigManagerInterface'`): Konfiguráció kezelő példány

**Visszatérési érték:**

- Típus: `None`

#### `start()`

```python
async def start(self) -> None
```

Indítja a live adatfolyam fogadását. Létrehozza a ZMQ SUB socketet, csatlakozik a megadott portra, és elindítja a háttérfolyamatot (_listen_loop) a tickek folyamatos fogadásához.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`LiveFeedError`**: Ha a csatlakozás vagy a fogadás során hiba történik.

#### `stop()`

```python
async def stop(self) -> None
```

Leállítja a live adatfolyam fogadását. Megszünteti a ZMQ kapcsolatot és leállítja a háttérfolyamatot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `is_running()`

```python
def is_running(self) -> bool
```

Visszaadja, hogy a live feed jelenleg fut-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a feed fut, False egyébként.

#### `_listen_loop()`

```python
async def _listen_loop(self) -> None
```

Háttérfolyamat a tickek folyamatos fogadásához. Ez a metódus egy végtelen ciklusban vár a ZMQ socketre érkező üzenetekre, dekódolja a JSON adatokat, és továbbítja a `_process_tick_data` metódusnak a teljes feldolgozásért és publikálásért.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_process_tick_data()`

```python
async def _process_tick_data(self, data: dict[str, object]) -> None
```

Feldolgozza a tick adatokat és publikálja az EventBus-on. A `_listen_loop` metódusból kapja a már dekódolt JSON adatokat. A timestamp milliszekundumban érkezik, ezért osztani kell 1000-el. A bid/ask értékek már float-ként érkeznek, nem kell castolni. Az ask_volume és bid_volume mezőket kiolvassa a JSON-ből és hozzáadja az event-hez.

**Paraméterek:**

- **`self`**
- **`data`** (`dict[str, object]`): A tick adatok dictionary-ben (timestamp ms-ban, bid/ask float, ask_volume/bid_volume float)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/collectors/jforex/implementations/live_feed.py`](../../neural_ai/collectors/jforex/implementations/live_feed.py)
