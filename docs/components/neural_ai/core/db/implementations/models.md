# Adatbázis Modellek

## Áttekintés

Adatbázis modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes adatbázis táblát és modellt a rendszerben, beleértve a DynamicConfig és LogEntry modelleket.

## Osztályok

### `DynamicConfig`

Dinamikus konfigurációs értékek tárolására szolgáló modell.

Ez a modell tárolja a futás közben módosítható konfigurációs értékeket, amelyek hot reload támogatással rendelkeznek.

#### Attribútumok

- `key`: A konfigurációs kulcs (egyedi).
- `value`: A konfigurációs érték (JSON formátumban).
- `value_type`: Az érték típusa (int, float, str, bool, list, dict).
- `category`: A konfiguráció kategóriája (risk, strategy, trading, system).
- `description`: A konfiguráció leírása.
- `is_active`: A konfiguráció aktív-e.

#### Oszlop Definíciók

##### `key`

A konfigurációs kulcs (egyedi).

- **Típus**: `String(255)`
- **Egyedi**: Igen
- **Indexelt**: Igen
- **Nullable**: Nem

##### `value`

A konfigurációs érték (JSON formátumban).

- **Típus**: `JSON`
- **Nullable**: Nem

##### `value_type`

Az érték típusa (int, float, str, bool, list, dict).

- **Típus**: `String(50)`
- **Nullable**: Nem

##### `category`

A konfiguráció kategóriája (risk, strategy, trading, system).

- **Típus**: `String(100)`
- **Indexelt**: Igen
- **Nullable**: Nem

##### `description`

A konfiguráció részletes leírása.

- **Típus**: `Text`
- **Nullable**: Igen

##### `is_active`

A konfiguráció aktív-e.

- **Típus**: `Boolean`
- **Default**: `True`
- **Nullable**: Nem

#### Indexek

- `idx_dynamic_config_category_active`: Kategória és aktív állapot indexe
- `idx_dynamic_config_key_active`: Kulcs és aktív állapot indexe

#### Metódusok

##### `__repr__()`

Modell string reprezentációja.

**Visszatérési érték:**
- `str`: A modell rövid string reprezentációja.

### `LogEntry`

Rendszer naplóbejegyzéseket tároló modell.

Ez a modell tárolja a rendszer által generált naplóbejegyzéseket strukturált formában az adatbázisban.

#### Attribútumok

- `level`: A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `logger_name`: A logger neve.
- `message`: A naplóüzenet.
- `module`: A modul neve, ahonnan a napló született.
- `function`: A függvény neve, ahonnan a napló született.
- `line_number`: A sor száma, ahonnan a napló született.
- `process_id`: A folyamat azonosítója.
- `thread_id`: A szál azonosítója.
- `exception_type`: A kivétel típusa (ha van).
- `exception_message`: A kivétel üzenete (ha van).
- `traceback`: A traceback információ (ha van).
- `extra_data`: További egyéni adatok (JSON formátumban).

#### Oszlop Definíciók

##### `level`

A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL).

- **Típus**: `String(20)`
- **Indexelt**: Igen
- **Nullable**: Nem

##### `logger_name`

A logger neve.

- **Típus**: `String(255)`
- **Indexelt**: Igen
- **Nullable**: Nem

##### `message`

A naplóüzenet.

- **Típus**: `Text`
- **Nullable**: Nem

##### `module`

A modul neve, ahonnan a napló született.

- **Típus**: `String(255)`
- **Nullable**: Igen

##### `function`

A függvény neve, ahonnan a napló született.

- **Típus**: `String(255)`
- **Nullable**: Igen

##### `line_number`

A sor száma, ahonnan a napló született.

- **Típus**: `Integer`
- **Nullable**: Igen

##### `process_id`

A folyamat azonosítója.

- **Típus**: `Integer`
- **Nullable**: Igen

##### `thread_id`

A szál azonosítója.

- **Típus**: `Integer`
- **Nullable**: Igen

##### `exception_type`

A kivétel típusa (ha van).

- **Típus**: `String(255)`
- **Nullable**: Igen

##### `exception_message`

A kivétel üzenete (ha van).

- **Típus**: `Text`
- **Nullable**: Igen

##### `traceback`

A traceback információ (ha van).

- **Típus**: `Text`
- **Nullable**: Igen

##### `extra_data`

További egyéni adatok (JSON formátumban).

- **Típus**: `JSON`
- **Nullable**: Igen

#### Indexek

- `idx_log_entries_level_created`: Szint és létrehozási idő indexe
- `idx_log_entries_logger_created`: Logger név és létrehozási idő indexe

#### Metódusok

##### `__repr__()`

Modell string reprezentációja.

**Visszatérési érték:**
- `str`: A modell rövid string reprezentációja.

## Használati Példák

### DynamicConfig használata

