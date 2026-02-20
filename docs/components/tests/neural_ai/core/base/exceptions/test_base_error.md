# tests/neural_ai/core/base/exceptions/test_base_error.py

Base kivételek tesztelése.

Ez a modul tartalmazza a neural_ai.core.base.exceptions modulban
definiált összes kivétel osztály tesztjeit.

## Importok

```python
import pytest
from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.exceptions import ConfigurationError
from neural_ai.core.base.exceptions import ConnectionError
from neural_ai.core.base.exceptions import DependencyError
from neural_ai.core.base.exceptions import InsufficientDiskSpaceError
from neural_ai.core.base.exceptions import NetworkException
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.base.exceptions import PermissionDeniedError
from neural_ai.core.base.exceptions import SingletonViolationError
# ... és még 5 import
```

## Osztály: `TestNeuralAIException`

NeuralAIException alap kivétel tesztjei.

### Metódusok

#### `test_base_exception_can_be_raised()`

```python
def test_base_exception_can_be_raised(self) -> None
```

Teszteli, hogy az alap kivétel dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_base_exception_with_message()`

```python
def test_base_exception_with_message(self) -> None
```

Teszteli a kivételt üzenettel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_base_exception_inheritance()`

```python
def test_base_exception_inheritance(self) -> None
```

Teszteli, hogy a kivétel az Exception osztályból származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestStorageException`

StorageException kivétel tesztjei.

### Metódusok

#### `test_storage_exception_can_be_raised()`

```python
def test_storage_exception_can_be_raised(self) -> None
```

Teszteli, hogy a tároló kivétel dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_exception_inheritance()`

```python
def test_storage_exception_inheritance(self) -> None
```

Teszteli, hogy a kivétel a NeuralAIException-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_exception_with_message()`

```python
def test_storage_exception_with_message(self) -> None
```

Teszteli a kivételt üzenettel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestStorageWriteError`

StorageWriteError kivétel tesztjei.

### Metódusok

#### `test_storage_write_error_can_be_raised()`

```python
def test_storage_write_error_can_be_raised(self) -> None
```

Teszteli, hogy az írási hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_write_error_inheritance()`

```python
def test_storage_write_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_write_error_message()`

```python
def test_storage_write_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestStorageReadError`

StorageReadError kivétel tesztjei.

### Metódusok

#### `test_storage_read_error_can_be_raised()`

```python
def test_storage_read_error_can_be_raised(self) -> None
```

Teszteli, hogy az olvasási hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_read_error_inheritance()`

```python
def test_storage_read_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_read_error_message()`

```python
def test_storage_read_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestStoragePermissionError`

StoragePermissionError kivétel tesztjei.

### Metódusok

#### `test_storage_permission_error_can_be_raised()`

```python
def test_storage_permission_error_can_be_raised(self) -> None
```

Teszteli, hogy a jogosultsági hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_permission_error_inheritance()`

```python
def test_storage_permission_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_permission_error_message()`

```python
def test_storage_permission_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigurationError`

ConfigurationError kivétel tesztjei.

### Metódusok

#### `test_configuration_error_can_be_raised()`

```python
def test_configuration_error_can_be_raised(self) -> None
```

Teszteli, hogy a konfigurációs hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_configuration_error_inheritance()`

```python
def test_configuration_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_configuration_error_message()`

```python
def test_configuration_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDependencyError`

DependencyError kivétel tesztjei.

### Metódusok

#### `test_dependency_error_can_be_raised()`

```python
def test_dependency_error_can_be_raised(self) -> None
```

Teszteli, hogy a függőségi hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dependency_error_inheritance()`

```python
def test_dependency_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_dependency_error_message()`

```python
def test_dependency_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestSingletonViolationError`

SingletonViolationError kivétel tesztjei.

### Metódusok

#### `test_singleton_violation_error_can_be_raised()`

```python
def test_singleton_violation_error_can_be_raised(self) -> None
```

Teszteli, hogy a singleton megsértésének hibája dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_singleton_violation_error_inheritance()`

```python
def test_singleton_violation_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_singleton_violation_error_message()`

```python
def test_singleton_violation_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestComponentNotFoundError`

ComponentNotFoundError kivétel tesztjei.

### Metódusok

#### `test_component_not_found_error_can_be_raised()`

```python
def test_component_not_found_error_can_be_raised(self) -> None
```

Teszteli, hogy a komponens nem található hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_component_not_found_error_inheritance()`

```python
def test_component_not_found_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_component_not_found_error_message()`

```python
def test_component_not_found_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestNetworkException`

NetworkException kivétel tesztjei.

### Metódusok

#### `test_network_exception_can_be_raised()`

```python
def test_network_exception_can_be_raised(self) -> None
```

Teszteli, hogy a hálózati kivétel dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_network_exception_inheritance()`

```python
def test_network_exception_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_network_exception_message()`

```python
def test_network_exception_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestTimeoutError`

TimeoutError kivétel tesztjei.

### Metódusok

#### `test_timeout_error_can_be_raised()`

```python
def test_timeout_error_can_be_raised(self) -> None
```

Teszteli, hogy az időtúllépési hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_timeout_error_inheritance()`

```python
def test_timeout_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_timeout_error_message()`

```python
def test_timeout_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConnectionError`

ConnectionError kivétel tesztjei.

### Metódusok

#### `test_connection_error_can_be_raised()`

```python
def test_connection_error_can_be_raised(self) -> None
```

Teszteli, hogy a kapcsolódási hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_connection_error_inheritance()`

```python
def test_connection_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_connection_error_message()`

```python
def test_connection_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestInsufficientDiskSpaceError`

InsufficientDiskSpaceError kivétel tesztjei.

### Metódusok

#### `test_insufficient_disk_space_error_can_be_raised()`

```python
def test_insufficient_disk_space_error_can_be_raised(self) -> None
```

Teszteli, hogy a lemezterület hiány hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_insufficient_disk_space_error_inheritance()`

```python
def test_insufficient_disk_space_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_insufficient_disk_space_error_message()`

```python
def test_insufficient_disk_space_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPermissionDeniedError`

PermissionDeniedError kivétel tesztjei.

### Metódusok

#### `test_permission_denied_error_can_be_raised()`

```python
def test_permission_denied_error_can_be_raised(self) -> None
```

Teszteli, hogy a jogosultság megtagadva hiba dobható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_permission_denied_error_inheritance()`

```python
def test_permission_denied_error_inheritance(self) -> None
```

Teszteli az öröklődést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_permission_denied_error_message()`

```python
def test_permission_denied_error_message(self) -> None
```

Teszteli a hibaüzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/base/exceptions/test_base_error.py`](../../tests/neural_ai/core/base/exceptions/test_base_error.py)
