"""Konfigurációs típusdefiníciók Pydantic BaseModel használatával.

Ez a modul definiálja a különböző konfigurációs szekciókhoz tartozó Pydantic
modelleket, amelyek biztosítják a típusbiztonságot, validációt és dokumentációt
a konfigurációs adatok kezelésére.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PathsConfig(BaseModel):
    """Rendszer útvonalak konfigurációja."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    data: str | None = Field(None, min_length=1, description="Adat könyvtár útvonala")
    logs: str | None = Field(None, min_length=1, description="Log könyvtár útvonala")
    models: str | None = Field(None, min_length=1, description="Model könyvtár útvonala")
    cache: str | None = Field(None, min_length=1, description="Cache könyvtár útvonala")


class StoragePartitioningConfig(BaseModel):
    """Tárolási particionálási konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class TimeframeConfig(BaseModel):
    """Időkeret specifikus konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    z_score_window: int | None = Field(None, ge=1, description="Z-score ablak méret")
    swing_window: int | None = Field(None, ge=1, description="Swing ablak méret")


class MarketHoursConfig(BaseModel):
    """Piaci órák konfigurációja."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    enabled: bool | None = Field(None, description="Piaci órák szűrése engedélyezve")
    weekdays: list[str] | None = Field(None, description="Engedélyezett napok")
    hours: list[str] | None = Field(None, description="Engedélyezett órák")
    timezone: str | None = Field(None, description="Időzóna")
    log_filtering: bool | None = Field(None, description="Szűrés naplózása")


class HandlerConfig(BaseModel):
    """Log handler konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    enabled: bool | None = Field(None, description="Handler engedélyezve")
    level: str | None = Field(
        None,
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Log szint"
    )
    colored: bool | None = Field(None, description="Színezett kimenet")
    filename: str | None = Field(None, min_length=1, description="Log fájl neve")
    json_format: bool | None = Field(None, description="JSON formátum használata")
    rotating: bool | None = Field(None, description="Rotáló fájl használata")
    max_bytes: int | None = Field(None, ge=1, description="Maximális fájlméret bájtban")
    backup_count: int | None = Field(None, ge=0, description="Mentési példányok száma")
    class_name: str | None = Field(
        None,
        alias="class",
        min_length=1,
        description="Handler osztály (pl. logging.handlers.RotatingFileHandler)"
    )
    maxBytes: int | None = Field(
        None, ge=1, description="Maximális fájlméret bájtban (RotatingFileHandler)"
    )
    backupCount: int | None = Field(
        None, ge=0, description="Backup fájlok száma (RotatingFileHandler)"
    )
    encoding: str | None = Field(None, min_length=1, description="Fájl kódolás (pl. utf-8)")


class LoggerConfig(BaseModel):
    """Egyedi logger konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    level: str | None = Field(
        None,
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Logger szintje"
    )
    propagate: bool | None = Field(None, description="Propagálás engedélyezése")


class DatabaseConnectionConfig(BaseModel):
    """Adatbázis kapcsolat konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    url: str | None = Field(None, min_length=1, description="Adatbázis kapcsolati URL")


class DatabasePoolConfig(BaseModel):
    """Adatbázis pool konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    size: int | None = Field(None, ge=1, description="Pool méret")
    recycle: int | None = Field(None, ge=1, description="Újrahasznosítási idő másodpercben")


class EventsConnectionConfig(BaseModel):
    """Esemény kapcsolat konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    protocol: str | None = Field(None, min_length=1, description="Protokoll típusa")
    host: str | None = Field(None, min_length=1, description="Host név vagy IP")
    pub_port: int | None = Field(None, ge=1, le=65535, description="Publisher port")
    sub_port: int | None = Field(None, ge=1, le=65535, description="Subscriber port")
    use_inproc: bool | None = Field(None, description="In-process kommunikáció használata")


class CollectorDownloadConfig(BaseModel):
    """Gyűjtő letöltési konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    timeout: int | None = Field(None, ge=1, description="Timeout másodpercben")
    max_retries: int | None = Field(
        None, ge=0, description="Maximális újrapróbálkozások száma"
    )
    retry_delay: int | None = Field(
        None, ge=0, description="Újrapróbálkozási késleltetés másodpercben"
    )
    chunk_size: int | None = Field(None, ge=1, description="Chunk méret bájtban")


class CollectorLoggingConfig(BaseModel):
    """Gyűjtő naplózási konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    level: str | None = Field(
        None,
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Log szint"
    )
    format: str | None = Field(None, min_length=1, description="Log formátum string")


