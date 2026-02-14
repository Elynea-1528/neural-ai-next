# 🏗️ Infrastructure Layer Stabilizáció - Részletes Tervezési Dokumentáció

**Dátum:** 2026-02-04  
**Fázis:** Phase 2 - Infrastructure Stabilizáció  
**Felelős:** Architect Agent  
**Státusz:** 📋 TERVEZÉS

---

## 📊 EXECUTIVE SUMMARY

### Cél
A Neural AI Next Infrastructure rétegének (Core) modernizálása Pydantic validációval, 100% teszt lefedettséggel és valódi konfiguráció integrációval.

### Scope
- **Logger Factory**: Hiányzó warning logolás + valódi YAML config teszt
- **DB Factory**: TypedDict → Pydantic migráció + URL validáció
- **SQLAlchemy Session**: Dinamikus pool konfiguráció
- **Core Init**: Integrációs teszt valódi config betöltéssel

### Sikerkritériumok
- ✅ `ruff check .` tiszta
- ✅ `pytest tests/core/logger/ tests/core/db/ tests/core/test_core_init.py` 100% pass
- ✅ TASK_TREE.md frissítve (2 piros → zöld)
- ✅ Atomic git commit létrehozva

---

## 🎯 ARCHITEKTÚRA ANALÍZIS

### Jelenlegi Állapot (AS-IS)

#### 1. Logger Factory (`neural_ai/core/logger/factory.py`)
**Státusz**: ⚠️ RÉSZBEN KÉSZ
- ✅ Strukturált logolás (structlog)
- ✅ TypedDict használat (LoggingConfig)
- ✅ configure() metódus implementálva
- ❌ Hiányzik: Warning logolás hiányos config esetén
- ❌ Hiányzik: Valódi YAML config teszt

**Teszt Lefedettség**: ~70%
```
tests/core/logger/test_logger_factory.py:
  ✅ get_logger (default, colored, rotating)
  ✅ register_logger
  ✅ configure (basic, rotating)
  ❌ configure + valós YAML fájl
  ❌ Hiányos config fallback + warning
```

#### 2. DB Factory (`neural_ai/core/db/factory.py`)
**Státusz**: ⚠️ ELAVULT (TypedDict)
- ✅ Async engine factory
- ✅ Session maker factory
- ❌ TypedDict (DatabaseConfig) - LECSERÉLENDŐ
- ❌ Hiányzik: URL formátum validáció
- ❌ Hiányzik: Pool konfig (hardcoded pool_size=20)

**Jelenlegi TypedDict**:
```python
class DatabaseConfig(TypedDict):
    url: str  # Nincs validáció!
```

**Teszt Lefedettség**: ~60% (csak mockolt tesztek)
```
tests/core/db/test_db_factory.py:
  ✅ get_session_maker (mocked)
  ✅ get_engine (mocked)
  ✅ create_engine (SQLite)
  ❌ Pydantic validáció tesztek
  ❌ Valódi config parsing
  ❌ URL formátum hibakezelés
```

#### 3. SQLAlchemy Session (`neural_ai/core/db/implementations/sqlalchemy_session.py`)
**Státusz**: ⚠️ HARDCODED KONFIG
- ✅ Async session management
- ❌ Hardcoded `pool_size=20` (sor 109)
- ❌ TypedDict használat

#### 4. Core Init (`tests/core/test_core_init.py`)
**Státusz**: ⚠️ CSAK MOCKOLT TESZTEK
- ✅ bootstrap_core() unit tesztek
- ❌ Hiányzik: Valódi YAML config betöltés teszt

---

## 🔧 TERVEZETT MEGOLDÁS (TO-BE)

### 1. Pydantic DatabaseConfig Model (types.py)

**Fájl**: `neural_ai/core/config/interfaces/types.py`

**Változtatás**: ÚJ DatabaseConfig Pydantic Model hozzáadása

