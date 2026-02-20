# tests/neural_ai/core/config/implementations/test_yaml_config_manager.py

YAMLConfigManager tesztek.

## Importok

```python
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import Mock
import pytest
import yaml
from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations.yaml_config_manager import ValidationContext
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.config.implementations.yaml_config_manager import ValidationContext
# ... és még 1 import
```

## Osztály: `TestValidationContext`

ValidationContext osztály tesztjei.

### Metódusok

#### `test_initialization()`

```python
def test_initialization(self) -> None
```

Teszteli a ValidationContext inicializálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_initialization_with_none_value()`

```python
def test_initialization_with_none_value(self) -> None
```

Teszteli a ValidationContext inicializálását None értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestYAMLConfigManager`

YAMLConfigManager osztály tesztjei.

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

#### `sample_config()`

```python
def sample_config(self) -> dict[str, Any]
```

Minta konfiguráció.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `config_file()`

```python
def config_file(self, temp_dir: Path, sample_config: dict[str, Any]) -> Path
```

Minta konfigurációs fájl létrehozása.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)
- **`sample_config`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `Path`

#### `test_initialization_without_filename()`

```python
def test_initialization_without_filename(self) -> None
```

Teszteli a YAMLConfigManager inicializálását fájlnév nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_initialization_with_filename()`

```python
def test_initialization_with_filename(self, config_file: Path) -> None
```

Teszteli a YAMLConfigManager inicializálását fájlnévvel.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_current_schema_version()`

```python
def test_get_current_schema_version(self) -> None
```

Teszteli a jelenlegi séma verzió lekérdezését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_check_schema_compatibility()`

```python
def test_check_schema_compatibility(self) -> None
```

Teszteli a séma kompatibilitás ellenőrzését.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_ensure_dict_with_dict()`

```python
def test_ensure_dict_with_dict(self) -> None
```

Teszteli a _ensure_dict metódust dictionary értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_ensure_dict_with_none()`

```python
def test_ensure_dict_with_none(self) -> None
```

Teszteli a _ensure_dict metódust None értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_ensure_dict_with_invalid_type()`

```python
def test_ensure_dict_with_invalid_type(self) -> None
```

Teszteli a _ensure_dict metódust érvénytelen típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_existing_value()`

```python
def test_get_existing_value(self, config_file: Path) -> None
```

Teszteli az érték lekérdezését létező kulccsal.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_nonexistent_value_with_default()`

```python
def test_get_nonexistent_value_with_default(self, config_file: Path) -> None
```

Teszteli az érték lekérdezését nem létező kulccsal alapértelmezett értékkel.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_nonexistent_path()`

```python
def test_get_nonexistent_path(self, config_file: Path) -> None
```

Teszteli az érték lekérdezését nem létező útvonallal.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_section_existing()`

```python
def test_get_section_existing(self, config_file: Path) -> None
```

Teszteli a szekció lekérdezését létező szekcióval.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_section_nonexistent()`

```python
def test_get_section_nonexistent(self, config_file: Path) -> None
```

Teszteli a szekció lekérdezését nem létező szekcióval.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_single_key()`

```python
def test_set_single_key(self) -> None
```

Teszteli az érték beállítását egyetlen kulccsal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_set_nested_keys()`

```python
def test_set_nested_keys(self) -> None
```

Teszteli az érték beállítását beágyazott kulcsokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_set_without_keys()`

```python
def test_set_without_keys(self) -> None
```

Teszteli az érték beállítását kulcsok nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_set_overwriting_value()`

```python
def test_set_overwriting_value(self) -> None
```

Teszteli a meglévő érték felülírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_with_filename()`

```python
def test_save_with_filename(self, temp_dir: Path) -> None
```

Teszteli a konfiguráció mentését fájlnévvel.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_without_filename()`

```python
def test_save_without_filename(self) -> None
```

Teszteli a konfiguráció mentését fájlnév nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_with_manager_filename()`

```python
def test_save_with_manager_filename(self, temp_dir: Path) -> None
```

