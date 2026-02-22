# tests/conftest.py

Pytest configuration and fixtures for test isolation.

Ez a fájl biztosítja a Singleton és DI Container állapot tisztítását
minden teszt között, megoldva a test isolation problémát.

## Importok

```python
import pytest
from typing import Generator
import sys
import gc
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.base.implementations.di_container import DIContainer
# ... és még 1 import
```

## Konstansok

- **`container`**
: `DIContainer()`


- **`env_vars_to_clear`**
: `['DATABASE_URL', 'NEURAL_AI_ENV', 'NEURAL_AI_CONFIG_PATH']`


### `reset_singletons()`

```python
def reset_singletons() -> Generator[None, None, None]
```

Automatikusan reseteli az összes Singleton példányt minden teszt előtt és után. Ez a fixture autouse=True-val fut minden tesztnél, biztosítva a tiszta állapotot.

**Visszatérési érték:**

- Típus: `Generator[None, None, None]`

### `_clear_all_singletons()`

```python
def _clear_all_singletons() -> None
```

Törli az összes Singleton példányt a memóriából.

**Visszatérési érték:**

- Típus: `None`

### `reset_di_container()`

```python
def reset_di_container() -> Generator[None, None, None]
```

Automatikusan reseteli a DI Container-t minden teszt előtt és után. Ez biztosítja, hogy a dependency injection állapot ne szivárogjon át tesztek között.

**Visszatérési érték:**

- Típus: `Generator[None, None, None]`

### `_clear_di_container()`

```python
def _clear_di_container() -> None
```

Törli a DI Container állapotát.

**Visszatérési érték:**

- Típus: `None`

### `clean_environment()`

```python
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None
```

Tiszta környezeti változók minden teszthez. Ez a fixture nem autouse, csak explicit használatra.

**Paraméterek:**

- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/conftest.py`](../../tests/conftest.py)
