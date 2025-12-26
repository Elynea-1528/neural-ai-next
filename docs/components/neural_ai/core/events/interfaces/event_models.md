# Esemény Modellek

## Áttekintés

Ez a modul definiálja az összes eseménytípust, amelyek az EventBus-on keresztül áramlanak a rendszerben. Minden esemény Pydantic BaseModel-ből származik, biztosítva a típusbiztosságot és a validációt.

## Esemény Típusok

### `EventType`

Eseménytípusok enumerációja.

```python
class EventType(str, Enum):
    """Eseménytípusok enumerációja."""
    
    MARKET_DATA = "market_data"
    TRADE = "trade"
    SIGNAL = "signal"
    SYSTEM_LOG = "system_log"
    ORDER = "order"
    POSITION = "position"
```

**Értékek:**
- `MARKET_DATA`: Piaci adat események
- `TRADE`: Kereskedési események
- `SIGNAL`: Jelzés események
- `SYSTEM_LOG`: Rendszer log események
- `ORDER`: Rendelés események
- `POSITION`: Pozíció események

**Használat:**

```python
from neural_ai.core.events.interfaces.event_models import EventType

# Esemény típusok elérése
print(EventType.MARKET_DATA)  # market_data
print(EventType.TRADE)        # trade
print(EventType.SIGNAL)       # signal
```

## Esemény Osztályok

### `MarketDataEvent`

Piaci adat esemény. Ez az esemény akkor jön létre, amikor új piaci adat érkezik a collectoroktól (JForex, MT5, IBKR).

```python
class MarketDataEvent(BaseModel):
    """Piaci adat esemény.
    
    Ez az esemény akkor jön létre, amikor új piaci adat érkezik
    a collectoroktól (JForex, MT5, IBKR).
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    bid: float = Field(..., description="A bid ár", gt=0)
    ask: float = Field(..., description="Az ask ár", gt=0)
    volume: int | None = Field(None, description="A volumen", ge=0)
    source: str = Field(..., description="Az adat forrása")
```

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma (pl. 'EURUSD')
- `timestamp` (datetime): Az esemény időbélyege
- `bid` (float): A bid ár (nagyobb mint 0)
- `ask` (float): Az ask ár (nagyobb mint 0)
- `volume` (int | None): A volumen (opcionális, nagyobb vagy egyenlő mint 0)
- `source` (str): Az adat forrása ('jforex', 'mt5', 'ibkr')

**Validáció:**
- A `source` értéke csak a következők közül választható: 'jforex', 'mt5', 'ibkr'

**Példa:**

```python
from datetime import datetime, UTC

event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    bid=1.0850,
    ask=1.0852,
    volume=1000000,
    source="mt5"
)
```

### `TradeEvent`

Kereskedési esemény. Ez az esemény akkor jön létre, amikor egy kereskedés végrehajtódik.

```python
class TradeEvent(BaseModel):
    """Kereskedési esemény.
    
    Ez az esemény akkor jön létre, amikor egy kereskedés végrehajtódik.
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="A kereskedés időbélyege")
    direction: str = Field(..., description="A kereskedés iránya")
    price: float = Field(..., description="A végrehajtási ár", gt=0)
    volume: float = Field(..., description="A kereskedés volumene", gt=0)
    order_id: str = Field(..., description="A rendelés egyedi azonosítója")
    strategy_id: str | None = Field(None, description="A stratégiát azonosító ID")
```

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma
- `timestamp` (datetime): A kereskedés időbélyege
- `direction` (str): A kereskedés iránya ('BUY' vagy 'SELL')
- `price` (float): A végrehajtási ár (nagyobb mint 0)
- `volume` (float): A kereskedés volumene lotban (nagyobb mint 0)
- `order_id` (str): A rendelés egyedi azonosítója
- `strategy_id` (str | None): A stratégiát azonosító ID (opcionális)

**Validáció:**
- A `direction` értéke csak 'BUY' vagy 'SELL' lehet

**Példa:**

```python
event = TradeEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    direction="BUY",
    price=1.0851,
    volume=0.01,
    order_id="ORD-12345",
    strategy_id="STRAT-001"
)
```

### `SignalEvent`

Jelzés esemény. Ez az esemény akkor jön létre, amikor a Strategy Engine jelzést generál.

