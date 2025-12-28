# Event Modellek

## Áttekintés

Az Event Modellek Pydantic BaseModel osztályok, amelyek az események adatszerkezetét definiálják. Minden eseménytípushoz tartozik egy dedikált modell, amely biztosítja az adatok validitását és szerializálhatóságát.

## Eseménytípusok

### `EventType` Enum

Az eseménytípusokat definiáló enumeráció.

**Értékek:**
- `MARKET_DATA`: Piaci adatok eseménye
- `TRADE`: Kereskedési esemény
- `SIGNAL`: Jelzés esemény
- `SYSTEM_LOG`: Rendszer napló esemény
- `ORDER`: Rendelés esemény
- `POSITION`: Pozíció esemény

## Esemény Modellek

### `MarketDataEvent`

Piaci adatokat tartalmazó esemény.

**Attribútumok:**
- `symbol` (str): A pénzpár szimbóluma (pl. "EURUSD")
- `timestamp` (datetime): Az esemény időbélyege
- `bid` (float): A vételi ár
- `ask` (float): Az eladási ár
- `source` (str): Az adat forrása (pl. "jforex", "dukascopy")
- `volume` (int, opcionális): A kereskedési volumen

**Validáció:**
- `bid` és `ask` pozitív számok
- `source` nem lehet üres string

**Példa:**
```python
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from datetime import datetime, timezone

event = MarketDataEvent(
    symbol="EURUSD",
    timestamp=datetime.now(timezone.utc),
    bid=1.0850,
    ask=1.0852,
    source="jforex",
    volume=100000
)
```

### `TradeEvent`

Kereskedési esemény.

**Attribútumok:**
- `trade_id` (str): A kereskedés egyedi azonosítója
- `symbol` (str): A pénzpár szimbóluma
- `direction` (str): A kereskedés iránya ("BUY" vagy "SELL")
- `price` (float): A kereskedési ár
- `volume` (float): A kereskedési volumen
- `timestamp` (datetime): Az esemény időbélyege
- `strategy_id` (str, opcionális): A stratégia azonosítója

**Validáció:**
- `direction` csak "BUY" vagy "SELL" lehet
- `price` és `volume` pozitív számok

### `SignalEvent`

Jelzés esemény.

**Attribútumok:**
- `signal_id` (str): A jelzés egyedi azonosítója
- `symbol` (str): A pénzpár szimbóluma
- `signal_type` (str): A jelzés típusa ("LONG", "SHORT", "EXIT")
- `confidence` (float): A jelzés megbízhatósága (0.0-1.0)
- `timestamp` (datetime): Az esemény időbélyege
- `entry_prices` (Optional[Dict[str, float]]): Belépési árak
- `stop_loss` (Optional[float]): Stop loss ár
- `take_profit` (Optional[float]): Take profit ár

**Validáció:**
- `signal_type` csak "LONG", "SHORT" vagy "EXIT" lehet
- `confidence` 0.0 és 1.0 között kell legyen

### `SystemLogEvent`

Rendszer napló esemény.

**Attribútumok:**
- `level` (str): A naplózási szint ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
- `message` (str): A napló üzenet
- `timestamp` (datetime): Az esemény időbélyege
- `component` (str): A komponens neve
- `extra_data` (Optional[Dict[str, Any]]): További adatok

**Validáció:**
- `level` csak a felsorolt értékek egyike lehet

### `OrderEvent`

Rendelés esemény.

**Attribútumok:**
- `order_id` (str): A rendelés egyedi azonosítója
- `symbol` (str): A pénzpár szimbóluma
- `order_type` (str): A rendelés típusa ("MARKET", "LIMIT", "STOP")
- `direction` (str): A rendelés iránya ("BUY" vagy "SELL")
- `volume` (float): A rendelési volumen
- `price` (Optional[float]): A rendelési ár (limit/stop esetén)
- `status` (str): A rendelés állapota ("PENDING", "FILLED", "CANCELLED", "REJECTED")
- `timestamp` (datetime): Az esemény időbélyege

**Validáció:**
- `order_type` és `status` csak a felsorolt értékek egyike lehet

### `PositionEvent`

Pozíció esemény.

**Attribútumok:**
- `position_id` (str): A pozíció egyedi azonosítója
- `symbol` (str): A pénzpár szimbóluma
- `direction` (str): A pozíció iránya ("LONG" vagy "SHORT")
- `volume` (float): A pozíció mérete
- `entry_price` (float): A belépési ár
- `current_price` (float): Az aktuális ár
- `status` (str): A pozíció állapota ("OPEN", "CLOSED", "PENDING")
- `profit_loss` (Optional[float]): A nyereség/veszteség
- `timestamp` (datetime): Az esemény időbélyege

**Validáció:**
- `direction` és `status` csak a felsorolt értékek egyike lehet

## Szerializáció és Deszerializáció

Az események automatikusan szerializálhatók JSON formátumba a `model_dump_json()` metódussal, és deszerializálhatók a `model_validate_json()` metódussal.

**Példa:**
```python
import json
from neural_ai.core.events.interfaces.event_models import MarketDataEvent

# Szerializáció
event = MarketDataEvent(...)
json_data = event.model_dump_json()

# Deszerializáció
event_dict = json.loads(json_data)
restored_event = MarketDataEvent(**event_dict)
```

## Tesztelés

Az összes esemény modell teljes tesztlefedettséggel rendelkezik. A tesztek a következőket ellenőrzik:
- Érvényes adatokkal történő létrehozás
- Hiányzó opcionális mezők kezelése
- Érvénytelen adatokra dobott validációs hibák
- Szerializáció és deszerializáció helyessége

**Tesztfájl:** [`tests/core/events/interfaces/test_event_models.py`](../../../../tests/core/events/interfaces/test_event_models.py)

**Coverage:** 99%

## Kapcsolódó dokumentáció

- [EventBus Interface](event_bus_interface.md)
- [EventBus Factory](../factory.md)
- [ZeroMQ EventBus Implementáció](../implementations/zeromq_bus.md)