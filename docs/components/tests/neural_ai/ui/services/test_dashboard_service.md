# 🧪 Teszt: tests/neural_ai/ui/services/test_dashboard_service.py

**Tesztelt modul:** [`neural_ai/ui/services/dashboard_service.py`](../../neural_ai/ui/services/dashboard_service.py)

Unit tesztek a dashboard_service modulhoz.

Ez a modul teszteli a DashboardService osztály funkcióit.

## Teszt Osztály: `TestDashboardServiceInit`

Tesztek a DashboardService inicializálásához.

### ✓ `test_init_creates_instance()`

Ellenőrzi, hogy a DashboardService létrehozható.

## Teszt Osztály: `TestDashboardServiceGetSystemOverview`

Tesztek a get_system_overview metódushoz.

### ✓ `test_get_system_overview_returns_data()`

Ellenőrzi, hogy a system overview adatokat ad vissza.

### ✓ `test_get_system_overview_uses_cache()`

Ellenőrzi, hogy a system overview cache-t használ.

## Teszt Osztály: `TestDashboardServiceGetHealthStatus`

Tesztek a get_health_status metódushoz.

### ✓ `test_get_health_status_returns_unknown_when_no_health_monitor()`

Ellenőrzi, hogy UNKNOWN-t ad vissza, ha nincs health monitor.

### ✓ `test_get_health_status_returns_status_map()`

Ellenőrzi, hogy a health status térképet ad vissza.

### ✓ `test_get_health_status_maps_all_statuses()`

Ellenőrzi, hogy minden ComponentStatus helyesen leképeződik.

## Teszt Osztály: `TestDashboardServiceGetPerformanceMetrics`

Tesztek a get_performance_metrics metódushoz.

### ✓ `test_get_performance_metrics_returns_data_from_system_info()`

Ellenőrzi, hogy a performance metrics adatokat ad vissza.

### ✓ `test_get_performance_metrics_returns_fallback_when_no_resources()`

Ellenőrzi, hogy fallback adatokat ad vissza, ha nincs resources.

## Teszt Osztály: `TestDashboardServiceGetRecentActivities`

Tesztek a get_recent_activities metódushoz.

### ✓ `test_get_recent_activities_returns_list()`

Ellenőrzi, hogy a recent activities listát ad vissza.

## Teszt Osztály: `TestDashboardServiceRefreshData`

Tesztek a refresh_data metódushoz.

### ✓ `test_refresh_data_clears_cache()`

Ellenőrzi, hogy a refresh_data törli a cache-t.

### ✓ `test_refresh_data_notifies_subscribers()`

Ellenőrzi, hogy a refresh_data értesíti a feliratkozókat.

## Teszt Osztály: `TestDashboardServiceSubscribeToUpdates`

Tesztek a subscribe_to_updates metódushoz.

### ✓ `test_subscribe_to_updates_adds_callback()`

Ellenőrzi, hogy a feliratkozás hozzáadja a callback-et.

### ✓ `test_subscribe_callback_handles_exception()`

Ellenőrzi, hogy a callback kivétel esetén sem állítja le a rendszert.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_dashboard_service.py`](../../tests/neural_ai/ui/services/test_dashboard_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/dashboard_service.py`](../../neural_ai/ui/services/dashboard_service.py)
