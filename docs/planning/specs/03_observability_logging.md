# 03 - Observability & Logging Specification

## 🎯 Cél és Filozófia

**Cél:** Intézményi szintű megfigyelhetőség (Observability) kialakítása strukturált naplózással, amely lehetővé teszi a rendszer teljes működésének nyomon követését, hibaelhárítását és teljesítményelemzését.

**Filozófia:**
- **Structured Logging:** Minden napló esemény strukturált JSON formátumban, géppel feldolgozható.
- **Context-Rich:** Minden log tartalmazza a szükséges kontextust (trace_id, component, symbol, stb.).
- **Multi-Destination:** Naplók irányítása konzolra (fejlesztés) és fájlba/DB-be (production).
- **Zero-Performance-Impact:** Aszinkron naplózás, hogy ne lassítsa a fő folyamatokat.

---

## 🏗️ Architektúra Áttekintés

### Logging Stack

```
┌─────────────────────────────────────────────┐
│          Application Components             │
│  (Collector, Strategy, Storage, EventBus)  │
└──────────────┬──────────────────────────────┘
               │
               │ structlog API
               ▼
┌─────────────────────────────────────────────┐
│         structlog (Core Logger)             │
│  - Context accumulation                      │
│  - Processor pipeline                        │
│  - Formatting                                 │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────┐    ┌──────────────┐
│ Console  │    │  File/DB     │
│ (Dev)    │    │ (Production) │
│ Color    │    │ JSON         │
└──────────┘    └──────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Log Analytics  │
              │  (Grafana, ELK) │
              └─────────────────┘
```

---

## 📚 Technológiai Stack

### Fő Könyvtárak

| Könyvtár | Verzió | Cél |
|----------|--------|-----|
| `structlog` | 23.1.0+ | Strukturált naplózás core |
| `python-json-logger` | 2.0.7+ | JSON formázás |
| `colorama` | 0.4.6+ | Konzol színezés (Windows) |

### Opcionális (jövőbeli)

| Könyvtár | Cél |
|----------|-----|
| `opentelemetry-api` | Distributed tracing |
| `prometheus-client` | Metrikák gyűjtése |
| `grafana-sdk` | Dashboard integráció |

---

## 🔧 Konfiguráció

### .env Konfiguráció

```bash
# ============================================
# LOGGING KONFIGURÁCIÓ
# ============================================
LOG_LEVEL=INFO
LOG_FORMAT=json  # json | console | both
LOG_FILE_PATH=./logs/neural_ai.log
LOG_MAX_FILE_SIZE=100MB
LOG_BACKUP_COUNT=5
LOG_ENABLE_JSON_INDENT=false
LOG_COLORED_CONSOLE=true

# ============================================
# TRACING KONFIGURÁCIÓ (jövőbeli)
# ============================================
# TRACING_ENABLED=false
# TRACING_SERVICE_NAME=neural-ai-next
# TRACING_AGENT_HOST=localhost
# TRACING_AGENT_PORT=6831
```

### Pydantic Settings

```python
from pydantic import Field, field_validator
from typing import Literal


class LoggingConfig(BaseSettings):
    """Naplózási konfiguráció."""
    
    log_level: str = Field(default='INFO')
    log_format: Literal['json', 'console', 'both'] = Field(default='json')
    log_file_path: str = Field(default='./logs/neural_ai.log')
    log_max_file_size: str = Field(default='100MB')
    log_backup_count: int = Field(default=5, ge=1, le=20)
    log_enable_json_indent: bool = Field(default=False)
    log_colored_console: bool = Field(default=True)
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid:
            raise ValueError(f'Invalid log level: {v}')
        return v.upper()
    
    @field_validator('log_max_file_size')
    @classmethod
    def validate_file_size(cls, v: str) -> str:
        # Formátum: 100MB, 1GB, 500KB
        import re
        pattern = r'^(\d+)(MB|GB|KB)$'
        if not re.match(pattern, v.upper()):
            raise ValueError(f'Invalid file size format: {v}')
        return v.upper()
```

---

## 🏗️ Logger Implementáció