```python
class SignalEvent(BaseModel):
    """Jelzés esemény.
    
    Ez az esemény akkor jön létre, amikor a Strategy Engine jelzést generál.
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="A jelzés időbélyege")
    signal_type: str = Field(..., description="A jelzés típusa")
    confidence: float = Field(..., description="A jelzés megbízhatósága", ge=0.0, le=1.0)
    strategy_id: str = Field(..., description="A stratégiát azonosító ID")
    price: float | None = Field(None, description="Az aktuális ár", gt=0)
    target_price: float | None = Field(None, description="A célár", gt=0)
    stop_loss: float | None = Field(None, description="Stop loss ár", gt=0)
```

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma
- `timestamp` (datetime): A jelzés időbélyege
- `signal_type` (str): A jelzés típusa
- `confidence` (float): A jelzés megbízhatósága (0.0 - 1.0 között)
- `strategy_id` (str): A stratégiát azonosító ID
- `price` (float | None): Az aktuális ár (opcionális)
- `target_price` (float | None): A célár (opcionális)
- `stop_loss` (float | None): Stop loss ár (opcionális)

**Validáció:**
- A `signal_type` értéke csak a következők közül választható: 'ENTRY_LONG', 'ENTRY_SHORT', 'EXIT_LONG', 'EXIT_SHORT', 'CLOSE_POSITION', 'REVERSE_POSITION'
- A `confidence` értéke 0.0 és 1.0 között kell legyen

**Példa:**

```python
event = SignalEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    signal_type="ENTRY_LONG",
    confidence=0.85,
    strategy_id="STRAT-001",
    price=1.0850,
    target_price=1.0900,
    stop_loss=1.0800
)
```

### `SystemLogEvent`

Rendszer log esemény. Ez az esemény a rendszer különböző komponenseinek log üzeneteit tartalmazza.

```python
class SystemLogEvent(BaseModel):
    """Rendszer log esemény.
    
    Ez az esemény a rendszer különböző komponenseinek log üzeneteit tartalmazza.
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    timestamp: datetime = Field(..., description="A log időbélyege")
    level: str = Field(..., description="A log szintje")
    component: str = Field(..., description="A komponens neve")
    message: str = Field(..., description="A log üzenet")
    extra_data: dict[str, Any] | None = Field(None, description="További adatok")
```

**Attribútumok:**
- `timestamp` (datetime): A log időbélyege
- `level` (str): A log szintje ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
- `component` (str): A komponens neve, amely generálta a logot
- `message` (str): A log üzenet
- `extra_data` (dict[str, Any] | None): További adatok (opcionális)

**Validáció:**
- A `level` értéke csak a következők közül választható: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

**Példa:**

```python
event = SystemLogEvent(
    timestamp=datetime.now(UTC),
    level="INFO",
    component="DataCollector",
    message="Sikeres adatgyűjtés MT5-ről",
    extra_data={"symbol": "EURUSD", "count": 100}
)
```

### `OrderEvent`

Rendelés esemény. Ez az esemény akkor jön létre, amikor új rendelést helyezünk vagy egy létező rendelés állapota megváltozik.

```python
class OrderEvent(BaseModel):
    """Rendelés esemény.
    
    Ez az esemény akkor jön létre, amikor új rendelést helyezünk vagy
    egy létező rendelés állapota megváltozik.
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    order_id: str = Field(..., description="A rendelés egyedi azonosítója")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    order_type: str = Field(..., description="A rendelés típusa")
    direction: str = Field(..., description="A rendelés iránya")
    volume: float = Field(..., description="A rendelés volumene", gt=0)
    price: float | None = Field(None, description="A rendelés ára", gt=0)
    status: str = Field(..., description="A rendelés állapota")
```

**Attribútumok:**
- `order_id` (str): A rendelés egyedi azonosítója
- `timestamp` (datetime): Az esemény időbélyege
- `symbol` (str): A pénzpár szimbóluma
- `order_type` (str): A rendelés típusa ('MARKET', 'LIMIT', 'STOP')
- `direction` (str): A rendelés iránya ('BUY' vagy 'SELL')
- `volume` (float): A rendelés volumene (nagyobb mint 0)
- `price` (float | None): A rendelés ára (opcionális limit/stop rendeléseknél)
- `status` (str): A rendelés állapota ('PENDING', 'FILLED', 'CANCELLED', 'REJECTED')

**Validáció:**
- A `order_type` értéke csak 'MARKET', 'LIMIT' vagy 'STOP' lehet
- A `direction` értéke csak 'BUY' vagy 'SELL' lehet
- A `status` értéke csak 'PENDING', 'FILLED', 'CANCELLED' vagy 'REJECTED' lehet

**Példa:**

```python
event = OrderEvent(
    order_id="ORD-12345",
    timestamp=datetime.now(UTC),
    symbol="EURUSD",
    order_type="MARKET",
    direction="BUY",
    volume=0.01,
    price=None,
    status="FILLED"
)
```

### `PositionEvent`

