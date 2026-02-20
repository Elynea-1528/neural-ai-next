# tests/neural_ai/core/base/exceptions/test_exceptions_init.py

Core base exceptions modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.exceptions.__init__.py fájlban
definiált exportokat és funkcionalitásokat.

## Importok

```python
from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.exceptions import ConfigurationError
from neural_ai.core.base.exceptions import ConnectionError
from neural_ai.core.base.exceptions import DependencyError
from neural_ai.core.base.exceptions import InsufficientDiskSpaceError
from neural_ai.core.base.exceptions import NetworkException
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.base.exceptions import PermissionDeniedError
from neural_ai.core.base.exceptions import SingletonViolationError
from neural_ai.core.base.exceptions import StorageException
# ... és még 7 import
```

## Osztály: `TestExceptionsInit`

Exceptions modul __init__.py tesztjei.

### Metódusok

#### `test_neural_ai_exception_import()`

```python
def test_neural_ai_exception_import(self) -> None
```

Teszteli, hogy a NeuralAIException importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_exception_import()`

```python
def test_storage_exception_import(self) -> None
```

Teszteli, hogy a StorageException importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_write_error_import()`

```python
def test_storage_write_error_import(self) -> None
```

Teszteli, hogy a StorageWriteError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_read_error_import()`

```python
def test_storage_read_error_import(self) -> None
```

Teszteli, hogy a StorageReadError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_permission_error_import()`

```python
def test_storage_permission_error_import(self) -> None
```

Teszteli, hogy a StoragePermissionError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_configuration_error_import()`

```python
def test_configuration_error_import(self) -> None
```

Teszteli, hogy a ConfigurationError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dependency_error_import()`

```python
def test_dependency_error_import(self) -> None
```

Teszteli, hogy a DependencyError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_singleton_violation_error_import()`

```python
def test_singleton_violation_error_import(self) -> None
```

Teszteli, hogy a SingletonViolationError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_component_not_found_error_import()`

```python
def test_component_not_found_error_import(self) -> None
```

Teszteli, hogy a ComponentNotFoundError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_network_exception_import()`

```python
def test_network_exception_import(self) -> None
```

Teszteli, hogy a NetworkException importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_timeout_error_import()`

```python
def test_timeout_error_import(self) -> None
```

Teszteli, hogy a TimeoutError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_connection_error_import()`

```python
def test_connection_error_import(self) -> None
```

Teszteli, hogy a ConnectionError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_insufficient_disk_space_error_import()`

```python
def test_insufficient_disk_space_error_import(self) -> None
```

Teszteli, hogy a InsufficientDiskSpaceError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_permission_denied_error_import()`

```python
def test_permission_denied_error_import(self) -> None
```

Teszteli, hogy a PermissionDeniedError importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_exports_available()`

```python
def test_all_exports_available(self) -> None
```

Teszteli, hogy minden exportált kivétel elérhető-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exception_inheritance_hierarchy()`

```python
def test_exception_inheritance_hierarchy(self) -> None
```

Teszteli a kivételek öröklődési hierarchiáját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exceptions_can_be_raised()`

```python
def test_exceptions_can_be_raised(self) -> None
```

Teszteli, hogy a kivételek dobhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exception_messages()`

```python
def test_exception_messages(self) -> None
```

Teszteli a kivételek üzeneteit.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/exceptions/test_exceptions_init.py`](../../tests/neural_ai/core/base/exceptions/test_exceptions_init.py)
