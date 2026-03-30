# 🧪 Teszt: tests/neural_ai/core/config/test_config_init.py

**Tesztelt modul:** [`neural_ai/core/config/config_init.py`](../../neural_ai/core/config/config_init.py)

Unit tesztek a neural_ai.core.config __init__ modulhoz.

Ez a modul teszteli a config modul publikus API-ját és exportált interfészeit.

## Teszt Osztály: `TestConfigModuleExports`

Tesztek a config modul exportálásához.

### ✓ `test_config_module_imports_exceptions()`

Ellenőrzi, hogy a config modul exportálja a kivétel osztályokat.

### ✓ `test_config_module_imports_factory()`

Ellenőrzi, hogy a config modul exportálja a factory osztályt.

### ✓ `test_config_module_imports_interfaces()`

Ellenőrzi, hogy a config modul exportálja az interfészeket.

### ✓ `test_config_module_all_exports()`

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

## Teszt Osztály: `TestConfigFactoryIntegration`

Integrációs tesztek a config factory használatához.

### ✓ `test_factory_creates_yaml_manager()`

Ellenőrzi, hogy a factory létrehoz egy YAML config manager példányt.

### ✓ `test_factory_get_manager_method_exists()`

Ellenőrzi, hogy a factory get_manager metódusa elérhető.

### ✓ `test_factory_create_manager_method_exists()`

Ellenőrzi, hogy a factory create_manager metódusa elérhető.

## Teszt Osztály: `TestConfigExceptionHierarchy`

Tesztek a config kivétel hierarchiához.

### ✓ `test_config_error_is_base_exception()`

Ellenőrzi, hogy a ConfigError az Exception leszármazottja.

### ✓ `test_specific_errors_inherit_from_config_error()`

Ellenőrzi, hogy a specifikus hibák a ConfigError leszármazottai.

### ✓ `test_config_errors_can_be_raised()`

Ellenőrzi, hogy a config hibák dobhatók.

---

**Teszt fájl:** [`tests/neural_ai/core/config/test_config_init.py`](../../tests/neural_ai/core/config/test_config_init.py)

**Tesztelt modul:** [`neural_ai/core/config/config_init.py`](../../neural_ai/core/config/config_init.py)
