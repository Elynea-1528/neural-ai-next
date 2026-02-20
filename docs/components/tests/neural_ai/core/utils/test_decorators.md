# tests/neural_ai/core/utils/test_decorators.py

Tesztek a neural_ai.core.utils.decorators modulhoz.

Ez a modul tartalmazza a @trace dekorátor tesztjeit, beleértve a
normál működést, hibakezelést, argumentum szerializálást és teljesítményt.

## Importok

```python
import time
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core.utils.decorators import trace
```

## Osztály: `TestTraceDecorator`

Tesztek a @trace dekorátorhoz.

### Metódusok

#### `test_trace_successful_execution()`

```python
def test_trace_successful_execution(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a sikeres függvényhívás logolását.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `add()`

```python
def add(a: int, b: int) -> int
```

**Paraméterek:**

- **`a`** (`int`)
- **`b`** (`int`)

**Visszatérési érték:**

- Típus: `int`

#### `test_trace_with_kwargs()`

```python
def test_trace_with_kwargs(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a kulcsszavas argumentumokkal történő hívást.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `multiply()`

```python
def multiply(a: int, b: int, factor: int = 1) -> int
```

**Paraméterek:**

- **`a`** (`int`)
- **`b`** (`int`)
- **`factor`** (`int`) = `1`

**Visszatérési érték:**

- Típus: `int`

#### `test_trace_with_unsafe_args()`

```python
def test_trace_with_unsafe_args(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a nem biztonságos argumentumok logolását.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `process_data()`

```python
def process_data(data: Any) -> str
```

**Paraméterek:**

- **`data`** (`Any`)

**Visszatérési érték:**

- Típus: `str`

#### `test_trace_function_name_preserved()`

```python
def test_trace_function_name_preserved(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli, hogy a függvény neve megőrződik a dekorálás után.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `my_custom_function()`

```python
def my_custom_function() -> str
```

**Visszatérési érték:**

- Típus: `str`

#### `test_trace_docstring_preserved()`

```python
def test_trace_docstring_preserved(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli, hogy a függvény docstringje megőrződik.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `documented_function()`

```python
def documented_function() -> None
```

Ez egy dokumentált függvény.

**Visszatérési érték:**

- Típus: `None`

#### `test_trace_exception_handling()`

```python
def test_trace_exception_handling(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a kivételkezelést és logolást.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `failing_function()`

```python
def failing_function() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `test_trace_call_id_uniqueness()`

```python
def test_trace_call_id_uniqueness(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli, hogy minden hívás egyedi call_id-t kap.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `simple_function()`

```python
def simple_function() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `test_trace_duration_measurement()`

```python
def test_trace_duration_measurement(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a futási idő mérésének helyességét.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `slow_function()`

```python
def slow_function() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `test_trace_with_mixed_args()`

```python
def test_trace_with_mixed_args(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a vegyes típusú argumentumok kezelését.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mixed_function()`

```python
def mixed_function(safe: str, unsafe: list[int], safe_num: int) -> str
```

**Paraméterek:**

- **`safe`** (`str`)
- **`unsafe`** (`list[int]`)
- **`safe_num`** (`int`)

**Visszatérési érték:**

- Típus: `str`

#### `test_trace_no_args_function()`

```python
def test_trace_no_args_function(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli az argumentumok nélküli függvényt.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `no_args_function()`

```python
def no_args_function() -> str
```

**Visszatérési érték:**

- Típus: `str`

#### `test_trace_with_safe_types()`

```python
def test_trace_with_safe_types(self, mock_ensure_logger: MagicMock) -> None
```

Teszteli a biztonságos típusok logolását.

**Paraméterek:**

- **`self`**
- **`mock_ensure_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `safe_types_function()`

```python
def safe_types_function(s: str, i: int, f: float, b: bool) -> None
```

**Paraméterek:**

- **`s`** (`str`)
- **`i`** (`int`)
- **`f`** (`float`)
- **`b`** (`bool`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestTraceDecoratorIntegration`

Integrációs tesztek a @trace dekorátorhoz.

### Metódusok

#### `test_trace_real_logger()`

```python
def test_trace_real_logger(self) -> None
```

Teszteli a dekorátort valós loggerrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `integration_test_function()`

```python
def integration_test_function(x: int, y: int) -> int
```

**Paraméterek:**

- **`x`** (`int`)
- **`y`** (`int`)

**Visszatérési érték:**

- Típus: `int`

#### `test_trace_performance_overhead()`

```python
def test_trace_performance_overhead(self) -> None
```

Teszteli a dekorátor teljesítménybeli hatását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `fast_function()`

```python
def fast_function() -> int
```

**Visszatérési érték:**

- Típus: `int`

---

**Forrásfájl:** [`tests/neural_ai/core/utils/test_decorators.py`](../../tests/neural_ai/core/utils/test_decorators.py)
