# core/events/exceptions/event_error.py

EventBus-specifikus kivételek.

Ez a modul tartalmazza az összes EventBus-műveletekhez kapcsolódó kivételeket.

## Osztályok

### `EventBusError`

Általános EventBus hiba.

### `PublishError`

Esemény közzététel hiba.

### `SubscriberError`

Feliratkozási hiba.


## Függvények

### `__init__`

Inicializálja a SubscriberError kivételt.

        Args:
            message: A hibaüzenet.
            subscriber_id: A feliratkozó azonosítója, ahol a hiba történt.


---

**Forrásfájl:** [`core/events/exceptions/event_error.py`](../../../neural_ai/core/events/exceptions/event_error.py)
