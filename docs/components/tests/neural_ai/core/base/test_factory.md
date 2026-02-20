# tests/neural_ai/core/base/test_factory.py

CoreComponentFactory tesztelése.

Ez a modul tartalmazza a CoreComponentFactory osztály egységtesztjeit,
beleértve a lazy loading, dependency injection és komponens létrehozási
funkcionalitás tesztelését.

## Importok

```python
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core.base.exceptions import ConfigurationError
from neural_ai.core.base.exceptions import DependencyError
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.factory import DEFAULT_CONFIG_FILE
# ... és még 30 import
```

## Konstansok

- **`mock_logger`**
: `DummyLogger(name='test')`


- **`logger`**
: `factory.logger`


- **`_`**
: `factory.config_manager`


- **`_`**
: `factory.storage`


- **`mock_logger`**
: `MagicMock(spec=LoggerInterface)`


- **`logger1`**
: `factory.logger`


- **`logger2`**
: `factory.logger`


- **`components`**
: `CoreComponentFactory.create_components(config_path=str(config_path), log_path=str(log_path), storage_path=str(storage_path))`


- **`components`**
: `CoreComponentFactory.create_components()`


- **`components`**
: `CoreComponentFactory.create_with_container(container)`


- **`mock_config`**
: `MagicMock()`


- **`components`**
: `CoreComponentFactory.create_minimal()`


- **`components`**
: `CoreComponentFactory.create_minimal()`


- **`mock_config`**
: `MagicMock()`


- **`components`**
: `CoreComponentFactory.create_minimal()`


- **`logger`**
: `CoreComponentFactory.create_logger('test_logger', {'level': 'INFO'})`


- **`config`**
: `CoreComponentFactory.create_config_manager(temp_file, {})`


- **`mock_config`**
: `MagicMock()`


- **`mock_logger`**
: `MagicMock()`


- **`mock_event_bus`**
: `MagicMock()`


- **`storage`**
: `CoreComponentFactory.create_storage(temp_dir, mock_logger, mock_config)`


- **`mock_logger`**
: `MagicMock()`


- **`mock_config`**
: `MagicMock()`


- **`cache1`**
: `factory._component_cache`


- **`cache2`**
: `factory._component_cache`


- **`logger`**
: `DefaultLogger(name='test')`


- **`result`**
: `factory._get_logger()`


- **`result`**
: `factory._get_logger()`


- **`invalid_logger`**
: `MagicMock()`


- **`mock_config`**
: `MagicMock(spec=ConfigManagerInterface)`


- **`result`**
: `factory._get_config_manager()`


- **`expensive_config1`**
: `factory._expensive_config`


- **`expensive_config2`**
: `factory._expensive_config`


- **`test_config`**
: `{'key': 'value'}`


- **`result`**
: `factory._process_config(test_config)`


- **`_`**
: `factory._expensive_config`


- **`lazy_attr_exists`**
: `hasattr(factory, '_lazy__expensive_config')`


- **`lazy_attr_exists_after`**
: `hasattr(factory, '_lazy__expensive_config')`


## Osztály: `DummyLogger(LoggerInterface)`

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str)
```

**Paraméterek:**

- **`self`**
- **`name`** (`str`)

#### `debug()`

```python
def debug(self, message: str)
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

#### `info()`

```python
def info(self, message: str)
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

#### `warning()`

```python
def warning(self, message: str)
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

#### `error()`

```python
def error(self, message: str)
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

#### `critical()`

```python
def critical(self, message: str)
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

#### `log()`

```python
def log(self, level: str, message: str)
```

**Paraméterek:**

- **`self`**
- **`level`** (`str`)
- **`message`** (`str`)

#### `set_level()`

```python
def set_level(self, level: int)
```

**Paraméterek:**

- **`self`**
- **`level`** (`int`)

#### `get_level()`

```python
def get_level(self) -> int
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

## Osztály: `TestCoreComponentFactory`

CoreComponentFactory osztály tesztjei.

### Metódusok

#### `test_init_with_container()`

```python
def test_init_with_container(self) -> None
```

Teszteli a factory inicializálását DI konténerrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_property_returns_logger()`

