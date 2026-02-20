# tests/neural_ai/core/db/implementations/test_models.py

Tesztek a neural_ai.core.db.implementations.models modulhoz.

Ez a modul tartalmazza a DynamicConfig és LogEntry modellek tesztjeit,
100% kódfedettségi célkitűzéssel.

## Importok

```python
from collections.abc import Generator
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from neural_ai.core.db.implementations.model_base import Base
from neural_ai.core.db.implementations.models import DynamicConfig
from neural_ai.core.db.implementations.models import LogEntry
# ... és még 1 import
```

## Osztály: `TestDynamicConfig`

DynamicConfig modell tesztjei.

### Metódusok

#### `engine()`

```python
def engine(self) -> Engine
```

In-memory SQLite engine létrehozása teszteléshez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Engine`

#### `session()`

```python
def session(self, engine: Engine) -> Generator[Session, None, None]
```

Adatbázis munkamenet létrehozása.

**Paraméterek:**

- **`self`**
- **`engine`** (`Engine`)

**Visszatérési érték:**

- Típus: `Generator[Session, None, None]`

#### `test_dynamic_config_creation()`

```python
def test_dynamic_config_creation(self, session: Session) -> None
```

DynamicConfig létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_default_values()`

```python
def test_dynamic_config_default_values(self, session: Session) -> None
```

DynamicConfig alapértelmezett értékeinek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_repr()`

```python
def test_dynamic_config_repr(self, session: Session) -> None
```

DynamicConfig __repr__ metódusának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_to_dict()`

```python
def test_dynamic_config_to_dict(self, session: Session) -> None
```

DynamicConfig to_dict metódusának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_unique_key()`

```python
def test_dynamic_config_unique_key(self, session: Session) -> None
```

DynamicConfig egyedi kulcsának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_different_value_types()`

```python
def test_dynamic_config_different_value_types(self, session: Session) -> None
```

DynamicConfig különböző értéktípusokkal való tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_json_serialization()`

```python
def test_dynamic_config_json_serialization(self, session: Session) -> None
```

DynamicConfig JSON értékének szerializálásának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLogEntry`

LogEntry modell tesztjei.

### Metódusok

#### `engine()`

```python
def engine(self) -> Engine
```

In-memory SQLite engine létrehozása teszteléshez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Engine`

#### `session()`

```python
def session(self, engine: Engine) -> Generator[Session, None, None]
```

Adatbázis munkamenet létrehozása.

**Paraméterek:**

- **`self`**
- **`engine`** (`Engine`)

**Visszatérési érték:**

- Típus: `Generator[Session, None, None]`

#### `test_log_entry_creation()`

```python
def test_log_entry_creation(self, session: Session) -> None
```

LogEntry létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_optional_fields()`

```python
def test_log_entry_optional_fields(self, session: Session) -> None
```

LogEntry opcionális mezőinek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_repr()`

```python
def test_log_entry_repr(self, session: Session) -> None
```

LogEntry __repr__ metódusának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_to_dict()`

```python
def test_log_entry_to_dict(self, session: Session) -> None
```

LogEntry to_dict metódusának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_different_levels()`

```python
def test_log_entry_different_levels(self, session: Session) -> None
```

LogEntry különböző naplózási szintek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_extra_data_types()`

```python
def test_log_entry_extra_data_types(self, session: Session) -> None
```

LogEntry extra_data különböző típusainak tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_long_message()`

```python
def test_log_entry_long_message(self, session: Session) -> None
```

LogEntry hosszú üzenetének tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_exception_data()`

```python
def test_log_entry_exception_data(self, session: Session) -> None
```

LogEntry kivétel adatokkal való tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestModelRelationships`

Modellek közötti kapcsolatok tesztelése.

### Metódusok

#### `engine()`

```python
def engine(self) -> Engine
```

In-memory SQLite engine létrehozása teszteléshez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Engine`

#### `session()`

```python
def session(self, engine: Engine) -> Generator[Session, None, None]
```

Adatbázis munkamenet létrehozása.

**Paraméterek:**

- **`self`**
- **`engine`** (`Engine`)

**Visszatérési érték:**

- Típus: `Generator[Session, None, None]`

#### `test_multiple_models_same_session()`

```python
def test_multiple_models_same_session(self, session: Session) -> None
```

Több modell egy munkamenetben való használatának tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_model_timestamps()`

```python
def test_model_timestamps(self, session: Session) -> None
```

Modellek időbélyegeinek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_model_deletion()`

```python
def test_model_deletion(self, session: Session) -> None
```

Modellek törlésének tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestModelValidation`

Modell validáció tesztelése.

### Metódusok

#### `engine()`

```python
def engine(self) -> Engine
```

In-memory SQLite engine létrehozása teszteléshez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Engine`

#### `session()`

```python
def session(self, engine: Engine) -> Generator[Session, None, None]
```

Adatbázis munkamenet létrehozása.

**Paraméterek:**

- **`self`**
- **`engine`** (`Engine`)

**Visszatérési érték:**

- Típus: `Generator[Session, None, None]`

#### `test_dynamic_config_nullable_fields()`

```python
def test_dynamic_config_nullable_fields(self, session: Session) -> None
```

DynamicConfig nem nullázható mezőinek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_nullable_fields()`

```python
def test_log_entry_nullable_fields(self, session: Session) -> None
```

LogEntry nem nullázható mezőinek tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_dynamic_config_string_length_limits()`

```python
def test_dynamic_config_string_length_limits(self, session: Session) -> None
```

DynamicConfig string mezőinek hosszkorlátainak tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_log_entry_string_length_limits()`

```python
def test_log_entry_string_length_limits(self, session: Session) -> None
```

LogEntry string mezőinek hosszkorlátainak tesztelése.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/implementations/test_models.py`](../../tests/neural_ai/core/db/implementations/test_models.py)
