# neural_ai/core/events/interfaces/event_models.py

Esemény modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes eseménytípust, amelyek az EventBus-on keresztül
áramlanak a rendszerben. Minden esemény Pydantic BaseModel-ből származik,
biztosítva a típusbiztosságot és a validációt.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
```

## Osztály: `EventType(str, Enum)`

Eseménytípusok enumerációja.

## Osztály: `MarketDataEvent(BaseModel)`

Piaci adat esemény.

Ez az esemény akkor jön létre, amikor új piaci adat érkezik
a collectoroktól (JForex, MT5, IBKR).

Attributes:
    symbol: A pénzpár szimbóluma (pl. 'EURUSD')
    timestamp: Az esemény időbélyege
    bid: A bid ár
    ask: Az ask ár
    volume: A volumen (opcionális, kompatibilitás miatt)
    ask_volume: Ask volumen (opcionális)
    bid_volume: Bid volumen (opcionális)
    source: Az adat forrása ('jforex', 'mt5', 'ibkr')

### Metódusok

#### `validate_source()`

```python
def validate_source(cls, v: str) -> str
```

Validálja a forrást.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `TradeEvent(BaseModel)`

Kereskedési esemény.

Ez az esemény akkor jön létre, amikor egy kereskedés végrehajtódik.

Attributes:
    symbol: A pénzpár szimbóluma
    timestamp: A kereskedés időbélyege
    direction: A kereskedés iránya ('BUY' vagy 'SELL')
    price: A végrehajtási ár
    volume: A kereskedés volumene (lotban)
    order_id: A rendelés egyedi azonosítója
    strategy_id: A stratégiát azonosító ID (opcionális)

### Metódusok

#### `validate_direction()`

```python
def validate_direction(cls, v: str) -> str
```

Validálja a kereskedés irányát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `SignalEvent(BaseModel)`

Jelzés esemény.

Ez az esemény akkor jön létre, amikor a Strategy Engine jelzést generál.

Attributes:
    symbol: A pénzpár szimbóluma
    timestamp: A jelzés időbélyege
    signal_type: A jelzés típusa (pl. 'ENTRY_LONG', 'EXIT_SHORT')
    confidence: A jelzés megbízhatósága (0.0 - 1.0)
    strategy_id: A stratégiát azonosító ID
    price: Az aktuális ár (opcionális)
    target_price: A célár (opcionális)
    stop_loss: Stop loss ár (opcionális)

### Metódusok

#### `validate_signal_type()`

```python
def validate_signal_type(cls, v: str) -> str
```

Validálja a jelzés típusát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `SystemLogEvent(BaseModel)`

Rendszer log esemény.

Ez az esemény a rendszer különböző komponenseinek log üzeneteit tartalmazza.

Attributes:
    timestamp: A log időbélyege
    level: A log szintje ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    component: A komponens neve, amely generálta a logot
    message: A log üzenet
    extra_data: További adatok (opcionális)

### Metódusok

#### `validate_level()`

```python
def validate_level(cls, v: str) -> str
```

Validálja a log szintjét.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `OrderEvent(BaseModel)`

Rendelés esemény.

Ez az esemény akkor jön létre, amikor új rendelést helyezünk vagy
egy létező rendelés állapota megváltozik.

Attributes:
    order_id: A rendelés egyedi azonosítója
    timestamp: Az esemény időbélyege
    symbol: A pénzpár szimbóluma
    order_type: A rendelés típusa ('MARKET', 'LIMIT', 'STOP')
    direction: A rendelés iránya ('BUY' vagy 'SELL')
    volume: A rendelés volumene
    price: A rendelés ára (opcionális limit/stop rendeléseknél)
    status: A rendelés állapota ('PENDING', 'FILLED', 'CANCELLED', 'REJECTED')

### Metódusok

#### `validate_order_type()`

```python
def validate_order_type(cls, v: str) -> str
```

Validálja a rendelés típusát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

#### `validate_direction()`

```python
def validate_direction(cls, v: str) -> str
```

Validálja a rendelés irányát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

#### `validate_status()`

```python
def validate_status(cls, v: str) -> str
```

Validálja a rendelés állapotát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `PositionEvent(BaseModel)`

Pozíció esemény.

Ez az esemény akkor jön létre, amikor pozíció nyílik vagy zárul.

Attributes:
    position_id: A pozíció egyedi azonosítója
    timestamp: Az esemény időbélyege
    symbol: A pénzpár szimbóluma
    direction: A pozíció iránya ('LONG' vagy 'SHORT')
    volume: A pozíció volumene
    entry_price: A belépési ár
    current_price: Az aktuális ár
    profit_loss: A nyereség/veszteség (opcionális)
    status: A pozíció állapota ('OPEN', 'CLOSED')

### Metódusok

#### `validate_direction()`

```python
def validate_direction(cls, v: str) -> str
```

Validálja a pozíció irányát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

#### `validate_status()`

```python
def validate_status(cls, v: str) -> str
```

Validálja a pozíció állapotát.

**Paraméterek:**

- **`cls`**
- **`v`** (`str`)

**Visszatérési érték:**

- Típus: `str`

---

**Forrásfájl:** [`neural_ai/core/events/interfaces/event_models.py`](../../neural_ai/core/events/interfaces/event_models.py)
