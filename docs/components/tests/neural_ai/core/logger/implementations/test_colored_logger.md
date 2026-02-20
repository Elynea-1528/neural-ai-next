# tests/neural_ai/core/logger/implementations/test_colored_logger.py

Colored logger implementáció tesztei.

## Importok

```python
import logging
import pytest
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
import io
import sys
import io
import sys
import io
import sys
import io
# ... és még 4 import
```

## Osztály: `TestColoredLogger`

ColoredLogger osztály tesztei.

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
def test_debug_logging(self, monkeypatch: pytest.MonkeyPatch) -> None
```

Debug üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `test_info_logging()`

```python
def test_info_logging(self, monkeypatch: pytest.MonkeyPatch) -> None
```

Info üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `test_warning_logging()`

```python
def test_warning_logging(self, monkeypatch: pytest.MonkeyPatch) -> None
```

Warning üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `test_error_logging()`

```python
def test_error_logging(self, monkeypatch: pytest.MonkeyPatch) -> None
```

Error üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `test_critical_logging()`

```python
def test_critical_logging(self, monkeypatch: pytest.MonkeyPatch) -> None
```

Critical üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**
- **`monkeypatch`** (`pytest.MonkeyPatch`)

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

#### `test_logger_name()`

```python
def test_logger_name(self) -> None
```

Logger nevének ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_colored_formatter_present()`

```python
def test_colored_formatter_present(self) -> None
```

Színes formázó jelenlétének ellenőrzése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_existing_handlers_removed()`

```python
def test_existing_handlers_removed(self) -> None
```

Teszteli, hogy a meglévő handlerek eltávolításra kerülnek. Ez a teszt lefedi a 54-55. sorokat, ahol a meglévő handlerek eltávolítása történik, hogy ne legyenek duplikált üzenetek.

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

**Forrásfájl:** [`tests/neural_ai/core/logger/implementations/test_colored_logger.py`](../../tests/neural_ai/core/logger/implementations/test_colored_logger.py)
