# tests/neural_ai/data/storage/implementations/test_parquet_storage.py

ParquetStorageService tesztesetek - teljes lefedettséget biztosít.

Ez a modul tartalmazza a ParquetStorageService osztály minden metódusának
egységtesztjeit, biztosítva a 100% kódlefedettséget.

Author: Neural AI Next Team
Version: 2.0.0

## Importok

```python
import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.core.base.implementations.singleton import SingletonMeta
```

## Konstansok

- **`service`**
: `ParquetStorageService(logger=mock_logger, config=None, event_bus=None, base_path=str(temp_dir), compression='snappy', hardware=mock_hardware)`


## Osztály: `TestParquetStorageService`

ParquetStorageService osztály tesztesetek.

### Metódusok

#### `test_initialization_with_hardware_and_logger()`

```python
async def test_initialization_with_hardware_and_logger(self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock)
```

Teszteli az inicializációt hardware és logger interfészekkel.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`mock_hardware`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

#### `test_initialization_without_hardware_and_logger()`

```python
async def test_initialization_without_hardware_and_logger(self, temp_dir: Path)
```

Teszteli az inicializációt factory-k használatával.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

#### `test_backend_selection_avx2()`

```python
def test_backend_selection_avx2(self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock)
```

Teszteli a PolarsBackend kiválasztását AVX2 támogatással.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`mock_hardware`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

#### `test_backend_selection_no_avx2()`

```python
def test_backend_selection_no_avx2(self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock)
```

Teszteli a PandasBackend kiválasztását AVX2 nélkül.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`mock_hardware`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

#### `test_get_path_with_unique_id()`

```python
def test_get_path_with_unique_id(self, storage_service: ParquetStorageService)
```

Teszteli az elérési út generálást egyedi azonosítóval.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_get_path_without_unique_id()`

```python
def test_get_path_without_unique_id(self, storage_service: ParquetStorageService)
```

Teszteli az elérési út generálást időbélyeggel.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_store_tick_data_success()`

```python
async def test_store_tick_data_success(self, storage_service: ParquetStorageService, mock_logger: MagicMock)
```

Teszteli a tick adatok sikeres tárolását.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`mock_logger`** (`MagicMock`)

#### `test_store_tick_data_empty_dataframe()`

```python
async def test_store_tick_data_empty_dataframe(self, storage_service: ParquetStorageService)
```

Teszteli az üres DataFrame visszautasítását.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_store_tick_data_missing_columns()`

```python
async def test_store_tick_data_missing_columns(self, storage_service: ParquetStorageService)
```

Teszteli a hiányzó oszlopok visszautasítását.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_read_tick_data_no_files()`

```python
async def test_read_tick_data_no_files(self, storage_service: ParquetStorageService)
```

