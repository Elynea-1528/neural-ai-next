# Tesztdokumentáció: `tests/core/config/test_config_exceptions.py`

## Áttekintés

Ez a dokumentáció a [`tests/core/config/test_config_exceptions.py`](tests/core/config/test_config_exceptions.py) tesztmodult ismerteti, amely a `neural_ai.core.config.exceptions` modulban található összes kivétel osztályt teszteli.

## Tesztelt Komponensek

A tesztmodul a következő kivétel osztályokat ellenőrzi:

- [`ConfigError`](../../neural_ai/core/config/exceptions/config_error.md) - Alap konfigurációs hiba
- [`ConfigLoadError`](../../neural_ai/core/config/exceptions/config_error.md) - Konfiguráció betöltési hiba
- [`ConfigSaveError`](../../neural_ai/core/config/exceptions/config_error.md) - Konfiguráció mentési hiba
- [`ConfigValidationError`](../../neural_ai/core/config/exceptions/config_error.md) - Konfiguráció validációs hiba
- [`ConfigTypeError`](../../neural_ai/core/config/exceptions/config_error.md) - Konfiguráció típus hiba
- [`ConfigKeyError`](../../neural_ai/core/config/exceptions/config_error.md) - Konfiguráció kulcs hiba

## Tesztosztályok

### 1. `TestConfigError`

Az alap `ConfigError` osztály tesztjei:

- **`test_config_error_basic_initialization`**: Ellenőrzi az alap inicializálást hibaüzenettel
- **`test_config_error_with_error_code`**: Ellenőrzi a hibakóddal történő inicializálást
- **`test_config_error_is_exception`**: Ellenőrzi az `Exception` osztályból való öröklődést

### 2. `TestConfigLoadError`

A `ConfigLoadError` osztály tesztjei:

- **`test_config_load_error_basic_initialization`**: Ellenőrzi az alap inicializálást
- **`test_config_load_error_with_file_path`**: Ellenőrzi a fájlúttal történő inicializálást
- **`test_config_load_error_with_original_error`**: Ellenőrzi az eredeti hibával történő inicializálást
- **`test_config_load_error_inheritance`**: Ellenőrzi az öröklődési láncolatot

### 3. `TestConfigSaveError`

A `ConfigSaveError` osztály tesztjei:

- **`test_config_save_error_basic_initialization`**: Ellenőrzi az alap inicializálást
- **`test_config_save_error_with_file_path`**: Ellenőrzi a fájlúttal történő inicializálást
- **`test_config_save_error_with_original_error`**: Ellenőrzi az eredeti hibával történő inicializálást
- **`test_config_save_error_inheritance`**: Ellenőrzi az öröklődési láncolatot

### 4. `TestConfigValidationError`

A `ConfigValidationError` osztály tesztjei:

- **`test_config_validation_error_basic_initialization`**: Ellenőrzi az alap inicializálást
- **`test_config_validation_error_with_field_path`**: Ellenőrzi a mezőúttal történő inicializálást
- **`test_config_validation_error_with_invalid_value`**: Ellenőrzi az érvénytelen értékkel történő inicializálást
- **`test_config_validation_error_inheritance`**: Ellenőrzi az öröklődési láncolatot

### 5. `TestConfigTypeError`

A `ConfigTypeError` osztály tesztjei:

- **`test_config_type_error_basic_initialization`**: Ellenőrzi az alap inicializálást
- **`test_config_type_error_with_field_path`**: Ellenőrzi a mezőúttal történő inicializálást
- **`test_config_type_error_with_types`**: Ellenőrzi a típusokkal történő inicializálást
- **`test_config_type_error_complete_initialization`**: Ellenőrzi a teljes inicializálást
- **`test_config_type_error_inheritance`**: Ellenőrzi az öröklődési láncolatot

### 6. `TestConfigKeyError`

A `ConfigKeyError` osztály tesztjei:

- **`test_config_key_error_basic_initialization`**: Ellenőrzi az alap inicializálást
- **`test_config_key_error_with_key_path`**: Ellenőrzi a kulcsúttal történő inicializálást
- **`test_config_key_error_with_available_keys`**: Ellenőrzi az elérhető kulcsokkal történő inicializálást
- **`test_config_key_error_complete_initialization`**: Ellenőrzi a teljes inicializálást
- **`test_config_key_error_inheritance`**: Ellenőrzi az öröklődési láncolatot

### 7. `TestExceptionHierarchy`

A kivétel hierarchia tesztjei:

- **`test_exception_hierarchy_structure`**: Ellenőrzi a kivétel hierarchia szerkezetét

### 8. `TestExceptionUsage`

A kivételek használatának tesztjei:

- **`test_raise_and_catch_specific_error`**: Teszteli a specifikus kivétel dobását és elkapását
- **`test_raise_and_catch_base_error`**: Teszteli az alap kivétel dobását és elkapását
- **`test_exception_chaining`**: Teszteli a kivétel láncolatot

## Tesztlefedettség

A tesztmodul **100%-os** utasítási és ág-lefedettséget biztosít a kivétel osztályok számára.

### Metrikák

- **Utasítási lefedettség (Statement Coverage)**: 100%
- **Ág-lefedettség (Branch Coverage)**: 100%
- **Összes teszteset**: 29
- **Sikeres tesztesetek**: 29
- **Sikertelen tesztesetek**: 0

## Futtatás

A teszteket a következő paranccsal lehet futtatni:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/test_config_exceptions.py -v
```

## Kimenet

A tesztfuttatás sikeres kimenete:

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /home/elynea/Dokumentumok/neural-ai-next
configfile: pyproject.toml
plugins: anyio-4.12.0, asyncio-1.3.0, cov-7.0.0
collected 29 items

tests/core/config/test_config_exceptions.py::TestConfigError::test_config_error_basic_initialization PASSED
tests/core/config/test_config_exceptions.py::TestConfigError::test_config_error_with_error_code PASSED
tests/core/config/test_config_exceptions.py::TestConfigError::test_config_error_is_exception PASSED
...
tests/core/config/test_config_exceptions.py::TestExceptionUsage::test_exception_chaining PASSED

============================== 29 passed in 0.11s ==============================
```

## Stabilitás

A tesztmodul **stabil** és **megbízható**. Minden teszteset konzisztensen sikeres, és nincs ismert hiba vagy instabilitás.

## Kapcsolódó Dokumentáció

- [Konfigurációs Kivételek](../../neural_ai/core/config/exceptions/config_error.md)
- [Konfigurációs Rendszer Architektúra](../../neural_ai/core/config/__init__.md)
- [Tesztelési Irányelvek](../../../development/architecture_standards.md)