# Events Kivételek - Áttekintés

## Áttekintés

Ez a csomag tartalmazza az EventBus-hoz kapcsolódó kivételeket.

## Elérhető kivételek

### [`EventBusError`](event_error.md#eventbuserror)
Általános EventBus hiba.

### [`PublishError`](event_error.md#publisherror)
Esemény közzététel hibája.

### [`SubscriberError`](event_error.md#subscriberror)
Feliratkozási hiba.

## Használat

```python
from neural_ai.core.events.exceptions import (
    EventBusError,
    PublishError,
    SubscriberError
)

try:
    await event_bus.publish("topic", event)
except PublishError as e:
    print(f"Közzétételi hiba: {e}")
    print(f"Esemény típusa: {e.event_type}")
```

## Kivétel hierarchia

```
NeuralAIException
└── EventBusError
    ├── PublishError
    └── SubscriberError
```

## További információk

- [Részletes kivétel dokumentáció](event_error.md)
- [Events modul áttekintés](../__init__.md)