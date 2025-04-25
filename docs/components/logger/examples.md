# Logger Komponens Használati Példák

## 1. Alap használat

### 1.1 Logger inicializálás

```python
from neural_ai.core.logger.implementations import LoggerFactory

# Alapértelmezett logger
logger = LoggerFactory.get_logger(__name__)

# Színes konzol logger
logger = LoggerFactory.get_logger(__name__, logger_type="colored")

# Fájl logger
logger = LoggerFactory.get_logger(__name__, logger_type="rotating_file")
```

### 1.2 Naplózási szintek

```python
# Különböző szintű üzenetek
logger.debug("Részletes diagnosztikai információ")
logger.info("Általános információs üzenet")
logger.warning("Figyelmeztetés - nem kritikus hiba")
logger.error("Hiba - művelet sikertelen")
logger.critical("Kritikus hiba - alkalmazás leállhat")
```

## 2. Haladó használat

### 2.1 Logger konfigurálás

```python
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="rotating_file",
    level="INFO",
    format="[{levelname}] {asctime} - {message}",
    filename="logs/app.log",
    max_bytes=1024*1024,  # 1MB
    backup_count=5
)
```

### 2.2 Strukturált naplózás

```python
# Kontextus információkkal
logger.info(
    "Felhasználó bejelentkezett",
    extra={
        "user_id": "123",
        "ip": "192.168.1.1",
        "browser": "Chrome"
    }
)

# Teljesítmény metrikákkal
logger.debug(
    "Adatbázis lekérdezés",
    extra={
        "query_time": 0.35,
        "rows_returned": 1000,
        "cache_hit": False
    }
)
```

## 3. Formázás

### 3.1 Egyedi formátumok

```python
# JSON formátum
logger = LoggerFactory.get_logger(
    __name__,
    format="{\"time\": \"%(asctime)s\", \"level\": \"%(levelname)s\", \"message\": \"%(message)s\"}"
)

# Részletes formátum
logger = LoggerFactory.get_logger(
    __name__,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
)
```

### 3.2 Színes kimenet

```python
# Színes konzol logger egyedi színekkel
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="colored",
    colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white"
    }
)
```

## 4. Fájl kezelés

### 4.1 Rotáló fájl logger

```python
# Méret alapú rotáció
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="rotating_file",
    filename="logs/app.log",
    max_bytes=1024*1024,  # 1MB
    backup_count=5
)

# Idő alapú rotáció
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="timed_rotating_file",
    filename="logs/app.log",
    when="midnight",
    interval=1,
    backup_count=7
)
```

### 4.2 Naplófájl tömörítés

```python
# Automatikus tömörítés
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="rotating_file",
    filename="logs/app.log",
    compress=True,
    compress_mode="gzip"
)
```

## 5. Hibakezelés

### 5.1 Kivételek naplózása

```python
try:
    result = process_data()
except Exception as e:
    # Kivétel stack trace naplózása
    logger.exception("Hiba az adatfeldolgozás során")

    # vagy részletes információkkal
    logger.error(
        "Feldolgozási hiba",
        extra={
            "error": str(e),
            "error_type": type(e).__name__,
            "data": input_data
        }
    )
```

### 5.2 Kontextus kezelés

```python
from neural_ai.core.logger.utils import log_context

# Kontextus menedzser használata
with log_context(logger, "user_id", "123"):
    logger.info("Művelet kezdése")  # user_id automatikusan hozzáadva
    process_user_data()
    logger.info("Művelet befejezve")
```

## 6. Teljesítmény mérés

### 6.1 Műveletek időmérése

```python
from neural_ai.core.logger.utils import log_timing

# Dekorátor használata
@log_timing(logger)
def process_large_dataset(data):
    # Feldolgozás
    pass

# vagy kontextus menedzserrel
with log_timing(logger, "data_processing"):
    process_large_dataset(data)
```

### 6.2 Metrikák naplózása

```python
def log_metrics(metrics: Dict[str, Any]) -> None:
    logger.info(
        "Teljesítmény metrikák",
        extra={
            "metrics": metrics,
            "timestamp": time.time(),
            "type": "performance_metrics"
        }
    )

# Használat
log_metrics({
    "response_time": 0.35,
    "memory_usage": 1024,
    "cpu_usage": 45.2
})
```

## 7. Integrációs példák

### 7.1 Config integrálás

```python
from neural_ai.core.config import ConfigManagerFactory

# Logger konfigurálása config fájlból
config = ConfigManagerFactory.get_manager("configs/logging.yaml")
logger = LoggerFactory.get_logger(__name__, **config.get_section("logger"))
```

### 7.2 Monitoring integrálás

```python
# Prometheus metrikák
from prometheus_client import Counter, Histogram

# Metrikák definiálása
log_counter = Counter("log_entries_total", "Total log entries", ["level"])
log_timing = Histogram("operation_duration_seconds", "Operation timing")

class MetricsLogger:
    def __init__(self, logger):
        self._logger = logger

    def info(self, msg, *args, **kwargs):
        log_counter.labels(level="info").inc()
        self._logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        log_counter.labels(level="error").inc()
        self._logger.error(msg, *args, **kwargs)

# Használat
logger = MetricsLogger(LoggerFactory.get_logger(__name__))
