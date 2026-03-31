# Failed Tesztek Elemzése

**Dátum**: 2026-03-31  
**Összes failed teszt**: 49 db  
**Összes passed teszt**: 2343 db  
**Baseline**: Megoldás 2 (import cache tisztítás eltávolítva)

## Összefoglaló

A 49 failed teszt **NEM** az import cache interferencia miatt van, hanem egyéb okokból:
- Configuration hibák (hiányzó config mock)
- Pydantic migration hiányosságok (dict vs Pydantic model)
- Mock assertion hibák
- Hiányzó függőségek (asyncpg)
- Attribute access hibák

## Kategóriák Hiba Típus Szerint

### 1. Configuration Hibák (ConfigLoadError) - 43 előfordulás

**Hiba**: `ConfigLoadError: Fájl nem található: config.yaml`

**Érintett tesztek**: Főleg `test_sqlalchemy_session.py` és `test_core_init.py`

**Ok**: A tesztek nem mock-olják megfelelően a config fájl betöltést.

**Javasolt megoldás**: 
- Mock config manager használata
- Fixture létrehozása a config mock-oláshoz
- `monkeypatch` használata a config fájl elérési útvonalhoz

### 2. AttributeError - 32 előfordulás

**Hiba**: `AttributeError: 'dict' object has no attribute 'volume_confirmation'`

**Érintett tesztek**: `test_support_processor.py` (D02) - 16 teszt

**Ok**: A D02 processor config-ja dict-ként van kezelve, nem Pydantic modellként.

**Javasolt megoldás**:
- Pydantic model létrehozása a D02 config-hoz
- Config validáció hozzáadása
- Tesztek frissítése Pydantic model használatára

**Egyéb AttributeError**:
- `test_ui_factory.py`: `'UIServiceFactory' object has no attribute '_logger'` (2 teszt)
  - Ok: Private attribute (`_logger`) helyett public (`logger`) használata
  - Megoldás: Attribute név javítása a tesztekben

### 3. AssertionError - 34 előfordulás

**Érintett tesztek**:
- `test_core_init.py`: 7 teszt - Mock assertion hibák
- `test_events_factory.py`: 4 teszt - Mock config property access hibák
- `test_config_implementations_init.py`: 1 teszt - implementations/__init__.py nem üres
- `test_d01_factory.py`: 1 teszt
- `test_validation_end_to_end.py`: 1 teszt

**Ok**: 
- Mock beállítások nem megfelelőek
- Várt értékek nem egyeznek a mock visszatérési értékekkel
- Mock property access hibák (pl. `mock.EventBusConfig().pub_port`)

**Javasolt megoldás**:
- Mock beállítások javítása
- `return_value` és `side_effect` helyes használata
- Mock property access javítása (PropertyMock használata)

### 4. ModuleNotFoundError - 8 előfordulás

**Hiba**: `ModuleNotFoundError: No module named 'asyncpg'`

**Érintett tesztek**: `test_sqlalchemy_session.py` - PostgreSQL tesztek

**Ok**: Az `asyncpg` modul nincs telepítve (PostgreSQL async driver).

**Javasolt megoldás**:
- `asyncpg` hozzáadása a dev dependencies-hez
- VAGY: PostgreSQL tesztek skip-elése, ha asyncpg nincs telepítve
- VAGY: Mock használata az asyncpg helyett

### 5. TypeError - 4 előfordulás

**Hiba**: `TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union`

**Érintett tesztek**: `test_base_factory.py::test_logger_property_returns_logger`

**Ok**: Az `isinstance()` check-ben használt típus nem megfelelő (valószínűleg mock object).

**Javasolt megoldás**:
- Mock típus javítása
- `spec` paraméter használata a mock-nál
- Típus ellenőrzés javítása

### 6. ValidationError (Pydantic) - 4 előfordulás

**Hiba**: `pydantic_core._pydantic_core.ValidationError: 1 validation error for DatabaseConfig`

**Érintett tesztek**: `test_sqlalchemy_session.py::test_get_engine_with_pool_config`

**Ok**: Pydantic validációs hiba - hiányzó vagy érvénytelen config mező.

**Javasolt megoldás**:
- Config mock javítása
- Pydantic model validációs szabályok ellenőrzése
- Teszt input adatok javítása

## Fájlok Szerint Csoportosítva

### 1. test_support_processor.py (D02) - 16 failed ⚠️ PRIORITÁS #1

**Hibák**:
- `AttributeError: 'dict' object has no attribute 'volume_confirmation'` (16 teszt)

