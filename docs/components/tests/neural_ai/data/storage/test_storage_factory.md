# tests/neural_ai/data/storage/test_storage_factory.py

StorageFactory teszt modul.

Ez a modul tartalmazza a StorageFactory osztály tesztjeit.

## Importok

```python
from pathlib import Path
from unittest.mock import MagicMock
import pytest
from neural_ai.data.storage.exceptions import StorageError
from neural_ai.data.storage.factory import StorageFactory
from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.base.implementations.singleton import SingletonMeta
```

## Konstansok

- **`mock_storage_class`**
: `MockStorage`


- **`mock_config`**
: `MagicMock()`


- **`storage`**
: `StorageFactory.get_storage(storage_type='file', base_path=str(tmp_path), config=mock_config)`


- **`mock_config`**
: `MagicMock()`


- **`storage`**
: `StorageFactory.get_storage(storage_type='parquet', base_path=str(tmp_path), hardware=mock_hardware, config=mock_config)`


- **`mock_config`**
: `MagicMock()`


- **`storage`**
: `StorageFactory.get_storage(storage_type='file', base_path=str(tmp_path), create_if_missing=True, config=mock_config)`


- **`mock_config`**
: `MagicMock()`


- **`mock_config`**
: `MagicMock()`


- **`mock_config`**
: `MagicMock()`


- **`mock_config`**
: `MagicMock()`


- **`storage`**
: `StorageFactory.get_storage(storage_type='file', config=mock_config)`


- **`mock_config`**
: `MagicMock()`


- **`storage`**
: `StorageFactory.get_storage(storage_type='file', base_path=str(tmp_path), hardware=None, config=mock_config)`


- **`initial_types`**
: `{'file', 'parquet'}`


## Osztály: `MockStorage(StorageInterface)`

### Metódusok

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`obj`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `save_dataframe()`

```python
def save_dataframe(self, df: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`df`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `delete()`

```python
def delete(self, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `exists()`

```python
def exists(self, path: str) -> bool
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

#### `list_dir()`

```python
def list_dir(self, path: str) -> list[str]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `list[str]`

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, object]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, object]`

## Osztály: `InvalidClass`

## Osztály: `FailingStorage(StorageInterface)`

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`obj`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `save_dataframe()`

```python
def save_dataframe(self, df: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`df`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `delete()`

```python
def delete(self, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `exists()`

```python
def exists(self, path: str) -> bool
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

#### `list_dir()`

```python
def list_dir(self, path: str) -> list[str]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `list[str]`

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, object]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, object]`

## Osztály: `UnexpectedErrorStorage(StorageInterface)`

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `save_object()`

```python
def save_object(self, obj: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`obj`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_object()`

```python
def load_object(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `save_dataframe()`

```python
def save_dataframe(self, df: object, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`df`** (`object`)
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_dataframe()`

```python
def load_dataframe(self, path: str) -> object
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `object`

#### `delete()`

```python
def delete(self, path: str) -> None
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `exists()`

```python
def exists(self, path: str) -> bool
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

#### `list_dir()`

```python
def list_dir(self, path: str) -> list[str]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `list[str]`

#### `get_metadata()`

```python
def get_metadata(self, path: str) -> dict[str, object]
```

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, object]`

## Osztály: `TestStorageFactory`

StorageFactory osztály tesztjei.

### Metódusok

#### `setup_method()`

```python
def setup_method(self) -> None
```

Teszt metódus előtti beállítás - Singleton cache törlése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_storage()`

```python
def test_register_storage(self) -> None
```

Teszteli a storage típus regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_register_storage_invalid_class()`

```python
def test_register_storage_invalid_class(self) -> None
```

Teszteli a nem StorageInterface-t implementáló osztály regisztrálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_file_type()`

```python
def test_get_storage_file_type(self, tmp_path: Path) -> None
```

Teszteli a file storage létrehozását.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_parquet_type()`

```python
def test_get_storage_parquet_type(self, tmp_path: Path) -> None
```

Teszteli a parquet storage létrehozását.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_with_kwargs()`

```python
def test_get_storage_with_kwargs(self, tmp_path: Path) -> None
```

Teszteli a storage létrehozást további paraméterekkel.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_invalid_config()`

```python
def test_get_storage_invalid_config(self, tmp_path: Path) -> None
```

Teszteli az érvénytelen konfigurációt (pl. tiltott storage típus).

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_invalid_type()`

```python
def test_get_storage_invalid_type(self) -> None
```

Teszteli a nem létező storage típus lekérését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_instantiation_failure()`

```python
def test_get_storage_instantiation_failure(self, tmp_path: Path) -> None
```

Teszteli a storage példányosítási hibát.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_unexpected_error()`

```python
def test_get_storage_unexpected_error(self, tmp_path: Path) -> None
```

Teszteli a váratlan hibát a storage létrehozásakor.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_default_base_path()`

```python
def test_get_storage_default_base_path(self) -> None
```

Teszteli a storage létrehozást alapértelmezett útvonallal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `test_get_storage_with_hardware_none()`

```python
def test_get_storage_with_hardware_none(self, tmp_path: Path) -> None
```

Teszteli a storage létrehozást hardware=None paraméterrel.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `test_initial_storage_types()`

```python
def test_initial_storage_types(self) -> None
```

Teszteli a kezdeti storage típusokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/storage/test_storage_factory.py`](../../tests/neural_ai/data/storage/test_storage_factory.py)
