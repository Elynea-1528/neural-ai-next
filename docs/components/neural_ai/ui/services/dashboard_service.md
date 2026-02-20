# neural_ai/ui/services/dashboard_service.py

Dashboard Service implementáció.

Ez a modul implementálja a dashboard szolgáltatást, amely
a fő irányítópult adatait és állapotát kezeli.

## Importok

```python
import asyncio
from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.core.system.interfaces.health_interface import ComponentStatus
from neural_ai.core.system.interfaces.health_interface import SystemHealth
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
```

## Osztály: `DashboardService(DashboardServiceInterface)`

Dashboard Service - Fő irányítópult kezeléséért felelős.

Ez az osztály implementálja a dashboard adatok lekérdezését és
kezelését végző metódusokat.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: Any, config: dict[str, Any], core_components: Any) -> None
```

A Dashboard Service inicializálása.

**Paraméterek:**

- **`self`**
- **`logger`** (`Any`): A logger példány
- **`config`** (`dict[str, Any]`): A szolgáltatás konfiguráció
- **`core_components`** (`Any`): A core komponensek

**Visszatérési érték:**

- Típus: `None`

#### `get_system_overview()`

```python
def get_system_overview(self) -> dict[str, Any]
```

Rendszer áttekintő adatok lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A rendszer aktuális állapota

#### `get_health_status()`

```python
def get_health_status(self) -> dict[str, str]
```

Rendszer egészségügyi állapotának lekérdezése. A metódus a valós HealthMonitor komponenst kérdezi le a backend rendszerből, és leképezi a komponens állapotokat UI-barát formátumba.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, str]`
- Dict[str, str]: A komponensek állapota (OK/WARNING/ERROR/CRITICAL/UNKNOWN)

#### `get_performance_metrics()`

```python
def get_performance_metrics(self) -> dict[str, float]
```

Teljesítmény metrikák lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, float]`
- Dict[str, float]: A rendszer teljesítményadatok

#### `get_recent_activities()`

```python
def get_recent_activities(self) -> list[dict[str, Any]]
```

Legutóbbi tevékenységek lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`
- List[Dict[str, Any]]: A tevékenységek listája

#### `refresh_data()`

```python
def refresh_data(self) -> None
```

Dashboard adatok frissítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `subscribe_to_updates()`

```python
def subscribe_to_updates(self, callback: Callable[[dict[str, Any]], None]) -> None
```

Feliratkozás dashboard frissítésekre.

**Paraméterek:**

- **`self`**
- **`callback`** (`Callable[[dict[str, Any]], None]`): A hívandó callback függvény

**Visszatérési érték:**

- Típus: `None`

#### `_notify_subscribers()`

```python
def _notify_subscribers(self, data: dict[str, Any]) -> None
```

Értesítés küldése a feliratkozóknak.

**Paraméterek:**

- **`self`**
- **`data`** (`dict[str, Any]`): Az értesítés adatai

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/services/dashboard_service.py`](../../neural_ai/ui/services/dashboard_service.py)
