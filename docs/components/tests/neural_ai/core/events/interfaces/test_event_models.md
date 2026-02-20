# tests/neural_ai/core/events/interfaces/test_event_models.py

Tesztek az EventModel-ekhez.

Ez a modul tartalmazza az összes eseménymodell tesztjeit,
beleértve a validációt és a szerializációt.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from datetime import UTC
from datetime import datetime
import pytest
from pydantic import ValidationError
from neural_ai.core.events.interfaces.event_models import EventType
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from neural_ai.core.events.interfaces.event_models import OrderEvent
from neural_ai.core.events.interfaces.event_models import PositionEvent
from neural_ai.core.events.interfaces.event_models import SignalEvent
from neural_ai.core.events.interfaces.event_models import SystemLogEvent
# ... és még 1 import
```

## Osztály: `TestEventType`

EventType enumeráció tesztei.

### Metódusok

#### `test_event_type_values()`

```python
def test_event_type_values(self) -> None
```

Teszteli az EventType értékeit.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMarketDataEvent`

MarketDataEvent tesztek.

### Metódusok

#### `test_valid_market_data_event()`

```python
def test_valid_market_data_event(self) -> None
```

Teszteli az érvényes MarketDataEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_market_data_event_without_volume()`

```python
def test_market_data_event_without_volume(self) -> None
```

Teszteli a MarketDataEvent létrehozását volume nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_market_data_event_invalid_source()`

```python
def test_market_data_event_invalid_source(self) -> None
```

Teszteli az érvénytelen forrást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_market_data_event_invalid_bid()`

```python
def test_market_data_event_invalid_bid(self) -> None
```

Teszteli az érvénytelen bid értéket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_market_data_event_invalid_ask()`

```python
def test_market_data_event_invalid_ask(self) -> None
```

Teszteli az érvénytelen ask értéket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestTradeEvent`

TradeEvent tesztek.

### Metódusok

#### `test_valid_trade_event()`

```python
def test_valid_trade_event(self) -> None
```

Teszteli az érvényes TradeEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_trade_event_without_strategy_id()`

```python
def test_trade_event_without_strategy_id(self) -> None
```

Teszteli a TradeEvent létrehozását strategy_id nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_trade_event_invalid_direction()`

```python
def test_trade_event_invalid_direction(self) -> None
```

Teszteli az érvénytelen irányt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_trade_event_invalid_price()`

```python
def test_trade_event_invalid_price(self) -> None
```

Teszteli az érvénytelen árat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestSignalEvent`

SignalEvent tesztek.

### Metódusok

#### `test_valid_signal_event()`

```python
def test_valid_signal_event(self) -> None
```

Teszteli az érvényes SignalEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_signal_event_without_prices()`

```python
def test_signal_event_without_prices(self) -> None
```

Teszteli a SignalEvent létrehozását árak nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_signal_event_invalid_signal_type()`

```python
def test_signal_event_invalid_signal_type(self) -> None
```

Teszteli az érvénytelen jelzés típust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_signal_event_invalid_confidence()`

```python
def test_signal_event_invalid_confidence(self) -> None
```

Teszteli az érvénytelen konfidenciát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestSystemLogEvent`

SystemLogEvent tesztek.

### Metódusok

#### `test_valid_system_log_event()`

```python
def test_valid_system_log_event(self) -> None
```

Teszteli az érvényes SystemLogEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_system_log_event_without_extra_data()`

```python
def test_system_log_event_without_extra_data(self) -> None
```

Teszteli a SystemLogEvent létrehozását extra_data nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_system_log_event_invalid_level()`

```python
def test_system_log_event_invalid_level(self) -> None
```

Teszteli az érvénytelen log szintet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestOrderEvent`

OrderEvent tesztek.

### Metódusok

#### `test_valid_order_event()`

```python
def test_valid_order_event(self) -> None
```

Teszteli az érvényes OrderEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_order_event_with_price()`

```python
def test_order_event_with_price(self) -> None
```

Teszteli az OrderEvent létrehozását árrésztvevővel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_order_event_invalid_order_type()`

```python
def test_order_event_invalid_order_type(self) -> None
```

Teszteli az érvénytelen rendelés típust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_order_event_invalid_direction()`

```python
def test_order_event_invalid_direction(self) -> None
```

Teszteli az érvénytelen irányt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_order_event_invalid_status()`

```python
def test_order_event_invalid_status(self) -> None
```

Teszteli az érvénytelen állapotot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPositionEvent`

PositionEvent tesztek.

### Metódusok

#### `test_valid_position_event()`

```python
def test_valid_position_event(self) -> None
```

Teszteli az érvényes PositionEvent létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_position_event_without_profit_loss()`

```python
def test_position_event_without_profit_loss(self) -> None
```

Teszteli a PositionEvent létrehozását profit_loss nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_position_event_invalid_direction()`

```python
def test_position_event_invalid_direction(self) -> None
```

Teszteli az érvénytelen irányt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_position_event_invalid_status()`

```python
def test_position_event_invalid_status(self) -> None
```

Teszteli az érvénytelen állapotot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/events/interfaces/test_event_models.py`](../../tests/neural_ai/core/events/interfaces/test_event_models.py)
