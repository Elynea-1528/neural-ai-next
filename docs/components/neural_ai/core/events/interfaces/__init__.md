# Events Interfészek

## Áttekintés

Ez a csomag tartalmazza az EventBus interfészt és az esemény modelleket.

## Elérhető esemény modellek

### Esemény Típusok
- **[`EventType`](event_models.md#eventtype)**: Eseménytípusok enumerációja

### Esemény Osztályok
- **[`MarketDataEvent`](event_models.md#marketdataevent)**: Piaci adat esemény
- **[`TradeEvent`](event_models.md#tradeevent)**: Kereskedési esemény
- **[`SignalEvent`](event_models.md#signalevent)**: Jelzés esemény
- **[`SystemLogEvent`](event_models.md#systemlogevent)**: Rendszer log esemény
- **[`OrderEvent`](event_models.md#orderevent)**: Rendelés esemény
- **[`PositionEvent`](event_models.md#positionevent)**: Pozíció esemény

## Használat

### Importálás

```python
from neural_ai.core.events.interfaces.event_models import (
    EventType,
    MarketDataEvent,
    TradeEvent,
    SignalEvent,
    SystemLogEvent,
    OrderEvent,
    PositionEvent
)
```

### Esemény létrehozása

```python
from datetime import datetime, UTC

# Piaci adat esemény
market_event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    bid=1.0850,
    ask=1.0852,
    source="mt5"
)

# Kereskedési esemény
trade_event = TradeEvent(
    symbol="EURUSD",
    timestamp=datetime.now(UTC),
    direction="BUY",
    price=1.0851,
    volume=0.01,
    order_id="ORD-12345"
)

# Jelzés esemény
signal_event = SignalEvent(
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

### Esemény közzététele

```python
import asyncio
from neural_ai.core.events import EventBusFactory

async def main():
    event_bus = await EventBusFactory.create_and_start()
    
    # Esemény közzététele
    await event_bus.publish(EventType.MARKET_DATA.value, market_event)
    await event_bus.publish(EventType.TRADE.value, trade_event)
    await event_bus.publish(EventType.SIGNAL.value, signal_event)
    
    await event_bus.stop()

asyncio.run(main())
```

### Esemény fogadása

```python
async def handle_market_data(event: MarketDataEvent):
    """Feldolgozza a piaci adat eseményeket."""
    print(f"Új piaci adat: {event.symbol}")
    print(f"Bid: {event.bid}, Ask: {event.ask}")
    print(f"Forrás: {event.source}")

# Feliratkozás
event_bus.subscribe(EventType.MARKET_DATA.value, handle_market_data)
```

## Esemény típusok

| Esemény Típus | Leírás | Modell |
|--------------|--------|--------|
| `market_data` | Piaci adat frissítések | `MarketDataEvent` |
| `trade` | Kereskedések | `TradeEvent` |
| `signal` | Jelzések a stratégiáktól | `SignalEvent` |
| `system_log` | Rendszer log üzenetek | `SystemLogEvent` |
| `order` | Rendelések | `OrderEvent` |
| `position` | Pozíció változások | `PositionEvent` |

## Validáció

Minden esemény osztály Pydantic BaseModel-ből származik, így automatikus validációval rendelkezik:

```python
# Érvénytelen adatok esetén hiba keletkezik
try:
    invalid_event = MarketDataEvent(
        symbol="EURUSD",
        timestamp=datetime.now(UTC),
        bid=-1.0,  # Érvénytelen: negatív ár
        ask=1.0852,
        source="invalid_source"  # Érvénytelen forrás
    )
except ValueError as e:
    print(f"Validációs hiba: {e}")
```

## További információk

- [Részletes Esemény Modell Dokumentáció](event_models.md)
- [Events Modul Áttekintés](../__init__.md)
- [EventBus Implementáció](../implementations/zeromq_bus.md)