# Adatbázis Session Kezelő

## Áttekintés

Ez a dokumentáció ismerteti a Neural AI Next rendszer adatbázis session kezelőjét, amely aszinkron adatbázis műveleteket tesz lehetővé SQLAlchemy 2.0 és asyncpg/aiosqlite segítségével.

## Architektúra

### Session Factory Pattern

A rendszer Factory pattern-t használ az AsyncSession objektumok létrehozásához, biztosítva a hatékony kapcsolatkezelést és a tranzakciók automatikus kezelését.

```
┌─────────────────────────────────────────┐
│         Database Session Layer          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────┐      │
│  │   DatabaseManager            │      │
│  │   - initialize()             │      │
│  │   - get_session()            │      │
│  │   - close()                  │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   get_db_session()           │      │
│  │   (Context Manager)          │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   async_sessionmaker         │      │
│  │   (SQLAlchemy Factory)       │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   create_async_engine()      │      │
│  │   (Connection Pool)          │      │
│  └──────────────────────────────┘      │
│                                         │
└─────────────────────────────────────────┘
```

## Fő Komponensek

### 1. DatabaseManager Osztály

Magas szintű interfész az adatbázis műveletekhez.

#### Metódusok

```python
class DatabaseManager:
    """Adatbázis kezelő osztály."""
    
    def __init__(self, config_manager: Optional[IConfigManager] = None):
        """Inicializálja az adatbázis kezelőt."""
    
    async def initialize(self) -> None:
        """Adatbázis inicializálása és táblák létrehozása."""
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Session lekérdezése context managerrel."""
    
    async def close(self) -> None:
        """Kapcsolat lezárása."""
```

#### Példa Használat

```python
from neural_ai.core.db.session import DatabaseManager
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory
)

# Inicializálás
config_manager = ConfigManagerFactory.get_manager()
db_manager = DatabaseManager(config_manager)
await db_manager.initialize()

# Session használata
async with db_manager.get_session() as session:
    result = await session.execute(select(DynamicConfig))
    configs = result.scalars().all()

# Lezárás
await db_manager.close()
```

### 2. get_db_session() Context Manager

Automatikus tranzakciókezelés biztosítása.

#### Jellemzők

- **Automatikus Commit:** Sikeres művelet után automatikusan commitol
- **Automatikus Rollback:** Hiba esetén automatikusan visszagörget
- **Automatikus Lezárás:** Minden esetben lezárja a session-t

#### Példa Használat

```python
from neural_ai.core.db.session import get_db_session

async def get_all_configs():
    """Összes konfiguráció lekérdezése."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig).where(
            DynamicConfig.is_active == True
        )
        result = await session.execute(stmt)
        return result.scalars().all()
```

### 3. Globális Függvények

#### get_database_url()

Adatbázis URL lekérdezése a konfigurációból.

```python
from neural_ai.core.db.session import get_database_url

# Alapértelmezett konfigurációval
db_url = get_database_url()

# Egyéni konfigurációval
custom_config = MockConfigManager()
db_url = get_database_url(custom_config)
```

#### create_engine()

Aszinkron adatbázis engine létrehozása.

```python
from neural_ai.core.db.session import create_engine

# SQLite engine
engine = create_engine("sqlite+aiosqlite:///neural_ai.db")

# PostgreSQL engine
engine = create_engine("postgresql+asyncpg://user:pass@localhost/db")
```

#### init_db() és close_db()

Adatbázis inicializálás és lezárás.

```python
from neural_ai.core.db.session import init_db, close_db

# Alkalmazás indításakor
await init_db()

# Alkalmazás leállításakor
await close_db()
```

## Konfiguráció

### Adatbázis URL Formátumok

#### SQLite (Fejlesztés)

```python
DB_URL=sqlite+aiosqlite:///neural_ai.db
```

#### PostgreSQL (Produkció)

```python
DB_URL=postgresql+asyncpg://user:password@localhost:5432/neural_ai
```

### Környezeti Változók

