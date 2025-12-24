# Esemény Modellek (Events)

## Áttekintés

Az esemény modellek a Neural AI Next rendszer eseményvezérelt architektúrájának alapvető építőkövei. Minden esemény Pydantic BaseModel-ből származik, ami biztosítja a típusbiztosságot, validációt és JSON szerializálást.

## Esemény Típusok

A rendszer a következő eseménytípusokat támogatja:

### EventType Enum

```python
class EventType(str, Enum):
    MARKET_DATA = "market_data"
    TRADE = "trade"
    SIGNAL = "signal"
    SYSTEM_LOG = "system_log"
    ORDER = "order"
    POSITION = "position"
```

## Esemény Osztályok

### MarketDataEvent

Piaci adat esemény, amely akkor jön létre, amikor új piaci adat érkezik a collectoroktól (JForex, MT5, IBKR).

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma (pl. 'EURUSD')
- `timestamp` (datetime): Az esemény időbélyege
- `bid` (float): A bid ár (gt=0)
- `ask` (float): Az ask ár (gt=0)
- `volume` (int | None): A volumen (opcionális, ge=0)
- `source` (str): Az adat forrása ('jforex', 'mt5', 'ibkr')

**Validációk:**
- A `source` csak érvényes források közül választható
- A `bid` és `ask` pozitív számok kell legyenek

**Példa:**
```python
event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0851,
    volume=1000000,
    source="mt5"
)
```

### TradeEvent

Kereskedési esemény, amely akkor jön létre, amikor egy kereskedés végrehajtódik.

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma
- `timestamp` (datetime): A kereskedés időbélyege
- `direction` (str): A kereskedés iránya ('BUY' vagy 'SELL')
- `price` (float): A végrehajtási ár (gt=0)
- `volume` (float): A kereskedés volumene (lotban, gt=0)
- `order_id` (str): A rendelés egyedi azonosítója
- `strategy_id` (str | None): A stratégiát azonosító ID (opcionális)

**Validációk:**
- A `direction` csak 'BUY' vagy 'SELL' lehet
- Az ár és volumen pozitív kell legyen

**Példa:**
```python
event = TradeEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    direction="BUY",
    price=1.0850,
    volume=0.01,
    order_id="order_123",
    strategy_id="momentum_strategy"
)
```

### SignalEvent

Jelzés esemény, amelyet a modellek generálnak kereskedési lehetőségek azonosításához.

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma
- `timestamp` (datetime): A jelzés időbélyege
- `signal_type` (str): A jelzés típusa ('ENTRY_LONG', 'ENTRY_SHORT', 'EXIT_LONG', 'EXIT_SHORT', 'HOLD')
- `confidence` (float): A jelzés megbízhatósága (0.0-1.0, ge=0, le=1)
- `strategy_id` (str): A stratégiát azonosító ID
- `price` (float | None): Az aktuális ár (opcionális, gt=0)
- `target_price` (float | None): A célár (opcionális, gt=0)
- `stop_loss` (float | None): A stop loss ár (opcionális, gt=0)

**Validációk:**
- A `confidence` 0 és 1 között kell legyen
- A `signal_type` csak érvényes típusok közül választható
- Az árak pozitívak kell legyenek

**Példa:**
```python
event = SignalEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    signal_type="ENTRY_LONG",
    confidence=0.85,
    strategy_id="neural_model_v1",
    price=1.0850,
    target_price=1.0900,
    stop_loss=1.0800
)
```

### SystemLogEvent

Rendszer napló esemény, amely a rendszer működéséről szóló információkat tartalmazza.

**Attribútumok:**
- `timestamp` (datetime): A naplóbejegyzés időbélyege
- `level` (str): A naplózási szint ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
- `component` (str): A komponens neve, amely a naplót generálta
- `message` (str): A naplóüzenet
- `extra_data` (dict | None): További adatok (opcionális)

**Validációk:**
- A `level` csak érvényes naplózási szintek közül választható

**Példa:**
```python
event = SystemLogEvent(
    timestamp=datetime.now(timezone.utc),
    level="INFO",
    component="EventBus",
    message="EventBus elindítva",
    extra_data={"port": 5555}
)
```

### OrderEvent

