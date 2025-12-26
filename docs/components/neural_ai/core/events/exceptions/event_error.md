# EventBus Kivételek

## Áttekintés

Ez a modul tartalmazza az összes EventBus-műveletekhez kapcsolódó kivételeket.

## Kivétel osztályok

### `EventBusError`

Általános EventBus hiba.

```python
class EventBusError(NeuralAIException):
    """Általános EventBus hiba."""
    
    def __init__(self, message: str, details: str | None = None) -> None:
        """Inicializálja az EventBusError kivételt.

        Args:
            message: A hibaüzenet.
            details: Opcionális részletes leírás a hibáról.
        """
```

**Attribútumok:**
- `message`: A hibaüzenet
- `details`: Opcionális részletes leírás a hibáról

**Példa használat:**

```python
from neural_ai.core.events.exceptions import EventBusError

try:
    # EventBus művelet
    pass
except EventBusError as e:
    print(f"Hiba: {e.message}")
    if e.details:
        print(f"Részletek: {e.details}")
```

### `PublishError`

Esemény közzététel hibája.

```python
class PublishError(EventBusError):
    """Esemény közzététel hiba."""
    
    def __init__(self, message: str, event_type: str | None = None) -> None:
        """Inicializálja a PublishError kivételt.

        Args:
            message: A hibaüzenet.
            event_type: Az esemény típusa, amelynek közzététele sikertelen volt.
        """
```

**Attribútumok:**
- `message`: A hibaüzenet
- `event_type`: Az esemény típusa, amelynek közzététele sikertelen volt

**Példa használat:**

```python
from neural_ai.core.events.exceptions import PublishError

try:
    await event_bus.publish("market_data", event)
except PublishError as e:
    print(f"Közzétételi hiba: {e.message}")
    print(f"Esemény típusa: {e.event_type}")
```

### `SubscriberError`

Feliratkozási hiba.

```python
class SubscriberError(EventBusError):
    """Feliratkozási hiba."""
    
    def __init__(self, message: str, subscriber_id: str | None = None) -> None:
        """Inicializálja a SubscriberError kivételt.

        Args:
            message: A hibaüzenet.
            subscriber_id: A feliratkozó azonosítója, ahol a hiba történt.
        """
```

**Attribútumok:**
- `message`: A hibaüzenet
- `subscriber_id`: A feliratkozó azonosítója, ahol a hiba történt

**Példa használat:**

```python
from neural_ai.core.events.exceptions import SubscriberError

try:
    event_bus.subscribe("market_data", callback)
except SubscriberError as e:
    print(f"Feliratkozási hiba: {e.message}")
    print(f"Feliratkozó ID: {e.subscriber_id}")
```

## Kivétel kezelés

### Általános hibakezelés

```python
from neural_ai.core.events.exceptions import (
    EventBusError,
    PublishError,
    SubscriberError
)

try:
    # EventBus művelet
    await event_bus.publish("topic", event)
except PublishError as e:
    # Közzétételi hibák kezelése
    logger.error(f"Közzétételi hiba: {e}")
except SubscriberError as e:
    # Feliratkozási hibák kezelése
    logger.error(f"Feliratkozási hiba: {e}")
except EventBusError as e:
    # Általános EventBus hibák kezelése
    logger.error(f"EventBus hiba: {e}")
```

### Hibajelzés

```python
from neural_ai.core.events.exceptions import PublishError

async def publish_event(event_bus, event_type, event):
    """Esemény közzététele hibakezeléssel."""
    try:
        await event_bus.publish(event_type, event)
        return True
    except PublishError as e:
        logger.error(f"Közzétételi hiba: {e.message}")
        # További teendők a hibával
        return False
```

## Kivétel láncolás

A kivételek a `NeuralAIException` osztályból származnak, így részei a rendszer széles kivétel hierarchiájának:

```
NeuralAIException
└── EventBusError
    ├── PublishError
    └── SubscriberError
```

## További információk

- [Events Kivételek Áttekintés](__init__.md)
- [Events Modul](../__init__.md)
- [Base Kivételek](../../base/exceptions/base_error.md)