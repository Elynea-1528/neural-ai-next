# EventBus Implementációk

## Áttekintés

Ez a csomag tartalmazza az EventBus különböző implementációit.

## Elérhető implementációk

### [`EventBus`](zeromq_bus.md#eventbus)
ZeroMQ alapú aszinkron eseménybusz implementáció.

### [`EventBusConfig`](zeromq_bus.md#eventbusconfig)
EventBus konfigurációs osztály.

## Használat

```python
from neural_ai.core.events.implementations import EventBus, EventBusConfig

# Alapértelmezett konfiguráció
config = EventBusConfig()
event_bus = EventBus(config)

# Egyéni portokkal
config = EventBusConfig(
    pub_port=6666,
    sub_port=6667
)
event_bus = EventBus(config)

# Indítás
await event_bus.start()

# Használat
await event_bus.publish("topic", event)

# Leállítás
await event_bus.stop()
```

## Implementáció részletek

### ZeroMQ EventBus

A jelenlegi implementáció ZeroMQ-t használ PUB/SUB mintázattal:

- **Teljesítmény:** Nagy teljesítményű aszinkron kommunikáció
- **Skálázhatóság:** Támogatja a több előfizetőt
- **Megbízhatóság:** Stabil kommunikáció TCP-n keresztül
- **Tesztelés:** Inproc transport támogatása teszteléshez

## Konfiguráció

```python
@dataclass
class EventBusConfig:
    zmq_context: Optional["zmq.asyncio.Context"] = None
    pub_port: int = 5555
    sub_port: int = 5556
    use_inproc: bool = False
```

## További információk

- [ZeroMQ EventBus Részletes Dokumentáció](zeromq_bus.md)
- [Events Modul Áttekintés](../__init__.md)
- [EventBus Factory](../factory.md)