```python
def test_logger_property_returns_logger(self) -> None
```

Teszteli, hogy a logger property logger interfészt ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_config_manager_property_raises_dependency_error()`

```python
def test_config_manager_property_raises_dependency_error(self) -> None
```

Teszteli, hogy a config manager property DependencyError-t dob, ha nincs regisztrálva.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_storage_property_raises_dependency_error()`

```python
def test_storage_property_raises_dependency_error(self) -> None
```

Teszteli, hogy a storage property DependencyError-t dob, ha nincs regisztrálva.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_reset_lazy_loaders()`

```python
def test_reset_lazy_loaders(self) -> None
```

Teszteli a lazy loader-ek visszaállítását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_storage_missing_base_directory()`

```python
def test_validate_dependencies_storage_missing_base_directory(self) -> None
```

Teszteli a storage függőség validálását hiányzó base_path esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_storage_invalid_path()`

```python
def test_validate_dependencies_storage_invalid_path(self) -> None
```

Teszteli a storage függőség validálását érvénytelen elérési úttal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_storage_valid()`

```python
def test_validate_dependencies_storage_valid(self) -> None
```

Teszteli a storage függőség validálását érvényes konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_logger_missing_name()`

```python
def test_validate_dependencies_logger_missing_name(self) -> None
```

Teszteli a logger függőség validálását hiányzó névvel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_logger_valid()`

```python
def test_validate_dependencies_logger_valid(self) -> None
```

Teszteli a logger függőség validálását érvényes konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_config_manager_missing_path()`

```python
def test_validate_dependencies_config_manager_missing_path(self) -> None
```

Teszteli a config manager függőség validálását hiányzó fájlúttal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_config_manager_nonexistent_file()`

```python
def test_validate_dependencies_config_manager_nonexistent_file(self) -> None
```

Teszteli a config manager függőség validálását nem létező fájllal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_config_manager_valid()`

```python
def test_validate_dependencies_config_manager_valid(self) -> None
```

Teszteli a config manager függőség validálását érvényes konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_validate_dependencies_invalid_component_type()`

```python
def test_validate_dependencies_invalid_component_type(self) -> None
```

Teszteli a függőség validálását érvénytelen komponens típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_components_with_all_paths()`

```python
def test_create_components_with_all_paths(self, mock_file_storage: MagicMock, mock_get_logger: MagicMock, mock_get_manager: MagicMock) -> None
```

Teszteli a komponensek létrehozását minden elérési úttal.

**Paraméterek:**

- **`self`**
- **`mock_file_storage`** (`MagicMock`)
- **`mock_get_logger`** (`MagicMock`)
- **`mock_get_manager`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_components_without_paths()`

```python
def test_create_components_without_paths(self) -> None
```

Teszteli a komponensek létrehozását elérési utak nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_with_container()`

```python
def test_create_with_container(self) -> None
```

Teszteli a komponensek létrehozását meglévő konténerből.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_minimal_with_config_file()`

```python
def test_create_minimal_with_config_file(self, mock_get_logger: MagicMock, mock_get_manager: MagicMock) -> None
```

Teszteli a minimális komponensek létrehozását config fájllal.

**Paraméterek:**

- **`self`**
- **`mock_get_logger`** (`MagicMock`)
- **`mock_get_manager`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_minimal_without_config_file()`

```python
def test_create_minimal_without_config_file(self, mock_get_logger: MagicMock, mock_get_manager: MagicMock) -> None
```

Teszteli a minimális komponensek létrehozását config fájl nélkül.

**Paraméterek:**

- **`self`**
- **`mock_get_logger`** (`MagicMock`)
- **`mock_get_manager`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_minimal_with_config_file_no_logger_section()`

```python
def test_create_minimal_with_config_file_no_logger_section(self, mock_get_logger: MagicMock, mock_get_manager: MagicMock) -> None
```

Teszteli a komponensek létrehozását config fájllal, de logger section nélkül.

**Paraméterek:**

