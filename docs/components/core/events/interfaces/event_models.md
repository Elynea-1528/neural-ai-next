# core/events/interfaces/event_models.py

Esemény modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes eseménytípust, amelyek az EventBus-on keresztül
áramlanak a rendszerben. Minden esemény Pydantic BaseModel-ből származik,
biztosítva a típusbiztosságot és a validációt.

Author: Neural AI Next Team
Version: 1.0.0

## Osztályok

### `EventType`

Eseménytípusok enumerációja.

### `MarketDataEvent`

Piaci adat esemény.

    Ez az esemény akkor jön létre, amikor új piaci adat érkezik
    a collectoroktól (JForex, MT5, IBKR).

    Attributes:
        symbol: A pénzpár szimbóluma (pl. 'EURUSD')
        timestamp: Az esemény időbélyege
        bid: A bid ár
        ask: Az ask ár
        volume: A volumen (opcionális)
        source: Az adat forrása ('jforex', 'mt5', 'ibkr')

### `TradeEvent`

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

### `SignalEvent`

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

### `SystemLogEvent`

Rendszer log esemény.

    Ez az esemény a rendszer különböző komponenseinek log üzeneteit tartalmazza.

    Attributes:
        timestamp: A log időbélyege
        level: A log szintje ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        component: A komponens neve, amely generálta a logot
        message: A log üzenet
        extra_data: További adatok (opcionális)

### `OrderEvent`

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

### `PositionEvent`

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


## Függvények

### `validate_source`

Validálja a forrást.

### `validate_direction`

Validálja a pozíció irányát.

### `validate_signal_type`

Validálja a jelzés típusát.

### `validate_level`

Validálja a log szintjét.

### `validate_order_type`

Validálja a rendelés típusát.

### `validate_status`

Validálja a pozíció állapotát.


---

**Forrásfájl:** [`core/events/interfaces/event_models.py`](../../../neural_ai/core/events/interfaces/event_models.py)