```python
from neural_ai.core.db.implementations.models import DynamicConfig
from neural_ai.core.db import get_db_session
from sqlalchemy import select

# Konfiguráció létrehozása
config = DynamicConfig(
    key="max_risk_per_trade",
    value=0.02,
    value_type="float",
    category="risk",
    description="Maximális kockázat egy kereskedésre (2%)",
    is_active=True
)

# Konfiguráció mentése
async with get_db_session() as session:
    session.add(config)
    await session.commit()

# Konfiguráció lekérdezése
async def get_config_value(key: str):
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(
            DynamicConfig.key == key,
            DynamicConfig.is_active == True
        )
        result = await session.execute(stmt)
        config = result.scalar_one_or_none()
        return config.value if config else None

# Összes aktív konfiguráció lekérdezése kategóriánként
async def get_configs_by_category(category: str):
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(
            DynamicConfig.category == category,
            DynamicConfig.is_active == True
        )
        result = await session.execute(stmt)
        return {config.key: config.value for config in result.scalars()}
```

### LogEntry használata

```python
from neural_ai.core.db.implementations.models import LogEntry
from neural_ai.core.db import get_db_session
from sqlalchemy import select, desc
import logging

# Naplóbejegyzés létrehozása
log_entry = LogEntry(
    level="ERROR",
    logger_name="trading.engine",
    message="Sikertelen rendelés küldés",
    module="trading_engine",
    function="send_order",
    line_number=245,
    process_id=12345,
    thread_id=67890,
    exception_type="OrderError",
    exception_message="Nincs elég egyenleg",
    traceback="Traceback...",
    extra_data={"order_id": 123, "symbol": "EURUSD"}
)

# Napló mentése
async with get_db_session() as session:
    session.add(log_entry)
    await session.commit()

# Hibák lekérdezése
async def get_recent_errors(limit: int = 50):
    async with get_db_session() as session:
        stmt = (
            select(LogEntry)
            .where(LogEntry.level.in_(["ERROR", "CRITICAL"]))
            .order_by(desc(LogEntry.created_at))
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

# Naplók lekérdezése logger név alapján
async def get_logs_by_logger(logger_name: str, hours: int = 24):
    from datetime import datetime, timedelta
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    async with get_db_session() as session:
        stmt = (
            select(LogEntry)
            .where(
                LogEntry.logger_name == logger_name,
                LogEntry.created_at >= start_time
            )
            .order_by(LogEntry.created_at)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
```

### Komplex lekérdezések

```python
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta

# Statisztikák lekérdezése
async def get_log_statistics():
    async with get_db_session() as session:
        # Összes naplóbejegyzés száma
        total_stmt = select(func.count(LogEntry.id))
        total = (await session.execute(total_stmt)).scalar()
        
        # Hibák száma az elmúlt 24 órában
        start_time = datetime.utcnow() - timedelta(hours=24)
        error_stmt = select(func.count(LogEntry.id)).where(
            and_(
                LogEntry.level.in_(["ERROR", "CRITICAL"]),
                LogEntry.created_at >= start_time
            )
        )
        errors = (await session.execute(error_stmt)).scalar()
        
        # Leggyakoribb logger nevek
        logger_stmt = (
            select(LogEntry.logger_name, func.count(LogEntry.id).label('count'))
            .group_by(LogEntry.logger_name)
            .order_by(desc('count'))
            .limit(10)
        )
        top_loggers = (await session.execute(logger_stmt)).all()
        
        return {
            'total_logs': total,
            'errors_last_24h': errors,
            'top_loggers': [{'name': name, 'count': count} for name, count in top_loggers]
        }
```

### Konfiguráció frissítése

```python
from sqlalchemy import update

async def update_config(key: str, new_value: any):
    """Konfiguráció frissítése."""
    async with get_db_session() as session:
        stmt = (
            update(DynamicConfig)
            .where(DynamicConfig.key == key)
            .values(value=new_value, updated_at=datetime.utcnow())
        )
        result = await session.execute(stmt)
        await session.commit()
        
        return result.rowcount > 0
```

## Adatbázis Séma

### dynamic_configs tábla

```sql
CREATE TABLE dynamic_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(255) UNIQUE NOT NULL,
    value JSON NOT NULL,
    value_type VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_dynamic_config_category_active (category, is_active),
    INDEX idx_dynamic_config_key_active (key, is_active)
);
```

### log_entries tábla

```sql
CREATE TABLE log_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(20) NOT NULL,
    logger_name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    module VARCHAR(255),
    function VARCHAR(255),
    line_number INTEGER,
    process_id INTEGER,
    thread_id INTEGER,
    exception_type VARCHAR(255),
    exception_message TEXT,
    traceback TEXT,
    extra_data JSON,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_log_entries_level_created (level, created_at),
    INDEX idx_log_entries_logger_created (logger_name, created_at)
);
```

## Kapcsolódó Dokumentáció

- [Model Base](model_base.md)
- [SQLAlchemy Session](sqlalchemy_session.md)
- [DB Implementációk](__init__.md)
- [DB Modul](../__init__.md)