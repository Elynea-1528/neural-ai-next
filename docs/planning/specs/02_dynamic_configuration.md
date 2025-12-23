# 02 - Dinamikus Konfiguráció (Hybrid Config System)

## 🎯 Cél és Szándék

Ez a dokumentum definiálja a **Neural AI Next** hibrid konfigurációs rendszerét, amely két rétegből áll: statikus `.env` fájl és dinamikus SQL adatbázis. A rendszer lehetővé teszi a futás közbeni konfiguráció módosítását anélkül, hogy újra kellene indítani az alkalmazást.

**Filozófia:** *"Static for environment, Dynamic for strategy"*

---

## 🏗️ Architektúra Áttekintés

### Két Rétegű Konfiguráció

```
┌─────────────────────────────────────────┐
│         CONFIGURATION LAYERS            │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────┐      │
│  │   LAYER 1: STATIC CONFIG     │      │
│  │   (.env file)                │      │
│  │   - DB URL                   │      │
│  │   - API Keys                 │      │
│  │   - Log Level                │      │
│  │   - Environment              │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│                 │ Bootstrap             │
│                 ▼                       │
│  ┌──────────────────────────────┐      │
│  │   LAYER 2: DYNAMIC CONFIG    │      │
│  │   (SQL Database)             │      │
│  │   - Risk %                   │      │
│  │   - Active Pairs             │      │
│  │   - Strategy Params          │      │
│  │   - Position Sizes           │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│                 │ Hot Reload            │
│                 ▼                       │
│  ┌──────────────────────────────┐      │
│  │   APPLICATION                │      │
│  │   (Real-time consumption)    │      │
│  └──────────────────────────────┘      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📦 Layer 1: Statikus Konfiguráció (.env)

### Cél

A környezetfüggő, ritkán változó beállítások tárolása. Ezek a beállítások csak alkalmazás indításkor olvashatók be.

### .env.example

```bash
# ============================================
# NEURAL AI NEXT - ENVIRONMENT CONFIGURATION
# ============================================

# Application Environment
APP_ENV=development
# Options: development, staging, production

# Logging Configuration
LOG_LEVEL=INFO
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Database Configuration
DB_URL=sqlite+aiosqlite:///neural_ai.db
# Production: postgresql+asyncpg://user:pass@localhost/neural_ai

