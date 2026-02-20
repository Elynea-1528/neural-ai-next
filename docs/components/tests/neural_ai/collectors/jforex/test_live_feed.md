# tests/neural_ai/collectors/jforex/test_live_feed.py

JForex Live Feed Tests.

Ez a modul tartalmazza a JForexLiveFeed osztály tesztjeit.

## Importok

```python
import asyncio
import json
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
import zmq
from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
```

## Osztály: `TestJForexLiveFeed`

JForexLiveFeed osztály tesztjei.

### Metódusok

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock logger létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_event_bus()`

```python
def mock_event_bus(self) -> AsyncMock
```

Mock event bus létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `AsyncMock`

#### `mock_config()`

```python
def mock_config(self) -> MagicMock
```

Mock config létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `live_feed()`

```python
def live_feed(self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config: MagicMock) -> JForexLiveFeed
```

JForexLiveFeed példány létrehozása.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_config`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `JForexLiveFeed`

#### `test_start_success()`

```python
async def test_start_success(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli a start metódus sikeres futását.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_when_already_running()`

```python
async def test_start_when_already_running(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy a start metódus figyelmeztet, ha már fut a feed.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_success()`

```python
async def test_stop_success(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli a stop metódus sikeres futását.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_when_not_running()`

```python
async def test_stop_when_not_running(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy a stop metódus nem csinál semmit, ha nem fut a feed.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_tick_data_success()`

```python
async def test_process_tick_data_success(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock) -> None
```

Teszteli a tick adatok feldolgozását.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_process_tick_data_error()`

```python
async def test_process_tick_data_error(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli a hibakezelést tick adatok feldolgozásakor.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_listen_loop_processes_tick()`

```python
async def test_listen_loop_processes_tick(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock) -> None
```

Teszteli, hogy a listen loop feldolgozza a tick üzeneteket.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_recv()`

```python
async def mock_recv()
```

#### `test_is_running_returns_correct_state()`

```python
def test_is_running_returns_correct_state(self, live_feed: JForexLiveFeed) -> None
```

Teszteli, hogy az is_running metódus helyes állapotot adja vissza.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_config_empty()`

```python
def mock_config_empty(self) -> MagicMock
```

Mock config létrehozása üres configgal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `live_feed_empty_config()`

```python
def live_feed_empty_config(self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config_empty: MagicMock) -> JForexLiveFeed
```

JForexLiveFeed példány létrehozása üres configgal.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_config_empty`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `JForexLiveFeed`

#### `test_init_with_empty_config_logs_warning()`

```python
def test_init_with_empty_config_logs_warning(self, live_feed_empty_config: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy üres config esetén warning log jelenik meg.

**Paraméterek:**

- **`self`**
- **`live_feed_empty_config`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_config_with_data()`

```python
def mock_config_with_data(self) -> MagicMock
```

Mock config létrehozása config adatokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_get()`

```python
def mock_get(section, key = None)
```

**Paraméterek:**

- **`section`**
- **`key`** = `None`

#### `live_feed_with_config()`

```python
def live_feed_with_config(self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config_with_data: MagicMock) -> JForexLiveFeed
```

JForexLiveFeed példány létrehozása config adatokkal.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_config_with_data`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `JForexLiveFeed`

#### `test_init_with_config_logs_debug()`

```python
def test_init_with_config_logs_debug(self, live_feed_with_config: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy config adatok esetén debug log jelenik meg.

**Paraméterek:**

- **`self`**
- **`live_feed_with_config`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_raises_exception_on_zmq_failure()`

```python
async def test_start_raises_exception_on_zmq_failure(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy start exception-t dob ZMQ hiba esetén.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_listen_loop_handles_socket_none()`

```python
async def test_listen_loop_handles_socket_none(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy listen loop kezeli, ha socket None.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/collectors/jforex/test_live_feed.py`](../../tests/neural_ai/collectors/jforex/test_live_feed.py)
