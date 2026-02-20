# tests/neural_ai/core/test_core_init.py

Tesztek a neural_ai.core.__init__.py modulhoz.

Ez a tesztmodul ellenőrzi a core bootstrap funkcionalitását, beleértve:
- Verzió lekérdezést
- Séma verzió lekérdezést
- Core komponensek inicializálását
- Globális komponens hozzáférést

## Importok

```python
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core import bootstrap_core
from neural_ai.core import get_core_components
from neural_ai.core import get_schema_version
from neural_ai.core import get_version
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.config.exceptions import ConfigValidationError
# ... és még 7 import
```

## Osztály: `TestVersionFunctions`

Tesztek a verzió lekérdező függvényekhez.

### Metódusok

#### `test_get_version_success()`

```python
def test_get_version_success(self) -> None
```

Teszteli a get_version függvényt sikeres verzió lekérdezés esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_version_failure()`

```python
def test_get_version_failure(self) -> None
```

Teszteli a get_version függvényt sikertelen verzió lekérdezés esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_version_returns_string()`

```python
def test_get_version_returns_string(self) -> None
```

Teszteli, hogy a get_version mindig stringgel tér vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_schema_version()`

```python
def test_get_schema_version(self) -> None
```

Teszteli a get_schema_version függvényt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_schema_version_returns_string()`

```python
def test_get_schema_version_returns_string(self) -> None
```

Teszteli, hogy a get_schema_version mindig stringgel tér vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestBootstrapCore`

Tesztek a bootstrap_core függvényhez.

### Metódusok

#### `setup_method()`

```python
def setup_method(self) -> None
```

Teszt előkészítés.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_core_success()`

```python
def test_bootstrap_core_success(self, mock_hardware_factory: MagicMock, mock_system_factory: MagicMock, mock_storage_factory: MagicMock, mock_logger_factory: MagicMock, mock_event_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt sikeres inicializálás esetén.

**Paraméterek:**

- **`self`**
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_system_factory`** (`MagicMock`)
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_core_with_custom_config()`

```python
def test_bootstrap_core_with_custom_config(self, mock_hardware_factory: MagicMock, mock_system_factory: MagicMock, mock_storage_factory: MagicMock, mock_event_factory: MagicMock, mock_logger_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt egyéni konfigurációval.

**Paraméterek:**

- **`self`**
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_system_factory`** (`MagicMock`)
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_core_import_error()`

```python
def test_bootstrap_core_import_error(self, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt import hiba esetén.

**Paraméterek:**

- **`self`**
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_core_returns_core_components()`

```python
def test_bootstrap_core_returns_core_components(self) -> None
```

Teszteli, hogy a bootstrap_core CoreComponents példánnyal tér vissza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_core_with_jforex_enabled()`

```python
def test_bootstrap_core_with_jforex_enabled(self, mock_jforex_factory: MagicMock, mock_hardware_factory: MagicMock, mock_system_factory: MagicMock, mock_storage_factory: MagicMock, mock_logger_factory: MagicMock, mock_event_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezés esetén. Ez a teszt lefedi a 202. sort, ahol a JForex Live Feed opcionálisan inicializálódik.

**Paraméterek:**

- **`self`**
- **`mock_jforex_factory`** (`MagicMock`)
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_system_factory`** (`MagicMock`)
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `get_side_effect()`

```python
def get_side_effect()
```

#### `get_section_side_effect()`

```python
def get_section_side_effect(key)
```

**Paraméterek:**

- **`key`**

#### `test_bootstrap_core_with_jforex_disabled()`

```python
def test_bootstrap_core_with_jforex_disabled(self, mock_jforex_factory: MagicMock, mock_hardware_factory: MagicMock, mock_system_factory: MagicMock, mock_storage_factory: MagicMock, mock_logger_factory: MagicMock, mock_event_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt JForex Live Feed tiltás esetén.

**Paraméterek:**

- **`self`**
- **`mock_jforex_factory`** (`MagicMock`)
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_system_factory`** (`MagicMock`)
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `get_side_effect()`

```python
def get_side_effect(key, default = None)
```

**Paraméterek:**

- **`key`**
- **`default`** = `None`

## Osztály: `TestGetCoreComponents`

Tesztek a get_core_components függvényhez.

### Metódusok

#### `test_get_core_components_first_call()`

```python
def test_get_core_components_first_call(self, mock_bootstrap: MagicMock) -> None
```

Teszteli a get_core_components függvényt első híváskor.

**Paraméterek:**

- **`self`**
- **`mock_bootstrap`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_core_components_cached()`

```python
def test_get_core_components_cached(self, mock_bootstrap: MagicMock) -> None
```

Teszteli a get_core_components függvényt, ha már inicializálva van.

**Paraméterek:**

- **`self`**
- **`mock_bootstrap`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_core_components_returns_core_components()`

```python
def test_get_core_components_returns_core_components(self, mock_bootstrap: MagicMock) -> None
```

Teszteli, hogy a get_core_components CoreComponents példánnyal tér vissza.

**Paraméterek:**

- **`self`**
- **`mock_bootstrap`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestIntegration`

Integrációs tesztek.

### Metódusok

#### `test_version_and_bootstrap_integration()`

```python
def test_version_and_bootstrap_integration(self) -> None
```

Teszteli a verzió lekérdezés és a bootstrap integrációját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_imports_available()`

```python
def test_all_imports_available(self) -> None
```

Teszteli, hogy minden publikus függvény elérhető-e a csomag szintjén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_core_components_singleton_pattern()`

```python
def test_core_components_singleton_pattern(self) -> None
```

Teszteli, hogy a CoreComponents singleton mintát követ-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestBootstrapCoreRealConfig`

Bootstrap valós config fájlokkal.

### Metódusok

#### `test_bootstrap_with_real_yaml_configs()`

```python
def test_bootstrap_with_real_yaml_configs(self, tmp_path: Path) -> None
```

Teljes bootstrap folyamat valós YAML config fájlokkal. Ez a teszt end-to-end ellenőrzi a config → parse → bootstrap láncot. NEM mockol semmit (kivéve hardver/külső rendszerek ha muszáj), valós fájlokból tölt be konfigurációt.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_bootstrap_with_invalid_database_config_raises_error()`

```python
def test_bootstrap_with_invalid_database_config_raises_error(self, tmp_path: Path) -> None
```

Érvénytelen database.yaml ConfigValidationError-t dob.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/test_core_init.py`](../../tests/neural_ai/core/test_core_init.py)
