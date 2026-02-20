# tests/neural_ai/core/system/test_system_factory.py

SystemComponentFactory tesztelése.

Ez a modul a SystemComponentFactory osztályt teszteli, amely felelős
a rendszer komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért.

## Importok

```python
import asyncio
import unittest
from unittest.mock import MagicMock
from neural_ai.core.system.factory import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import ComponentHealth
from neural_ai.core.system.interfaces.health_interface import ComponentStatus
from neural_ai.core.system.interfaces.health_interface import HealthCheckInterface
from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
from neural_ai.core.system.interfaces.health_interface import HealthStatus
```

## Osztály: `TestSystemComponentFactory(unittest.TestCase)`

SystemComponentFactory osztály tesztjei.

### Metódusok

#### `setUp()`

```python
def setUp(self) -> None
```

Tesztelés előtti beállítások.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `tearDown()`

```python
def tearDown(self) -> None
```

Tesztelés utáni takarítás.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_monitor_default()`

```python
def test_create_health_monitor_default(self) -> None
```

Alapértelmezett HealthMonitor létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_monitor_with_name()`

```python
def test_create_health_monitor_with_name(self) -> None
```

HealthMonitor létrehozása névvel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_monitor_with_logger()`

```python
def test_create_health_monitor_with_logger(self) -> None
```

HealthMonitor létrehozása loggerrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_monitor_caching()`

```python
def test_create_health_monitor_caching(self) -> None
```

HealthMonitor gyorsítótár tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_check_default()`

```python
def test_create_health_check_default(self) -> None
```

Alapértelmezett HealthCheck létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_check_with_logger()`

```python
def test_create_health_check_with_logger(self) -> None
```

HealthCheck létrehozása loggerrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_health_check_invalid_type()`

```python
def test_create_health_check_invalid_type(self) -> None
```

Érvénytelen HealthCheck típus tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_component()`

```python
def test_register_component(self) -> None
```

Komponens regisztrálásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_component_with_custom_check()`

```python
def test_register_component_with_custom_check(self) -> None
```

Komponens regisztrálása egyedi ellenőrzéssel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_component_nonexistent_monitor()`

```python
def test_register_component_nonexistent_monitor(self) -> None
```

Komponens regisztrálása nem létező monitorhoz.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_unregister_component()`

```python
def test_unregister_component(self) -> None
```

Komponens eltávolításának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_unregister_component_nonexistent_monitor()`

```python
def test_unregister_component_nonexistent_monitor(self) -> None
```

Komponens eltávolítása nem létező monitorból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_health_monitor()`

```python
def test_get_health_monitor(self) -> None
```

HealthMonitor lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_health_monitor_nonexistent()`

```python
def test_get_health_monitor_nonexistent(self) -> None
```

Nem létező HealthMonitor lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_registered_monitors()`

```python
def test_get_registered_monitors(self) -> None
```

Regisztrált monitorok listázásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_clear_monitors()`

```python
def test_clear_monitors(self) -> None
```

Monitorok törlésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_health_monitor_integration()`

```python
def test_health_monitor_integration(self) -> None
```

HealthMonitor integrációs teszt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_health_monitor_with_system_metrics()`

```python
def test_health_monitor_with_system_metrics(self) -> None
```

HealthMonitor rendszer metrikák gyűjtésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_component_fallback_implementation()`

```python
def test_register_component_fallback_implementation(self) -> None
```

Teszteli a register_component fallback implementációját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/system/test_system_factory.py`](../../tests/neural_ai/core/system/test_system_factory.py)
