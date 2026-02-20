# tests/neural_ai/core/events/implementations/test_zeromq_bus.py

Tesztek a ZeroMQBus implementációhoz.

Ez a modul tartalmazza a ZeroMQBus tesztjeit, ZMQ mocking-gal.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import asyncio
from datetime import UTC
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core.events.exceptions.event_error import EventBusError
from neural_ai.core.events.exceptions.event_error import PublishError
# ... és még 15 import
```

## Konstansok

- **`original_instances`**
: `getattr(SingletonMeta, '_instances', {}).copy()`


## Osztály: `TestEventBusInitialization`

EventBus inicializálás tesztek.

### Metódusok

#### `test_default_initialization()`

```python
def test_default_initialization(self, mock_context_class: MagicMock) -> None
```

Teszteli az alapértelmezett inicializálást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_custom_config_initialization()`

```python
def test_custom_config_initialization(self, mock_context_class: MagicMock) -> None
```

Teszteli az egyéni konfigurációval történő inicializálást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_external_zmq_context()`

```python
def test_external_zmq_context(self, mock_context_class: MagicMock) -> None
```

Teszteli a külső ZMQ kontextus használatát.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_zmq_import_error()`

```python
def test_zmq_import_error(self, mock_context_class: MagicMock) -> None
```

Teszteli a ZMQ import hibát.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusStartStop`

EventBus indítás és leállítás tesztek.

### Metódusok

#### `test_start_success()`

```python
async def test_start_success(self, mock_context_class: MagicMock) -> None
```

Teszteli a sikeres indítást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_with_inproc()`

```python
async def test_start_with_inproc(self, mock_context_class: MagicMock) -> None
```

Teszteli az indítást inproc transporttal.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_twice()`

```python
async def test_start_twice(self, mock_context_class: MagicMock) -> None
```

Teszteli a többszöri indítást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_success()`

```python
async def test_stop_success(self, mock_context_class: MagicMock) -> None
```

Teszteli a sikeres leállítást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_without_start()`

```python
async def test_stop_without_start(self, mock_context_class: MagicMock) -> None
```

Teszteli a leállítást indítás nélkül.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_twice()`

```python
async def test_stop_twice(self, mock_context_class: MagicMock) -> None
```

Teszteli a többszöri leállítást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusPublish`

EventBus publish tesztek.

### Metódusok

#### `test_publish_success()`

```python
async def test_publish_success(self, mock_context_class: MagicMock) -> None
```

Teszteli a sikeres esemény közzétételt.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_not_started()`

```python
async def test_publish_not_started(self, mock_context_class: MagicMock) -> None
```

Teszteli a közzétételt indítás nélkül.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_no_publisher()`

```python
async def test_publish_no_publisher(self, mock_context_class: MagicMock) -> None
```

Teszteli a közzétételt publisher socket nélkül.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_batch_events()`

```python
async def test_publish_batch_events(self, mock_context_class: MagicMock) -> None
```

Teszteli a batch (lista) események közzétételét.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusSubscribeUnsubscribe`

EventBus feliratkozás és leiratkozás tesztek.

### Metódusok

#### `test_subscribe_new_event_type()`

```python
def test_subscribe_new_event_type(self, mock_context_class: MagicMock) -> None
```

Teszteli az új eseménytípusra való feliratkozást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_subscribe_multiple_callbacks()`

```python
def test_subscribe_multiple_callbacks(self, mock_context_class: MagicMock) -> None
```

Teszteli több callback feliratkozását ugyanarra az eseménytípusra.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_unsubscribe_existing()`

```python
def test_unsubscribe_existing(self, mock_context_class: MagicMock) -> None
```

Teszteli a létező feliratkozás lemondását.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_unsubscribe_non_existing()`

```python
def test_unsubscribe_non_existing(self, mock_context_class: MagicMock) -> None
```

Teszteli a nem létező feliratkozás lemondását.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_unsubscribe_non_existing_event_type()`

```python
def test_unsubscribe_non_existing_event_type(self, mock_context_class: MagicMock) -> None
```

Teszteli a nem létező eseménytípus lemondását.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusContextManager`

EventBus context manager tesztek.

### Metódusok

#### `test_async_context_manager()`

```python
async def test_async_context_manager(self, mock_context_class: MagicMock) -> None
```

Teszteli az aszinkron context managert.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusDeserialization`

EventBus deszerializáció tesztek.

### Metódusok

#### `test_deserialize_market_data()`

```python
def test_deserialize_market_data(self, mock_context_class: MagicMock) -> None
```

Teszteli a MarketDataEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_unknown_event_type()`

```python
def test_deserialize_unknown_event_type(self, mock_context_class: MagicMock) -> None
```

Teszteli az ismeretlen eseménytípus deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_invalid_data()`

```python
def test_deserialize_invalid_data(self, mock_context_class: MagicMock) -> None
```

Teszteli az érvénytelen adat deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusDispatch`

EventBus esemény továbbítás tesztek.

### Metódusok

#### `test_dispatch_event_success()`

```python
async def test_dispatch_event_success(self, mock_context_class: MagicMock) -> None
```

Teszteli a sikeres esemény továbbítást.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dispatch_event_no_subscribers()`

```python
async def test_dispatch_event_no_subscribers(self, mock_context_class: MagicMock) -> None
```

Teszteli az esemény továbbítást feliratkozók nélkül.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dispatch_event_callback_error()`

