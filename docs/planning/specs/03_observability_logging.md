# 03 - Megfigyelhetőség és Logolás (Observability & Logging)

## 🎯 Cél és Szándék

Ez a dokumentum definiálja a **Neural AI Next** strukturált logolási és megfigyelhetőségi rendszerét. A rendszer `structlog`-ot használ JSON formátumban a fájlba/adatbázisba íráshoz, és színes konzol kimenethez a fejlesztés során.

**Filozófia:** *"Every log tells a story with context"*

---

## 🏗️ Architektúra Áttekintés

### Logolási Rétegek

```
┌─────────────────────────────────────────┐
│         LOGGING ARCHITECTURE            │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────┐      │
│  │   APPLICATION LOGS           │      │
│  │   - structlog (JSON)         │      │
│  │   - Context: trace_id,       │      │
│  │     component, symbol        │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│                 ├───────────────────────┤
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   OUTPUT TARGETS             │      │
│  ├──────────────────────────────┤      │
│  │ 1. Console (Color)           │      │
│  │ 2. File (JSON)               │      │
│  │ 3. Database (SQL)            │      │
│  │ 4. Sentry (Errors)           │      │
│  └──────────────────────────────┘      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📦 Technológiai Stack

### Fő Függőségek

```python
# pyproject.toml
dependencies = [
    "structlog>=23.1.0",
    "python-json-logger>=2.0.7",
    "sentry-sdk>=1.35.0",
    "prometheus-client>=0.19.0",
    "opentelemetry-api>=1.21.0",  # Jövőbeli tracing
]
```

### Konfiguráció

```python
# configs/logger/logging.yaml
version: 1
disable_existing_loggers: false

formatters:
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: "%(asctime)s %(name)s %(levelname)s %(message)s"
  colored:
    class: structlog.stdlib.ProcessorFormatter
    processor: structlog.dev.ConsoleRenderer(colors=True)

handlers:
  console:
    class: logging.StreamHandler
    formatter: colored
    level: INFO
  file:
    class: logging.handlers.RotatingFileHandler
    filename: /var/log/neural_ai/app.log
    formatter: json
    maxBytes: 10485760  # 10MB
    backupCount: 5
    level: DEBUG
  database:
    class: neural_ai.core.logger.handlers.DatabaseHandler
    formatter: json
    level: WARNING

loggers:
  neural_ai:
    level: DEBUG
    handlers: [console, file, database]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

---

## 🎨 Structlog Konfiguráció

### Alap Konfiguráció

```python
import structlog
from structlog.types import EventDict, Processor
import logging
import sys
from datetime import datetime

def configure_structlog() -> None:
    """Structlog konfigurációja."""
    
    # Processzorok láncolata
    processors: List[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        add_correlation_id,
        add_component_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]
    
    # Konzol processzor (fejlesztéshez)
    console_processors = processors + [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta
    ]
    
    # Fájl processzor (JSON formátum)
    file_processors = processors + [
        structlog.processors.JSONRenderer()
    ]
    
    # Structlog konfiguráció
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Standard logging konfiguráció
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
```

### Egyéni Processzorok

```python
import uuid
from typing import Dict, Any

def add_correlation_id(logger, method_name, event_dict) -> EventDict:
    """Trace ID hozzáadása minden loghoz."""
    # Ha nincs trace_id a contextben, generálunk egyet
    if 'trace_id' not in event_dict:
        event_dict['trace_id'] = str(uuid.uuid4())
    
    return event_dict

def add_component_context(logger, method_name, event_dict) -> EventDict:
    """Komponens kontextus hozzáadása."""
    # Komponens nevének kinyerése a logger névből
    logger_name = event_dict.get('logger', '')
    if '.' in logger_name:
        parts = logger_name.split('.')
        if len(parts) >= 2:
            event_dict['component'] = f"{parts[0]}.{parts[1]}"
        else:
            event_dict['component'] = parts[0]
    else:
        event_dict['component'] = logger_name
    
    return event_dict

def add_symbol_context(symbol: str):
    """Szimbólum kontextus hozzáadása."""
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(symbol=symbol)
```

---

## 📝 Log Típusok és Formátumok

### 1. Market Data Logs