### Core Logger Factory

```python
import structlog
from structlog.types import Processor, EventDict
import logging
import sys
import json
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class NeuralAILoggerFactory:
    """Neural AI Next logger factory structlog alapokon."""
    
    @staticmethod
    def configure(log_config: LoggingConfig) -> None:
        """Globális logger konfiguráció."""
        
        # Processzorok összeállítása
        processors = NeuralAILoggerFactory._get_processors(log_config)
        
        # structlog konfiguráció
        structlog.configure(
            processors=processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
            context_class=dict,
        )
        
        # Standard library logging konfiguráció
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, log_config.log_level)
        )
    
    @staticmethod
    def _get_processors(log_config: LoggingConfig) -> list[Processor]:
        """Processzor pipeline összeállítása."""
        processors = [
            # 1. Context adatok hozzáadása
            structlog.contextvars.merge_contextvars,
            
            # 2. Log level filter
            structlog.stdlib.filter_by_level,
            
            # 3. Standard library logging integráció
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            
            # 4. Időbélyeg hozzáadása
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            
            # 5. Stack info (hibákhoz)
            structlog.processors.StackInfoRenderer(),
            
            # 6. Exception formázás
            structlog.processors.format_exc_info,
            
            # 7. Unicode dekódolás
            structlog.processors.UnicodeDecoder(),
            
            # 8. Console vagy JSON formázás
            *NeuralAILoggerFactory._get_formatters(log_config),
            
            # 9. Console vagy File output
            *NeuralAILoggerFactory._get_outputs(log_config),
        ]
        
        return processors
    
    @staticmethod
    def _get_formatters(log_config: LoggingConfig) -> list[Processor]:
        """Formázók kiválasztása."""
        if log_config.log_format == 'json':
            return [
                structlog.processors.JSONRenderer(
                    serializer=json.dumps,
                    indent=2 if log_config.log_enable_json_indent else None
                )
            ]
        elif log_config.log_format == 'console':
            return [
                structlog.dev.ConsoleRenderer(
                    colors=log_config.log_colored_console
                )
            ]
        else:  # both
            # JSON a fájlba, Console a képernyőre
            return [
                structlog.processors.JSONRenderer()
            ]
    
    @staticmethod
    def _get_outputs(log_config: LoggingConfig) -> list:
        """Output kezelők."""
        # Jelenleg a structlog a stdout-ra ír
        # File output-ot külön kell kezelni
        return []
    
    @staticmethod
    def get_logger(name: str) -> structlog.BoundLogger:
        """Logger példány lekérdezése."""
        return structlog.get_logger(name)
```

---

## 📝 Logging Best Practices

### 1. Context Accumulation (Kontextus Gyűjtés)

```python
import structlog
from neural_ai.core.config import StaticConfig

logger = structlog.get_logger(__name__)

class CollectorService:
    def __init__(self, config: StaticConfig):
        self.config = config
        # Bind context adatok a loggerhez
        self.logger = logger.bind(
            component="collector.jforex",
            symbols=config.trading_symbols,
            version=config.app_version
        )
    
    async def download_tick_data(self, symbol: str, date: datetime):
        """Tick adatok letöltése."""
        
        # További context hozzáadása
        log = self.logger.bind(symbol=symbol, date=date.isoformat())
        
        log.info("download_start", message="Starting tick data download")
        
        try:
            # Letöltési logika...
            tick_count = await self._fetch_from_jforex(symbol, date)
            
            log.info(
                "download_complete",
                tick_count=tick_count,
                duration_ms=123.45
            )
            
            return tick_count
            
        except Exception as e:
            log.error(
                "download_failed",
                error=str(e),
                error_type=type(e).__name__
            )
            raise
```

### 2. Event-Driven Logging (Esemény Alapú Naplózás)

