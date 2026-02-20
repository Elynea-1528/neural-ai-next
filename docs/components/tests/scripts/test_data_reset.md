# tests/scripts/test_data_reset.py

Data reset szkript teszt modul.

Ez a modul tartalmazza a data_reset.py szkript tesztjeit.

## Importok

```python
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from scripts.data_reset import check_directory_exists
from scripts.data_reset import create_directories_if_needed
from scripts.data_reset import main
# ... és még 2 import
```

## Osztály: `TestDataReset`

Data reset szkript tesztjei.

### Metódusok

#### `temp_base_dir()`

```python
def temp_base_dir(self)
```

Ideiglenes alap könyvtár létrehozása a tesztekhez.

**Paraméterek:**

- **`self`**

#### `test_check_directory_exists_true()`

```python
def test_check_directory_exists_true(self, temp_base_dir: Path) -> None
```

Teszteli a könyvtár létezésének ellenőrzését létező könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`temp_base_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_directory_exists_false_no_dir()`

```python
def test_check_directory_exists_false_no_dir(self, temp_base_dir: Path) -> None
```

Teszteli a könyvtár létezésének ellenőrzését nem létező könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`temp_base_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_directory_exists_false_file()`

```python
def test_check_directory_exists_false_file(self, temp_base_dir: Path) -> None
```

Teszteli a könyvtár létezésének ellenőrzését fájl esetén.

**Paraméterek:**

- **`self`**
- **`temp_base_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_tick_data_exists()`

```python
def test_remove_tick_data_exists(self, mock_check_dir: MagicMock, mock_rmtree: MagicMock) -> None
```

Teszteli a tick adatok törlését létező könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)
- **`mock_rmtree`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_tick_data_not_exists()`

```python
def test_remove_tick_data_not_exists(self, mock_check_dir: MagicMock) -> None
```

Teszteli a tick adatok törlését nem létező könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_tick_data_exception()`

```python
def test_remove_tick_data_exception(self, mock_check_dir: MagicMock, mock_rmtree: MagicMock) -> None
```

Teszteli a tick adatok törlését kivétel esetén.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)
- **`mock_rmtree`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_logs_exists_with_files()`

```python
def test_remove_logs_exists_with_files(self, mock_check_dir: MagicMock, mock_rmtree: MagicMock, mock_remove: MagicMock, mock_islink: MagicMock, mock_isfile: MagicMock, mock_isdir: MagicMock, mock_listdir: MagicMock) -> None
```

Teszteli a logok törlését létező könyvtár esetén fájlokkal.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)
- **`mock_rmtree`** (`MagicMock`)
- **`mock_remove`** (`MagicMock`)
- **`mock_islink`** (`MagicMock`)
- **`mock_isfile`** (`MagicMock`)
- **`mock_isdir`** (`MagicMock`)
- **`mock_listdir`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_logs_not_exists()`

```python
def test_remove_logs_not_exists(self, mock_check_dir: MagicMock) -> None
```

Teszteli a logok törlését nem létező könyvtár esetén.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_logs_exception()`

```python
def test_remove_logs_exception(self, mock_check_dir: MagicMock, mock_listdir: MagicMock) -> None
```

Teszteli a logok törlését kivétel esetén.

**Paraméterek:**

- **`self`**
- **`mock_check_dir`** (`MagicMock`)
- **`mock_listdir`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_directories_if_needed()`

```python
def test_create_directories_if_needed(self, mock_mkdir: MagicMock) -> None
```

Teszteli a szükséges könyvtárak létrehozását.

**Paraméterek:**

- **`self`**
- **`mock_mkdir`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_success()`

```python
def test_main_success(self, mock_print: MagicMock, mock_create_dirs: MagicMock, mock_remove_tick: MagicMock, mock_remove_logs: MagicMock) -> None
```

Teszteli a main függvényt sikeres végrehajtás esetén.

**Paraméterek:**

- **`self`**
- **`mock_print`** (`MagicMock`)
- **`mock_create_dirs`** (`MagicMock`)
- **`mock_remove_tick`** (`MagicMock`)
- **`mock_remove_logs`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_failure_tick_data()`

```python
def test_main_failure_tick_data(self, mock_print: MagicMock, mock_create_dirs: MagicMock, mock_remove_tick: MagicMock, mock_remove_logs: MagicMock) -> None
```

Teszteli a main függvényt tick adatok törlésének sikertelensége esetén.

**Paraméterek:**

- **`self`**
- **`mock_print`** (`MagicMock`)
- **`mock_create_dirs`** (`MagicMock`)
- **`mock_remove_tick`** (`MagicMock`)
- **`mock_remove_logs`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_failure_logs()`

```python
def test_main_failure_logs(self, mock_print: MagicMock, mock_create_dirs: MagicMock, mock_remove_tick: MagicMock, mock_remove_logs: MagicMock) -> None
```

Teszteli a main függvényt logok törlésének sikertelensége esetén.

**Paraméterek:**

- **`self`**
- **`mock_print`** (`MagicMock`)
- **`mock_create_dirs`** (`MagicMock`)
- **`mock_remove_tick`** (`MagicMock`)
- **`mock_remove_logs`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_main_failure_both()`

```python
def test_main_failure_both(self, mock_print: MagicMock, mock_create_dirs: MagicMock, mock_remove_tick: MagicMock, mock_remove_logs: MagicMock) -> None
```

Teszteli a main függvényt mindkét törlés sikertelensége esetén.

**Paraméterek:**

- **`self`**
- **`mock_print`** (`MagicMock`)
- **`mock_create_dirs`** (`MagicMock`)
- **`mock_remove_tick`** (`MagicMock`)
- **`mock_remove_logs`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/scripts/test_data_reset.py`](../../tests/scripts/test_data_reset.py)
