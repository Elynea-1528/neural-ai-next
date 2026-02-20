# tests/scripts/test_migrate_structure.py

Migrate structure szkript teszt modul.

Ez a modul tartalmazza a migrate_structure.py szkript tesztjeit.

## Importok

```python
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from scripts.migrate_structure import main
from scripts.migrate_structure import migrate_tick_structure
```

## Osztály: `TestMigrateStructure`

Migrate structure szkript tesztjei.

### Metódusok

#### `temp_base_dir()`

```python
def temp_base_dir(self)
```

Ideiglenes alap könyvtár létrehozása a tesztekhez.

**Paraméterek:**

- **`self`**

#### `test_migrate_tick_structure_no_base_dir()`

```python
def test_migrate_tick_structure_no_base_dir(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt nem létező alapkönyvtár esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_no_symbol_dirs()`

```python
def test_migrate_tick_structure_no_symbol_dirs(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt szimbólum könyvtárak nélkül.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_no_tick_dir()`

```python
def test_migrate_tick_structure_no_tick_dir(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt tick könyvtár nélküli szimbólum esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_empty_tick_dir()`

```python
def test_migrate_tick_structure_empty_tick_dir(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt üres tick könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_with_content()`

```python
def test_migrate_tick_structure_with_content(self, mock_move: MagicMock, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt tick könyvtár tartalommal.

**Paraméterek:**

- **`self`**
- **`mock_move`** (`MagicMock`)
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_tick_not_dir()`

```python
def test_migrate_tick_structure_tick_not_dir(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt amikor a tick 'útvonal' nem mappa.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_rmdir_exception_empty()`

```python
def test_migrate_tick_structure_rmdir_exception_empty(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt OSError esetén üres tick mappa törlésekor.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_target_exists()`

```python
def test_migrate_tick_structure_target_exists(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt amikor a célmappa már létezik.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_move_exception()`

```python
def test_migrate_tick_structure_move_exception(self, mock_move: MagicMock, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt OSError esetén az áthelyezéskor.

**Paraméterek:**

- **`self`**
- **`mock_move`** (`MagicMock`)
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_migrate_tick_structure_rmdir_exception_after_move()`

```python
def test_migrate_tick_structure_rmdir_exception_after_move(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a migrációt OSError esetén tick mappa törlésekor tartalom áthelyezése után.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_success()`

```python
def test_main_success(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a main függvényt sikeres végrehajtás esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_logger_none()`

```python
def test_main_logger_none(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a main függvényt None logger esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_exception()`

```python
def test_main_exception(self, mock_create_minimal: MagicMock) -> None
```

Teszteli a main függvényt kivétel esetén.

**Paraméterek:**

- **`self`**
- **`mock_create_minimal`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/scripts/test_migrate_structure.py`](../../tests/scripts/test_migrate_structure.py)