```python
class DatabaseConfig(BaseModel):
    """Teljes adatbázis konfiguráció Pydantic validációval.
    
    ARCHITEKTÚRA: Szigorú validáció a connection URL-re és pool paraméterekre.
    Lásd: docs/development/architecture_standards.md - Típusbiztonság
    """
    
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    connection: DatabaseConnectionConfig = Field(
        ..., 
        description="Adatbázis kapcsolat konfiguráció"
    )
    pool: DatabasePoolConfig | None = Field(
        None, 
        description="Connection pool konfiguráció"
    )
    
    @field_validator('connection')
    @classmethod
    def validate_connection_url(cls, v: DatabaseConnectionConfig) -> DatabaseConnectionConfig:
        """Ellenőrzi a connection URL formátumát.
        
        Támogatott formátumok:
        - sqlite+aiosqlite:///path/to/db.db
        - postgresql+asyncpg://user:pass@host:port/dbname
        """
        if not v.url:
            raise ValueError("Adatbázis URL megadása kötelező!")
        
        url = v.url.lower()
        valid_prefixes = [
            "sqlite+aiosqlite://",
            "postgresql+asyncpg://",
            "mysql+aiomysql://"
        ]
        
        if not any(url.startswith(prefix) for prefix in valid_prefixes):
            raise ValueError(
                f"Érvénytelen adatbázis URL formátum: {v.url}. "
                f"Támogatott: {', '.join(valid_prefixes)}"
            )
        
        return v
    
    @field_validator('pool')
    @classmethod
    def validate_pool_config(cls, v: DatabasePoolConfig | None) -> DatabasePoolConfig | None:
        """Validálja a pool konfigurációt."""
        if v and v.size is not None and v.size < 1:
            raise ValueError("Pool size nem lehet kisebb mint 1!")
        return v
```

**Indoklás**:
- Pydantic > TypedDict (runtime validáció)
- URL formátum check KRITIKUS (rossz URL → crash)
- Pool size >= 1 biztonsági korlát

---

### 2. DB Factory Refaktorálás (factory.py)

**Fájl**: `neural_ai/core/db/factory.py`

**Változtatások**:
1. Import Pydantic DatabaseConfig a types.py-ból
2. TypedDict eltávolítása
3. Pydantic validáció használata

```python
# ELŐTTE (TypedDict - sor 24-31):
from typing import TypedDict

class DatabaseConfig(TypedDict):
    url: str

# UTÁNA (Pydantic import):
from neural_ai.core.config.interfaces.types import DatabaseConfig
```

**NEM változik**: Factory metódusok logikája (get_engine, get_session_maker stb.)

---

### 3. SQLAlchemy Session Refaktorálás (sqlalchemy_session.py)

**Fájl**: `neural_ai/core/db/implementations/sqlalchemy_session.py`

**Változtatások**:

1. **Import cseréje** (sor 28-35):
```python
# ELŐTTE:
from typing import TypedDict

class DatabaseConfig(TypedDict):
    url: str

# UTÁNA:
from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabasePoolConfig
```

2. **create_engine() dinamikus pool** (sor 86-113):
```python
def create_engine(
    db_url: str, 
    echo: bool = False,
    pool_config: DatabasePoolConfig | None = None  # ÚJ paraméter
) -> AsyncEngine:
    """Aszinkron adatbázis engine létrehozása.
    
    Args:
        db_url: Az adatbázis URL.
        echo: SQL lekérdezések naplózásának engedélyezése.
        pool_config: Opcionális pool konfiguráció.
    """
    # SQLite esetén pool tiltása
    if "sqlite" in db_url:
        engine = create_async_engine(
            db_url,
            echo=echo,
            poolclass=NullPool,
            connect_args={"check_same_thread": False},
        )
    else:
        # PostgreSQL és más DB-k - dinamikus pool
        pool_size = pool_config.size if pool_config and pool_config.size else 20
        pool_recycle = pool_config.recycle if pool_config and pool_config.recycle else 3600
        
        engine = create_async_engine(
            db_url,
            echo=echo,
            pool_size=pool_size,
            pool_recycle=pool_recycle,
            max_overflow=0,
        )
    
    return engine
```

3. **get_engine() pool átadás** (sor 116-134):
```python
def get_engine(config_manager: ConfigManagerInterface | None = None) -> AsyncEngine:
    global _engine
    
    if _engine is None:
        db_url = get_database_url(config_manager)
        echo = ConfigManagerFactory.get_manager("config.yaml").get("log_level", "INFO") == "DEBUG"
        
        # Pool config lekérése
        db_config_raw = config_manager.get("database") if config_manager else {}
        pool_config = None
        if db_config_raw and isinstance(db_config_raw, dict):
            pool_raw = db_config_raw.get("pool")
            if pool_raw:
                from neural_ai.core.config.interfaces.types import DatabasePoolConfig
                pool_config = DatabasePoolConfig(**pool_raw)
        
        _engine = create_engine(db_url, echo=echo, pool_config=pool_config)
    
    return _engine
```

