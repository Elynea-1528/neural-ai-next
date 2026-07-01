# 🔄 Debug-Complex Delegálási Parancs

**FROM:** QA Mode (Validation Complete)  
**TO:** Debug-Complex Mode (Root Cause Fix)  
**DATE:** 2026-07-01 19:40 UTC+2  
**STATUS:** 🔴 CRITICAL - Test Isolation Failure

---

## 📋 Mission Brief

**51 failed test** a mock assertion refactoring után. **QA scope kész**, de **session lifecycle + mock strategy** szintű hibák maradtak. Debug-Complex szükséges.

---

## 🎯 Primary Objectives

### 1. Session Lifecycle Collision (15 failed tests)

**File:** [`neural_ai/core/db/implementations/sqlalchemy_session.py`](neural_ai/core/db/implementations/sqlalchemy_session.py)

**Problem Hypothesis:**
```python
class DatabaseManager:
    _instance = None  # ⚠️ Singleton + pytest-xdist = COLLISION
    
    @classmethod
    def get_engine(cls):
        if cls._instance is None:
            cls._instance = create_engine(...)
        return cls._instance
```

**Collision Scenario:**
```
pytest-xdist worker gw0:
├── Calls get_engine()
├── _instance created + cached
└── Session active ✅

pytest-xdist worker gw1 (PARALLEL, DIFFERENT PROCESS):
├── Tries to access same _instance
├── Session already closed (gw0 finished)
└── ValueError: Session is closed ❌
```

**Failed Tests (15):**
```
tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py
├── TestDatabaseURL::test_get_database_url_without_config
├── TestCreateEngine::test_create_engine_postgresql*
├── TestGetEngine::test_get_engine_*
├── TestGetAsyncSessionMaker::test_get_async_session_maker_*
├── TestDatabaseManager::test_database_manager_*
├── TestContextManagers::test_get_db_session*
└── TestDatabaseInitialization::test_*_db
```

**Solution Approach:**
```python
# conftest.py - Session-level cleanup
@pytest.fixture(autouse=True)
def cleanup_db_singleton():
    """Reset database singleton cache after each test"""
    yield
    # Clear singleton
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    DatabaseManager._instance = None
    DatabaseManager._async_session_maker = None
```

**Validation:**
```bash
# Should pass individually
pytest tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseURL::test_get_database_url_without_config --forked -v

# Should pass in batch
pytest tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py --forked -v
```

---

### 2. Dict vs. BaseModel Mock Strategy (18 failed tests)

**File:** [`tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py`](tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py)

**Problem:**
```python
# ❌ HIBÁS - Config is dict, but code expects BaseModel
config_mock = {"d2": {"merge_levels": 5}}
processor = D2SupportProcessor(config=config_mock)
# AttributeError: 'dict' object has no attribute 'get_d2_config'

# ✅ HELYES - Pydantic BaseModel
from pydantic import BaseModel
class D2Config(BaseModel):
    merge_levels: int = 5
    # ... other fields

config_mock = D2Config(merge_levels=5)
processor = D2SupportProcessor(config=config_mock)
```

**Failed Tests (18):**
```
test_d02_processor_happy_path
test_d02_processor_defaults
test_merge_levels_missing_level_merge_config
test_merge_levels_large_dataframe_skip_merge
test_confirm_with_volume_missing_config
test_confirm_with_volume_false
test_confirm_with_volume_true
test_nearest_support_no_candidates_below
test_nearest_resistance_no_candidates_above
test_process_with_bid_columns_no_mid
test_process_with_simple_ohlc_no_mid
test_process_with_market_hours_enabled_filtering
test_process_with_market_hours_outside_hours
test_process_calculates_nearest_support
test_process_calculates_nearest_resistance
test_process_with_insufficient_data
```

**Solution Approach:**

1. **Identify Config Interface:**
   ```python
   # neural_ai/processors/dimensions/d02_support/interfaces/
   class D2Config(BaseModel):
       merge_levels: int
       volume_threshold: float
       market_hours: Optional[dict]
   ```

2. **Create Fixture in conftest.py:**
   ```python
   @pytest.fixture
   def d2_config_mock():
       """Return proper Pydantic config mock"""
       from neural_ai.processors.dimensions.d02_support.interfaces import D2Config
       return D2Config(
           merge_levels=5,
           volume_threshold=1000.0,
           market_hours=None
       )
   ```

