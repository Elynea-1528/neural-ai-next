# neural_ai/core/db/implementations/sqlalchemy_session.py

Adatbázis session kezelő a Neural AI Next rendszerhez.

Ez a modul biztosítja az AsyncSession factory-t és a kapcsolódó segédfunkciókat
az adatbázis műveletek aszinkron kezeléséhez.

## Importok

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
from typing import cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
# ... és még 10 import
```

## Konstansok

- **`config_manager`**
: `ConfigManagerFactory.get_manager('config.yaml')`


- **`db_config_raw`**
: `config_manager.get('database')`


- **`db_config`**
: `DatabaseConfig(**db_config_raw)`


- **`db_url`**
: `db_config.connection.url`


- **`db_url`**
: `None`


- **`db_url`**
: `cast(str | None, config_manager.get('db_url'))`


- **`engine`**
: `create_async_engine(db_url, echo=echo, poolclass=NullPool, connect_args={'check_same_thread': False})`


- **`pool_size`**
: `pool_config.size if pool_config and pool_config.size else 20`


- **`pool_recycle`**
: `pool_config.recycle if pool_config and pool_config.recycle else 3600`


- **`engine`**
: `create_async_engine(db_url, echo=echo, pool_size=pool_size, pool_recycle=pool_recycle, max_overflow=0)`


- **`db_url`**
: `get_database_url(config_manager)`


- **`echo`**
: `False`


- **`echo`**
: `config_manager.get('log_level', 'INFO') == 'DEBUG'`


- **`fallback_config`**
: `ConfigManagerFactory.get_manager('config.yaml')`


- **`echo`**
: `fallback_config.get('log_level', 'INFO') == 'DEBUG'`


- **`pool_config`**
: `None`


- **`db_config_raw`**
: `config_manager.get('database')`


- **`pool_raw`**
: `db_config_raw.get('pool')`


- **`pool_config`**
: `DatabasePoolConfig(**pool_raw)`


- **`_engine`**
: `create_engine(db_url, echo=echo, pool_config=pool_config)`


- **`engine`**
: `get_engine(config_manager)`


- **`_async_session_maker`**
: `async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)`


- **`session_maker`**
: `get_async_session_maker()`


- **`session_maker`**
: `get_async_session_maker()`


- **`engine`**
: `get_engine()`


- **`_engine`**
: `None`


- **`_async_session_maker`**
: `None`


## Osztály: `DatabaseManager`

Adatbázis kezelő osztály a Neural AI Next rendszerhez.

Ez az osztály magas szintű interfészt biztosít az adatbázis műveletekhez,
beleértve a session kezelést, inicializálást és lezárást.

Attributes:
    config_manager: A konfiguráció kezelő példány.
    logger: A logger interfész.

### Metódusok

#### `__init__()`

```python
def __init__(self, config_manager: ConfigManagerInterface, logger: 'LoggerInterface')
```

Inicializálja az adatbázis kezelőt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`ConfigManagerInterface`): Konfiguráció kezelő (KÖTELEZŐ - Dependency Injection).
- **`logger`** (`'LoggerInterface'`): Logger interfész (KÖTELEZŐ - Dependency Injection).

#### `initialize()`

```python
async def initialize(self) -> None
```

Adatbázis inicializálása a kezelővel. Létrehozza az engine-t és a session maker-t, majd létrehozza a táblákat. A pool konfigurációt a configs/database.yaml fájlból olvassa be.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_session()`

```python
async def get_session(self) -> AsyncGenerator[AsyncSession, None]
```

Session lekérdezése a kezelőből. Yields: AsyncSession: Az adatbázis session.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `AsyncGenerator[AsyncSession, None]`

**Kivételek:**

- **`RuntimeError`**: Ha a kezelő nincs inicializálva.

#### `get_active_configs()`

```python
async def get_active_configs(self) -> dict[str, object]
```

