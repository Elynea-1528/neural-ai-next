# neural_ai/core/db/__init__.py

Adatbázis modul a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kapcsolat kezelést, modelleket és session
factory-t az aszinkron adatbázis műveletekhez.

## Importok

```python
from factory import DatabaseFactory
from implementations.model_base import Base
from implementations.models import DynamicConfig
from implementations.models import LogEntry
from implementations.sqlalchemy_session import DatabaseManager
from implementations.sqlalchemy_session import close_db
from implementations.sqlalchemy_session import create_engine
from implementations.sqlalchemy_session import get_async_session_maker
from implementations.sqlalchemy_session import get_database_url
from implementations.sqlalchemy_session import get_db_session
# ... és még 3 import
```

## Konstansok

- **`__all__`**
: `['Base', 'DynamicConfig', 'LogEntry', 'get_db_session', 'get_db_session_direct', 'get_engine', 'get_async_session_maker', 'init_db', 'close_db', 'DatabaseManager', 'DatabaseFactory', 'get_database_url', 'create_engine']`


---

**Forrásfájl:** [`neural_ai/core/db/__init__.py`](../../neural_ai/core/db/__init__.py)
