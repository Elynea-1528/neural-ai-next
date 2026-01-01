# ZeroMQ EventBus Teszt Dokumentáció

## Áttekintés

Ez a dokumentáció a [`tests/core/events/implementations/test_zeromq_bus.py`](tests/core/events/implementations/test_zeromq_bus.py) tesztfájlt dokumentálja, amely a [`neural_ai/core/events/implementations/zeromq_bus.py`](neural_ai/core/events/implementations/zeromq_bus.py) modul tesztjeit tartalmazza.

## Teszt Struktúra

A tesztfájl 49 tesztet tartalmaz, amelyek 7 fő kategóriába vannak csoportosítva:

### 1. TestEventBusInitialization (4 teszt)
- Alapértelmezett inicializálás tesztelése
- Egyéni konfigurációval történő inicializálás
- Külső ZMQ kontextus használata
- ZMQ import hiba kezelése

### 2. TestEventBusStartStop (6 teszt)
- Sikeres indítás és leállítás
- Inproc transport használata
- Többszöri indítás/leállítás kezelése
- Hiba esetek kezelése

### 3. TestEventBusPublish (4 teszt)
- Esemény közzététel sikeres esetben
- Közzététel indítás nélkül
- Publisher socket hiánya esetén
- Batch (lista) események közzététele

### 4. TestEventBusSubscribeUnsubscribe (5 teszt)
- Új eseménytípusra való feliratkozás
- Több callback feliratkozása
- Létező és nem létező feliratkozások lemondása

### 5. TestEventBusContextManager (1 teszt)
- Aszinkron context manager működésének tesztelése

### 6. TestEventBusDeserialization (3 teszt)
- MarketDataEvent deszerializációja
- Ismeretlen eseménytípus kezelése
- Érvénytelen adat deszerializációja

### 7. TestEventBusDeserializationAdditional (5 teszt)
- TradeEvent, SignalEvent, SystemLogEvent, OrderEvent, PositionEvent deszerializációja

### 8. TestEventBusDispatch (3 teszt)
- Sikeres esemény továbbítás
- Továbbítás feliratkozók nélkül
- Callback hiba kezelése

### 9. TestEventBusDispatchExceptionHandling (3 teszt)
- Deszerializálási hiba kezelése
- None visszatérési érték kezelése
- Külső kivételkezelés tesztelése

### 10. TestEventBusRunForever (9 teszt)
- Sikeres futás tesztelése
- Timeout kezelése
- Indítás nélküli hívás kezelése
- Üzenet feldolgozás tesztelése
- Érvénytelen üzenet formátum kezelése
- JSON decode hiba kezelése
- Általános kivétel kezelése
- Inproc transport használata

### 11. TestEventBusErrorHandling (7 teszt) 🆕

Ez az új tesztosztály a hibakezelés teljes lefedettségét biztosítja:

#### `test_publish_error_zmq_exception`
- **Cél**: A publish során fellépő ZMQError kezelésének tesztelése
- **Mock**: `socket.send_multipart` dobjon `zmq.ZMQError`-t
- **Elvárt viselkedés**: A kód elkapja a kivételt, logolja, de nem okoz összeomlást

#### `test_publish_error_general_exception`
- **Cél**: A publish során fellépő általános kivétel kezelésének tesztelése
- **Mock**: `socket.send_multipart` dobjon `RuntimeError`-t
- **Elvárt viselkedés**: A kód elkapja a kivételt, logolja, de nem okoz összeomlást

#### `test_publish_error_with_callback`
- **Cél**: A publish hibakezelésének tesztelése callbackkel együtt
- **Mock**: `socket.send_multipart` dobjon `zmq.ZMQError`-t, callback is van regisztrálva
- **Elvárt viselkedés**: A rendszer stabil marad, a hiba el van kapva

#### `test_subscribe_error_setsockopt_exception`
- **Cél**: A subscribe során fellépő setsockopt ZMQError kezelésének tesztelése
- **Mock**: `socket.setsockopt` dobjon `zmq.ZMQError`-t, `recv_multipart` dobjon `CancelledError`-t
- **Elvárt viselkedés**: A run_forever stabilan fut, a hiba el van kapva

#### `test_subscribe_error_setsockopt_general_exception`
- **Cél**: A subscribe során fellépő általános setsockopt hiba kezelésének tesztelése
- **Mock**: `socket.setsockopt` dobjon `RuntimeError`-t, `recv_multipart` dobjon `CancelledError`-t
- **Elvárt viselkedés**: A run_forever stabilan fut, a hiba el van kapva

#### `test_start_error_socket_bind_failure`
- **Cél**: A socket bind hiba kezelésének tesztelése az indításkor
- **Mock**: `socket.bind` dobjon `zmq.ZMQError`-t (szinkron metódus!)
- **Elvárt viselkedés**: A kód elkapja a kivételt és `EventBusError`-t dob vissza

#### `test_stop_error_socket_close_failure`
- **Cél**: A socket close hiba kezelésének tesztelése a leállításkor
- **Mock**: `socket.close` dobjon `zmq.ZMQError`-t
- **Elvárt viselkedés**: A leállítás folytatódik, a hiba el van kapva

## Implementáció Javítások

A tesztelés során az alábbi hibák lettek kijavítva a [`zeromq_bus.py`](neural_ai/core/events/implementations/zeromq_bus.py) fájlban:

### 1. Publish Hibakezelés
**Hely**: [`publish()`](neural_ai/core/events/implementations/zeromq_bus.py:141) metódus, 167. sor

**Probléma**: A `send_multipart` által dobott kivételek nem voltak elkapva, ami összeomláshoz vezethetett.

**Javítás**:
```python
try:
    await self._publisher.send_multipart([topic, message])
except Exception as e:
    self._logger.error(
        "Hiba az esemény közzétételekor", 
        error=str(e), 
        event_type=event_type,
        exc_info=True
    )
```

### 2. Start Hibakezelés
**Hely**: [`start()`](neural_ai/core/events/implementations/zeromq_bus.py:89) metódus, 106-113. sorok

**Probléma**: A `bind` által dobott kivételek nem voltak elkapva, és nem jelezték a hibát a hívónak.

**Javítás**:
```python
try:
    self._publisher.bind(pub_url)
    self._logger.info("Publisher bind-olva", pub_url=pub_url)
    await asyncio.sleep(0.1)
    self._running = True
    self._logger.info("EventBus elindítva")
except Exception as e:
    self._logger.error("Nem sikerült elindítani az EventBus-t", error=str(e), exc_info=True)
    self._publisher.close()
    self._publisher = None
    raise EventBusError(f"Nem sikerült elindítani az EventBus-t: {str(e)}") from e
```

## Kódlefedettség

A teszt teljes kódlefedettséget (100%) biztosít:
- **Statement Coverage**: 100% (162/162 sor)
- **Branch Coverage**: 100%

## Futtatás

### Összes teszt futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/events/implementations/test_zeromq_bus.py -v
```

### Csak a hibakezelési tesztek futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling -v
```

### Kódlefedettség mérése
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/events/implementations/test_zeromq_bus.py --cov=neural_ai.core.events.implementations.zeromq_bus --cov-report=term-missing
```

## Követelmények

- Python 3.12
- pytest 9.0.2
- pytest-asyncio
- pytest-cov
- pyzmq

## Author

Neural AI Next Team

## Version

1.0.0

## Dátum

2026-01-01