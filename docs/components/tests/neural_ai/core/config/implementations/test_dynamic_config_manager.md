# 🧪 Teszt: tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py

**Tesztelt modul:** [`neural_ai/core/config/implementations/dynamic_config_manager.py`](../../neural_ai/core/config/implementations/dynamic_config_manager.py)

Tesztek a DynamicConfigManager osztályhoz.

## Teszt Osztály: `TestDynamicConfigManagerInit`

DynamicConfigManager inicializálásának tesztjei.

### ✓ `test_init_without_session_raises_value_error()`

Teszt: ValueError-t dob, ha nincs session megadva.

### ✓ `test_init_with_session_success()`

Teszt: Sikeres inicializálás sessionnel.

### ✓ `test_init_with_session_and_logger_success()`

Teszt: Sikeres inicializálás sessionnel és loggerrel.

## Teszt Osztály: `TestDynamicConfigManagerGet`

DynamicConfigManager get metódusának tesztjei.

### ✓ `test_get_with_multiple_keys_raises_value_error()`

Teszt: ValueError-t dob, ha több kulcsot adnak meg.

### ✓ `test_get_from_cache()`

Teszt: Érték lekérése a cache-ből.

### ✓ `test_get_from_database_success()`

Teszt: Érték lekérése az adatbázisból.

### ✓ `test_get_from_database_not_found_returns_default()`

Teszt: Alapértelmezett érték visszaadása, ha a kulcs nem található.

### ✓ `test_get_database_error_raises_config_error()`

Teszt: ConfigError-t dob adatbázis hiba esetén.

## Teszt Osztály: `TestDynamicConfigManagerSet`

DynamicConfigManager set metódusának tesztjei.

### ✓ `test_set_with_multiple_keys_raises_value_error()`

Teszt: ValueError-t dob, ha több kulcsot adnak meg.

### ✓ `test_set_new_config_success()`

Teszt: Új konfiguráció létrehozása.

### ✓ `test_set_existing_config_success()`

Teszt: Meglévő konfiguráció frissítése.

### ✓ `test_set_database_error_raises_config_error()`

Teszt: ConfigError-t dob adatbázis hiba esetén.

## Teszt Osztály: `TestDynamicConfigManagerGetSection`

DynamicConfigManager get_section metódusának tesztjei.

### ✓ `test_get_section_success()`

Teszt: Konfigurációs szekció lekérdezése.

### ✓ `test_get_section_not_found_raises_key_error()`

Teszt: KeyError-t dob, ha a szekció nem található.

### ✓ `test_get_section_database_error_raises_config_error()`

Teszt: ConfigError-t dob adatbázis hiba esetén.

## Teszt Osztály: `TestDynamicConfigManagerNotImplementedMethods`

Nem implementált metódusok tesztjei.

### ✓ `test_save_raises_not_implemented_error()`

Teszt: save metódus NotImplementedError-t dob.

### ✓ `test_load_raises_not_implemented_error()`

Teszt: load metódus NotImplementedError-t dob.

### ✓ `test_load_directory_raises_not_implemented_error()`

Teszt: load_directory metódus NotImplementedError-t dob.

## Teszt Osztály: `TestDynamicConfigManagerValidate`

DynamicConfigManager validate metódusának tesztjei.

### ✓ `test_validate_success()`

Teszt: Sikeres validáció.

### ✓ `test_validate_missing_required_field()`

Teszt: Validáció hiba, ha kötelező mező hiányzik.

### ✓ `test_validate_invalid_type()`

Teszt: Validáció hiba, ha az érték típusa nem megfelelő.

## Teszt Osztály: `TestDynamicConfigManagerListeners`

Listener metódusok tesztjei.

### ✓ `test_add_listener_success()`

Teszt: Listener hozzáadása.

### ✓ `test_remove_listener_success()`

Teszt: Listener eltávolítása.

### ✓ `test_remove_nonexistent_listener_no_error()`

Teszt: Nem létező listener eltávolítása nem okoz hibát.

