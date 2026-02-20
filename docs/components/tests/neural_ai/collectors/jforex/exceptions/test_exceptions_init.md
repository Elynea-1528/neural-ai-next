# tests/neural_ai/collectors/jforex/exceptions/test_exceptions_init.py

Tests for JForex exceptions __init__.py exports.

## Importok

```python
from neural_ai.collectors.jforex.exceptions import DataNotAvailableError
from neural_ai.collectors.jforex.exceptions import DecodeError
from neural_ai.collectors.jforex.exceptions import DownloadError
from neural_ai.collectors.jforex.exceptions import JForexError
```

## Osztály: `TestJForexExceptionsInit`

Test cases for JForex exceptions exports.

### Metódusok

#### `test_jforexerror_exported()`

```python
def test_jforexerror_exported(self) -> None
```

Test that JForexError is exported.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_downloaderror_exported()`

```python
def test_downloaderror_exported(self) -> None
```

Test that DownloadError is exported.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_decodeerror_exported()`

```python
def test_decodeerror_exported(self) -> None
```

Test that DecodeError is exported.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_datanotavailableerror_exported()`

```python
def test_datanotavailableerror_exported(self) -> None
```

Test that DataNotAvailableError is exported.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exception_instantiation()`

```python
def test_exception_instantiation(self) -> None
```

Test that exceptions can be instantiated with messages.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/collectors/jforex/exceptions/test_exceptions_init.py`](../../tests/neural_ai/collectors/jforex/exceptions/test_exceptions_init.py)
