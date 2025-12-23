# 02 - Dynamic Configuration Specification

## 🎯 Cél és Filozófia

**Cél:** Hibrid konfigurációs rendszer kialakítása, amely a statikus és dinamikus beállításokat egységesen kezeli, lehetővé téve a futás közbeni módosításokat anélkül, hogy a rendszert újra kellene indítani.

**Filozófia:**
- **Layer Separation:** Statikus (környezeti) és dinamikus (üzleti) konfigurációk szétválasztása.
- **Hot Reload:** Dinamikus konfigurációk változásainak automatikus érvényesítése.
- **Database-First:** Minden üzleti logika konfigurációja az adatbázisból származik.
- **Type Safety:** Pydantic modellek garantálják a típusbiztosságot.

---

## 🏗️ Architektúra Áttekintés

### Két Rétegű Konfigurációs Modell

```
┌─────────────────────────────────────────┐
│  Layer 1: Static Configuration (.env)   │
│  - Környezeti változók                   │
│  - API kulcsok                           │
│  - Adatbázis URL-ek                      │
│  - Hardver specifikációk                 │
└──────────────┬──────────────────────────┘
               │
               │ Pydantic Settings
               ▼
┌─────────────────────────────────────────┐
│   Config Manager (Singleton)            │
│  - .env betöltés                         │
│  - Validáció                             │
│  - Cache kezelés                         │
└──────────────┬──────────────────────────┘
               │
               │
               ▼
┌─────────────────────────────────────────┐
│  Layer 2: Dynamic Configuration (DB)    │
│  - Kockázati paraméterek                 │
│  - Aktív szimbólumok                     │
│  - Stratégia beállítások                 │
│  - Collector intervallek                 │
└──────────────┬──────────────────────────┘
               │
               │ Polling / WebSocket
               ▼
┌─────────────────────────────────────────┐
│   Hot Reload Manager                    │
│  - Változás észlelés                     │
│  - Cache frissítés                       │
│  - Komponens értesítés                   │
└─────────────────────────────────────────┘
```

---

## 📋 Layer 1: Statikus Konfiguráció (.env)

### Teljes .env.example

```bash
# ============================================
# ALAP KÖRNYEZETI BEÁLLÍTÁSOK
# ============================================
APP_ENV=development
APP_NAME=Neural AI Next
APP_VERSION=1.0.0
LOG_LEVEL=INFO

# ============================================
# ADATBÁZIS KAPCSOLAT
# ============================================
# SQLite (fejlesztéshez)
DB_URL=sqlite+aiosqlite:///neural_ai.db

# PostgreSQL (production)
# DB_URL=postgresql+asyncpg://user:pass@localhost/neural_ai

# ============================================
# KERESKEDÉSI SZIMBÓLUMOK
# ============================================
# Csak a prémium instrumentumok
TRADING_SYMBOLS=["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "XAUUSD"]

# ============================================
# JFOREX API (Tick Adatok)
# ============================================
JFOREX_API_ENABLED=true
JFOREX_API_URL=https://www.dukascopy.com/datafeed
JFOREX_API_KEY=your_api_key_here
JFOREX_RATE_LIMIT=10  # requests per second
JFOREX_TIMEOUT=30  # seconds

# ============================================
# META TRADER 5 API
# ============================================
MT5_SERVER_ENABLED=true
MT5_SERVER_HOST=0.0.0.0
MT5_SERVER_PORT=8000
MT5_API_KEY=your_mt5_api_key

# ============================================
# EVENT BUS KONFIGURÁCIÓ
# ============================================
EVENT_BUS_BACKEND=asyncio  # asyncio | zeromq
EVENT_BUS_HOST=localhost
EVENT_BUS_PORT=5555
EVENT_BUS_MAX_QUEUE_SIZE=10000

# ============================================
# STORAGE (PARQUET) KONFIGURÁCIÓ
# ============================================
DATA_DIRECTORY=./data
PARQUET_COMPRESSION=snappy  # snappy | gzip | uncompressed
PARQUET_ROW_GROUP_SIZE=50000
PARQUET_WRITE_BATCH_SIZE=10000

# ============================================
# AI MODEL KONFIGURÁCIÓ
# ============================================
TORCH_DEVICE=cuda  # cuda | cpu
TORCH_CUDA_DEVICE=0
MODEL_BATCH_SIZE=32
MODEL_CACHE_DIR=./models

# ============================================
# STRATÉGIA KONFIGURÁCIÓ
# ============================================
STRATEGY_ENABLED=true
STRATEGY_BACKTEST_MODE=false
STRATEGY_LIVE_TRADING=false  # ÓVATOSAN!

# ============================================
# RISK MANAGEMENT ALAPÉRTÉKEK
# ============================================
RISK_DEFAULT_MAX_PERCENT=0.02  # 2%
RISK_DEFAULT_MIN_RR_RATIO=1.5
RISK_DEFAULT_ATR_MULTIPLIER=1.5

# ============================================
# OBSERVABILITY (LOGOLÁS ÉS METRIKÁK)
# ============================================
LOG_FORMAT=json  # json | console
LOG_FILE_PATH=./logs/neural_ai.log
LOG_MAX_FILE_SIZE=100MB
LOG_BACKUP_COUNT=5

# METRICS_ENABLED=true
# METRICS_PORT=9090

# ============================================
# FEJLESZTŐI BEÁLLÍTÁSOK
# ============================================
DEBUG_MODE=false
ENABLE_PROFILING=false
ENABLE_CORS=true
```

