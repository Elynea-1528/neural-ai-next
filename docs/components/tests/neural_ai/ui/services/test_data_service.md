# tests/neural_ai/ui/services/test_data_service.py

Data Service tesztelése.

Ez a modul a DataService osztály tesztjeit tartalmazza.

## Importok

```python
import unittest
from datetime import UTC
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import PropertyMock
from unittest.mock import patch
import pandas
# ... és még 12 import
```

## Osztály: `TestDataService(unittest.IsolatedAsyncioTestCase)`

DataService osztály tesztjei.

### Metódusok

#### `setUp()`

```python
def setUp(self) -> None
```

Teszt előkészítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init()`

```python
def test_init(self) -> None
```

Teszteli a DataService inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_data()`

```python
def test_load_data(self) -> None
```

Teszteli az adatok betöltését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_data_invalid_source()`

```python
def test_load_data_invalid_source(self) -> None
```

Teszteli a hibakezelést érvénytelen adatforrás esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_data_sources()`

```python
def test_get_data_sources(self) -> None
```

Teszteli az adatforrások lekérdezését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_data_info()`

```python
def test_get_data_info(self) -> None
```

Teszteli az adatforrás információk lekérdezését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_data_info_invalid_source()`

```python
def test_get_data_info_invalid_source(self) -> None
```

Teszteli a hibakezelést érvénytelen adatforrás esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_apply_filters()`

```python
def test_apply_filters(self) -> None
```

Teszteli a szűrők alkalmazását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_apply_filters_range()`

```python
def test_apply_filters_range(self) -> None
```

Teszteli a tartomány szűrést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_export_data()`

```python
def test_export_data(self) -> None
```

Teszteli az adatok exportálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_export_data_invalid_format()`

```python
def test_export_data_invalid_format(self) -> None
```

Teszteli a hibakezelést érvénytelen formátum esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_export_data_empty()`

```python
def test_export_data_empty(self) -> None
```

Teszteli az üres adatok exportálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_list_available_data()`

```python
def test_list_available_data(self, mock_run: MagicMock) -> None
```

Teszteli az elérhető adatok listázását (csak tick_data).

**Paraméterek:**

- **`self`**
- **`mock_run`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_list_available_data_with_symbol()`

```python
def test_list_available_data_with_symbol(self, mock_run: MagicMock) -> None
```

Teszteli az elérhető adatok listázását egyedi szimbólummal.

**Paraméterek:**

- **`self`**
- **`mock_run`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_list_available_data_no_files()`

```python
def test_list_available_data_no_files(self, mock_run: MagicMock) -> None
```

Teszteli az elérhető adatok listázását, ha nincs fájl.

**Paraméterek:**

- **`self`**
- **`mock_run`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_storage_path()`

```python
def test_get_storage_path(self) -> None
```

Teszteli a tárolási útvonal lekérdezését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_storage_path_default()`

```python
def test_get_storage_path_default(self) -> None
```

Teszteli az alapértelmezett tárolási útvonal lekérdezését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_valid_config()`

```python
def test_get_configured_symbols_with_valid_config(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését érvényes konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_empty_config()`

```python
def test_get_configured_symbols_with_empty_config(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését üres konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_none_config()`

```python
def test_get_configured_symbols_with_none_config(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését None konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_invalid_config_type()`

```python
def test_get_configured_symbols_with_invalid_config_type(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését érvénytelen típusú konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_no_config()`

```python
def test_get_configured_symbols_with_no_config(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését, ha nincs konfig.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_configured_symbols_with_exception()`

```python
def test_get_configured_symbols_with_exception(self) -> None
```

Teszteli a konfigurált szimbólumok lekérdezését kivétel esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_generate_mock_data()`

```python
def test_generate_mock_data(self) -> None
```

Teszteli a mock adatok generálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_generate_mock_data_with_filters()`

```python
def test_generate_mock_data_with_filters(self) -> None
```

Teszteli a mock adatok generálását szűrőkkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_download_history_with_existing_data_skip()`

```python
async def test_download_history_with_existing_data_skip(self, mock_sleep: MagicMock, mock_print: MagicMock, mock_stat: MagicMock, mock_exists: MagicMock) -> None
```

Teszteli a download_history metódust, amikor az adat már létezik és skip-eli.

**Paraméterek:**

- **`self`**
- **`mock_sleep`** (`MagicMock`)
- **`mock_print`** (`MagicMock`)
- **`mock_stat`** (`MagicMock`)
- **`mock_exists`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `get_component_side_effect()`

```python
def get_component_side_effect(name: str) -> Any
```

**Paraméterek:**

- **`name`** (`str`)

**Visszatérési érték:**

- Típus: `Any`

#### `test_download_history_with_new_data_download()`

```python
async def test_download_history_with_new_data_download(self, mock_sleep: MagicMock, mock_print: MagicMock, mock_exists: MagicMock) -> None
```

Teszteli a download_history metódust, amikor új adat letöltésre kerül.

**Paraméterek:**

- **`self`**
- **`mock_sleep`** (`MagicMock`)
- **`mock_print`** (`MagicMock`)
- **`mock_exists`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `get_component_side_effect()`

```python
def get_component_side_effect(name: str) -> Any
```

**Paraméterek:**

- **`name`** (`str`)

**Visszatérési érték:**

- Típus: `Any`

---

**Forrásfájl:** [`tests/neural_ai/ui/services/test_data_service.py`](../../tests/neural_ai/ui/services/test_data_service.py)
