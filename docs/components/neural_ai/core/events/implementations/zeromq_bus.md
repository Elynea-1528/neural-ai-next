# ZeroMQ EventBus Implementáció

## Áttekintés

EventBus implementáció ZeroMQ-val és asyncio-val. Ez a modul biztosítja az eseményvezérelt architektúra magját, lehetővé téve a komponensek közötti laza csatolást Pub/Sub mintázattal.

## Osztályok

### `EventBusConfig`

EventBus konfiguráció.

```python
@dataclass
class EventBusConfig:
    """EventBus konfiguráció.

    Attributes:
        zmq_context: ZeroMQ kontextus (opcionális, létrejön ha nincs megadva)
        pub_port: Publisher port (alapértelmezett: 5555)
        sub_port: Subscriber port (alapértelmezett: 5556)
        use_inproc: Használjon inproc transportot teszteléshez (alapértelmezett: False)
    """
```

**Attribútumok:**
- `zmq_context` (Optional[zmq.asyncio.Context]): ZeroMQ kontextus
- `pub_port` (int): Publisher port, alapértelmezett: 5555
- `sub_port` (int): Subscriber port, alapértelmezett: 5556
- `use_inproc` (bool): Inproc transport teszteléshez, alapértelmezett: False

**Példa használat:**

```python
from neural_ai.core.events.implementations.zeromq_bus import EventBusConfig

# Alapértelmezett konfiguráció
config = EventBusConfig()

# Egyéni portokkal
config = EventBusConfig(
    pub_port=6666,
    sub_port=6667
)

# Teszteléshez inproc transporttal
config = EventBusConfig(use_inproc=True)
```

### `EventBus`

ZeroMQ alapú aszinkron eseménybusz.

```python
class EventBus:
    """ZeroMQ alapú aszinkron eseménybusz.

    Ez az osztály biztosítja az események közzétételét és feliratkozást
    a rendszer különböző komponensei számára. A ZeroMQ PUB/SUB mintázatot használja.
    """
```

#### Inicializálás

```python
def __init__(self, config: EventBusConfig | None = None) -> None:
    """Inicializálja az EventBus-t.

    Args:
        config: EventBus konfiguráció (opcionális)
    """
```

**Példa:**

```python
from neural_ai.core.events.implementations.zeromq_bus import EventBus, EventBusConfig

config = EventBusConfig(pub_port=6666)
event_bus = EventBus(config)
```

#### Metódusok

##### `start()`

Elindítja az EventBus-t és létrehozza a socketeket.

```python
async def start(self) -> None:
    """Elindítja az EventBus-t és létrehozza a socketeket."""
```

**Példa:**

```python
await event_bus.start()
```

##### `stop()`

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

```python
async def stop(self) -> None:
    """Leállítja az EventBus-t és felszabadítja az erőforrásokat."""
```

**Példa:**

```python
await event_bus.stop()
```

##### `publish()`

Esemény közzététele a buszon.

```python
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

**Példa:**

```python
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from datetime import datetime, UTC

event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    bid=1.0850,
    ask=1.0852,
    source="mt5"
)

await event_bus.publish("market_data", event)
```

##### `subscribe()`

Feliratkozás eseménytípusra.

```python
def subscribe(self, event_type: str, callback: EventCallback) -> None:
    """Feliratkozás eseménytípusra.

    Args:
        event_type: Az esemény típusa, amire feliratkozunk
        callback: A callback függvény, amely az eseményt fogadja

    Note:
        A callback-nek aszinkronnak kell lennie (async def)
    """
```

**Példa:**

```python
async def handle_market_data(event):
    print(f"Piaci adat érkezett: {event.symbol} - {event.bid}")

event_bus.subscribe("market_data", handle_market_data)
```

##### `unsubscribe()`

Leiratkozás eseménytípusról.

```python
def unsubscribe(self, event_type: str, callback: EventCallback) -> None:
    """Leiratkozás eseménytípusról.

    Args:
        event_type: Az esemény típusa
        callback: A callback függvény, amelyet eltávolítunk
    """
```

**Példa:**

```python
event_bus.unsubscribe("market_data", handle_market_data)
```

##### `run_forever()`

Eseménybusz örök futás (blokkoló).

```python
async def run_forever(self) -> None:
    """Eseménybusz örök futás (blokkoló).

    Ez a metódus egy végtelen ciklusban fogadja az eseményeket
    és továbbítja azokat a feliratkozóknak.

    Note:
        Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd
    """
```

**Példa:**

```python
import asyncio

async def main():
    event_bus = EventBus()
    await event_bus.start()
    
    # Futtatás háttérben
    task = asyncio.create_task(event_bus.run_forever())
    
    # Egyéb műveletek...
    
    await task

asyncio.run(main())
```

## Komplex példa

```python
import asyncio
from datetime import datetime, UTC
from neural_ai.core.events.implementations.zeromq_bus import EventBus, EventBusConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent, TradeEvent

async def market_data_handler(event):
    """Feldolgozza a piaci adat eseményeket."""
    print(f"Piaci adat: {event.symbol} - Bid: {event.bid}, Ask: {event.ask}")

async def trade_handler(event):
    """Feldolgozza a kereskedési eseményeket."""
    print(f"Kereskedés: {event.symbol} - {event.direction} - Ár: {event.price}")

async def main():
    # EventBus létrehozása
    config = EventBusConfig(pub_port=6666)
    event_bus = EventBus(config)
    
    # Indítás
    await event_bus.start()
    
    # Feliratkozás
    event_bus.subscribe("market_data", market_data_handler)
    event_bus.subscribe("trade", trade_handler)
    
    # Események közzététele
    market_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        bid=1.0850,
        ask=1.0852,
        source="mt5"
    )
    
    trade_event = TradeEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        direction="BUY",
        price=1.0851,
        volume=0.01,
        order_id="ORD-12345"
    )
    
    await event_bus.publish("market_data", market_event)
    await event_bus.publish("trade", trade_event)
    
    # Várakozás a feldolgozásra
    await asyncio.sleep(1)
    
    # Leállítás
    await event_bus.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Context Manager használat

```python
async def main():
    async with EventBus() as event_bus:
        # EventBus itt aktív
        await event_bus.publish("topic", event)
        await asyncio.sleep(1)
    # EventBus automatikusan leáll
```

## Támogatott eseménytípusok

- `market_data`: Piaci adat események
- `trade`: Kereskedési események
- `signal`: Jelzés események
- `system_log`: Rendszer log események
- `order`: Rendelés események
- `position`: Pozíció események

## Teljesítmény és skálázhatóság

- **Aszinkron működés:** Az asyncio használata lehetővé teszi a nagy teljesítményt
- **ZeroMQ PUB/SUB:** Hatékony üzenetküldés több előfizetőnek
- **JSON szerializálás:** Könnyű és gyors adatátvitel
- **Inproc transport:** Gyors teszteléshez

## További információk

- [Events Modul Áttekintés](../__init__.md)
- [EventBus Factory](../factory.md)
- [Esemény Modellek](../interfaces/event_models.md)