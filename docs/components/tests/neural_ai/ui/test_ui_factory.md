# 🧪 Teszt: tests/neural_ai/ui/test_ui_factory.py

**Tesztelt modul:** [`neural_ai/ui/ui_factory.py`](../../neural_ai/ui/ui_factory.py)

Tesztek a UI Service Factory számára.

## Teszt Osztály: `TestUIServiceFactory`

A UIServiceFactory tesztosztálya.

### ✓ `test_factory_initialization()`

A factory inicializálásának tesztelése.

### ✓ `test_initialize_with_bridge()`

A factory inicializálásának tesztelése bridge-el.

### ✓ `test_get_navigation_service_before_initialization()`

Navigation service lekérdezése inicializálás előtt.

### ✓ `test_get_navigation_service_after_initialization()`

Navigation service lekérdezése inicializálás után.

### ✓ `test_get_dashboard_service_before_initialization()`

Dashboard service lekérdezése inicializálás előtt.

### ✓ `test_get_dashboard_service_after_initialization()`

Dashboard service lekérdezése inicializálás után.

### ✓ `test_get_data_service_before_initialization()`

Data service lekérdezése inicializálás előtt.

### ✓ `test_get_data_service_after_initialization()`

Data service lekérdezése inicializálás után.

### ✓ `test_get_ai_service_before_initialization()`

AI service lekérdezése inicializálás előtt.

### ✓ `test_get_ai_service_after_initialization()`

AI service lekérdezése inicializálás után.

### ✓ `test_get_strategy_service_before_initialization()`

Strategy service lekérdezése inicializálás előtt.

### ✓ `test_get_strategy_service_after_initialization()`

Strategy service lekérdezése inicializálás után.

### ✓ `test_get_live_ops_service_before_initialization()`

Live Ops service lekérdezése inicializálás előtt.

### ✓ `test_get_live_ops_service_after_initialization()`

Live Ops service lekérdezése inicializálás után.

### ✓ `test_get_all_services()`

Az összes szolgáltatás lekérdezésének tesztelése.

### ✓ `test_get_all_services_before_initialization()`

Összes szolgáltatás lekérdezése inicializálás előtt.

### ✓ `test_is_initialized_property()`

Az is_initialized property tesztelése.

### ✓ `test_reset_method()`

A reset metódus tesztelése.

### ✓ `test_singleton_pattern()`

A Singleton minta tesztelése.

### ✓ `test_data_service_compatibility()`

DataService kompatibilitás ellenőrzése a factory-val.

### ✓ `test_service_caching()`

Szolgáltatások gyorsítótárazásának tesztelése.

## Teszt Osztály: `TestUIConfigValidation`

UIConfig Pydantic validáció tesztek.

### ✓ `test_valid_ui_config()`

Érvényes UI konfiguráció tesztelése.

### ✓ `test_invalid_theme_raises_error()`

Érvénytelen téma ValidationError-t dob.

### ✓ `test_negative_refresh_rate_raises_error()`

Negatív refresh_rate ValidationError-t dob.

### ✓ `test_zero_refresh_rate_raises_error()`

Nulla refresh_rate ValidationError-t dob.

### ✓ `test_factory_validates_config()`

Factory Pydantic validációt végez.

### ✓ `test_default_values()`

Alapértelmezett értékek tesztelése.

### ✓ `test_nested_config_validation()`

Beágyazott konfiguráció validálása.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_ui_factory.py`](../../tests/neural_ai/ui/test_ui_factory.py)

**Tesztelt modul:** [`neural_ai/ui/ui_factory.py`](../../neural_ai/ui/ui_factory.py)
