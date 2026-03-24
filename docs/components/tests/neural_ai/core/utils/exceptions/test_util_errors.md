# 🧪 Teszt: tests/neural_ai/core/utils/exceptions/test_util_errors.py

**Tesztelt modul:** [`neural_ai/core/utils/exceptions/util_errors.py`](../../neural_ai/core/utils/exceptions/util_errors.py)

Tesztek az util kivételekhez.

Ez a modul tartalmazza a UtilError és HardwareDetectionError osztályok
tesztelését, valamint az __init__.py exportjainak ellenőrzését.

## Teszt Osztály: `TestUtilError`

UtilError tesztjei.

### ✓ `test_util_error_creation()`

Teszteli a UtilError létrehozását.

### ✓ `test_util_error_with_details()`

Teszteli a UtilError létrehozását részletekkel.

### ✓ `test_util_error_is_neural_ai_exception()`

Teszteli, hogy a UtilError a NeuralAIException leszármazottja.

### ✓ `test_util_error_is_exception()`

Teszteli, hogy a UtilError az Exception leszármazottja.

## Teszt Osztály: `TestHardwareDetectionError`

HardwareDetectionError tesztjei.

### ✓ `test_hardware_detection_error_creation()`

Teszteli a HardwareDetectionError létrehozását.

### ✓ `test_hardware_detection_error_with_type()`

Teszteli a HardwareDetectionError létrehozását hardver típussal.

### ✓ `test_hardware_detection_error_inheritance()`

Teszteli, hogy a HardwareDetectionError a UtilError leszármazottja.

### ✓ `test_hardware_detection_error_is_exception()`

Teszteli, hogy a HardwareDetectionError az Exception leszármazottja.

## Teszt Osztály: `TestInitExports`

__init__.py exportok tesztjei.

### ✓ `test_init_exports_util_error()`

Teszteli, hogy az __init__.py exportálja-e a UtilError-t.

### ✓ `test_init_exports_hardware_detection_error()`

Teszteli, hogy az __init__.py exportálja-e a HardwareDetectionError-t.

### ✓ `test_init_all_list()`

Teszteli, hogy az __all__ lista tartalmazza-e a szükséges exportokat.

### ✓ `test_direct_import_from_module()`

Teszteli a közvetlen importot a modulból.

---

**Teszt fájl:** [`tests/neural_ai/core/utils/exceptions/test_util_errors.py`](../../tests/neural_ai/core/utils/exceptions/test_util_errors.py)

**Tesztelt modul:** [`neural_ai/core/utils/exceptions/util_errors.py`](../../neural_ai/core/utils/exceptions/util_errors.py)
