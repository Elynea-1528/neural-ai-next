# neural_ai/core/utils/decorators.py

Funkcionális dekorátorok a Neural AI Next rendszerhez.

Ez a modul a rendszer által használt dekorátorokat tartalmazza, beleértve
a `@trace` dekorátort, amely funkcióhívások nyomon követését és logolását
teszi lehetővé structlog segítségével.

## Importok

```python
import time
import uuid
from collections.abc import Callable
from functools import wraps
from typing import Any
from typing import TypeVar
from typing import cast
from neural_ai.core.logger.factory import LoggerFactory
```

## Konstansok

- **`F`**
: `TypeVar('F', bound=Callable[..., Any])`


- **`R`**
: `TypeVar('R')`


- **`_trace_logger`**
: `None`


- **`_trace_logger`**
: `_get_trace_logger()`


- **`_SAFE_TYPES`**
: `(str, int, float, bool, type(None))`


- **`call_id`**
: `str(uuid.uuid4())`


- **`start_time`**
: `time.perf_counter()`


- **`result`**
: `func(*args, **kwargs)`


- **`duration_ms`**
: `(time.perf_counter() - start_time) * 1000`


- **`duration_ms`**
: `(time.perf_counter() - start_time) * 1000`


### `_get_trace_logger()`

```python
def _get_trace_logger() -> Any
```

**Visszatérési érték:**

- Típus: `Any`

### `_ensure_trace_logger()`

```python
def _ensure_trace_logger() -> Any
```

**Visszatérési érték:**

- Típus: `Any`

### `_serialize_arg()`

```python
def _serialize_arg(arg: Any) -> str
```

Egy argumentum biztonságos szöveges reprezentációját adja vissza. Csak biztonságos típusokat (str, int, float, bool, None) konvertál közvetlenül, minden egyéb típus esetén "UNSAFE_ARG" értéket ad vissza.

**Paraméterek:**

- **`arg`** (`Any`): A konvertálandó argumentum.

**Visszatérési érték:**

- Típus: `str`
- Az argumentum szöveges reprezentációja, vagy "UNSAFE_ARG" ha a típus nem biztonságos.

### `trace()`

```python
def trace(func: Callable[P, R]) -> Callable[P, R]
```

Dekorátor a funkcióhívások nyomon követéséhez és logolásához. A dekorátor minden függvényhíváskor logolja a következő információkat: - call_id: Egyedi azonosító (UUID4) - function: A hívott függvény neve - args: A függvény argumentumainak biztonságos reprezentációja - duration_ms: A függvény futási ideje milliszekundumban A logolás DEBUG szinten történik a "neural_ai.trace" loggeren keresztül.

**Paraméterek:**

- **`func`** (`Callable[P, R]`): A dekorálandó függvény.

**Visszatérési érték:**

- Típus: `Callable[P, R]`
- A dekorált függvény, amely automatikusan logolja a hívásokat.

**Példák:**

```python
    >>> @trace
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    ...
    >>> result = add(5, 3)
    # Log output:
    # call_id=... function=add args=['5', '3'] duration_ms=0.123
```

### `wrapper()`

```python
def wrapper() -> Any
```

A dekorált függvényt becsomagoló wrapper függvény.

**Visszatérési érték:**

- Típus: `Any`
- A dekorált függvény visszatérési értéke.

---

**Forrásfájl:** [`neural_ai/core/utils/decorators.py`](../../neural_ai/core/utils/decorators.py)