Aktív dinamikus konfigurációk lekérdezése. Visszaadja az összes aktív dinamikus konfigurációt kulcs-érték párokként.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, object]`
- Szótár az aktív konfigurációkulcsokkal és értékeikkel.

**Kivételek:**

- **`RuntimeError`**: Ha a kezelő nincs inicializálva.

#### `close()`

```python
async def close(self) -> None
```

Adatbázis kapcsolat lezárása. Felszabadítja az engine erőforrásait.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `get_database_url()`

```python
def get_database_url(config_manager: ConfigManagerInterface | None = None) -> str
```

Adatbázis URL lekérdezése a konfigurációból.

**Paraméterek:**

- **`config_manager`** (`ConfigManagerInterface | None`) = `None`: Opcionális konfiguráció kezelő. Ha nincs megadva, létrehoz egy újat a ConfigManagerFactory segítségével.

**Visszatérési érték:**

- Típus: `str`
- Az adatbázis URL string formátumban.

**Kivételek:**

- **`ValueError`**: Ha az adatbázis URL nincs konfigurálva.

### `create_engine()`

```python
def create_engine(db_url: str, echo: bool = False, pool_config: DatabasePoolConfig | None = None) -> AsyncEngine
```

Aszinkron adatbázis engine létrehozása. Dinamikus pool konfigurációval rendelkezik - a pool paraméterek a config fájlból vagy a pool_config paraméterből jönnek.

**Paraméterek:**

- **`db_url`** (`str`): Az adatbázis URL (pl. sqlite+aiosqlite:///neural_ai.db).
- **`echo`** (`bool`) = `False`: SQL lekérdezések naplózásának engedélyezése.
- **`pool_config`** (`DatabasePoolConfig | None`) = `None`: Opcionális DatabasePoolConfig objektum a connection pool beállításokhoz. Ha nincs megadva, alapértelmezett értékeket használ (size=20, recycle=3600).

**Visszatérési érték:**

- Típus: `AsyncEngine`
- Az létrehozott SQLAlchemy async engine.

**Példák:**

```python
    >>> # Alapértelmezett pool
    >>> engine = create_engine("postgresql+asyncpg://localhost/db")
    >>>
    >>> # Custom pool konfig
    >>> pool_cfg = DatabasePoolConfig(size=10, recycle=1800)
    >>> engine = create_engine("postgresql+asyncpg://localhost/db", pool_config=pool_cfg)
```

### `get_engine()`

```python
def get_engine(config_manager: ConfigManagerInterface | None = None) -> AsyncEngine
```

Globális adatbázis engine lekérdezése. Ha az engine még nincs létrehozva, létrehozza azt a konfiguráció alapján. A pool konfigurációt a configs/database.yaml fájlból olvassa be.

**Paraméterek:**

- **`config_manager`** (`ConfigManagerInterface | None`) = `None`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**

- Típus: `AsyncEngine`
- A globális SQLAlchemy async engine.

### `get_async_session_maker()`

```python
def get_async_session_maker(config_manager: ConfigManagerInterface | None = None) -> async_sessionmaker[AsyncSession]
```

AsyncSession factory lekérdezése. Ha a session maker még nincs létrehozva, létrehozza azt.

**Paraméterek:**

- **`config_manager`** (`ConfigManagerInterface | None`) = `None`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**

- Típus: `async_sessionmaker[AsyncSession]`
- Az async_sessionmaker objektum.

### `get_db_session()`

```python
async def get_db_session() -> AsyncGenerator[AsyncSession, None]
```

Dependency injection függvény a FastAPI számára. Ez a függvény biztosítja az adatbázis session-t a request élettartamára. Automatikusan kezeli a session lezárását és a tranzakciók commit/rollback-jét. Yields: AsyncSession: Az adatbázis session.

**Visszatérési érték:**

- Típus: `AsyncGenerator[AsyncSession, None]`

**Példák:**

```python
    ```python
    async def some_operation():
        async with get_db_session() as session:
            result = await session.execute(select(MyModel))
            return result.scalars().all()
    ```
```

### `get_db_session_direct()`

```python
async def get_db_session_direct() -> AsyncSession
```

Közvetlen adatbázis session lekérdezése. Ez a függvény manuális session kezelést tesz lehetővé. A hívó felelőssége a session lezárása.

**Visszatérési érték:**

- Típus: `AsyncSession`
- AsyncSession: Az adatbázis session.

**Példák:**

```python
    ```python
    async def some_operation():
        session = await get_db_session_direct()
        try:
            result = await session.execute(select(MyModel))
            await session.commit()
            return result.scalars().all()
        finally:
            await session.close()
    ```
```

### `init_db()`

```python
async def init_db(logger: 'LoggerInterface') -> None
```

Adatbázis inicializálása. Létrehozza az összes táblát az adatbázisban a modellek alapján. Ez a függvény az alkalmazás indításakor hívandó.

**Paraméterek:**

- **`logger`** (`'LoggerInterface'`): Logger interfész a naplózáshoz.

**Visszatérési érték:**

- Típus: `None`

### `close_db()`

```python
async def close_db(logger: 'LoggerInterface') -> None
```

Adatbázis kapcsolat lezárása. Ez a függvény az alkalmazás leállításakor hívandó.

**Paraméterek:**

- **`logger`** (`'LoggerInterface'`): Logger interfész a naplózáshoz.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/db/implementations/sqlalchemy_session.py`](../../neural_ai/core/db/implementations/sqlalchemy_session.py)
