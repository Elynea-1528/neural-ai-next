# neural_ai/core/system/__init__.py

Rendszer komponensek modul.

Ez a modul a rendszer szintű komponensek (pl. HealthMonitor) interfészeit
és factory osztályait exportálja.

## Importok

```python
from neural_ai.core.system.factory import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import ComponentHealth
from neural_ai.core.system.interfaces.health_interface import ComponentStatus
from neural_ai.core.system.interfaces.health_interface import HealthCheckInterface
from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
from neural_ai.core.system.interfaces.health_interface import HealthStatus
from neural_ai.core.system.interfaces.health_interface import SystemHealth
```

## Konstansok

- **`__all__`**
: `['SystemComponentFactory', 'HealthMonitorInterface', 'HealthCheckInterface', 'ComponentHealth', 'ComponentStatus', 'HealthStatus', 'SystemHealth']`


---

**Forrásfájl:** [`neural_ai/core/system/__init__.py`](../../neural_ai/core/system/__init__.py)
