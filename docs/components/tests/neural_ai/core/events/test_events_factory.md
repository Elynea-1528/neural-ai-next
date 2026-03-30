# 🧪 Teszt: tests/neural_ai/core/events/test_events_factory.py

**Tesztelt modul:** [`neural_ai/core/events/events_factory.py`](../../neural_ai/core/events/events_factory.py)

Tesztek az EventBusFactory-hez.

Ez a modul tartalmazza az EventBusFactory tesztjeit.

Author: Neural AI Next Team
Version: 1.0.0

## Teszt Osztály: `TestEventBusFactoryCreate`

EventBusFactory create metódus tesztek.

### ✓ `test_create_default()`

Teszteli az alapértelmezett EventBus létrehozást.

### ✓ `test_create_with_config()`

Teszteli az EventBus létrehozást konfigurációval.

### ✓ `test_create_returns_interface()`

Teszteli, hogy az EventBusFactory EventBusInterface-t ad vissza.

## Teszt Osztály: `TestEventBusFactoryCreateAndStart`

EventBusFactory create_and_start metódus tesztek.

### ✓ `test_create_and_start_default()`

Teszteli az alapértelmezett EventBus létrehozást és indítását.

### ✓ `test_create_and_start_with_config()`

Teszteli az EventBus létrehozást és indítását konfigurációval.

### ✓ `test_create_and_start_returns_interface()`

Teszteli, hogy a create_and_start EventBusInterface-t ad vissza.

## Teszt Osztály: `TestEventBusFactoryCreateFromConfig`

EventBusFactory create_from_config metódus tesztek.

### ✓ `test_create_from_config_success()`

Teszteli a sikeres EventBus létrehozást konfigurációkezelőből.

### ✓ `test_create_from_config_with_key_error()`

Teszteli az EventBus létrehozást KeyError esetén.

### ✓ `test_create_from_config_with_value_error()`

Teszteli az EventBus létrehozást ValueError esetén.

### ✓ `test_create_from_config_partial_config()`

Teszteli az EventBus létrehozást részleges konfigurációval.

### ✓ `test_create_from_config_returns_interface()`

Teszteli, hogy a create_from_config EventBusInterface-t ad vissza.

## Teszt Osztály: `TestEventBusFactoryGetEventBus`

EventBusFactory get_event_bus statikus metódus tesztek.

### ✓ `test_get_event_bus_creates_with_logger()`

Teszteli a get_event_bus statikus metódust.

### ✓ `test_get_event_bus_returns_interface()`

Teszteli, hogy a get_event_bus EventBusInterface-t ad vissza.

## Teszt Osztály: `TestEventBusFactoryStaticMethods`

EventBusFactory példány metódusok tesztek.

### ✓ `test_factory_methods_are_instance_methods()`

Teszteli, hogy a factory metódusok példány metódusok.

---

**Teszt fájl:** [`tests/neural_ai/core/events/test_events_factory.py`](../../tests/neural_ai/core/events/test_events_factory.py)

**Tesztelt modul:** [`neural_ai/core/events/events_factory.py`](../../neural_ai/core/events/events_factory.py)
