# 🧪 Teszt: tests/neural_ai/ui/services/test_dashboard_service.py

**Tesztelt modul:** [`neural_ai/ui/services/dashboard_service.py`](../../neural_ai/ui/services/dashboard_service.py)

Dashboard Service tesztek.

## Teszt Osztály: `TestDashboardService`

Dashboard Service tesztek osztálya.

### ✓ `test_init()`

Teszteli a Dashboard Service inicializálását.

### ✓ `test_get_health_status_with_available_monitor()`

Teszteli az egészségügyi állapot lekérdezését, ha a monitor elérhető.

### ✓ `test_get_health_status_without_health_monitor()`

Teszteli az egészségügyi állapot lekérdezését, ha a health monitor nem elérhető.

### ✓ `test_get_health_status_all_status_types()`

Teszteli az összes állapot típus leképezését.

### ✓ `test_get_system_overview()`

Teszteli a rendszer áttekintő adatok lekérdezését.

### ✓ `test_get_performance_metrics_with_resources()`

Teszteli a teljesítmény metrikák lekérdezését resources adatokkal.

### ✓ `test_get_performance_metrics_without_resources()`

Teszteli a teljesítmény metrikák lekérdezését resources adatok nélkül.

### ✓ `test_get_recent_activities()`

Teszteli a legutóbbi tevékenységek lekérdezését.

### ✓ `test_refresh_data()`

Teszteli a dashboard adatok frissítését.

### ✓ `test_subscribe_to_updates()`

Teszteli a feliratkozást dashboard frissítésekre.

### ✓ `test_notify_subscribers()`

Teszteli a feliratkozók értesítését.

### ✓ `test_notify_subscribers_with_exception()`

Teszteli a feliratkozók értesítését, ha egy callback hibát dob.

### ✓ `test_cached_data_persistence()`

Teszteli, hogy az adatok tényleg gyorsítótárazásra kerülnek.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_dashboard_service.py`](../../tests/neural_ai/ui/services/test_dashboard_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/dashboard_service.py`](../../neural_ai/ui/services/dashboard_service.py)
