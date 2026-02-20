# tests/neural_ai/processors/test_time_alignment_service.py

TimeAlignmentService tesztek.

## Importok

```python
from collections.abc import Mapping
from decimal import Decimal
from typing import Any
from typing import AnyStr
import polars
import pytest
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.implementations.time_alignment_service import TimeAlignmentService
```

## Osztály: `MockLogger(LoggerInterface)`

Mock logger implementáció a teszteléshez.

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, config: Any | None = None) -> None
```

Inicializálás.

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

Debug üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

Info üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

Warning üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

Error üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

Critical üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

Log szint beállítása.

**Paraméterek:**

- **`self`**
- **`level`** (`int`)

**Visszatérési érték:**

- Típus: `None`

#### `get_level()`

```python
def get_level(self) -> int
```

Log szint lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

## Osztály: `TestTimeAlignmentService`

TimeAlignmentService osztály tesztei.

### Metódusok

#### `mock_logger()`

```python
def mock_logger(self) -> MockLogger
```

Mock logger fixture.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MockLogger`

#### `service()`

```python
def service(self, mock_logger: MockLogger) -> TimeAlignmentService
```

TimeAlignmentService fixture.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `TimeAlignmentService`

#### `test_init()`

```python
def test_init(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

Inicializálás teszt.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_reindex_to_grid_tick()`

```python
def test_reindex_to_grid_tick(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

reindex_to_grid tick esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_reindex_to_grid_minute()`

```python
def test_reindex_to_grid_minute(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

reindex_to_grid perc esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_market_hours_filter()`

```python
def test_market_hours_filter(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

market_hours_filter teszt.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_handle_gaps_tick()`

```python
def test_handle_gaps_tick(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

handle_gaps tick esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_handle_gaps_forward_fill()`

```python
def test_handle_gaps_forward_fill(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

handle_gaps forward_fill esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_handle_gaps_mask()`

```python
def test_handle_gaps_mask(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

handle_gaps mask esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

#### `test_handle_gaps_unknown_method()`

```python
def test_handle_gaps_unknown_method(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None
```

handle_gaps ismeretlen method esetében.

**Paraméterek:**

- **`self`**
- **`service`** (`TimeAlignmentService`)
- **`mock_logger`** (`MockLogger`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/processors/test_time_alignment_service.py`](../../tests/neural_ai/processors/test_time_alignment_service.py)
