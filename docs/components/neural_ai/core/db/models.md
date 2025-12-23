# Adatbázis Modellek

## Áttekintés

Ez a dokumentáció ismerteti a Neural AI Next rendszer adatbázis modelleket, beleértve a `DynamicConfig` és `LogEntry` modelleket, amelyek a rendszer alapvető adattárolási rétegét alkotják.

## Modell Architektúra

### Öröklési Fa

```
Base (DeclarativeBase)
├── DynamicConfig
│   └── dynamic_configs tábla
└── LogEntry
    └── log_entries tábla
```

### Tábla Kapcsolatok

```
┌─────────────────────┐
│   dynamic_configs   │
├─────────────────────┤
│ id (PK)             │
│ key (UNIQUE)        │
│ value (JSON)        │
│ value_type          │
│ category            │
│ description         │
│ is_active           │
│ created_at          │
│ updated_at          │
└─────────────────────┘

┌─────────────────────┐
│     log_entries     │
├─────────────────────┤
│ id (PK)             │
│ level               │
│ logger_name         │
│ message             │
│ module              │
│ function            │
│ line_number         │
│ process_id          │
│ thread_id           │
│ exception_type      │
│ exception_message   │
│ traceback           │
│ extra_data (JSON)   │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

## DynamicConfig Modell

### Cél és Felhasználás

A `DynamicConfig` modell a futás közben módosítható konfigurációs értékek tárolására szolgál. Ezek a konfigurációk hot reload támogatással rendelkeznek, azaz az alkalmazás azonnal érzékeli a változásokat.

### Mezők

| Mező | Típus | Leírás | Kötelező |
|------|-------|--------|----------|
| `id` | Integer | Elsődleges kulcs, autoincrement | ✅ |
| `key` | String(255) | Konfigurációs kulcs (egyedi) | ✅ |
| `value` | JSON | Konfigurációs érték | ✅ |
| `value_type` | String(50) | Érték típusa (int, float, str, bool, list, dict) | ✅ |
| `category` | String(100) | Konfiguráció kategóriája | ✅ |
| `description` | Text | Részletes leírás | ❌ |
| `is_active` | Boolean | Aktív-e a konfiguráció | ✅ |
| `created_at` | DateTime | Létrehozás időpontja (UTC) | ✅ |
| `updated_at` | DateTime | Utolsó módosítás időpontja (UTC) | ✅ |

### Kategóriák

- **risk**: Kockázatkezelési paraméterek
- **strategy**: Stratégia konfigurációk
- **trading**: Kereskedési beállítások
- **system**: Rendszer szintű konfigurációk

### Példa Használat

#### Létrehozás

```python
from neural_ai.core.db.models import DynamicConfig
from neural_ai.core.db.session import get_db_session

async def create_config():
    """Konfiguráció létrehozása."""
    async with get_db_session() as session:
        config = DynamicConfig(
            key="risk.max_position_size_percent",
            value=2.5,
            value_type="float",
            category="risk",
            description="Maximum pozícióméret a portfólió százalékában"
        )
        session.add(config)
        await session.commit()
        return config
```

#### Olvasás

```python
from sqlalchemy import select

async def get_config(key: str):
    """Konfiguráció lekérdezése kulcs alapján."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(
            DynamicConfig.key == key,
            DynamicConfig.is_active == True
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
```

#### Frissítés

```python
async def update_config(key: str, value: Any):
    """Konfiguráció frissítése."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(DynamicConfig.key == key)
        result = await session.execute(stmt)
        config = result.scalar_one()
        
        config.value = value
        config.value_type = type(value).__name__
        
        await session.commit()
        return config
