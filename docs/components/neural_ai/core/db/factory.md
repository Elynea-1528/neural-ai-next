# neural_ai/core/db/factory.py

Adatbázis factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kezelő komponensek létrehozását a factory
minta segítségével, beleértve a session maker-t és a DatabaseManager-t.

## Importok

```python
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.db.implementations.sqlalchemy_session import create_engine
from neural_ai.core.db.implementations.sqlalchemy_session import get_async_session_maker
from neural_ai.core.db.implementations.sqlalchemy_session import get_engine
from neural_ai.core.logger.interfaces import LoggerInterface
```

## Osztály: `DatabaseFactory`

Factory osztály adatbázis komponensek létrehozásához.

Ez az osztály felelős az adatbázis kezelő komponensek példányosításáért,
beleértve a session factory-ket és a DatabaseManager-t.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: 'LoggerInterface', config_manager: ConfigManagerInterface) -> None
```

Inicializálja az adatbázis factory-t.

**Paraméterek:**

- **`self`**
- **`logger`** (`'LoggerInterface'`): Logger interfész a naplózáshoz.
- **`config_manager`** (`ConfigManagerInterface`): Konfiguráció kezelő interfész.

**Visszatérési érték:**

- Típus: `None`

#### `get_session_maker()`

```python
def get_session_maker(self) -> async_sessionmaker[AsyncSession]
```

Session maker létrehozása vagy visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `async_sessionmaker[AsyncSession]`
- Az async_sessionmaker objektum.

#### `get_engine()`

```python
def get_engine(self) -> AsyncEngine
```

Adatbázis engine létrehozása vagy visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `AsyncEngine`
- Az SQLAlchemy async engine.

#### `create_engine()`

```python
def create_engine(self, db_url: str, echo: bool = False) -> AsyncEngine
```

Egyéni adatbázis engine létrehozása.

**Paraméterek:**

- **`self`**
- **`db_url`** (`str`): Az adatbázis URL.
- **`echo`** (`bool`) = `False`: SQL lekérdezések naplózásának engedélyezése.

**Visszatérési érték:**

- Típus: `AsyncEngine`
- Az létrehozott SQLAlchemy async engine.

#### `create_manager()`

```python
def create_manager(self) -> DatabaseManager
```

DatabaseManager példány létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `DatabaseManager`
- Az inicializált DatabaseManager példány.

---

**Forrásfájl:** [`neural_ai/core/db/factory.py`](../../neural_ai/core/db/factory.py)
