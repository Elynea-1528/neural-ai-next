# tests/neural_ai/core/config/test_config_factory.py

Config Factory tesztmodul.

Ez a modul tartalmazza a konfigurációs factory teszteit,
ellenőrzi a megfelelő példányosítást és a hibakezelést.

## Importok

```python
from pathlib import Path
from unittest.mock import MagicMock
import pytest
from neural_ai.core.config.exceptions.config_error import ConfigLoadError
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.async_config_interface import AsyncConfigManagerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
# ... és még 2 import
```

## Osztály: `TestConfigManagerFactory`

ConfigManagerFactory osztály tesztjei.

### Metódusok

#### `config_file()`

```python
def config_file(self, tmp_path: Path) -> Path
```

Létrehoz egy ideiglenes config fájlt.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `Path`

#### `test_get_manager_should_return_valid_interface()`

```python
def test_get_manager_should_return_valid_interface(self, config_file: Path) -> None
```

Teszteli, hogy a factory létrehoz egy érvényes konfigurációs interfészt.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_invalid_extension_should_raise_error()`

```python
def test_get_manager_with_invalid_extension_should_raise_error(self) -> None
```

Teszteli, hogy érvénytelen kiterjesztés esetén hiba keletkezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_should_return_valid_interface()`

```python
async def test_get_async_manager_should_return_valid_interface(self) -> None
```

Teszteli, hogy a factory létrehoz egy érvényes aszinkron konfigurációs interfészt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_should_be_created()`

```python
async def test_get_async_manager_should_be_created(self) -> None
```

Teszteli, hogy az aszinkron interfész létrejön.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_should_handle_yaml_extension()`

```python
def test_get_manager_should_handle_yaml_extension(self, config_file: Path) -> None
```

Teszteli, hogy a factory kezeli a YAML kiterjesztést.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_should_handle_yml_extension()`

```python
def test_get_manager_should_handle_yml_extension(self, tmp_path: Path) -> None
```

Teszteli, hogy a factory kezeli a YML kiterjesztést.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_without_extension_should_use_default_yaml()`

```python
def test_get_manager_without_extension_should_use_default_yaml(self, tmp_path: Path) -> None
```

Teszteli, hogy kiterjesztés nélküli fájlnál alapértelmezett YAML kezelőt használ.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_should_return_valid_interface()`

```python
def test_create_manager_should_return_valid_interface(self, config_file: Path) -> None
```

Teszteli, hogy a create_manager létrehoz egy érvényes konfigurációs interfészt.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_manager_with_invalid_type_should_raise_error()`

```python
def test_create_manager_with_invalid_type_should_raise_error(self) -> None
```

Teszteli, hogy érvénytelen típus esetén hiba keletkezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_with_invalid_type_should_raise_error()`

```python
async def test_get_async_manager_with_invalid_type_should_raise_error(self) -> None
```

Teszteli, hogy érvénytelen aszinkron típus esetén hiba keletkezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_supported_extensions_should_return_list()`

```python
def test_get_supported_extensions_should_return_list(self) -> None
```

Teszteli, hogy a támogatott kiterjesztések listája visszaadódik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_supported_async_types_should_return_list()`

```python
def test_get_supported_async_types_should_return_list(self) -> None
```

Teszteli, hogy a támogatott aszinkron típusok listája visszaadódik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_manager_should_add_new_manager()`

```python
def test_register_manager_should_add_new_manager(self, tmp_path: Path) -> None
```

Teszteli, hogy új kezelő regisztrálható.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_should_pass_session_and_logger()`

```python
async def test_get_async_manager_should_pass_session_and_logger(self) -> None
```

Teszteli, hogy az aszinkron kezelő megkapja a sessiont és loggert.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_should_create_separate_instances()`

```python
def test_get_manager_should_create_separate_instances(self, config_file: Path) -> None
```

Teszteli, hogy a factory külön példányokat hoz létre.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_should_handle_valid_kwargs()`

```python
async def test_get_async_manager_should_handle_valid_kwargs(self) -> None
```

Teszteli, hogy az aszinkron kezelő kezeli a valid paramétereket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_async_manager_should_add_new_async_manager()`

```python
def test_register_async_manager_should_add_new_async_manager(self) -> None
```

Teszteli, hogy új aszinkron kezelő regisztrálható.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_async_manager_without_session_should_raise_error()`

```python
async def test_get_async_manager_without_session_should_raise_error(self) -> None
```

Teszteli, hogy session nélkül hiba keletkezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_explicit_type_should_use_that_type()`

```python
def test_get_manager_with_explicit_type_should_use_that_type(self, tmp_path: Path) -> None
```

Teszteli, hogy explicit típusmegadás esetén azt használja.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_register_manager_should_normalize_extension()`

```python
def test_register_manager_should_normalize_extension(self) -> None
```

Teszteli, hogy a register_manager normalizálja a kiterjesztést (88. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_manager_should_validate_extension_not_empty()`

```python
def test_register_manager_should_validate_extension_not_empty(self) -> None
```

Teszteli, hogy a register_manager ellenőrzi az üres kiterjesztést (88. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_manager_should_validate_manager_is_type()`

```python
def test_register_manager_should_validate_manager_is_type(self) -> None
```

Teszteli, hogy a register_manager ellenőrzi a típus érvényességét (91. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_async_manager_should_validate_manager_type_not_empty()`

```python
def test_register_async_manager_should_validate_manager_type_not_empty(self) -> None
```

Teszteli, hogy a register_async_manager ellenőrzi az üres típust (119. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_async_manager_should_validate_async_manager_is_type()`

```python
def test_register_async_manager_should_validate_async_manager_is_type(self) -> None
```

Teszteli, hogy a register_async_manager ellenőrzi a típus érvényességét (125. sor).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_explicit_type_should_normalize_type()`

```python
def test_get_manager_with_explicit_type_should_normalize_type(self, tmp_path: Path) -> None
```

Teszteli, hogy a get_manager normalizálja az explicit típust (161. sor).

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_explicit_type_should_handle_dot_prefix()`

```python
def test_get_manager_with_explicit_type_should_handle_dot_prefix(self, tmp_path: Path) -> None
```

Teszteli, hogy a get_manager kezeli a ponttal kezdődő explicit típust (161. sor).

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_manager_with_explicit_type_should_raise_error_for_invalid_type()`

```python
def test_get_manager_with_explicit_type_should_raise_error_for_invalid_type(self, tmp_path: Path) -> None
```

Teszteli, hogy a get_manager hibát dob érvénytelen explicit típus esetén (161. sor).

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/test_config_factory.py`](../../tests/neural_ai/core/config/test_config_factory.py)