```

#### Törlés (Soft Delete)

```python
async def deactivate_config(key: str):
    """Konfiguráció inaktiválása."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(DynamicConfig.key == key)
        result = await session.execute(stmt)
        config = result.scalar_one()
        
        config.is_active = False
        await session.commit()
```

### Indexek

- `idx_dynamic_config_category_active`: Kategória és aktív státusz
- `idx_dynamic_config_key_active`: Kulcs és aktív státusz

### Érték Típusok

```python
# Integer érték
config = DynamicConfig(
    key="system.max_retries",
    value=3,
    value_type="int",
    category="system"
)

# Float érték
config = DynamicConfig(
    key="risk.max_daily_loss_percent",
    value=5.0,
    value_type="float",
    category="risk"
)

# String érték
config = DynamicConfig(
    key="trading.active_symbols",
    value="EURUSD,GBPUSD,XAUUSD",
    value_type="str",
    category="trading"
)

# Boolean érték
config = DynamicConfig(
    key="strategy.d1_enabled",
    value=True,
    value_type="bool",
    category="strategy"
)

# Lista érték
config = DynamicConfig(
    key="trading.active_pairs",
    value=["EURUSD", "GBPUSD", "XAUUSD"],
    value_type="list",
    category="trading"
)

# Dictionary érték
config = DynamicConfig(
    key="risk.position_sizes",
    value={"EURUSD": 0.01, "XAUUSD": 0.005},
    value_type="dict",
    category="risk"
)
```

## LogEntry Modell

### Cél és Felhasználás

A `LogEntry` modell a rendszer naplóbejegyzéseit tárolja strukturált formában az adatbázisban. Ez lehetővé teszi a naplók hatékony szűrését, rendezését és elemzését.

### Mezők

| Mező | Típus | Leírás | Kötelező |
|------|-------|--------|----------|
| `id` | Integer | Elsődleges kulcs, autoincrement | ✅ |
| `level` | String(20) | Napló szintje | ✅ |
| `logger_name` | String(255) | Logger neve | ✅ |
| `message` | Text | Naplóüzenet | ✅ |
| `module` | String(255) | Modul neve | ❌ |
| `function` | String(255) | Függvény neve | ❌ |
| `line_number` | Integer | Sor száma | ❌ |
| `process_id` | Integer | Folyamat azonosító | ❌ |
| `thread_id` | Integer | Szál azonosító | ❌ |
| `exception_type` | String(255) | Kivétel típusa | ❌ |
| `exception_message` | Text | Kivétel üzenete | ❌ |
| `traceback` | Text | Traceback információ | ❌ |
| `extra_data` | JSON | Egyéni adatok | ❌ |
| `created_at` | DateTime | Létrehozás időpontja (UTC) | ✅ |
| `updated_at` | DateTime | Utolsó módosítás időpontja (UTC) | ✅ |

### Napló Szintek

- **DEBUG**: Részletes hibakeresési információk
- **INFO**: Általános tájékoztató üzenetek
- **WARNING**: Figyelmeztetések
- **ERROR**: Hibaüzenetek
- **CRITICAL**: Kritikus hibák

### Példa Használat

#### Egyszerű Napló Létrehozása

```python
from neural_ai.core.db.models import LogEntry
from neural_ai.core.db.session import get_db_session

async def log_info_message():
    """Információs naplóbejegyzés létrehozása."""
    async with get_db_session() as session:
        log_entry = LogEntry(
            level="INFO",
            logger_name="data_collector",
            message="Adatgyűjtés elindult",
            module="collectors/mt5/server.py",
            function="start_collection",
            line_number=42
        )
        session.add(log_entry)
        await session.commit()
```

#### Hiba Naplózása Kivétellel

```python
import traceback

async def log_error_with_exception():
    """Hiba naplózása kivétel információkkal."""
    try:
        # Valami kockázatos művelet
        result = risky_operation()
    except Exception as e:
        async with get_db_session() as session:
            log_entry = LogEntry(
                level="ERROR",
                logger_name="risk_manager",
                message="Hiba történt a kockázatkezelés során",
                exception_type=type(e).__name__,
                exception_message=str(e),
                traceback=traceback.format_exc(),
                extra_data={
                    "user_id": 123,
                    "request_id": "abc-def-ghi"
                }
            )
            session.add(log_entry)
            await session.commit()
```

#### Naplók Lekérdezése

```python
from sqlalchemy import select
from datetime import datetime, timedelta

async def get_recent_errors():
    """Utolsó 24 óra ERROR szintű naplóinak lekérdezése."""
    async with get_db_session() as session:
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        stmt = select(LogEntry).where(
            LogEntry.level == "ERROR",
            LogEntry.created_at >= cutoff_time
        ).order_by(LogEntry.created_at.desc())
        
        result = await session.execute(stmt)
        return result.scalars().all()
```

### Indexek

- `idx_log_entries_level_created`: Szint és létrehozás időpontja
- `idx_log_entries_logger_created`: Logger név és létrehozás időpontja

## Base Osztály

### Közös Funkcionalitás

A `Base` osztály biztosítja az összes modell által használt alapvető funkcionalitást.

#### Mezők

- `id`: Elsődleges kulcs
- `created_at`: Létrehozás időpontja
- `updated_at`: Utolsó módosítás időpontja

#### Metódusok

```python
class Base(DeclarativeBase):
    """SQLAlchemy deklaratív alaposztály."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Modell átalakítása dictionary formátumba."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result
    
    def __repr__(self) -> str:
        """Modell string reprezentációja."""
        class_name = self.__class__.__name__
        return f"<{class_name}(id={self.id})>"
