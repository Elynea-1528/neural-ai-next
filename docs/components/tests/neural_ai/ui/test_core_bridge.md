# tests/neural_ai/ui/test_core_bridge.py

Core Bridge tesztesetek - teljes lefedettség biztosítása.

## Importok

```python
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch
import pytest
from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.core.base.implementations.singleton import SingletonMeta
```

## Osztály: `TestCoreBridge`

CoreBridge osztály tesztelése.

### Metódusok

#### `setup_method()`

```python
def setup_method(cls)
```

Reset singleton for test isolation.

**Paraméterek:**

- **`cls`**

#### `teardown_method()`

```python
def teardown_method(cls)
```

Clean up after each test.

**Paraméterek:**

- **`cls`**

#### `test_singleton_pattern()`

```python
def test_singleton_pattern(self)
```

Singleton minta tesztelése.

**Paraméterek:**

- **`self`**

#### `test_initialization()`

```python
def test_initialization(self)
```

Inicializálás tesztelése.

**Paraméterek:**

- **`self`**

#### `test_initialization_strategy_service()`

```python
def test_initialization_strategy_service(self)
```

Strategy Service inicializálás tesztelése.

**Paraméterek:**

- **`self`**

#### `test_initialization_strategy_service_error()`

```python
def test_initialization_strategy_service_error(self)
```

Strategy Service inicializálási hiba tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_not_initialized()`

```python
def test_get_component_not_initialized(self)
```

Komponens lekérés inicializálatlan bridge esetén.

**Paraméterek:**

- **`self`**

#### `test_get_component_parquet_storage()`

```python
def test_get_component_parquet_storage(self)
```

Parquet storage komponens lekérés tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_parquet_storage_none()`

```python
def test_get_component_parquet_storage_none(self)
```

Parquet storage None esetén.

**Paraméterek:**

- **`self`**

#### `test_get_component_bi5_downloader()`

```python
def test_get_component_bi5_downloader(self)
```

BI5 downloader komponens létrehozás tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_bi5_downloader_missing_deps()`

```python
def test_get_component_bi5_downloader_missing_deps(self)
```

BI5 downloader hiányzó függőségekkel.

**Paraméterek:**

- **`self`**

#### `test_get_component_strategy_service()`

```python
def test_get_component_strategy_service(self)
```

Strategy Service komponens lekérés tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_strategy_service_none()`

```python
def test_get_component_strategy_service_none(self)
```

Strategy Service None esetén.

**Paraméterek:**

- **`self`**

#### `test_get_component_config()`

```python
def test_get_component_config(self)
```

Config komponens lekérés tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_config_none()`

```python
def test_get_component_config_none(self)
```

Config None esetén.

**Paraméterek:**

- **`self`**

#### `test_get_component_unknown()`

```python
def test_get_component_unknown(self)
```

Ismeretlen komponens típus tesztelése.

**Paraméterek:**

- **`self`**

#### `test_get_component_logger()`

```python
def test_get_component_logger(self)
```

Logger komponens lekérés tesztelése.

**Paraméterek:**

- **`self`**

#### `test_send_command_connected()`

```python
def test_send_command_connected(self)
```

Parancs küldés csatlakoztatott bridge esetén.

**Paraméterek:**

- **`self`**

#### `test_send_command_not_connected()`

```python
def test_send_command_not_connected(self)
```

Parancs küldés nem csatlakoztatott bridge esetén.

**Paraméterek:**

- **`self`**

#### `test_get_system_info_connected()`

```python
def test_get_system_info_connected(self)
```

Rendszerinformáció lekérés csatlakoztatott bridge esetén.

**Paraméterek:**

- **`self`**

#### `test_get_system_info_not_connected()`

```python
def test_get_system_info_not_connected(self)
```

Rendszerinformáció lekérés nem csatlakoztatott bridge esetén.

**Paraméterek:**

- **`self`**

#### `test_core_property()`

```python
def test_core_property(self)
```

Core property tesztelése.

**Paraméterek:**

- **`self`**

#### `test_is_connected_property()`

```python
def test_is_connected_property(self)
```

is_connected property tesztelése.

**Paraméterek:**

- **`self`**

---

**Forrásfájl:** [`tests/neural_ai/ui/test_core_bridge.py`](../../tests/neural_ai/ui/test_core_bridge.py)
