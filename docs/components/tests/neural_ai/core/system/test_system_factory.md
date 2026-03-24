# 🧪 Teszt: tests/neural_ai/core/system/test_system_factory.py

**Tesztelt modul:** [`neural_ai/core/system/system_factory.py`](../../neural_ai/core/system/system_factory.py)

SystemComponentFactory tesztelése.

Ez a modul a SystemComponentFactory osztályt teszteli, amely felelős
a rendszer komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért.

## Teszt Osztály: `TestSystemComponentFactory`

SystemComponentFactory osztály tesztjei.

### ✓ `test_create_health_monitor_default()`

Alapértelmezett HealthMonitor létrehozásának tesztelése.

### ✓ `test_create_health_monitor_with_name()`

HealthMonitor létrehozása névvel.

### ✓ `test_create_health_monitor_with_logger()`

HealthMonitor létrehozása loggerrel.

### ✓ `test_create_health_monitor_caching()`

HealthMonitor gyorsítótár tesztelése.

### ✓ `test_create_health_check_default()`

Alapértelmezett HealthCheck létrehozásának tesztelése.

### ✓ `test_create_health_check_with_logger()`

HealthCheck létrehozása loggerrel.

### ✓ `test_create_health_check_invalid_type()`

Érvénytelen HealthCheck típus tesztelése.

### ✓ `test_register_component()`

Komponens regisztrálásának tesztelése.

### ✓ `test_register_component_with_custom_check()`

Komponens regisztrálása egyedi ellenőrzéssel.

### ✓ `test_register_component_nonexistent_monitor()`

Komponens regisztrálása nem létező monitorhoz.

### ✓ `test_unregister_component()`

Komponens eltávolításának tesztelése.

### ✓ `test_unregister_component_nonexistent_monitor()`

Komponens eltávolítása nem létező monitorból.

### ✓ `test_get_health_monitor()`

HealthMonitor lekérdezésének tesztelése.

### ✓ `test_get_health_monitor_nonexistent()`

Nem létező HealthMonitor lekérdezésének tesztelése.

### ✓ `test_get_registered_monitors()`

Regisztrált monitorok listázásának tesztelése.

### ✓ `test_clear_monitors()`

Monitorok törlésének tesztelése.

### ✓ `test_health_monitor_integration()`

HealthMonitor integrációs teszt.

### ✓ `test_health_monitor_with_system_metrics()`

HealthMonitor rendszer metrikák gyűjtésének tesztelése.

### ✓ `test_register_component_fallback_implementation()`

Teszteli a register_component fallback implementációját.

---

**Teszt fájl:** [`tests/neural_ai/core/system/test_system_factory.py`](../../tests/neural_ai/core/system/test_system_factory.py)

**Tesztelt modul:** [`neural_ai/core/system/system_factory.py`](../../neural_ai/core/system/system_factory.py)