## Teszt Osztály: `TestDynamicConfigManagerHotReload`

Hot reload metódusok tesztjei.

### ✓ `test_start_hot_reload_success()`

Teszt: Hot reload indítása.

### ✓ `test_start_hot_reload_when_already_running_raises_runtime_error()`

Teszt: RuntimeError-t dob, ha a hot reload már fut.

### ✓ `test_stop_hot_reload_success()`

Teszt: Hot reload leállítása.

### ✓ `test_stop_hot_reload_when_not_running_no_error()`

Teszt: Hot reload leállítása nem okoz hibát, ha nem fut.

## Teszt Osztály: `TestDynamicConfigManagerGetAll`

DynamicConfigManager get_all metódusának tesztjei.

### ✓ `test_get_all_success()`

Teszt: Összes konfiguráció lekérdezése.

### ✓ `test_get_all_with_category_filter()`

Teszt: Konfigurációk lekérdezése kategória szerint.

### ✓ `test_get_all_database_error_raises_config_error()`

Teszt: ConfigError-t dob adatbázis hiba esetén.

## Teszt Osztály: `TestDynamicConfigManagerSetWithMetadata`

DynamicConfigManager set_with_metadata metódusának tesztjei.

### ✓ `test_set_with_metadata_new_config_success()`

Teszt: Új konfiguráció létrehozása metaadatokkal.

### ✓ `test_set_with_metadata_existing_config_success()`

Teszt: Meglévő konfiguráció frissítése metaadatokkal.

## Teszt Osztály: `TestDynamicConfigManagerDelete`

DynamicConfigManager delete metódusának tesztjei.

### ✓ `test_delete_existing_config_success()`

Teszt: Konfiguráció törlése (soft delete).

### ✓ `test_delete_nonexistent_config_returns_false()`

Teszt: False visszaadása, ha a konfiguráció nem található.

### ✓ `test_delete_database_error_raises_config_error()`

Teszt: ConfigError-t dob adatbázis hiba esetén.

## Teszt Osztály: `CustomType`

## Teszt Osztály: `TestDynamicConfigManagerDetermineValueType`

_determine_value_type metódus tesztjei.

### ✓ `test_determine_value_type_bool()`

Teszt: Boolean típus felismerése.

### ✓ `test_determine_value_type_int()`

Teszt: Integer típus felismerése.

### ✓ `test_determine_value_type_float()`

Teszt: Float típus felismerése.

### ✓ `test_determine_value_type_str()`

Teszt: String típus felismerése.

### ✓ `test_determine_value_type_list()`

Teszt: List típus felismerése.

### ✓ `test_determine_value_type_dict()`

Teszt: Dict típus felismerése.

### ✓ `test_determine_value_type_unknown_defaults_to_str()`

Teszt: Ismeretlen típus esetén str visszaadása.

## Teszt Osztály: `TestDynamicConfigManagerNotifyListeners`

_notify_listeners metódus tesztjei.

### ✓ `test_notify_listeners_success()`

Teszt: Listener-ek értesítése.

### ✓ `test_listener()`

### ✓ `test_notify_listeners_with_exception_in_listener()`

Teszt: Listener hiba esetén a többi listener még mindig hívódik.

## Teszt Osztály: `TestDynamicConfigManagerCheckForUpdates`

_check_for_updates metódus tesztjei.

### ✓ `test_check_for_updates_first_time_loads_all()`

Teszt: Első alkalommal betölti az összes konfigurációt.

### ✓ `test_check_for_updates_with_changes()`

Teszt: Változások észlelése és cache frissítése.

### ✓ `test_listener()`

### ✓ `test_check_for_updates_database_error_logged()`

Teszt: Adatbázis hiba esetén a hiba naplózásra kerül.

---

**Teszt fájl:** [`tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py`](../../tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py)

**Tesztelt modul:** [`neural_ai/core/config/implementations/dynamic_config_manager.py`](../../neural_ai/core/config/implementations/dynamic_config_manager.py)
