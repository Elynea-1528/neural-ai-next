"""Konfigurációs típusdefiníciók TypedDict használatával.

Ez a modul definiálja a különböző konfigurációs szekciókhoz tartozó TypedDict osztályokat,
amelyek biztosítják a típusbiztonságot és dokumentációt a konfigurációs adatok kezelésére.
"""

from typing import Literal, TypedDict


class PathsConfig(TypedDict, total=False):
    """Rendszer útvonalak konfigurációja."""
    data: str
    logs: str
    models: str
    cache: str


class SystemConfig(TypedDict, total=False):
    """Rendszer szintű konfiguráció."""
    app_name: str
    version: str
    environment: Literal["development", "staging", "production"]
    debug: bool
    paths: PathsConfig


class StoragePartitioningConfig(TypedDict, total=False):
    """Tárolási particionálási konfiguráció."""


class StorageConfig(TypedDict, total=False):
    """Adattárolási konfiguráció."""
    type: Literal["parquet", "csv", "json"]
    base_path: str
    compression: str
    engine: str
    partitioning: list[str]


class TimeframeConfig(TypedDict, total=False):
    """Időkeret specifikus konfiguráció."""
    z_score_window: int
    swing_window: int


class ProcessorConfig(TypedDict, total=False):
    """Egyedi processzor konfiguráció."""
    required_timeframes: list[str]
    z_score_window: int
    use_mid_price: bool
    calc_shadows: bool
    swing_window: int
    min_distance: int
    use_close_open: bool
    use_high_low: bool
    primary_weight: float
    secondary_weight: float
    level_merge: float
    min_touches: int
    volume_confirmation: bool
    strength_window: int
    timeframe_configs: dict[str, TimeframeConfig]


class ProcessorsConfig(TypedDict, total=False):
    """Processzorok konfigurációja."""
    processors: dict[str, ProcessorConfig]


class HandlerConfig(TypedDict, total=False):
    """Log handler konfiguráció."""
    enabled: bool
    level: str
    colored: bool
    filename: str
    json_format: bool
    rotating: bool
    max_bytes: int
    backup_count: int


class LoggerConfig(TypedDict, total=False):
    """Egyedi logger konfiguráció."""
    level: str
    propagate: bool


class LoggingConfig(TypedDict, total=False):
    """Naplózási konfiguráció."""
    default_level: str
    handlers: dict[str, HandlerConfig]
    loggers: dict[str, LoggerConfig]


class DatabaseConnectionConfig(TypedDict, total=False):
    """Adatbázis kapcsolat konfiguráció."""
    url: str


class DatabasePoolConfig(TypedDict, total=False):
    """Adatbázis pool konfiguráció."""
    size: int
    recycle: int


class DatabaseConfig(TypedDict, total=False):
    """Adatbázis konfiguráció."""
    type: Literal["sqlite", "postgresql", "mysql"]
    connection: DatabaseConnectionConfig
    pool: DatabasePoolConfig


class EventsConnectionConfig(TypedDict, total=False):
    """Esemény kapcsolat konfiguráció."""
    protocol: str
    host: str
    pub_port: int
    sub_port: int
    use_inproc: bool


class EventsConfig(TypedDict, total=False):
    """Esemény rendszer konfiguráció."""
    type: Literal["zeromq", "redis", "rabbitmq"]
    connection: EventsConnectionConfig
    socket_timeout: int


class CollectorDownloadConfig(TypedDict, total=False):
    """Gyűjtő letöltési konfiguráció."""
    timeout: int
    max_retries: int
    retry_delay: int
    chunk_size: int


class CollectorLoggingConfig(TypedDict, total=False):
    """Gyűjtő naplózási konfiguráció."""
    level: str
    format: str


class CollectorRateLimitingConfig(TypedDict, total=False):
    """Gyűjtő rate limiting konfiguráció."""
    max_concurrent: int
    request_delay: float


class CollectorCircuitBreakerConfig(TypedDict, total=False):
    """Gyűjtő circuit breaker konfiguráció."""
    failure_threshold: int
    recovery_timeout: int
    expected_exceptions: list[str]


class CollectorDateRangeConfig(TypedDict, total=False):
    """Gyűjtő dátumtartomány konfiguráció."""
    start: str
    end: str


class JForexConfig(TypedDict, total=False):
    """JForex gyűjtő konfiguráció."""
    enabled: bool
    base_url: str
    download: CollectorDownloadConfig
    logging: CollectorLoggingConfig
    symbols: list[str]
    date_range: CollectorDateRangeConfig
    rate_limiting: CollectorRateLimitingConfig
    circuit_breaker: CollectorCircuitBreakerConfig


class JForexLiveConfig(TypedDict, total=False):
    """JForex live feed konfiguráció."""
    enabled: bool
    host: str
    tick_port: int
    command_port: int


class CollectorsConfig(TypedDict, total=False):
    """Gyűjtők konfigurációja."""
    jforex: JForexConfig
    jforex_live: JForexLiveConfig


class IngestionConfig(TypedDict, total=False):
    """Adatbevitel konfiguráció."""
    buffer_size_limit: int
    flush_interval_minutes: int


class ConfigSchema(TypedDict, total=False):
    """Általános konfigurációs séma típus."""
    system: SystemConfig
    storage: StorageConfig
    processors: ProcessorsConfig
    logging: LoggingConfig
    database: DatabaseConfig
    events: EventsConfig
    collectors: CollectorsConfig
    ingestion: IngestionConfig
