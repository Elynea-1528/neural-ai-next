# 🧪 Teszt: tests/neural_ai/core/events/interfaces/test_event_models.py

**Tesztelt modul:** [`neural_ai/core/events/interfaces/event_models.py`](../../neural_ai/core/events/interfaces/event_models.py)

Tesztek az EventModel-ekhez.

Ez a modul tartalmazza az összes eseménymodell tesztjeit,
beleértve a validációt és a szerializációt.

Author: Neural AI Next Team
Version: 1.0.0

## Teszt Osztály: `TestEventType`

EventType enumeráció tesztei.

### ✓ `test_event_type_values()`

Teszteli az EventType értékeit.

## Teszt Osztály: `TestMarketDataEvent`

MarketDataEvent tesztek.

### ✓ `test_valid_market_data_event()`

Teszteli az érvényes MarketDataEvent létrehozását.

### ✓ `test_market_data_event_without_volume()`

Teszteli a MarketDataEvent létrehozását volume nélkül.

### ✓ `test_market_data_event_invalid_source()`

Teszteli az érvénytelen forrást.

### ✓ `test_market_data_event_invalid_bid()`

Teszteli az érvénytelen bid értéket.

### ✓ `test_market_data_event_invalid_ask()`

Teszteli az érvénytelen ask értéket.

## Teszt Osztály: `TestTradeEvent`

TradeEvent tesztek.

### ✓ `test_valid_trade_event()`

Teszteli az érvényes TradeEvent létrehozását.

### ✓ `test_trade_event_without_strategy_id()`

Teszteli a TradeEvent létrehozását strategy_id nélkül.

### ✓ `test_trade_event_invalid_direction()`

Teszteli az érvénytelen irányt.

### ✓ `test_trade_event_invalid_price()`

Teszteli az érvénytelen árat.

## Teszt Osztály: `TestSignalEvent`

SignalEvent tesztek.

### ✓ `test_valid_signal_event()`

Teszteli az érvényes SignalEvent létrehozását.

### ✓ `test_signal_event_without_prices()`

Teszteli a SignalEvent létrehozását árak nélkül.

### ✓ `test_signal_event_invalid_signal_type()`

Teszteli az érvénytelen jelzés típust.

### ✓ `test_signal_event_invalid_confidence()`

Teszteli az érvénytelen konfidenciát.

## Teszt Osztály: `TestSystemLogEvent`

SystemLogEvent tesztek.

### ✓ `test_valid_system_log_event()`

Teszteli az érvényes SystemLogEvent létrehozását.

### ✓ `test_system_log_event_without_extra_data()`

Teszteli a SystemLogEvent létrehozását extra_data nélkül.

### ✓ `test_system_log_event_invalid_level()`

Teszteli az érvénytelen log szintet.

## Teszt Osztály: `TestOrderEvent`

OrderEvent tesztek.

### ✓ `test_valid_order_event()`

Teszteli az érvényes OrderEvent létrehozását.

### ✓ `test_order_event_with_price()`

Teszteli az OrderEvent létrehozását árrésztvevővel.

### ✓ `test_order_event_invalid_order_type()`

Teszteli az érvénytelen rendelés típust.

### ✓ `test_order_event_invalid_direction()`

Teszteli az érvénytelen irányt.

### ✓ `test_order_event_invalid_status()`

Teszteli az érvénytelen állapotot.

## Teszt Osztály: `TestPositionEvent`

PositionEvent tesztek.

### ✓ `test_valid_position_event()`

Teszteli az érvényes PositionEvent létrehozását.

### ✓ `test_position_event_without_profit_loss()`

Teszteli a PositionEvent létrehozását profit_loss nélkül.

### ✓ `test_position_event_invalid_direction()`

Teszteli az érvénytelen irányt.

### ✓ `test_position_event_invalid_status()`

Teszteli az érvénytelen állapotot.

---

**Teszt fájl:** [`tests/neural_ai/core/events/interfaces/test_event_models.py`](../../tests/neural_ai/core/events/interfaces/test_event_models.py)

**Tesztelt modul:** [`neural_ai/core/events/interfaces/event_models.py`](../../neural_ai/core/events/interfaces/event_models.py)