class CollectorRateLimitingConfig(BaseModel):
    """Gyűjtő rate limiting konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    max_concurrent: int | None = Field(
        None, ge=1, description="Maximális párhuzamos kérések"
    )
    request_delay: float | None = Field(
        None, ge=0.0, description="Kérések közötti késleltetés másodpercben"
    )


class CollectorCircuitBreakerConfig(BaseModel):
    """Gyűjtő circuit breaker konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    failure_threshold: int | None = Field(None, ge=1, description="Hiba küszöb")
    recovery_timeout: int | None = Field(
        None, ge=1, description="Helyreállítási timeout másodpercben"
    )
    expected_exceptions: list[str] | None = Field(
        None, description="Várt kivételek listája"
    )


class CollectorDateRangeConfig(BaseModel):
    """Gyűjtő dátumtartomány konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    start: str | None = Field(None, min_length=1, description="Kezdő dátum (ISO formátum)")
    end: str | None = Field(None, min_length=1, description="Befejező dátum (ISO formátum)")


class SystemConfig(BaseModel):
    """Rendszer szintű konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    app_name: str | None = Field(None, min_length=1, description="Alkalmazás neve")
    version: str | None = Field(None, min_length=1, description="Verzió szám")
    environment: Literal["development", "staging", "production"] | None = Field(
        None,
        description="Környezet típusa"
    )
    debug: bool | None = Field(None, description="Debug mód")
    paths: PathsConfig | None = Field(None, description="Útvonal konfigurációk")


class StorageConfig(BaseModel):
    """Adattárolási konfiguráció.

    ARCHITEKTÚRA SZABÁLY: Csak Parquet storage engedélyezett!
    CSV/JSON használata tiltott a storage rétegben.
    Lásd: docs/development/architecture_standards.md - Storage szabályok
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    type: Literal["parquet", "csv", "json"] | None = Field(
        "parquet",
        description="Storage backend típusa"
    )
    base_path: str | None = Field(None, min_length=1, description="Tárolási könyvtár")
    compression: str | None = Field(
        "snappy",
        pattern="^(snappy|gzip|lz4|zstd)$",
        description="Kompressziós algoritmus"
    )
    engine: str | None = Field(
        "fastparquet",
        pattern="^(fastparquet|pyarrow)$",
        description="Parquet engine"
    )
    partitioning: list[str] | None = Field(
        None,
        description="Particionálási oszlopok"
    )

    @field_validator("type")
    @classmethod
    def validate_no_csv_json(cls, v: str | None) -> str | None:
        """CSV/JSON storage tiltott architektúra szabályok szerint."""
        if v in ("csv", "json"):
            raise ValueError(
                f"'{v}' storage TILOS! Csak Parquet engedélyezett. "
                "Lásd: docs/development/architecture_standards.md - Storage szabályok"
            )
        return v


class ProcessorConfig(BaseModel):
    """Egyedi processzor konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    required_timeframes: list[str] | None = Field(None, description="Szükséges timeframe-ek")
    z_score_window: int | None = Field(None, ge=1, description="Z-score ablak méret")
    use_mid_price: bool | None = Field(None, description="Mid price használata")
    calc_shadows: bool | None = Field(None, description="Árnyékok kalkulációja")
    swing_window: int | None = Field(None, ge=1, description="Swing ablak méret")
    min_distance: int | None = Field(None, ge=1, description="Minimális távolság")
    use_close_open: bool | None = Field(None, description="Close/Open használata")
    use_high_low: bool | None = Field(None, description="High/Low használata")
    primary_weight: float | None = Field(None, ge=0.0, le=1.0, description="Elsődleges súly")
    secondary_weight: float | None = Field(None, ge=0.0, le=1.0, description="Másodlagos súly")
    level_merge: float | None = Field(None, ge=0.0, description="Szint egyesítési távolság")
    min_touches: int | None = Field(None, ge=1, description="Minimális érintések száma")
    volume_confirmation: bool | None = Field(None, description="Volumen megerősítés")
    strength_window: int | None = Field(None, ge=1, description="Erősség ablak méret")
    market_hours: MarketHoursConfig | None = Field(
        None, description="Piaci órák konfigurációja"
    )
    min_candles: int | None = Field(None, ge=1, description="Minimális gyertyák száma")
    timeframe_configs: dict[str, TimeframeConfig] | None = Field(
        None,
        description="Timeframe specifikus konfigurációk"
    )

    @field_validator("required_timeframes")
    @classmethod
    def validate_timeframes(cls, v: list[str] | None) -> list[str] | None:
        """Csak standard Forex timeframe-ek engedélyezettek."""
        if v is None:
            return v

        valid_tf = {"M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"}
        for tf in v:
            if tf not in valid_tf:
                raise ValueError(
                    f"Érvénytelen timeframe: {tf}. "
                    f"Érvényes timeframe-ek: {valid_tf}"
                )
        return v