```

### Automatikus Táblanév Generálás

A `Base` osztály automatikusan generálja a táblaneveket a class nevek alapján:

```python
DynamicConfig -> dynamic_configs
LogEntry -> log_entries
```

## CRUD Műveletek

### Tömeges Műveletek

#### Batch Insert

```python
async def bulk_insert_configs():
    """Tömeges konfiguráció beszúrás."""
    configs = [
        DynamicConfig(
            key=f"config.{i}",
            value=i * 10,
            value_type="int",
            category="test"
        )
        for i in range(1000)
    ]
    
    async with get_db_session() as session:
        session.add_all(configs)
        await session.commit()
```

#### Batch Update

```python
from sqlalchemy import update

async def bulk_update_category(old_cat: str, new_cat: str):
    """Kategória tömeges frissítése."""
    async with get_db_session() as session:
        stmt = update(DynamicConfig).where(
            DynamicConfig.category == old_cat
        ).values(category=new_cat)
        
        await session.execute(stmt)
        await session.commit()
```

### Komplex Lekérdezések

#### Szűrés És Rendezés

```python
from sqlalchemy import and_, or_

async def get_active_risk_configs():
    """Aktív risk kategóriájú konfigok lekérdezése."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(
            and_(
                DynamicConfig.category == "risk",
                DynamicConfig.is_active == True
            )
        ).order_by(
            DynamicConfig.key.asc(),
            DynamicConfig.updated_at.desc()
        )
        
        result = await session.execute(stmt)
        return result.scalars().all()
```

#### Aggregációk

```python
from sqlalchemy import func

async def get_config_stats():
    """Konfiguráció statisztikák."""
    async with get_db_session() as session:
        # Konfigok száma kategóriánként
        stmt = select(
            DynamicConfig.category,
            func.count(DynamicConfig.id).label('count')
        ).group_by(DynamicConfig.category)
        
        result = await session.execute(stmt)
        return result.all()
```

## Adatbiztonság

### Validáció

A modellek automatikusan validálják a bemeneti adatokat:

```python
# Hiba: Túl hosszú kulcs
config = DynamicConfig(key="x" * 256, ...)  # ValueError

# Hiba: Érvénytelen value_type
config = DynamicConfig(value_type="invalid", ...)  # ValidationError
```

### Constraint-ek

- **Unique Constraint**: `key` mező egyediségének garantálása
- **Check Constraint**: `value_type` érvényességének ellenőrzése
- **Not Null**: Kötelező mezők kitöltésének ellenőrzése

## Teljesítmény Optimalizálás

### Indexelés

A gyakran használt lekérdezések optimalizálása:

```python
# Gyors keresés kulcs alapján
stmt = select(DynamicConfig).where(DynamicConfig.key == "test.key")

# Gyors szűrés kategória és aktív státusz alapján
stmt = select(DynamicConfig).where(
    DynamicConfig.category == "risk",
    DynamicConfig.is_active == True
)
```

### Pagináció

```python
from sqlalchemy import desc

async def get_logs_paginated(page: int = 1, per_page: int = 50):
    """Naplók lapozható lekérdezése."""
    async with get_db_session() as session:
        stmt = select(LogEntry).order_by(
            desc(LogEntry.created_at)
        ).offset((page - 1) * per_page).limit(per_page)
        
        result = await session.execute(stmt)
        return result.scalars().all()
```

## Tesztelés

### Unit Tesztek

```bash
# Modellek CRUD tesztek
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/test_models.py -v
```

### Teszt Adatok

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_dynamic_config_crud(async_session: AsyncSession):
    """DynamicConfig CRUD műveletek tesztelése."""
    # Create
    config = DynamicConfig(...)
    async_session.add(config)
    await async_session.commit()
    
    # Read
    stmt = select(DynamicConfig).where(DynamicConfig.id == config.id)
    result = await async_session.execute(stmt)
    fetched = result.scalar_one()
    
    assert fetched.key == config.key
    
    # Update
    fetched.value = "new_value"
    await async_session.commit()
    
    # Delete
    await async_session.delete(fetched)
    await async_session.commit()
```

## Kapcsolódó Dokumentáció

- [Session Kezelés](session.md) - Adatbázis session factory
- [Dinamikus Konfiguráció](../../../planning/specs/02_dynamic_configuration.md)
- [Fejlesztési Útmutató](../../../development/unified_development_guide.md)