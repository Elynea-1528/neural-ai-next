# neural_ai/core/db/implementations/__init__.py

Adatbázis implementációk a Neural AI Next rendszerhez.

Ez a modul tartalmazza az adatbázis műveletek konkrét implementációit.

## Importok

```python
from model_base import Base
from models import DynamicConfig
from models import LogEntry
from sqlalchemy_session import DatabaseManager
from sqlalchemy_session import close_db
from sqlalchemy_session import create_engine
from sqlalchemy_session import get_async_session_maker
from sqlalchemy_session import get_database_url
from sqlalchemy_session import get_db_session
from sqlalchemy_session import get_db_session_direct
# ... és még 2 import
```

## Konstansok

- **`__all__`**
: `['Base', 'DynamicConfig', 'LogEntry', 'get_db_session', 'get_db_session_direct', 'get_engine', 'get_async_session_maker', 'init_db', 'close_db', 'DatabaseManager', 'get_database_url', 'create_engine']`


---

**Forrásfájl:** [`neural_ai/core/db/implementations/__init__.py`](../../neural_ai/core/db/implementations/__init__.py)
