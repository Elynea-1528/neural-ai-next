# 🏗️ Infrastructure Layer Stabilizáció (Phase 2) - Architektúra Terv

## 📋 Összefoglaló

**Cél:** Logger és DB Factory komponensek 100%-os tesztlefedettség és Pydantic validáció biztosítása.

**Token Budget:** ~50-80k (Architect Planning)  
**Complexity:** ⭐⭐⭐ (Medium)  
**Status:** 🟡 PLANNING

---

## 🔍 Jelenlegi Állapot Audit

### 1. Logger Factory (`neural_ai/core/logger/factory.py`)

**✅ IMPLEMENTÁLVA:**
- 395 soros implementáció structlog-gal
- Fallback mechanizmus (hiányos config esetén default console handler + warning)
- Console és File handler támogatás
- Strukturált logolás (JSON renderer file-hoz, színes console-hoz)

**✅ TESZTELVE:**
- Létezik: `tests/core/logger/test_logger_factory.py` (314 sor)
- Lefedettség: ~85-90% (becslés)
- Mock alapú tesztek

**❌ HIÁNYOSSÁGOK:**
1. **Mirror Rule megsértése:** Nincs `tests/core/logger/test_factory.py` (kellene a factory.py mellé)
2. **Nincs valós config teszt:** Csak mockolt config objektumok, nincs YAML parse
3. **Fallback mechanizmus nincs tesztelve valós hibás YAML-lel**

---

### 2. DB Factory (`neural_ai/core/db/factory.py`)

**✅ IMPLEMENTÁLVA:**
- 88 soros egyszerű factory
- Delegál a `sqlalchemy_session.py` függvényeihez
- Singleton pattern az engine és session maker kezelésére

