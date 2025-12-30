# JForexLiveFeed Implementáció

## Áttekintés

A `JForexLiveFeed` osztály a JForex live adatfolyam fogadását implementálja ZMQ (ZeroMQ) socketen keresztül. Ez az implementáció felelős a Java Bridge-el (`NeuralBridgeStrategy`) való kommunikációért, amely valós idejű tick adatokat küld a Python oldalra.

## Architektúra

### Osztálydiagram

```mermaid
classDiagram
    class JForexLiveFeed {
        -LoggerInterface logger
        -EventBusInterface event_bus
        -ConfigManagerInterface config
        -bool _running
        -Socket _socket
        -Context _context
        -Task _listen_task
        -str _host
        -int _tick_port
        -int _command_port
        +start() async
        +stop() async
        +is_running() bool
        -_listen_loop() async
        -_process_tick_data(dict) async
    }
    
    JForexLiveFeed --> ILiveFeed : implements
    JForexLiveFeed --> LoggerInterface : depends on
    JForexLiveFeed --> EventBusInterface : depends on
    JForexLiveFeed --> ConfigManagerInterface : depends on
    JForexLiveFeed --> MarketDataEvent : creates
```

### Függőségek

- **LoggerInterface**: Naplózási műveletekhez
- **EventBusInterface**: Piaci adatok publikálásához
- **ConfigManagerInterface**: Konfiguráció betöltéséhez
- **zmq.asyncio**: Aszinkron ZMQ kommunikációhoz

## Konfiguráció

A `JForexLiveFeed` a következő konfigurációs paramétereket használja a `configs/collectors.yaml` fájlból:

```yaml
jforex_live:
  enabled: true
  host: "127.0.0.1"
  tick_port: 5555
  command_port: 5556
```

### Konfigurációs paraméterek

| Paraméter | Típus | Alapértelmezett | Leírás |
|-----------|-------|-----------------|---------|
| `enabled` | bool | `false` | Engedélyezi-e a live feedet |
| `host` | str | `"127.0.0.1"` | A Java Bridge hoszt címe |
| `tick_port` | int | `5555` | Port a tick adatok fogadásához |
| `command_port` | int | `5556` | Port a parancsok küldéséhez (jelenleg nem használt) |

## Metódusok

### `start()`

Indítja a live adatfolyam fogadását.

**Működés:**
1. Létrehozza a ZMQ contextet
2. Létrehozza a SUB socketet
3. Csatlakozik a Java Bridge-hez (`tcp://{host}:{tick_port}`)
4. Feliratkozik minden üzenetre (`setsockopt_string(zmq.SUBSCRIBE, "")`)
5. Elindítja a háttérfolyamatot (`_listen_loop`)

**Kivételek:**
- `LiveFeedError`: Ha a csatlakozás vagy a fogadás során hiba történik

**Példa:**
```python
await live_feed.start()
```

### `stop()`

Leállítja a live adatfolyam fogadását.

**Működés:**
1. Beállítja a `_running` flaget `False`-ra
2. Leállítja a háttérfolyamatot
3. Lezárja a socketet
4. Lezárja a contextet

**Példa:**
```python
await live_feed.stop()
```

### `is_running()`

Visszaadja, hogy a live feed jelenleg fut-e.

**Visszatérési érték:**
- `bool`: `True`, ha a feed fut, `False` egyébként

**Példa:**
```python
if live_feed.is_running():
    print("Live feed is running")
```

### `_listen_loop()` (privát)

Háttérfolyamat a tickek folyamatos fogadásához.

**Működés:**
1. Végtelen ciklusban vár a ZMQ socketre érkező üzenetekre
2. JSON dekódolja a bejövő üzeneteket
3. Ha az üzenet típusa "TICK", akkor feldolgozza a `_process_tick_data` metódussal
4. Hibák esetén naplózza a hibát és vár 1 másodpercet

### `_process_tick_data(data)` (privát)