- **`self`**
- **`mock_get_logger`** (`MagicMock`)
- **`mock_get_manager`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_logger()`

```python
def test_create_logger(self, mock_get_logger: MagicMock) -> None
```

Teszteli a logger létrehozását.

**Paraméterek:**

- **`self`**
- **`mock_get_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_logger_invalid_config()`

```python
def test_create_logger_invalid_config(self) -> None
```

Teszteli a logger létrehozását érvénytelen konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_config_manager()`

```python
def test_create_config_manager(self, mock_get_manager: MagicMock) -> None
```

Teszteli a config manager létrehozását.

**Paraméterek:**

- **`self`**
- **`mock_get_manager`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_config_manager_invalid_path()`

```python
def test_create_config_manager_invalid_path(self) -> None
```

Teszteli a config manager létrehozását érvénytelen elérési úttal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_create_storage()`

```python
def test_create_storage(self, mock_get_manager: MagicMock, mock_get_logger: MagicMock, mock_get_event_bus: MagicMock) -> None
```

Teszteli a storage létrehozását.

**Paraméterek:**

- **`self`**
- **`mock_get_manager`** (`MagicMock`)
- **`mock_get_logger`** (`MagicMock`)
- **`mock_get_event_bus`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `test_create_storage_invalid_path()`

```python
def test_create_storage_invalid_path(self) -> None
```

Teszteli a storage létrehozását érvénytelen elérési úttal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_lazy_property_decorator_exists()`

```python
def test_lazy_property_decorator_exists(self) -> None
```

Teszteli, hogy a lazy property dekorátorok léteznek.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_component_cache_lazy_property()`

```python
def test_component_cache_lazy_property(self) -> None
```

Teszteli a komponens gyorsítótár lazy property működését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_logger_with_registered_logger()`

```python
def test_get_logger_with_registered_logger(self) -> None
```

Teszteli a _get_logger metódust regisztrált loggerrel (58-59. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_logger_fallback_to_default_logger_factory()`

```python
def test_get_logger_fallback_to_default_logger_factory(self) -> None
```

Teszteli, hogy a _get_logger metódus fallbackel a DefaultLoggerFactory-ra, ha a konténer None-t ad vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_logger_with_invalid_logger_raises_dependency_error()`

```python
def test_get_logger_with_invalid_logger_raises_dependency_error(self) -> None
```

Teszteli a _get_logger metódust érvénytelen loggerrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_config_manager_with_registered_config()`

```python
def test_get_config_manager_with_registered_config(self) -> None
```

Teszteli a _get_config_manager metódust regisztrált config managerrel (74-77. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_raises_dependency_error_if_not_found()`

```python
def test_get_storage_raises_dependency_error_if_not_found(self) -> None
```

Teszteli, hogy a _get_storage DependencyError-t dob, ha nincs regisztrálva.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_expensive_config_lazy_property()`

```python
def test_expensive_config_lazy_property(self) -> None
```

Teszteli az _expensive_config lazy property működését (111-114. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `isinstance_mock()`

```python
def isinstance_mock(obj: Any, class_or_tuple: Any) -> bool
```

**Paraméterek:**

- **`obj`** (`Any`)
- **`class_or_tuple`** (`Any`)

**Visszatérési érték:**

- Típus: `bool`

### `test_process_config()`

```python
def test_process_config(self) -> None
```

Teszteli a _process_config metódust (125. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_reset_lazy_loaders_clears_lazy_properties()`

```python
def test_reset_lazy_loaders_clears_lazy_properties(self) -> None
```

Teszteli, hogy a reset_lazy_loaders törli a lazy property-ket (146. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `isinstance_mock()`

```python
def isinstance_mock(obj: Any, class_or_tuple: Any) -> bool
```

**Paraméterek:**

- **`obj`** (`Any`)
- **`class_or_tuple`** (`Any`)

**Visszatérési érték:**

- Típus: `bool`

---

**Forrásfájl:** [`tests/neural_ai/core/base/test_factory.py`](../../tests/neural_ai/core/base/test_factory.py)
