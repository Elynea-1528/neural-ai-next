# tests/neural_ai/core/logger/interfaces/test_logger_interface.py

Logger interfész tesztek.

## Importok

```python
from collections.abc import Mapping
from typing import Any
from typing import AnyStr
import pytest
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Konstansok

- **`mock_logger`**
: `MockLogger('test_logger')`


- **`level`**
: `mock_logger.get_level()`


## Osztály: `MockLogger(LoggerInterface)`

Mock logger implementáció a teszteléshez.

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, config: Any | None = None) -> None
```

**Paraméterek:**

- **`self`**
- **`name`** (`str`)
- **`config`** (`Any | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `debug()`

```python
def debug(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

**Paraméterek:**

- **`self`**
- **`level`** (`int`)

**Visszatérési érték:**

- Típus: `None`

#### `get_level()`

```python
def get_level(self) -> int
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

## Osztály: `TestLoggerInterface`

LoggerInterface osztály tesztei.

### Metódusok

#### `test_interface_is_abstract()`

```python
def test_interface_is_abstract(self) -> None
```

Interfész absztrakt osztály-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_has_required_methods()`

```python
def test_interface_has_required_methods(self) -> None
```

Interfész tartalmazza a szükséges metódusokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_abstract_methods_implemented()`

```python
def test_all_abstract_methods_implemented(self) -> None
```

Összes absztrakt metódus implementálva van-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/interfaces/test_logger_interface.py`](../../tests/neural_ai/core/logger/interfaces/test_logger_interface.py)
