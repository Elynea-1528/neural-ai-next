# EventBus Interface

## Áttekintés

Az EventBus Interface az eseményvezérelt architektúra magját definiálja. Egy egységes interfészt biztosít az események közzétételére és feliratkozására, lehetővé téve a komponensek közötti laza csatolást.

## Interfész

```python
class EventBusInterface(ABC)
```

## Konfiguráció

### `EventBusConfig`

Az EventBus konfigurációját leíró adat osztály.

**Attribútumok:**
- `zmq_context` (Optional[Any]): Külső ZeroMQ kontextus (opcionális)
- `pub_port` (int): Publisher port (alapértelmezett: 5555)
- `sub_port` (int): Subscriber port (alapértelmezett: 5556)
- `use_inproc` (bool): Inproc transport használata teszteléshez (alapértelmezett: False)

**Példa:**
```python
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig

# Alapértelmezett konfiguráció
config = EventBusConfig()

# Egyéni konfiguráció
config = EventBusConfig(
    pub_port=6666,
    sub_port=6667,
    use_inproc=True
)
```

## Metódusok

### `@property config() -> EventBusConfig`

Visszaadja az EventBus konfigurációját.

### `async start() -> None`

Elindítja az EventBus-t és létrehozza a szükséges socketeket.

**Kivételek:**
- `EventBusError`: Ha az EventBus már fut

### `async stop() -> None`

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

### `async publish(event_type: str, event: BaseModel) -> None`

Esemény közzététele a buszon.

**Paraméterek:**
- `event_type` (str): Az esemény típusa (pl. 'market_data', 'trade')
- `event` (BaseModel): Az esemény objektum (Pydantic modell)

**Kivételek:**
- `EventBusError`: Ha az EventBus nincs elindítva
- `PublishError`: Ha a publisher socket nincs inicializálva

**Példa:**
```python
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from datetime import datetime, timezone

event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0852,
    source="jforex"
)

await bus.publish("market_data", event)
```

### `subscribe(event_type: str, callback: EventCallback) -> None`

Feliratkozás eseménytípusra.

**Paraméterek:**
- `event_type` (str): Az esemény típusa
- `callback` (EventCallback): A callback függvény, amely az eseményt fogadja

**Megjegyzés:** A callback-nek aszinkronnak kell lennie (async def)

**Példa:**
```python
async def handle_market_data(event: MarketDataEvent) -> None:
    print(f"Received market data: {event.symbol} {event.bid}")

bus.subscribe("market_data", handle_market_data)
```

### `unsubscribe(event_type: str, callback: EventCallback) -> None`

Leiratkozás eseménytípusról.

**Paraméterek:**
- `event_type` (str): Az esemény típusa
- `callback` (EventCallback): A callback függvény, amelyet eltávolítunk

### `async run_forever() -> None`

Eseménybusz örök futás (blokkoló metódus). Végtelen ciklusban fogadja az eseményeket és továbbítja azokat a feliratkozóknak.

**Megjegyzés:** Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd.

## Tesztelés

Az interfész teljes tesztlefedettséggel rendelkezik. A tesztek a következőket ellenőrzik:
- Konfiguráció alapértelmezett és egyéni értékei
- Konfiguráció megváltoztathatatlansága
- Interfész absztrakt metódusainak jelenléte
- Metódusok aláírásainak helyessége

**Tesztfájl:** [`tests/core/events/interfaces/test_event_bus_interface.py`](../../../../tests/core/events/interfaces/test_event_bus_interface.py)

**Coverage:** 79%

## Kapcsolódó dokumentáció

- [EventBus Factory](../factory.md)
- [ZeroMQ EventBus Implementáció](../implementations/zeromq_bus.md)
- [Event Modellek](event_models.md)
- [Event Kivételek](../exceptions/event_error.md)