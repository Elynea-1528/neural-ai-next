# 🧪 Teszt: tests/neural_ai/core/test_core_init.py

**Tesztelt modul:** [`neural_ai/core/core_init.py`](../../neural_ai/core/core_init.py)

Tesztek a neural_ai.core.__init__.py modulhoz.

# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false
# Module import fixture type inference hibák.

Ez a tesztmodul ellenőrzi a core bootstrap funkcionalitását, beleértve:
- Verzió lekérdezést
- Séma verzió lekérdezést
- Core komponensek inicializálását
- Globális komponens hozzáférést

## Teszt Osztály: `TestVersionFunctions`

Tesztek a verzió lekérdező függvényekhez.

### ✓ `test_get_version_success()`

Teszteli a get_version függvényt sikeres verzió lekérdezés esetén.

### ✓ `test_get_version_failure()`

Teszteli a get_version függvényt sikertelen verzió lekérdezés esetén.

### ✓ `test_get_version_returns_string()`

Teszteli, hogy a get_version mindig stringgel tér vissza.

### ✓ `test_get_schema_version()`

Teszteli a get_schema_version függvényt.

### ✓ `test_get_schema_version_returns_string()`

Teszteli, hogy a get_schema_version mindig stringgel tér vissza.

## Teszt Osztály: `TestBootstrapCore`

Tesztek a bootstrap_core függvényhez.

### ✓ `test_bootstrap_core_success()`

Teszteli a bootstrap_core függvényt sikeres inicializálás esetén.

### ✓ `test_bootstrap_core_with_custom_config()`

Teszteli a bootstrap_core függvényt egyéni konfigurációval.

### ✓ `test_bootstrap_core_import_error()`

Teszteli a bootstrap_core függvényt import hiba esetén.

### ✓ `test_bootstrap_core_config_load_error()`

Teszteli a bootstrap_core függvényt config betöltési hiba esetén. Ez a teszt lefedi a 138-141 sorokat (ConfigLoadError exception handling).

### ✓ `test_bootstrap_core_returns_core_components()`

Teszteli, hogy a bootstrap_core CoreComponents példánnyal tér vissza.

### ✓ `test_bootstrap_core_with_jforex_enabled()`

Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezés esetén. Ez a teszt lefedi a 202. sort, ahol a JForex Live Feed opcionálisan inicializálódik.

### ✓ `test_bootstrap_core_with_jforex_disabled()`

Teszteli a bootstrap_core függvényt JForex Live Feed tiltás esetén.

## Teszt Osztály: `TestGetCoreComponents`

Tesztek a get_core_components függvényhez.

### ✓ `test_get_core_components_first_call()`

Teszteli a get_core_components függvényt első híváskor.

### ✓ `test_get_core_components_cached()`

Teszteli a get_core_components függvényt, ha már inicializálva van.

### ✓ `test_get_core_components_returns_core_components()`

Teszteli, hogy a get_core_components CoreComponents példánnyal tér vissza.

## Teszt Osztály: `TestIntegration`

Integrációs tesztek.

### ✓ `test_version_and_bootstrap_integration()`

Teszteli a verzió lekérdezés és a bootstrap integrációját.

### ✓ `test_all_imports_available()`

Teszteli, hogy minden publikus függvény elérhető-e a csomag szintjén.

### ✓ `test_core_components_singleton_pattern()`

Teszteli, hogy a CoreComponents singleton mintát követ-e.

## Teszt Osztály: `TestBootstrapCoreRealConfig`

Bootstrap valós config fájlokkal.

### ✓ `test_bootstrap_with_real_yaml_configs()`

Teljes bootstrap folyamat valós YAML config fájlokkal. Ez a teszt end-to-end ellenőrzi a config → parse → bootstrap láncot. NEM mockol semmit (kivéve hardver/külső rendszerek ha muszáj), valós fájlokból tölt be konfigurációt.

### ✓ `test_bootstrap_with_invalid_database_config_raises_error()`

Érvénytelen database.yaml ConfigValidationError-t dob.

## Teszt Osztály: `TestBootstrapCoreStorageError`

Tesztek a bootstrap_core storage hibakezelésére.

### ✓ `test_bootstrap_core_storage_init_failure()`

Teszteli a bootstrap_core függvényt storage inicializálási hiba esetén. Ez a teszt lefedi a 144-147 sorokat (storage exception handling).

## Teszt Osztály: `TestBootstrapCoreJForexLiveFeed`

Tesztek a bootstrap_core JForex Live Feed inicializálására.

### ✓ `test_bootstrap_core_jforex_live_feed_enabled()`

Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezve esetén. Ez a teszt lefedi a 200-202 sorokat (JForex live feed init).

---

**Teszt fájl:** [`tests/neural_ai/core/test_core_init.py`](../../tests/neural_ai/core/test_core_init.py)

**Tesztelt modul:** [`neural_ai/core/core_init.py`](../../neural_ai/core/core_init.py)
