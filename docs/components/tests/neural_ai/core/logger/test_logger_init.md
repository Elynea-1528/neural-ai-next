# tests/neural_ai/core/logger/test_logger_init.py

Logger __init__.py export tesztjei.

## Importok

```python
from unittest.mock import patch
from neural_ai.core.logger import ColoredLogger
from neural_ai.core.logger import DefaultLogger
from neural_ai.core.logger import LoggerConfigurationError
from neural_ai.core.logger import LoggerError
from neural_ai.core.logger import LoggerFactory
from neural_ai.core.logger import LoggerFactoryInterface
from neural_ai.core.logger import LoggerInitializationError
from neural_ai.core.logger import LoggerInterface
from neural_ai.core.logger import RotatingFileLogger
# ... és még 8 import
```

## Osztály: `TestLoggerInitExports`

Logger modul exportjainak tesztelése.

### Metódusok

#### `test_version_export()`

```python
def test_version_export(self) -> None
```

Verziószám exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_schema_version_export()`

```python
def test_schema_version_export(self) -> None
```

Sémaverzió exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_interface_export()`

```python
def test_logger_interface_export(self) -> None
```

LoggerInterface exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_factory_interface_export()`

```python
def test_logger_factory_interface_export(self) -> None
```

LoggerFactoryInterface exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_factory_export()`

```python
def test_logger_factory_export(self) -> None
```

LoggerFactory exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_colored_logger_export()`

```python
def test_colored_logger_export(self) -> None
```

ColoredLogger exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_default_logger_export()`

```python
def test_default_logger_export(self) -> None
```

DefaultLogger exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_rotating_file_logger_export()`

```python
def test_rotating_file_logger_export(self) -> None
```

RotatingFileLogger exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_error_export()`

```python
def test_logger_error_export(self) -> None
```

LoggerError exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_configuration_error_export()`

```python
def test_logger_configuration_error_export(self) -> None
```

LoggerConfigurationError exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_initialization_error_export()`

```python
def test_logger_initialization_error_export(self) -> None
```

LoggerInitializationError exportálásának ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_exports_in_all_list()`

```python
def test_all_exports_in_all_list(self) -> None
```

Minden export szerepel a __all__ listában.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_import_all_from_logger()`

```python
def test_import_all_from_logger(self) -> None
```

Az összes export importálható a __all__ listából.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_version_fallback_on_package_not_found()`

```python
def test_version_fallback_on_package_not_found(self, mock_version) -> None
```

Teszteli a fallback mechanizmust, ha a csomag nincs telepítve.

**Paraméterek:**

- **`self`**
- **`mock_version`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/test_logger_init.py`](../../tests/neural_ai/core/logger/test_logger_init.py)