```python
from neural_ai.core.events import MarketDataEvent, EventBus

class StrategyEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.logger = structlog.get_logger("strategy.engine")
        
        # Feliratkozás eseményekre
        self.event_bus.subscribe(MarketDataEvent, self._on_market_data)
    
    async def _on_market_data(self, event: MarketDataEvent):
        """Market data esemény feldolgozása."""
        
        log = self.logger.bind(
            symbol=event.symbol,
            trace_id=event.trace_id,
            source=event.source
        )
        
        log.debug("market_data_received", bid=event.bid, ask=event.ask)
        
        # AI model futtatása
        signal = await self._run_ai_models(event)
        
        if signal:
            log.info(
                "signal_generated",
                direction=signal.direction,
                confidence=signal.confidence,
                strategy=signal.source_strategy
            )
```

### 3. Performance Monitoring (Teljesítmény Nyomon Követés)

```python
import time
from functools import wraps

def timed(logger_name: str = __name__):
    """Dekorátor metódusok időzítéséhez."""
    logger = structlog.get_logger(logger_name)
    
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            
            log = logger.bind(
                function=func.__name__,
                module=func.__module__
            )
            
            log.debug("function_start")
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                
                log.info(
                    "function_complete",
                    duration_ms=round(duration_ms, 2),
                    success=True
                )
                return result
                
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                
                log.error(
                    "function_failed",
                    duration_ms=round(duration_ms, 2),
                    error=str(e),
                    success=False
                )
                raise
        
        return async_wrapper
    return decorator


# Használat:
class StorageService:
    @timed("storage.parquet")
    async def save_tick_data(self, symbol: str, data: pd.DataFrame):
        """Tick adatok mentése Parquet formátumban."""
        # Mentési logika...
        pass
```

---

## 📊 Log Schema Definíció

### Standard Log Mezők

Minden naplóbejegyzés tartalmazza ezeket a mezőket:

```json
{
  "timestamp": "2025-12-23T20:00:00.123456Z",
  "level": "INFO",
  "event": "tick_received",
  "logger": "collector.jforex",
  "component": "collector.jforex",
  "trace_id": "abc123def456",
  "symbol": "EURUSD",
  "source": "JForex",
  "message": "Tick data received and processed"
}
```

### Komponens Specifikus Mezők

#### Collector Logs
```json
{
  "event": "download_complete",
  "symbol": "EURUSD",
  "date": "2025-12-23",
  "tick_count": 86400,
  "duration_ms": 1234.56,
  "file_size_mb": 2.5,
  "compression_ratio": 0.85
}
```

#### Strategy Logs
```json
{
  "event": "signal_generated",
  "symbol": "EURUSD",
  "direction": "LONG",
  "confidence": 0.85,
  "strategy": "hierarchical_v1",
  "model_version": "1.2.3",
  "reason": "D1+D2+D3 confluence"
}
```

#### Storage Logs
```json
{
  "event": "parquet_write",
  "symbol": "EURUSD",
  "year": 2025,
  "month": 12,
  "day": 23,
  "row_count": 86400,
  "file_path": "/data/EURUSD/tick/year=2025/month=12/day=23.parquet",
  "compression": "snappy",
  "duration_ms": 234.56
}
```

#### EventBus Logs
```json
{
  "event": "event_published",
  "event_type": "MarketDataEvent",
  "channel": "tick_data",
  "subscriber_count": 3,
  "queue_size": 150,
  "processing_time_ms": 1.23
}
```

---

## 🔍 Log Analytics és Query

### 1. JSON Log Query (jq)

```bash
# Összes ERROR szintű log kinyerése
cat logs/neural_ai.log | jq 'select(.level == "ERROR")'

# EURUSD tick adatok szűrése
cat logs/neural_ai.log | jq 'select(.symbol == "EURUSD" and .event == "tick_received")'

# Teljesítmény metrikák
cat logs/neural_ai.log | jq 'select(.duration_ms != null) | {function: .function, duration: .duration_ms}'
```

### 2. SQL Query (ha logok az adatbázisban vannak)

