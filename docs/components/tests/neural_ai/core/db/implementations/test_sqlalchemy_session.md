# tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py

Tesztek a neural_ai.core.db.implementations.sqlalchemy_session modulhoz.

Ez a modul tartalmazza az adatbázis session kezelő függvények és osztályok tesztjeit.

## Importok

```python
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.exceptions import DBConnectionError
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
# ... és még 15 import
```

## Osztály: `TestDatabaseURL`

Adatbázis URL lekérdezés tesztjei.

### Metódusok

#### `test_get_database_url_with_provided_config()`

```python
def test_get_database_url_with_provided_config(self) -> None
```

Teszteli az adatbázis URL lekérdezést megadott konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_database_url_fallback_to_env()`

```python
def test_get_database_url_fallback_to_env(self) -> None
```

Teszteli az adatbázis URL lekérdezést env fallbackkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_database_url_without_config()`

```python
def test_get_database_url_without_config(self) -> None
```

Teszteli az adatbázis URL lekérdezést konfig nélkül (line 47).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_database_url_raises_error_when_missing()`

```python
def test_get_database_url_raises_error_when_missing(self) -> None
```

Teszteli, hogy a függvény hibát dob, ha az URL hiányzik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestCreateEngine`

Engine létrehozás tesztjei.

### Metódusok

#### `test_create_engine_sqlite()`

```python
def test_create_engine_sqlite(self) -> None
```

Teszteli az engine létrehozást SQLite URL-lel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_engine_with_echo()`

```python
def test_create_engine_with_echo(self) -> None
```

Teszteli az engine létrehozást echo módban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_create_engine_postgresql()`

```python
def test_create_engine_postgresql(self) -> None
```

Teszteli az engine létrehozást PostgreSQL URL-lel (line 88).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestGetEngine`

Globális engine lekérdezés tesztjei.

### Metódusok

#### `test_get_engine_creates_on_first_call()`

```python
def test_get_engine_creates_on_first_call(self, mock_create: MagicMock, mock_config_factory: MagicMock, mock_get_url: MagicMock) -> None
```

Teszteli, hogy az engine létrejön az első hívásnál.

**Paraméterek:**

- **`self`**
- **`mock_create`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_get_url`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_engine_caches_result()`

```python
def test_get_engine_caches_result(self, mock_create: MagicMock, mock_config_factory: MagicMock, mock_get_url: MagicMock) -> None
```

Teszteli, hogy az engine cache-elődik.

**Paraméterek:**

- **`self`**
- **`mock_create`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_get_url`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestGetAsyncSessionMaker`

Session maker lekérdezés tesztjei.

### Metódusok

#### `test_get_async_session_maker_creates_once()`

```python
def test_get_async_session_maker_creates_once(self, mock_get_engine: MagicMock) -> None
```

Teszteli, hogy a session maker csak egyszer jön létre.

**Paraméterek:**

- **`self`**
- **`mock_get_engine`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDatabaseManager`

DatabaseManager osztály tesztjei.

### Metódusok

#### `test_database_manager_initialization()`

```python
async def test_database_manager_initialization(self) -> None
```

Teszteli a DatabaseManager inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_initialize()`

```python
async def test_database_manager_initialize(self) -> None
```

Teszteli a DatabaseManager initialize metódusát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_get_session()`

```python
async def test_database_manager_get_session(self) -> None
```

Teszteli a DatabaseManager get_session metódusát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_get_session_raises_when_not_initialized()`

```python
async def test_database_manager_get_session_raises_when_not_initialized(self) -> None
```

Teszteli, hogy get_session hibát dob, ha nincs inicializálva.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_close()`

```python
async def test_database_manager_close(self) -> None
```

Teszteli a DatabaseManager close metódusát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_singleton_pattern()`

```python
async def test_database_manager_singleton_pattern(self) -> None
```

Teszteli, hogy a DatabaseManager Singleton mintát követ.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_get_session_exception_rollback()`

```python
async def test_database_manager_get_session_exception_rollback(self) -> None
```

Teszteli a DatabaseManager get_session exception rollback-ját (lines 295-297).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_get_active_configs()`

```python
async def test_database_manager_get_active_configs(self) -> None
```

Teszteli a DatabaseManager get_active_configs metódusát (lines 312-325).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_manager_get_active_configs_not_initialized()`

```python
async def test_database_manager_get_active_configs_not_initialized(self) -> None
```

Teszteli, hogy get_active_configs hibát dob, ha nincs inicializálva (line 315).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestContextManagers`

Context manager függvények tesztjei.

### Metódusok

#### `test_get_db_session()`

```python
async def test_get_db_session(self) -> None
```

Teszteli a get_db_session context managert.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_db_session_direct()`

```python
async def test_get_db_session_direct(self) -> None
```

Teszteli a get_db_session_direct függvényt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_db_session_exception_rollback()`

```python
async def test_get_db_session_exception_rollback(self) -> None
```

Teszteli a get_db_session exception rollback-ját (lines 169-171).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDatabaseInitialization`

Adatbázis inicializálás tesztjei.

### Metódusok

#### `test_init_db()`

```python
async def test_init_db(self) -> None
```

Teszteli az init_db függvényt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_close_db()`

```python
async def test_close_db(self) -> None
```

Teszteli a close_db függvényt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestGetActiveConfigs`

Aktív konfigurációk lekérdezésének tesztjei.

### Metódusok

#### `test_get_active_configs()`

```python
async def test_get_active_configs(self) -> None
```

Teszteli a get_active_configs függvényt a DatabaseManager-en keresztül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](../../tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py)
