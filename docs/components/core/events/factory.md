# EventBus Factory

## Áttekintés

Az EventBus Factory az eseménybusz létrehozásáért felelős statikus osztály. A factory mintát követve biztosítja az EventBus példányok egységes és konfigurálható létrehozását.

## Osztály

```python
class EventBusFactory
```

## Metódusok

### `create(config: Optional[EventBusConfig] = None) -> EventBusInterface`

Létrehoz egy új EventBus példányt a megadott konfigurációval.

**Paraméterek:**
- `config` (EventBusConfig, opcionális): Az EventBus konfigurációja. Ha nincs megadva, az alapértelmezett konfigurációt használja.

**Visszatérési érték:**
- `EventBusInterface`: Az új EventBus példány

**Példa:**
```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig

# Alapértelmezett konfigurációval
bus = EventBusFactory.create()

# Egyéni konfigurációval
config = EventBusConfig(pub_port=6666, sub_port=6667, use_inproc=True)
bus = EventBusFactory.create(config)
```

### `create_and_start(config: Optional[EventBusConfig] = None) -> EventBusInterface`

Létrehoz egy új EventBus példányt és elindítja azt.

**Paraméterek:**
- `config` (EventBusConfig, opcionális): Az EventBus konfigurációja.

**Visszatérési érték:**
- `EventBusInterface`: Az elindított EventBus példány

**Példa:**
```python
from neural_ai.core.events.factory import EventBusFactory

# Létrehozás és indítás egy lépésben
bus = await EventBusFactory.create_and_start()
```

### `create_from_config(config_manager: ConfigManagerInterface, config_key: str = "events") -> EventBusInterface`

Létrehoz egy EventBus példányt a konfigurációs managerből betöltött beállításokkal.

**Paraméterek:**
- `config_manager` (ConfigManagerInterface): A konfigurációs manager
- `config_key` (str, opcionális): A konfigurációs kulcs (alapértelmezett: "events")

**Visszatérési érték:**
- `EventBusInterface`: Az új EventBus példány

**Példa:**
```python
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.config.factory import ConfigFactory

# Konfigurációs manager létrehozása
config_manager = ConfigFactory.create_yaml_config_manager("configs/events.yaml")

# EventBus létrehozása a konfigurációból
bus = EventBusFactory.create_from_config(config_manager, "events")
```

## Tesztelés

A factory teljes tesztlefedettséggel rendelkezik. A tesztek a következőket ellenőrzik:
- Alapértelmezett EventBus létrehozás
- Egyéni konfigurációval történő létrehozás
- Factory metódusok statikus jellege
- Konfigurációs managerből történő létrehozás
- Hibakezelés érvénytelen konfiguráció esetén

**Tesztfájl:** [`tests/core/events/test_factory.py`](../../../tests/core/events/test_factory.py)

**Coverage:** 100%

## Kapcsolódó dokumentáció

- [EventBus Interface](interfaces/event_bus_interface.md)
- [ZeroMQ EventBus Implementáció](implementations/zeromq_bus.md)
- [Event Modellek](interfaces/event_models.md)
- [Event Kivételek](exceptions/event_error.md)