# tests/neural_ai/data/storage/implementations/test_file_storage.py

FileStorage teszt modul.

Ez a modul tartalmazza a FileStorage osztály tesztjeit.

## Importok

```python
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
import pandas
import pytest
from neural_ai.data.storage.exceptions import StorageFormatError
from neural_ai.data.storage.exceptions import StorageIOError
# ... és még 8 import
```

## Konstansok

- **`obj`**
: `NonSerializable()`


- **`test_file`**
: `storage._get_full_path('test_no_extension')`


- **`test_file`**
: `storage._get_full_path('invalid.pkl')`


- **`test_file`**
: `temp_dir / 'meta_error.txt'`


- **`test_dir`**
: `storage._get_full_path('delete_dir')`


- **`test_file`**
: `temp_dir / 'delete_error.txt'`


- **`test_file`**
: `storage._get_full_path('not_a_dir.txt')`


- **`test_dir`**
: `storage._get_full_path('glob_error_dir')`


## Osztály: `NonSerializable`

## Osztály: `TestFileStorage`

FileStorage osztály tesztjei.

### Metódusok

#### `temp_dir()`

```python
def temp_dir(self) -> Path
```

Ideiglenes könyvtár létrehozása a tesztekhez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock logger fixture.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `storage()`

```python
def storage(self, temp_dir: Path, mock_logger: MagicMock) -> FileStorage
```

FileStorage példány létrehozása logger-rel.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `FileStorage`

#### `sample_dataframe()`

```python
def sample_dataframe(self) -> pd.DataFrame
```

Minta DataFrame létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `pd.DataFrame`

#### `sample_object()`

```python
def sample_object(self) -> dict[str, object]
```

Minta Python objektum létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, object]`

#### `test_init_default_path()`

```python
def test_init_default_path(self, mock_logger: MagicMock) -> None
```

Teszteli az alapértelmezett útvonal beállítását.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_init_custom_path()`

```python
def test_init_custom_path(self, temp_dir: Path, mock_logger: MagicMock) -> None
```

Teszteli az egyéni útvonal beállítását.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_logger()`

```python
def test_init_with_logger(self, temp_dir: Path) -> None
```

Teszteli a logger beállítását.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_full_path_absolute()`

```python
def test_get_full_path_absolute(self, storage: FileStorage) -> None
```

