# tests/neural_ai/core/events/test_events_factory.py

Tesztek az EventBusFactory-hez.

Ez a modul tartalmazza az EventBusFactory tesztjeit.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
import inspect
```

## Osztály: `TestEventBusFactoryCreate`

EventBusFactory create metódus tesztek.

### Metódusok

#### `test_create_default()`

```python
def test_create_default(self, mock_event_bus_class: MagicMock) -> None
```

Teszteli az alapértelmezett EventBus létrehozást.

**Paraméterek:**

- **`self`**
- **`mock_event_bus_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_with_config()`

```python
def test_create_with_config(self, mock_event_bus_class: MagicMock) -> None
```

Teszteli az EventBus létrehozást konfigurációval.

**Paraméterek:**

- **`self`**
- **`mock_event_bus_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_returns_interface()`

```python
def test_create_returns_interface(self) -> None
```

Teszteli, hogy az EventBusFactory EventBusInterface-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusFactoryCreateAndStart`

EventBusFactory create_and_start metódus tesztek.

### Metódusok

#### `test_create_and_start_default()`

```python
async def test_create_and_start_default(self, mock_event_bus_class: MagicMock) -> None
```

Teszteli az alapértelmezett EventBus létrehozást és indítását.

**Paraméterek:**

- **`self`**
- **`mock_event_bus_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_and_start_with_config()`

```python
async def test_create_and_start_with_config(self, mock_event_bus_class: MagicMock) -> None
```

Teszteli az EventBus létrehozást és indítását konfigurációval.

**Paraméterek:**

- **`self`**
- **`mock_event_bus_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_and_start_returns_interface()`

```python
async def test_create_and_start_returns_interface(self) -> None
```

Teszteli, hogy a create_and_start EventBusInterface-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusFactoryCreateFromConfig`

EventBusFactory create_from_config metódus tesztek.

### Metódusok

#### `test_create_from_config_success()`

```python
def test_create_from_config_success(self) -> None
```

Teszteli a sikeres EventBus létrehozást konfigurációkezelőből.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_from_config_with_key_error()`

```python
def test_create_from_config_with_key_error(self) -> None
```

Teszteli az EventBus létrehozást KeyError esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_from_config_with_value_error()`

```python
def test_create_from_config_with_value_error(self) -> None
```

Teszteli az EventBus létrehozást ValueError esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_from_config_partial_config()`

```python
def test_create_from_config_partial_config(self) -> None
```

Teszteli az EventBus létrehozást részleges konfigurációval.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_from_config_returns_interface()`

```python
def test_create_from_config_returns_interface(self) -> None
```

Teszteli, hogy a create_from_config EventBusInterface-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusFactoryStaticMethods`

EventBusFactory példány metódusok tesztek.

### Metódusok

#### `test_factory_methods_are_instance_methods()`

```python
def test_factory_methods_are_instance_methods(self) -> None
```

Teszteli, hogy a factory metódusok példány metódusok.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/events/test_events_factory.py`](../../tests/neural_ai/core/events/test_events_factory.py)
