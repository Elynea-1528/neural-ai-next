# 🧪 Teszt: tests/neural_ai/core/logger/exceptions/test_logger_error.py

**Tesztelt modul:** [`neural_ai/core/logger/exceptions/logger_error.py`](../../neural_ai/core/logger/exceptions/logger_error.py)

Logger error exception tesztek.

## Teszt Osztály: `TestLoggerError`

LoggerError osztály tesztei.

### ✓ `test_logger_error_is_exception()`

LoggerError Exception-ből származik.

### ✓ `test_logger_error_can_be_raised()`

LoggerError kiváltható.

### ✓ `test_logger_error_has_message()`

LoggerError tartalmaz üzenetet.

### ✓ `test_logger_error_without_message()`

LoggerError hozható létre üzenet nélkül.

## Teszt Osztály: `TestLoggerConfigurationError`

LoggerConfigurationError osztály tesztei.

### ✓ `test_logger_configuration_error_is_logger_error()`

LoggerConfigurationError LoggerError-ből származik.

### ✓ `test_logger_configuration_error_can_be_raised()`

LoggerConfigurationError kiváltható.

### ✓ `test_logger_configuration_error_has_message()`

LoggerConfigurationError tartalmaz üzenetet.

### ✓ `test_logger_configuration_error_without_message()`

LoggerConfigurationError hozható létre üzenet nélkül.

## Teszt Osztály: `TestLoggerInitializationError`

LoggerInitializationError osztály tesztei.

### ✓ `test_logger_initialization_error_is_logger_error()`

LoggerInitializationError LoggerError-ből származik.

### ✓ `test_logger_initialization_error_can_be_raised()`

LoggerInitializationError kiváltható.

### ✓ `test_logger_initialization_error_has_message()`

LoggerInitializationError tartalmaz üzenetet.

### ✓ `test_logger_initialization_error_without_message()`

LoggerInitializationError hozható létre üzenet nélkül.

## Teszt Osztály: `TestLoggerErrorHierarchy`

Logger error hierarchia tesztek.

### ✓ `test_logger_error_hierarchy()`

A kivételek helyes hierarchiát alkotnak.

### ✓ `test_catch_logger_error_catches_subclasses()`

LoggerError elkapja az összes alosztályt.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/exceptions/test_logger_error.py`](../../tests/neural_ai/core/logger/exceptions/test_logger_error.py)

**Tesztelt modul:** [`neural_ai/core/logger/exceptions/logger_error.py`](../../neural_ai/core/logger/exceptions/logger_error.py)