```python
import structlog

logger = structlog.get_logger("neural_ai.core.market_data")

async def process_tick(symbol: str, bid: float, ask: float):
    """Tick adat feldolgozása."""
    structlog.contextvars.bind_contextvars(symbol=symbol)
    
    logger.info(
        "tick_received",
        bid=bid,
        ask=ask,
        spread=ask - bid,
        source="jforex"
    )
```

**Kimenet (JSON):**
```json
{
  "timestamp": "2023-12-23T21:30:00.123456Z",
  "level": "info",
  "event": "tick_received",
  "symbol": "EURUSD",
  "bid": 1.10456,
  "ask": 1.10458,
  "spread": 0.00002,
  "source": "jforex",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "component": "neural_ai.core.market_data"
}
```

### 2. Trade Execution Logs

```python
logger = structlog.get_logger("neural_ai.core.execution")

async def execute_trade(signal: SignalEvent):
    """Trade végrehajtása."""
    structlog.contextvars.bind_contextvars(
        symbol=signal.symbol,
        strategy_id=signal.strategy_id
    )
    
    logger.info(
        "trade_execution_started",
        direction=signal.signal_type,
        confidence=signal.confidence
    )
    
    try:
        # Trade végrehajtása
        result = await broker.execute(signal)
        
        logger.info(
            "trade_executed",
            order_id=result.order_id,
            price=result.price,
            volume=result.volume
        )
        
    except Exception as e:
        logger.error(
            "trade_execution_failed",
            error=str(e),
            exc_info=True
        )
        raise
```

**Kimenet (Hiba esetén):**
```json
{
  "timestamp": "2023-12-23T21:30:05.789012Z",
  "level": "error",
  "event": "trade_execution_failed",
  "symbol": "EURUSD",
  "strategy_id": "d3_trend_v1",
  "error": "Insufficient funds",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "component": "neural_ai.core.execution",
  "exception": "Traceback (most recent call last)..."
}
```

### 3. Strategy Decision Logs

```python
logger = structlog.get_logger("neural_ai.strategy.engine")

async def generate_signal(market_data: MarketDataEvent):
    """Jelzés generálása."""
    structlog.contextvars.bind_contextvars(symbol=market_data.symbol)
    
    # AI model futtatása
    prediction = await model.predict(market_data)
    
    logger.debug(
        "model_prediction",
        prediction=prediction,
        confidence=prediction.confidence,
        model_version="v2.5.1"
    )
    
    if prediction.should_trade:
        logger.info(
            "signal_generated",
            signal_type=prediction.signal_type,
            confidence=prediction.confidence,
            reasoning=prediction.reasoning
        )
```

---

## 🗄️ Adatbázis Logolás

### Adatbázis Schema

```python
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LogEntry(Base):
    """Log bejegyzés táblája."""
    
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)
    component = Column(String(255), nullable=False, index=True)
    symbol = Column(String(10), index=True)
    trace_id = Column(String(36), index=True)
    event = Column(String(255))
    message = Column(Text)
    data = Column(JSON)  # Egyéb kontextus adatok
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LogEntry(level='{self.level}', event='{self.event}')>"
```

### Database Handler

```python
import logging
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseHandler(logging.Handler):
    """Logolás adatbázisba."""
    
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory
    
    def emit(self, record):
        """Log rekord feldolgozása."""
        try:
            # JSON adatok kinyerése
            data = getattr(record, 'data', {})
            
            log_entry = LogEntry(
                timestamp=datetime.fromtimestamp(record.created),
                level=record.levelname,
                component=getattr(record, 'component', 'unknown'),
                symbol=getattr(record, 'symbol', None),
                trace_id=getattr(record, 'trace_id', None),
                event=getattr(record, 'event', record.getMessage()),
                message=record.getMessage(),
                data=data
            )
            
            # Aszinkron mentés
            asyncio.create_task(self._save_log(log_entry))
            
        except Exception as e:
            # Ne dobjunk hibát a log handlerben
            print(f"Database log handler error: {e}")
    
    async def _save_log(self, log_entry: LogEntry):
        """Log bejegyzés aszinkron mentése."""
        async with self.session_factory() as session:
            session.add(log_entry)
            await session.commit()
```

---

## 📊 Metrikák és Monitoring

### Prometheus Metrikák

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrikák definiálása
tick_counter = Counter(
    'neural_ai_ticks_total',
    'Total number of ticks processed',
    ['symbol', 'source']
)

