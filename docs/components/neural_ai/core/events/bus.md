# EventBus Implementáció

## Áttekintés

Az EventBus a Neural AI Next rendszer eseményvezérelt architektúrájának magja. ZeroMQ PUB/SUB mintázatot használ aszinkron kommunikációra a rendszer különböző komponensei között.

## Architektúra

### PUB/SUB Mintázat

Az EventBus ZeroMQ PUB/SUB socketeket használ:
- **Publisher**: Eseményeket küld a buszra
- **Subscriber**: Eseményeket fogad a buszról
- **Topic-based filtering**: Minden eseménynek van típusa, amire fel lehet iratkozni

### Transport Layer

- **TCP**: Éles környezetben (alapértelmezett port: 5555)
- **Inproc**: Teszteléshez, memóriabeli kommunikáció

## EventBusConfig

Az EventBus konfigurációját az `EventBusConfig` osztály tárolja:

```python
@dataclass
class EventBusConfig:
    zmq_context: Optional['zmq.asyncio.Context'] = None
    pub_port: int = 5555
    sub_port: int = 5556
    use_inproc: bool = False
```

**Paraméterek:**
- `zmq_context`: ZeroMQ kontextus (opcionális)
- `pub_port`: Publisher port (alapértelmezett: 5555)
- `sub_port`: Subscriber port (alapértelmezett: 5556)
- `use_inproc`: Használjon inproc transportot teszteléshez

## EventBus Osztály

### Inicializálás

```python
from neural_ai.core.events.bus import EventBus, EventBusConfig

# Alapértelmezett konfiguráció
bus = EventBus()

# Egyéni konfiguráció
config = EventBusConfig(
    pub_port=6666,
    use_inproc=True
)
bus = EventBus(config=config)
```

### Metódusok

#### start()

Elindítja az EventBus-t és létrehozza a socketeket.

```python
await bus.start()
```

**Működés:**
- Létrehozza a ZeroMQ kontextust (ha nincs megadva)
- Bind-olja a publisher socketet a megadott portra
- Beállítja a futási állapotot `True`-ra

#### stop()

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

```python
await bus.stop()
```

**Működés:**
- Bezárja a publisher socketet
- Terminálja a ZeroMQ kontextust (ha saját)
- Beállítja a futási állapotot `False`-ra

#### publish()

Eseményt tesz közzé a buszon.

```python
await bus.publish(event_type: str, event: BaseModel)
```

**Paraméterek:**
- `event_type`: Az esemény típusa (pl. 'market_data', 'signal')
- `event`: Az esemény objektum (Pydantic BaseModel)

**Működés:**
1. Szerializálja az eseményt JSON formátumba
2. Hozzáadja a meta adatokat (`_event_type`, `_timestamp`)
3. Elküldi a ZeroMQ publisher socketen keresztül

**Példa:**
```python
from neural_ai.core.events.events import MarketDataEvent
from datetime import datetime, timezone

event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0851,
    source="mt5"
)

await bus.publish("market_data", event)
```

#### subscribe()

Feliratkozás egy eseménytípusra.

```python
bus.subscribe(event_type: str, callback: Callable[[BaseModel], Any])
```

**Paraméterek:**
- `event_type`: Az esemény típusa
- `callback`: A callback függvény (aszinkron kell legyen)

**Példa:**
```python
async def handle_market_data(event: MarketDataEvent):
    print(f"Új piaci adat: {event.symbol} - {event.bid}")

bus.subscribe("market_data", handle_market_data)
```

#### unsubscribe()

Leiratkozás egy eseménytípusról.

```python
bus.unsubscribe(event_type: str, callback: Callable[[BaseModel], Any])
```

**Példa:**
```python
bus.unsubscribe("market_data", handle_market_data)
```

#### run_forever()

Események fogadása és továbbítása (blokkoló metódus).

```python
await bus.run_forever()
```

**Működés:**
- Létrehozza a subscriber socketet
- Feliratkozik az összes témakörre
- Végtelen ciklusban fogadja az eseményeket
- Továbbítja azokat a feliratkozóknak

**Note:** Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd.

### Aszinkron Context Manager

Az EventBus támogatja az aszinkron context manager-t:

```python
async with EventBus(config=config) as bus:
    # EventBus itt fut
    await bus.publish("market_data", event)
# EventBus automatikusan leáll
```

## Használati Példák

### Egyszerű Publisher

```python
import asyncio
from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent
from datetime import datetime, timezone

async def main():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    
    # Esemény létrehozása
    event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=1.0850,
        ask=1.0851,
        source="mt5"
    )
    
    # Közzététel
    await bus.publish("market_data", event)
    
    await bus.stop()

asyncio.run(main())
```

### Publisher és Subscriber

```python
import asyncio
from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent
from datetime import datetime, timezone

# Subscriber callback
async def handle_market_data(event: MarketDataEvent):
    print(f"Fogadott esemény: {event.symbol}")
    print(f"Bid: {event.bid}, Ask: {event.ask}")

async def main():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    
    # Feliratkozás
    bus.subscribe("market_data", handle_market_data)
    
    # Esemény közzététele
    event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=1.0850,
        ask=1.0851,
        source="mt5"
    )
    
    await bus.publish("market_data", event)
    
    # Kis várakozás, hogy a callback lefusson
    await asyncio.sleep(0.1)
    
    await bus.stop()

asyncio.run(main())
```