Teszteli az abszolút útvonal kezelését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_full_path_relative()`

```python
def test_get_full_path_relative(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a relatív útvonal kezelését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_exists_true()`

```python
def test_exists_true(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a létező fájl ellenőrzését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_exists_false()`

```python
def test_exists_false(self, storage: FileStorage) -> None
```

Teszteli a nem létező fájl ellenőrzését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_parquet()`

```python
def test_save_dataframe_parquet(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame mentését Parquet formátumban.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_invalid_format()`

```python
def test_save_dataframe_invalid_format(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame mentését érvénytelen formátumban.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_not_found()`

```python
def test_load_dataframe_not_found(self, storage: FileStorage) -> None
```

Teszteli a DataFrame betöltését nem létező fájlból.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_pickle()`

```python
def test_save_object_pickle(self, storage: FileStorage, sample_object: dict[str, object]) -> None
```

Teszteli a Python objektum mentését pickle formátumban.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_object`** (`dict[str, object]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_invalid_format()`

```python
def test_save_object_invalid_format(self, storage: FileStorage, sample_object: dict[str, object]) -> None
```

Teszteli a Python objektum mentését érvénytelen formátumban.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_object`** (`dict[str, object]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_object_not_found()`

```python
def test_load_object_not_found(self, storage: FileStorage) -> None
```

Teszteli a Python objektum betöltését nem létező fájlból.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_metadata_file()`

```python
def test_get_metadata_file(self, storage: FileStorage) -> None
```

Teszteli a fájl metaadatok lekérdezését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_metadata_not_found()`

```python
def test_get_metadata_not_found(self, storage: FileStorage) -> None
```

Teszteli a metaadatok lekérdezését nem létező fájlból.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_file()`

```python
def test_delete_file(self, storage: FileStorage) -> None
```

Teszteli a fájl törlését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_not_found()`

```python
def test_delete_not_found(self, storage: FileStorage) -> None
```

Teszteli a nem létező fájl törlését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_list_dir()`

```python
def test_list_dir(self, storage: FileStorage) -> None
```

Teszteli a könyvtár listázását.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_list_dir_with_pattern()`

```python
def test_list_dir_with_pattern(self, storage: FileStorage) -> None
```

Teszteli a könyvtár listázását mintával.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_list_dir_not_found()`

```python
def test_list_dir_not_found(self, storage: FileStorage) -> None
```

Teszteli a könyvtár listázását nem létező könyvtárból.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_permissions_read_only()`

```python
def test_check_permissions_read_only(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli az olvasási jogosultság ellenőrzését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_storage_info()`

```python
def test_get_storage_info(self, storage: FileStorage) -> None
```

Teszteli a tároló információk lekérdezését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_with_kwargs()`

```python
def test_save_dataframe_with_kwargs(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame mentését **kwargs paraméterekkel.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_with_kwargs()`

```python
def test_load_dataframe_with_kwargs(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame betöltését **kwargs paraméterekkel.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_with_kwargs()`

```python
def test_save_object_with_kwargs(self, storage: FileStorage, sample_object: dict[str, object]) -> None
```

Teszteli a Python objektum mentését **kwargs paraméterekkel.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_object`** (`dict[str, object]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_object_with_kwargs()`

```python
def test_load_object_with_kwargs(self, storage: FileStorage, sample_object: dict[str, object]) -> None
```

Teszteli a Python objektum betöltését **kwargs paraméterekkel.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_object`** (`dict[str, object]`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_disk_space_sufficient()`

```python
def test_check_disk_space_sufficient(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a lemezterület ellenőrzését elegendő terület esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_disk_space_insufficient()`

```python
def test_check_disk_space_insufficient(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a lemezterület ellenőrzését elégtelen terület esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_disk_space_os_error()`

```python
def test_check_disk_space_os_error(self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a lemezterület ellenőrzését OS hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_statvfs()`

```python
def mock_statvfs(path: Path) -> None
```

**Paraméterek:**

- **`path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_permissions_write_denied()`

```python
def test_check_permissions_write_denied(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a jogosultság ellenőrzését írási jog nélkül.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_permissions_read_denied()`

```python
def test_check_permissions_read_denied(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a jogosultság ellenőrzését olvasási jog nélkül.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_permissions_parent_not_exists()`

```python
def test_check_permissions_parent_not_exists(self, storage: FileStorage, temp_dir: Path) -> None
```

Teszteli a jogosultság ellenőrzését nem létező szülőkönyvtár esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_storage_info_os_error()`

```python
def test_get_storage_info_os_error(self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a tároló információk lekérdezését OS hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_statvfs()`

```python
def mock_statvfs(path: Path) -> None
```

**Paraméterek:**

- **`path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_atomic_write_bytes()`

```python
def test_atomic_write_bytes(self, storage: FileStorage) -> None
```

Teszteli az atomi írást bytes tartalommal (bináris mód).

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_format_detection_failure()`

```python
def test_save_dataframe_format_detection_failure(self, storage: FileStorage) -> None
```

Teszteli a DataFrame mentését formátum meghatározási hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_excel_format_detection()`

```python
def test_save_dataframe_excel_format_detection(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame mentését Excel formátum automatikus felismerésével.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_dataframe_disk_space_check_failure()`

```python
def test_save_dataframe_disk_space_check_failure(self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a DataFrame mentését lemezterület ellenőrzési hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_memory_usage()`

```python
def mock_memory_usage() -> Any
```

**Visszatérési érték:**

- Típus: `Any`

#### `test_save_dataframe_io_error()`

```python
def test_save_dataframe_io_error(self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a DataFrame mentését IO hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_mkdir()`

```python
def mock_mkdir() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_format_detection_failure()`

```python
def test_load_dataframe_format_detection_failure(self, storage: FileStorage) -> None
```

Teszteli a DataFrame betöltését formátum meghatározási hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_excel_format_detection()`

```python
def test_load_dataframe_excel_format_detection(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None
```

Teszteli a DataFrame betöltését Excel formátum automatikus felismerésével.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_io_error()`

```python
def test_load_dataframe_io_error(self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a DataFrame betöltését IO hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`sample_dataframe`** (`pd.DataFrame`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_read()`

```python
def mock_read() -> None
```

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_format_detection_failure()`

```python
def test_save_object_format_detection_failure(self, storage: FileStorage) -> None
```

Teszteli az objektum mentését formátum meghatározási hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_serialization_error()`

```python
def test_save_object_serialization_error(self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli az objektum mentését szerializációs hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_dump()`

```python
def mock_dump() -> None
```

**Visszatérési érték:**

- Típus: `None`

### `test_save_object_io_error()`

```python
def test_save_object_io_error(self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli az objektum mentését IO hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_mkdir()`

```python
def mock_mkdir() -> None
```

**Visszatérési érték:**

- Típus: `None`

### `test_load_object_format_detection_failure()`

```python
def test_load_object_format_detection_failure(self, storage: FileStorage) -> None
```

Teszteli az objektum betöltését formátum meghatározási hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

### `test_load_object_deserialization_error()`

```python
def test_load_object_deserialization_error(self, storage: FileStorage) -> None
```

Teszteli az objektum betöltését deszerializációs hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

### `test_load_object_os_error()`

```python
def test_load_object_os_error(self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli az objektum betöltését OS hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_open()`

```python
def mock_open() -> None
```

**Visszatérési érték:**

- Típus: `None`

### `test_get_metadata_os_error()`

```python
def test_get_metadata_os_error(self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a metaadatok lekérdezését OS hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_stat()`

```python
def mock_stat() -> None
```

**Visszatérési érték:**

- Típus: `None`

### `test_delete_directory()`

```python
def test_delete_directory(self, storage: FileStorage) -> None
```

Teszteli a könyvtár törlését.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

### `test_delete_io_error()`

```python
def test_delete_io_error(self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a fájl törlését IO hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`temp_dir`** (`Path`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_unlink()`

```python
def mock_unlink() -> None
```

**Visszatérési érték:**

- Típus: `None`

### `test_list_dir_not_directory()`

```python
def test_list_dir_not_directory(self, storage: FileStorage) -> None
```

Teszteli a könyvtár listázását, ha az útvonal nem könyvtár.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)

**Visszatérési érték:**

- Típus: `None`

### `test_list_dir_glob_error()`

```python
def test_list_dir_glob_error(self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch) -> None
```

Teszteli a könyvtár listázását glob hiba esetén.

**Paraméterek:**

- **`self`**
- **`storage`** (`FileStorage`)
- **`monkeypatch`** (`pytest.MonkeyPatch`)

**Visszatérési érték:**

- Típus: `None`

### `mock_glob()`

```python
def mock_glob() -> None
```

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/storage/implementations/test_file_storage.py`](../../tests/neural_ai/data/storage/implementations/test_file_storage.py)