**Érintett tesztek**:
- `test_d02_processor_happy_path`
- `test_d02_processor_defaults`
- `TestD02ProcessorMissingConfigBranches::test_merge_levels_missing_level_merge_config`
- `TestD02ProcessorMissingConfigBranches::test_merge_levels_large_dataframe_skip_merge`
- `TestD02ProcessorMissingConfigBranches::test_confirm_with_volume_missing_config`
- `TestD02ProcessorMissingConfigBranches::test_confirm_with_volume_false`
- `TestD02ProcessorMissingConfigBranches::test_confirm_with_volume_true`
- `TestD02ProcessorNearestLevelsEdgeCases::test_nearest_support_no_candidates_below`
- `TestD02ProcessorNearestLevelsEdgeCases::test_nearest_resistance_no_candidates_above`
- `TestD02ProcessorMidColumnsHandling::test_process_with_bid_columns_no_mid`
- `TestD02ProcessorMidColumnsHandling::test_process_with_simple_ohlc_no_mid`
- `TestD02ProcessorMarketHoursFiltering::test_process_with_market_hours_enabled_filtering`
- `TestD02ProcessorMarketHoursFiltering::test_process_with_market_hours_outside_hours`
- `TestD02ProcessorNearestLevels::test_process_calculates_nearest_support`
- `TestD02ProcessorNearestLevels::test_process_calculates_nearest_resistance`
- `TestD02ProcessorEdgeCases::test_process_with_insufficient_data`

**Javasolt megoldás**:
```python
# Pydantic model létrehozása
from pydantic import BaseModel, Field

class D02Config(BaseModel):
    volume_confirmation: bool = Field(default=True)
    level_merge: dict = Field(default_factory=dict)
    # ... további mezők
```

**Érintett fájlok**:
- `neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`
- `tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py`

### 2. test_sqlalchemy_session.py - 16 failed ⚠️ PRIORITÁS #2

**Hibák**:
- `ConfigLoadError: Fájl nem található: config.yaml` (10 teszt)
- `ModuleNotFoundError: No module named 'asyncpg'` (4 teszt)
- `ValidationError: 1 validation error for DatabaseConfig` (1 teszt)
- `AssertionError: Regex pattern did not match` (1 teszt)

**Érintett tesztek**:
- `TestDatabaseURL::test_get_database_url_without_config`
- `TestCreateEngine::test_create_engine_postgresql`
- `TestCreateEngine::test_create_engine_postgresql_with_pool_config`
- `TestCreateEngine::test_create_engine_postgresql_with_none_pool_values`
- `TestGetEngine::test_get_engine_creates_on_first_call`
- `TestGetEngine::test_get_engine_caches_result`
- `TestGetEngine::test_get_engine_echo_fallback_exception`
- `TestGetEngine::test_get_engine_with_pool_config`
- `TestGetAsyncSessionMaker::test_get_async_session_maker_creates_once`
- `TestDatabaseManager::test_database_manager_initialize_with_pool_config`
- `TestContextManagers::test_get_db_session`
- `TestContextManagers::test_get_db_session_direct`
- `TestContextManagers::test_get_db_session_exception_rollback`
- `TestContextManagers::test_get_db_session_finally_block`
- `TestDatabaseInitialization::test_init_db`
- `TestDatabaseInitialization::test_close_db`

**Javasolt megoldás**:
1. Config mock fixture létrehozása
2. `asyncpg` hozzáadása a dependencies-hez VAGY PostgreSQL tesztek skip-elése
3. Pydantic DatabaseConfig validáció javítása

**Érintett fájlok**:
- `neural_ai/core/db/implementations/sqlalchemy_session.py`
- `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`
- `tests/conftest.py` (config mock fixture)

### 3. test_core_init.py - 7 failed ⚠️ PRIORITÁS #3

**Hibák**:
- `AssertionError: assert False` (4 teszt)
- `AssertionError: assert <MagicMock ...> is <MagicMock ...>` (2 teszt)
- `AssertionError: assert <MagicMock ...> == 'sqlite+aiosqlite:///:memory:'` (1 teszt)

**Érintett tesztek**:
- `TestBootstrapCore::test_bootstrap_core_success`
- `TestBootstrapCore::test_bootstrap_core_returns_core_components`
- `TestGetCoreComponents::test_get_core_components_first_call`
- `TestGetCoreComponents::test_get_core_components_returns_core_components`
- `TestIntegration::test_version_and_bootstrap_integration`
- `TestIntegration::test_core_components_singleton_pattern`
- `TestBootstrapCoreRealConfig::test_bootstrap_with_real_yaml_configs`

**Javasolt megoldás**:
- Mock beállítások javítása
- `return_value` helyes használata
- Mock singleton pattern javítása

**Érintett fájlok**:
- `neural_ai/core/__init__.py`
- `tests/neural_ai/core/test_core_init.py`

### 4. test_events_factory.py - 4 failed ⚠️ PRIORITÁS #4

**Hibák**:
- `AssertionError: assert <MagicMock name='mock.EventBusConfig().pub_port' ...> == 7777` (4 teszt)

**Érintett tesztek**:
- `TestEventBusFactoryCreateFromConfig::test_create_from_config_success`
- `TestEventBusFactoryCreateFromConfig::test_create_from_config_with_key_error`
- `TestEventBusFactoryCreateFromConfig::test_create_from_config_with_value_error`
- `TestEventBusFactoryCreateFromConfig::test_create_from_config_partial_config`

**Javasolt megoldás**:
- Mock property access javítása
- `PropertyMock` használata
- Mock config object helyes beállítása

