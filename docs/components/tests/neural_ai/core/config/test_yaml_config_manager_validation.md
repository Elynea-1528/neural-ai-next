# 🧪 Teszt: tests/neural_ai/core/config/test_yaml_config_manager_validation.py

**Tesztelt modul:** [`neural_ai/core/config/yaml_config_manager_validation.py`](../../neural_ai/core/config/yaml_config_manager_validation.py)

YAMLConfigManager típus validálás tesztek.

## Teszt Osztály: `TestConfigManagerTypeValidation`

ConfigManager.get() típus validálás tesztek.

### ✓ `test_get_with_valid_string_keys()`

Teszteljük, hogy string kulcsokkal működik.

### ✓ `test_get_with_single_key()`

Teszteljük, hogy egyetlen kulccsal is működik.

### ✓ `test_get_with_nested_keys()`

Teszteljük, hogy többszintű nested kulcsokkal működik.

### ✓ `test_get_with_invalid_dict_key_raises_type_error()`

Teszteljük, hogy dict kulcs TypeError-t dob.

### ✓ `test_get_with_invalid_int_key_raises_type_error()`

Teszteljük, hogy int kulcs TypeError-t dob.

### ✓ `test_get_with_invalid_none_key_raises_type_error()`

Teszteljük, hogy None kulcs TypeError-t dob.

### ✓ `test_get_with_invalid_list_key_raises_type_error()`

Teszteljük, hogy list kulcs TypeError-t dob.

### ✓ `test_get_with_default_value()`

Teszteljük, hogy a default paraméter működik.

### ✓ `test_get_nonexistent_key_returns_none()`

Teszteljük, hogy nem létező kulcs None-t ad vissza.

### ✓ `test_get_error_message_contains_helpful_info()`

Teszteljük, hogy a hibaüzenet tartalmaz hasznos információkat.

### ✓ `test_multiple_valid_string_keys()`

Teszteljük, hogy több string kulccsal is működik.

---

**Teszt fájl:** [`tests/neural_ai/core/config/test_yaml_config_manager_validation.py`](../../tests/neural_ai/core/config/test_yaml_config_manager_validation.py)

**Tesztelt modul:** [`neural_ai/core/config/yaml_config_manager_validation.py`](../../neural_ai/core/config/yaml_config_manager_validation.py)