Rendelés esemény, amely a rendelések életciklusát követi nyomon.

**Attribútumok:**
- `order_id` (str): A rendelés egyedi azonosítója
- `timestamp` (datetime): A rendelés időbélyege
- `symbol` (str): A pénzpár szimbóluma
- `order_type` (str): A rendelés típusa ('MARKET', 'LIMIT', 'STOP')
- `direction` (str): A rendelés iránya ('BUY' vagy 'SELL')
- `volume` (float): A rendelés volumene (gt=0)
- `price` (float | None): Az ár (LIMIT/STOP rendeléseknél kötelező, gt=0)
- `status` (str): A rendelés állapota ('PENDING', 'FILLED', 'CANCELLED', 'REJECTED')

**Validációk:**
- A `order_type` csak érvényes típusok közül választható
- A `direction` csak 'BUY' vagy 'SELL' lehet
- A `status` csak érvényes állapotok közül választható
- LIMIT/STOP rendeléseknél a `price` kötelező

**Példa:**
```python
event = OrderEvent(
    order_id="order_456",
    timestamp=datetime.now(timezone.utc),
    symbol="EURUSD",
    order_type="LIMIT",
    direction="BUY",
    volume=0.01,
    price=1.0800,
    status="PENDING"
)
```

### PositionEvent

Pozíció esemény, amely a pozíciók életciklusát követi nyomon.

**Attribútumok:**
- `position_id` (str): A pozíció egyedi azonosítója
- `timestamp` (datetime): A pozíció időbélyege
- `symbol` (str): A pénzpár szimbóluma
- `direction` (str): A pozíció iránya ('LONG' vagy 'SHORT')
- `volume` (float): A pozíció volumene (gt=0)
- `entry_price` (float): A belépési ár (gt=0)
- `current_price` (float): Az aktuális piaci ár (gt=0)
- `profit_loss` (float | None): A nyereség/veszteség (opcionális)
- `status` (str): A pozíció állapota ('OPEN', 'CLOSED', 'PENDING')

**Validációk:**
- A `direction` csak 'LONG' vagy 'SHORT' lehet
- A `status` csak érvényes állapotok közül választható
- Az árak pozitívak kell legyenek

**Példa:**
```python
event = PositionEvent(
    position_id="pos_789",
    timestamp=datetime.now(timezone.utc),
    symbol="EURUSD",
    direction="LONG",
    volume=0.01,
    entry_price=1.0850,
    current_price=1.0860,
    profit_loss=10.0,
    status="OPEN"
)
```

## JSON Szerializálás

Minden esemény automatikusan támogatja a JSON szerializálást a `model_dump()` metódussal:

```python
# Esemény létrehozása
event = MarketDataEvent(...)

# JSON formátumba konvertálás
event_dict = event.model_dump()
json_str = event.model_dump_json()

# Visszanyerés JSON-ból
event = MarketDataEvent.model_validate_json(json_str)
```

## Használat

### Importálás

```python
from neural_ai.core.events.events import (
    EventType,
    MarketDataEvent,
    TradeEvent,
    SignalEvent,
    SystemLogEvent,
    OrderEvent,
    PositionEvent
)
```

### Esemény Létrehozása

```python
from datetime import datetime, timezone

# MarketDataEvent létrehozása
market_event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0851,
    source="mt5"
)

# SignalEvent létrehozása
signal_event = SignalEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    signal_type="ENTRY_LONG",
    confidence=0.85,
    strategy_id="neural_model_v1"
)
```

### Validáció

A Pydantic automatikusan validálja az adatokat:

```python
try:
    event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(timezone.utc),
        bid=-1.0,  # Hiba: negatív ár
        ask=1.0851,
        source="mt5"
    )
except ValidationError as e:
    print(f"Validációs hiba: {e}")
```

## Kapcsolódó Dokumentáció

- [EventBus implementáció](bus.md)
- [System Architecture Spec](../planning/specs/01_system_architecture.md)
- [Pydantic dokumentáció](https://docs.pydantic.dev/)

## Verzió Történet

- **v1.0.0** (2025-12-23): Kezdeti implementáció
  - Mind a 6 alapesemény típus implementálva
  - Teljes validáció és típusbiztonság
  - JSON szerializálás támogatása