### Pydantic Settings Modell

```python
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class StaticConfig(BaseSettings):
    """Statikus konfiguráció betöltése .env fájlból."""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    
    # Alap beállítások
    app_env: str = Field(default='development')
    app_name: str = Field(default='Neural AI Next')
    app_version: str = Field(default='1.0.0')
    log_level: str = Field(default='INFO')
    
    # Adatbázis
    db_url: str = Field(
        default='sqlite+aiosqlite:///neural_ai.db',
        description='Database connection URL'
    )
    
    # Kereskedési szimbólumok
    trading_symbols: List[str] = Field(
        default=['EURUSD', 'XAUUSD'],
        description='Aktív kereskedési párok'
    )
    
    # JForex API
    jforex_api_enabled: bool = Field(default=True)
    jforex_api_url: str = Field(default='https://www.dukascopy.com/datafeed')
    jforex_api_key: Optional[str] = None
    jforex_rate_limit: int = Field(default=10, ge=1, le=100)
    jforex_timeout: int = Field(default=30, ge=5, le=60)
    
    # MT5 API
    mt5_server_enabled: bool = Field(default=True)
    mt5_server_host: str = Field(default='0.0.0.0')
    mt5_server_port: int = Field(default=8000, ge=1024, le=65535)
    mt5_api_key: Optional[str] = None
    
    # Event Bus
    event_bus_backend: str = Field(default='asyncio')
    event_bus_host: str = Field(default='localhost')
    event_bus_port: int = Field(default=5555, ge=1024, le=65535)
    event_bus_max_queue_size: int = Field(default=10000, ge=1000)
    
    # Storage
    data_directory: str = Field(default='./data')
    parquet_compression: str = Field(default='snappy')
    parquet_row_group_size: int = Field(default=50000, ge=1000)
    parquet_write_batch_size: int = Field(default=10000, ge=1000)
    
    # AI Model
    torch_device: str = Field(default='cuda')
    torch_cuda_device: int = Field(default=0, ge=0)
    model_batch_size: int = Field(default=32, ge=1, le=1024)
    model_cache_dir: str = Field(default='./models')
    
    # Stratégia
    strategy_enabled: bool = Field(default=True)
    strategy_backtest_mode: bool = Field(default=False)
    strategy_live_trading: bool = Field(default=False)
    
    # Risk Management
    risk_default_max_percent: float = Field(
        default=0.02,
        ge=0.001,
        le=0.1,
        description='Default maximum risk per trade (2%)'
    )
    risk_default_min_rr_ratio: float = Field(
        default=1.5,
        ge=1.0,
        le=5.0
    )
    risk_default_atr_multiplier: float = Field(
        default=1.5,
        ge=0.5,
        le=5.0
    )
    
    # Logging
    log_format: str = Field(default='json')
    log_file_path: str = Field(default='./logs/neural_ai.log')
    log_max_file_size: str = Field(default='100MB')
    log_backup_count: int = Field(default=5, ge=1)
    
    # Fejlesztői
    debug_mode: bool = Field(default=False)
    enable_profiling: bool = Field(default=False)
    enable_cors: bool = Field(default=True)
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Invalid log level. Must be one of: {valid_levels}')
        return v.upper()
    
    @field_validator('parquet_compression')
    @classmethod
    def validate_compression(cls, v: str) -> str:
        valid_types = ['snappy', 'gzip', 'uncompressed']
        if v.lower() not in valid_types:
            raise ValueError(f'Invalid compression. Must be one of: {valid_types}')
        return v.lower()
    
    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == 'production'
    
    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == 'development'
```