class LoggingConfig(BaseModel):
    """Naplózási konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True,
    )

    default_level: str | None = Field(
        "INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Alapértelmezett log szint"
    )
    handlers: dict[str, HandlerConfig] | None = Field(None, description="Handler konfigurációk")
    loggers: dict[str, LoggerConfig] | None = Field(None, description="Logger konfigurációk")


class DatabaseConfig(BaseModel):
    """Teljes adatbázis konfiguráció Pydantic validációval.

    Ez a modell reprezentálja a teljes adatbázis konfigurációt, beleértve
    a kapcsolati beállításokat és az opcionális connection pool paramétereket.
    Szigorú validációt biztosít a connection URL formátumára és a pool méretére.

    ARCHITEKTÚRA SZABÁLY: Csak async database driver-ek engedélyezettek!
    Támogatott formátumok:
        - sqlite+aiosqlite:///path/to/db.db
        - postgresql+asyncpg://user:pass@host:port/dbname
        - mysql+aiomysql://user:pass@host:port/dbname

    Lásd: docs/development/architecture_standards.md - Típusbiztonság

    Attributes:
        connection: Adatbázis kapcsolat konfigurációja (kötelező)
        pool: Connection pool konfiguráció (opcionális)

    Raises:
        ValueError: Ha a connection URL formátuma érvénytelen
        ValueError: Ha a pool size < 1

    Example:
        >>> config = DatabaseConfig(
        ...     connection=DatabaseConnectionConfig(
        ...         url="sqlite+aiosqlite:///neural_ai.db"
        ...     ),
        ...     pool=DatabasePoolConfig(size=5, recycle=3600)
        ... )
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    connection: DatabaseConnectionConfig = Field(
        ...,
        description="Adatbázis kapcsolat konfiguráció (kötelező)"
    )
    pool: DatabasePoolConfig | None = Field(
        None,
        description="Connection pool konfiguráció (opcionális, csak nem-SQLite DB-khez)"
    )

    @field_validator('connection')
    @classmethod
    def validate_connection_url(
        cls, v: DatabaseConnectionConfig
    ) -> DatabaseConnectionConfig:
        """Ellenőrzi a connection URL formátumát.

        Támogatott async driver formátumok:
        - sqlite+aiosqlite:// (SQLite async)
        - postgresql+asyncpg:// (PostgreSQL async)
        - mysql+aiomysql:// (MySQL async)

        Args:
            v: A DatabaseConnectionConfig objektum

        Returns:
            DatabaseConnectionConfig: A validált konfiguráció

        Raises:
            ValueError: Ha az URL formátuma nem támogatott
        """
        if not v.url:
            raise ValueError("Adatbázis URL megadása kötelező!")

        url_lower = v.url.lower()
        valid_prefixes = [
            "sqlite+aiosqlite://",
            "postgresql+asyncpg://",
            "mysql+aiomysql://"
        ]

        if not any(url_lower.startswith(prefix) for prefix in valid_prefixes):
            raise ValueError(
                f"Érvénytelen adatbázis URL formátum: {v.url}. "
                f"Támogatott async driver-ek: {', '.join(valid_prefixes)}"
            )

        return v

    @field_validator('pool')
    @classmethod
    def validate_pool_config(
        cls, v: DatabasePoolConfig | None
    ) -> DatabasePoolConfig | None:
        """Validálja a pool konfigurációt.

        Ellenőrzi, hogy a pool size legalább 1, ha meg van adva.

        Args:
            v: A DatabasePoolConfig objektum vagy None

        Returns:
            DatabasePoolConfig | None: A validált pool konfiguráció

        Raises:
            ValueError: Ha a pool size < 1
        """
        if v and v.size is not None and v.size < 1:
            raise ValueError("Pool size nem lehet kisebb mint 1!")
        return v


class EventsConfig(BaseModel):
    """Esemény rendszer konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    type: Literal["zeromq", "redis", "rabbitmq"] | None = Field(
        None,
        description="Esemény rendszer típusa"
    )
    connection: EventsConnectionConfig | None = Field(None, description="Kapcsolat konfiguráció")
    socket_timeout: int | None = Field(None, ge=1, description="Socket timeout milliszekundumban")


class JForexConfig(BaseModel):
    """JForex gyűjtő konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    enabled: bool | None = Field(None, description="Gyűjtő engedélyezve")
    base_url: str | None = Field(
        "https://datafeed.dukascopy.com",
        pattern=r"^https?://",
        description="JForex API alap URL"
    )
    download: CollectorDownloadConfig | None = Field(None, description="Letöltési konfiguráció")
    logging: CollectorLoggingConfig | None = Field(
        None, description="Naplózási konfiguráció"
    )
    symbols: list[str] | None = Field(None, description="Szimbólumok listája")
    date_range: CollectorDateRangeConfig | None = Field(
        None, description="Dátumtartomány konfiguráció"
    )
    rate_limiting: CollectorRateLimitingConfig | None = Field(
        None, description="Rate limiting konfiguráció"
    )
    circuit_breaker: CollectorCircuitBreakerConfig | None = Field(
        None, description="Circuit breaker konfiguráció"
    )

    @field_validator("symbols")
    @classmethod
    def validate_symbols_not_empty(cls, v: list[str] | None) -> list[str] | None:
        """Symbols lista nem lehet üres."""
        if v is not None and len(v) == 0:
            raise ValueError("Symbols lista nem lehet üres!")
        return v