3. **Update Test Imports:**
   ```python
   # Before
   config_mock = {"d2": {"merge_levels": 5}}
   
   # After
   from conftest import d2_config_mock
   # Or use fixture parameter
   def test_something(d2_config_mock):
       processor = D2SupportProcessor(config=d2_config_mock)
   ```

**Validation:**
```bash
pytest tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py --forked -v
```

---

### 3. Private Attribute Mock Pattern (2 failed tests)

**File:** [`tests/neural_ai/ui/test_ui_factory.py`](tests/neural_ai/ui/test_ui_factory.py)

**Problem:**
```python
# ❌ HIBÁS - Mock not initialized with spec
mock_logger = Mock()
service = UIService(logger=mock_logger)
service._logger.info(...)  # ❌ AttributeError

# ✅ HELYES - Mock with spec_set
mock_logger = Mock(spec_set=['info', 'error', 'warning'])
service = UIService(logger=mock_logger)
service._logger.info(...)  # ✅ Works (internal mock call)
```

**Failed Tests (2):**
```
tests/neural_ai/ui/test_ui_factory.py::TestUIServiceFactoryInit::test_init_creates_instance
tests/neural_ai/ui/test_ui_factory.py::TestUIServiceFactoryInitialize::test_initialize_with_dict_config
```

**Solution Approach:**

```python
# conftest.py - Add logger fixture with proper spec
@pytest.fixture
def mock_logger():
    """Logger mock with proper spec"""
    from unittest.mock import Mock
    mock = Mock(spec_set=['info', 'error', 'warning', 'debug'])
    return mock

# test_ui_factory.py
def test_init_creates_instance(mock_logger):
    """Test with proper logger mock"""
    factory = UIServiceFactory(logger=mock_logger)
    service = factory.create()
    
    mock_logger.info.assert_called_once()  # ✅ Works
```

**Validation:**
```bash
pytest tests/neural_ai/ui/test_ui_factory.py --forked -v
```

---

### 4. Implementation Leak Check (1 failed test)

**File:** [`neural_ai/core/config/implementations/__init__.py`](neural_ai/core/config/implementations/__init__.py)

**Problem:**
```python
# ❌ ROSSZ - Implementations exported
from .concrete_impl import ConcreteClass

# ✅ HELYES - Empty (facade pattern)
# (nothing here)
```

**Failed Test (1):**
```
tests/neural_ai/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_module_is_empty
```

**Solution:**
```bash
# Check file
cat neural_ai/core/config/implementations/__init__.py

# If not empty, truncate
echo "" > neural_ai/core/config/implementations/__init__.py

# Verify
pytest tests/neural_ai/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_module_is_empty -v
```

---

### 5. Event Factory Config Mock (4 failed tests)

**File:** [`tests/neural_ai/core/events/test_events_factory.py`](tests/neural_ai/core/events/test_events_factory.py)

**Problem Cascade:**
```
Config dict mock (like D2)
    ↓
EventBusFactory expects Pydantic config
    ↓
AttributeError: 'dict' object has no attribute 'get_event_config'
```

**Failed Tests (4):**
```
TestEventBusFactoryCreateFromConfig::test_create_from_config_success
TestEventBusFactoryCreateFromConfig::test_create_from_config_with_key_error
TestEventBusFactoryCreateFromConfig::test_create_from_config_with_value_error
TestEventBusFactoryCreateFromConfig::test_create_from_config_partial_config
```

**Solution:**
```python
# Same pattern as D2
@pytest.fixture
def event_config_mock():
    """Event config Pydantic model"""
    from neural_ai.core.events.interfaces import EventBusConfig
    return EventBusConfig(
        transport="zeromq",
        port=5555
    )

# Update tests
def test_create_from_config_success(event_config_mock):
    factory = EventBusFactory()
    bus = factory.create_from_config(event_config_mock)
```

---

### 6. Core Init Bootstrap (7 failed tests)

**File:** [`tests/neural_ai/core/test_core_init.py`](tests/neural_ai/core/test_core_init.py)

**Problem:**
```
Bootstrap sequence:
1. HardwareInfo (✅)
2. ConfigManager (✅)
3. Logger (✅)
4. EventBus (❌ config mock wrong)
5. Storage (❌ cascading)
6. Database (❌ cascading)
7. SystemMonitor (❌ cascading)
```

