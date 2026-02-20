# tests/neural_ai/collectors/jforex/test_live_feed_integration.py

JForex Live Feed Integration Tests.

Ez a modul tartalmazza a JForexLiveFeed integrációs tesztjeit.
A tesztek a valós JForexLiveFeed logikát használják, de a ZMQ socketet mock-olják.

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

## Osztály: `TestJForexLiveFeedIntegration`

JForexLiveFeed integrációs tesztjei.

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

JForexLiveFeed példány létrehozása (VALÓS, NEM mock).

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_config`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `JForexLiveFeed`

#### `test_valid_json_creates_market_data_event()`

```python
async def test_valid_json_creates_market_data_event(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock) -> None
```

Teszteli, hogy érvényes JSON input MarketDataEvent-et hoz létre.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_invalid_json_handles_gracefully()`

```python
async def test_invalid_json_handles_gracefully(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy hibás JSON string gracefully kezelődik.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_recv()`

```python
async def mock_recv()
```

#### `test_missing_required_fields()`

```python
async def test_missing_required_fields(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock) -> None
```

Teszteli, hogy hiányzó kötelező mezők esetén error log történik.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_negative_bid_price()`

```python
async def test_negative_bid_price(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock) -> None
```

Teszteli, hogy negatív bid ár Pydantic validáció hibát okoz.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_multiple_ticks_sequential()`

```python
async def test_multiple_ticks_sequential(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock) -> None
```

Teszteli, hogy több tick egymás után feldolgozható.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_zmq_socket_mock_full_flow()`

```python
async def test_zmq_socket_mock_full_flow(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock) -> None
```

Teszteli a teljes flowt: ZMQ context → socket → recv_string → MarketDataEvent.

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

#### `test_reconnect_on_socket_error()`

```python
async def test_reconnect_on_socket_error(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None
```

Teszteli, hogy socket ZMQError esetén a listen loop nem crashel, hanem logol.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_recv()`

```python
async def mock_recv()
```

#### `test_event_bus_publish_called_with_correct_topic()`

```python
async def test_event_bus_publish_called_with_correct_topic(self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock) -> None
```

Teszteli, hogy az event bus publish mindig 'market_data' topickal hívódik.

**Paraméterek:**

- **`self`**
- **`live_feed`** (`JForexLiveFeed`)
- **`mock_event_bus`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/collectors/jforex/test_live_feed_integration.py`](../../tests/neural_ai/collectors/jforex/test_live_feed_integration.py)
