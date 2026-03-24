# 🧪 Teszt: tests/neural_ai/core/config/exceptions/test_config_error.py

**Tesztelt modul:** [`neural_ai/core/config/exceptions/config_error.py`](../../neural_ai/core/config/exceptions/config_error.py)

Átfogó tesztek a konfigurációs kivételekhez.

Ez a modul tartalmazza a ConfigError és leszármazott osztályok
részletes tesztelését, beleértve az attribútumok ellenőrzését.

## Teszt Osztály: `TestConfigError`

ConfigError alaposztály tesztjei.

### ✓ `test_base_error_creation()`

Teszteli az alap ConfigError létrehozását.

### ✓ `test_base_error_with_code()`

Teszteli a ConfigError létrehozását hibakóddal.

## Teszt Osztály: `TestConfigLoadError`

ConfigLoadError tesztjei.

### ✓ `test_load_error_creation()`

Teszteli a ConfigLoadError létrehozását.

### ✓ `test_load_error_without_optional_params()`

Teszteli a ConfigLoadError létrehozását opcionális paraméterek nélkül.

## Teszt Osztály: `TestConfigSaveError`

ConfigSaveError tesztjei.

### ✓ `test_save_error_creation()`

Teszteli a ConfigSaveError létrehozását.

### ✓ `test_save_error_without_optional_params()`

Teszteli a ConfigSaveError létrehozását opcionális paraméterek nélkül.

## Teszt Osztály: `TestConfigValidationError`

ConfigValidationError tesztjei.

### ✓ `test_validation_error_creation()`

Teszteli a ConfigValidationError létrehozását.

### ✓ `test_validation_error_without_optional_params()`

Teszteli a ConfigValidationError létrehozását opcionális paraméterek nélkül.

## Teszt Osztály: `TestConfigTypeError`

ConfigTypeError tesztjei.

### ✓ `test_type_error_creation()`

Teszteli a ConfigTypeError létrehozását.

### ✓ `test_type_error_without_optional_params()`

Teszteli a ConfigTypeError létrehozását opcionális paraméterek nélkül.

## Teszt Osztály: `TestConfigKeyError`

ConfigKeyError tesztjei.

### ✓ `test_key_error_creation()`

Teszteli a ConfigKeyError létrehozását.

### ✓ `test_key_error_without_optional_params()`

Teszteli a ConfigKeyError létrehozását opcionális paraméterek nélkül.

### ✓ `test_key_error_with_none_available_keys()`

Teszteli a ConfigKeyError létrehozását None available_keys paraméterrel.

## Teszt Osztály: `TestExceptionHierarchy`

Kivétel hierarchia tesztjei.

### ✓ `test_exception_inheritance()`

Teszteli, hogy a kivételek helyesen öröklődnek.

### ✓ `test_exception_is_exception()`

Teszteli, hogy minden kivétel az Exception leszármazottja.

---

**Teszt fájl:** [`tests/neural_ai/core/config/exceptions/test_config_error.py`](../../tests/neural_ai/core/config/exceptions/test_config_error.py)

**Tesztelt modul:** [`neural_ai/core/config/exceptions/config_error.py`](../../neural_ai/core/config/exceptions/config_error.py)