**Failed Tests (7):**
```
TestBootstrapCore::test_bootstrap_core_success
TestBootstrapCore::test_bootstrap_core_returns_core_components
TestGetCoreComponents::test_get_core_components_first_call
TestGetCoreComponents::test_get_core_components_returns_core_components
TestIntegration::test_version_and_bootstrap_integration
TestIntegration::test_core_components_singleton_pattern
TestBootstrapCoreRealConfig::test_bootstrap_with_real_yaml_configs
```

**Solution:**
```python
# conftest.py - Full mock bootstrap
@pytest.fixture
def mock_bootstrap_config():
    """Complete config for bootstrap testing"""
    from pydantic import BaseModel
    
    class BootstrapConfig(BaseModel):
        event_bus: dict
        storage: dict
        database: dict
        logger: dict
    
    return BootstrapConfig(
        event_bus={"transport": "zeromq"},
        storage={"backend": "parquet"},
        database={"url": "sqlite:///:memory:"},
        logger={"level": "DEBUG"}
    )
```

---

## 🔧 Implementation Plan

### Phase 1: Singleton Cleanup (Konfidencia: 95%)
1. Add `cleanup_db_singleton` fixture to conftest.py
2. Run DB tests
3. Verify: `pytest tests/neural_ai/core/db/... --forked -v`

### Phase 2: Config Mock Strategy (Konfidencia: 90%)
1. Create Pydantic config fixtures (D2, Events, Bootstrap)
2. Update test imports
3. Run processor tests
4. Verify: `pytest tests/neural_ai/processors/... --forked -v`

### Phase 3: Private Attribute Mock (Konfidencia: 85%)
1. Add `mock_logger` fixture with `spec_set`
2. Update UI factory tests
3. Verify: `pytest tests/neural_ai/ui/... --forked -v`

### Phase 4: Implementation Leak Fix (Konfidencia: 100%)
1. Check and fix `implementations/__init__.py`
2. Verify: `pytest tests/neural_ai/core/config/... --forked -v`

### Phase 5: Cascade Validation (Konfidencia: 80%)
1. Run full suite: `pytest tests/ --forked -v`
2. Verify all 51 failed → 0 failed
3. Check performance regression

---

## 📊 Success Criteria

| Metric | Current | Target |
|:-------|:-------:|:------:|
| **Failed tests** | 51 | 0 |
| **Passed tests** | 2370 | 2378 (2370+8) |
| **Skipped tests** | 26 | 26 |
| **Isolation errors** | 51 | 0 |
| **Type errors** | 0 | 0 |
| **Performance** | ~450s | ~300s (expected) |

---

## 📎 Related Files

**To Debug:**
- [`sqlalchemy_session.py`](neural_ai/core/db/implementations/sqlalchemy_session.py)
- [`test_support_processor.py`](tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py)
- [`test_ui_factory.py`](tests/neural_ai/ui/test_ui_factory.py)
- [`test_events_factory.py`](tests/neural_ai/core/events/test_events_factory.py)
- [`test_core_init.py`](tests/neural_ai/core/test_core_init.py)

**To Update:**
- [`conftest.py`](tests/conftest.py) - Add fixtures + cleanup

**To Fix:**
- [`neural_ai/core/config/implementations/__init__.py`](neural_ai/core/config/implementations/__init__.py)

---

## 🚀 Execution Checklist

- [ ] Understand singleton cache collision
- [ ] Review conftest.py current state
- [ ] Implement cleanup_db_singleton fixture
- [ ] Create Pydantic config fixtures
- [ ] Add mock_logger with spec_set
- [ ] Fix implementations/__init__.py
- [ ] Run Phase 1 tests
- [ ] Run Phase 2 tests
- [ ] Run Phase 3 tests
- [ ] Run Phase 4 tests
- [ ] Run full suite validation
- [ ] Measure performance
- [ ] Document findings

---

## ⚠️ Critical Notes

1. **DO NOT** fix logic errors - only fixture/mock scope issues
2. **MUST** preserve existing passing tests (2370)
3. **MUST** maintain type safety (mypy pass)
4. **MUST** run full suite after each phase
5. **DO NOT** modify actual implementation code (only tests + conftest)

---

**QA Delegation Complete**  
**Debug-Complex: Ready to Execute**  
**ETA: 2-3 hours**
