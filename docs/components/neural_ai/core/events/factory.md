# neural_ai/core/events/factory.py

EventBus factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az EventBus létrehozását a konfiguráció alapján.
A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk
egyszerű cseréjét.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.implementations.zeromq_bus import EventBusConfig
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
```

## Osztály: `EventBusFactory`

EventBus factory osztály.

Ez az osztály felelős az EventBus példányok létrehozásáért.
Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', config_manager: 'ConfigManagerInterface') -> None
```

Inicializálja az EventBusFactory-t.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): Logger interfész a logoláshoz
- **`config_manager`** (`'ConfigManagerInterface'`): Konfigurációkezelő interfész

**Visszatérési érték:**

- Típus: `None`

#### `create()`

```python
def create(self, config: 'EventBusConfig | None' = None) -> 'EventBusInterface'
```

Létrehozza az EventBus példányt.

**Paraméterek:**

- **`self`**
- **`config`** (`'EventBusConfig | None'`) = `None`: EventBus konfiguráció (opcionális)

**Visszatérési érték:**

- Típus: `'EventBusInterface'`
- EventBusInterface: Az EventBus példány Note: Jelenleg csak a ZeroMQ-s implementációt támogatja.

#### `create_and_start()`

```python
async def create_and_start(self, config: 'EventBusConfig | None' = None) -> 'EventBusInterface'
```

Létrehozza és elindítja az EventBus példányt.

**Paraméterek:**

- **`self`**
- **`config`** (`'EventBusConfig | None'`) = `None`: EventBus konfiguráció (opcionális)

**Visszatérési érték:**

- Típus: `'EventBusInterface'`
- EventBusInterface: Az elindított EventBus példány

#### `get_event_bus()`

```python
def get_event_bus(logger: 'LoggerInterface') -> 'EventBusInterface'
```

Létrehozza az EventBus példányt alapértelmezett konfigurációval.

**Paraméterek:**

- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `'EventBusInterface'`
- EventBusInterface: Az EventBus példány

#### `create_from_config()`

```python
def create_from_config(self) -> 'EventBusInterface'
```

Létrehozza az EventBus példányt konfigurációkezelő alapján.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'EventBusInterface'`
- EventBusInterface: Az EventBus példány Note: A metódus biztonságosan kezeli a konfiguráció hiányát, alapértelmezett értékeket használva.

---

**Forrásfájl:** [`neural_ai/core/events/factory.py`](../../neural_ai/core/events/factory.py)
