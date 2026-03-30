# 🧪 Teszt: tests/neural_ai/core/system/exceptions/test_health_error.py

**Tesztelt modul:** [`neural_ai/core/system/exceptions/health_error.py`](../../neural_ai/core/system/exceptions/health_error.py)

Unit tesztek a Health Exception osztályokhoz.

## Teszt Osztály: `TestHealthError`

Tesztek a HealthError alap kivételhez.

### ✓ `test_health_error_is_exception()`

Ellenőrzi, hogy HealthError az Exception leszármazottja.

### ✓ `test_health_error_can_be_raised()`

Ellenőrzi, hogy HealthError dobható.

### ✓ `test_health_error_with_message()`

Ellenőrzi, hogy HealthError üzenettel dobható.

## Teszt Osztály: `TestHealthMonitorError`

Tesztek a HealthMonitorError kivételhez.

### ✓ `test_health_monitor_error_is_health_error()`

Ellenőrzi, hogy HealthMonitorError a HealthError leszármazottja.

### ✓ `test_health_monitor_error_can_be_raised()`

Ellenőrzi, hogy HealthMonitorError dobható.

### ✓ `test_health_monitor_error_with_message()`

Ellenőrzi, hogy HealthMonitorError üzenettel dobható.

### ✓ `test_health_monitor_error_caught_as_health_error()`

Ellenőrzi, hogy HealthMonitorError elkapható HealthError-ként.

## Teszt Osztály: `TestHealthCheckError`

Tesztek a HealthCheckError kivételhez.

### ✓ `test_health_check_error_is_health_error()`

Ellenőrzi, hogy HealthCheckError a HealthError leszármazottja.

### ✓ `test_health_check_error_can_be_raised()`

Ellenőrzi, hogy HealthCheckError dobható.

### ✓ `test_health_check_error_with_message()`

Ellenőrzi, hogy HealthCheckError üzenettel dobható.

### ✓ `test_health_check_error_caught_as_health_error()`

Ellenőrzi, hogy HealthCheckError elkapható HealthError-ként.

## Teszt Osztály: `TestComponentNotFoundError`

Tesztek a ComponentNotFoundError kivételhez.

### ✓ `test_component_not_found_error_is_health_monitor_error()`

Ellenőrzi, hogy ComponentNotFoundError a HealthMonitorError leszármazottja.

### ✓ `test_component_not_found_error_is_health_error()`

Ellenőrzi, hogy ComponentNotFoundError a HealthError leszármazottja.

### ✓ `test_component_not_found_error_can_be_raised()`

Ellenőrzi, hogy ComponentNotFoundError dobható.

### ✓ `test_component_not_found_error_with_message()`

Ellenőrzi, hogy ComponentNotFoundError üzenettel dobható.

### ✓ `test_component_not_found_error_caught_as_health_monitor_error()`

Ellenőrzi, hogy ComponentNotFoundError elkapható HealthMonitorError-ként.

### ✓ `test_component_not_found_error_caught_as_health_error()`

Ellenőrzi, hogy ComponentNotFoundError elkapható HealthError-ként.

---

**Teszt fájl:** [`tests/neural_ai/core/system/exceptions/test_health_error.py`](../../tests/neural_ai/core/system/exceptions/test_health_error.py)

**Tesztelt modul:** [`neural_ai/core/system/exceptions/health_error.py`](../../neural_ai/core/system/exceptions/health_error.py)