Teszteli az olvasást amikor nincsenek fájlok.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_read_tick_data_with_files()`

```python
async def test_read_tick_data_with_files(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli az olvasást létező fájlokkal.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_get_available_dates()`

```python
async def test_get_available_dates(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli az elérhető dátumok lekérdezést.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_get_available_dates_no_symbol()`

```python
async def test_get_available_dates_no_symbol(self, storage_service: ParquetStorageService)
```

Teszteli az elérhető dátumokat nem létező szimbólum esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_calculate_checksum_no_files()`

```python
async def test_calculate_checksum_no_files(self, storage_service: ParquetStorageService)
```

Teszteli a checksum számítást amikor nincsenek fájlok.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_calculate_checksum_with_files()`

```python
async def test_calculate_checksum_with_files(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a checksum számítást létező fájlokkal.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_verify_data_integrity_valid()`

```python
async def test_verify_data_integrity_valid(self, storage_service: ParquetStorageService, temp_dir: Path, mock_logger: MagicMock)
```

Teszteli az adat integritás ellenőrzést érvényes adatokkal.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)
- **`mock_logger`** (`MagicMock`)

#### `test_verify_data_integrity_no_files()`

```python
async def test_verify_data_integrity_no_files(self, storage_service: ParquetStorageService)
```

Teszteli az adat integritás ellenőrzést hiányzó fájlok esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_verify_data_integrity_missing_columns()`

```python
async def test_verify_data_integrity_missing_columns(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli az adat integritás ellenőrzést hiányzó oszlopokkal.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_get_storage_stats()`

```python
async def test_get_storage_stats(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a tárolási statisztikák lekérdezést.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_concat_dataframes_polars()`

```python
def test_concat_dataframes_polars(self, storage_service: ParquetStorageService)
```

Teszteli a DataFrame összefűzést Polars esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_concat_dataframes_pandas()`

```python
def test_concat_dataframes_pandas(self, storage_service: ParquetStorageService)
```

Teszteli a DataFrame összefűzést Pandas esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_deduplicate_data_polars()`

```python
def test_deduplicate_data_polars(self, storage_service: ParquetStorageService)
```

Teszteli a deduplikációt Polars esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_deduplicate_data_pandas()`

```python
def test_deduplicate_data_pandas(self, storage_service: ParquetStorageService)
```

Teszteli a deduplikációt Pandas esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_sort_by_timestamp_polars()`

```python
def test_sort_by_timestamp_polars(self, storage_service: ParquetStorageService)
```

Teszteli a rendezést timestamp szerint Polars esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_sort_by_timestamp_pandas()`

```python
def test_sort_by_timestamp_pandas(self, storage_service: ParquetStorageService)
```

Teszteli a rendezést timestamp szerint Pandas esetén.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_filter_by_timestamp()`

```python
def test_filter_by_timestamp(self, storage_service: ParquetStorageService)
```

Teszteli az időbélyeg szerinti szűrést.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_read_parquet_async()`

```python
def test_read_parquet_async(self, storage_service: ParquetStorageService)
```

Teszteli az aszinkron Parquet olvasást.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `run_test()`

```python
async def run_test()
```

#### `test_save_dataframe()`

```python
def test_save_dataframe(self, storage_service: ParquetStorageService)
```

Teszteli a DataFrame mentését StorageInterface-en keresztül.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_load_dataframe()`

```python
def test_load_dataframe(self, storage_service: ParquetStorageService)
```

Teszteli a DataFrame betöltését StorageInterface-en keresztül.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)

#### `test_exists()`

```python
def test_exists(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli az útvonal létezésének ellenőrzését.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_get_metadata()`

```python
def test_get_metadata(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a fájl metaadatainak lekérdezését.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_delete_file()`

```python
def test_delete_file(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a fájl törlését.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_delete_directory()`

```python
def test_delete_directory(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a könyvtár törlését.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

#### `test_list_dir()`

```python
def test_list_dir(self, storage_service: ParquetStorageService, temp_dir: Path)
```

Teszteli a könyvtár tartalmának listázását.

**Paraméterek:**

- **`self`**
- **`storage_service`** (`ParquetStorageService`)
- **`temp_dir`** (`Path`)

### `temp_dir()`

```python
def temp_dir()
```

Ideiglenes könyvtár fixture.

### `mock_hardware()`

```python
def mock_hardware()
```

Mock HardwareInterface fixture.

### `mock_logger()`

```python
def mock_logger() -> MagicMock
```

Mock LoggerInterface fixture.

**Visszatérési érték:**

- Típus: `MagicMock`

### `clear_singletons()`

```python
def clear_singletons()
```

Singleton példányok törlése minden teszt előtt.

### `storage_service()`

```python
async def storage_service(temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock)
```

ParquetStorageService fixture teljes mock konfigurációval.

**Paraméterek:**

- **`temp_dir`** (`Path`)
- **`mock_hardware`** (`MagicMock`)
- **`mock_logger`** (`MagicMock`)

---

**Forrásfájl:** [`tests/neural_ai/data/storage/implementations/test_parquet_storage.py`](../../tests/neural_ai/data/storage/implementations/test_parquet_storage.py)
