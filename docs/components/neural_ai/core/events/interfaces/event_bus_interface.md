# neural_ai/core/events/interfaces/event_bus_interface.py

EventBus interfész a Neural AI Next rendszerhez.

Ez a modul definiálja az EventBus interfészt, amely biztosítja
az eseményvezérelt architektúra alapjait.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from pydantic import BaseModel
```

## Konstansok

- **`EventCallback`**
: `Callable[['BaseModel'], Any]`


## Osztály: `EventBusConfig`

EventBus konfiguráció.

Attributes:
    zmq_context: ZeroMQ kontextus (opcionális, létrejön ha nincs megadva)
    pub_port: Publisher port (alapértelmezett: 5555)
    sub_port: Subscriber port (alapértelmezett: 5556)
    use_inproc: Használjon inproc transportot teszteléshez (alapértelmezett: False)

## Osztály: `EventBusInterface(ABC)`

EventBus interfész.

Ez az interfész definiálja az eseménybusz alapvető műveleteit:
- Események közzététele
- Feliratkozás eseményekre
- Leiratkozás eseményekről
- Bus indítása és leállítása

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
- Az EventBus konfigurációja

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
async def publish(self, event_type: str, event: 'BaseModel') -> None
```

Esemény közzététele a buszon.

**Paraméterek:**

- **`self`**
- **`event_type`** (`str`): Az esemény típusa (pl. 'market_data', 'trade')
- **`event`** (`'BaseModel'`): Az esemény objektum (Pydantic BaseModel)

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

#### `run_forever()`

```python
async def run_forever(self) -> None
```

Eseménybusz örök futás (blokkoló). Ez a metódus egy végtelen ciklusban fogadja az eseményeket és továbbítja azokat a feliratkozóknak. Note: Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/events/interfaces/event_bus_interface.py`](../../neural_ai/core/events/interfaces/event_bus_interface.py)
