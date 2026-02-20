# neural_ai/core/system/factory.py

Rendszer komponensek factory implementáció.

Ez a modul biztosítja a SystemComponentFactory osztályt, amely felelős a rendszer
szintű komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért. A factory
mintát követve centralizálja a komponens példányosítást és életciklus kezelést.

A factory támogatja a következő komponenseket:
- health_monitor: Rendszer egészségügyi monitorozás

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.core.system.interfaces.health_interface import HealthCheckInterface
from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.system.implementations.health_monitor import HealthMonitor
# ... és még 2 import
```

## Osztály: `SystemComponentFactory`

Factory osztály rendszer komponensek létrehozásához.

A factory mintát követve centralizálja a rendszer szintű komponensek
létrehozását és életciklus kezelését. Támogatja a különböző komponens
implementációk regisztrálását és lekérdezését.

A factory alkalmazza a Dependency Injection elvet, és csak interfészeken
keresztül kommunikál a konkrét implementációkkal.

Attributes:
    _health_monitors: Létrehozott HealthMonitor példányok gyorsítótárban.

### Metódusok

#### `create_health_monitor()`

```python
def create_health_monitor(cls, name: str = 'default', config: 'ConfigManagerInterface | None' = None, logger: 'LoggerInterface | None' = None, eventbus: 'EventBusInterface | None' = None, storage: 'StorageInterface | None' = None, hardware: 'HardwareInterface | None' = None) -> HealthMonitorInterface
```

HealthMonitor példány létrehozása vagy visszaadása. A metódus létrehozza a HealthMonitor komponenst a megadott paraméterekkel, vagy visszaadja a meglévő példányt, ha már létezik az adott névvel.

**Paraméterek:**

- **`cls`**
- **`name`** (`str`) = `'default'`: A HealthMonitor egyedi neve (alapértelmezett: "default")
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: ConfigManager interfész (opcionális)
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális)
- **`eventbus`** (`'EventBusInterface | None'`) = `None`: EventBus interfész (opcionális)
- **`storage`** (`'StorageInterface | None'`) = `None`: Storage interfész (opcionális)
- **`hardware`** (`'HardwareInterface | None'`) = `None`: Hardware interfész (opcionális) **kwargs: További paraméterek a HealthMonitor konstruktorának

**Visszatérési érték:**

- Típus: `HealthMonitorInterface`
- HealthMonitorInterface: Az inicializált HealthMonitor példány Példa: >>> from neural_ai.core.logger import LoggerFactory >>> logger = LoggerFactory.get_logger("system") >>> monitor = SystemComponentFactory.create_health_monitor( ...     name="main", ...     logger=logger ... ) >>> health = await monitor.check_health() >>> print(f"Rendszer állapota: {health.overall_status.value}")

#### `create_health_check()`

```python
def create_health_check(cls, component_name: str, logger: 'LoggerInterface | None' = None, health_check_type: str = 'default') -> HealthCheckInterface
```

HealthCheck példány létrehozása. A metódus létrehozza a megadott típusú HealthCheck komponenst.

**Paraméterek:**

- **`cls`**
- **`component_name`** (`str`): A komponens neve, amelyet az ellenőrzés monitoroz
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális)
- **`health_check_type`** (`str`) = `'default'`: Az ellenőrzés típusa (alapértelmezett: "default") **kwargs: További paraméterek a HealthCheck konstruktorának

**Visszatérési érték:**

- Típus: `HealthCheckInterface`
- HealthCheckInterface: Az inicializált HealthCheck példány

**Kivételek:**

- **`ValueError`**: Ha az ismeretlen health_check_type van megadva

#### `register_component()`

```python
def register_component(cls, monitor_name: str, component_name: str, health_check: 'HealthCheckInterface | None' = None) -> None
```

Regisztrál egy komponenst a HealthMonitor-ban. A metódus regisztrálja a megadott komponenst a monitorozásra a HealthMonitor-ban. Ha nincs megadva egyedi HealthCheck, akkor alapértelmezett ellenőrzést használ.

**Paraméterek:**

- **`cls`**
- **`monitor_name`** (`str`): A HealthMonitor neve, amelybe regisztrálunk
- **`component_name`** (`str`): A regisztrálandó komponens neve
- **`health_check`** (`'HealthCheckInterface | None'`) = `None`: Egyedi HealthCheck interfész (opcionális)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a megadott monitor_name nem létezik

#### `unregister_component()`

```python
def unregister_component(cls, monitor_name: str, component_name: str) -> None
```

Eltávolít egy komponenst a HealthMonitor-ból.

**Paraméterek:**

- **`cls`**
- **`monitor_name`** (`str`): A HealthMonitor neve, amelyből eltávolítunk
- **`component_name`** (`str`): Az eltávolítandó komponens neve

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a megadott monitor_name nem létezik

#### `get_health_monitor()`

```python
def get_health_monitor(cls, name: str) -> 'HealthMonitorInterface | None'
```

Lekéri a megadott névvel rendelkező HealthMonitor-t.

**Paraméterek:**

- **`cls`**
- **`name`** (`str`): A HealthMonitor neve

**Visszatérési érték:**

- Típus: `'HealthMonitorInterface | None'`
- HealthMonitorInterface | None: A HealthMonitor példány, ha létezik, egyébként None

#### `get_registered_monitors()`

```python
def get_registered_monitors(cls) -> list[str]
```

Visszaadja a regisztrált HealthMonitor-ok neveit.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A regisztrált HealthMonitor-ok neveinek listája

#### `clear_monitors()`

```python
def clear_monitors(cls) -> None
```

Törli az összes HealthMonitor példányt a gyorsítótárból. Ez a metódus hasznos teszteléskor vagy amikor teljesen új HealthMonitor példányokat szeretnénk létrehozni.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/system/factory.py`](../../neural_ai/core/system/factory.py)