### Több Subscriber

```python
import asyncio
from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent
from datetime import datetime, timezone

# Különböző subscriber callbacks
async def logger_callback(event: MarketDataEvent):
    print(f"[LOG] Piaci adat: {event.symbol}")

async def strategy_callback(event: MarketDataEvent):
    print(f"[STRATEGY] Jelzés generálása: {event.symbol}")

async def database_callback(event: MarketDataEvent):
    print(f"[DB] Adat mentése: {event.symbol}")

async def main():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    
    # Több feliratkozó ugyanarra az eseményre
    bus.subscribe("market_data", logger_callback)
    bus.subscribe("market_data", strategy_callback)
    bus.subscribe("market_data", database_callback)
    
    # Esemény közzététele
    event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=1.0850,
        ask=1.0851,
        source="mt5"
    )
    
    await bus.publish("market_data", event)
    
    # Kis várakozás
    await asyncio.sleep(0.1)
    
    await bus.stop()

asyncio.run(main())
```

### Különböző Eseménytípusok

```python
import asyncio
from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent, SignalEvent
from datetime import datetime, timezone

# Különböző eseménytípusokra feliratkozó callbacks
async def market_data_handler(event: MarketDataEvent):
    print(f"Piaci adat: {event.symbol}")

async def signal_handler(event: SignalEvent):
    print(f"Jelzés: {event.signal_type} - {event.symbol}")

async def main():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    
    # Feliratkozás különböző eseménytípusokra
    bus.subscribe("market_data", market_data_handler)
    bus.subscribe("signal", signal_handler)
    
    # MarketDataEvent közzététele
    market_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=1.0850,
        ask=1.0851,
        source="mt5"
    )
    await bus.publish("market_data", market_event)
    
    # SignalEvent közzététele
    signal_event = SignalEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        signal_type="ENTRY_LONG",
        confidence=0.85,
        strategy_id="neural_model_v1"
    )
    await bus.publish("signal", signal_event)
    
    # Kis várakozás
    await asyncio.sleep(0.1)
    
    await bus.stop()

asyncio.run(main())
```

## Hibakezelés

### Esemény Deszerializálási Hiba

Ha egy eseményt nem sikerül deszerializálni, a rendszer naplózza a hibát és kihagyja az eseményt:

```python
# A hiba automatikusan kezelődik és naplózásra kerül
await bus.publish("unknown_type", invalid_event)
```

### Callback Hiba

Ha egy callback hibát okoz, a rendszer naplózza a hibát és folytatja a többi callback feldolgozását:

```python
async def problematic_callback(event):
    raise ValueError("Hiba a feldolgozásban")

# A hiba naplózásra kerül, de a többi callback lefut
bus.subscribe("market_data", problematic_callback)
```

## Teljesítmény és Skálázhatóság

### ZeroMQ Előnyök

- **Gyorsaság**: ZeroMQ nagy teljesítményű üzenetküldést biztosít
- **Megbízhatóság**: Automatikus újracsatlakozás és hibahelyreállítás
- **Skálázhatóság**: Több publisher és subscriber támogatása
- **Aszinkron**: Teljes aszinkron működés asyncio-val

### Best Practices

1. **Használj context manager-t** az erőforrások automatikus felszabadításához
2. **Mindig kezeld a kivételeket** a callback-ekben
3. **Használj inproc transportot** egységtesztekhez
4. **Ne blokkolj** a callback-ekben hosszú műveletekkel
5. **Unsubscribe-olj** ha már nincs szükség a feliratkozásra

## Tesztelés

### Egységtesztek

```python
import pytest
from neural_ai.core.events.bus import EventBus, EventBusConfig

@pytest.mark.asyncio
async def test_event_bus_start_stop():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    assert bus._running is True
    
    await bus.stop()
    assert bus._running is False
```

### Integrációs Tesztek

```python
import pytest
from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_publish_and_subscribe():
    config = EventBusConfig(use_inproc=True)
    bus = EventBus(config=config)
    
    await bus.start()
    
    received_events = []
    
    async def callback(event):
        received_events.append(event)
    
    bus.subscribe("market_data", callback)
    
    event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=1.0850,
        ask=1.0851,
        source="mt5"
    )
    
    await bus.publish("market_data", event)
    await asyncio.sleep(0.1)
    
    await bus.stop()
```

## Kapcsolódó Dokumentáció

- [Esemény Modellek](events.md)
- [System Architecture Spec](../planning/specs/01_system_architecture.md)
- [ZeroMQ dokumentáció](https://zeromq.org/)
- [Asyncio dokumentáció](https://docs.python.org/3/library/asyncio.html)

## Verzió Történet

- **v1.1.0** (2025-12-23): Refaktorálás és fejlesztés
  - Típusos visszatérési értékek (nincs `Any`)
  - Teljes típusannotáció a Pylance Strict mode-hoz
  - Deprecated `datetime.utcnow()` cseréje `datetime.now(timezone.utc)`-ra
  - EventCallback típus alias a jobb olvashatóságért
  - Enhanced context manager típusannotációkkal
  - Improved hibakezelés és naplózás

- **v1.0.0** (2025-12-23): Kezdeti implementáció
  - ZeroMQ PUB/SUB alapú EventBus
  - Teljes aszinkron működés
  - JSON szerializálás/deszerializálás
  - Több feliratkozó támogatása
  - Hibakezelés és naplózás