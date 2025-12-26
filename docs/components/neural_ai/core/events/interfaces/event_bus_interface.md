# EventBus Interface

## Áttekintés

Az `EventBusInterface` egy absztrakt interfész, amely definiálja az eseménybusz alapvető műveleteit a Neural AI Next rendszerben. Ez az interfész biztosítja a Dependency Injection (DI) alapú architektúra megvalósítását, lehetővé téve a különböző EventBus implementációk egyszerű cseréjét.

## Jellemzők

### EventBusConfig

Az EventBus konfigurációját leíró adat osztály.

```python
@dataclass
class EventBusConfig:
    zmq_context: Any = None
    pub_port: int = 5555
    sub_port: int = 5556
    use_inproc: bool = False
```

**Paraméterek:**
- `zmq_context`: ZeroMQ kontextus (opcionális)
- `pub_port`: Publisher port (alapértelmezett: 5555)
- `sub_port`: Subscriber port (alapértelmezett: 5556)
- `use_inproc`: Inproc transport használata teszteléshez (alapértelmezett: False)

### EventBusInterface

Az eseménybusz alapvető műveleteit definiáló interfész.

#### Metódusok

##### `config` property
```python
@property
@abstractmethod
def config(self) -> EventBusConfig:
    """Visszaadja az EventBus konfigurációját."""
```

##### `start()`
```python
@abstractmethod
async def start(self) -> None:
    """Elindítja az EventBus-t és létrehozza a socketeket."""
```

##### `stop()`
```python
@abstractmethod
async def stop(self) -> None:
    """Leállítja az EventBus-t és felszabadítja az erőforrásokat."""
```

##### `publish()`
```python
@abstractmethod
async def publish(self, event_type: str, event: "BaseModel") -> None:
    """Esemény közzététele a buszon.
    
    Args:
        event_type: Az esemény típusa (pl. 'market_data', 'trade')
        event: Az esemény objektum (Pydantic BaseModel)
    
    Raises:
        EventBusError: Ha az EventBus nincs elindítva
        PublishError: Ha a publisher socket nincs inicializálva
    """
```

##### `subscribe()`
```python
@abstractmethod
def subscribe(self, event_type: str, callback: EventCallback) -> None:
    """Feliratkozás eseménytípusra.
    
    Args:
        event_type: Az esemény típusa, amire feliratkozunk
        callback: A callback függvény, amely az eseményt fogadja
    """
```

##### `unsubscribe()`
```python
@abstractmethod
def unsubscribe(self, event_type: str, callback: EventCallback) -> None:
    """Leiratkozás eseménytípusról.
    
    Args:
        event_type: Az esemény típusa
        callback: A callback függvény, amelyet eltávolítunk
    """
```

##### `run_forever()`
```python
@abstractmethod
async def run_forever(self) -> None:
    """Eseménybusz örök futás (blokkoló).
    
    Ez a metódus egy végtelen ciklusban fogadja az eseményeket
    és továbbítja azokat a feliratkozóknak.
    """
```

## Használat

### Factory használata

Az EventBus létrehozásához mindig az `EventBusFactory`-t használjuk:

```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces import EventBusConfig

# Alapértelmezett konfiguráció
bus = EventBusFactory.create()

# Egyéni konfiguráció
config = EventBusConfig(use_inproc=True, pub_port=6666)
bus = EventBusFactory.create(config=config)
```

### Interfész használata

A kódban mindig az interfészt használjuk, ne a konkrét implementációt:

```python
from neural_ai.core.events.interfaces import EventBusInterface, EventBusConfig
from neural_ai.core.events.factory import EventBusFactory

class MyComponent:
    def __init__(self, event_bus: EventBusInterface):
        self.event_bus = event_bus
    
    async def process_data(self):
        await self.event_bus.start()
        # ... események küldése/fogadása
```

## Implementációk

### ZeroMQ Bus

A `zeromq_bus.py` fájl tartalmazza a ZeroMQ alapú implementációt:

```python
from neural_ai.core.events.implementations.zeromq_bus import EventBus

# Az EventBus osztály implementálja az EventBusInterface-t
```

## Típusok

### EventCallback

```python
from collections.abc import Callable
from typing import Any
from pydantic import BaseModel

EventCallback = Callable[["BaseModel"], Any]
```

Ez a típusalias definiálja a callback függvények signatúráját, amelyek eseményeket fogadnak.

## Hibakezelés

Az interfész a következő kivételeket használja:

- `EventBusError`: Általános EventBus hiba
- `PublishError`: Közzétételi hiba

## Tesztelés

A teszteléshez használjuk a Factory-t és mock objektumokat:

```python
import pytest
from unittest.mock import AsyncMock
from neural_ai.core.events.factory import EventBusFactory

def test_subscribe():
    bus = EventBusFactory.create()
    callback = AsyncMock()
    
    bus.subscribe("market_data", callback)
    # A teszt a viselkedést ellenőrzi, nem a belső állapotot
```

## Architektúra

Az EventBus interfész része a Neural AI Next DI architektúrájának:

1. **Interfész**: `EventBusInterface` definiálja a szerződést
2. **Implementáció**: `EventBus` (ZeroMQ) megvalósítja az interfészt
3. **Factory**: `EventBusFactory` felelős a példányosításért
4. **Használat**: A kliensek csak az interfészt és a factory-t használják

Ez az architektúra biztosítja a laza csatolást és a tesztelhetőséget.