Feldolgozza a tick adatokat és publikálja az EventBus-on.

**Paraméterek:**
- `data` (dict): A tick adatok dictionary-ben

**Működés:**
1. Létrehozza a `MarketDataEvent`-et a tick adatokból
2. Publikálja az eseményt az EventBus-on a "market_data" topicra
3. Hibák esetén naplózza a hibát

## Használati példa

```python
from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.core.config.factory import ConfigFactory
from neural_ai.core.events.factory import EventFactory
from neural_ai.core.logger.factory import LoggerFactory

# Komponensek létrehozása
config = ConfigFactory.create_yaml_config_manager("configs")
logger = LoggerFactory.create_default_logger("jforex_live")
event_bus = EventFactory.create_zeromq_bus(config, logger)

# Live feed létrehozása
live_feed = JForexFactory.create_live_feed(
    config=config,
    logger=logger,
    event_bus=event_bus
)

# Live feed indítása
await live_feed.start()

# ... alkalmazás logika ...

# Live feed leállítása
await live_feed.stop()
```

## Üzenet formátum

A Java Bridge a következő JSON formátumban küldi a tick adatokat:

```json
{
  "type": "TICK",
  "symbol": "EURUSD",
  "timestamp": "2025-01-01T12:00:00.000Z",
  "bid": 1.10000,
  "ask": 1.10010,
  "volume": 1000
}
```

### Mezők leírása

| Mező | Típus | Leírás |
|------|-------|---------|
| `type` | str | Üzenet típusa (jelenleg csak "TICK") |
| `symbol` | str | A pénzpár szimbóluma (pl. "EURUSD") |
| `timestamp` | str | Az időbélyeg ISO 8601 formátumban |
| `bid` | float | A bid ár |
| `ask` | float | Az ask ár |
| `volume` | int | A volumen (opcionális) |

## Hibakezelés

A `JForexLiveFeed` robusztus hibakezelést implementál:

1. **Csatlakozási hiba**: Ha a ZMQ socket nem tud csatlakozni, a hiba naplózásra kerül és a feed nem indul el
2. **JSON dekódolási hiba**: Ha egy üzenet érvénytelen JSON-t tartalmaz, a hiba naplózásra kerül és az üzenet figyelmen kívül marad
3. **Tick feldolgozási hiba**: Ha egy tick adat érvénytelen, a hiba naplózásra kerül és az üzenet figyelmen kívül marad
4. **Általános hiba**: Bármely egyéb hiba esetén a rendszer naplózza a hibát és 1 másodpercet vár a következő próbálkozás előtt

## Teljesítmény

- **Késés**: A tickeket valós időben dolgozza fel, a ZMQ alacsony késleltetésű kommunikációt biztosít
- **Memóriahasználat**: Az üzeneteket azonnal feldolgozza és továbbítja, nem tárolja őket
- **Skálázhatóság**: A ZMQ aszinkron működése lehetővé teszi nagy mennyiségű tick feldolgozását

## Biztonság

- **Localhost kommunikáció**: A ZMQ socket csak localhost-on kommunikál (127.0.0.1)
- **SUB socket**: A Python oldal csak fogad, nem küld adatokat a Java Bridge-nek
- **Validáció**: A bejövő tick adatokat validálja a `MarketDataEvent` modell segítségével

## Fejlesztési jegyzetek

- Az osztály teljes egészében aszinkron működik
- A ZMQ context és socket élettartamát az osztály kezeli
- Az EventBus-on történő publikálás nem blokkoló
- A konfigurációból történő betöltés hibatűrő (alapértelmezett értékekkel)

## Kapcsolódó dokumentáció

- [ILiveFeed Interface](interfaces/live_interface.md)
- [JForex Factory](factory.md)
- [MarketDataEvent](../../../core/events/interfaces/event_models.md)
- [EventBus Interface](../../../core/events/interfaces/event_bus_interface.md)