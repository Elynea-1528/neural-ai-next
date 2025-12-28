# Event Kivételek

## Áttekintés

Az Event kivételek az EventBus rendszer hibakezelését biztosítják. Minden kivétel a `BaseException` osztályból származik, és specifikus hibákat jelöl a rendszer különböző részeiben.

## Kivétel hierarchia

```
BaseException
├── EventBusError
│   └── PublishError
└── SubscribeError
```

## Kivételek

### `EventBusError`

Az EventBus általános hibáit jelző kivétel osztály.

**Osztály:**
```python
class EventBusError(Exception)
```

**Konstruktor:**
```python
def __init__(self, message: str = "EventBus hiba történt") -> None
```

**Használat:**
```python
from neural_ai.core.events.exceptions.event_error import EventBusError

# Kivétel dobása
if not self._running:
    raise EventBusError("EventBus nincs elindítva")

# Kivétel elkapása
try:
    await bus.publish("market_data", event)
except EventBusError as e:
    print(f"Hiba: {e}")
```

**Gyakori okok:**
- EventBus nincs elindítva
- EventBus már fut
- Érvénytelen művelet

### `PublishError`

A közzétételi hibákat jelző kivétel osztály.

**Osztály:**
```python
class PublishError(EventBusError)
```

**Konstruktor:**
```python
def __init__(self, message: str = "Hiba történt az esemény közzétételekor") -> None
```

**Használat:**
```python
from neural_ai.core.events.exceptions.event_error import PublishError

# Kivétel dobása
if self._publisher is None:
    raise PublishError("Publisher socket nincs inicializálva")

# Kivétel elkapása
try:
    await bus.publish("market_data", event)
except PublishError as e:
    print(f"Közzétételi hiba: {e}")
```

**Gyakori okok:**
- Publisher socket nincs inicializálva
- Hálózati hiba
- Érvénytelen esemény adatok

### `SubscribeError`

A feliratkozási hibákat jelző kivétel osztály.

**Osztály:**
```python
class SubscribeError(EventBusError)
```

**Konstruktor:**
```python
def __init__(self, message: str = "Hiba történt a feliratkozás során") -> None
```

**Használat:**
```python
from neural_ai.core.events.exceptions.event_error import SubscribeError

# Kivétel dobása
if event_type not in self._subscribers:
    raise SubscribeError(f"Ismeretlen eseménytípus: {event_type}")

# Kivétel elkapása
try:
    bus.subscribe("unknown_event", callback)
except SubscribeError as e:
    print(f"Feliratkozási hiba: {e}")
```

**Gyakori okok:**
- Ismeretlen eseménytípus
- Érvénytelen callback függvény
- Duplikált feliratkozás

## Hibakezelés minták

### Alapvető hibakezelés

```python
from neural_ai.core.events.exceptions.event_error import (
    EventBusError,
    PublishError,
    SubscribeError
)

try:
    bus = await EventBusFactory.create_and_start()
    bus.subscribe("market_data", callback)
    await bus.publish("market_data", event)
except EventBusError as e:
    print(f"EventBus hiba: {e}")
except PublishError as e:
    print(f"Közzétételi hiba: {e}")
except SubscribeError as e:
    print(f"Feliratkozási hiba: {e}")
```

### Reszponzív hibakezelés

```python
async def publish_with_retry(bus, event_type, event, max_retries=3):
    """Közzététel újrapróbálkozással."""
    for attempt in range(max_retries):
        try:
            await bus.publish(event_type, event)
            return
        except PublishError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Próbálkozás {attempt + 1}/{max_retries}: {e}")
            await asyncio.sleep(1)
```

### Callback hibakezelés

```python
async def safe_callback(event):
    """Biztonságos callback hibakezeléssel."""
    try:
        # Callback logika
        await process_event(event)
    except Exception as e:
        logger.error(f"Callback hiba: {e}")
        # Nem dobjuk tovább a hibát, hogy ne befolyásolja a többi callback-et

bus.subscribe("market_data", safe_callback)
```

## Tesztelés

A kivétel osztályok részben tesztelve vannak. A tesztek a következőket ellenőrzik:
- Kivétel létrehozása alapértelmezett üzenettel
- Kivétel létrehozása egyéni üzenettel
- Kivétel hierarchia helyessége

**Tesztfájl:** A kivételek tesztelése a [`test_zeromq_bus.py`](../../../../tests/core/events/implementations/test_zeromq_bus.py) fájlban történik.

**Coverage:** 85%

## Best Practices

1. **Specifikus kivételek használata:** Mindig a legspecifikusabb kivételt kapd el
2. **Informativ hibaüzenetek:** A hibaüzenetek legyenek egyértelműek és informatívak
3. **Hiba naplózása:** Minden hibát naplózz a rendszer logjába
4. **Reszponzív kezelés:** Ne hagyd, hogy egy hiba az egész rendszert leállítsa
5. **Callback hibák elkülönítése:** A callback hibák ne befolyásolják a többi feliratkozót

## Kapcsolódó dokumentáció

- [EventBus Interface](../interfaces/event_bus_interface.md)
- [EventBus Factory](../factory.md)
- [ZeroMQ EventBus Implementáció](../implementations/zeromq_bus.md)