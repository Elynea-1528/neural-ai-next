# 🧪 Teszt: tests/neural_ai/core/logger/test_logger_factory.py

**Tesztelt modul:** [`neural_ai/core/logger/logger_factory.py`](../../neural_ai/core/logger/logger_factory.py)

Logger Factory tesztek - Mirror Test a factory.py-hoz.

Ez a teszt suite kiegészíti a test_logger_factory.py-t
valós config betöltéssel és edge case teszteléssel.

## Teszt Osztály: `TestLoggerFactoryRealConfig`

Valós YAML config tesztelése.

### ✓ `test_configure_with_real_yaml_parsing()`

Valós YAML fájl betöltése és config alkalmazása.

### ✓ `test_configure_fallback_with_missing_handlers()`

Hiányos config esetén fallback console handler + warning.

### ✓ `test_configure_fallback_warning_is_structured()`

A fallback warning strukturált logolással történik.

## Teszt Osztály: `TestLoggerFactoryCoverage`

100%-os lefedettség biztosítása.

### ✓ `test_all_branches_in_get_logger()`

get_logger() minden ága le van fedve.

### ✓ `test_configure_file_handler_creation()`

configure() file handler létrehozásának tesztelése.

### ✓ `test_configure_rotating_file_handler()`

Rotating file handler létrehozásának tesztelése.

### ✓ `test_configure_trace_file_handler()`

Trace file handler létrehozásának tesztelése.

### ✓ `test_configure_trace_file_handler_non_rotating()`

Trace file handler nem-rotating változatának tesztelése.

### ✓ `test_schema_version_methods()`

Schema version getter/setter tesztelése.

### ✓ `test_clear_instances()`

clear_instances() metódus tesztelése.

### ✓ `test_get_registered_types()`

get_registered_types() metódus tesztelése.

### ✓ `test_is_logger_registered()`

is_logger_registered() metódus tesztelése.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/test_logger_factory.py`](../../tests/neural_ai/core/logger/test_logger_factory.py)

**Tesztelt modul:** [`neural_ai/core/logger/logger_factory.py`](../../neural_ai/core/logger/logger_factory.py)
