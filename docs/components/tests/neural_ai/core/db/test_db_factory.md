# tests/neural_ai/core/db/test_db_factory.py

Tesztek a neural_ai.core.db.factory modulhoz.

Ez a modul tartalmazza a DatabaseFactory osztály és annak metódusainak tesztjeit.

## Importok

```python
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.config.interfaces.types import DatabaseConfig
# ... és még 18 import
```

## Osztály: `TestDatabaseFactory`

DatabaseFactory osztály tesztjei.

### Metódusok

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock logger fixture.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_config()`

```python
def mock_config(self) -> MagicMock
```

Mock config manager fixture.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `factory()`

```python
def factory(self, mock_logger: MagicMock, mock_config: MagicMock) -> DatabaseFactory
```

DatabaseFactory fixture.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `DatabaseFactory`

#### `test_get_session_maker_without_config()`

```python
def test_get_session_maker_without_config(self, mock_get_session_maker: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli a session maker lekérdezést konfig nélkül.

**Paraméterek:**

- **`self`**
- **`mock_get_session_maker`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_session_maker_with_config()`

```python
def test_get_session_maker_with_config(self, mock_get_session_maker: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli a session maker lekérdezést konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_get_session_maker`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_engine_without_config()`

```python
def test_get_engine_without_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli az engine lekérdezést konfig nélkül.

**Paraméterek:**

- **`self`**
- **`mock_get_engine`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_engine_with_config()`

```python
def test_get_engine_with_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli az engine lekérdezést konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_get_engine`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_engine_with_custom_url()`

```python
def test_create_engine_with_custom_url(self, factory: DatabaseFactory) -> None
```

Teszteli az egyéni engine létrehozást.

**Paraméterek:**

- **`self`**
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_engine_with_echo_enabled()`

```python
def test_create_engine_with_echo_enabled(self, factory: DatabaseFactory) -> None
```

Teszteli az engine létrehozást echo módban.

**Paraméterek:**

- **`self`**
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_without_config()`

```python
def test_create_manager_without_config(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli a DatabaseManager létrehozást konfig nélkül.

**Paraméterek:**

- **`self`**
- **`mock_get_manager`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_with_config()`

```python
def test_create_manager_with_config(self, factory: DatabaseFactory) -> None
```

Teszteli a DatabaseManager létrehozást konfiggal.

**Paraméterek:**

- **`self`**
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_session_maker_caches_result()`

```python
def test_get_session_maker_caches_result(self, mock_get_session: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli, hogy a session maker cache-elődik a modul szintjén.

**Paraméterek:**

- **`self`**
- **`mock_get_session`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_engine_caches_result()`

```python
def test_get_engine_caches_result(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli, hogy az engine cache-elődik a modul szintjén.

**Paraméterek:**

- **`self`**
- **`mock_get_engine`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_engine_different_urls()`

```python
def test_create_engine_different_urls(self, factory: DatabaseFactory) -> None
```

Teszteli az engine létrehozást különböző URL-ekkel.

**Paraméterek:**

- **`self`**
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_methods_return_consistent_types()`

```python
def test_factory_methods_return_consistent_types(self, mock_get_engine: MagicMock, mock_get_session_maker: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli, hogy a factory metódusok konzisztens típusokat adnak vissza.

**Paraméterek:**

- **`self`**
- **`mock_get_engine`** (`MagicMock`)
- **`mock_get_session_maker`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_is_stateless()`

```python
def test_factory_is_stateless(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None
```

Teszteli, hogy a factory osztály állapotmentes-e.

**Paraméterek:**

- **`self`**
- **`mock_get_manager`** (`MagicMock`)
- **`factory`** (`DatabaseFactory`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDatabaseConfigPydanticValidation`

Pydantic DatabaseConfig validációs tesztek.

Ezek a tesztek ellenőrzik a DatabaseConfig Pydantic model működését,
beleértve a URL formátum validációt és a pool size ellenőrzést.

### Metódusok

#### `test_database_config_valid_sqlite_url()`

```python
def test_database_config_valid_sqlite_url(self) -> None
```

Érvényes SQLite URL validálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_valid_postgresql_url()`

```python
def test_database_config_valid_postgresql_url(self) -> None
```

Érvényes PostgreSQL URL validálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_valid_mysql_url()`

```python
def test_database_config_valid_mysql_url(self) -> None
```

Érvényes MySQL URL validálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_invalid_url_raises_error()`

```python
def test_database_config_invalid_url_raises_error(self) -> None
```

Érvénytelen URL formátum hibát dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_missing_url_raises_error()`

```python
def test_database_config_missing_url_raises_error(self) -> None
```

Hiányzó URL esetén hibát dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_pool_size_validation_valid()`

```python
def test_database_config_pool_size_validation_valid(self) -> None
```

Pool size >= 1 esetén sikeres validáció.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_pool_size_validation_invalid()`

```python
def test_database_config_pool_size_validation_invalid(self) -> None
```

Pool size < 1 esetén hibát dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_pool_optional()`

```python
def test_database_config_pool_optional(self) -> None
```

Pool konfig opcionális - None is érvényes.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_with_real_yaml_config()`

```python
def test_factory_with_real_yaml_config(self, tmp_path: Path) -> None
```

Factory valós YAML konfigurációval.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/test_db_factory.py`](../../tests/neural_ai/core/db/test_db_factory.py)
