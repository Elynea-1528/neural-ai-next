# tests/neural_ai/core/db/test_db_init.py

Tesztek a neural_ai.core.db.__init__ modulhoz.

Ez a modul teszteli, hogy a __init__.py fájlban exportált osztályok és függvények
helyesen importálhatók-e.

## Importok

```python
from neural_ai.core.db import Base
from neural_ai.core.db import DatabaseFactory
from neural_ai.core.db import DatabaseManager
from neural_ai.core.db import DynamicConfig
from neural_ai.core.db import LogEntry
from neural_ai.core.db import close_db
from neural_ai.core.db import create_engine
from neural_ai.core.db import get_async_session_maker
from neural_ai.core.db import get_database_url
from neural_ai.core.db import get_db_session
# ... és még 3 import
```

## Osztály: `TestDbInit`

Teszt osztály a neural_ai.core.db.__init__ modulhoz.

### Metódusok

#### `test_base_import()`

```python
def test_base_import(self) -> None
```

Teszteli, hogy a Base osztály importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_models_import()`

```python
def test_models_import(self) -> None
```

Teszteli, hogy a model osztályok importálhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_session_functions_import()`

```python
def test_session_functions_import(self) -> None
```

Teszteli, hogy a session függvények importálhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_classes_import()`

```python
def test_classes_import(self) -> None
```

Teszteli, hogy az osztályok importálhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_helper_functions_import()`

```python
def test_helper_functions_import(self) -> None
```

Teszteli, hogy a segédfüggvények importálhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_imports_are_callable()`

```python
def test_all_imports_are_callable(self) -> None
```

Teszteli, hogy az importált függvények hívhatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_imports_are_not_none()`

```python
def test_all_imports_are_not_none(self) -> None
```

Teszteli, hogy az összes importált objektum nem None.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_model_base_relationship()`

```python
def test_model_base_relationship(self) -> None
```

Teszteli, hogy a modellek a Base osztályból származnak-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/test_db_init.py`](../../tests/neural_ai/core/db/test_db_init.py)
