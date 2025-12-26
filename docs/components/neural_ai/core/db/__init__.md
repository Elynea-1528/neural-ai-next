# Neural AI Core DB Modul

## Áttekintés

Adatbázis modul a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kapcsolat kezelést, modelleket és session factory-t az aszinkron adatbázis műveletekhez.

## Exportált Komponensek

### Modellek

- [`Base`](implementations/model_base.md#base): SQLAlchemy deklaratív alaposztály
- [`DynamicConfig`](implementations/models.md#dynamicconfig): Dinamikus konfigurációs értékek tárolására
- [`LogEntry`](implementations/models.md#logentry): Rendszer naplóbejegyzéseket tároló modell

### Session Függvények

- [`get_db_session`](implementations/sqlalchemy_session.md#get_db_session): Dependency injection függvény FastAPI-hoz
- [`get_db_session_direct`](implementations/sqlalchemy_session.md#get_db_session_direct): Közvetlen adatbázis session lekérdezése
- [`get_engine`](implementations/sqlalchemy_session.md#get_engine): Globális adatbázis engine lekérdezése
- [`get_async_session_maker`](implementations/sqlalchemy_session.md#get_async_session_maker): AsyncSession factory lekérdezése
- [`init_db`](implementations/sqlalchemy_session.md#init_db): Adatbázis inicializálása
- [`close_db`](implementations/sqlalchemy_session.md#close_db): Adatbázis kapcsolat lezárása

### Osztályok

- [`DatabaseManager`](implementations/sqlalchemy_session.md#databasemanager): Adatbázis kezelő osztály
- [`DatabaseFactory`](factory.md#databasefactory): Factory osztály adatbázis komponensek létrehozásához

### Segédfüggvények

- [`get_database_url`](implementations/sqlalchemy_session.md#get_database_url): Adatbázis URL lekérdezése
- [`create_engine`](implementations/sqlalchemy_session.md#create_engine): Aszinkron adatbázis engine létrehozása

## Használati Példák

### Alap adatbázis inicializálás

```python
from neural_ai.core.db import init_db, close_db
import asyncio

async def main():
    # Adatbázis inicializálása
    await init_db()
    
    # Alkalmazás logika...
    
    # Adatbázis lezárása
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())
```

### Session használata

```python
from neural_ai.core.db import get_db_session
from neural_ai.core.db.implementations.models import DynamicConfig
from sqlalchemy import select

async def get_configs():
    async with get_db_session() as session:
        result = await session.execute(select(DynamicConfig))
        configs = result.scalars().all()
        return configs
```

### DatabaseManager használata

```python
from neural_ai.core.db import DatabaseManager
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

- [Kivételek](exceptions/)
- [Implementációk](implementations/)
- [Factory](factory.md)
- [Interfészek](interfaces/)