# tests/neural_ai/core/utils/exceptions/test_util_errors.py

Tesztek az util kivételekhez.

Ez a modul tartalmazza a UtilError és HardwareDetectionError osztályok
tesztelését, valamint az __init__.py exportjainak ellenőrzését.

## Importok

```python
from neural_ai.core.utils.exceptions import HardwareDetectionError
from neural_ai.core.utils.exceptions import UtilError
from neural_ai.core.utils.exceptions.util_error import HardwareDetectionError
from neural_ai.core.utils.exceptions.util_error import UtilError
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.utils.exceptions import UtilError
from neural_ai.core.utils.exceptions import HardwareDetectionError
import neural_ai.core.utils.exceptions
from neural_ai.core.utils.exceptions.util_error import HardwareDetectionError
from neural_ai.core.utils.exceptions.util_error import UtilError
```

## Osztály: `TestUtilError`

UtilError tesztjei.

### Metódusok

#### `test_util_error_creation()`

```python
def test_util_error_creation(self) -> None
```

Teszteli a UtilError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_util_error_with_details()`

```python
def test_util_error_with_details(self) -> None
```

Teszteli a UtilError létrehozását részletekkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_util_error_is_neural_ai_exception()`

```python
def test_util_error_is_neural_ai_exception(self) -> None
```

Teszteli, hogy a UtilError a NeuralAIException leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_util_error_is_exception()`

```python
def test_util_error_is_exception(self) -> None
```

Teszteli, hogy a UtilError az Exception leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestHardwareDetectionError`

HardwareDetectionError tesztjei.

### Metódusok

#### `test_hardware_detection_error_creation()`

```python
def test_hardware_detection_error_creation(self) -> None
```

Teszteli a HardwareDetectionError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_hardware_detection_error_with_type()`

```python
def test_hardware_detection_error_with_type(self) -> None
```

Teszteli a HardwareDetectionError létrehozását hardver típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_hardware_detection_error_inheritance()`

```python
def test_hardware_detection_error_inheritance(self) -> None
```

Teszteli, hogy a HardwareDetectionError a UtilError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_hardware_detection_error_is_exception()`

```python
def test_hardware_detection_error_is_exception(self) -> None
```

Teszteli, hogy a HardwareDetectionError az Exception leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestInitExports`

__init__.py exportok tesztjei.

### Metódusok

#### `test_init_exports_util_error()`

```python
def test_init_exports_util_error(self) -> None
```

Teszteli, hogy az __init__.py exportálja-e a UtilError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_exports_hardware_detection_error()`

```python
def test_init_exports_hardware_detection_error(self) -> None
```

Teszteli, hogy az __init__.py exportálja-e a HardwareDetectionError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_all_list()`

```python
def test_init_all_list(self) -> None
```

Teszteli, hogy az __all__ lista tartalmazza-e a szükséges exportokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_direct_import_from_module()`

```python
def test_direct_import_from_module(self) -> None
```

Teszteli a közvetlen importot a modulból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/utils/exceptions/test_util_errors.py`](../../tests/neural_ai/core/utils/exceptions/test_util_errors.py)
