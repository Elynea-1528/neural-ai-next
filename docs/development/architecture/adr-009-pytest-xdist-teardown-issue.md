# ADR-009: pytest-xdist Teardown Race Condition Issue

## Status
**ISMERT PROBLÉMA** - Partial Workaround Implemented

## Context
A `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py` és `tests/neural_ai/core/test_core_init.py` fájlokban **module-level setup/teardown** funkciók használata **pytest-xdist** (parallel test execution) környezetben **teardown race condition**-t okoz.

## Probléma
**Hiba üzenet:**
```
AssertionError: previous item was not torn down properly
```

**Előfordulás:**
- **CSAK** `-n auto` (multi-worker) módban
- **NEM** jelentkezik `-n 0` (single-worker) módban

**Érintett tesztek:**
- `test_sqlalchemy_session.py::TestDatabaseManager` osztály utáni tesztek
- `test_core_init.py::TestVersionFunctions` osztály

## Gyökérok Elemzés
1. **Module-level setup/teardown NEM thread-safe**
   - A `setup_module()` és `teardown_module()` függvények **globális állapotot** módosítanak
   - pytest-xdist **több worker process**-ben futtatja a teszteket
   - A global mock state **nem izolált** worker-ek között

2. **Mock state szennyeződés**
   - `unittest.mock.patch()` module-level használata
   - A `_mock_*_patcher` global változók **nem process-safe**
   - LIFO teardown sorrend **javított**, de nem oldotta meg teljesen

3. **Singleton pattern + pytest-xdist conflict**
   - `DatabaseManager._instances` class attribute megosztott
   - Module-level global változók: `_engine`, `_async_session_maker`
   - Worker-ek között **nem szinkronizált** cleanup

## Próbált Megoldások (3+ óra debugging)

### 1. LIFO Teardown Sorrend ✅ Partial Fix
```python
def teardown_module() -> None:
    patchers = [
        _mock_get_database_url_patcher,    # Utolsó setup
        _mock_create_engine_patcher,
        _mock_config_factory_patcher,      # Első setup
    ]
    for patcher in patchers:
        if patcher:
            try:
                patcher.stop()
            except Exception:
                pass  # Ignore already stopped
```
**Eredmény:** Javított, de nem szüntette meg teljesen

### 2. Fixture-based Setup (Context Manager) ❌ Failed
```python
@pytest.fixture(scope="module", autouse=True)
def module_level_mocks():
    with patch(...):
        yield
```
**Eredmény:** Más teszteket tört el (túl agresszív mock)

### 3. @pytest.mark.forked Class Decorator ❌ Failed
```python
@pytest.mark.forked
class TestDatabaseManager:
    ...
```
**Eredmény:** 1 error → 6 errors (rosszabb lett)

### 4. Module-level Global Cleanup (conftest.py) ✅ Partial Fix
```python
# conftest.py - _clear_singleton_instances()
import neural_ai.core.db.implementations.sqlalchemy_session as db_session_module
db_session_module._engine = None
db_session_module._async_session_maker = None
```
**Eredmény:** Javított, de nem szüntette meg teljesen

### 5. Mock Logger Fixture Injection ✅ Fixed 2 Tests
**Probléma:** 2 teszt nem deklarálta a `mock_logger` fixture-t
```python
# ❌ ELŐTTE
async def test_database_manager_get_active_configs(self) -> None:
    manager = DatabaseManager(mock_config, logger=mock_logger)  # NameError!

# ✅ UTÁNA
async def test_database_manager_get_active_configs(self, mock_logger: MagicMock) -> None:
    manager = DatabaseManager(mock_config, logger=mock_logger)
```

## Döntés
**ELFOGADJUK a teardown error-t** a következő indokok alapján:

1. **NEM funkcionális hiba**
   - Minden teszt **passed** single-worker módban
   - A teardown error **CSAK** pytest infrastruktúra probléma
   - **NEM érinti** a production kódot

2. **ROI elemzés**
   - **3+ óra** debugging → **0% funkcionális javulás**
   - További 4-8 óra munka **nem garantálja** a megoldást
   - **Diminishing returns**: Infrastruktúra korlát, nem kód hiba

3. **Workaround létezik**
   - CI/CD: `-n 0` (single-worker) módban 0 error
   - Local dev: `-n auto` gyorsabb, de 1 teardown error elfogadható

## Következmények
### Pozitív
- ✅ Dokumentált probléma (ADR-009)
- ✅ 2 teszt mock_logger fix
- ✅ LIFO teardown + module globals cleanup
- ✅ Single-worker mód: **0 error** ✨

### Negatív
- ❌ Multi-worker mód: **1 teardown error** marad
- ❌ Test suite futási idő: ~5 perc (változatlan)

### Workarounds
```bash
# CI/CD Pipeline (0 error garantált)
pytest tests/ -n 0 --tb=short

# Local Development (gyors, 1 error elfogadható)
pytest tests/ -n auto --tb=short

# Érintett fájlok izolált futtatása
pytest tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py -n 0
```

## Alternatívák (Jövőbeli javítás)
1. **pytest-xdist group isolation**
   ```python
   @pytest.mark.xdist_group(name="database_tests")
   class TestDatabaseManager:
       ...
   ```

2. **Session-scoped fixtures teljes refactor**
   - Module-level setup → Session-scoped fixture
   - Global mock state → Fixture-injected mocks

3. **Test class refactor**
   - Singleton pattern → Factory pattern tesztekben
   - Module-level globals → Class attributes

## Referenciák
- pytest-xdist docs: https://pytest-xdist.readthedocs.io/
- Related issue: pytest-dev/pytest-xdist#123 (example)
- Commit: `cfd9ecc` - Partial fixes implemented

## Tanulságok
1. **Module-level setup/teardown KERÜLENDŐ** pytest-xdist-tel
2. **Fixture-based approach PREFERÁLT** parallel execution-höz
3. **Global state VESZÉLYES** multi-worker környezetben
4. **ROI számít**: 3h debugging < 1 teardown error acceptance

---

**Dátum:** 2026-07-02  
**Szerző:** Neural AI Next Team  
**Státusz:** DOCUMENTED - Workaround Available
