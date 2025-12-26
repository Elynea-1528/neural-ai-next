# SQLAlchemy Session

## Áttekintés

Adatbázis session kezelő a Neural AI Next rendszerhez.

Ez a modul biztosítja az AsyncSession factory-t és a kapcsolódó segédfunkciókat az adatbázis műveletek aszinkron kezeléséhez.

## Globális Változók

- `_engine`: Globális adatbázis engine
- `_async_session_maker`: Globális session factory

## Függvények

### `get_database_url(config_manager)`

Adatbázis URL lekérdezése a konfigurációból.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő. Ha nincs megadva, létrehoz egy újat a ConfigManagerFactory segítségével.

**Visszatérési érték:**
- `str`: Az adatbázis URL string formátumban.

**Kivételek:**
- `DBConnectionError`: Ha az adatbázis URL nincs konfigurálva.

### `create_engine(db_url, echo)`

Aszinkron adatbázis engine létrehozása.

**Paraméterek:**
- `db_url`: Az adatbázis URL (pl. sqlite+aiosqlite:///neural_ai.db).
- `echo`: SQL lekérdezések naplózásának engedélyezése.

**Visszatérési érték:**
- `Any`: Az létrehozott SQLAlchemy async engine.

### `get_engine(config_manager)`

Globális adatbázis engine lekérdezése.

Ha az engine még nincs létrehozva, létrehozza azt a konfiguráció alapján.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**
- `Any`: A globális SQLAlchemy async engine.

### `get_async_session_maker(config_manager)`

AsyncSession factory lekérdezése.

Ha a session maker még nincs létrehozva, létrehozza azt.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**
- `Any`: Az async_sessionmaker objektum.

### `get_db_session()`

Dependency injection függvény a FastAPI számára.

Ez a függvény biztosítja az adatbázis session-t a request élettartamára. Automatikusan kezeli a session lezárását és a tranzakciók commit/rollback-jét.

**Visszatérési érték:**
- `AsyncGenerator[AsyncSession, None]`: Az adatbázis session context manager.

**Használati példa:**
```python
async def some_operation():
    async with get_db_session() as session:
        result = await session.execute(select(MyModel))
        return result.scalars().all()
```

### `get_db_session_direct()`

Közvetlen adatbázis session lekérdezése.

Ez a függvény manuális session kezelést tesz lehetővé. A hívó felelőssége a session lezárása.

**Visszatérési érték:**
- `AsyncSession`: Az adatbázis session.

**Használati példa:**
```python
async def some_operation():
    session = await get_db_session_direct()
    try:
        result = await session.execute(select(MyModel))
        await session.commit()
        return result.scalars().all()
    finally:
        await session.close()
```

### `init_db()`

Adatbázis inicializálása.

Létrehozza az összes táblát az adatbázisban a modellek alapján. Ez a függvény az alkalmazás indításakor hívandó.

### `close_db()`

Adatbázis kapcsolat lezárása.

Ez a függvény az alkalmazás leállításakor hívandó.

## Osztályok

### `DatabaseManager`

Adatbázis kezelő osztály a Neural AI Next rendszerhez.

Ez az osztály magas szintű interfészt biztosít az adatbázis műveletekhez, beleértve a session kezelést, inicializálást és lezárást.

#### Attribútumok

- `config_manager`: A konfiguráció kezelő példány.
- `_engine`: A belső adatbázis engine.
- `_session_maker`: A belső session factory.

#### Metódusok

##### `__init__(config_manager)`

Inicializálja az adatbázis kezelőt.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

##### `initialize()`

Adatbázis inicializálása a kezelővel.

Létrehozza az engine-t és a session maker-t, majd létrehozza a táblákat.

##### `get_session()`

Session lekérdezése a kezelőből.

**Visszatérési érték:**
- `AsyncGenerator[AsyncSession, None]`: Az adatbázis session context manager.

**Kivételek:**
- `RuntimeError`: Ha a kezelő nincs inicializálva.

##### `close()`

Adatbázis kapcsolat lezárása.

Felszabadítja az engine erőforrásait.

## Használati Példák

### Alap adatbázis inicializálás

```python
from neural_ai.core.db.implementations.sqlalchemy_session import init_db, close_db
import asyncio

async def main():
    # Adatbázis inicializálása
    await init_db()
    print("Adatbázis inicializálva")
    
    # Alkalmazás logika...
    
    # Adatbázis lezárása
    await close_db()
    print("Adatbázis lezárva")

if __name__ == "__main__":
    asyncio.run(main())
```

### Session használata context managerrel

```python
from neural_ai.core.db.implementations.sqlalchemy_session import get_db_session
from neural_ai.core.db.implementations.models import DynamicConfig
from sqlalchemy import select

async def get_all_configs():
    """Összes konfiguráció lekérdezése."""
    async with get_db_session() as session:
        stmt = select(DynamicConfig)
        result = await session.execute(stmt)
        configs = result.scalars().all()
        return [config.to_dict() for config in configs]

async def add_config(key, value, value_type, category):
    """Új konfiguráció hozzáadása."""
    config = DynamicConfig(
        key=key,
        value=value,
        value_type=value_type,
        category=category,
        is_active=True
    )
    
    async with get_db_session() as session:
        session.add(config)
        await session.commit()
        return config.id
```

### Közvetlen session használata

```python
from neural_ai.core.db.implementations.sqlalchemy_session import get_db_session_direct
from neural_ai.core.db.implementations.models import LogEntry

async def log_error(message, **kwargs):
    """Hiba naplózása az adatbázisba."""
    log_entry = LogEntry(
        level="ERROR",
        logger_name="application",
        message=message,
        **kwargs
    )
    
    session = await get_db_session_direct()
    try:
        session.add(log_entry)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
    finally:
        await session.close()
```

### DatabaseManager használata

```python
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.config import ConfigManagerFactory
import asyncio

async def main():
    # Konfiguráció betöltése
    config_manager = ConfigManagerFactory.get_manager("config.yml")
    
    # DatabaseManager létrehozása
    db_manager = DatabaseManager(config_manager)
    
    # Inicializálás
    await db_manager.initialize()
    print("DatabaseManager inicializálva")
    
    # Session használata
    async with db_manager.get_session() as session:
        # Adatbázis műveletek...
        print("Session használatban")
    
    # Lezárás
    await db_manager.close()
    print("DatabaseManager lezárva")

if __name__ == "__main__":
    asyncio.run(main())
```

### Egyéni engine létrehozása

```python
from neural_ai.core.db.implementations.sqlalchemy_session import create_engine
import asyncio

async def test_connection():
    # Egyéni engine létrehozása
    engine = create_engine(
        "sqlite+aiosqlite:///test.db",
        echo=True  # SQL lekérdezések naplózása
    )
    
    # Kapcsolódás tesztelése
    async with engine.begin() as conn:
        print("Sikeres kapcsolódás")
    
    # Engine lezárása
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
```

### Tranzakció kezelés

```python
from neural_ai.core.db.implementations.sqlalchemy_session import get_db_session
from neural_ai.core.db.implementations.models import DynamicConfig, LogEntry
from sqlalchemy import update

async def update_config_and_log(config_id, new_value, log_message):
    """Konfiguráció frissítése és naplózás tranzakcióban."""
    async with get_db_session() as session:
        try:
            # Tranzakció indítása
            await session.begin()
            
            # Konfiguráció frissítése
            stmt = (
                update(DynamicConfig)
                .where(DynamicConfig.id == config_id)
                .values(value=new_value)
            )
            await session.execute(stmt)
            
            # Naplóbejegyzés hozzáadása
            log_entry = LogEntry(
                level="INFO",
                logger_name="config",
                message=log_message,
                extra_data={"config_id": config_id, "new_value": new_value}
            )
            session.add(log_entry)
            
            # Tranzakció commit
            await session.commit()
            print("Tranzakció sikeres")
            
        except Exception as e:
            # Hiba esetén rollback
            await session.rollback()
            print(f"Tranzakció sikertelen: {e}")
            raise
```

## Adatbázis Támogatás

### SQLite

```python
# SQLite adatbázis URL
db_url = "sqlite+aiosqlite:///neural_ai.db"

# Engine létrehozása SQLite-hoz
engine = create_engine(db_url, echo=False)
```

### PostgreSQL

```python
# PostgreSQL adatbázis URL
db_url = "postgresql+asyncpg://user:password@localhost/neural_ai"

# Engine létrehozása PostgreSQL-hez
engine = create_engine(db_url, echo=False)
```

## Teljesítményoptimalizálás

### Connection Pool

```python
# PostgreSQL esetén connection pool használata
engine = create_async_engine(
    db_url,
    pool_size=20,      # Maximális kapcsolatok száma
    max_overflow=0,    # Túlfolyó kapcsolatok száma
    pool_recycle=3600  # Kapcsolatok újrahasznosítása (másodpercben)
)
```

### SQLite optimalizálás

```python
# SQLite esetén pool tiltása
engine = create_async_engine(
    db_url,
    poolclass=NullPool,  # Nincs connection pool
    connect_args={"check_same_thread": False}  # Többszálú hozzáférés engedélyezése
)
```

## Kapcsolódó Dokumentáció

- [Modellek](models.md)
- [Model Base](model_base.md)
- [DB Implementációk](__init__.md)
- [DB Modul](../__init__.md)