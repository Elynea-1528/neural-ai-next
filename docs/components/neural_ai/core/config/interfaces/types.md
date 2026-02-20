# neural_ai/core/config/interfaces/types.py

Konfigurációs típusdefiníciók Pydantic BaseModel használatával.

Ez a modul definiálja a különböző konfigurációs szekciókhoz tartozó Pydantic
modelleket, amelyek biztosítják a típusbiztonságot, validációt és dokumentációt
a konfigurációs adatok kezelésére.

## Importok

```python
from typing import Literal
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
```

## Osztály: `PathsConfig(BaseModel)`

Rendszer útvonalak konfigurációja.

## Osztály: `StoragePartitioningConfig(BaseModel)`

Tárolási particionálási konfiguráció.

## Osztály: `TimeframeConfig(BaseModel)`

Időkeret specifikus konfiguráció.

## Osztály: `MarketHoursConfig(BaseModel)`

Piaci órák konfigurációja.

## Osztály: `HandlerConfig(BaseModel)`

Log handler konfiguráció.

## Osztály: `LoggerConfig(BaseModel)`

Egyedi logger konfiguráció.

## Osztály: `DatabaseConnectionConfig(BaseModel)`

Adatbázis kapcsolat konfiguráció.

## Osztály: `DatabasePoolConfig(BaseModel)`

Adatbázis pool konfiguráció.

## Osztály: `EventsConnectionConfig(BaseModel)`

Esemény kapcsolat konfiguráció.

## Osztály: `CollectorDownloadConfig(BaseModel)`

Gyűjtő letöltési konfiguráció.

## Osztály: `CollectorLoggingConfig(BaseModel)`

Gyűjtő naplózási konfiguráció.

## Osztály: `CollectorRateLimitingConfig(BaseModel)`

Gyűjtő rate limiting konfiguráció.

## Osztály: `CollectorCircuitBreakerConfig(BaseModel)`

Gyűjtő circuit breaker konfiguráció.

## Osztály: `CollectorDateRangeConfig(BaseModel)`

Gyűjtő dátumtartomány konfiguráció.

## Osztály: `SystemConfig(BaseModel)`

Rendszer szintű konfiguráció.

## Osztály: `StorageConfig(BaseModel)`

Adattárolási konfiguráció.

ARCHITEKTÚRA SZABÁLY: Csak Parquet storage engedélyezett!
CSV/JSON használata tiltott a storage rétegben.
Lásd: docs/development/architecture_standards.md - Storage szabályok

### Metódusok

#### `validate_no_csv_json()`

```python
def validate_no_csv_json(cls, v: str | None) -> str | None
```

CSV/JSON storage tiltott architektúra szabályok szerint.

**Paraméterek:**

- **`cls`**
- **`v`** (`str | None`)

**Visszatérési érték:**

- Típus: `str | None`

## Osztály: `ProcessorConfig(BaseModel)`

Egyedi processzor konfiguráció.

### Metódusok

#### `validate_timeframes()`

```python
def validate_timeframes(cls, v: list[str] | None) -> list[str] | None
```

Csak standard Forex timeframe-ek engedélyezettek.

**Paraméterek:**

- **`cls`**
- **`v`** (`list[str] | None`)

**Visszatérési érték:**

- Típus: `list[str] | None`

## Osztály: `LoggingConfig(BaseModel)`

Naplózási konfiguráció.

## Osztály: `DatabaseConfig(BaseModel)`

Teljes adatbázis konfiguráció Pydantic validációval.

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

### Metódusok

#### `validate_connection_url()`

```python
def validate_connection_url(cls, v: DatabaseConnectionConfig) -> DatabaseConnectionConfig
```

Ellenőrzi a connection URL formátumát. Támogatott async driver formátumok: - sqlite+aiosqlite:// (SQLite async) - postgresql+asyncpg:// (PostgreSQL async) - mysql+aiomysql:// (MySQL async)

**Paraméterek:**

- **`cls`**
- **`v`** (`DatabaseConnectionConfig`): A DatabaseConnectionConfig objektum

**Visszatérési érték:**

- Típus: `DatabaseConnectionConfig`
- DatabaseConnectionConfig: A validált konfiguráció

**Kivételek:**

- **`ValueError`**: Ha az URL formátuma nem támogatott

#### `validate_pool_config()`

```python
def validate_pool_config(cls, v: DatabasePoolConfig | None) -> DatabasePoolConfig | None
```

Validálja a pool konfigurációt. Ellenőrzi, hogy a pool size legalább 1, ha meg van adva.

**Paraméterek:**

- **`cls`**
- **`v`** (`DatabasePoolConfig | None`): A DatabasePoolConfig objektum vagy None

**Visszatérési érték:**

- Típus: `DatabasePoolConfig | None`
- DatabasePoolConfig | None: A validált pool konfiguráció

**Kivételek:**

- **`ValueError`**: Ha a pool size < 1

## Osztály: `EventsConfig(BaseModel)`

Esemény rendszer konfiguráció.

## Osztály: `JForexConfig(BaseModel)`

JForex gyűjtő konfiguráció.

### Metódusok

#### `validate_symbols_not_empty()`

```python
def validate_symbols_not_empty(cls, v: list[str] | None) -> list[str] | None
```

Symbols lista nem lehet üres.

**Paraméterek:**

- **`cls`**
- **`v`** (`list[str] | None`)

**Visszatérési érték:**

- Típus: `list[str] | None`

## Osztály: `JForexLiveConfig(BaseModel)`

JForex live feed konfiguráció.

## Osztály: `ProcessorsConfig(BaseModel)`

Processzorok konfigurációja.

## Osztály: `CollectorsConfig(BaseModel)`

Gyűjtők konfigurációja.

## Osztály: `IngestionConfig(BaseModel)`

Adatbevitel konfiguráció.

## Osztály: `UIDateRangeConfig(BaseModel)`

UI Dátumtartomány konfiguráció.

## Osztály: `UIJForexConfig(BaseModel)`

UI JForex konfiguráció.

## Osztály: `DataServiceConfig(BaseModel)`

UI Adatszolgáltatás konfiguráció.

## Osztály: `NavigationConfig(BaseModel)`

Navigáció konfiguráció.

## Osztály: `DashboardConfig(BaseModel)`

Dashboard konfiguráció.

## Osztály: `AIServiceConfig(BaseModel)`

AI szolgáltatás konfiguráció.

## Osztály: `StrategyConfig(BaseModel)`

Stratégia konfiguráció.

## Osztály: `LiveOpsConfig(BaseModel)`

Live Ops konfiguráció.

## Osztály: `UIConfig(BaseModel)`

UI Factory konfiguráció Pydantic validációval.

## Osztály: `ConfigSchema(BaseModel)`

Általános konfigurációs séma típus.

Ez a root konfiguráció modell, amely összeköti az összes alrendszer konfigurációját.

---

**Forrásfájl:** [`neural_ai/core/config/interfaces/types.py`](../../neural_ai/core/config/interfaces/types.py)
