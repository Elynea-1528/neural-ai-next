# DB Implementációk Modul

## Áttekintés

Adatbázis implementációk a Neural AI Next rendszerhez.

Ez a modul tartalmazza az adatbázis műveletek konkrét implementációit.

## Exportált Komponensek

### Modellek

- [`Base`](model_base.md#base): SQLAlchemy deklaratív alaposztály
- [`DynamicConfig`](models.md#dynamicconfig): Dinamikus konfigurációs értékek tárolására
- [`LogEntry`](models.md#logentry): Rendszer naplóbejegyzéseket tároló modell

### Session Függvények

- [`get_db_session`](sqlalchemy_session.md#get_db_session): Dependency injection függvény FastAPI-hoz
- [`get_db_session_direct`](sqlalchemy_session.md#get_db_session_direct): Közvetlen adatbázis session lekérdezése
- [`get_engine`](sqlalchemy_session.md#get_engine): Globális adatbázis engine lekérdezése
- [`get_async_session_maker`](sqlalchemy_session.md#get_async_session_maker): AsyncSession factory lekérdezése
- [`init_db`](sqlalchemy_session.md#init_db): Adatbázis inicializálása
- [`close_db`](sqlalchemy_session.md#close_db): Adatbázis kapcsolat lezárása

### Osztályok

- [`DatabaseManager`](sqlalchemy_session.md#databasemanager): Adatbázis kezelő osztály

### Segédfüggvények

- [`get_database_url`](sqlalchemy_session.md#get_database_url): Adatbázis URL lekérdezése
- [`create_engine`](sqlalchemy_session.md#create_engine): Aszinkron adatbázis engine létrehozása

## Használati Példák

### Modellek használata

```python
from neural_ai.core.db.implementations.models import DynamicConfig, LogEntry
from neural_ai.core.db.implementations.model_base import Base
from sqlalchemy import Column, String, Integer

# Egyéni modell létrehozása
class MyCustomModel(Base):
    __tablename__ = 'custom_models'
    
    name = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)

# Modell használata
config = DynamicConfig(
    key="my_config",
    value={"setting": "value"},
    value_type="dict",
    category="system"
)
```

### Session függvények használata

```python
from neural_ai.core.db.implementations.sqlalchemy_session import (
    get_db_session,
    get_db_session_direct,
    init_db,
    close_db
)
import asyncio

async def example_usage():
    # Adatbázis inicializálása
    await init_db()
    
    # Session használata context managerrel
    async with get_db_session() as session:
        # Adatbázis műveletek...
        pass
    
    # Közvetlen session használata
    session = await get_db_session_direct()
    try:
        # Adatbázis műveletek...
        await session.commit()
    finally:
        await session.close()
    
    # Adatbázis lezárása
    await close_db()

if __name__ == "__main__":
    asyncio.run(example_usage())
```

### DatabaseManager használata

```python
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
from neural_ai.core.config import ConfigManagerFactory
import asyncio

async def main():
    config_manager = ConfigManagerFactory.get_manager("config.yml")
    db_manager = DatabaseManager(config_manager)
    
    # Inicializálás
    await db_manager.initialize()
    
    # Session használata
    async with db_manager.get_session() as session:
        # Adatbázis műveletek...
        pass
    
    # Lezárás
    await db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Kapcsolódó Dokumentáció

- [Modellek](models.md)
- [Model Base](model_base.md)
- [SQLAlchemy Session](sqlalchemy_session.md)
- [DB Modul](../__init__.md)