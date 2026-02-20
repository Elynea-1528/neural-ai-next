# tests/neural_ai/core/events/exceptions/test_event_error.py

EventBus kivételek tesztek.

## Importok

```python
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.events.exceptions.event_error import EventBusError
from neural_ai.core.events.exceptions.event_error import PublishError
from neural_ai.core.events.exceptions.event_error import SubscriberError
```

## Osztály: `TestEventBusError`

EventBusError osztály tesztei.

### Metódusok

#### `test_event_bus_error_creation()`

```python
def test_event_bus_error_creation(self) -> None
```

EventBusError létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_event_bus_error_with_details()`

```python
def test_event_bus_error_with_details(self) -> None
```

EventBusError létrehozása részletekkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_event_bus_error_is_neural_ai_exception()`

```python
def test_event_bus_error_is_neural_ai_exception(self) -> None
```

EventBusError NeuralAIException-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPublishError`

PublishError osztály tesztei.

### Metódusok

#### `test_publish_error_creation()`

```python
def test_publish_error_creation(self) -> None
```

PublishError létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_error_with_event_type()`

```python
def test_publish_error_with_event_type(self) -> None
```

PublishError létrehozása event type-nal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_error_inheritance()`

```python
def test_publish_error_inheritance(self) -> None
```

PublishError EventBusError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestSubscriberError`

SubscriberError osztály tesztei.

### Metódusok

#### `test_subscriber_error_creation()`

```python
def test_subscriber_error_creation(self) -> None
```

SubscriberError létrehozásának tesztelése (47-48. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_subscriber_error_with_subscriber_id()`

```python
def test_subscriber_error_with_subscriber_id(self) -> None
```

SubscriberError létrehozása subscriber ID-vel (47-48. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_subscriber_error_inheritance()`

```python
def test_subscriber_error_inheritance(self) -> None
```

SubscriberError EventBusError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/events/exceptions/test_event_error.py`](../../tests/neural_ai/core/events/exceptions/test_event_error.py)
