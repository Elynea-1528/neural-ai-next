# tests/neural_ai/ui/interfaces/test_data_service_interface.py

DataServiceInterface tesztelése.

Ez a tesztcsomag ellenőrzi a DataServiceInterface interfész megfelelő definícióját
és a Protocol szerződés betartását.

## Importok

```python
import sys
from collections.abc import Generator
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas
import pytest
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
```

## Osztály: `MockDataService(DataServiceInterface)`

Mock implementáció a DataServiceInterface teszteléséhez.

### Metódusok

#### `load_data()`

```python
def load_data(self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000) -> Generator[list[dict[str, Any]], None, None]
```

Mock adatok betöltése.

**Paraméterek:**

- **`self`**
- **`source`** (`str`)
- **`filters`** (`dict[str, Any] | None`) = `None`
- **`chunk_size`** (`int`) = `10000`

**Visszatérési érték:**

- Típus: `Generator[list[dict[str, Any]], None, None]`

#### `get_data_sources()`

```python
def get_data_sources(self) -> list[dict[str, str]]
```

Mock adatforrások.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, str]]`

#### `get_data_info()`

```python
def get_data_info(self, source: str) -> dict[str, Any]
```

Mock adatforrás információk.

**Paraméterek:**

- **`self`**
- **`source`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `apply_filters()`

```python
def apply_filters(self, data: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]
```

Mock szűrés.

**Paraméterek:**

- **`self`**
- **`data`** (`list[dict[str, Any]]`)
- **`filters`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`

#### `export_data()`

```python
def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool
```

Mock exportálás.

**Paraméterek:**

- **`self`**
- **`data`** (`list[dict[str, Any]]`)
- **`format`** (`str`)
- **`destination`** (`str`)

**Visszatérési érték:**

- Típus: `bool`

#### `get_default_date_range()`

```python
def get_default_date_range(self) -> tuple[datetime, datetime]
```

Mock alapértelmezett dátumtartomány.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `tuple[datetime, datetime]`

#### `download_history()`

```python
async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]
```

Mock történelmi adatok letöltése.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`)
- **`start`** (`datetime`)
- **`end`** (`datetime`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `list_available_data()`

```python
def list_available_data(self, symbol: str | None = None) -> pd.DataFrame
```

Mock elérhető adatok listázása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `pd.DataFrame`

#### `get_storage_path()`

```python
def get_storage_path(self) -> Path
```

Mock tárhely elérési út.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Path`

#### `get_configured_symbols()`

```python
def get_configured_symbols(self) -> list[str]
```

Mock konfigurált szimbólumok.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`

## Osztály: `TestDataServiceInterface`

DataServiceInterface tesztosztály.

### Metódusok

#### `test_interface_is_protocol()`

```python
def test_interface_is_protocol(self)
```

Teszteli, hogy az interfész Protocol-t követ.

**Paraméterek:**

- **`self`**

#### `test_interface_is_runtime_checkable()`

```python
def test_interface_is_runtime_checkable(self)
```

Teszteli, hogy az interfész runtime_checkable.

**Paraméterek:**

- **`self`**

#### `test_mock_implements_interface()`

```python
def test_mock_implements_interface(self)
```

Teszteli, hogy a mock osztály implementálja az interfészt.

**Paraméterek:**

- **`self`**

#### `test_load_data_signature()`

```python
def test_load_data_signature(self)
```

Teszteli a load_data metódus szignatúráját.

**Paraméterek:**

- **`self`**

#### `test_get_data_sources_return_type()`

```python
def test_get_data_sources_return_type(self)
```

Teszteli a get_data_sources visszatérési értékét.

**Paraméterek:**

- **`self`**

#### `test_get_data_info_return_type()`

```python
def test_get_data_info_return_type(self)
```

Teszteli a get_data_info visszatérési értékét.

**Paraméterek:**

- **`self`**

#### `test_apply_filters_functionality()`

```python
def test_apply_filters_functionality(self)
```

Teszteli az apply_filters metódust.

**Paraméterek:**

- **`self`**

#### `test_export_data_return_type()`

```python
def test_export_data_return_type(self)
```

Teszteli az export_data visszatérési értékét.

**Paraméterek:**

- **`self`**

#### `test_get_default_date_range()`

```python
def test_get_default_date_range(self)
```

Teszteli a get_default_date_range metódust.

**Paraméterek:**

- **`self`**

#### `test_download_history_async()`

```python
async def test_download_history_async(self)
```

Teszteli a download_history aszinkron metódust.

**Paraméterek:**

- **`self`**

#### `test_list_available_data_return_type()`

```python
def test_list_available_data_return_type(self)
```

Teszteli a list_available_data visszatérési értékét.

**Paraméterek:**

- **`self`**

#### `test_list_available_data_with_symbol_filter()`

```python
def test_list_available_data_with_symbol_filter(self)
```

Teszteli a list_available_data szűrést.

**Paraméterek:**

- **`self`**

#### `test_get_storage_path_return_type()`

```python
def test_get_storage_path_return_type(self)
```

Teszteli a get_storage_path visszatérési értékét.

**Paraméterek:**

- **`self`**

#### `test_get_configured_symbols()`

```python
def test_get_configured_symbols(self)
```

Teszteli a get_configured_symbols metódust.

**Paraméterek:**

- **`self`**

#### `test_interface_methods_exist()`

```python
def test_interface_methods_exist(self)
```

Teszteli, hogy az interfész minden metódusa létezik.

**Paraméterek:**

- **`self`**

#### `test_interface_type_hints()`

```python
def test_interface_type_hints(self)
```

Teszteli a típusos megjelöléseket.

**Paraméterek:**

- **`self`**

## Osztály: `TestDataServiceInterfaceIntegration`

Integrációs tesztek a DataServiceInterface-hez.

### Metódusok

#### `test_chunk_based_loading()`

```python
def test_chunk_based_loading(self)
```

Teszteli a chunk-based adatbetöltést.

**Paraméterek:**

- **`self`**

#### `test_data_pipeline_flow()`

```python
def test_data_pipeline_flow(self)
```

Teszteli az adatfeldolgozási folyamatot.

**Paraméterek:**

- **`self`**

#### `test_async_data_download_flow()`

```python
async def test_async_data_download_flow(self)
```

Teszteli az aszinkron adatletöltési folyamatot.

**Paraméterek:**

- **`self`**

---

**Forrásfájl:** [`tests/neural_ai/ui/interfaces/test_data_service_interface.py`](../../tests/neural_ai/ui/interfaces/test_data_service_interface.py)
