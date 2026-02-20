# tests/neural_ai/core/config/test_yaml_config_manager_validation.py

YAMLConfigManager típus validálás tesztek.

## Importok

```python
import pytest
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
```

## Osztály: `TestConfigManagerTypeValidation`

ConfigManager.get() típus validálás tesztek.

### Metódusok

#### `test_get_with_valid_string_keys()`

```python
def test_get_with_valid_string_keys(self)
```

Teszteljük, hogy string kulcsokkal működik.

**Paraméterek:**

- **`self`**

#### `test_get_with_single_key()`

```python
def test_get_with_single_key(self)
```

Teszteljük, hogy egyetlen kulccsal is működik.

**Paraméterek:**

- **`self`**

#### `test_get_with_nested_keys()`

```python
def test_get_with_nested_keys(self)
```

Teszteljük, hogy többszintű nested kulcsokkal működik.

**Paraméterek:**

- **`self`**

#### `test_get_with_invalid_dict_key_raises_type_error()`

```python
def test_get_with_invalid_dict_key_raises_type_error(self)
```

Teszteljük, hogy dict kulcs TypeError-t dob.

**Paraméterek:**

- **`self`**

#### `test_get_with_invalid_int_key_raises_type_error()`

```python
def test_get_with_invalid_int_key_raises_type_error(self)
```

Teszteljük, hogy int kulcs TypeError-t dob.

**Paraméterek:**

- **`self`**

#### `test_get_with_invalid_none_key_raises_type_error()`

```python
def test_get_with_invalid_none_key_raises_type_error(self)
```

Teszteljük, hogy None kulcs TypeError-t dob.

**Paraméterek:**

- **`self`**

#### `test_get_with_invalid_list_key_raises_type_error()`

```python
def test_get_with_invalid_list_key_raises_type_error(self)
```

Teszteljük, hogy list kulcs TypeError-t dob.

**Paraméterek:**

- **`self`**

#### `test_get_with_default_value()`

```python
def test_get_with_default_value(self)
```

Teszteljük, hogy a default paraméter működik.

**Paraméterek:**

- **`self`**

#### `test_get_nonexistent_key_returns_none()`

```python
def test_get_nonexistent_key_returns_none(self)
```

Teszteljük, hogy nem létező kulcs None-t ad vissza.

**Paraméterek:**

- **`self`**

#### `test_get_error_message_contains_helpful_info()`

```python
def test_get_error_message_contains_helpful_info(self)
```

Teszteljük, hogy a hibaüzenet tartalmaz hasznos információkat.

**Paraméterek:**

- **`self`**

#### `test_multiple_valid_string_keys()`

```python
def test_multiple_valid_string_keys(self)
```

Teszteljük, hogy több string kulccsal is működik.

**Paraméterek:**

- **`self`**

---

**Forrásfájl:** [`tests/neural_ai/core/config/test_yaml_config_manager_validation.py`](../../tests/neural_ai/core/config/test_yaml_config_manager_validation.py)
