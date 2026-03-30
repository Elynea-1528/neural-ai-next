# neural_ai/collectors/jforex/factory.py

JForex Collector Factory.

## Importok

```python
from typing import TYPE_CHECKING
from typing import cast
from pydantic import ValidationError
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.config.interfaces.types import JForexConfig
from neural_ai.core.config.interfaces.types import JForexLiveConfig
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
# ... és még 4 import
```

## Osztály: `JForexFactory`

Factory JForex Collector komponensek létrehozására.

Dependency injection-t biztosít a JForex letöltő példányokhoz.

### Metódusok

#### `create_downloader()`

```python
def create_downloader(config: 'ConfigManagerInterface', logger: 'LoggerInterface', event_bus: 'EventBusInterface | None', storage: 'StorageInterface') -> IJForexDownloader
```

JForex letöltő példány létrehozása DI-vel.

**Paraméterek:**

- **`config`** (`'ConfigManagerInterface'`): Konfiguráció kezelő példány
- **`logger`** (`'LoggerInterface'`): Logger példány
- **`event_bus`** (`'EventBusInterface | None'`): Event bus piaci adatok publikálására
- **`storage`** (`'StorageInterface'`): Storage interfész adat perzisztenciához

**Visszatérési érték:**

- Típus: `IJForexDownloader`
- JForex letöltő példány, ami megvalósítja az IJForexDownloader-t

#### `create_live_feed()`

```python
def create_live_feed(config: 'ConfigManagerInterface', logger: 'LoggerInterface', event_bus: 'EventBusInterface') -> ILiveFeed
```

JForex live feed példány létrehozása DI-vel.

**Paraméterek:**

- **`config`** (`'ConfigManagerInterface'`): Konfiguráció kezelő példány
- **`logger`** (`'LoggerInterface'`): Logger példány
- **`event_bus`** (`'EventBusInterface'`): Event bus piaci adatok publikálására

**Visszatérési érték:**

- Típus: `ILiveFeed`
- JForex live feed példány, ami megvalósítja az ILiveFeed-et

---

**Forrásfájl:** [`neural_ai/collectors/jforex/factory.py`](../../neural_ai/collectors/jforex/factory.py)
