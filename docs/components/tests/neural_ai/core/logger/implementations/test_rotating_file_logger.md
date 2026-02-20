# tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py

Rotating file logger implementáció tesztei.

## Importok

```python
import logging
import tempfile
from pathlib import Path
import pytest
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger
import io
```

## Osztály: `TestRotatingFileLogger`

RotatingFileLogger osztály tesztei.

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

#### `test_init_without_file_raises_error()`

```python
def test_init_without_file_raises_error(self) -> None
```

Logger inicializálás fájl nélkül hibát dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_empty_file_raises_error()`

```python
def test_init_with_empty_file_raises_error(self) -> None
```

Logger inicializálás üres fájlnévvel hibát dob. Ez a teszt lefedi a 60. sort, ahol a ValueError-t dobjuk.

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

#### `test_init_creates_directory()`

```python
def test_init_creates_directory(self) -> None
```

Logger létrehozza a könyvtárat, ha az nem létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_debug_logging()`

```python
def test_debug_logging(self) -> None
```

Debug üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_debug_logging_without_kwargs()`

```python
def test_debug_logging_without_kwargs(self) -> None
```

Debug üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 106. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_info_logging()`

```python
def test_info_logging(self) -> None
```

Info üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_info_logging_without_kwargs()`

```python
def test_info_logging_without_kwargs(self) -> None
```

Info üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 118. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_warning_logging()`

```python
def test_warning_logging(self) -> None
```

Warning üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_warning_logging_without_kwargs()`

```python
def test_warning_logging_without_kwargs(self) -> None
```

Warning üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 130. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_error_logging()`

```python
def test_error_logging(self) -> None
```

Error üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_error_logging_without_kwargs()`

```python
def test_error_logging_without_kwargs(self) -> None
```

Error üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 142. sort.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_critical_logging()`

```python
def test_critical_logging(self) -> None
```

Critical üzenet logolásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_critical_logging_without_kwargs()`

```python
def test_critical_logging_without_kwargs(self) -> None
```

Critical üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 154. sort.

**Paraméterek:**

- **`self`**

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

#### `test_invalid_rotation_type_raises_error()`

```python
def test_invalid_rotation_type_raises_error(self) -> None
```

Érvénytelen rotáció típus hibát dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_time_based_rotation()`

```python
def test_time_based_rotation(self) -> None
```

Időalapú rotáció tesztelése. Ez a teszt lefedi a 75. sort, ahol a TimedRotatingFileHandler-t hozzuk létre.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_clean_old_logs()`

```python
def test_clean_old_logs(self) -> None
```

Régi log fájlok törlésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_existing_handlers_removed()`

```python
def test_existing_handlers_removed(self) -> None
```

Teszteli, hogy a meglévő handlerek eltávolításra kerülnek. Ez a teszt lefedi a 56. sort, ahol a meglévő handlerek eltávolítása történik.

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

**Forrásfájl:** [`tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py`](../../tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py)