```sql
-- Leggyakoribb hibák
SELECT event, error, COUNT(*) as count
FROM logs
WHERE level = 'ERROR'
  AND timestamp > NOW() - INTERVAL '1 day'
GROUP BY event, error
ORDER BY count DESC
LIMIT 10;

-- Átlagos feldolgozási idő komponensenként
SELECT component, AVG(duration_ms) as avg_duration
FROM logs
WHERE duration_ms IS NOT NULL
  AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY component;

-- Jelzések statisztikája
SELECT symbol, direction, COUNT(*) as signal_count, AVG(confidence) as avg_confidence
FROM logs
WHERE event = 'signal_generated'
  AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY symbol, direction;
```

---

## 🎨 Console Output (Fejlesztői Környezet)

### Színes Console Log Format

```
2025-12-23 20:00:00 [INFO    ] collector.jforex | download_start
  symbol=EURUSD date=2025-12-23 source=JForex
2025-12-23 20:00:01 [INFO    ] collector.jforex | download_complete
  tick_count=86400 duration_ms=1234.56 file_size_mb=2.5
2025-12-23 20:00:02 [WARNING ] strategy.engine | low_confidence_signal
  symbol=EURUSD confidence=0.45 threshold=0.7
2025-12-23 20:00:03 [ERROR   ] storage.parquet | write_failed
  symbol=EURUSD error="Disk full" error_type=OSError
```

### Színkódok

- **INFO:** Kék
- **WARNING:** Sárga
- **ERROR:** Piros
- **CRITICAL:** Piros háttérrel
- **DEBUG:** Szürke

---

## 🚀 Advanced Features

### 1. Distributed Tracing (jövőbeli)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Tracing konfiguráció
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

class EventBus:
    async def publish(self, event: BaseEvent):
        with tracer.start_as_current_span("event_publish") as span:
            span.set_attribute("event.type", type(event).__name__)
            span.set_attribute("event.symbol", getattr(event, 'symbol', None))
            
            # Event publishing logic...
            log = self.logger.bind(trace_id=span.get_span_context().trace_id)
            log.info("event_published", event_type=type(event).__name__)
```

### 2. Metrics Collection (jövőbeli)

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrikák definiálása
tick_counter = Counter('tick_received_total', 'Total ticks received', ['symbol', 'source'])
processing_time = Histogram('tick_processing_seconds', 'Tick processing time')
queue_size = Gauge('eventbus_queue_size', 'EventBus queue size')

# Metrikák frissítése
class CollectorService:
    async def process_tick(self, tick: TickData):
        with processing_time.time():
            tick_counter.labels(symbol=tick.symbol, source='JForex').inc()
            
            # Feldolgozás...
            await self.event_bus.publish(tick)
```

---

## 🧪 Tesztelési Stratégia

### Unit Tesztek

```python
import pytest
import structlog

def test_logger_configuration():
    """Teszteli a logger konfigurációt."""
    config = LoggingConfig(log_format='console')
    NeuralAILoggerFactory.configure(config)
    
    logger = structlog.get_logger("test")
    logger.info("test_message", key="value")
    
    # Assert: Console output ellenőrzése (capture stdout)

def test_logger_with_context():
    """Teszteli a context accumulation-t."""
    logger = structlog.get_logger("test")
    bound_logger = logger.bind(user_id=123, session_id="abc")
    
    bound_logger.info("user_action", action="login")
    
    # Assert: Log tartalmazza a user_id és session_id mezőket
```

### Integration Tesztek

```python
@pytest.mark.asyncio
async def test_collector_logging():
    """Teszteli a collector naplózását."""
    collector = CollectorService(config)
    
    with LogCapture() as logs:
        await collector.download_tick_data("EURUSD", datetime.now())
        
        # Assert: Logok tartalmazzák a várt eseményeket
        logs.check(
            ('collector.jforex', 'INFO', 'download_start'),
            ('collector.jforex', 'INFO', 'download_complete')
        )
```

---

## 🔗 Kapcsolódó Dokumentumok

- [`01_system_architecture.md`](01_system_architecture.md) - Event-Driven architektúra
- [`02_dynamic_configuration.md`](02_dynamic_configuration.md) - Konfiguráció kezelés
- [`docs/development/core_dependencies.md`](../development/core_dependencies.md) - DI Container
- [`pyproject.toml`](../../pyproject.toml) - Függőségek