```bash
# .env fájlban
DB_URL=sqlite+aiosqlite:///neural_ai.db
LOG_LEVEL=INFO
```

## Tranzakció Kezelés

### Automatikus Tranzakciók

A `get_db_session()` context manager automatikusan kezeli a tranzakciókat:

```python
async with get_db_session() as session:
    # Tranzakció automatikusan elindul
    
    # Műveletek
    config = DynamicConfig(key="test", value=42, ...)
    session.add(config)
    
    # Sikeres esetben automatikusan commit
# Hiba esetén automatikusan rollback
```

### Kivétel Kezelés

```python
async with get_db_session() as session:
    try:
        # Kockázatos művelet
        await session.execute(dangerous_operation)
    except Exception as e:
        # A context manager automatikusan rollbackel
        logger.error(f"Hiba történt: {e}")
        raise
```

## Kapcsolat Pool Kezelés

### SQLite

SQLite esetén nincs connection pool, minden session új kapcsolatot nyit:

```python
engine = create_async_engine(
    db_url,
    poolclass=NullPool,  # Nincs pool
    connect_args={"check_same_thread": False}
)
```

### PostgreSQL

PostgreSQL esetén connection pool használata:

```python
engine = create_async_engine(
    db_url,
    pool_size=20,        # Maximális 20 kapcsolat
    max_overflow=0       # Nincs overflow
)
```

## Teljesítmény Optimalizálás

### 1. Session Cache-elés

A session maker egyszer jön létre és gyorsítótárazódik:

```python
# Első hívás - létrehozza
session1 = await get_db_session_direct()

# Második hívás - újrahasznosítja
session2 = await get_db_session_direct()
```

### 2. Expire on Commit

A `expire_on_commit=False` beállítás optimalizálja a műveleteket:

```python
async_sessionmaker(engine, expire_on_commit=False)
```

### 3. Batch Műveletek

Tömeges adatbeszúrás optimalizálása:

```python
async with get_db_session() as session:
    configs = [
        DynamicConfig(key=f"config.{i}", value=i, ...)
        for i in range(1000)
    ]
    session.add_all(configs)  # Egyszeri hozzáadás
    await session.commit()    # Egyszeri commit
```

## Hibaelhárítás

### Gyakori Hibák

#### 1. Session Already Closed

```python
# Hiba: Session már lezárásra került
session = await get_db_session_direct()
await session.close()
await session.execute(select(...))  # Hiba!
```

**Megoldás:** Használd a context managert:

```python
async with get_db_session() as session:
    await session.execute(select(...))  # Biztonságos
```

#### 2. Transaction Rollback

```python
# Tranzakció már rollbackelve
async with get_db_session() as session:
    await session.rollback()  # Explicit rollback
    await session.commit()    # Hiba!
```

**Megoldás:** Hagyd a context managerra a rollback kezelést.

### Naplózás

Debug módban az összes SQL lekérdezés naplózásra kerül:

```python
# Ha LOG_LEVEL=DEBUG
engine = create_engine(db_url, echo=True)
```

## Biztonság

### Kapcsolat Biztonság

- **Titkosítás:** PostgreSQL esetén SSL/TLS titkosítás
- **Hitelesítés:** Jelszó alapú hitelesítés
- **Hozzáférés Szabályozás:** IP alapú szűrés

### Adatbiztonság

- **Tranzakciók:** ACID tulajdonságok garantálása
- **Rollback:** Hiba esetén automatikus visszagörgetés
- **Konzisztencia:** Adatbázis constraint-ekkel való védelem

## Tesztelés

### Unit Tesztek

```bash
# Session factory tesztek
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/test_session.py -v
```

### Integration Tesztek

```bash
# Teljes adatbázis réteg tesztelése
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/ -v
```

## Kapcsolódó Dokumentáció

- [Adatbázis Modellek](models.md) - DynamicConfig és LogEntry modellek
- [Konfiguráció Kezelés](../../config/implementations/config_manager_factory.md)
- [Fejlesztési Útmutató](../../../development/unified_development_guide.md)