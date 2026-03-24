# tests/neural_ai/core/db/conftest.py

Pytest fixtures a neural_ai.core.db tesztek számára.

Ez a modul tartalmazza a közös fixture-öket és setup/teardown logikát
az adatbázis tesztek számára.

## Importok

```python
import pytest
import neural_ai.core.db.implementations.sqlalchemy_session
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
```

### `reset_db_globals()`

```python
async def reset_db_globals()
```

Reset database global state minden teszt előtt és után. Ez a fixture biztosítja, hogy a globális _engine és _async_session_maker változók tiszták legyenek minden teszt előtt és után, elkerülve a test isolation problémákat.

### `reset_db_singleton()`

```python
def reset_db_singleton()
```

Reset DatabaseManager singleton minden teszt előtt és után. Ez a fixture biztosítja, hogy a DatabaseManager Singleton példány tiszta legyen minden teszt előtt és után.

---

**Forrásfájl:** [`tests/neural_ai/core/db/conftest.py`](../../tests/neural_ai/core/db/conftest.py)
