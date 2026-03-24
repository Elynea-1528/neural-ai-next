# 🧪 Teszt: tests/neural_ai/core/config/test_config_factory.py

**Tesztelt modul:** [`neural_ai/core/config/config_factory.py`](../../neural_ai/core/config/config_factory.py)

Config Factory tesztmodul.

Ez a modul tartalmazza a konfigurációs factory teszteit,
ellenőrzi a megfelelő példányosítást és a hibakezelést.

## Teszt Osztály: `TestConfigManagerFactory`

ConfigManagerFactory osztály tesztjei.

### ✓ `test_get_manager_should_return_valid_interface()`

Teszteli, hogy a factory létrehoz egy érvényes konfigurációs interfészt.

### ✓ `test_get_manager_with_invalid_extension_should_raise_error()`

Teszteli, hogy érvénytelen kiterjesztés esetén hiba keletkezik.

### ✓ `test_get_async_manager_should_return_valid_interface()`

Teszteli, hogy a factory létrehoz egy érvényes aszinkron konfigurációs interfészt.

### ✓ `test_get_async_manager_should_be_created()`

Teszteli, hogy az aszinkron interfész létrejön.

### ✓ `test_get_manager_should_handle_yaml_extension()`

Teszteli, hogy a factory kezeli a YAML kiterjesztést.

### ✓ `test_get_manager_should_handle_yml_extension()`

Teszteli, hogy a factory kezeli a YML kiterjesztést.

### ✓ `test_get_manager_without_extension_should_use_default_yaml()`

Teszteli, hogy kiterjesztés nélküli fájlnál alapértelmezett YAML kezelőt használ.

### ✓ `test_create_manager_should_return_valid_interface()`

Teszteli, hogy a create_manager létrehoz egy érvényes konfigurációs interfészt.

### ✓ `test_create_manager_with_invalid_type_should_raise_error()`

Teszteli, hogy érvénytelen típus esetén hiba keletkezik.

### ✓ `test_get_async_manager_with_invalid_type_should_raise_error()`

Teszteli, hogy érvénytelen aszinkron típus esetén hiba keletkezik.

### ✓ `test_get_supported_extensions_should_return_list()`

Teszteli, hogy a támogatott kiterjesztések listája visszaadódik.

### ✓ `test_get_supported_async_types_should_return_list()`

Teszteli, hogy a támogatott aszinkron típusok listája visszaadódik.

### ✓ `test_register_manager_should_add_new_manager()`

Teszteli, hogy új kezelő regisztrálható.

### ✓ `test_get_async_manager_should_pass_session_and_logger()`

Teszteli, hogy az aszinkron kezelő megkapja a sessiont és loggert.

### ✓ `test_get_manager_should_create_separate_instances()`

Teszteli, hogy a factory külön példányokat hoz létre.

### ✓ `test_get_async_manager_should_handle_valid_kwargs()`

Teszteli, hogy az aszinkron kezelő kezeli a valid paramétereket.

### ✓ `test_register_async_manager_should_add_new_async_manager()`

Teszteli, hogy új aszinkron kezelő regisztrálható.

### ✓ `test_get_async_manager_without_session_should_raise_error()`

Teszteli, hogy session nélkül hiba keletkezik.

### ✓ `test_get_manager_with_explicit_type_should_use_that_type()`

Teszteli, hogy explicit típusmegadás esetén azt használja.

### ✓ `test_register_manager_should_normalize_extension()`

Teszteli, hogy a register_manager normalizálja a kiterjesztést (88. sor).

### ✓ `test_register_manager_should_validate_extension_not_empty()`

Teszteli, hogy a register_manager ellenőrzi az üres kiterjesztést (88. sor).

### ✓ `test_register_manager_should_validate_manager_is_type()`

Teszteli, hogy a register_manager ellenőrzi a típus érvényességét (91. sor).

### ✓ `test_register_async_manager_should_validate_manager_type_not_empty()`

Teszteli, hogy a register_async_manager ellenőrzi az üres típust (119. sor).

### ✓ `test_register_async_manager_should_validate_async_manager_is_type()`

Teszteli, hogy a register_async_manager ellenőrzi a típus érvényességét (125. sor).

### ✓ `test_get_manager_with_explicit_type_should_normalize_type()`

Teszteli, hogy a get_manager normalizálja az explicit típust (161. sor).

### ✓ `test_get_manager_with_explicit_type_should_handle_dot_prefix()`

Teszteli, hogy a get_manager kezeli a ponttal kezdődő explicit típust (161. sor).

### ✓ `test_get_manager_with_explicit_type_should_raise_error_for_invalid_type()`

Teszteli, hogy a get_manager hibát dob érvénytelen explicit típus esetén (161. sor).

---

**Teszt fájl:** [`tests/neural_ai/core/config/test_config_factory.py`](../../tests/neural_ai/core/config/test_config_factory.py)

**Tesztelt modul:** [`neural_ai/core/config/config_factory.py`](../../neural_ai/core/config/config_factory.py)