Teszteli a konfiguráció mentését a manager fájlnevével.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_existing_file()`

```python
def test_load_existing_file(self, config_file: Path) -> None
```

Teszteli a konfiguráció betöltését létező fájlból.

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_nonexistent_file()`

```python
def test_load_nonexistent_file(self, temp_dir: Path) -> None
```

Teszteli a konfiguráció betöltését nem létező fájlból.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_invalid_yaml()`

```python
def test_load_invalid_yaml(self, temp_dir: Path) -> None
```

Teszteli a konfiguráció betöltését érvénytelen YAML fájlból.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_with_schema_version()`

```python
def test_load_with_schema_version(self, temp_dir: Path) -> None
```

Teszteli a konfiguráció betöltését séma verzióval.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_valid_config()`

```python
def test_validate_valid_config(self) -> None
```

Teszteli a konfiguráció validálását érvényes konfiggal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_invalid_type()`

```python
def test_validate_invalid_type(self) -> None
```

Teszteli a konfiguráció validálását érvénytelen típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_missing_required()`

```python
def test_validate_missing_required(self) -> None
```

Teszteli a konfiguráció validálását hiányzó kötelező mezővel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_optional_field()`

```python
def test_validate_optional_field(self) -> None
```

Teszteli a konfiguráció validálását opcionális mezővel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_choices_valid()`

```python
def test_validate_choices_valid(self) -> None
```

Teszteli a choices validálását érvényes értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_choices_invalid()`

```python
def test_validate_choices_invalid(self) -> None
```

Teszteli a choices validálását érvénytelen értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_range_valid()`

```python
def test_validate_range_valid(self) -> None
```

Teszteli a range validálását érvényes értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_range_invalid_min()`

```python
def test_validate_range_invalid_min(self) -> None
```

Teszteli a range validálását érvénytelen minimum értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_range_invalid_max()`

```python
def test_validate_range_invalid_max(self) -> None
```

Teszteli a range validálását érvénytelen maximum értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_dict()`

```python
def test_validate_nested_dict(self) -> None
```

Teszteli a beágyazott dictionary validálását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_dict_invalid()`

```python
def test_validate_nested_dict_invalid(self) -> None
```

Teszteli a beágyazott dictionary validálását érvénytelen értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory()`

```python
def test_load_directory(self, temp_dir: Path) -> None
```

Teszteli a mappa betöltését.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_nonexistent()`

```python
def test_load_directory_nonexistent(self, temp_dir: Path) -> None
```

Teszteli a mappa betöltését nem létező mappából.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_not_a_directory()`

```python
def test_load_directory_not_a_directory(self, temp_dir: Path) -> None
```

Teszteli a mappa betöltését, ha az útvonal nem mappa.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_dict_with_non_dict_value()`

```python
def test_validate_dict_with_non_dict_value(self) -> None
```

Teszteli a _validate_dict metódust nem dictionary értékkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_unsupported_type()`

```python
def test_validate_unsupported_type(self) -> None
```

Teszteli a validálást nem támogatott típussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_creates_directory()`

```python
def test_save_creates_directory(self, temp_dir: Path) -> None
```

Teszteli, hogy a save létrehozza a könyvtárat, ha az nem létezik.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_save_error_handling()`

```python
def test_save_error_handling(self, temp_dir: Path) -> None
```

Teszteli a hibakezelést mentéskor.

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_with_logger_debug()`

```python
def test_get_with_logger_debug(self, config_file: Path) -> None
```

Teszteli a get metódust logger debug üzenettel (sor 123-130).

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_nested_creates_intermediate_dicts()`

```python
def test_set_nested_creates_intermediate_dicts(self) -> None
```

Teszteli, hogy a set létrehozza a köztes dictionary-ket (sor 169).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_with_incompatible_schema_version_warning()`

```python
def test_load_with_incompatible_schema_version_warning(self, temp_dir: Path) -> None
```

Teszteli a betöltést inkompatibilis séma verzióval (sor 228-234).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_dict_with_dict_value()`

