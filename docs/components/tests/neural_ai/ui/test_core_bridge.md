# 🧪 Teszt: tests/neural_ai/ui/test_core_bridge.py

**Tesztelt modul:** [`neural_ai/ui/core_bridge.py`](../../neural_ai/ui/core_bridge.py)

Unit tesztek a core_bridge modulhoz.

Ez a modul teszteli a CoreBridge osztály funkcióit.

## Teszt Osztály: `TestCoreBridgeInit`

Tesztek a CoreBridge inicializálásához.

### ✓ `test_init_creates_instance()`

Ellenőrzi, hogy a CoreBridge létrehozható.

### ✓ `test_get_instance_returns_self()`

Ellenőrzi, hogy a get_instance visszaadja a példányt.

## Teszt Osztály: `TestCoreBridgeInitialize`

Tesztek a CoreBridge.initialize metódushoz.

### ✓ `test_initialize_success()`

Ellenőrzi, hogy az initialize sikeresen inicializálja a bridge-t.

### ✓ `test_initialize_calls_strategy_service_init()`

Ellenőrzi, hogy az initialize meghívja a strategy service inicializálást.

## Teszt Osztály: `TestCoreBridgeGetComponent`

Tesztek a CoreBridge.get_component metódushoz.

### ✓ `test_get_component_raises_error_when_not_initialized()`

Ellenőrzi, hogy a get_component hibát dob inicializálás nélkül.

### ✓ `test_get_component_parquet_storage()`

Ellenőrzi, hogy a get_component visszaadja a parquet storage-t.

### ✓ `test_get_component_config()`

Ellenőrzi, hogy a get_component visszaadja a config-ot.

### ✓ `test_get_component_logger()`

Ellenőrzi, hogy a get_component visszaadja a logger-t.

### ✓ `test_get_component_unknown_type()`

Ellenőrzi, hogy a get_component None-t ad vissza ismeretlen típusra.

## Teszt Osztály: `TestCoreBridgeSendCommand`

Tesztek a CoreBridge.send_command metódushoz.

### ✓ `test_send_command_returns_error_when_not_connected()`

Ellenőrzi, hogy a send_command hibát ad vissza kapcsolat nélkül.

### ✓ `test_send_command_success()`

Ellenőrzi, hogy a send_command sikeresen küld parancsot.

## Teszt Osztály: `TestCoreBridgeGetSystemInfo`

Tesztek a CoreBridge.get_system_info metódushoz.

### ✓ `test_get_system_info_returns_error_when_not_connected()`

Ellenőrzi, hogy a get_system_info hibát ad vissza kapcsolat nélkül.

### ✓ `test_get_system_info_success()`

Ellenőrzi, hogy a get_system_info visszaadja a rendszerinformációt.

## Teszt Osztály: `TestCoreBridgeProperties`

Tesztek a CoreBridge property-khez.

### ✓ `test_is_connected_default_false()`

Ellenőrzi, hogy az is_connected alapértelmezetten False.

### ✓ `test_is_connected_true_after_initialize()`

Ellenőrzi, hogy az is_connected True az initialize után.

### ✓ `test_core_property_default_none()`

Ellenőrzi, hogy a core property alapértelmezetten None.

### ✓ `test_core_property_setter()`

Ellenőrzi, hogy a core property setter működik.

### ✓ `test_connected_property_setter()`

Ellenőrzi, hogy a connected property setter működik.

### ✓ `test_strategy_service_property_default_none()`

Ellenőrzi, hogy a strategy_service property alapértelmezetten None.

### ✓ `test_strategy_service_property_setter()`

Ellenőrzi, hogy a strategy_service property setter működik.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_core_bridge.py`](../../tests/neural_ai/ui/test_core_bridge.py)

**Tesztelt modul:** [`neural_ai/ui/core_bridge.py`](../../neural_ai/ui/core_bridge.py)
