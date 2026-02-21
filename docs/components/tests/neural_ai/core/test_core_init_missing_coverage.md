# tests/neural_ai/core/test_core_init_missing_coverage.py

Tesztek a neural_ai.core.__init__.py hiányzó coverage ágaihoz.

Ez a tesztmodul kiegészíti a test_core_init.py-t, és a következő
hiányzó ágakat fedi le:
- Storage inicializálási hiba (144-147)
- JForex Live Feed inicializálás (200-202)

## Importok

```python
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.core import bootstrap_core
```

## Osztály: `TestBootstrapCoreStorageError`

Tesztek a bootstrap_core storage hibakezelésére.

### Metódusok

#### `test_bootstrap_core_storage_init_failure()`

```python
def test_bootstrap_core_storage_init_failure(self, mock_storage_factory: MagicMock, mock_event_factory: MagicMock, mock_db_factory: MagicMock, mock_hardware_factory: MagicMock, mock_logger_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt storage inicializálási hiba esetén. Ez a teszt lefedi a 144-147 sorokat (storage exception handling).

**Paraméterek:**

- **`self`**
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_db_factory`** (`MagicMock`)
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestBootstrapCoreJForexLiveFeed`

Tesztek a bootstrap_core JForex Live Feed inicializálására.

### Metódusok

#### `test_bootstrap_core_jforex_live_feed_enabled()`

```python
def test_bootstrap_core_jforex_live_feed_enabled(self, mock_jforex_factory: MagicMock, mock_persister: MagicMock, mock_system_factory: MagicMock, mock_storage_factory: MagicMock, mock_event_factory: MagicMock, mock_db_factory: MagicMock, mock_hardware_factory: MagicMock, mock_logger_factory: MagicMock, mock_config_factory: MagicMock, mock_di_container: MagicMock) -> None
```

Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezve esetén. Ez a teszt lefedi a 200-202 sorokat (JForex live feed init).

**Paraméterek:**

- **`self`**
- **`mock_jforex_factory`** (`MagicMock`)
- **`mock_persister`** (`MagicMock`)
- **`mock_system_factory`** (`MagicMock`)
- **`mock_storage_factory`** (`MagicMock`)
- **`mock_event_factory`** (`MagicMock`)
- **`mock_db_factory`** (`MagicMock`)
- **`mock_hardware_factory`** (`MagicMock`)
- **`mock_logger_factory`** (`MagicMock`)
- **`mock_config_factory`** (`MagicMock`)
- **`mock_di_container`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `mock_get()`

```python
def mock_get(key: str, subkey: str | None = None) -> dict
```

**Paraméterek:**

- **`key`** (`str`)
- **`subkey`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `dict`

---

**Forrásfájl:** [`tests/neural_ai/core/test_core_init_missing_coverage.py`](../../tests/neural_ai/core/test_core_init_missing_coverage.py)
