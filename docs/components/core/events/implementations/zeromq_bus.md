# core/events/implementations/zeromq_bus.py

EventBus implementáció ZeroMQ-val és asyncio-val.

Ez a modul biztosítja az eseményvezérelt architektúra magját, lehetővé téve
a komponensek közötti laza csatolást Pub/Sub mintázattal.

Author: Neural AI Next Team
Version: 1.0.0

## Osztályok

### `EventBus`

ZeroMQ alapú aszinkron eseménybusz.

    Ez az osztály biztosítja az események közzétételét és feliratkozást
    a rendszer különböző komponensei számára. A ZeroMQ PUB/SUB mintázatot használja.

    A specifikációban említett asyncio.Queue-s megvalósítás helyett egyből
    ZeroMQ-t használunk a teljesítmény és a skálázhatóság érdekében.

    Attributes:
        config: Az EventBus konfigurációja
        _context: ZeroMQ kontextus
        _publisher: Publisher socket
        _subscribers: Feliratkozók szótára event_type -> callback lista
        _running: Futási állapot jelzője


## Függvények

### `config`

Visszaadja az EventBus konfigurációját.

### `__init__`

Inicializálja az EventBus-t.

        Args:
            config: EventBus konfiguráció (opcionális)

### `start`

Elindítja az EventBus-t és létrehozza a socketeket.

### `stop`

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

### `publish`

Esemény közzététele a buszon.

        Args:
            event_type: Az esemény típusa (pl. 'market_data', 'trade')
            event: Az esemény objektum (Pydantic BaseModel) VAGY események listája

        Raises:
            EventBusError: Ha az EventBus nincs elindítva
            PublishError: Ha a publisher socket nincs inicializálva

### `subscribe`

Feliratkozás eseménytípusra.

        Args:
            event_type: Az esemény típusa, amire feliratkozunk
            callback: A callback függvény, amely az eseményt fogadja

        Note:
            A callback-nek aszinkronnak kell lennie (async def)

### `unsubscribe`

Leiratkozás eseménytípusról.

        Args:
            event_type: Az esemény típusa
            callback: A callback függvény, amelyet eltávolítunk

### `_dispatch_event`

Esemény továbbítása a feliratkozóknak.

        Args:
            event_type: Az esemény típusa
            event_data: Az esemény adatai

### `_deserialize_event`

Deserializálja az eseményt a megfelelő Pydantic modellbe.

        Args:
            event_type: Az esemény típusa
            event_data: Az esemény adatai

        Returns:
            A deserializált esemény objektum vagy None ha hiba történt

### `run_forever`

Eseménybusz örök futás (blokkoló).

        Ez a metódus egy végtelen ciklusban fogadja az eseményeket
        és továbbítja azokat a feliratkozóknak.

        Note:
            Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd

### `__aenter__`

Aszinkron context manager.

        Returns:
            Az EventBus példány

### `__aexit__`

Aszinkron context manager lezárás.

        Args:
            exc_type: A kivétel típusa (ha volt kivétel)
            exc_val: A kivétel objektum (ha volt kivétel)
            exc_tb: A traceback objektum (ha volt kivétel)


---

**Forrásfájl:** [`core/events/implementations/zeromq_bus.py`](../../../neural_ai/core/events/implementations/zeromq_bus.py)
