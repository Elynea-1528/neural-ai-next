# tests/neural_ai/data/storage/backends/test_polars_backend.py

Polars Backend Teszt Modul.

Ez a modul tartalmazza a PolarsBackend osztály tesztjeit.

## Importok

```python
import tempfile
from pathlib import Path
from typing import Any
import pytest
from neural_ai.data.storage.backends.polars_backend import PolarsBackend
from neural_ai.data.storage.backends.polars_backend import PolarsDataFrame
from neural_ai.data.storage.backends.polars_backend import PolarsDataFrame
from neural_ai.data.storage.backends.polars_backend import PolarsDataFrame
from neural_ai.data.storage.backends.polars_backend import PolarsDataFrame
from neural_ai.data.storage.backends.polars_backend import PolarsDataFrame
```

## Osztály: `TestPolarsDataFrame`

PolarsDataFrame wrapper osztály tesztjei.

### Metódusok

#### `test_init()`

```python
def test_init(self) -> None
```

Teszteli a PolarsDataFrame inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_import_polars()`

```python
def test_import_polars(self) -> None
```

Teszteli a lazy import funkcionalitást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_pl_property()`

```python
def test_pl_property(self) -> None
```

Teszteli a pl property-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_pa_property()`

```python
def test_pa_property(self) -> None
```

Teszteli a pa property-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_pq_property()`

```python
def test_pq_property(self) -> None
```

Teszteli a pq property-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPolarsBackend`

PolarsBackend osztály tesztjei.

### Metódusok

#### `logger()`

```python
def logger(self, mocker)
```

Visszaad egy mock logger-t.

**Paraméterek:**

- **`self`**
- **`mocker`**

#### `backend()`

```python
def backend(self, logger) -> PolarsBackend
```

Visszaad egy PolarsBackend példányt.

**Paraméterek:**

- **`self`**
- **`logger`**

**Visszatérési érték:**

- Típus: `PolarsBackend`

#### `sample_dataframe()`

```python
def sample_dataframe(self, backend: PolarsBackend) -> Any
```

Visszaad egy mint DataFrame-et.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)

**Visszatérési érték:**

- Típus: `Any`

#### `temp_dir()`

```python
def temp_dir(self) -> Path
```

Visszaad egy ideiglenes könyvtárat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`

#### `test_init()`

```python
def test_init(self, backend: PolarsBackend) -> None
```

Teszteli a PolarsBackend inicializálását.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)

**Visszatérési érték:**

- Típus: `None`

#### `test_write_basic()`

```python
def test_write_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli az alap write műveletet.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_write_with_compression()`

```python
def test_write_with_compression(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a write műveletet tömörítéssel.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_write_invalid_data()`

```python
def test_write_invalid_data(self, backend: PolarsBackend, temp_dir: Path) -> None
```

Teszteli a write műveletet érvénytelen adatokkal.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_write_invalid_path()`

```python
def test_write_invalid_path(self, backend: PolarsBackend, sample_dataframe: Any) -> None
```

Teszteli a write műveletet érvénytelen elérési úttal.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_basic()`

```python
def test_read_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli az alap read műveletet.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_with_columns()`

```python
def test_read_with_columns(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a read műveletet oszlopszűréssel.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_file_not_found()`

```python
def test_read_file_not_found(self, backend: PolarsBackend, temp_dir: Path) -> None
```

Teszteli a read műveletet nem létező fájllal.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_chunked()`

```python
def test_read_chunked(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a chunkolt olvasást.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_append_to_new_file()`

```python
def test_append_to_new_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a hozzáfűzést új fájlhoz.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_append_to_existing_file()`

```python
def test_append_to_existing_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a hozzáfűzést meglévő fájlhoz.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_append_with_schema_validation_valid()`

```python
def test_append_with_schema_validation_valid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_append_with_schema_validation_invalid()`

```python
def test_append_with_schema_validation_invalid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_append_invalid_data()`

```python
def test_append_invalid_data(self, backend: PolarsBackend, temp_dir: Path) -> None
```

Teszteli a hozzáfűzést érvénytelen adatokkal.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_supports_format()`

```python
def test_supports_format(self, backend: PolarsBackend) -> None
```

Teszteli a supports_format metódust.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_info()`

```python
def test_get_info(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a get_info metódust.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_info_file_not_found()`

```python
def test_get_info_file_not_found(self, backend: PolarsBackend, temp_dir: Path) -> None
```

Teszteli a get_info metódust nem létező fájllal.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_data()`

```python
def test_validate_data(self, backend: PolarsBackend, sample_dataframe: Any) -> None
```

Teszteli a validate_data metódust.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_repr()`

```python
def test_repr(self, backend: PolarsBackend) -> None
```

Teszteli a __repr__ metódust.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)

**Visszatérési érték:**

- Típus: `None`

#### `test_write_partitioned()`

```python
def test_write_partitioned(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a particionált írást.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_with_filters()`

```python
def test_read_with_filters(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli az olvasást szűrőkkel.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_schema_valid()`

```python
def test_validate_schema_valid(self, backend: PolarsBackend, sample_dataframe: Any) -> None
```

Teszteli a _validate_schema metódust érvényes esetre.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_schema_invalid()`

```python
def test_validate_schema_invalid(self, backend: PolarsBackend, sample_dataframe: Any) -> None
```

Teszteli a _validate_schema metódust érvénytelen esetre.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_schema_exception()`

```python
def test_validate_schema_exception(self, backend: PolarsBackend) -> None
```

Teszteli a _validate_schema metódust kivétel esetén.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)

**Visszatérési érték:**

- Típus: `None`

#### `test_read_chunked_implementation()`

```python
def test_read_chunked_implementation(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None
```

Teszteli a _read_chunked metódust.

**Paraméterek:**

- **`self`**
- **`backend`** (`PolarsBackend`)
- **`sample_dataframe`** (`Any`)
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/storage/backends/test_polars_backend.py`](../../tests/neural_ai/data/storage/backends/test_polars_backend.py)
