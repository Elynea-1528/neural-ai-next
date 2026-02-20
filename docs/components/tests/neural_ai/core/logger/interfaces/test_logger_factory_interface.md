# tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py

Logger factory interfész tesztek.

## Importok

```python
import pytest
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
```

## Osztály: `TestLoggerFactoryInterface`

LoggerFactoryInterface osztály tesztei.

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

#### `test_register_logger_raises_not_implemented()`

```python
def test_register_logger_raises_not_implemented(self) -> None
```

register_logger metódus NotImplementedError-t dob. Ez a teszt lefedi a 35. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_logger_raises_not_implemented()`

```python
def test_get_logger_raises_not_implemented(self) -> None
```

get_logger metódus NotImplementedError-t dob. Ez a teszt lefedi a 54. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_raises_not_implemented()`

```python
def test_configure_raises_not_implemented(self) -> None
```

configure metódus NotImplementedError-t dob. Ez a teszt lefedi a 67. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py`](../../tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py)
