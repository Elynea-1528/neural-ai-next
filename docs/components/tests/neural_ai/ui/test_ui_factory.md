# 🧪 Teszt: tests/neural_ai/ui/test_ui_factory.py

**Tesztelt modul:** [`neural_ai/ui/ui_factory.py`](../../neural_ai/ui/ui_factory.py)

Unit tesztek a factory modulhoz.

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false
# Mock dict type inference hibák.

Ez a modul teszteli a UIServiceFactory osztály funkcióit.

## Teszt Osztály: `TestUIServiceFactoryInit`

Tesztek a UIServiceFactory inicializálásához.

### ✓ `test_init_creates_instance()`

Ellenőrzi, hogy a UIServiceFactory létrehozható.

## Teszt Osztály: `TestUIServiceFactoryInitialize`

Tesztek a UIServiceFactory.initialize metódushoz.

### ✓ `test_initialize_with_dict_config()`

Ellenőrzi, hogy az initialize dict config-gal működik.

### ✓ `test_initialize_with_uiconfig()`

Ellenőrzi, hogy az initialize UIConfig-gal működik.

## Teszt Osztály: `TestUIServiceFactoryGetNavigationService`

Tesztek a get_navigation_service metódushoz.

### ✓ `test_get_navigation_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_navigation_service_success()`

Ellenőrzi, hogy a navigation service lekérhető.

## Teszt Osztály: `TestUIServiceFactoryGetDataService`

Tesztek a get_data_service metódushoz.

### ✓ `test_get_data_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_data_service_success()`

Ellenőrzi, hogy a data service lekérhető.

## Teszt Osztály: `TestUIServiceFactoryGetDashboardService`

Tesztek a get_dashboard_service metódushoz.

### ✓ `test_get_dashboard_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_dashboard_service_success()`

Ellenőrzi, hogy a dashboard service lekérhető.

## Teszt Osztály: `TestUIServiceFactoryGetAIService`

Tesztek a get_ai_service metódushoz.

### ✓ `test_get_ai_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_ai_service_success()`

Ellenőrzi, hogy az AI service lekérhető.

## Teszt Osztály: `TestUIServiceFactoryGetStrategyService`

Tesztek a get_strategy_service metódushoz.

### ✓ `test_get_strategy_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_strategy_service_success()`

Ellenőrzi, hogy a strategy service lekérhető.

## Teszt Osztály: `TestUIServiceFactoryGetLiveOpsService`

Tesztek a get_live_ops_service metódushoz.

### ✓ `test_get_live_ops_service_raises_error_when_not_initialized()`

Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva.

### ✓ `test_get_live_ops_service_success()`

Ellenőrzi, hogy a live ops service lekérhető.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_ui_factory.py`](../../tests/neural_ai/ui/test_ui_factory.py)

**Tesztelt modul:** [`neural_ai/ui/ui_factory.py`](../../neural_ai/ui/ui_factory.py)