---

## 📊 Layer 2: Dinamikus Konfiguráció (Adatbázis)

### Adatbázis Schema

```sql
-- ============================================
-- DINAMIKUS KONFIGURÁCIÓS TÁBLA
-- ============================================
CREATE TABLE config_dynamic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value JSON NOT NULL,
    value_type TEXT NOT NULL,  -- 'int', 'float', 'str', 'bool', 'list', 'dict'
    category TEXT NOT NULL,    -- 'risk', 'trading', 'strategy', 'collector', 'system'
    description TEXT,
    min_value JSON,            -- Validációhoz (opcionális)
    max_value JSON,            -- Validációhoz (opcionális)
    allowed_values JSON,       -- Enum értékek (opcionális)
    is_hot_reloadable BOOLEAN DEFAULT TRUE,
    updated_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_config_category ON config_dynamic(category);
CREATE INDEX idx_config_hot_reload ON config_dynamic(is_hot_reloadable);

-- ============================================
-- KONFIGURÁCIÓS VÁLTOZÁSOK NAPLÓJA
-- ============================================
CREATE TABLE config_change_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT NOT NULL,
    old_value JSON,
    new_value JSON,
    changed_by TEXT NOT NULL,
    change_reason TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (config_key) REFERENCES config_dynamic(key)
);

CREATE INDEX idx_change_log_key ON config_change_log(config_key);
CREATE INDEX idx_change_log_timestamp ON config_change_log(changed_at DESC);
```

### Alapértelmezett Konfigurációk