```python
async def test_dispatch_event_callback_error(self, mock_context_class: MagicMock) -> None
```

Teszteli a callback hibát.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusDeserializationAdditional`

További deszerializáció tesztek a hiányzó sorok lefedésére.

### Metódusok

#### `test_deserialize_trade_event()`

```python
def test_deserialize_trade_event(self, mock_context_class: MagicMock) -> None
```

Teszteli a TradeEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_signal_event()`

```python
def test_deserialize_signal_event(self, mock_context_class: MagicMock) -> None
```

Teszteli a SignalEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_system_log_event()`

```python
def test_deserialize_system_log_event(self, mock_context_class: MagicMock) -> None
```

Teszteli a SystemLogEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_order_event()`

```python
def test_deserialize_order_event(self, mock_context_class: MagicMock) -> None
```

Teszteli a OrderEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_deserialize_position_event()`

```python
def test_deserialize_position_event(self, mock_context_class: MagicMock) -> None
```

Teszteli a PositionEvent deszerializációját.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusDispatchExceptionHandling`

Esemény továbbítás kivételkezelés tesztek.

### Metódusok

#### `test_dispatch_event_deserialization_error()`

```python
async def test_dispatch_event_deserialization_error(self, mock_context_class: MagicMock) -> None
```

Teszteli a deserializálási hiba kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dispatch_event_deserialization_returns_none()`

```python
async def test_dispatch_event_deserialization_returns_none(self, mock_context_class: MagicMock) -> None
```

Teszteli a None visszatérési érték kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dispatch_event_outer_exception_handling()`

```python
async def test_dispatch_event_outer_exception_handling(self, mock_context_class: MagicMock) -> None
```

Teszteli a külső try-except blokk kivételkezelését (219-220. sorok).

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestEventBusRunForever`

EventBus run_forever metódus tesztek.

### Metódusok

#### `test_run_forever_success()`

```python
async def test_run_forever_success(self, mock_context_class: MagicMock) -> None
```

Teszteli a run_forever sikeres futását.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_timeout_handling()`

```python
async def test_run_forever_timeout_handling(self, mock_context_class: MagicMock) -> None
```

Teszteli a timeout kezelését a run_forever-ben.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_not_started()`

```python
async def test_run_forever_not_started(self, mock_context_class: MagicMock) -> None
```

Teszteli a run_forever hívását indítás nélkül.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_run_forever_message_processing()`

```python
async def test_run_forever_message_processing(self, mock_context_class: MagicMock) -> None
```

Teszteli az üzenet feldolgozást a run_forever-ben.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_invalid_message_format()`

```python
async def test_run_forever_invalid_message_format(self, mock_context_class: MagicMock) -> None
```

Teszteli az érvénytelen üzenet formátum kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_json_decode_error()`

```python
async def test_run_forever_json_decode_error(self, mock_context_class: MagicMock) -> None
```

Teszteli a JSON decode hiba kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_general_exception_handling()`

```python
async def test_run_forever_general_exception_handling(self, mock_context_class: MagicMock) -> None
```

Teszteli az általános kivétel kezelését a run_forever-ben.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

#### `test_run_forever_with_inproc()`

```python
async def test_run_forever_with_inproc(self, mock_context_class: MagicMock) -> None
```

Teszteli a run_forever-t inproc transporttal (284. sor lefedése).

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `recv_multipart_side_effect()`

```python
async def recv_multipart_side_effect()
```

## Osztály: `TestEventBusErrorHandling`

EventBus hiba kezelés tesztek a lefedettség növelésére.

### Metódusok

#### `test_publish_error_zmq_exception()`

```python
async def test_publish_error_zmq_exception(self, mock_context_class: MagicMock) -> None
```

Teszteli a publish során fellépő ZMQError kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_error_general_exception()`

```python
async def test_publish_error_general_exception(self, mock_context_class: MagicMock) -> None
```

Teszteli a publish során fellépő általános kivétel kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_publish_error_with_callback()`

```python
async def test_publish_error_with_callback(self, mock_context_class: MagicMock) -> None
```

Teszteli a publish hibakezelését callbackkel együtt.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_subscribe_error_setsockopt_exception()`

```python
async def test_subscribe_error_setsockopt_exception(self, mock_context_class: MagicMock) -> None
```

Teszteli a subscribe során fellépő setsockopt hiba kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_subscribe_error_setsockopt_general_exception()`

```python
async def test_subscribe_error_setsockopt_general_exception(self, mock_context_class: MagicMock) -> None
```

Teszteli a subscribe során fellépő általános setsockopt hiba kezelését.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_error_socket_bind_failure()`

```python
async def test_start_error_socket_bind_failure(self, mock_context_class: MagicMock) -> None
```

Teszteli a socket bind hiba kezelését az indításkor.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_error_socket_close_failure()`

```python
async def test_stop_error_socket_close_failure(self, mock_context_class: MagicMock) -> None
```

Teszteli a socket close hiba kezelését a leállításkor.

**Paraméterek:**

- **`self`**
- **`mock_context_class`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `reset_singleton()`

```python
def reset_singleton()
```

Singleton reset minden teszt előtt.

---

**Forrásfájl:** [`tests/neural_ai/core/events/implementations/test_zeromq_bus.py`](../../tests/neural_ai/core/events/implementations/test_zeromq_bus.py)