# Broker Configuration
TRADING_SYMBOLS=["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "USDCHF"]
# Only premium instruments (High Liquidity, Low Spread)

# JForex Configuration
JFOREX_USERNAME=your_username
JFOREX_PASSWORD=your_password_encrypted
JFOREX_API_URL=https://www.dukascopy.com/api

# MT5 Configuration
MT5_SERVER=YourBrokerServer
MT5_LOGIN=1234567
MT5_PASSWORD=your_password_encrypted
MT5_WEB_API_URL=http://localhost:8080/api/v1

# IBKR Configuration (Future)
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1

# Data Storage
DATA_BASE_PATH=/data/tick
# Absolute path for tick data storage

# Redis Configuration (Caching)
REDIS_URL=redis://localhost:6379/0

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your-secret-key-here

# ZeroMQ Configuration
ZMQ_EVENTBUS_PORT=5555
ZMQ_PUB_SUB_PORT=5556

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
PROMETHEUS_PORT=9090

# AI/ML Configuration
PYTORCH_DEVICE=cuda
# Options: cuda, cpu, mps
CUDA_DEVICE=0
# GPU device index

# Backtesting
BACKTEST_DATA_PATH=/data/backtest
VECTORBT_CACHE_SIZE=10000
```

### Pydantic Settings Osztály

```python
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from typing import List
import json

class StaticConfig(BaseSettings):
    """Statikus konfiguráció Pydantic modelje."""
    
    # Application
    app_env: str = Field(default="development", env="APP_ENV")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database
    db_url: str = Field(
        default="sqlite+aiosqlite:///neural_ai.db",
        env="DB_URL"
    )
    
    # Trading
    trading_symbols: List[str] = Field(
        default=["EURUSD", "XAUUSD"],
        env="TRADING_SYMBOLS"
    )
    
    @validator('trading_symbols', pre=True)
    def parse_trading_symbols(cls, v):
        """JSON stringből listát alakít."""
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    # JForex
    jforex_username: str = Field(env="JFOREX_USERNAME")
    jforex_password: str = Field(env="JFOREX_PASSWORD")
    jforex_api_url: str = Field(
        default="https://www.dukascopy.com/api",
        env="JFOREX_API_URL"
    )
    
    # MT5
    mt5_server: str = Field(env="MT5_SERVER")
    mt5_login: int = Field(env="MT5_LOGIN")
    mt5_password: str = Field(env="MT5_PASSWORD")
    mt5_web_api_url: str = Field(
        default="http://localhost:8080/api/v1",
        env="MT5_WEB_API_URL"
    )
    
    # Data
    data_base_path: str = Field(
        default="/data/tick",
        env="DATA_BASE_PATH"
    )
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_secret_key: str = Field(env="API_SECRET_KEY")
    
    # ZeroMQ
    zmq_eventbus_port: int = Field(default=5555, env="ZMQ_EVENTBUS_PORT")
    zmq_pub_sub_port: int = Field(default=5556, env="ZMQ_PUB_SUB_PORT")
    
    # AI/ML
    pytorch_device: str = Field(default="cuda", env="PYTORCH_DEVICE")
    cuda_device: int = Field(default=0, env="CUDA_DEVICE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
```

**Függőségek:** `pydantic`, `pydantic-settings`, `python-dotenv`

---

## 📦 Layer 2: Dinamikus Konfiguráció (SQL Database)

### Cél

A futás közben változtatható beállítások tárolása. Ezek a beállítások "Hot Reload" támogatással rendelkeznek, azaz az alkalmazás azonnal érzékeli a változásokat anélkül, hogy újra kellene indítani.

### Adatbázis Schema

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DynamicConfig(Base):
    """Dinamikus konfiguráció táblája."""
    
    __tablename__ = 'dynamic_config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=False)
    value_type = Column(String(50), nullable=False)
    # Options: 'int', 'float', 'str', 'bool', 'list', 'dict'
    
    category = Column(String(100), nullable=False, index=True)
    # Options: 'risk', 'strategy', 'trading', 'system'
    
    description = Column(String(1000))
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DynamicConfig(key='{self.key}', value={self.value})>"
```

### Alap Konfigurációk

```python
DEFAULT_DYNAMIC_CONFIGS = [
    {
        'key': 'risk.max_position_size_percent',
        'value': 2.0,
        'value_type': 'float',
        'category': 'risk',
        'description': 'Maximum pozícióméret a portfólió százalékában'
    },
    {
        'key': 'risk.max_daily_loss_percent',
        'value': 5.0,
        'value_type': 'float',
        'category': 'risk',
        'description': 'Maximum napi veszteség százalékban'
    },
    {
        'key': 'risk.global_risk_multiplier',
        'value': 1.0,
        'value_type': 'float',
        'category': 'risk',
        'description': 'Globális kockázat szorzó (0.5 = félkockázat, 2.0 = dupla kockázat)'
    },
    {
        'key': 'trading.active_symbols',
        'value': ['EURUSD', 'XAUUSD', 'GBPUSD'],
        'value_type': 'list',
        'category': 'trading',
        'description': 'Aktív kereskedési szimbólumok listája'
    },
    {
        'key': 'trading.trading_hours_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'trading',
        'description': 'Kereskedési órák figyelembe vétele'
    },
    {
        'key': 'trading.session_break_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'trading',
        'description': 'Session break-ek figyelembe vétele'
    },
    {
        'key': 'strategy.d1_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'strategy',
        'description': 'D1 Alap adatok processzor engedélyezése'
    },
    {
        'key': 'strategy.d2_support_resistance_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'strategy',
        'description': 'D2 Support/Resistance processzor engedélyezése'
    },
    {
        'key': 'strategy.d3_trend_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'strategy',
        'description': 'D3 Trend processzor engedélyezése'
    },
    {
        'key': 'strategy.d15_risk_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'strategy',
        'description': 'D15 Kockázatkezelés processzor engedélyezése'
    },
    {
        'key': 'system.data_collection_enabled',
        'value': True,
        'value_type': 'bool',
        'category': 'system',
        'description': 'Adatgyűjtés engedélyezése'
    },
    {
        'key': 'system.auto_restart_on_error',
        'value': True,
        'value_type': 'bool',
        'category': 'system',
        'description': 'Automatikus újraindítás hiba esetén'
    },
]
```

### DynamicConfigManager Osztály

```python
from typing import Any, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

class DynamicConfigManager:
    """Dinamikus konfiguráció kezelő."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self._cache: Dict[str, Any] = {}
        self._listeners: List[Callable] = []
        self._last_update: Optional[datetime] = None
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Konfigurációs érték lekérdezése."""
        # Először cache-ből próbálkozunk
        if key in self._cache:
            return self._cache[key]
        
        # Adatbázisból olvasás
        stmt = select(DynamicConfig).where(
            DynamicConfig.key == key,
            DynamicConfig.is_active == True
        )
        result = await self.session.execute(stmt)
        config = result.scalar_one_or_none()
        
        if config is None:
            return default
        
        # Cache-be mentés
        self._cache[key] = config.value
        return config.value
    
    async def set(self, key: str, value: Any, **kwargs) -> None:
        """Konfigurációs érték beállítása."""
        # Érték típusának meghatározása
        value_type = type(value).__name__
        
        # Létezik-e már a konfig?
        stmt = select(DynamicConfig).where(DynamicConfig.key == key)
        result = await self.session.execute(stmt)
        config = result.scalar_one_or_none()
        
        if config is None:
            # Új konfig létrehozása
            config = DynamicConfig(
                key=key,
                value=value,
                value_type=value_type,
                **kwargs
            )
            self.session.add(config)
        else:
            # Meglévő konfig frissítése
            config.value = value
            config.value_type = value_type
            for k, v in kwargs.items():
                setattr(config, k, v)
        
        await self.session.commit()
        
        # Cache frissítése
        self._cache[key] = value
        
        # Esemény küldése a listener-eknek
        await self._notify_listeners(key, value)
    
    async def get_all(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Összes konfiguráció lekérdezése."""
        stmt = select(DynamicConfig).where(DynamicConfig.is_active == True)
        if category:
            stmt = stmt.where(DynamicConfig.category == category)
        
        result = await self.session.execute(stmt)
        configs = result.scalars().all()
        
        return {c.key: c.value for c in configs}
    
    def add_listener(self, callback: Callable[[str, Any], Awaitable[None]]) -> None:
        """Listener hozzáadása konfiguráció változásokhoz."""
        self._listeners.append(callback)
    
    async def _notify_listeners(self, key: str, value: Any) -> None:
        """Listener-ek értesítése konfiguráció változásról."""
        for listener in self._listeners:
            try:
                await listener(key, value)
            except Exception as e:
                # Log error but don't crash
                logger.error(f"Config listener error: {e}")
    
    async def start_hot_reload(self, interval: int = 5) -> None:
        """Hot reload indítása (háttérben fut)."""
        while True:
            try:
                await self._check_for_updates()
            except Exception as e:
                logger.error(f"Hot reload error: {e}")
            
            await asyncio.sleep(interval)
    
    async def _check_for_updates(self) -> None:
        """Ellenőrzi, hogy történt-e változás az adatbázisban."""
        if self._last_update is None:
            # Első alkalommal betöltjük az összeset
            self._cache = await self.get_all()
            self._last_update = datetime.utcnow()
            return
        
        # Utolsó frissítés időpontja után változott-e valami?
        stmt = select(DynamicConfig).where(
            DynamicConfig.updated_at > self._last_update
        )
        result = await self.session.execute(stmt)
        updated_configs = result.scalars().all()
        
        for config in updated_configs:
            old_value = self._cache.get(config.key)
            if old_value != config.value:
                self._cache[config.key] = config.value
                await self._notify_listeners(config.key, config.value)
        
        self._last_update = datetime.utcnow()
```

**Függőségek:** `sqlalchemy`, `aiosqlite` (vagy `asyncpg` productionban)

---

## 🔄 Hot Reload Mechanizmus

### Koncepció

A Hot Reload lehetővé teszi, hogy a konfiguráció változásait az alkalmazás azonnal érzékelje anélkül, hogy újra kellene indítani. Ez különösen fontos a következő esetekben:

- Kockázati paraméterek módosítása
- Aktív szimbólumok váltása
- Stratégia paraméterek finomhangolása

### Implementáció

```python
import asyncio
from typing import Dict, Any

class ConfigReloader:
    """Konfiguráció Hot Reload kezelő."""
    
    def __init__(self, config_manager: DynamicConfigManager):
        self.config_manager = config_manager
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Hot reload indítása."""
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(
                self.config_manager.start_hot_reload(interval=5)
            )
            logger.info("Config Hot Reload started")
    
    async def stop(self) -> None:
        """Hot reload leállítása."""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            logger.info("Config Hot Reload stopped")
    
    def add_config_listener(
        self,
        key: str,
        callback: Callable[[Any], Awaitable[None]]
    ) -> None:
        """Listener hozzáadása specifikus konfigurációs kulcshoz."""
        async def listener(k: str, v: Any) -> None:
            if k == key:
                await callback(v)
        
        self.config_manager.add_listener(listener)
```

### Példa: Risk Manager Hot Reload

```python
class RiskManager:
    """Kockázatkezelő, ami reagál a konfiguráció változásaira."""
    
    def __init__(self, config_manager: DynamicConfigManager):
        self.config_manager = config_manager
        self.max_position_size = 2.0  # Default
        
        # Listener regisztrálása
        config_manager.add_listener(self._on_config_change)
    
    async def _on_config_change(self, key: str, value: Any) -> None:
        """Konfiguráció változás kezelése."""
        if key == 'risk.max_position_size_percent':
            self.max_position_size = float(value)
            logger.info(f"Max position size updated to {value}%")
        
        elif key == 'risk.global_risk_multiplier':
            # Azonnal érvényesüljön a kockázati szorzó
            await self.recalculate_all_positions()
            logger.info(f"Global risk multiplier updated to {value}")
    
    async def recalculate_all_positions(self) -> None:
        """Összes pozíció újraszámolása."""
        # Implementáció...
        pass
```

---

## 🖥️ Jövőbeli GUI Integráció

### Koncepció

A jövőben tervezett webes felület (React/Vue.js) közvetlenül az adatbázist fogja írni, az alkalmazás pedig onnan olvassa a változásokat Hot Reload segítségével.

### API Végpontok (Tervezés alatt)

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/config")

class ConfigUpdateRequest(BaseModel):
    value: Any
    description: Optional[str] = None

@router.get("/{key}")
async def get_config(key: str, manager: DynamicConfigManager = Depends()):
    """Konfiguráció lekérdezése."""
    value = await manager.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return {"key": key, "value": value}

@router.put("/{key}")
async def update_config(
    key: str,
    request: ConfigUpdateRequest,
    manager: DynamicConfigManager = Depends()
):
    """Konfiguráció frissítése."""
    await manager.set(key, request.value, description=request.description)
    return {"key": key, "value": request.value}

@router.get("/category/{category}")
async def get_configs_by_category(
    category: str,
    manager: DynamicConfigManager = Depends()
):
    """Összes konfiguráció lekérdezése kategóriából."""
    configs = await manager.get_all(category=category)
    return configs
```

---

## 🔐 Biztonság

### Jelszavak és API Kulcsok

A `.env` fájlban tárolt érzékeny adatok (jelszavak, API kulcsok) titkosítva tárolódnak:

```python
from cryptography.fernet import Fernet
import base64

class SecureConfig:
    """Titkosított konfiguráció kezelő."""
    
    def __init__(self, encryption_key: str):
        self.cipher = Fernet(encryption_key.encode())
    
    def encrypt(self, value: str) -> str:
        """Érték titkosítása."""
        encrypted = self.cipher.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_value: str) -> str:
        """Érték visszafejtése."""
        encrypted = base64.urlsafe_b64decode(encrypted_value.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()
```

**Függőség:** `cryptography`

---

## 📋 Következő Lépések

1. **Logging:** Lásd [`03_observability_logging.md`](03_observability_logging.md)
2. **Adattárolás:** Lásd [`04_data_warehouse.md`](04_data_warehouse.md)
3. **Collectorok:** Lásd [`05_collectors_strategy.md`](05_collectors_strategy.md)

---

## 🔗 Kapcsolódó Dokumentumok

- [Rendszerarchitektúra](01_system_architecture.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)
- [Core Dependencies](docs/development/core_dependencies.md)