**Érintett fájlok**:
- `neural_ai/core/events/factory.py`
- `tests/neural_ai/core/events/test_events_factory.py`

### 5. test_ui_factory.py - 2 failed ⚠️ PRIORITÁS #5

**Hibák**:
- `AttributeError: 'UIServiceFactory' object has no attribute '_logger'. Did you mean: 'logger'?` (2 teszt)

**Érintett tesztek**:
- `TestUIServiceFactoryInit::test_init_creates_instance`
- `TestUIServiceFactoryInitialize::test_initialize_with_dict_config`

**Javasolt megoldás**:
- Teszt javítása: `_logger` helyett `logger` használata
- VAGY: UIServiceFactory javítása: public `logger` property létrehozása

**Érintett fájlok**:
- `neural_ai/ui/factory.py`
- `tests/neural_ai/ui/test_ui_factory.py`

### 6. Egyéb (5 teszt) ⚠️ PRIORITÁS #6

#### test_base_factory.py - 1 failed
- **Hiba**: `TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union`
- **Teszt**: `TestCoreComponentFactory::test_logger_property_returns_logger`
- **Megoldás**: Mock típus javítása, `spec` paraméter használata

#### test_config_implementations_init.py - 1 failed
- **Hiba**: `AssertionError: Az implementations/__init__.py-nak üresnek kell lennie!`
- **Teszt**: `TestConfigImplementationsInit::test_module_is_empty`
- **Megoldás**: `neural_ai/core/config/implementations/__init__.py` kiürítése

#### test_d01_factory.py - 1 failed
- **Hiba**: `AssertionError: assert False`
- **Teszt**: `TestD01PriceFactory::test_factory_has_create_processor_method`
- **Megoldás**: Factory method implementálása vagy teszt javítása

#### test_validation_end_to_end.py - 1 failed
- **Hiba**: `Failed: Váratlan hiba a teszt futtatása közben: A validációs szkript nem jelezte a sikert`
- **Teszt**: `test_end_to_end_validation`
- **Megoldás**: Validációs szkript javítása vagy teszt javítása

## Javítási Prioritás

### 🔴 PRIORITÁS #1: D02 Support Processor (16 teszt)
**Probléma**: Dict helyett Pydantic model használata szükséges  
**Megoldás**: Pydantic model létrehozása + config validáció  
**Érintett fájlok**: 
- `neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`
- `tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py`

**Becsült idő**: 2-3 óra

### 🔴 PRIORITÁS #2: SQLAlchemy Session (16 teszt)
**Probléma**: Hiányzó config mock + asyncpg modul  
**Megoldás**: Config mock fixture + asyncpg telepítése/mock  
**Érintett fájlok**:
- `neural_ai/core/db/implementations/sqlalchemy_session.py`
- `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`
- `tests/conftest.py`

**Becsült idő**: 2-3 óra

### 🟡 PRIORITÁS #3: Core Init (7 teszt)
**Probléma**: Mock assertion hibák  
**Megoldás**: Mock beállítások javítása  
**Érintett fájlok**:
- `tests/neural_ai/core/test_core_init.py`

**Becsült idő**: 1-2 óra

### 🟡 PRIORITÁS #4: Events Factory (4 teszt)
**Probléma**: Mock property access hibák  
**Megoldás**: PropertyMock használata  
**Érintett fájlok**:
- `tests/neural_ai/core/events/test_events_factory.py`

**Becsült idő**: 1 óra

### 🟢 PRIORITÁS #5: UI Factory (2 teszt)
**Probléma**: Private vs public attribute  
**Megoldás**: Attribute név javítása  
**Érintett fájlok**:
- `tests/neural_ai/ui/test_ui_factory.py`

**Becsült idő**: 30 perc

### 🟢 PRIORITÁS #6: Egyéb (5 teszt)
**Probléma**: Különböző hibák  
**Megoldás**: Egyedi javítások  
**Érintett fájlok**: Különböző

**Becsült idő**: 2-3 óra

## Következő Lépés

**DELEGÁLÁS**: Code-Fix módra váltás a PRIORITÁS #1 javításához.

**Parancs**:
```
switch_mode: code-fix
Üzenet: "Code-Fix! Javítsd a D02 Support Processor config hibáját. 16 teszt bukik, mert a config dict-ként van kezelve, nem Pydantic modellként. AttributeError: 'dict' object has no attribute 'volume_confirmation'. Hozz létre Pydantic modellt a D02 config-hoz és frissítsd a teszteket."
```

## Összefoglalás

- **Baseline**: 49 failed, 2343 passed (Megoldás 2 - import cache tisztítás nélkül)
- **Fő probléma**: Pydantic migration hiányosságok + config mock hibák
- **Leggyakoribb hiba**: AttributeError (D02 processor) - 16 teszt
- **Második leggyakoribb**: ConfigLoadError (SQLAlchemy) - 16 teszt
- **Becsült teljes javítási idő**: 9-14 óra
- **Következő lépés**: D02 Support Processor javítása (PRIORITÁS #1)
