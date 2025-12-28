# EventBus Rendszer

## Áttekintés

Az EventBus rendszer a Neural AI Next projekt eseményvezérelt architektúrájának magja. Lehetővé teszi a komponensek közötti laza csatolást és aszinkron kommunikációt a ZeroMQ PUB/SUB mintázatán alapuló hatékony implementációval.

## Főbb jellemzők

- **Aszinkron működés:** Minden művelet nem blokkoló, asyncio alapú
- **Típusbiztos események:** Pydantic modellekkel validált események
- **Hatékony továbbítás:** ZeroMQ PUB/SUB mintázat
- **Singleton design:** Egységes EventBus példány az egész alkalmazásban
- **Konfigurálható:** Rugalmas konfigurációs lehetőségek
- **Tesztelhető:** Teljes mock-olhatóság ZMQ komponensek esetén

## Komponensek

### 1. [EventBus Factory](factory.md)

Az EventBus létrehozásáért felelős statikus osztály. Támogatja az alapértelmezett, egyéni és konfigurációs fájlból történő létrehozást.

**Kulcsmetódusok:**
- `create(config)`: EventBus létrehozása
- `create_and_start(config)`: Létrehozás és indítás egy lépésben
- `create_from_config(config_manager)`: Konfigurációból történő létrehozás

### 2. [EventBus Interface](interfaces/event_bus_interface.md)

Az eseménybusz interfésze, amely definiálja a kötelező metódusokat és a konfigurációt.

**Kulcsmetódusok:**
- `start()`: EventBus indítása
- `stop()`: EventBus leállítása
- `publish(event_type, event)`: Esemény közzététele
- `subscribe(event_type, callback)`: Feliratkozás eseményre
- `unsubscribe(event_type, callback)`: Leiratkozás eseményről

### 3. [Event Modellek](interfaces/event_models.md)

A rendszer által támogatott eseménytípusok Pydantic modellekben.

**Támogatott események:**
- `MarketDataEvent`: Piaci adatok
- `TradeEvent`: Kereskedési események
- `SignalEvent`: Jelzések
- `SystemLogEvent`: Rendszer naplók
- `OrderEvent`: Rendelések
- `PositionEvent`: Pozíciók

### 4. [ZeroMQ Implementáció](implementations/zeromq_bus.md)

Az EventBus Interface ZeroMQ alapú implementációja.

**Jellemzők:**
- TCP és inproc transport támogatás
- JSON szerializáció
- Aszinkron context manager
- Hatékony eseménytovábbítás

### 5. [Event Kivételek](exceptions/event_error.md)

A rendszer hibakezelését biztosító kivétel osztályok.

**Kivételek:**
- `EventBusError`: Általános EventBus hibák
- `PublishError`: Közzétételi hibák
- `SubscribeError`: Feliratkozási hibák

## Gyors útmutató

### Telepítés

```bash
pip install pyzmq
```

### Alapvető használat

```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from datetime import datetime, timezone

# EventBus létrehozása és indítása
bus = await EventBusFactory.create_and_start()

# Callback definiálása
async def handle_market_data(event: MarketDataEvent) -> None:
    print(f"Market data: {event.symbol} {event.bid}/{event.ask}")

# Feliratkozás
bus.subscribe("market_data", handle_market_data)

# Esemény közzététele
event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0852,
    source="jforex"
)

await bus.publish("market_data", event)
```

### Aszinkron Context Manager

```python
async with EventBus() as bus:
    # EventBus itt elindul
    await bus.publish("market_data", event)
    # EventBus itt automatikusan leáll
```

## Tesztelés

Az EventBus rendszer teljes tesztlefedettséggel rendelkezik:

- **Összes teszt:** 75 db
- **Átfutás arány:** 100%
- **Teljes coverage:** 88%

### Teszt struktúra

```
tests/core/events/
├── test_factory.py                          # Factory tesztjei
├── interfaces/
│   ├── test_event_bus_interface.py         # Interface tesztjei
│   └── test_event_models.py                # Modellek tesztjei
└── implementations/
    └── test_zeromq_bus.py                  # ZeroMQ implementáció tesztjei
```

### ZMQ Mocking

A tesztek során a ZeroMQ-t teljesen mock-oljuk:

```python
@patch("zmq.asyncio.Context")
def test_example(self, mock_context_class):
    mock_context = MagicMock()
    mock_socket = AsyncMock()
    mock_context.socket.return_value = mock_socket
    mock_context_class.return_value = mock_context
    
    # Teszt logika...
```

## Architektúra

### Komponens diagram

```
┌─────────────────┐
│  EventBus       │
│  Factory        │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  EventBus       │
│  Interface      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  ZeroMQ         │
│  EventBus       │
│  (Singleton)    │
└────────┬────────┘
         │
         v
┌─────────────────┐         ┌─────────────────┐
│  Publisher      │────────>│  Subscribers    │
│  (ZeroMQ PUB)   │         │  (Callbacks)    │
└─────────────────┘         └─────────────────┘
```

### Adatfolyam

1. **Esemény létrehozása:** Pydantic modellként
2. **Közzététel:** `publish()` metódus hívása
3. **Szerializáció:** JSON formátumba konvertálás
4. **Továbbítás:** ZeroMQ PUB/SUB keresztül
5. **Deszerializáció:** Pydantic modellbe visszaalakítás
6. **Callback hívás:** Feliratkozók értesítése

## Best Practices

1. **Mindig használj Factory-t:** Ne példányosítsd közvetlenül az EventBus-t
2. **Aszinkron callback-ek:** A callback függvények legyenek async
3. **Hibakezelés:** Mindig kezeld a kivételeket
4. **Context manager:** Használd az async context managert, ahol lehet
5. **Tesztelés:** Mock-old a ZeroMQ-t a tesztek során

## Teljesítmény

- **Átviteli sebesség:** Több ezer esemény/másodperc
- **Késleltetés:** Alacsony, milliszekundumos tartomány
- **Memória hatékonyság:** Hatékony szerializáció és deszerializáció
- **Skálázhatóság:** Több komponens egyszerre használhatja

## Korlátozások

- **Singleton:** Csak egy EventBus példány lehet
- **ZeroMQ függőség:** Szükséges a `pyzmq` csomag
- `run_forever()`: Blokkoló metódus, csak külön task-ként használható

## Jövőbeli fejlesztések

- [ ] Több EventBus példány támogatása
- [ ] Redis backend támogatás
- [ ] WebSocket interfész
- [ ] Esemény replay funkcionalitás
- [ ] Haladó filtering és routing

## Kapcsolódó dokumentáció

- [Architektúra áttekintés](../../architecture/hierarchical_system/overview.md)
- [Core komponensek](../main.md)
- [Config rendszer](../config/factory.md)
- [Logger rendszer](../logger/factory.md)