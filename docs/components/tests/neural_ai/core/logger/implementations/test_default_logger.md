# tests/neural_ai/core/logger/implementations/test_default_logger.py

Default logger implementáció tesztei.

## Importok

```python
import logging
import pytest
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
```

## Osztály: `TestDefaultLogger`

DefaultLogger osztály tesztei.

### Metódusok

#### `test_init_basic()`

```python
def test_init_basic(self) -> None
```

Alap logger inicializálás tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_custom_level()`

```python
def test_init_with_custom_level(self) -> None
```

Logger inicializálás egyéni szinttel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_debug_logging()`

```python
def test_debug_logging(self, capsys: pytest.CaptureFixture[str]) -> None
```

Debug üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`capsys`** (`pytest.CaptureFixture[str]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_info_logging()`

```python
def test_info_logging(self, capsys: pytest.CaptureFixture[str]) -> None
```

Info üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`capsys`** (`pytest.CaptureFixture[str]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_warning_logging()`

```python
def test_warning_logging(self, capsys: pytest.CaptureFixture[str]) -> None
```

Warning üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`capsys`** (`pytest.CaptureFixture[str]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_error_logging()`

```python
def test_error_logging(self, capsys: pytest.CaptureFixture[str]) -> None
```

Error üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`capsys`** (`pytest.CaptureFixture[str]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_critical_logging()`

```python
def test_critical_logging(self, capsys: pytest.CaptureFixture[str]) -> None
```

Critical üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`capsys`** (`pytest.CaptureFixture[str]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_level()`

```python
def test_set_level(self) -> None
```

Log szint módosításának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_di_dependencies_none()`

```python
def test_di_dependencies_none(self) -> None
```

DI függőségek None értékkel történő elfogadásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/implementations/test_default_logger.py`](../../tests/neural_ai/core/logger/implementations/test_default_logger.py)
