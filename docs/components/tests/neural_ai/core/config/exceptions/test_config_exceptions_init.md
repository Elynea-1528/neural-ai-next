# 🧪 Teszt: tests/neural_ai/core/config/exceptions/test_config_exceptions_init.py

**Tesztelt modul:** [`neural_ai/core/config/exceptions/config_exceptions_init.py`](../../neural_ai/core/config/exceptions/config_exceptions_init.py)

Unit tesztek a neural_ai.core.config.exceptions __init__ modulhoz.

Ez a modul teszteli a config exceptions modul publikus API-ját és exportált kivételeit.

## Teszt Osztály: `TestConfigExceptionsModuleExports`

Tesztek a config exceptions modul exportálásához.

### ✓ `test_exceptions_module_exports_config_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigError-t.

### ✓ `test_exceptions_module_exports_config_load_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigLoadError-t.

### ✓ `test_exceptions_module_exports_config_save_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigSaveError-t.

### ✓ `test_exceptions_module_exports_config_validation_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigValidationError-t.

### ✓ `test_exceptions_module_exports_config_type_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigTypeError-t.

### ✓ `test_exceptions_module_exports_config_key_error()`

Ellenőrzi, hogy az exceptions modul exportálja a ConfigKeyError-t.

### ✓ `test_exceptions_module_all_exports()`

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

## Teszt Osztály: `TestConfigErrorHierarchy`

Tesztek a config kivétel hierarchiához.

### ✓ `test_config_error_is_base_exception()`

Ellenőrzi, hogy a ConfigError az Exception leszármazottja.

### ✓ `test_config_load_error_inherits_from_config_error()`

Ellenőrzi, hogy a ConfigLoadError a ConfigError leszármazottja.

### ✓ `test_config_save_error_inherits_from_config_error()`

Ellenőrzi, hogy a ConfigSaveError a ConfigError leszármazottja.

### ✓ `test_config_validation_error_inherits_from_config_error()`

Ellenőrzi, hogy a ConfigValidationError a ConfigError leszármazottja.

### ✓ `test_config_type_error_inherits_from_config_error()`

Ellenőrzi, hogy a ConfigTypeError a ConfigError leszármazottja.

### ✓ `test_config_key_error_inherits_from_config_error()`

Ellenőrzi, hogy a ConfigKeyError a ConfigError leszármazottja.

## Teszt Osztály: `TestConfigErrorRaising`

Tesztek a config kivételek dobásához.

### ✓ `test_config_error_can_be_raised()`

Ellenőrzi, hogy a ConfigError kivétel dobható.

### ✓ `test_config_load_error_can_be_raised()`

Ellenőrzi, hogy a ConfigLoadError kivétel dobható.

### ✓ `test_config_save_error_can_be_raised()`

Ellenőrzi, hogy a ConfigSaveError kivétel dobható.

### ✓ `test_config_validation_error_can_be_raised()`

Ellenőrzi, hogy a ConfigValidationError kivétel dobható.

### ✓ `test_config_type_error_can_be_raised()`

Ellenőrzi, hogy a ConfigTypeError kivétel dobható.

### ✓ `test_config_key_error_can_be_raised()`

Ellenőrzi, hogy a ConfigKeyError kivétel dobható.

## Teszt Osztály: `TestConfigErrorChaining`

Tesztek a config kivétel láncoláshoz.

### ✓ `test_config_error_with_chaining()`

Ellenőrzi a ConfigError exception chaining-et.

### ✓ `test_config_load_error_with_chaining()`

Ellenőrzi a ConfigLoadError exception chaining-et.

### ✓ `test_config_validation_error_with_chaining()`

Ellenőrzi a ConfigValidationError exception chaining-et.

---

**Teszt fájl:** [`tests/neural_ai/core/config/exceptions/test_config_exceptions_init.py`](../../tests/neural_ai/core/config/exceptions/test_config_exceptions_init.py)

**Tesztelt modul:** [`neural_ai/core/config/exceptions/config_exceptions_init.py`](../../neural_ai/core/config/exceptions/config_exceptions_init.py)