Pozíció esemény. Ez az esemény akkor jön létre, amikor pozíció nyílik vagy zárul.

```python
class PositionEvent(BaseModel):
    """Pozíció esemény.
    
    Ez az esemény akkor jön létre, amikor pozíció nyílik vagy zárul.
    """
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    position_id: str = Field(..., description="A pozíció egyedi azonosítója")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    direction: str = Field(..., description="A pozíció iránya")
    volume: float = Field(..., description="A pozíció volumene", gt=0)
    entry_price: float = Field(..., description="A belépési ár", gt=0)
    current_price: float = Field(..., description="Az aktuális ár", gt=0)
    profit_loss: float | None = Field(None, description="A nyereség/veszteség")
    status: str = Field(..., description="A pozíció állapota")
```

**Attribútumok:**
- `position_id` (str): A pozíció egyedi azonosítója
- `timestamp` (datetime): Az esemény időbélyege
- `symbol` (str): A pénzpár szimbóluma
- `direction` (str): A pozíció iránya ('LONG' vagy 'SHORT')
- `volume` (float): A pozíció volumene (nagyobb mint 0)
- `entry_price` (float): A belépési ár (nagyobb mint 0)
- `current_price` (float): Az aktuális ár (nagyobb mint 0)
- `profit_loss` (float | None): A nyereség/veszteség (opcionális)
- `status` (str): A pozíció állapota ('OPEN' vagy 'CLOSED')

**Validáció:**
- A `direction` értéke csak 'LONG' vagy 'SHORT' lehet
- A `status` értéke csak 'OPEN' vagy 'CLOSED' lehet

**Példa:**

```python
event = PositionEvent(
    position_id="POS-67890",
    timestamp=datetime.now(UTC),
    symbol="EURUSD",
    direction="LONG",
    volume=0.01,
    entry_price=1.0850,
    current_price=1.0860,
    profit_loss=10.0,
    status="OPEN"
)
```

## Komplex példa: Események létrehozása és kezelése

```python
import asyncio
from datetime import datetime, UTC
from neural_ai.core.events import EventBusFactory, EventType
from neural_ai.core.events.interfaces.event_models import (
    MarketDataEvent,
    TradeEvent,
    SignalEvent,
    SystemLogEvent,
    OrderEvent,
    PositionEvent
)

async def handle_market_data(event: MarketDataEvent):
    print(f"Piaci adat: {event.symbol} - Bid: {event.bid}, Ask: {event.ask}")

async def handle_trade(event: TradeEvent):
    print(f"Kereskedés: {event.symbol} - {event.direction} - Ár: {event.price}")

async def handle_signal(event: SignalEvent):
    print(f"Jelzés: {event.signal_type} - Megbízhatóság: {event.confidence}")

async def main():
    # EventBus létrehozása
    event_bus = await EventBusFactory.create_and_start()
    
    # Feliratkozások
    event_bus.subscribe(EventType.MARKET_DATA.value, handle_market_data)
    event_bus.subscribe(EventType.TRADE.value, handle_trade)
    event_bus.subscribe(EventType.SIGNAL.value, handle_signal)
    
    # Események létrehozása
    market_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        bid=1.0850,
        ask=1.0852,
        source="mt5"
    )
    
    trade_event = TradeEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        direction="BUY",
        price=1.0851,
        volume=0.01,
        order_id="ORD-12345"
    )
    
    signal_event = SignalEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        signal_type="ENTRY_LONG",
        confidence=0.85,
        strategy_id="STRAT-001"
    )
    
    # Események közzététele
    await event_bus.publish(EventType.MARKET_DATA.value, market_event)
    await event_bus.publish(EventType.TRADE.value, trade_event)
    await event_bus.publish(EventType.SIGNAL.value, signal_event)
    
    # Várakozás a feldolgozásra
    await asyncio.sleep(1)
    
    # Leállítás
    await event_bus.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Validáció és hibakezelés

Mivel minden esemény Pydantic modell, automatikus validáció történik:

```python
try:
    # Érvénytelen piaci adat (negatív ár)
    invalid_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        bid=-1.0,  # Hiba: negatív ár
        ask=1.0852,
        source="mt5"
    )
except ValueError as e:
    print(f"Validációs hiba: {e}")

try:
    # Érvénytelen forrás
    invalid_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        bid=1.0850,
        ask=1.0852,
        source="invalid_source"  # Hiba: érvénytelen forrás
    )
except ValueError as e:
    print(f"Validációs hiba: {e}")
```

## További információk

- [Events Interfészek Áttekintés](__init__.md)
- [Events Modul](../__init__.md)
- [EventBus Implementáció](../implementations/zeromq_bus.md)