# 🧪 Teszt: tests/neural_ai/core/config/implementations/test_yaml_config_manager.py

**Tesztelt modul:** [`neural_ai/core/config/implementations/yaml_config_manager.py`](../../neural_ai/core/config/implementations/yaml_config_manager.py)

YAMLConfigManager tesztek.

## Teszt Osztály: `TestValidationContext`

ValidationContext osztály tesztjei.

### ✓ `test_initialization()`

Teszteli a ValidationContext inicializálását.

### ✓ `test_initialization_with_none_value()`

Teszteli a ValidationContext inicializálását None értékkel.

## Teszt Osztály: `TestYAMLConfigManager`

YAMLConfigManager osztály tesztjei.

### ✓ `test_initialization_without_filename()`

Teszteli a YAMLConfigManager inicializálását fájlnév nélkül.

### ✓ `test_initialization_with_filename()`

Teszteli a YAMLConfigManager inicializálását fájlnévvel.

### ✓ `test_get_current_schema_version()`

Teszteli a jelenlegi séma verzió lekérdezését.

### ✓ `test_check_schema_compatibility()`

Teszteli a séma kompatibilitás ellenőrzését.

### ✓ `test_ensure_dict_with_dict()`

Teszteli a _ensure_dict metódust dictionary értékkel.

### ✓ `test_ensure_dict_with_none()`

Teszteli a _ensure_dict metódust None értékkel.

### ✓ `test_ensure_dict_with_invalid_type()`

Teszteli a _ensure_dict metódust érvénytelen típussal.

### ✓ `test_get_existing_value()`

Teszteli az érték lekérdezését létező kulccsal.

### ✓ `test_get_nonexistent_value_with_default()`

Teszteli az érték lekérdezését nem létező kulccsal alapértelmezett értékkel.

### ✓ `test_get_nonexistent_path()`

Teszteli az érték lekérdezését nem létező útvonallal.

### ✓ `test_get_section_existing()`

Teszteli a szekció lekérdezését létező szekcióval.

### ✓ `test_get_section_nonexistent()`

Teszteli a szekció lekérdezését nem létező szekcióval.

### ✓ `test_set_single_key()`

Teszteli az érték beállítását egyetlen kulccsal.

### ✓ `test_set_nested_keys()`

Teszteli az érték beállítását beágyazott kulcsokkal.

### ✓ `test_set_without_keys()`

Teszteli az érték beállítását kulcsok nélkül.

### ✓ `test_set_overwriting_value()`

Teszteli a meglévő érték felülírását.

### ✓ `test_save_with_filename()`

Teszteli a konfiguráció mentését fájlnévvel.

### ✓ `test_save_without_filename()`

Teszteli a konfiguráció mentését fájlnév nélkül.

### ✓ `test_save_with_manager_filename()`

Teszteli a konfiguráció mentését a manager fájlnevével.

### ✓ `test_load_existing_file()`

Teszteli a konfiguráció betöltését létező fájlból.

### ✓ `test_load_nonexistent_file()`

Teszteli a konfiguráció betöltését nem létező fájlból.

### ✓ `test_load_invalid_yaml()`

Teszteli a konfiguráció betöltését érvénytelen YAML fájlból.

### ✓ `test_load_with_schema_version()`

Teszteli a konfiguráció betöltését séma verzióval.

### ✓ `test_validate_valid_config()`

Teszteli a konfiguráció validálását érvényes konfiggal.

### ✓ `test_validate_invalid_type()`

Teszteli a konfiguráció validálását érvénytelen típussal.

### ✓ `test_validate_missing_required()`

Teszteli a konfiguráció validálását hiányzó kötelező mezővel.

### ✓ `test_validate_optional_field()`

Teszteli a konfiguráció validálását opcionális mezővel.

### ✓ `test_validate_choices_valid()`

Teszteli a choices validálását érvényes értékkel.

### ✓ `test_validate_choices_invalid()`

Teszteli a choices validálását érvénytelen értékkel.

### ✓ `test_validate_range_valid()`

Teszteli a range validálását érvényes értékkel.

### ✓ `test_validate_range_invalid_min()`

Teszteli a range validálását érvénytelen minimum értékkel.

### ✓ `test_validate_range_invalid_max()`

Teszteli a range validálását érvénytelen maximum értékkel.

### ✓ `test_validate_nested_dict()`

Teszteli a beágyazott dictionary validálását.

