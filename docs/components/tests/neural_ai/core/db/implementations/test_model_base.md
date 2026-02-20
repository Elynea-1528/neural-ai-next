# tests/neural_ai/core/db/implementations/test_model_base.py

Tesztek a model_base modulhoz.

Ez a modul tartalmazza a Base osztály és annak metódusainak tesztjeit.

## Importok

```python
from collections.abc import Generator
from datetime import datetime
import pytest
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
# ... és még 3 import
```

## Konstansok

- **`SessionLocal`**
: `sessionmaker(bind=engine)`


- **`session`**
: `SessionLocal()`


## Osztály: `DummyModel(Base)`

Teszt modell a Base osztály teszteléséhez.

## Osztály: `TestBase`

A Base osztály tesztjei.

### Metódusok

#### `test_base_initialization()`

```python
def test_base_initialization(self) -> None
```

Teszteli a Base osztály inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_id_column_properties()`

```python
def test_id_column_properties(self) -> None
```

Teszteli az id oszlop tulajdonságait.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_created_at_column_properties()`

```python
def test_created_at_column_properties(self) -> None
```

Teszteli a created_at oszlop tulajdonságait.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_updated_at_column_properties()`

```python
def test_updated_at_column_properties(self) -> None
```

Teszteli az updated_at oszlop tulajdonságait.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_automatic_tablename_generation()`

```python
def test_automatic_tablename_generation(self) -> None
```

Teszteli az automatikus táblanév generálást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_model_creation_with_defaults()`

```python
def test_model_creation_with_defaults(self, session: Session) -> None
```

Teszteli a modell létrehozását alapértelmezett értékekkel.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_to_dict_method()`

```python
def test_to_dict_method(self, session: Session) -> None
```

Teszteli a to_dict metódust.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_to_dict_datetime_isoformat()`

```python
def test_to_dict_datetime_isoformat(self, session: Session) -> None
```

Teszteli, hogy a datetime értékek ISO formátumban vannak-e.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_repr_method()`

```python
def test_repr_method(self, session: Session) -> None
```

Teszteli a __repr__ metódust.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_updated_at_changes_on_update()`

```python
def test_updated_at_changes_on_update(self, session: Session) -> None
```

Teszteli, hogy az updated_at módosul-e frissítéskor.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_created_at_does_not_change_on_update()`

```python
def test_created_at_does_not_change_on_update(self, session: Session) -> None
```

Teszteli, hogy a created_at ne változzon frissítéskor.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

#### `test_multiple_models_have_different_ids()`

```python
def test_multiple_models_have_different_ids(self, session: Session) -> None
```

Teszteli, hogy különböző modelleknek különböző id-ja van.

**Paraméterek:**

- **`self`**
- **`session`** (`Session`)

**Visszatérési érték:**

- Típus: `None`

### `engine()`

```python
def engine() -> Engine
```

In-memory SQLite engine létrehozása teszteléshez.

**Visszatérési érték:**

- Típus: `Engine`

### `session()`

```python
def session(engine: Engine) -> Generator[Session, None, None]
```

Teszt session létrehozása és törlése.

**Paraméterek:**

- **`engine`** (`Engine`)

**Visszatérési érték:**

- Típus: `Generator[Session, None, None]`

---

**Forrásfájl:** [`tests/neural_ai/core/db/implementations/test_model_base.py`](../../tests/neural_ai/core/db/implementations/test_model_base.py)
