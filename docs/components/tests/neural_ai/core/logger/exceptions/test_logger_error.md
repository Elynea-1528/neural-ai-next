# tests/neural_ai/core/logger/exceptions/test_logger_error.py

Logger error exception tesztek.

## Importok

```python
import pytest
from neural_ai.core.logger.exceptions.logger_error import LoggerConfigurationError
from neural_ai.core.logger.exceptions.logger_error import LoggerError
from neural_ai.core.logger.exceptions.logger_error import LoggerInitializationError
```

## Osztály: `TestLoggerError`

LoggerError osztály tesztei.

### Metódusok

#### `test_logger_error_is_exception()`

```python
def test_logger_error_is_exception(self) -> None
```

LoggerError Exception-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_error_can_be_raised()`

```python
def test_logger_error_can_be_raised(self) -> None
```

LoggerError kiváltható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_error_has_message()`

```python
def test_logger_error_has_message(self) -> None
```

LoggerError tartalmaz üzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_error_without_message()`

```python
def test_logger_error_without_message(self) -> None
```

LoggerError hozható létre üzenet nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLoggerConfigurationError`

LoggerConfigurationError osztály tesztei.

### Metódusok

#### `test_logger_configuration_error_is_logger_error()`

```python
def test_logger_configuration_error_is_logger_error(self) -> None
```

LoggerConfigurationError LoggerError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_configuration_error_can_be_raised()`

```python
def test_logger_configuration_error_can_be_raised(self) -> None
```

LoggerConfigurationError kiváltható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_configuration_error_has_message()`

```python
def test_logger_configuration_error_has_message(self) -> None
```

LoggerConfigurationError tartalmaz üzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_configuration_error_without_message()`

```python
def test_logger_configuration_error_without_message(self) -> None
```

LoggerConfigurationError hozható létre üzenet nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLoggerInitializationError`

LoggerInitializationError osztály tesztei.

### Metódusok

#### `test_logger_initialization_error_is_logger_error()`

```python
def test_logger_initialization_error_is_logger_error(self) -> None
```

LoggerInitializationError LoggerError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_initialization_error_can_be_raised()`

```python
def test_logger_initialization_error_can_be_raised(self) -> None
```

LoggerInitializationError kiváltható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_initialization_error_has_message()`

```python
def test_logger_initialization_error_has_message(self) -> None
```

LoggerInitializationError tartalmaz üzenetet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_initialization_error_without_message()`

```python
def test_logger_initialization_error_without_message(self) -> None
```

LoggerInitializationError hozható létre üzenet nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLoggerErrorHierarchy`

Logger error hierarchia tesztek.

### Metódusok

#### `test_logger_error_hierarchy()`

```python
def test_logger_error_hierarchy(self) -> None
```

A kivételek helyes hierarchiát alkotnak.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_catch_logger_error_catches_subclasses()`

```python
def test_catch_logger_error_catches_subclasses(self) -> None
```

LoggerError elkapja az összes alosztályt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `raise_config_error()`

```python
def raise_config_error() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `raise_init_error()`

```python
def raise_init_error() -> None
```

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/exceptions/test_logger_error.py`](../../tests/neural_ai/core/logger/exceptions/test_logger_error.py)