---

### 4. Logger Factory Fejlesztés (factory.py)

**Fájl**: `neural_ai/core/logger/factory.py`

**Változtatás**: Warning logolás a configure() metódusban (sor 156-178)

```python
@classmethod
def configure(cls, config: dict[str, Any]) -> None:
    """Logger rendszer konfigurálása structlog-gal.
    
    Args:
        config: Konfigurációs dict.
    """
    from pathlib import Path
    
    # TypedDict használata config casting-gal
    typed_config = cast(LoggingConfig, config)
    
    # ÚJ: Hiányos config ellenőrzése
    if not typed_config.get("handlers"):
        import logging
        fallback_logger = logging.getLogger(__name__)
        fallback_logger.warning(
            "Hiányos logger konfiguráció! Alapértelmezett konzol handler lesz használva.",
            extra={"component": "LoggerFactory"}
        )
        # Fallback config
        typed_config["handlers"] = {
            "console": {"enabled": True, "level": "INFO", "colored": True}
        }
    
    # ... meglévő kód folytatódik
```

---

### 5. DB Factory Tesztek Bővítése

**Fájl**: `tests/core/db/test_db_factory.py`

**ÚJ TESZT ESETEK**:

```python
class TestDatabaseFactoryPydanticValidation:
    """Pydantic validációs tesztek."""
    
    def test_database_config_valid_sqlite_url(self):
        """Érvényes SQLite URL validálása."""
        from neural_ai.core.config.interfaces.types import (
            DatabaseConfig, 
            DatabaseConnectionConfig
        )
        
        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="sqlite+aiosqlite:///test.db"
            )
        )
        assert config.connection.url.startswith("sqlite+aiosqlite://")
    
    def test_database_config_invalid_url_raises_error(self):
        """Érvénytelen URL formátum hibát dob."""
        from neural_ai.core.config.interfaces.types import (
            DatabaseConfig,
            DatabaseConnectionConfig
        )
        
        with pytest.raises(ValueError, match="Érvénytelen adatbázis URL"):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url="mysql://invalid"  # Nem async driver
                )
            )
    
    def test_database_config_pool_size_validation(self):
        """Pool size < 1 esetén hibát dob."""
        from neural_ai.core.config.interfaces.types import (
            DatabaseConfig,
            DatabaseConnectionConfig,
            DatabasePoolConfig
        )
        
        with pytest.raises(ValueError, match="Pool size nem lehet kisebb"):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url="postgresql+asyncpg://localhost/test"
                ),
                pool=DatabasePoolConfig(size=0)  # INVALID!
            )
    
    def test_factory_with_real_yaml_config(self, tmp_path: Path):
        """Factory valós YAML konfiggal."""
        # Temporary YAML fájl létrehozása
        yaml_content = """
database:
  connection:
    url: "sqlite+aiosqlite:///test_real.db"
  pool:
    size: 10
    recycle: 1800
"""
        config_file = tmp_path / "database_test.yaml"
        config_file.write_text(yaml_content)
        
        # Config betöltése
        from neural_ai.core.config.factory import ConfigManagerFactory
        config_manager = ConfigManagerFactory.create_manager("yaml")
        config_manager.load_file(str(config_file))
        
        # Factory tesztelése
        factory = DatabaseFactory(
            logger=MagicMock(),
            config_manager=config_manager
        )
        
        engine = factory.get_engine()
        assert engine is not None
```

---

### 6. Logger Factory Teszt Bővítés

**Fájl**: `tests/core/logger/test_logger_factory.py`

**ÚJ TESZT ESETEK**:

