# Maradék 36 Failed Teszt Elemzése

**Dátum**: 2026-03-31  
**Haladás**: 41/49 javítva (84%) → **KORREKCIÓ: 36 failed teszt maradt**  
**Eredeti**: 49 failed teszt  
**D02 javítás**: 17 teszt javítva (BaseDimensionProcessor Pydantic migráció)  
**D01 javítás**: 24 teszt javítva (`.get()` → attribute access)  
**Maradt**: **36 failed teszt**

## 📊 Összefoglaló

A BaseDimensionProcessor Pydantic migrációja és a D01 `.get()` → attribute access javítás után **36 failed teszt** maradt. A pytest summary:

```
===== 36 failed, 2356 passed, 14 skipped, 14 warnings in 671.50s (0:11:11) =====
```

## 🗂️ Kategóriák

### 🔴 KATEGÓRIA #1: Mock Property Access Hibák (11 teszt)

**Probléma**: Mock objektumok property access-e nem működik megfelelően a Pydantic migrációval.

#### Events Factory (4 teszt)

**Érintett tesztek**:
- [`test_create_from_config_success`](tests/neural_ai/core/events/test_events_factory.py:1)
- [`test_create_from_config_with_key_error`](tests/neural_ai/core/events/test_events_factory.py:1)
- [`test_create_from_config_with_value_error`](tests/neural_ai/core/events/test_events_factory.py:1)
- [`test_create_from_config_partial_config`](tests/neural_ai/core/events/test_events_factory.py:1)

**Hiba típusa**: AssertionError

**Hiba üzenet**:
```python
AssertionError: assert <MagicMock name='mock.EventBusConfig().pub_port' id='...'> == 7777
 +  where <MagicMock name='mock.EventBusConfig().pub_port' id='...'> = <MagicMock name='mock.EventBusConfig()' id='...'>.pub_port
```

**Root Cause**: A mock objektum `.pub_port` property-je nem ad vissza értéket, hanem egy újabb MagicMock-ot. A Pydantic modell attribute access-e nem működik a mock-kal.

**Javasolt megoldás**: 
1. Mock `return_value` beállítása Pydantic modellre
2. Vagy `mock.EventBusConfig.return_value.pub_port = 7777` explicit beállítás

**Becsült idő**: 15 perc

---

#### Core Init (7 teszt)

**Érintett tesztek**:
- [`test_bootstrap_core_success`](tests/neural_ai/core/test_core_init.py:1)
- [`test_bootstrap_core_returns_core_components`](tests/neural_ai/core/test_core_init.py:1)
- [`test_get_core_components_first_call`](tests/neural_ai/core/test_core_init.py:1)
- [`test_get_core_components_returns_core_components`](tests/neural_ai/core/test_core_init.py:1)
- [`test_version_and_bootstrap_integration`](tests/neural_ai/core/test_core_init.py:1)
- [`test_core_components_singleton_pattern`](tests/neural_ai/core/test_core_init.py:1)
- [`test_bootstrap_with_real_yaml_configs`](tests/neural_ai/core/test_core_init.py:1)

**Hiba típusa**: AssertionError

**Hiba üzenet**:
```python
AssertionError: assert <MagicMock name='mock.logger' id='...'> == <MagicMock name='mock.logger' id='...'>
```

**Root Cause**: A mock objektum `.logger` property-je nem egyezik meg az elvárt mock-kal. A CoreComponents Pydantic modell attribute access-e nem működik a mock-kal.

**Javasolt megoldás**: 
1. Mock `return_value` beállítása Pydantic modellre
2. Vagy explicit mock property beállítás

**Becsült idő**: 20 perc

---

### 🔴 KATEGÓRIA #2: SQLAlchemy Session - ConfigLoadError (10 teszt)

**Probléma**: Hiányzó `config.yaml` mock a tesztekben.

