# EventBusFactory - EventBus Gyár Osztály

## Áttekintés

Az `EventBusFactory` osztály felelős az EventBus példányok létrehozásáért a Neural AI Next rendszerben. A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk egyszerű cseréjét.

## Osztály leírása

```python
class EventBusFactory:
    """EventBus factory osztály.
    
    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).
    """
```

## Metódusok

### `create()`

Létrehozza az EventBus példányt.

```python
@staticmethod
def create(config: "EventBusConfig | None" = None) -> "EventBus":
    """Létrehozza az EventBus példányt.

    Args:
        config: EventBus konfiguráció (opcionális)

    Returns:
        EventBus: Az EventBus példány

    Note:
        Jelenleg csak a ZeroMQ-s implementációt támogatja.
    """
```

**Paraméterek:**
- `config` (EventBusConfig | None, opcionális): EventBus konfiguráció

**Visszatérési érték:**
- `EventBus`: Az EventBus példány

**Példa használat:**

```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.implementations.zeromq_bus import EventBusConfig

# Alapértelmezett konfigurációval
event_bus = EventBusFactory.create()

# Egyéni konfigurációval
config = EventBusConfig(
    pub_port=6666,
    sub_port=6667
)
event_bus = EventBusFactory.create(config)
```

### `create_and_start()`

Létrehozza és elindítja az EventBus példányt.

```python
@staticmethod
async def create_and_start(config: "EventBusConfig | None" = None) -> "EventBus":
    """Létrehozza és elindítja az EventBus példányt.

    Args:
        config: EventBus konfiguráció (opcionális)

    Returns:
        EventBus: Az elindított EventBus példány
    """
```

**Paraméterek:**
- `config` (EventBusConfig | None, opcionális): EventBus konfiguráció

**Visszatérési érték:**
- `EventBus`: Az elindított EventBus példány

**Példa használat:**

```python
import asyncio
from neural_ai.core.events.factory import EventBusFactory

async def main():
    # Létrehozás és indítás egy lépésben
    event_bus = await EventBusFactory.create_and_start()
    
    # Használat...
    await event_bus.publish("test_topic", test_event)
    
    # Leállítás
    await event_bus.stop()

asyncio.run(main())
```

## Jelenlegi implementáció

Jelenleg a factory csak a ZeroMQ-s implementációt támogatja:

```python
from neural_ai.core.events.implementations.zeromq_bus import EventBus
```

## Jövőbeli bővíthetőség

A factory mintázat lehetővé teszi a jövőben más implementációk hozzáadását:

- Redis alapú EventBus
- Kafka alapú EventBus
- RabbitMQ alapú EventBus
- Egyéni implementációk

## Kapcsolódó dokumentáció

- [EventBus Implementáció](implementations/zeromq_bus.md)
- [EventBus Konfiguráció](implementations/zeromq_bus.md#eventbusconfig)
- [Events Modul Áttekintés](__init__.md)