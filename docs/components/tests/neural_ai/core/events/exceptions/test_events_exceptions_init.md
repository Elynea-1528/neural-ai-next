# tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py

Tesztek a core.events.exceptions.__init__.py exportjaihoz.

Ez a modul ellenőrzi, hogy a core.events.exceptions csomag megfelelően exportálja-e
a szükséges kivételeket.

## Importok

```python
from neural_ai.core.events.exceptions import EventBusError
from neural_ai.core.events.exceptions import PublishError
from neural_ai.core.events.exceptions import SubscriberError
from neural_ai.core.events.exceptions.event_error import EventBusError
from neural_ai.core.events.exceptions.event_error import PublishError
from neural_ai.core.events.exceptions.event_error import SubscriberError
from neural_ai.core.events.exceptions import __all__
from neural_ai.core.events import exceptions
```

## Osztály: `TestExceptionsInitExports`

Teszteli a core.events.exceptions.__init__.py exportjait.

### Metódusok

#### `test_event_bus_error_exported()`

```python
def test_event_bus_error_exported(self) -> None
```

Teszteli, hogy az EventBusError elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_error_exported()`

```python
def test_publish_error_exported(self) -> None
```

Teszteli, hogy a PublishError elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_subscriber_error_exported()`

```python
def test_subscriber_error_exported(self) -> None
```

Teszteli, hogy a SubscriberError elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_imports_in_all_list()`

```python
def test_all_imports_in_all_list(self) -> None
```

Teszteli, hogy minden import szerepel-e a __all__ listában.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_import_from_exceptions_package()`

```python
def test_import_from_exceptions_package(self) -> None
```

Teszteli, hogy az exceptions csomagból lehet-e importálni.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py`](../../tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py)