```sql
-- ============================================
-- RISK MANAGEMENT KONFIGURÁCIÓK
-- ============================================
INSERT INTO config_dynamic (key, value, value_type, category, description, is_hot_reloadable) VALUES
('risk.max_percent_per_trade', '0.02', 'float', 'risk', 'Maximum kockázat egy kereskedésre (2%)', TRUE),
('risk.max_daily_loss', '0.05', 'float', 'risk', 'Maximum napi veszteség (5%)', TRUE),
('risk.min_risk_reward_ratio', '1.5', 'float', 'risk', 'Minimum kockázat/nyereség arány', TRUE),
('risk.atr_stop_multiplier', '1.5', 'float', 'risk', 'ATR alapú stop loss szorzó', TRUE),
('risk.max_open_positions', '5', 'int', 'risk', 'Maximum egyidejű nyitott pozíciók', TRUE),
('risk.position_sizing_method', 'fixed_fractional', 'str', 'risk', 'Pozíció méretezési módszer', TRUE);

-- ============================================
-- TRADING KONFIGURÁCIÓK
-- ============================================
INSERT INTO config_dynamic (key, value, value_type, category, description, is_hot_reloadable) VALUES
('trading.active_symbols', '["EURUSD", "XAUUSD"]', 'list', 'trading', 'Aktív kereskedési szimbólumok', TRUE),
('trading.session_filter', 'all', 'str', 'trading', 'Kereskedési szession szűrő', TRUE),
('trading.max_trades_per_day', '10', 'int', 'trading', 'Maximum kereskedések száma naponta', TRUE),
('trading.min_volume_threshold', '0.8', 'float', 'trading', 'Minimum volumen küszöb', TRUE),
('trading.max_spread_ratio', '0.0003', 'float', 'trading', 'Maximum spread arány', TRUE);

-- ============================================
-- STRATÉGIA KONFIGURÁCIÓK
-- ============================================
INSERT INTO config_dynamic (key, value, value_type, category, description, is_hot_reloadable) VALUES
('strategy.enabled', 'true', 'bool', 'strategy', 'Stratégia engedélyezve', TRUE),
('strategy.name', 'hierarchical_v1', 'str', 'strategy', 'Aktív stratégia neve', FALSE),
('strategy.confidence_threshold', '0.7', 'float', 'strategy', 'Minimum bizonyossági küszöb', TRUE),
('strategy.max_signals_per_hour', '3', 'int', 'strategy', 'Maximum jelzés óránként', TRUE),
('strategy.required_confirmations', '2', 'int', 'strategy', 'Szükséges megerősítések száma', TRUE);

-- ============================================
-- COLLECTOR KONFIGURÁCIÓK
-- ============================================
INSERT INTO config_dynamic (key, value, value_type, category, description, is_hot_reloadable) VALUES
('collector.jforex.enabled', 'true', 'bool', 'collector', 'JForex collector engedélyezve', TRUE),
('collector.jforex.interval_seconds', '60', 'int', 'collector', 'Letöltési intervallum', TRUE),
('collector.jforex.lookback_days', '7', 'int', 'collector', 'Visszatekintési napok', TRUE),
('collector.mt5.enabled', 'true', 'bool', 'collector', 'MT5 collector engedélyezve', TRUE),
('collector.mt5.port', '8000', 'int', 'collector', 'MT5 API port', FALSE);

-- ============================================
-- RENDSZER KONFIGURÁCIÓK
-- ============================================
INSERT INTO config_dynamic (key, value, value_type, category, description, is_hot_reloadable) VALUES
('system.data_retention_days', '365', 'int', 'system', 'Adatmegőrzési időtartam napokban', FALSE),
('system.cleanup_interval_hours', '24', 'int', 'system', 'Takarítási intervallum', TRUE),
('system.performance_monitoring', 'true', 'bool', 'system', 'Teljesítmény monitorozás', TRUE);
```

---

## 🔄 Hot Reload Mechanizmus

### Konfiguráció Manager Implementáció