```python
def test_configure_with_real_yaml_file(tmp_path: Path) -> None:
    """Logger konfigurálása valódi YAML fájlból."""
    yaml_content = """
default_level: "DEBUG"
handlers:
  console:
    enabled: true
    level: "INFO"
    colored: true
  file:
    enabled: true
    filename: "logs/test_real.log"
    level: "DEBUG"
    json_format: true
    rotating: true
    max_bytes: 1048576
    backup_count: 3
loggers:
  neural_ai:
    level: "DEBUG"
    propagate: true
"""
    config_file = tmp_path / "logging_test.yaml"
    config_file.write_text(yaml_content)
    
    # YAML betöltése
    import yaml
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Configure hívás
    LoggerFactory.configure(config)
    
    # Ellenőrzés
    logger = LoggerFactory.get_logger("test_yaml", level=logging.DEBUG)
    assert logger.get_level() == 10  # DEBUG

def test_configure_missing_handlers_warning(caplog) -> None:
    """Hiányos konfig esetén warning logolás."""
    import logging
    
    # Hiányos config (nincs handlers)
    incomplete_config = {
        "default_level": "INFO"
        # handlers hiányzik!
    }
    
    with caplog.at_level(logging.WARNING):
        LoggerFactory.configure(incomplete_config)
    
    # Ellenőrizzük, hogy volt-e warning
    assert any("Hiányos logger konfiguráció" in record.message 
               for record in caplog.records)
```

---

### 7. Core Init Integrációs Teszt

**Fájl**: `tests/core/test_core_init.py`

**ÚJ TESZT OSZTÁLY**:

```python
class TestRealConfigIntegration:
    """Valódi konfiguráció integrációs tesztek."""
    
    def test_bootstrap_with_real_yaml_config(self, tmp_path: Path) -> None:
        """Bootstrap valós YAML config fájlokkal."""
        # Temporary config könyvtár
        config_dir = tmp_path / "configs"
        config_dir.mkdir()
        
        # database.yaml
        (config_dir / "database.yaml").write_text("""
type: "sqlite"
connection:
  url: "sqlite+aiosqlite:///test_bootstrap.db"
pool:
  size: 5
  recycle: 3600
""")
        
        # logging.yaml
        (config_dir / "logging.yaml").write_text("""
default_level: "INFO"
handlers:
  console:
    enabled: true
    level: "INFO"
loggers:
  neural_ai:
    level: "INFO"
""")
        
        # storage.yaml
        (config_dir / "storage.yaml").write_text("""
backend: "polars"
base_path: "data/storage"
""")
        
        # Bootstrap hívás a custom config dir-rel
        with patch("neural_ai.core.config.factory.ConfigManagerFactory.create_manager") as mock_cfg:
            mock_config = MagicMock()
            
            # Mock config responses
            def get_side_effect(key, default=None):
                if key == "database":
                    return {
                        "connection": {"url": "sqlite+aiosqlite:///test_bootstrap.db"},
                        "pool": {"size": 5}
                    }
                elif key == "storage":
                    return {"base_path": "data/storage"}
                return default
            
            mock_config.get.side_effect = get_side_effect
            mock_config.load_directory.return_value = None
            mock_cfg.return_value = mock_config
            
            # Bootstrap
            core = bootstrap_core()
            
            # Assertions
            assert core is not None
            assert core.has_config()
            assert core.has_logger()
            assert core.has_database()
```

---

## 📂 FÁJLVÁLTOZÁSOK ÖSSZEFOGLALÓ

| # | Fájl | Művelet | Súlyosság | Tesztelés |
|---|------|---------|-----------|-----------|
| 1 | `neural_ai/core/config/interfaces/types.py` | ✏️ MÓDOSÍTÁS (DatabaseConfig hozzáadás) | 🔴 KRITIKUS | Unit |
| 2 | `neural_ai/core/db/factory.py` | ✏️ REFACTOR (TypedDict → Pydantic) | 🔴 KRITIKUS | Unit |
| 3 | `neural_ai/core/db/implementations/sqlalchemy_session.py` | ✏️ MÓDOSÍTÁS (dinamikus pool) | 🟠 MAGAS | Unit |
| 4 | `neural_ai/core/logger/factory.py` | ✏️ MÓDOSÍTÁS (warning logolás) | 🟡 KÖZEPES | Unit |
| 5 | `tests/core/db/test_db_factory.py` | ➕ BŐVÍTÉS (Pydantic + valós config) | 🟢 NORMÁL | - |
| 6 | `tests/core/logger/test_logger_factory.py` | ➕ BŐVÍTÉS (valós YAML teszt) | 🟢 NORMÁL | - |
| 7 | `tests/core/test_core_init.py` | ➕ BŐVÍTÉS (integrációs teszt) | 🟢 NORMÁL | - |
| 8 | `docs/development/TASK_TREE.md` | ✏️ FRISSÍTÉS (státusz) | 🟢 NORMÁL | - |

