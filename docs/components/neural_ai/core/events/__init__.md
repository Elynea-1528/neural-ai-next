# Events Modul - Eseményvezérelt Architektúra

## Áttekintés

Az Events modul biztosítja az eseményvezérelt architektúra magját a Neural AI Next rendszerhez, lehetővé téve a komponensek közötti laza csatolást.

## Komponensek

### Factory
- **[`EventBusFactory`](factory.md)**: EventBus példányosításáért felelős gyár osztály

### Esemény Típusok
- **[`EventType`](interfaces/event_models.md#eventtype)**: Eseménytípusok enumerációja

### Esemény Modellek
Az alábbi Pydantic BaseModel alapú esemény osztályok használhatók:

- **[`MarketDataEvent`](interfaces/event_models.md#marketdataevent)**: Piaci adat esemény
- **[`TradeEvent`](interfaces/event_models.md#tradeevent)**: Kereskedési esemény
- **[`SignalEvent`](interfaces/event_models.md#signalevent)**: Jelzés esemény
- **[`SystemLogEvent`](interfaces/event_models.md#systemlogevent)**: Rendszer log esemény
- **[`OrderEvent`](interfaces/event_models.md#orderevent)**: Rendelés esemény
- **[`PositionEvent`](interfaces/event_models.md#positionevent)**: Pozíció esemény

## Használat

```python
from neural_ai.core.events import EventBusFactory, MarketDataEvent, EventType

# EventBus létrehozása
event_bus = await EventBusFactory.create_and_start()

# Esemény közzététele
event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(),
    bid=1.0850,
    ask=1.0852,
    source="mt5"
)
await event_bus.publish(EventType.MARKET_DATA.value, event)
```

## Modul szerkezete

```
neural_ai/core/events/
├── interfaces/          # Esemény modellek és interfészek
│   └── event_models.py  # Pydantic esemény modellek
├── implementations/     # EventBus implementációk
│   └── zeromq_bus.py    # ZeroMQ alapú EventBus
├── exceptions/          # Kivételek
│   └── event_error.py   # EventBus specifikus kivételek
└── factory.py           # EventBus factory
```

## További információk

- [EventBus Factory](factory.md)
- [Esemény Modellek](interfaces/event_models.md)
- [ZeroMQ Implementáció](implementations/zeromq_bus.md)
- [Kivételek](exceptions/event_error.md)