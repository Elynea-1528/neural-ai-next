# neural_ai/core/events/implementations/zeromq_bus.py

EventBus implementáció ZeroMQ-val és asyncio-val.

Ez a modul biztosítja az eseményvezérelt architektúra magját, lehetővé téve
a komponensek közötti laza csatolást Pub/Sub mintázattal.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import asyncio
import json
from collections.abc import Callable
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.events.exceptions import EventBusError
# ... és még 15 import
```

## Konstansok

- **`logger`**
: `LoggerFactory.get_logger(__name__)`


- **`EventCallback`**
: `Callable[['BaseModel'], 'Any']`


## Osztály: `EventBus(EventBusInterface)`

ZeroMQ alapú aszinkron eseménybusz.

Ez az osztály biztosítja az események közzétételét és feliratkozást
a rendszer különböző komponensei számára. A ZeroMQ PUB/SUB mintázatot használja.

A specifikációban említett asyncio.Queue-s megvalósítás helyett egyből
ZeroMQ-t használunk a teljesítmény és a skálázhatóság érdekében.

Attributes:
    config: Az EventBus konfigurációja
    _context: ZeroMQ kontextus
    _publisher: Publisher socket
    _subscribers: Feliratkozók szótára event_type -> callback lista
    _running: Futási állapot jelzője

### Metódusok

#### `config()`

```python
def config(self) -> EventBusConfig
```

Visszaadja az EventBus konfigurációját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `EventBusConfig`

#### `__init__()`

```python
def __init__(self, config: EventBusConfig | None = None, logger: 'LoggerInterface | None' = None) -> None
```

Inicializálja az EventBus-t.

**Paraméterek:**

- **`self`**
- **`config`** (`EventBusConfig | None`) = `None`: EventBus konfiguráció (opcionális)
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész (KÖTELEZŐ - Dependency Injection)

**Visszatérési érték:**

- Típus: `None`

#### `start()`

```python
async def start(self) -> None
```

Elindítja az EventBus-t és létrehozza a socketeket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `stop()`

```python
async def stop(self) -> None
```

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `publish()`

```python
async def publish(self, event_type: str, event: 'BaseModel | list[BaseModel]') -> None
```

Esemény közzététele a buszon.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa (pl. 'market_data', 'trade')
- **`event`** (`'BaseModel | list[BaseModel]'`): Az esemény objektum (Pydantic BaseModel) VAGY események listája

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`EventBusError`**: Ha az EventBus nincs elindítva
- **`PublishError`**: Ha a publisher socket nincs inicializálva

#### `subscribe()`

```python
def subscribe(self, event_type: str, callback: EventCallback) -> None
```

Feliratkozás eseménytípusra.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa, amire feliratkozunk
- **`callback`** (`EventCallback`): A callback függvény, amely az eseményt fogadja Note: A callback-nek aszinkronnak kell lennie (async def)

**Visszatérési érték:**

- Típus: `None`

#### `unsubscribe()`

```python
def unsubscribe(self, event_type: str, callback: EventCallback) -> None
```

Leiratkozás eseménytípusról.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa
- **`callback`** (`EventCallback`): A callback függvény, amelyet eltávolítunk

**Visszatérési érték:**

- Típus: `None`

#### `_dispatch_event()`

```python
async def _dispatch_event(self, event_type: str, event_data: dict[str, Any]) -> None
```

Esemény továbbítása a feliratkozóknak.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa
- **`event_data`** (`dict[str, Any]`): Az esemény adatai

**Visszatérési érték:**

- Típus: `None`

#### `_deserialize_event()`

```python
def _deserialize_event(self, event_type: str, event_data: dict[str, Any]) -> Optional['BaseModel']
```

Deserializálja az eseményt a megfelelő Pydantic modellbe.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa
- **`event_data`** (`dict[str, Any]`): Az esemény adatai

**Visszatérési érték:**

- Típus: `Optional['BaseModel']`
- A deserializált esemény objektum vagy None ha hiba történt

#### `run_forever()`

```python
async def run_forever(self) -> None
```

Eseménybusz örök futás (blokkoló). Ez a metódus egy végtelen ciklusban fogadja az eseményeket és továbbítja azokat a feliratkozóknak. Note: Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `__aenter__()`

```python
async def __aenter__(self) -> 'EventBus'
```

Aszinkron context manager.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'EventBus'`
- Az EventBus példány

#### `__aexit__()`

```python
async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None
```

Aszinkron context manager lezárás.

**Paraméterek:**

- **`self`**
- **`exc_type`** (`type[BaseException] | None`): A kivétel típusa (ha volt kivétel)
- **`exc_val`** (`BaseException | None`): A kivétel objektum (ha volt kivétel)
- **`exc_tb`** (`Any | None`): A traceback objektum (ha volt kivétel)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/events/implementations/zeromq_bus.py`](../../neural_ai/core/events/implementations/zeromq_bus.py)