**Érintett tesztek**:
- [`test_get_database_url_without_config`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_engine_creates_on_first_call`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_engine_caches_result`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_engine_echo_fallback_exception`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_async_session_maker_creates_once`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_db_session`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_db_session_direct`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_db_session_finally_block`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_init_db`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_get_db_session_exception_rollback`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1) (részben)

**Hiba típusa**: ConfigLoadError

**Hiba üzenet**:
```
neural_ai.core.config.exceptions.config_error.ConfigLoadError: Fájl nem található: config.yaml
```

**Root Cause**: A tesztek nem mock-olják a config betöltést, így a valódi fájlrendszert próbálják elérni.

**Javasolt megoldás**: 
1. Mock `ConfigManager.get()` metódust
2. Vagy fixture-rel biztosítani a config mock-ot

**Becsült idő**: 30 perc

---

### 🟡 KATEGÓRIA #3: SQLAlchemy Session - asyncpg hiányzik (4 teszt)

**Probléma**: A `asyncpg` modul nincs telepítve a környezetben.

**Érintett tesztek**:
- [`test_create_engine_postgresql`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_create_engine_postgresql_with_pool_config`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_create_engine_postgresql_with_none_pool_values`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)
- [`test_database_manager_initialize_with_pool_config`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)

**Hiba típusa**: ModuleNotFoundError

**Hiba üzenet**:
```
ModuleNotFoundError: No module named 'asyncpg'
```

**Root Cause**: A PostgreSQL async driver (`asyncpg`) nincs telepítve.

**Javasolt megoldás**: 
1. Telepíteni az `asyncpg` modult: `pip install asyncpg`
2. Vagy mock-olni az import-ot a tesztekben

**Becsült idő**: 5 perc (telepítés) vagy 15 perc (mock)

---

### 🟡 KATEGÓRIA #4: SQLAlchemy Session - Egyéb (2 teszt)

#### Pydantic ValidationError (1 teszt)

**Érintett teszt**:
- [`test_get_engine_with_pool_config`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)

**Hiba típusa**: ValidationError

**Hiba üzenet**:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for DatabaseConfig
connection
  Field required [type=missing, input_value={'pool': {'size': 15, 'recycle': 2400}}, input_type=dict]
```

**Root Cause**: A teszt nem adja meg a kötelező `connection` mezőt a DatabaseConfig-nak.

**Javasolt megoldás**: 
1. Teszt javítása: `connection` mező hozzáadása a mock config-hoz

**Becsült idő**: 5 perc

---

#### Mock Assertion (1 teszt)

**Érintett teszt**:
- [`test_close_db`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)

**Hiba típusa**: AssertionError

**Hiba üzenet**:
```
AssertionError: Expected 'dispose' to have been called once. Called 0 times.
```

**Root Cause**: A `dispose` metódus nem lett meghívva, mert a teszt előfeltételei nem teljesültek (ConfigLoadError miatt).

**Javasolt megoldás**: 
1. Config mock javítása (KATEGÓRIA #2 megoldása után automatikusan javul)

**Becsült idő**: 0 perc (automatikus javulás)

---

### 🟡 KATEGÓRIA #5: Config Implementations Init (1 teszt)

**Érintett teszt**:
- [`test_module_is_empty`](tests/neural_ai/core/config/implementations/test_config_implementations_init.py:1)

**Hiba típusa**: AssertionError

**Hiba üzenet**:
```
AssertionError: Az implementations/__init__.py-nak üresnek kell lennie! Talált attribútumok: ['dynamic_config_manager', 'yaml_config_manager']
assert 2 == 0
 +  where 2 = len(['dynamic_config_manager', 'yaml_config_manager'])
```

**Root Cause**: A [`neural_ai/core/config/implementations/__init__.py`](neural_ai/core/config/implementations/__init__.py:1) fájl nem üres, pedig a DDD szabvány szerint üresnek kellene lennie.

**Javasolt megoldás**: 
1. Törölni az exportokat a [`neural_ai/core/config/implementations/__init__.py`](neural_ai/core/config/implementations/__init__.py:1) fájlból
2. Vagy a tesztet módosítani, ha az export szándékos

**Becsült idő**: 5 perc

---

### 🟡 KATEGÓRIA #6: Base Factory (1 teszt)

**Érintett teszt**:
- [`test_logger_property_returns_logger`](tests/neural_ai/core/base/test_base_factory.py:1)

**Hiba típusa**: TypeError

**Hiba üzenet**:
```
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

**Root Cause**: Az `isinstance()` hívás második paramétere nem megfelelő típus. Valószínűleg egy mock objektum vagy string.

**Javasolt megoldás**: 
1. Ellenőrizni a teszt kódját, hogy mi a második paraméter
2. Javítani a mock beállítást

**Becsült idő**: 10 perc

---

### 🟡 KATEGÓRIA #7: D01 Factory (1 teszt)

**Érintett teszt**:
- [`test_factory_has_create_processor_method`](tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py:1)

**Hiba típusa**: AttributeError

**Hiba üzenet**:
```
AttributeError: type object 'D01PriceFactory' has no attribute 'create_processor'
```

**Root Cause**: A [`D01PriceFactory`](neural_ai/processors/dimensions/d01_price/factory.py:1) osztálynak nincs `create_processor` metódusa.

**Javasolt megoldás**: 
1. Hozzáadni a `create_processor` metódust a factory-hoz
2. Vagy a tesztet javítani, ha a metódus neve megváltozott

**Becsült idő**: 10 perc

---

### 🟡 KATEGÓRIA #8: Dimensions Base (3 teszt)

**Érintett tesztek**:
- [`test_concrete_implementation_can_be_instantiated`](tests/neural_ai/processors/dimensions/test_dimensions_base.py:1)
- [`test_initialization_loads_config`](tests/neural_ai/processors/dimensions/test_dimensions_base.py:1)
- [`test_initialization_with_missing_config`](tests/neural_ai/processors/dimensions/test_dimensions_base.py:1)

**Hiba típusa**: AssertionError

**Hiba üzenet**:
```
AssertionError: ProcessorConfig(required_timeframes=None, z_score_window=None, ...) == {}

Full diff:
- {}
+ ProcessorConfig(required_timeframes=None, z_score_window=None, ...)
```

**Root Cause**: A teszt azt várja, hogy a config egy üres dict `{}`, de a Pydantic migráció után egy `ProcessorConfig` objektum lett.

**Javasolt megoldás**: 
1. Tesztek javítása: `assert isinstance(processor.config, ProcessorConfig)`
2. Vagy `assert processor.config == ProcessorConfig()` (default értékekkel)

**Becsült idő**: 15 perc

---

### 🟡 KATEGÓRIA #9: UI Factory (2 teszt)

**Érintett tesztek**:
- [`test_init_creates_instance`](tests/neural_ai/ui/test_ui_factory.py:1)
- [`test_initialize_with_dict_config`](tests/neural_ai/ui/test_ui_factory.py:1)

**Hiba típusa**: AttributeError

**Hiba üzenet**:
```
AttributeError: 'UIServiceFactory' object has no attribute '_logger'. Did you mean: 'logger'?
```

**Root Cause**: A teszt a `_logger` private attribútumot keresi, de az osztály `logger` publikus attribútumot használ.

**Javasolt megoldás**: 
1. Tesztek javítása: `_logger` → `logger`
2. Vagy az osztály javítása, ha a `_logger` a helyes

**Becsült idő**: 5 perc

---

### 🟢 KATEGÓRIA #10: Validation E2E (1 teszt)

**Érintett teszt**:
- [`test_end_to_end_validation`](tests/scripts/test_validation_end_to_end.py:1)

**Hiba típusa**: Failed

**Hiba üzenet**:
```
Failed: Váratlan hiba a teszt futtatása közben: A validációs szkript nem jelezte a sikert
```

**Root Cause**: A validációs szkript nem találta meg a "🎉 END-TO-END VALIDÁCIÓ SIKERES!" üzenetet a kimenetben. A kimenetben látható, hogy az adatok validálása sikertelen volt ("❌ Nincs elérhető adat").

**Javasolt megoldás**: 
1. Ellenőrizni, hogy az adatok letöltése sikeres volt-e
2. Javítani a validációs szkriptet vagy a tesztet

**Becsült idő**: 20 perc

---

## 🎯 Javítási Prioritás

### 🔴 PRIORITÁS #1: Mock Property Access Hibák (11 teszt)

**Probléma**: Mock objektumok property access-e nem működik a Pydantic migrációval.

**Megoldás**: Mock `return_value` beállítása Pydantic modellekre.

**Érintett fájlok**:
- [`tests/neural_ai/core/events/test_events_factory.py`](tests/neural_ai/core/events/test_events_factory.py:1)
- [`tests/neural_ai/core/test_core_init.py`](tests/neural_ai/core/test_core_init.py:1)

**Becsült idő**: 35 perc

---

### 🔴 PRIORITÁS #2: SQLAlchemy Session - ConfigLoadError (10 teszt)

**Probléma**: Hiányzó config mock a tesztekben.

**Megoldás**: Mock `ConfigManager.get()` metódust vagy fixture-rel biztosítani a config mock-ot.

**Érintett fájlok**:
- [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)

**Becsült idő**: 30 perc

---

### 🟡 PRIORITÁS #3: SQLAlchemy Session - asyncpg hiányzik (4 teszt)

**Probléma**: A `asyncpg` modul nincs telepítve.

**Megoldás**: Telepíteni az `asyncpg` modult vagy mock-olni az import-ot.

**Érintett fájlok**:
- [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py:1)

**Becsült idő**: 5 perc (telepítés) vagy 15 perc (mock)

---

### 🟡 PRIORITÁS #4: Dimensions Base (3 teszt)

**Probléma**: Teszt azt várja, hogy a config egy üres dict, de Pydantic objektum lett.

**Megoldás**: Tesztek javítása Pydantic objektum ellenőrzésre.

**Érintett fájlok**:
- [`tests/neural_ai/processors/dimensions/test_dimensions_base.py`](tests/neural_ai/processors/dimensions/test_dimensions_base.py:1)

**Becsült idő**: 15 perc

---

### 🟡 PRIORITÁS #5: Egyéb Hibák (8 teszt)

**Problémák**:
- Config Implementations Init (1 teszt) - 5 perc
- Base Factory (1 teszt) - 10 perc
- D01 Factory (1 teszt) - 10 perc
- UI Factory (2 teszt) - 5 perc
- SQLAlchemy Session - Egyéb (2 teszt) - 5 perc
- Validation E2E (1 teszt) - 20 perc

**Becsült idő**: 55 perc

---

## 📈 Összefoglalás

- **Baseline**: 36 failed teszt (49-ből 41 javítva korábban, de valójában 36 maradt)
- **Fő probléma**: Mock property access hibák (11 teszt) és ConfigLoadError (10 teszt)
- **Becsült teljes javítási idő**: ~2.5 óra
- **Következő lépés**: PRIORITÁS #1 javítása (Mock Property Access)

---

## 🚀 Következő Parancs

**DELEGÁLÁS**: Code-Fix módra váltás a PRIORITÁS #1 javításához.

**Parancs**:
```
Code-Fix! Javítsd a Mock Property Access hibákat (11 teszt). 

Probléma: A Pydantic migrációval a mock objektumok property access-e nem működik. A mock.EventBusConfig().pub_port és mock.logger property-k MagicMock objektumokat adnak vissza értékek helyett.

Érintett fájlok:
- tests/neural_ai/core/events/test_events_factory.py (4 teszt)
- tests/neural_ai/core/test_core_init.py (7 teszt)

Megoldás: Mock return_value beállítása Pydantic modellekre vagy explicit property beállítás.

Példa:
mock_config = MagicMock()
mock_config.pub_port = 7777
mock_config.sub_port = 7778
mock.EventBusConfig.return_value = mock_config
```
