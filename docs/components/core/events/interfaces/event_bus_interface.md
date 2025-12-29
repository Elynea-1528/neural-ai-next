# core/events/interfaces/event_bus_interface.py

EventBus interfész a Neural AI Next rendszerhez.

Ez a modul definiálja az EventBus interfészt, amely biztosítja
az eseményvezérelt architektúra alapjait.

Author: Neural AI Next Team
Version: 1.0.0

## Osztályok

### `EventBusConfig`

EventBus konfiguráció.

    Attributes:
        zmq_context: ZeroMQ kontextus (opcionális, létrejön ha nincs megadva)
        pub_port: Publisher port (alapértelmezett: 5555)
        sub_port: Subscriber port (alapértelmezett: 5556)
        use_inproc: Használjon inproc transportot teszteléshez (alapértelmezett: False)

### `EventBusInterface`

EventBus interfész.

    Ez az interfész definiálja az eseménybusz alapvető műveleteit:
    - Események közzététele
    - Feliratkozás eseményekre
    - Leiratkozás eseményekről
    - Bus indítása és leállítása


## Függvények

### `config`

Visszaadja az EventBus konfigurációját.

        Returns:
            Az EventBus konfigurációja

### `start`

Elindítja az EventBus-t és létrehozza a socketeket.

### `stop`

Leállítja az EventBus-t és felszabadítja az erőforrásokat.

### `publish`

Esemény közzététele a buszon.

        Args:
            event_type: Az esemény típusa (pl. 'market_data', 'trade')
            event: Az esemény objektum (Pydantic BaseModel)

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

### `run_forever`

Eseménybusz örök futás (blokkoló).

        Ez a metódus egy végtelen ciklusban fogadja az eseményeket
        és továbbítja azokat a feliratkozóknak.

        Note:
            Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd


---

**Forrásfájl:** [`core/events/interfaces/event_bus_interface.py`](../../../neural_ai/core/events/interfaces/event_bus_interface.py)
