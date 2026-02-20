# neural_ai/core/system/implementations/health_monitor.py

Rendszer egészségügyi monitorozás implementációja.

Ez a modul a `HealthMonitorInterface` interfész konkrét implementációját tartalmazza,
amely a rendszer komponenseinek egészségügyi állapotát monitorozza, és metrikákat gyűjt.

## Importok

```python
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
import psutil
from neural_ai.core.system.interfaces.health_interface import ComponentHealth
from neural_ai.core.system.interfaces.health_interface import ComponentStatus
from neural_ai.core.system.interfaces.health_interface import HealthCheckInterface
from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
from neural_ai.core.system.interfaces.health_interface import HealthStatus
from neural_ai.core.system.interfaces.health_interface import SystemHealth
# ... és még 5 import
```

## Osztály: `HealthMonitor(HealthMonitorInterface)`

Rendszer egészségügyi monitorozást implementáló osztály.

Ez az osztály a `HealthMonitorInterface` interfészt implementálja, és felelős
a rendszer komponenseinek egészségügyi állapotának monitorozásáért, valamint
a rendszer szintű metrikák (CPU, memória, stb.) gyűjtéséért.

Attributes:
    _components: A monitorozott komponensek szótárát tárolja
    _logger: A naplózó interfész (opcionális)

### Metódusok

#### `__init__()`

```python
def __init__(self, config: Optional['ConfigManagerInterface'] = None, logger: Optional['LoggerInterface'] = None, eventbus: Optional['EventBusInterface'] = None, storage: Optional['StorageInterface'] = None, hardware: Optional['HardwareInterface'] = None) -> None
```

Inicializálja a HealthMonitor osztályt.

**Paraméterek:**

- **`self`**
- **`config`** (`Optional['ConfigManagerInterface']`) = `None`: A konfiguráció kezelő interfész (opcionális)
- **`logger`** (`Optional['LoggerInterface']`) = `None`: A naplózó interfész (opcionális)
- **`eventbus`** (`Optional['EventBusInterface']`) = `None`: Az eseménybusz interfész (opcionális)
- **`storage`** (`Optional['StorageInterface']`) = `None`: A tároló interfész (opcionális)
- **`hardware`** (`Optional['HardwareInterface']`) = `None`: A hardver interfész (opcionális)

**Visszatérési érték:**

- Típus: `None`

#### `check_health()`

```python
async def check_health(self) -> SystemHealth
```

Ellenőrzi a teljes rendszer egészségügyi állapotát. A metódus összegyűjti az összes komponens és a rendszer egészségügyi információit, majd összesíti azokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `SystemHealth`
- SystemHealth: A rendszer teljes egészségügyi állapota

**Példák:**

```python
    >>> monitor = HealthMonitor()
    >>> health = monitor.check_health()
    >>> print(f"Rendszer állapota: {health.overall_status.value}")
```

#### `check_component()`

```python
async def check_component(self, component_name: str) -> ComponentHealth
```

Ellenőrzi egy adott komponens egészségügyi állapotát.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve

**Visszatérési érték:**

- Típus: `ComponentHealth`
- ComponentHealth: A komponens egészségügyi információi

**Kivételek:**

- **`ValueError`**: Ha a komponens nem létezik

**Példák:**

```python
    >>> monitor = HealthMonitor()
    >>> monitor.register_component("database")
    >>> health = monitor.check_component("database")
    >>> print(f"Komponens állapota: {health.status.value}")
```

#### `get_registered_components()`

```python
def get_registered_components(self) -> list[str]
```

Visszaadja a monitorozott komponensek listáját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A monitorozott komponensek nevei

**Példák:**

```python
    >>> monitor = HealthMonitor()
    >>> monitor.register_component("database")
    >>> monitor.register_component("storage")
    >>> components = monitor.get_registered_components()
    >>> print(f"Monitorozott komponensek: {components}")
```

#### `register_component()`

```python
def register_component(self, component_name: str, health_check: Optional['HealthCheckInterface'] = None) -> None
```

Regisztrál egy új komponenst a monitorozásra.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve
- **`health_check`** (`Optional['HealthCheckInterface']`) = `None`: Az egészségügyi ellenőrzés interfésze (opcionális)

**Visszatérési érték:**

- Típus: `None`

**Példák:**

```python
    >>> monitor = HealthMonitor()
    >>> # Alapértelmezett ellenőrzéssel
    >>> monitor.register_component("database")
    >>> # Egyedi ellenőrzéssel
    >>> custom_check = CustomHealthCheck()
    >>> monitor.register_component("storage", custom_check)
```

#### `unregister_component()`

```python
def unregister_component(self, component_name: str) -> None
```

Eltávolít egy komponenst a monitorozás alól.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve

**Visszatérési érték:**

- Típus: `None`

**Példák:**

```python
    >>> monitor = HealthMonitor()
    >>> monitor.register_component("database")
    >>> monitor.unregister_component("database")
```

#### `_collect_system_metrics()`

```python
def _collect_system_metrics(self) -> dict[str, float]
```

Gyűjti a rendszer szintű metrikákat. A metódus a rendszer erőforrás-használatát gyűjti (CPU, memória, stb.).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, float]`
- Dict[str, float]: A rendszer metrikák szótára

#### `_register_bootstrap_components()`

```python
def _register_bootstrap_components(self) -> None
```

Regisztrálja az összes bootstrap komponenst egészségügyi ellenőrzésre. Ez a metódus automatikusan regisztrálja az összes rendelkezésre álló bootstrap komponenst, hogy a rendszer egészségügyi állapota teljes képet adjon.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `DefaultHealthCheck(HealthCheckInterface)`

Alapértelmezett egészségügyi ellenőrzés implementációja.

Ez az osztály egy egyszerű egészségügyi ellenőrzést valósít meg,
amely mindig HEALTHY státuszt ad vissza. Használható olyan komponensekhez,
amelyeknek nincs specifikus egészségügyi ellenőrzésük.

Attributes:
    _name: A komponens neve
    _logger: A naplózó interfész (opcionális)

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, logger: Optional['LoggerInterface'] = None) -> None
```

Inicializálja a DefaultHealthCheck osztályt.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A komponens neve
- **`logger`** (`Optional['LoggerInterface']`) = `None`: A naplózó interfész (opcionális)

**Visszatérési érték:**

- Típus: `None`

#### `check()`

```python
async def check(self) -> ComponentHealth
```

Végrehajtja az egészségügyi ellenőrzést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `ComponentHealth`
- ComponentHealth: Az ellenőrzés eredménye (mindig HEALTHY)

#### `get_name()`

```python
def get_name(self) -> str
```

Visszaadja az ellenőrzés nevét.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az ellenőrzés neve

---

**Forrásfájl:** [`neural_ai/core/system/implementations/health_monitor.py`](../../neural_ai/core/system/implementations/health_monitor.py)