trade_counter = Counter(
    'neural_ai_trades_total',
    'Total number of trades executed',
    ['symbol', 'direction', 'strategy']
)

trade_latency = Histogram(
    'neural_ai_trade_latency_seconds',
    'Trade execution latency',
    ['symbol']
)

active_positions = Gauge(
    'neural_ai_active_positions',
    'Number of active positions',
    ['symbol']
)

# Használat
async def process_tick(symbol: str, source: str):
    """Tick feldolgozás metrikákkal."""
    tick_counter.labels(symbol=symbol, source=source).inc()
    
    start_time = time.time()
    # Trade végrehajtás
    await execute_trade(...)
    
    latency = time.time() - start_time
    trade_latency.labels(symbol=symbol).observe(latency)
```

### Grafana Dashboard (Tervezés)

```
┌─────────────────────────────────────────────────┐
│         NEURAL AI NEXT - DASHBOARD              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐  ┌─────────────────┐     │
│  │ Ticks/sec       │  │ Active Positions│     │
│  │ 1,234           │  │ 5               │     │
│  └─────────────────┘  └─────────────────┘     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Trades by Strategy (Last Hour)          │   │
│  │ ██████████ D3_Trend: 45 trades          │   │
│  │ ██████ D2_SR: 28 trades                 │   │
│  │ ████ D5_Momentum: 18 trades             │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Trade Latency (P99)                     │   │
│  │ EURUSD: 125ms                           │   │
│  │ XAUUSD: 98ms                            │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔍 Hibakeresés és Trace-ek

### OpenTelemetry Integráció (Jövőbeli)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

def setup_tracing() -> None:
    """Tracing konfiguráció."""
    trace.set_tracer_provider(TracerProvider())
    
    # Jaeger exporter (vagy Zipkin, stb.)
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

# Használat
tracer = trace.get_tracer(__name__)

async def process_market_data(symbol: str):
    """Market data feldolgozás trace-el."""
    with tracer.start_as_current_span("process_market_data") as span:
        span.set_attribute("symbol", symbol)
        
        # Feldolgozás...
        await analyze_data(symbol)
```

---

## 🎯 Log Szintek és Használat

### Log Szintek Stratégiája

```python
# DEBUG: Részletes fejlesztői információk
logger.debug("detailed_state", internal_state={...})

# INFO: Normál működés, fontos események
logger.info("trade_executed", order_id="...", price=1.2345)

# WARNING: Váratlan, de nem kritikus helyzetek
logger.warning("high_spread", symbol="EURUSD", spread=0.00005)

# ERROR: Hiba történt, de az alkalmazás fut tovább
logger.error("api_call_failed", url="...", status_code=500)

# CRITICAL: Kritikus hiba, alkalmazás leállhat
logger.critical("database_connection_lost", error="...")
```

### Kontextus Adatok

```python
# Minden loghoz automatikusan hozzáadódik:
# - timestamp: ISO 8601 formátum
# - trace_id: Egyedi azonosító a request-hez
# - component: Komponens neve
# - level: Log szint

# Kézi kontextus hozzáadása
structlog.contextvars.bind_contextvars(
    symbol="EURUSD",
    strategy_id="d3_trend_v1",
    user_id="trader_001"
)

logger.info("position_opened", volume=0.1, price=1.1045)
```

---

## 🔐 Biztonság

### Érzékeny Adatok Maszkolása

```python
def mask_sensitive_data(logger, method_name, event_dict) -> EventDict:
    """Érzékeny adatok maszkolása."""
    sensitive_keys = ['password', 'api_key', 'secret', 'token']
    
    for key in event_dict:
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            event_dict[key] = '***MASKED***'
    
    return event_dict

# Processzor hozzáadása
processors = [
    mask_sensitive_data,
    # ... egyéb processzorok
]
```

---

## 📋 Következő Lépések

1. **Adattárolás:** Lásd [`04_data_warehouse.md`](04_data_warehouse.md)
2. **Collectorok:** Lásd [`05_collectors_strategy.md`](05_collectors_strategy.md)

---

## 🔗 Kapcsolódó Dokumentumok

- [Rendszerarchitektúra](01_system_architecture.md)
- [Dinamikus Konfiguráció](02_dynamic_configuration.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)