```python
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import json
from datetime import datetime
import structlog

logger = structlog.get_logger()


class DynamicConfigManager:
    """Dinamikus konfigurációk kezelése hot reload-al."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.cache: Dict[str, Any] = {}
        self.last_update: Optional[datetime] = None
        self.subscribers: Dict[str, list] = {}  # key -> [callback functions]
        self.running = False
        
    async def initialize(self):
        """Kezdeti konfiguráció betöltése."""
        logger.info("dynamic_config_initialize_start")
        
        query = select(ConfigDynamic)
        result = await self.db.execute(query)
        configs = result.scalars().all()
        
        for config in configs:
            self.cache[config.key] = self._parse_value(config)
        
        self.last_update = datetime.utcnow()
        logger.info("dynamic_config_initialize_complete", count=len(self.cache))
    
    def _parse_value(self, config: ConfigDynamic) -> Any:
        """JSON érték feldolgozása a value_type alapján."""
        raw_value = json.loads(config.value)
        
        type_mapping = {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict
        }
        
        try:
            return type_mapping[config.value_type](raw_value)
        except (ValueError, KeyError) as e:
            logger.error(
                "dynamic_config_parse_error",
                key=config.key,
                value=raw_value,
                expected_type=config.value_type,
                error=str(e)
            )
            return raw_value
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Konfiguráció lekérdezése a cache-ből."""
        return self.cache.get(key, default)
    
    async def set(self, key: str, value: Any, updated_by: str, reason: str = None):
        """Konfiguráció frissítése (adminisztratív)."""
        # Validáció
        if key not in self.cache:
            raise ValueError(f"Unknown config key: {key}")
        
        # Érték frissítése az adatbázisban
        query = select(ConfigDynamic).where(ConfigDynamic.key == key)
        result = await self.db.execute(query)
        config = result.scalar_one_or_none()
        
        if not config:
            raise ValueError(f"Config not found: {key}")
        
        # Változás naplózása
        old_value = self.cache[key]
        await self._log_change(key, old_value, value, updated_by, reason)
        
        # Adatbázis frissítés
        config.value = json.dumps(value)
        config.updated_at = datetime.utcnow()
        config.updated_by = updated_by
        await self.db.commit()
        
        # Cache frissítés
        self.cache[key] = value
        self.last_update = datetime.utcnow()
        
        # Értesítés a feliratkozóknak
        await self._notify_subscribers(key, old_value, value)
        
        logger.info(
            "dynamic_config_updated",
            key=key,
            old_value=old_value,
            new_value=value,
            updated_by=updated_by
        )
    
    def subscribe(self, key: str, callback):
        """Feliratkozás konfiguráció változásaira."""
        if key not in self.subscribers:
            self.subscribers[key] = []
        self.subscribers[key].append(callback)
        logger.debug("dynamic_config_subscribed", key=key, callback=str(callback))
    
    def unsubscribe(self, key: str, callback):
        """Leiratkozás konfiguráció változásairól."""
        if key in self.subscribers:
            try:
                self.subscribers[key].remove(callback)
                logger.debug("dynamic_config_unsubscribed", key=key)
            except ValueError:
                pass
    
    async def _notify_subscribers(self, key: str, old_value: Any, new_value: Any):
        """Értesítés küldése a feliratkozóknak."""
        if key not in self.subscribers:
            return
        
        for callback in self.subscribers[key]:
            try:
                await callback(key, old_value, new_value)
            except Exception as e:
                logger.error(
                    "dynamic_config_callback_error",
                    key=key,
                    callback=str(callback),
                    error=str(e)
                )
    
    async def _log_change(self, key: str, old_value: Any, new_value: Any, 
                         updated_by: str, reason: str = None):
        """Változás naplózása."""
        change_log = ConfigChangeLog(
            config_key=key,
            old_value=json.dumps(old_value),
            new_value=json.dumps(new_value),
            changed_by=updated_by,
            change_reason=reason
        )
        self.db.add(change_log)
    
    async def start_watching(self, interval_seconds: int = 5):
        """Változások figyelése az adatbázisban (polling)."""
        self.running = True
        logger.info("dynamic_config_watcher_started", interval=interval_seconds)
        
        while self.running:
            try:
                await asyncio.sleep(interval_seconds)
                await self._check_for_changes()
            except asyncio.CancelledError:
                logger.info("dynamic_config_watcher_cancelled")
                break
            except Exception as e:
                logger.error("dynamic_config_watcher_error", error=str(e))
                await asyncio.sleep(10)  # Várakozás hiba esetén
    
    async def stop_watching(self):
        """Figyelés leállítása."""
        self.running = False
        logger.info("dynamic_config_watcher_stopped")
    
    async def _check_for_changes(self):
        """Ellenőrzi az adatbázis változásokat."""
        if not self.last_update:
            return
        
        query = select(ConfigDynamic).where(
            ConfigDynamic.updated_at > self.last_update,
            ConfigDynamic.is_hot_reloadable == True
        )
        result = await self.db.execute(query)
        changed_configs = result.scalars().all()
        
        for config in changed_configs:
            old_value = self.cache.get(config.key)
            new_value = self._parse_value(config)
            
            if old_value != new_value:
                self.cache[config.key] = new_value
                await self._notify_subscribers(config.key, old_value, new_value)
                logger.info(
                    "dynamic_config_hot_reloaded",
                    key=config.key,
                    old_value=old_value,
                    new_value=new_value
                )
        
        self.last_update = datetime.utcnow()
```

---

## 🔧 Használati Példák

### 1. Statikus Konfiguráció Betöltése

