# neural_ai/core/base/implementations/component_bundle.py

Core komponensek gyűjtemény.

## Importok

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Optional
from typing import TypeVar
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.utils.decorators import trace
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
# ... és még 35 import
```

## Konstansok

- **`T`**
: `TypeVar('T')`


## Osztály: `CoreComponents`

Alap komponensek lusta betöltéssel.

### Metódusok

#### `__init__()`

```python
def __init__(self, container: DIContainer | None = None, logger: LoggerInterface | None = None)
```

Alap komponensek inicializálása.

**Paraméterek:**

- **`self`**
- **`container`** (`DIContainer | None`) = `None`: Egy függőséginjektáló konténer példány. Ha nincs megadva, új konténert hoz létre.
- **`logger`** (`LoggerInterface | None`) = `None`: Logger példány (opcionális - próbálja a container-ből kiolvasni).

#### `config()`

```python
def config(self) -> ConfigManagerInterface | None
```

Konfiguráció kezelő komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `ConfigManagerInterface | None`
- A konfiguráció kezelő példánya, vagy None ha nincs regisztrálva.

#### `logger()`

```python
def logger(self) -> LoggerInterface | None
```

Naplózó komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `LoggerInterface | None`
- A naplózó példánya, vagy None ha nincs regisztrálva.

#### `storage()`

```python
def storage(self) -> StorageInterface | None
```

Tároló komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `StorageInterface | None`
- A tároló példánya, vagy None ha nincs regisztrálva.

#### `database()`

```python
def database(self) -> DatabaseManager | None
```

Adatbázis komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `DatabaseManager | None`
- Az adatbázis példánya, vagy None ha nincs regisztrálva.

#### `event_bus()`

```python
def event_bus(self) -> EventBusInterface | None
```

Esemény busz komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `EventBusInterface | None`
- Az esemény busz példánya, vagy None ha nincs regisztrálva.

#### `hardware()`

```python
def hardware(self) -> HardwareInterface | None
```

Hardver információ komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `HardwareInterface | None`
- A hardver információ példánya, vagy None ha nincs regisztrálva.

#### `persister()`

```python
def persister(self) -> MarketDataPersister | None
```

Market data persister komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MarketDataPersister | None`
- A market data persister példánya, vagy None ha nincs regisztrálva.

#### `live_feed()`

```python
def live_feed(self) -> ILiveFeed | None
```

Live feed komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `ILiveFeed | None`
- A live feed példánya, vagy None ha nincs regisztrálva.

#### `health_monitor()`

```python
def health_monitor(self) -> HealthMonitorInterface | None
```

Health monitor komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `HealthMonitorInterface | None`
- A health monitor példánya, vagy None ha nincs regisztrálva.

#### `set_config()`

```python
def set_config(self, config: ConfigManagerInterface) -> None
```

Beállítja a konfiguráció komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`config`** (`ConfigManagerInterface`): A konfiguráció kezelő implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_logger()`

```python
def set_logger(self, logger: LoggerInterface) -> None
```

Beállítja a naplózó komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`logger`** (`LoggerInterface`): A naplózó implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_storage()`

```python
def set_storage(self, storage: StorageInterface) -> None
```

Beállítja a tároló komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`storage`** (`StorageInterface`): A tároló implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_database()`

```python
def set_database(self, database: DatabaseManager) -> None
```

Beállítja az adatbázis komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`database`** (`DatabaseManager`): Az adatbázis implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_event_bus()`

```python
def set_event_bus(self, event_bus: EventBusInterface) -> None
```

Beállítja az esemény busz komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`event_bus`** (`EventBusInterface`): Az esemény busz implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_hardware()`

```python
def set_hardware(self, hardware: HardwareInterface) -> None
```

Beállítja a hardver információ komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`hardware`** (`HardwareInterface`): A hardver információ implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_persister()`

```python
def set_persister(self, persister: MarketDataPersister) -> None
```

Beállítja a market data persister komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`persister`** (`MarketDataPersister`): A market data persister implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_live_feed()`

```python
def set_live_feed(self, live_feed: ILiveFeed) -> None
```

Beállítja a live feed komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`live_feed`** (`ILiveFeed`): A live feed implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `set_health_monitor()`

```python
def set_health_monitor(self, health_monitor: HealthMonitorInterface) -> None
```

Beállítja a health monitor komponenst (csak teszteléshez).

**Paraméterek:**

- **`self`**
- **`health_monitor`** (`HealthMonitorInterface`): A health monitor implementáció példánya.

**Visszatérési érték:**

- Típus: `None`

#### `has_config()`

```python
def has_config(self) -> bool
```

Ellenőrzi, hogy van-e config komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van config komponens, False ha nincs

#### `has_logger()`

```python
def has_logger(self) -> bool
```

Ellenőrzi, hogy van-e logger komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van logger komponens, False ha nincs

#### `has_storage()`

```python
def has_storage(self) -> bool
```

Ellenőrzi, hogy van-e storage komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van storage komponens, False ha nincs

#### `has_database()`

```python
def has_database(self) -> bool
```

Ellenőrzi, hogy van-e database komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van database komponens, False ha nincs

#### `has_event_bus()`

```python
def has_event_bus(self) -> bool
```

Ellenőrzi, hogy van-e event_bus komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van event_bus komponens, False ha nincs

#### `has_hardware()`

```python
def has_hardware(self) -> bool
```

Ellenőrzi, hogy van-e hardware komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van hardware komponens, False ha nincs

#### `has_persister()`

```python
def has_persister(self) -> bool
```

Ellenőrzi, hogy van-e persister komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van persister komponens, False ha nincs

#### `has_live_feed()`

```python
def has_live_feed(self) -> bool
```

Ellenőrzi, hogy van-e live feed komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van live feed komponens, False ha nincs

#### `has_health_monitor()`

```python
def has_health_monitor(self) -> bool
```

Ellenőrzi, hogy van-e health monitor komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha van health monitor komponens, False ha nincs

#### `validate()`

```python
def validate(self) -> bool
```

Ellenőrzi, hogy minden szükséges komponens megvan-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha minden komponens megvan, False ha valamelyik hiányzik

---

**Forrásfájl:** [`neural_ai/core/base/implementations/component_bundle.py`](../../neural_ai/core/base/implementations/component_bundle.py)
