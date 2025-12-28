# ZeroMQ EventBus Implementáció

## Áttekintés

A ZeroMQ EventBus az EventBus Interface aszinkron implementációja, amely a ZeroMQ PUB/SUB mintázatát használja az események hatékony továbbítására. A rendszer teljesítményre és skálázhatóságra lett optimalizálva.

## Osztály

```python
class EventBus(EventBusInterface, metaclass=SingletonMeta)
```

## Jellemzők

- **Aszinkron működés:** Minden művelet aszinkron, nem blokkolja a fő szálat
- **Singleton minta:** Az EventBus egyetlen példányban létezik az alkalmazásban
- **ZeroMQ PUB/SUB:** Hatékony eseménytovábbítás TCP vagy inproc transporttal
- **Pydantic modellek:** Típusbiztos események validációval
- **JSON szerializáció:** Platformfüggetlen adatcsere
- **Context Manager:** Aszinkron context manager támogatás

## Inicializálás

### Alapértelmezett inicializálás

```python
from neural_ai.core.events.factory import EventBusFactory

bus = EventBusFactory.create()
```

### Egyéni konfigurációval

```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig

config = EventBusConfig(
    pub_port=6666,
    sub_port=6667,
    use_inproc=True  # Teszteléshez
)

bus = EventBusFactory.create(config)
```

### Külső ZMQ kontextussal

```python
import zmq.asyncio

context = zmq.asyncio.Context()
config = EventBusConfig(zmq_context=context)

bus = EventBusFactory.create(config)
```

## Használat

### Esemény közzététele

```python
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from datetime import datetime, timezone

# EventBus létrehozása és indítása
bus = await EventBusFactory.create_and_start()

# Esemény létrehozása
event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0852,
    source="jforex"
)

# Esemény közzététele
await bus.publish("market_data", event)
```

### Feliratkozás eseményekre

```python
async def handle_market_data(event: MarketDataEvent) -> None:
    """Callback függvény a market data események kezelésére."""
    print(f"Market data received: {event.symbol}")
    print(f"Bid: {event.bid}, Ask: {event.ask}")

# Feliratkozás az eseményre
bus.subscribe("market_data", handle_market_data)
```

### Aszinkron Context Manager

```python
async with EventBus() as bus:
    # EventBus itt elindul
    event = MarketDataEvent(...)
    await bus.publish("market_data", event)
    # EventBus itt leáll
```

### Események fogadása végtelen ciklusban

```python
import asyncio

async def main():
    bus = await EventBusFactory.create_and_start()
    
    # Feliratkozás
    async def handle_event(event):
        print(f"Event received: {event}")
    
    bus.subscribe("market_data", handle_event)
    
    # Események fogadása
    await bus.run_forever()

asyncio.run(main())
```

## Architektúra

### Publisher/Subscriber minta

A ZeroMQ EventBus a PUB/SUB mintázatot követi:

1. **Publisher:** Az EventBus létrehozza a publisher sockettet, amely a megadott porton bind-ol
2. **Subscriber:** A `run_forever()` metódus létrehozza a subscriber sockettet, amely connect-ol a publisherhez
3. **Témakörök:** Minden eseménytípushoz tartozik egy témakör (topic)
4. **Üzenet formátum:** `[topic, json_data]` multipart üzenetek

### Adatfolyam

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Publisher  │────────>│  ZeroMQ Bus  │────────>│ Subscribers │
│  (Component)│         │  (PUB/SUB)   │         │ (Callbacks) │
└─────────────┘         └──────────────┘         └─────────────┘
```

### Szerializáció

Az események a következő lépéseken mennek át:

1. **Pydantic modell:** Az esemény Pydantic objektumként érkezik
2. **JSON konverzió:** `model_dump_json()` metódussal JSON formátumba konvertálódik
3. **Meta adatok:** Hozzáadódik az `_event_type` és `_timestamp` mező
4. **UTF-8 kódolás:** A JSON string UTF-8 byte array-é konvertálódik
5. **ZeroMQ küldés:** Multipart üzenetként továbbítódik

### Deszerializáció

A fogadó oldalon a fordított folyamat zajlik:

1. **ZeroMQ fogadás:** Multipart üzenet érkezik
2. **JSON dekódolás:** UTF-8 string-é konvertálódik
3. **Meta adatok eltávolítása:** Az `_` prefixű mezők eltávolítása
4. **Pydantic modell:** A megfelelő Pydantic osztályba deszerializálás
5. **Callback hívás:** Az esemény továbbítása a feliratkozóknak

## Hibakezelés

### EventBusError

Az EventBus általános hibáit jelzi.

**Okok:**
- EventBus nincs elindítva
- EventBus már fut

### PublishError

A közzétételi hibákat jelzi.

**Okok:**
- Publisher socket nincs inicializálva
- Hálózati hiba

### Callback hibák

Ha egy callback hibát dob, az nem befolyásolja a többi callback-et. A hiba csak logolásra kerül.

## Tesztelés

A ZeroMQ EventBus implementáció kiterjedt tesztelésen esett át, különös figyelemmel a ZMQ mocking-ra.

### Tesztelt területek

- **Inicializálás:** Alapértelmezett, egyéni konfiguráció, külső ZMQ kontextus
- **Indítás/Leállítás:** Sikeres indítás, többszöri indítás, leállítás, hibakezelés
- **Közzététel:** Sikeres közzététel, hibakezelés, nincs publisher
- **Feliratkozás:** Új eseménytípus, több callback, leiratkozás
- **Context Manager:** Aszinkron context manager működése
- **Deszerializáció:** Különböző eseménytípusok, hibás adatok
- **Továbbítás:** Sikeres továbbítás, nincs feliratkozó, callback hiba

### ZMQ Mocking

A tesztek során a ZeroMQ-t teljesen mock-oljuk, hogy ne nyissunk valódi socketeket:

```python
@patch("zmq.asyncio.Context")
def test_example(self, mock_context_class):
    mock_context = MagicMock()
    mock_socket = AsyncMock()
    mock_context.socket.return_value = mock_socket
    mock_context_class.return_value = mock_context
    
    # Teszt logika...
```

**Tesztfájl:** [`tests/core/events/implementations/test_zeromq_bus.py`](../../../../tests/core/events/implementations/test_zeromq_bus.py)

**Coverage:** 78%

## Teljesítmény

A ZeroMQ EventBus a következő teljesítménybeli előnyökkel rendelkezik:

- **Alacsony késleltetés:** ZeroMQ optimalizált üzenetküldést biztosít
- **Magas átviteli sebesség:** Több ezer esemény/másodperc
- **Aszinkron működés:** Nem blokkolja a fő szálat
- **Hatékony szerializáció:** JSON formátum gyors feldolgozással

## Korlátozások

- **Singleton minta:** Csak egy EventBus példány lehet az alkalmazásban
- `run_forever()` blokkoló: Végtelen ciklusban fut, csak külön task-ként használható
- **ZeroMQ függőség:** Szükséges a `pyzmq` csomag telepítése

## Kapcsolódó dokumentáció

- [EventBus Interface](../interfaces/event_bus_interface.md)
- [EventBus Factory](../factory.md)
- [Event Modellek](../interfaces/event_models.md)
- [Event Kivételek](../exceptions/event_error.md)