```python
from docs.planning.specs.config_schema import StaticConfig

# .env fájl betöltése
config = StaticConfig()

print(f"App Environment: {config.app_env}")
print(f"Database URL: {config.db_url}")
print(f"Active Symbols: {config.trading_symbols}")

if config.is_production:
    print("Running in PRODUCTION mode")
```

### 2. Dinamikus Konfiguráció Használata

```python
from docs.planning.specs.config_manager import DynamicConfigManager

# Inicializálás
config_manager = DynamicConfigManager(db_session)
await config_manager.initialize()

# Érték lekérdezése
max_risk = await config_manager.get('risk.max_percent_per_trade', 0.02)
active_symbols = await config_manager.get('trading.active_symbols', [])

print(f"Max Risk: {max_risk * 100}%")
print(f"Active Symbols: {active_symbols}")
```

### 3. Hot Reload - Stratégia Komponens

```python
class StrategyEngine:
    def __init__(self, config_manager: DynamicConfigManager):
        self.config = config_manager
        self.max_risk = 0.02
        self.confidence_threshold = 0.7
        
        # Feliratkozás a konfiguráció változásokra
        self.config.subscribe('risk.max_percent_per_trade', self._on_risk_changed)
        self.config.subscribe('strategy.confidence_threshold', self._on_threshold_changed)
    
    async def _on_risk_changed(self, key: str, old_value: float, new_value: float):
        """Kockázati limit változás kezelése."""
        logger.info("strategy_risk_limit_changed", old=old_value, new=new_value)
        self.max_risk = new_value
        
        # Új kockázati limit alkalmazása a nyitott pozíciókra
        await self._recalculate_position_sizes()
    
    async def _on_threshold_changed(self, key: str, old_value: float, new_value: float):
        """Bizonyossági küszöb változás kezelése."""
        logger.info("strategy_confidence_threshold_changed", old=old_value, new=new_value)
        self.confidence_threshold = new_value
```

### 4. Konfiguráció Frissítése (Adminisztratív)

```python
# Risk limit emelése futás közben
await config_manager.set(
    key='risk.max_percent_per_trade',
    value=0.03,  # 2% -> 3%
    updated_by='admin',
    reason='Increased risk tolerance based on performance'
)

# Automatikusan:
# 1. Frissül az adatbázisban
# 2. Cache-be kerül az új érték
# 3. Minden feliratkozó komponens értesítést kap
# 4. A StrategyEngine automatikusan alkalmazza az új limitet
```

---

## 🧪 Tesztelési Stratégia

### Unit Tesztek

```python
import pytest
from pytest_asyncio import fixture

@fixture
async def config_manager():
    manager = DynamicConfigManager(test_db_session)
    await manager.initialize()
    return manager

@pytest.mark.asyncio
async def test_config_initialization(config_manager):
    """Teszteli a konfiguráció inicializálását."""
    assert len(config_manager.cache) > 0
    assert config_manager.last_update is not None

@pytest.mark.asyncio
async def test_config_get(config_manager):
    """Teszteli az érték lekérdezést."""
    value = await config_manager.get('risk.max_percent_per_trade')
    assert value == 0.02

@pytest.mark.asyncio
async def test_config_set_and_notify(config_manager):
    """Teszteli az érték frissítést és értesítést."""
    callback_called = False
    old_val = None
    new_val = None
    
    async def test_callback(key, old, new):
        nonlocal callback_called, old_val, new_val
        callback_called = True
        old_val = old
        new_val = new
    
    config_manager.subscribe('risk.max_percent_per_trade', test_callback)
    
    await config_manager.set(
        key='risk.max_percent_per_trade',
        value=0.03,
        updated_by='test'
    )
    
    assert callback_called
    assert old_val == 0.02
    assert new_val == 0.03
```

---

## 🔗 Kapcsolódó Dokumentumok

- [`01_system_architecture.md`](01_system_architecture.md) - Event-Driven architektúra
- [`03_observability_logging.md`](03_observability_logging.md) - Naplózási konfiguráció
- [`docs/development/core_dependencies.md`](../development/core_dependencies.md) - DI Container használata