class JForexLiveConfig(BaseModel):
    """JForex live feed konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    enabled: bool | None = Field(None, description="Live feed engedélyezve")
    host: str | None = Field(None, min_length=1, description="Host név vagy IP")
    tick_port: int | None = Field(None, ge=1, le=65535, description="Tick adatok portja")
    command_port: int | None = Field(None, ge=1, le=65535, description="Parancsok portja")


class ProcessorsConfig(BaseModel):
    """Processzorok konfigurációja."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    processors: dict[str, ProcessorConfig] | None = Field(
        None, description="Processzor konfigurációk"
    )


class CollectorsConfig(BaseModel):
    """Gyűjtők konfigurációja."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    jforex: JForexConfig | None = Field(None, description="JForex gyűjtő konfiguráció")
    jforex_live: JForexLiveConfig | None = Field(None, description="JForex live feed konfiguráció")


class IngestionConfig(BaseModel):
    """Adatbevitel konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    buffer_size_limit: int | None = Field(
        None, ge=1, description="Buffer méret limit"
    )
    flush_interval_minutes: int | None = Field(
        None, ge=1, description="Flush intervallum percekben"
    )


class UIDateRangeConfig(BaseModel):
    """UI Dátumtartomány konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    start: str | None = Field(None, min_length=1, description="Kezdő dátum (ISO formátum)")
    end: str | None = Field(None, min_length=1, description="Befejező dátum (ISO formátum)")


class UIJForexConfig(BaseModel):
    """UI JForex konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    symbols: list[str] | None = Field(None, description="Szimbólumok listája")
    date_range: UIDateRangeConfig | None = Field(None, description="Dátumtartomány")


class DataServiceConfig(BaseModel):
    """UI Adatszolgáltatás konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    jforex: UIJForexConfig | None = Field(None, description="JForex konfiguráció")


class NavigationConfig(BaseModel):
    """Navigáció konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    default_page: str | None = Field(None, description="Alapértelmezett oldal")


class DashboardConfig(BaseModel):
    """Dashboard konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    refresh_rate: int | None = Field(None, ge=1, description="Frissítési ráta másodpercben")


class AIServiceConfig(BaseModel):
    """AI szolgáltatás konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    model_path: str | None = Field(None, description="Modell útvonala")


class StrategyConfig(BaseModel):
    """Stratégia konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    backtest_enabled: bool | None = Field(None, description="Backtest engedélyezve")


class LiveOpsConfig(BaseModel):
    """Live Ops konfiguráció."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    auto_reconnect: bool | None = Field(None, description="Automatikus újracsatlakozás")


class UIConfig(BaseModel):
    """UI Factory konfiguráció Pydantic validációval."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    theme: Literal["light", "dark"] | None = Field("light", description="UI téma")
    refresh_rate: int | None = Field(
        None, ge=1, description="Globális frissítési ráta másodpercben"
    )
    navigation: NavigationConfig | None = Field(None, description="Navigáció konfiguráció")
    dashboard: DashboardConfig | None = Field(None, description="Dashboard konfiguráció")
    data_service: DataServiceConfig | None = Field(
        None, description="Adatszolgáltatás konfiguráció"
    )
    ai_service: AIServiceConfig | None = Field(None, description="AI szolgáltatás konfiguráció")
    strategy: StrategyConfig | None = Field(None, description="Stratégia konfiguráció")
    live_ops: LiveOpsConfig | None = Field(None, description="Live Ops konfiguráció")


class ConfigSchema(BaseModel):
    """Általános konfigurációs séma típus.

    Ez a root konfiguráció modell, amely összeköti az összes alrendszer konfigurációját.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    system: SystemConfig | None = Field(None, description="Rendszer konfiguráció")
    storage: StorageConfig | None = Field(None, description="Tárolási konfiguráció")
    processors: ProcessorsConfig | None = Field(None, description="Processzorok konfigurációja")
    logging: LoggingConfig | None = Field(None, description="Naplózási konfiguráció")
    database: DatabaseConfig | None = Field(None, description="Adatbázis konfiguráció")
    events: EventsConfig | None = Field(None, description="Esemény rendszer konfiguráció")
    collectors: CollectorsConfig | None = Field(None, description="Gyűjtők konfigurációja")
    ingestion: IngestionConfig | None = Field(None, description="Adatbevitel konfiguráció")
    ui: UIConfig | None = Field(None, description="UI konfiguráció")
