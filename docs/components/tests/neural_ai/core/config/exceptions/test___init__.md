# tests/neural_ai/core/config/exceptions/test___init__.py

Unit tesztek a neural_ai.core.config.exceptions __init__ modulhoz.

Ez a modul teszteli a config exceptions modul publikus API-ját és exportált kivételeit.

## Importok

```python
import pytest
from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.exceptions import ConfigSaveError
from neural_ai.core.config.exceptions import ConfigValidationError
from neural_ai.core.config.exceptions import ConfigTypeError
from neural_ai.core.config.exceptions import ConfigKeyError
from neural_ai.core.config.exceptions import __all__
from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.exceptions import ConfigError
# ... és még 18 import
```

## Osztály: `TestConfigExceptionsModuleExports`

Tesztek a config exceptions modul exportálásához.

### Metódusok

#### `test_exceptions_module_exports_config_error()`

```python
def test_exceptions_module_exports_config_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_exports_config_load_error()`

```python
def test_exceptions_module_exports_config_load_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigLoadError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_exports_config_save_error()`

```python
def test_exceptions_module_exports_config_save_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigSaveError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_exports_config_validation_error()`

```python
def test_exceptions_module_exports_config_validation_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigValidationError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_exports_config_type_error()`

```python
def test_exceptions_module_exports_config_type_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigTypeError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_exports_config_key_error()`

```python
def test_exceptions_module_exports_config_key_error(self) -> None
```

Ellenőrzi, hogy az exceptions modul exportálja a ConfigKeyError-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_module_all_exports()`

```python
def test_exceptions_module_all_exports(self) -> None
```

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigErrorHierarchy`

Tesztek a config kivétel hierarchiához.

### Metódusok

#### `test_config_error_is_base_exception()`

```python
def test_config_error_is_base_exception(self) -> None
```

Ellenőrzi, hogy a ConfigError az Exception leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_load_error_inherits_from_config_error()`

```python
def test_config_load_error_inherits_from_config_error(self) -> None
```

Ellenőrzi, hogy a ConfigLoadError a ConfigError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_save_error_inherits_from_config_error()`

```python
def test_config_save_error_inherits_from_config_error(self) -> None
```

Ellenőrzi, hogy a ConfigSaveError a ConfigError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_validation_error_inherits_from_config_error()`

```python
def test_config_validation_error_inherits_from_config_error(self) -> None
```

Ellenőrzi, hogy a ConfigValidationError a ConfigError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_type_error_inherits_from_config_error()`

```python
def test_config_type_error_inherits_from_config_error(self) -> None
```

Ellenőrzi, hogy a ConfigTypeError a ConfigError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_key_error_inherits_from_config_error()`

```python
def test_config_key_error_inherits_from_config_error(self) -> None
```

Ellenőrzi, hogy a ConfigKeyError a ConfigError leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigErrorRaising`

Tesztek a config kivételek dobásához.

### Metódusok

#### `test_config_error_can_be_raised()`

```python
def test_config_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_load_error_can_be_raised()`

```python
def test_config_load_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigLoadError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_save_error_can_be_raised()`

```python
def test_config_save_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigSaveError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_validation_error_can_be_raised()`

```python
def test_config_validation_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigValidationError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_type_error_can_be_raised()`

```python
def test_config_type_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigTypeError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_key_error_can_be_raised()`

```python
def test_config_key_error_can_be_raised(self) -> None
```

Ellenőrzi, hogy a ConfigKeyError kivétel dobható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigErrorChaining`

Tesztek a config kivétel láncoláshoz.

### Metódusok

#### `test_config_error_with_chaining()`

```python
def test_config_error_with_chaining(self) -> None
```

Ellenőrzi a ConfigError exception chaining-et.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_load_error_with_chaining()`

```python
def test_config_load_error_with_chaining(self) -> None
```

Ellenőrzi a ConfigLoadError exception chaining-et.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_validation_error_with_chaining()`

```python
def test_config_validation_error_with_chaining(self) -> None
```

Ellenőrzi a ConfigValidationError exception chaining-et.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/exceptions/test___init__.py`](../../tests/neural_ai/core/config/exceptions/test___init__.py)
