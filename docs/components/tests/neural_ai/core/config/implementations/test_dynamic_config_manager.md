# tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py

Tesztek a DynamicConfigManager osztályhoz.

## Importok

```python
from datetime import UTC
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager
from neural_ai.core.db.implementations.models import DynamicConfig
```

## Osztály: `TestDynamicConfigManagerInit`

DynamicConfigManager inicializálásának tesztjei.

### Metódusok

#### `test_init_without_session_raises_value_error()`

```python
def test_init_without_session_raises_value_error(self) -> None
```

Teszt: ValueError-t dob, ha nincs session megadva.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_session_success()`

```python
def test_init_with_session_success(self, mock_session: AsyncMock) -> None
```

Teszt: Sikeres inicializálás sessionnel.

**Paraméterek:**

- **`self`**
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_session_and_logger_success()`

```python
def test_init_with_session_and_logger_success(self, mock_session: AsyncMock, mock_logger: MagicMock) -> None
```

Teszt: Sikeres inicializálás sessionnel és loggerrel.

**Paraméterek:**

- **`self`**
- **`mock_session`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerGet`

DynamicConfigManager get metódusának tesztjei.

### Metódusok

#### `test_get_with_multiple_keys_raises_value_error()`

```python
async def test_get_with_multiple_keys_raises_value_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: ValueError-t dob, ha több kulcsot adnak meg.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_from_cache()`

```python
async def test_get_from_cache(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Érték lekérése a cache-ből.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_from_database_success()`

```python
async def test_get_from_database_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Érték lekérése az adatbázisból.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_from_database_not_found_returns_default()`

```python
async def test_get_from_database_not_found_returns_default(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Alapértelmezett érték visszaadása, ha a kulcs nem található.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_database_error_raises_config_error()`

```python
async def test_get_database_error_raises_config_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: ConfigError-t dob adatbázis hiba esetén.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerSet`

DynamicConfigManager set metódusának tesztjei.

### Metódusok

#### `test_set_with_multiple_keys_raises_value_error()`

```python
async def test_set_with_multiple_keys_raises_value_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: ValueError-t dob, ha több kulcsot adnak meg.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_new_config_success()`

```python
async def test_set_new_config_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Új konfiguráció létrehozása.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_existing_config_success()`

```python
async def test_set_existing_config_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Meglévő konfiguráció frissítése.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_database_error_raises_config_error()`

```python
async def test_set_database_error_raises_config_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: ConfigError-t dob adatbázis hiba esetén.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerGetSection`

DynamicConfigManager get_section metódusának tesztjei.

### Metódusok

#### `test_get_section_success()`

```python
async def test_get_section_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Konfigurációs szekció lekérdezése.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_section_not_found_raises_key_error()`

```python
async def test_get_section_not_found_raises_key_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: KeyError-t dob, ha a szekció nem található.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_section_database_error_raises_config_error()`

```python
async def test_get_section_database_error_raises_config_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: ConfigError-t dob adatbázis hiba esetén.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerNotImplementedMethods`

Nem implementált metódusok tesztjei.

### Metódusok

#### `test_save_raises_not_implemented_error()`

```python
async def test_save_raises_not_implemented_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: save metódus NotImplementedError-t dob.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_raises_not_implemented_error()`

```python
async def test_load_raises_not_implemented_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: load metódus NotImplementedError-t dob.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_raises_not_implemented_error()`

```python
async def test_load_directory_raises_not_implemented_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: load_directory metódus NotImplementedError-t dob.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerValidate`

DynamicConfigManager validate metódusának tesztjei.

### Metódusok

#### `test_validate_success()`

```python
async def test_validate_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Sikeres validáció.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_missing_required_field()`

```python
async def test_validate_missing_required_field(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Validáció hiba, ha kötelező mező hiányzik.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_invalid_type()`

```python
async def test_validate_invalid_type(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Validáció hiba, ha az érték típusa nem megfelelő.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerListeners`

Listener metódusok tesztjei.

### Metódusok

#### `test_add_listener_success()`

```python
def test_add_listener_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Listener hozzáadása.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `dummy_listener()`

```python
async def dummy_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_listener_success()`

```python
def test_remove_listener_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Listener eltávolítása.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `dummy_listener()`

```python
async def dummy_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_remove_nonexistent_listener_no_error()`

```python
def test_remove_nonexistent_listener_no_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Nem létező listener eltávolítása nem okoz hibát.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `dummy_listener()`

```python
async def dummy_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerHotReload`

Hot reload metódusok tesztjei.

### Metódusok

#### `test_start_hot_reload_success()`

```python
async def test_start_hot_reload_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Hot reload indítása.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_start_hot_reload_when_already_running_raises_runtime_error()`

```python
async def test_start_hot_reload_when_already_running_raises_runtime_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: RuntimeError-t dob, ha a hot reload már fut.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_hot_reload_success()`

```python
async def test_stop_hot_reload_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Hot reload leállítása.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_stop_hot_reload_when_not_running_no_error()`

```python
async def test_stop_hot_reload_when_not_running_no_error(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Hot reload leállítása nem okoz hibát, ha nem fut.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerGetAll`

DynamicConfigManager get_all metódusának tesztjei.

### Metódusok

#### `test_get_all_success()`

```python
async def test_get_all_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Összes konfiguráció lekérdezése.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_all_with_category_filter()`

```python
async def test_get_all_with_category_filter(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Konfigurációk lekérdezése kategória szerint.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_all_database_error_raises_config_error()`

```python
async def test_get_all_database_error_raises_config_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: ConfigError-t dob adatbázis hiba esetén.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerSetWithMetadata`

DynamicConfigManager set_with_metadata metódusának tesztjei.

### Metódusok

#### `test_set_with_metadata_new_config_success()`

```python
async def test_set_with_metadata_new_config_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Új konfiguráció létrehozása metaadatokkal.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_with_metadata_existing_config_success()`

```python
async def test_set_with_metadata_existing_config_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Meglévő konfiguráció frissítése metaadatokkal.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerDelete`

DynamicConfigManager delete metódusának tesztjei.

### Metódusok

#### `test_delete_existing_config_success()`

```python
async def test_delete_existing_config_success(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Konfiguráció törlése (soft delete).

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_nonexistent_config_returns_false()`

```python
async def test_delete_nonexistent_config_returns_false(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: False visszaadása, ha a konfiguráció nem található.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_database_error_raises_config_error()`

```python
async def test_delete_database_error_raises_config_error(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: ConfigError-t dob adatbázis hiba esetén.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `CustomType`

## Osztály: `TestDynamicConfigManagerDetermineValueType`

_determine_value_type metódus tesztjei.

### Metódusok

#### `test_determine_value_type_bool()`

```python
def test_determine_value_type_bool(self) -> None
```

Teszt: Boolean típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_int()`

```python
def test_determine_value_type_int(self) -> None
```

Teszt: Integer típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_float()`

```python
def test_determine_value_type_float(self) -> None
```

Teszt: Float típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_str()`

```python
def test_determine_value_type_str(self) -> None
```

Teszt: String típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_list()`

```python
def test_determine_value_type_list(self) -> None
```

Teszt: List típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_dict()`

```python
def test_determine_value_type_dict(self) -> None
```

Teszt: Dict típus felismerése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_determine_value_type_unknown_defaults_to_str()`

```python
def test_determine_value_type_unknown_defaults_to_str(self) -> None
```

Teszt: Ismeretlen típus esetén str visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerNotifyListeners`

_notify_listeners metódus tesztjei.

### Metódusok

#### `test_notify_listeners_success()`

```python
async def test_notify_listeners_success(self, config_manager: DynamicConfigManager) -> None
```

Teszt: Listener-ek értesítése.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)

**Visszatérési érték:**

- Típus: `None`

#### `test_listener()`

```python
async def test_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_notify_listeners_with_exception_in_listener()`

```python
async def test_notify_listeners_with_exception_in_listener(self, config_manager: DynamicConfigManager, mock_logger: MagicMock) -> None
```

Teszt: Listener hiba esetén a többi listener még mindig hívódik.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `error_listener()`

```python
async def error_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `good_listener()`

```python
async def good_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDynamicConfigManagerCheckForUpdates`

_check_for_updates metódus tesztjei.

### Metódusok

#### `test_check_for_updates_first_time_loads_all()`

```python
async def test_check_for_updates_first_time_loads_all(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Első alkalommal betölti az összes konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_for_updates_with_changes()`

```python
async def test_check_for_updates_with_changes(self, config_manager: DynamicConfigManager, mock_session: AsyncMock) -> None
```

Teszt: Változások észlelése és cache frissítése.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_listener()`

```python
async def test_listener(key: str, value: Any) -> None
```

**Paraméterek:**

- **`key`** (`str`)
- **`value`** (`Any`)

**Visszatérési érték:**

- Típus: `None`

#### `test_check_for_updates_database_error_logged()`

```python
async def test_check_for_updates_database_error_logged(self, config_manager: DynamicConfigManager, mock_session: AsyncMock, mock_logger: MagicMock) -> None
```

Teszt: Adatbázis hiba esetén a hiba naplózásra kerül.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`DynamicConfigManager`)
- **`mock_session`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

### `mock_session()`

```python
def mock_session() -> AsyncMock
```

Mock AsyncSession létrehozása.

**Visszatérési érték:**

- Típus: `AsyncMock`

### `mock_logger()`

```python
def mock_logger() -> MagicMock
```

Mock Logger létrehozása.

**Visszatérési érték:**

- Típus: `MagicMock`

### `config_manager()`

```python
def config_manager(mock_session: AsyncMock) -> DynamicConfigManager
```

DynamicConfigManager létrehozása mock sessionnel.

**Paraméterek:**

- **`mock_session`** (`AsyncMock`)

**Visszatérési érték:**

- Típus: `DynamicConfigManager`

### `config_manager_with_logger()`

```python
def config_manager_with_logger(mock_session: AsyncMock, mock_logger: MagicMock) -> DynamicConfigManager
```

DynamicConfigManager létrehozása loggerrel.

**Paraméterek:**

- **`mock_session`** (`AsyncMock`)
- **`mock_logger`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `DynamicConfigManager`

---

**Forrásfájl:** [`tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py`](../../tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py)
