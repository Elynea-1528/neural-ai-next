# 🧪 Teszt: tests/neural_ai/core/base/implementations/test_component_bundle.py

**Tesztelt modul:** [`neural_ai/core/base/implementations/component_bundle.py`](../../neural_ai/core/base/implementations/component_bundle.py)

CoreComponents tesztelése.

Ez a modul tartalmazza a CoreComponents osztály egységtesztjeit,
beleértve a komponens lekérdezést, beállítást és validálást.

## Teszt Osztály: `TestCoreComponents`

CoreComponents osztály tesztjei.

### ✓ `test_init_with_container()`

Teszteli a komponensek inicializálását meglévő konténerrel.

### ✓ `test_init_without_container()`

Teszteli a komponensek inicializálását új konténerrel.

### ✓ `test_config_property_none()`

Teszteli a config property-t ha nincs config komponens.

### ✓ `test_config_property_with_instance()`

Teszteli a config property-t ha van config komponens.

### ✓ `test_logger_property_none()`

Teszteli a logger property-t ha nincs logger komponens.

### ✓ `test_logger_property_with_instance()`

Teszteli a logger property-t ha van logger komponens.

### ✓ `test_storage_property_none()`

Teszteli a storage property-t ha nincs storage komponens.

### ✓ `test_storage_property_with_instance()`

Teszteli a storage property-t ha van storage komponens.

### ✓ `test_database_property_none()`

Teszteli a database property-t ha nincs database komponens.

### ✓ `test_database_property_with_instance()`

Teszteli a database property-t ha van database komponens.

### ✓ `test_event_bus_property_none()`

Teszteli a event_bus property-t ha nincs event_bus komponens.

### ✓ `test_event_bus_property_with_instance()`

Teszteli a event_bus property-t ha van event_bus komponens.

### ✓ `test_hardware_property_none()`

Teszteli a hardware property-t ha nincs hardware komponens.

### ✓ `test_hardware_property_with_instance()`

Teszteli a hardware property-t ha van hardware komponens.

### ✓ `test_has_config_false()`

Teszteli a has_config metódust ha nincs config.

### ✓ `test_has_config_true()`

Teszteli a has_config metódust ha van config.

### ✓ `test_has_logger_false()`

Teszteli a has_logger metódust ha nincs logger.

### ✓ `test_has_logger_true()`

Teszteli a has_logger metódust ha van logger.

### ✓ `test_has_storage_false()`

Teszteli a has_storage metódust ha nincs storage.

### ✓ `test_has_storage_true()`

Teszteli a has_storage metódust ha van storage.

### ✓ `test_has_database_false()`

Teszteli a has_database metódust ha nincs database.

### ✓ `test_has_database_true()`

Teszteli a has_database metódust ha van database.

### ✓ `test_has_event_bus_false()`

Teszteli a has_event_bus metódust ha nincs event_bus.

### ✓ `test_has_event_bus_true()`

Teszteli a has_event_bus metódust ha van event_bus.

### ✓ `test_has_hardware_false()`

Teszteli a has_hardware metódust ha nincs hardware.

### ✓ `test_has_hardware_true()`

Teszteli a has_hardware metódust ha van hardware.

### ✓ `test_validate_false_when_empty()`

Teszteli a validate metódust üres komponensekkel.

### ✓ `test_validate_true_when_all_present()`

Teszteli a validate metódust minden komponenssel.

### ✓ `test_validate_false_when_some_missing()`

Teszteli a validate metódust néhány hiányzó komponenssel.

### ✓ `test_persister_property_none()`

Teszteli a persister property-t ha nincs persister komponens.

### ✓ `test_persister_property_with_instance()`

Teszteli a persister property-t ha van persister komponens.

### ✓ `test_live_feed_property_none()`

Teszteli a live_feed property-t ha nincs live_feed komponens.

### ✓ `test_live_feed_property_with_instance()`

Teszteli a live_feed property-t ha van live_feed komponens.

### ✓ `test_set_persister()`

Teszteli a set_persister metódust.

### ✓ `test_set_live_feed()`

Teszteli a set_live_feed metódust.

### ✓ `test_has_persister_false()`

Teszteli a has_persister metódust ha nincs persister.

### ✓ `test_has_persister_true()`

Teszteli a has_persister metódust ha van persister.

### ✓ `test_has_live_feed_false()`

Teszteli a has_live_feed metódust ha nincs live_feed.

### ✓ `test_has_live_feed_true()`

Teszteli a has_live_feed metódust ha van live_feed.

---

**Teszt fájl:** [`tests/neural_ai/core/base/implementations/test_component_bundle.py`](../../tests/neural_ai/core/base/implementations/test_component_bundle.py)

**Tesztelt modul:** [`neural_ai/core/base/implementations/component_bundle.py`](../../neural_ai/core/base/implementations/component_bundle.py)
