# tests/neural_ai/ui/services/test_dashboard_service.py

Dashboard Service tesztek.

## Importok

```python
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
import pytest
from neural_ai.core.system.interfaces.health_interface import ComponentHealth
from neural_ai.core.system.interfaces.health_interface import ComponentStatus
from neural_ai.core.system.interfaces.health_interface import HealthStatus
from neural_ai.core.system.interfaces.health_interface import SystemHealth
from neural_ai.ui.services.dashboard_service import DashboardService
```

## Osztály: `TestDashboardService`

Dashboard Service tesztek osztálya.

### Metódusok

#### `mock_components()`

```python
def mock_components(self) -> MagicMock
```

Mock CoreComponents létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock Logger létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_config()`

```python
def mock_config(self) -> dict[str, Any]
```

Mock Config létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `mock_system_health()`

```python
def mock_system_health(self) -> SystemHealth
```

Mock SystemHealth létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `SystemHealth`

#### `test_init()`

```python
def test_init(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a Dashboard Service inicializálását.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_health_status_with_available_monitor()`

```python
def test_get_health_status_with_available_monitor(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock, mock_system_health: SystemHealth) -> None
```

Teszteli az egészségügyi állapot lekérdezését, ha a monitor elérhető.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)
- **`mock_system_health`** (`SystemHealth`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_health_status_without_health_monitor()`

```python
def test_get_health_status_without_health_monitor(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli az egészségügyi állapot lekérdezését, ha a health monitor nem elérhető.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_health_status_all_status_types()`

```python
def test_get_health_status_all_status_types(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli az összes állapot típus leképezését.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_system_overview()`

```python
def test_get_system_overview(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a rendszer áttekintő adatok lekérdezését.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_performance_metrics_with_resources()`

```python
def test_get_performance_metrics_with_resources(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a teljesítmény metrikák lekérdezését resources adatokkal.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_performance_metrics_without_resources()`

```python
def test_get_performance_metrics_without_resources(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a teljesítmény metrikák lekérdezését resources adatok nélkül.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_recent_activities()`

```python
def test_get_recent_activities(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a legutóbbi tevékenységek lekérdezését.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_refresh_data()`

```python
def test_refresh_data(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a dashboard adatok frissítését.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_subscribe_to_updates()`

```python
def test_subscribe_to_updates(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a feliratkozást dashboard frissítésekre.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_notify_subscribers()`

```python
def test_notify_subscribers(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a feliratkozók értesítését.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_notify_subscribers_with_exception()`

```python
def test_notify_subscribers_with_exception(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli a feliratkozók értesítését, ha egy callback hibát dob.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `failing_callback()`

```python
def failing_callback(data: dict[str, Any]) -> None
```

**Paraméterek:**

- **`data`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_cached_data_persistence()`

```python
def test_cached_data_persistence(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> None
```

Teszteli, hogy az adatok tényleg gyorsítótárazásra kerülnek.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/ui/services/test_dashboard_service.py`](../../tests/neural_ai/ui/services/test_dashboard_service.py)