```python
def test_validate_dict_with_dict_value(self) -> None
```

Teszteli a _validate_dict metódust dictionary értékkel (sor 264-265).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_type_with_none_value()`

```python
def test_validate_type_with_none_value(self) -> None
```

Teszteli a _validate_type metódust None értékkel (sor 316).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_dict_valid()`

```python
def test_validate_nested_dict_valid(self) -> None
```

Teszteli a _validate_nested metódust érvényes beágyazott dictionary-vel (sor 337-338).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_logs_debug_messages()`

```python
def test_load_directory_logs_debug_messages(self, temp_dir: Path) -> None
```

Teszteli a load_directory debug log üzeneteit (sor 414).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_system_yaml_special_handling()`

```python
def test_load_directory_system_yaml_special_handling(self, temp_dir: Path) -> None
```

Teszteli a system.yaml speciális kezelését (sor 430-431).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_without_logger_no_debug()`

```python
def test_get_without_logger_no_debug(self, config_file: Path) -> None
```

Teszteli a get metódust logger nélkül (sor 123).

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_creates_intermediate_dicts_edge_case()`

```python
def test_set_creates_intermediate_dicts_edge_case(self) -> None
```

Teszteli a set metódust, amikor a köztes dictionary-ket kell létrehozni (sor 169).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_dict_with_none_value()`

```python
def test_validate_dict_with_none_value(self) -> None
```

Teszteli a _validate_dict metódust None értékkel (sor 264-265).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_type_with_no_type_specified()`

```python
def test_validate_type_with_no_type_specified(self) -> None
```

Teszteli a _validate_type metódust, ha nincs típus megadva (sor 316).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_without_schema()`

```python
def test_validate_nested_without_schema(self) -> None
```

Teszteli a _validate_nested metódust, ha nincs schema megadva (sor 337-338).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_without_logger_no_debug()`

```python
def test_load_directory_without_logger_no_debug(self, temp_dir: Path) -> None
```

Teszteli a load_directory-t logger nélkül (sor 414).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_system_yaml_no_overwrite()`

```python
def test_load_directory_system_yaml_no_overwrite(self, temp_dir: Path) -> None
```

Teszteli, hogy a system.yaml nem írja felül a meglévő kulcsokat (sor 430-431).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_returns_default_when_current_not_dict()`

```python
def test_get_returns_default_when_current_not_dict(self, config_file: Path) -> None
```

Teszteli a get metódust, amikor a köztes érték nem dictionary (sor 123).

**Paraméterek:**

- **`self`**
- **`config_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_set_raises_error_when_intermediate_not_dict()`

```python
def test_set_raises_error_when_intermediate_not_dict(self) -> None
```

Teszteli a set metódust, amikor a köztes érték nem dictionary (sor 169).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_dict_with_non_dict_value_error_path()`

```python
def test_validate_dict_with_non_dict_value_error_path(self) -> None
```

Teszteli a _validate_dict hibautat nem dictionary értéknél (sor 264-265).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_with_non_dict_value_error_path()`

```python
def test_validate_nested_with_non_dict_value_error_path(self) -> None
```

Teszteli a _validate_nested hibautat nem dictionary értéknél (sor 337-338).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_directory_error_handling()`

```python
def test_load_directory_error_handling(self, temp_dir: Path) -> None
```

Teszteli a load_directory hibakezelését (sor 430-431).

**Paraméterek:**

- **`self`**
- **`temp_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_dict_with_non_dict_no_type_specified()`

```python
def test_validate_dict_with_non_dict_no_type_specified(self) -> None
```

Teszteli a _validate_dict-et, ha nincs type megadva (sor 264-265).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validate_nested_with_non_dict_no_type_specified()`

```python
def test_validate_nested_with_non_dict_no_type_specified(self) -> None
```

Teszteli a _validate_nested-et, ha nincs type megadva (sor 337-338).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/implementations/test_yaml_config_manager.py`](../../tests/neural_ai/core/config/implementations/test_yaml_config_manager.py)
