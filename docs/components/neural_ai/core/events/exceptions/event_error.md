# neural_ai/core/events/exceptions/event_error.py

EventBus-specifikus kivételek.

Ez a modul tartalmazza az összes EventBus-műveletekhez kapcsolódó kivételeket.

## Importok

```python
from neural_ai.core.base.exceptions import NeuralAIException
```

## Osztály: `EventBusError(NeuralAIException)`

Általános EventBus hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, details: str | None = None) -> None
```

Inicializálja az EventBusError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`details`** (`str | None`) = `None`: Opcionális részletes leírás a hibáról.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `PublishError(EventBusError)`

Esemény közzététel hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, event_type: str | None = None) -> None
```

Inicializálja a PublishError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`event_type`** (`str | None`) = `None`: Az esemény típusa, amelynek közzététele sikertelen volt.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `SubscriberError(EventBusError)`

Feliratkozási hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, subscriber_id: str | None = None) -> None
```

Inicializálja a SubscriberError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`subscriber_id`** (`str | None`) = `None`: A feliratkozó azonosítója, ahol a hiba történt.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/events/exceptions/event_error.py`](../../neural_ai/core/events/exceptions/event_error.py)