### ✓ `test_validate_nested_dict_invalid()`

Teszteli a beágyazott dictionary validálását érvénytelen értékkel.

### ✓ `test_load_directory()`

Teszteli a mappa betöltését.

### ✓ `test_load_directory_nonexistent()`

Teszteli a mappa betöltését nem létező mappából.

### ✓ `test_load_directory_not_a_directory()`

Teszteli a mappa betöltését, ha az útvonal nem mappa.

### ✓ `test_validate_dict_with_non_dict_value()`

Teszteli a _validate_dict metódust nem dictionary értékkel.

### ✓ `test_validate_unsupported_type()`

Teszteli a validálást nem támogatott típussal.

### ✓ `test_save_creates_directory()`

Teszteli, hogy a save létrehozza a könyvtárat, ha az nem létezik.

### ✓ `test_save_error_handling()`

Teszteli a hibakezelést mentéskor.

### ✓ `test_get_with_logger_debug()`

Teszteli a get metódust logger debug üzenettel (sor 123-130).

### ✓ `test_set_nested_creates_intermediate_dicts()`

Teszteli, hogy a set létrehozza a köztes dictionary-ket (sor 169).

### ✓ `test_load_with_incompatible_schema_version_warning()`

Teszteli a betöltést inkompatibilis séma verzióval (sor 228-234).

### ✓ `test_validate_dict_with_dict_value()`

Teszteli a _validate_dict metódust dictionary értékkel (sor 264-265).

### ✓ `test_validate_type_with_none_value()`

Teszteli a _validate_type metódust None értékkel (sor 316).

### ✓ `test_validate_nested_dict_valid()`

Teszteli a _validate_nested metódust érvényes beágyazott dictionary-vel (sor 337-338).

### ✓ `test_load_directory_logs_debug_messages()`

Teszteli a load_directory debug log üzeneteit (sor 414).

### ✓ `test_load_directory_system_yaml_special_handling()`

Teszteli a system.yaml speciális kezelését (sor 430-431).

### ✓ `test_get_without_logger_no_debug()`

Teszteli a get metódust logger nélkül (sor 123).

### ✓ `test_set_creates_intermediate_dicts_edge_case()`

Teszteli a set metódust, amikor a köztes dictionary-ket kell létrehozni (sor 169).

### ✓ `test_validate_dict_with_none_value()`

Teszteli a _validate_dict metódust None értékkel (sor 264-265).

### ✓ `test_validate_type_with_no_type_specified()`

Teszteli a _validate_type metódust, ha nincs típus megadva (sor 316).

### ✓ `test_validate_nested_without_schema()`

Teszteli a _validate_nested metódust, ha nincs schema megadva (sor 337-338).

### ✓ `test_load_directory_without_logger_no_debug()`

Teszteli a load_directory-t logger nélkül (sor 414).

### ✓ `test_load_directory_system_yaml_no_overwrite()`

Teszteli, hogy a system.yaml nem írja felül a meglévő kulcsokat (sor 430-431).

### ✓ `test_get_returns_default_when_current_not_dict()`

Teszteli a get metódust, amikor a köztes érték nem dictionary (sor 123).

### ✓ `test_set_raises_error_when_intermediate_not_dict()`

Teszteli a set metódust, amikor a köztes érték nem dictionary (sor 169).

### ✓ `test_validate_dict_with_non_dict_value_error_path()`

Teszteli a _validate_dict hibautat nem dictionary értéknél (sor 264-265).

### ✓ `test_validate_nested_with_non_dict_value_error_path()`

Teszteli a _validate_nested hibautat nem dictionary értéknél (sor 337-338).

### ✓ `test_load_directory_error_handling()`

Teszteli a load_directory hibakezelését (sor 430-431).

### ✓ `test_validate_dict_with_non_dict_no_type_specified()`

Teszteli a _validate_dict-et, ha nincs type megadva (sor 264-265).

### ✓ `test_validate_nested_with_non_dict_no_type_specified()`

Teszteli a _validate_nested-et, ha nincs type megadva (sor 337-338).

---

**Teszt fájl:** [`tests/neural_ai/core/config/implementations/test_yaml_config_manager.py`](../../tests/neural_ai/core/config/implementations/test_yaml_config_manager.py)

**Tesztelt modul:** [`neural_ai/core/config/implementations/yaml_config_manager.py`](../../neural_ai/core/config/implementations/yaml_config_manager.py)