---

## 🧪 QA PROTOKOLL

### Pre-Commit Checklist

```bash
# 1. Linting
ruff check .

# 2. Type Checking
mypy neural_ai/core/logger neural_ai/core/db

# 3. Unit Tesztek
pytest tests/core/logger/test_logger_factory.py -v
pytest tests/core/db/test_db_factory.py -v
pytest tests/core/test_core_init.py -v

# 4. Teljes Core Teszt
pytest tests/core/ -v --cov=neural_ai/core --cov-report=term-missing

# 5. Integrációs Teszt (valódi config)
pytest tests/core/test_core_init.py::TestRealConfigIntegration -v
```

### Várt Output
```
tests/core/logger/test_logger_factory.py .......... PASSED (100%)
tests/core/db/test_db_factory.py ................ PASSED (100%)
tests/core/test_core_init.py .................... PASSED (100%)

Coverage:
  neural_ai/core/logger/factory.py    100%
  neural_ai/core/db/factory.py        100%
```

---

## 🎯 TASK BREAKDOWN (Orchestrator számára)

### FÁZIS 1: Pydantic Model Létrehozás
**File**: `neural_ai/core/config/interfaces/types.py`
- Hozzáadás: DatabaseConfig class (~50 sor)
- Validátorok: validate_connection_url, validate_pool_config

### FÁZIS 2: DB Layer Refaktorálás
**Files**:
1. `neural_ai/core/db/factory.py`
   - TypedDict törlése (sor 24-31)
   - Import: Pydantic DatabaseConfig
   
2. `neural_ai/core/db/implementations/sqlalchemy_session.py`
   - TypedDict törlése (sor 28-35)
   - create_engine(): pool_config paraméter
   - get_engine(): pool config olvasás

### FÁZIS 3: Logger Factory Warning
**File**: `neural_ai/core/logger/factory.py`
- configure(): hiányos config ellenőrzés + warning (sor 156-178)

### FÁZIS 4: Tesztek Implementálása
**Files**:
1. `tests/core/db/test_db_factory.py`
   - TestDatabaseFactoryPydanticValidation class (~100 sor)
   
2. `tests/core/logger/test_logger_factory.py`
   - test_configure_with_real_yaml_file (~30 sor)
   - test_configure_missing_handlers_warning (~20 sor)
   
3. `tests/core/test_core_init.py`
   - TestRealConfigIntegration class (~80 sor)

### FÁZIS 5: Dokumentáció & Commit
- TASK_TREE.md frissítése
- Git commit: `refactor(core): Logger és DB factory stabilizáció (Pydantic + Tests)`

---

## 🚨 KOCKÁZATOK ÉS MITIGÁCIÓ

| Kockázat | Valószínűség | Hatás | Mitigáció |
|----------|--------------|-------|-----------|
| Pydantic validáció eltöri a meglévő kódot | 🟡 KÖZEPES | 🔴 MAGAS | Fokozatos migráció, backward compat |
| Pool konfig rossz → connection leak | 🟢 ALACSONY | 🔴 MAGAS | Default értékek + validáció |
| YAML teszt nem hordozható | 🟡 KÖZEPES | 🟡 KÖZEPES | tmp_path fixture használata |

---

## 📌 REFERENCIÁK

- **Architecture Standards**: `docs/development/architecture_standards.md`
- **Agent Hierarchy**: `docs/development/hierarchical_agent_system.md`
- **Pydantic Docs**: https://docs.pydantic.dev/latest/
- **SQLAlchemy Pool**: https://docs.sqlalchemy.org/en/20/core/pooling.html

---

## ✅ DEFINITION OF DONE

- [ ] DatabaseConfig Pydantic model létrehozva
- [ ] DB Factory TypedDict → Pydantic migrálva
- [ ] SQLAlchemy session dinamikus pool konfig
- [ ] Logger Factory warning logolás implementálva
- [ ] DB Factory Pydantic tesztek (5+ új teszt)
- [ ] Logger Factory valós YAML teszt (2+ új teszt)
- [ ] Core Init integrációs teszt (1+ új teszt)
- [ ] `ruff check .` tiszta
- [ ] `pytest tests/core/` 100% pass
- [ ] TASK_TREE.md frissítve
- [ ] Git commit létrehozva

---

**Készítette:** Architect Agent  
**Jóváhagyásra vár:** User review
