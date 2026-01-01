# ZeroMQ EventBus Implementáció

## Áttekintés

Ez a dokumentum a [`zeromq_bus.py`](../../../../neural_ai/core/events/implementations/zeromq_bus.py) fájl működését és architektúráját írja le. Az EventBus a rendszer eseményvezérelt architektúrájának magja, amely ZeroMQ PUB/SUB mintázatot használ a komponensek közötti kommunikációhoz.

## Architektúra

### Osztály: `EventBus`

Az EventBus egy singleton osztály, amely az [`EventBusInterface`](../../interfaces/event_bus_interface.md)-t implementálja. Aszinkron működést biztosít asyncio és ZeroMQ kombinációjával.

#### Attribútumok

- `_config: EventBusConfig` - Az EventBus konfigurációja
- `_context: zmq.asyncio.Context` - ZeroMQ kontextus
- `_publisher: zmq.Socket | None` - Publisher socket
- `_subscribers: dict[str, list[EventCallback]]` - Feliratkozók szótára
- `_running: bool` - Futási állapot jelzője
- `_logger: structlog.BoundLogger` - Logger példány

#### Metódusok

##### `__init__(config: EventBusConfig | None = None)`

Inicializálja az EventBus-t. Létrehozza a ZeroMQ kontextust és inicializálja a socketeket.

**Paraméterek:**
- `config`: EventBus konfiguráció (opcionális, alapértelmezett: `EventBusConfig()`)

**Kivételek:**
- `ImportError`: Ha a ZeroMQ nincs telepítve

##### `async start() -> None`

Elindítja az EventBus-t és létrehozza a socketeket. Beállítja a végtelen buffer méreteket a teljesítmény érdekében:

```python
self._publisher.setsockopt(self._zmq.SNDHWM, 0)  # Végtelen küldési buffer
self._publisher.setsockopt(self._zmq.RCVHWM, 0)  # Végtelen fogadási buffer
```

**Fontos:** A buffer méretek beállítása a socket létrehozása után, de a bind előtt történik.

##### `async stop() -> None`

Leállítja az EventBus-t és felszabadítja az erőforrásokat. Bezárja a publisher socketet és a kontextust.

##### `async publish(event_type: str, event: Union[BaseModel, list[BaseModel]]) -> None`

Esemény közzététele a buszon. Támogatja az egyedi eseményeket és batch (lista) eseményeket is.

**Paraméterek:**
- `event_type`: Az esemény típusa (pl. 'market_data', 'trade')
- `event`: Az esemény objektum (Pydantic BaseModel) vagy események listája

**Kivételek:**
- `EventBusError`: Ha az EventBus nincs elindítva
- `PublishError`: Ha a publisher socket nincs inicializálva

##### `subscribe(event_type: str, callback: EventCallback) -> None`

Feliratkozás eseménytípusra.

**Paraméterek:**
- `event_type`: Az esemény típusa, amire feliratkozunk
- `callback`: A callback függvény, amely az eseményt fogadja

**Megjegyzés:** A callback-nek aszinkronnak kell lennie (async def)

##### `unsubscribe(event_type: str, callback: EventCallback) -> None`

Leiratkozás eseménytípusról.

**Paraméterek:**
- `event_type`: Az esemény típusa
- `callback`: A callback függvény, amelyet eltávolítunk

##### `async run_forever() -> None`

Eseménybusz örök futás (blokkoló). Ez a metódus egy végtelen ciklusban fogadja az eseményeket és továbbítja azokat a feliratkozóknak.

**Megjegyzés:** Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd.

##### `async _dispatch_event(event_type: str, event_data: dict[str, Any]) -> None`

Esemény továbbítása a feliratkozóknak (belső metódus).

##### `_deserialize_event(event_type: str, event_data: dict[str, Any]) -> Optional[BaseModel]`

Deserializálja az eseményt a megfelelő Pydantic modellbe (belső metódus).

## Konfiguráció

Az EventBus konfigurációja az [`EventBusConfig`](../../interfaces/event_bus_interface.md) osztályon keresztül történik, amely a következő paramétereket támogatja:

- `pub_port: int` - Publisher port (alapértelmezett: 5555)
- `use_inproc: bool` - Inproc transport használata teszteléshez (alapértelmezett: False)
- `zmq_context: Optional[zmq.Context]` - Külső ZeroMQ kontextus (opcionális)

## Használati példa

```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent

# Konfiguráció létrehozása
config = EventBusConfig(pub_port=5555, use_inproc=False)

# EventBus példányosítása
event_bus = EventBusFactory.get_event_bus(config)

# Indítás
await event_bus.start()

# Esemény közzététele
event = MarketDataEvent(symbol="EURUSD", price=1.1234, volume=1000)
await event_bus.publish("market_data", event)

# Feliratkozás
async def handle_market_data(event: MarketDataEvent) -> None:
    print(f"Received market data: {event}")

event_bus.subscribe("market_data", handle_market_data)

# Leállítás
await event_bus.stop()
```

## Teljesítményoptimalizálás

### Végtelen Buffer Méretek

A refaktorálás során bevezettük a végtelen buffer méreteket a publisher socketen:

- **SNDHWM (Send High Water Mark) = 0**: Végtelen küldési buffer, ami garantálja, hogy a gyors producer nem blokkol a lassú consumer miatt
- **RCVHWM (Receive High Water Mark) = 0**: Végtelen fogadási buffer (bár a publisher nem fogad, de biztonsági okokból beállítjuk)

Ez a konfiguráció különösen fontos a nagy frekvenciájú tick adatok esetén, ahol a rendszernek képesnek kell lennie nagy mennyiségű adatot feldolgozni anélkül, hogy elveszítené azokat.

## Típusbiztonság

A kód szigorú típusellenőrzést alkalmaz:

- `TYPE_CHECKING` blokk a körkörös importok elkerülésére
- `Union[BaseModel, list[BaseModel]]` a batch és egyedi események támogatásához
- `Optional` típus a nullable értékekhez
- `Any` típus kerülése ahol lehetséges

## Hibakezelés

Az EventBus robusztus hibakezelést implementál:

- Minden metódus tartalmaz `try-except` blokkokat
- A hibák részletesen logolásra kerülnek structlog-gal
- A kritikus hibák kivételt dobnak, a nem kritikusak logolás után nem befolyásolják a rendszer működését

## Függőségek

- `pyzmq` - ZeroMQ Python binding
- `pydantic` - Adatvalidáció és serializáció
- `structlog` - Logolás
- `asyncio` - Aszinkron működés

## Kapcsolódó dokumentáció

- [EventBus Interface](../../interfaces/event_bus_interface.md)
- [Event Models](../../interfaces/event_models.md)
- [EventBus Factory](../factory.md)
- [EventBus Exceptions](../exceptions/index.md)