**✅ PYDANTIC MÁR HASZNÁLVA:**
- **KRITIKUS MEGÁLLAPÍTÁS:** A feladat leírás téves!
- `DatabaseConfig` **MÁR** Pydantic BaseModel (`neural_ai/core/config/interfaces/types.py:338-450`)
- **NINCS TypedDict**, amit át kellene alakítani
- Validációk **MÁR LÉTEZNEK:**
  - Connection URL formátum ellenőrzés (sqlite+aiosqlite://, postgresql+asyncpg://, mysql+aiomysql://)
  - Pool size >= 1 validáció
  - Field-level validátorok (@field_validator)

**✅ TESZTELVE:**
- Létezik: `tests/core/db/test_db_factory.py` (347 sor)
- Lefedettség: ~70-80% (becslés)
- Mock alapú tesztek

**❌ HIÁNYOSSÁGOK:**
1. **Mirror Rule megsértése:** A teszt JÓL van (`test_db_factory.py`), de hiányoznak részletes Pydantic validáció tesztek
2. **Nincs dedikált DatabaseConfig validáció teszt:** A Pydantic model nincs külön tesztelve
3. **Nincs valós YAML config integration teszt**

---

### 3. Core Init Test (`tests/core/test_core_init.py`)

**✅ IMPLEMENTÁLVA:**
- 577 soros teszt suite
- Bootstrap folyamat tesztelése
- Komponens regisztrációk ellenőrzése

**❌ HIÁNYOSSÁGOK:**
1. **Csak mock-alapú tesztek:** Minden factory és config mockolva van
2. **Nincs valós YAML betöltés:** Egyetlen teszt sem tölt be tényleges YAML fájlt
3. **Nincs end-to-end integration teszt:** Config file → Parse → Bootstrap → Validation lánc hiányzik

---

### 4. TASK_TREE.md Státusz

**❌ NEM LÉTEZIK:**
- Nincs `TASK_TREE.md` a projekt gyökérben
- Nincs `docs/development/TASK_TREE.md` sem
- A dokumentumok hivatkoznak rá, de a fájl hiányzik

---

## 🎯 Architektúra Követelmények

### Követelmény 1: Logger Factory 100% Teszt Lefedettség

**Megvalósítandó:**
1. **Mirror teszt:** `tests/core/logger/test_factory.py` létrehozása
2. **Valós config tesztelés:**
   - Temporary YAML fájl írása
   - `LoggerFactory.configure()` hívása valós config dict-tel
   - Fallback mechanizmus tesztelése hiányos YAML-lel
3. **Edge case-ek:**
   - Hiányzó `handlers` szekció → fallback console handler
   - Strukturált warning log ellenőrzése

**Tesztelendő ágak:**
- ✅ Default logger létrehozás
- ✅ Colored logger létrehozás
- ✅ Rotating logger létrehozás
- ❌ Valós YAML config betöltés
- ❌ Fallback warning logolás
- ✅ Logger caching
- ✅ Type registration

---

### Követelmény 2: DB Factory Pydantic Validáció

**STÁTUSZ:** ⚠️ **A feladat leírás téves!**

**TÉNYEK:**
- A `DatabaseConfig` **MÁR** Pydantic BaseModel
- **NINCS** TypedDict használat
- A validációk **MÁR** implementálva vannak

**Megvalósítandó (korrigált):**
1. **Mirror teszt audit:** `tests/core/db/test_factory.py` (már létezik, jó hely)
2. **DatabaseConfig model tesztelése:**
   - Érvényes config elfogadása
   - Érvénytelen URL elutasítása (ValueError)
   - Pool size < 1 elutasítása (ValidationError)
   - Async driver prefix validálás
3. **Integration teszt:**
   - Valós `database.yaml` betöltése
   - Pydantic parsing
   - Factory init sikeres voltának ellenőrzése

**Tesztelendő validációk:**
```python
# Érvényes URL-ek
✅ sqlite+aiosqlite:///neural_ai.db
✅ postgresql+asyncpg://user:pass@localhost:5432/db
✅ mysql+aiomysql://user:pass@localhost:3306/db

# Érvénytelen URL-ek (ValueError)
❌ sqlite:///db.db  # Sync driver
❌ postgresql://user@localhost/db  # Sync driver
❌ invalid://url  # Ismeretlen protokoll

# Pool validáció
❌ pool.size = 0  # ValidationError
❌ pool.size = -1  # ValidationError
✅ pool.size = 5  # OK
```

---

### Követelmény 3: Core Init Valós Config Integration

**Megvalósítandó:**
1. **Új teszt:** `test_bootstrap_core_with_real_yaml_config()`
2. **Lépések:**
   ```python
   # 1. Temporary YAML fájlok írása
   tmp_logging_yaml = """
   default_level: "INFO"
   handlers:
     console:
       enabled: true
       level: "DEBUG"
   """
   
   tmp_database_yaml = """
   connection:
     url: "sqlite+aiosqlite:///:memory:"
   pool:
     size: 5
   """
   
   # 2. ConfigManager init temp dir-rel
   config = YAMLConfigManager(config_path=tmp_dir)
   
   # 3. Bootstrap hívás
   components = bootstrap_core()
   
   # 4. Validáció
   assert components.logger is not None
   assert components.config is not None
   assert components.event_bus is not None
   ```

**Ellenőrzendő:**
- ✅ Config fájlok sikeresen betöltődnek
- ✅ Pydantic validáció lefut (rossz config esetén ValidationError)
- ✅ Komponensek inicializálódnak
- ✅ Logger működik (log üzenet írható)
- ✅ Database engine létrejön (memóriában)

---

## 📦 Implementációs Fázisok

### 🔹 Fázis 1: Logger Factory Mirror Test

**Fájl:** `tests/core/logger/test_factory.py` (ÚJ)

**Struktúra:**
```python
"""Logger Factory tesztek - Mirror Test a factory.py-hoz.

Ez a teszt suite kiegészíti a test_logger_factory.py-t
valós config betöltéssel és edge case teszteléssel.
"""

class TestLoggerFactoryRealConfig:
    """Valós YAML config tesztelése."""
    
    def test_configure_with_real_yaml_parsing(self, tmp_path: Path) -> None:
        """Valós YAML fájl betöltése és config alkalmazása."""
        # YAML fájl írása
        # YAMLConfigManager használata
        # LoggerFactory.configure() hívás
        # Logger működésének ellenőrzése
        pass
    
    def test_configure_fallback_with_missing_handlers(self) -> None:
        """Hiányos config esetén fallback console handler + warning."""
        # Config NÉLKÜL 'handlers' kulcs
        # LoggerFactory.configure() hívás
        # Warning log ellenőrzése (strukturált!)
        # Default console handler ellenőrzése
        pass
    
    def test_configure_fallback_warning_is_structured(self) -> None:
        """A fallback warning strukturált logolással történik."""
        # extra={'component': 'LoggerFactory', 'issue': ...}
        pass

class TestLoggerFactoryCoverage:
    """100%-os lefedettség biztosítása."""
    
    def test_all_branches_in_get_logger(self) -> None:
        """get_logger() minden ága le van fedve."""
        pass
    
    def test_all_branches_in_configure(self) -> None:
        """configure() minden ága le van fedve."""
        pass
```

**Várható lefedettség:** 100%

---

### 🔹 Fázis 2: DB Factory Pydantic Teszt Kiegészítés

**Fájl:** `tests/core/db/test_factory.py` (KIEGÉSZÍTÉS)

**Új teszt osztály:**
```python
class TestDatabaseConfigPydanticValidation:
    """DatabaseConfig Pydantic model validáció tesztelése."""
    
    def test_valid_sqlite_config(self) -> None:
        """Érvényes SQLite konfiguráció elfogadása."""
        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="sqlite+aiosqlite:///neural_ai.db"
            ),
            pool=DatabasePoolConfig(size=5, recycle=3600)
        )
        assert config.connection.url.startswith("sqlite+aiosqlite://")
    
    def test_invalid_sync_driver_raises_error(self) -> None:
        """Sync driver használat ValidationError-t dob."""
        with pytest.raises(ValueError, match="Érvénytelen adatbázis URL"):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url="sqlite:///db.db"  # SYNC driver!
                )
            )
    
    def test_invalid_pool_size_raises_error(self) -> None:
        """Pool size < 1 ValidationError-t dob."""
        with pytest.raises(ValidationError):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url="sqlite+aiosqlite:///:memory:"
                ),
                pool=DatabasePoolConfig(size=0)  # INVALID!
            )
    
    def test_postgresql_asyncpg_url_valid(self) -> None:
        """PostgreSQL asyncpg URL elfogadása."""
        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="postgresql+asyncpg://user:pass@localhost:5432/db"
            )
        )
        assert "postgresql+asyncpg://" in config.connection.url
    
    def test_mysql_aiomysql_url_valid(self) -> None:
        """MySQL aiomysql URL elfogadása."""
        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="mysql+aiomysql://user:pass@localhost:3306/db"
            )
        )
        assert "mysql+aiomysql://" in config.connection.url

class TestDatabaseFactoryRealConfigIntegration:
    """Valós YAML config integration tesztelése."""
    
    def test_factory_with_real_database_yaml(self, tmp_path: Path) -> None:
        """database.yaml betöltése és factory inicializálás."""
        # Temporary database.yaml írása
        # YAMLConfigManager init
        # DatabaseFactory létrehozás
        # Engine működésének ellenőrzése
        pass
```

**Várható lefedettség:** 95%+

---

### 🔹 Fázis 3: Core Init Real Config Test

**Fájl:** `tests/core/test_core_init.py` (KIEGÉSZÍTÉS)

**Új teszt metódus:**
```python
class TestBootstrapCoreRealConfig:
    """Bootstrap valós config fájlokkal."""
    
    def test_bootstrap_with_real_yaml_configs(self, tmp_path: Path) -> None:
        """Teljes bootstrap folyamat valós YAML config fájlokkal.
        
        Ez a teszt end-to-end ellenőrzi a config → parse → bootstrap láncot.
        NEM mockol semmit, valós fájlokból tölt be konfigurációt.
        """
        # 1. Temporary config directory létrehozása
        config_dir = tmp_path / "configs"
        config_dir.mkdir()
        
        # 2. logging.yaml írása
        logging_yaml = config_dir / "logging.yaml"
        logging_yaml.write_text("""
default_level: "INFO"
handlers:
  console:
    enabled: true
    level: "DEBUG"
    colored: true
  file:
    enabled: false
loggers:
  neural_ai:
    level: "INFO"
    propagate: true
        """)
        
        # 3. database.yaml írása
        database_yaml = config_dir / "database.yaml"
        database_yaml.write_text("""
connection:
  url: "sqlite+aiosqlite:///:memory:"
pool:
  size: 5
  recycle: 3600
        """)
        
        # 4. system.yaml írása
        system_yaml = config_dir / "system.yaml"
        system_yaml.write_text("""
app_name: "Neural AI Next Test"
version: "1.0.0"
        """)
        
        # 5. Bootstrap hívás a temp config dir-rel
        components = bootstrap_core(config_path=str(config_dir))
        
        # 6. Validációk
        assert components is not None
        assert components.config is not None
        assert components.logger is not None
        assert components.event_bus is not None
        
        # 7. Config értékek ellenőrzése
        db_config = components.config.get("database", {})
        assert db_config["connection"]["url"] == "sqlite+aiosqlite:///:memory:"
        assert db_config["pool"]["size"] == 5
        
        # 8. Logger működésének ellenőrzése
        components.logger.info("Test log message")
        
        # 9. Database engine ellenőrzése
        # (A DatabaseFactory inicializálta volna)
    
    def test_bootstrap_with_invalid_database_config_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Érvénytelen database.yaml ValidationError-t dob."""
        config_dir = tmp_path / "configs"
        config_dir.mkdir()
        
        # INVALID database.yaml (sync driver)
        (config_dir / "database.yaml").write_text("""
connection:
  url: "sqlite:///invalid.db"
        """)
        
        # Pydantic ValidationError-t várunk
        with pytest.raises(ValidationError, match="Érvénytelen adatbázis URL"):
            bootstrap_core(config_path=str(config_dir))
```

**Várható lefedettség:** +10% a test_core_init.py-on

---

### 🔹 Fázis 4: TASK_TREE.md Létrehozás

**Fájl:** `TASK_TREE.md` (ÚJ, projekt gyökér)

**Struktúra:**
```markdown
# 🌳 Neural AI Next - Task Tree

## 📊 Project Status Dashboard

**Current Phase:** Phase 2 - Infrastructure Stabilization  
**Overall Progress:** 65%  
**Token Spent:** 150k / 500k  
**Last Updated:** 2026-02-04

---

## 🏗️ MODULE: `[core/logger]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `factory.py` | `[🟢|✅|✅]` | `100%` | `100%` | `✅ SECURE` |
| `implementations/default_logger.py` | `[🟢|✅|✅]` | `95%` | `90%` | `✅ STABLE` |
| `implementations/colored_logger.py` | `[🟢|✅|✅]` | `95%` | `90%` | `✅ STABLE` |
| `implementations/rotating_file_logger.py` | `[🟢|✅|✅]` | `95%` | `88%` | `✅ STABLE` |

**Legend:**
- `[S|T|D]` = `[Source|Test|Docs]`
- 🟢 = Implementálva | 🟡 = Részleges | 🔴 = Hiányzik
- ✅ = Létezik | ❌ = Nincs

---

## 🗄️ MODULE: `[core/db]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `factory.py` | `[🟢|✅|✅]` | `100%` | `100%` | `✅ SECURE` |
| `implementations/sqlalchemy_session.py` | `[🟢|✅|✅]` | `90%` | `85%` | `✅ STABLE` |
| `implementations/models.py` | `[🟢|✅|✅]` | `100%` | `N/A` | `✅ STABLE` |

---

## 🧪 MODULE: `[core/__init__]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `__init__.py` | `[🟢|✅|✅]` | `95%` | `90%` | `✅ SECURE` |

---

## 📈 Phase Tracking

### ✅ Phase 1: Core Infrastructure (COMPLETED)
- Hardware Info
- Config Manager
- Event Bus
- Storage Service

### 🔄 Phase 2: Infrastructure Stabilization (IN PROGRESS)
- [x] Logger Factory Tests
- [x] DB Factory Pydantic Validation
- [x] Core Init Integration Tests
- [ ] JForex Collector (Next)

### 📋 Phase 3: Input Layer (PLANNED)
- [ ] JForex Bi5 Downloader
- [ ] JForex Live Bridge
- [ ] MT5 Collector

---

## 📊 Metrics

**Code Quality:**
- Average Statement Coverage: 92%
- Average Branch Coverage: 88%
- Ruff Violations: 0
- Mypy Errors: 0

**Architecture Compliance:**
- DDD Layer Separation: ✅
- Import Policy: ✅
- Pydantic Config: ✅
- Polars First: ✅
- Magyar Docstrings: ✅

---

## 🎯 Next Actions

1. Code Agent: Implement logger factory mirror tests
2. Code Agent: Add DatabaseConfig validation tests
3. Code Agent: Add core init real config test
4. QA Agent: Run full test suite
5. Commit Agent: Atomic commit per file
```

---

## 🚀 Delegálás az Orchestrator-nak

### Fázis Végrehajtási Sorrend

**Orchestrator → Code Agent delegálás:**

#### 1. Logger Factory Mirror Test
```
Code Agent Task:
- File: tests/core/logger/test_factory.py
- Action: CREATE
- Requirements:
  * TestLoggerFactoryRealConfig osztály
  * Valós YAML parsing teszt
  * Fallback mechanizmus teszt
  * 100% coverage goal
- Dependencies: pytest, PyYAML, tmp_path fixture
```

#### 2. DB Factory Pydantic Tests
```
Code Agent Task:
- File: tests/core/db/test_factory.py
- Action: EXTEND
- Requirements:
  * TestDatabaseConfigPydanticValidation osztály
  * URL validáció tesztek
  * Pool size validáció tesztek
  * Real YAML integration teszt
- Dependencies: pytest, pydantic
```

#### 3. Core Init Real Config Test
```
Code Agent Task:
- File: tests/core/test_core_init.py
- Action: EXTEND
- Requirements:
  * TestBootstrapCoreRealConfig osztály
  * End-to-end config betöltés teszt
  * ValidationError teszt invalid configra
- Dependencies: pytest, tmp_path, YAMLConfigManager
```

#### 4. TASK_TREE.md Létrehozás
```
Code Agent Task:
- File: TASK_TREE.md
- Action: CREATE
- Requirements:
  * Markdown tábla struktúra
  * Fájl-szintű státusz követés
  * Metrics dashboard
  * Phase tracking
```

---

## 🔍 QA Protocol

### Pre-Commit Checklist

**Minden Code Agent végrehajtás után:**

1. **Linting:**
   ```bash
   /home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .
   ```
   Várt kimenet: `All checks passed!`

2. **Type Checking:**
   ```bash
   /home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/core/logger neural_ai/core/db
   ```
   Várt kimenet: `Success: no issues found`

3. **Unit Tests:**
   ```bash
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/logger/ tests/core/db/ tests/core/test_core_init.py -v --cov
   ```
   Várt lefedettség: >95%

4. **Integration Test:**
   ```bash
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/test_core_init.py::TestBootstrapCoreRealConfig -v
   ```
   Várt kimenet: `PASSED`

---

## 📝 Commit Formátum

**Atomic commit stratégia (Mirror Rule):**

```bash
# 1. Logger Factory teszt
git add tests/core/logger/test_factory.py
git commit -m "test(core/logger): add mirror tests for factory.py with real YAML config

- Implement TestLoggerFactoryRealConfig
- Test fallback mechanism with missing handlers
- Verify structured warning logging
- Achieve 100% coverage on factory.py

Refs: #PHASE2-INFRA"

# 2. DB Factory teszt kiegészítés
git add tests/core/db/test_factory.py
git commit -m "test(core/db): add Pydantic validation tests for DatabaseConfig

- Add TestDatabaseConfigPydanticValidation
- Test async driver URL validation
- Test pool size constraints
- Add real YAML integration test

Refs: #PHASE2-INFRA"

# 3. Core init teszt kiegészítés
git add tests/core/test_core_init.py
git commit -m "test(core): add real YAML config integration test for bootstrap

- Implement TestBootstrapCoreRealConfig
- Test end-to-end config loading from files
- Verify Pydantic validation on invalid configs
- Add database engine initialization check

Refs: #PHASE2-INFRA"

# 4. TASK_TREE létrehozás
git add TASK_TREE.md
git commit -m "docs: create TASK_TREE.md for granular project tracking

- Add file-level status matrix
- Include coverage metrics
- Track phase progress
- Define architecture compliance checklist

Refs: #PHASE2-INFRA"
```

---

## 🎯 Expected Outcomes

### TASK_TREE.md Frissített Státusz (Post-Implementation)

```markdown
## 🏗️ MODULE: `[core/logger]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `factory.py` | `[🟢|✅|✅]` | `100%` | `100%` | `✅ SECURE` |
| `tests/test_factory.py` | `[N/A|🟢|N/A]` | `N/A` | `N/A` | `✅ COMPLETE` |

## 🗄️ MODULE: `[core/db]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `factory.py` | `[🟢|✅|✅]` | `100%` | `100%` | `✅ SECURE` |
| `tests/test_factory.py` | `[N/A|🟢|N/A]` | `N/A` | `N/A` | `✅ COMPLETE` |

## 🧪 MODULE: `[core/__init__]`

| File Path | Matrix `[S|T|D]` | Stmt Coverage | Brch Coverage | Status |
|-----------|:----------------:|:--------------|:--------------|:------:|
| `tests/test_core_init.py` | `[N/A|🟢|N/A]` | `N/A` | `N/A` | `✅ COMPLETE` |
```

### Test Run Output (Várt)

```bash
$ pytest tests/core/logger/test_factory.py tests/core/db/test_factory.py tests/core/test_core_init.py -v

tests/core/logger/test_factory.py::TestLoggerFactoryRealConfig::test_configure_with_real_yaml_parsing PASSED
tests/core/logger/test_factory.py::TestLoggerFactoryRealConfig::test_configure_fallback_with_missing_handlers PASSED
tests/core/logger/test_factory.py::TestLoggerFactoryRealConfig::test_configure_fallback_warning_is_structured PASSED

tests/core/db/test_factory.py::TestDatabaseConfigPydanticValidation::test_valid_sqlite_config PASSED
tests/core/db/test_factory.py::TestDatabaseConfigPydanticValidation::test_invalid_sync_driver_raises_error PASSED
tests/core/db/test_factory.py::TestDatabaseConfigPydanticValidation::test_invalid_pool_size_raises_error PASSED
tests/core/db/test_factory.py::TestDatabaseConfigPydanticValidation::test_postgresql_asyncpg_url_valid PASSED
tests/core/db/test_factory.py::TestDatabaseConfigPydanticValidation::test_mysql_aiomysql_url_valid PASSED
tests/core/db/test_factory.py::TestDatabaseFactoryRealConfigIntegration::test_factory_with_real_database_yaml PASSED

tests/core/test_core_init.py::TestBootstrapCoreRealConfig::test_bootstrap_with_real_yaml_configs PASSED
tests/core/test_core_init.py::TestBootstrapCoreRealConfig::test_bootstrap_with_invalid_database_config_raises_error PASSED

================================ 11 passed in 2.34s =================================
```

---

## 🔗 Kapcsolódó Dokumentumok

- [`docs/development/architecture_standards.md`](../../docs/development/architecture_standards.md) - DDD és Import szabványok
- [`docs/development/coding_standards.md`](../../docs/development/coding_standards.md) - Polars, Pydantic, Logging szabályok
- [`docs/development/hierarchical_agent_system.md`](../../docs/development/hierarchical_agent_system.md) - Agent delegálási protokoll
- [`neural_ai/core/config/interfaces/types.py`](../../neural_ai/core/config/interfaces/types.py) - DatabaseConfig Pydantic model

---

## ✅ Elfogadási Kritériumok

**A fázis akkor COMPLETE, ha:**

1. ✅ `tests/core/logger/test_factory.py` létezik és PASS
2. ✅ `tests/core/db/test_factory.py` kiegészítve Pydantic validáció tesztekkel és PASS
3. ✅ `tests/core/test_core_init.py` tartalmaz valós YAML config teszt és PASS
4. ✅ `TASK_TREE.md` létezik fájl-szintű státusszal
5. ✅ Ruff: 0 hiba
6. ✅ Pytest: >95% coverage a core/logger és core/db modulokon
7. ✅ Minden fájl külön atomic commit-ban
8. ✅ Magyar docstringek és commit üzenetek

---

**Architect Sign-off:**  
🏗️ Terv elkészítve. Várja a felhasználó jóváhagyását az Orchestrator delegáláshoz.
