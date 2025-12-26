# DatabaseFactory

## Áttekintés

Adatbázis factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kezelő komponensek létrehozását a factory minta segítségével, beleértve a session maker-t és a DatabaseManager-t.

## Osztály

### `DatabaseFactory`

Factory osztály adatbázis komponensek létrehozásához.

Ez az osztály felelős az adatbázis kezelő komponensek példányosításáért, beleértve a session factory-ket és a DatabaseManager-t.

#### Statikus Metódusok

##### `get_session_maker(config_manager)`

Session maker létrehozása vagy visszaadása.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**
- `Any`: Az async_sessionmaker objektum.

##### `get_engine(config_manager)`

Adatbázis engine létrehozása vagy visszaadása.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**
- `Any`: Az SQLAlchemy async engine.

##### `create_engine(db_url, echo)`

Egyéni adatbázis engine létrehozása.

**Paraméterek:**
- `db_url`: Az adatbázis URL.
- `echo`: SQL lekérdezések naplózásának engedélyezése.

**Visszatérési érték:**
- `Any`: Az létrehozott SQLAlchemy async engine.

##### `create_manager(config_manager)`

DatabaseManager példány létrehozása.

**Paraméterek:**
- `config_manager`: Opcionális konfiguráció kezelő.

**Visszatérési érték:**
- `DatabaseManager`: Az inicializált DatabaseManager példány.

## Használati Példák

### Alap session maker használat

```python
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.config import ConfigManagerFactory

# Konfiguráció betöltése
config_manager = ConfigManagerFactory.get_manager("config.yml")

# Session maker létrehozása
session_maker = DatabaseFactory.get_session_maker(config_manager)

# Session használata
async with session_maker() as session:
    # Adatbázis műveletek...
    pass
```

### Egyéni engine létrehozása

```python
from neural_ai.core.db.factory import DatabaseFactory

# Egyéni adatbázis engine létrehozása
engine = DatabaseFactory.create_engine(
    db_url="sqlite+aiosqlite:///test.db",
    echo=True  # SQL lekérdezések naplózása
)
```

### DatabaseManager létrehozása

```python
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.config import ConfigManagerFactory
import asyncio

async def main():
    # Konfiguráció betöltése
    config_manager = ConfigManagerFactory.get_manager("config.yml")
    
    # DatabaseManager létrehozása
    db_manager = DatabaseFactory.create_manager(config_manager)
    
    # Inicializálás
    await db_manager.initialize()
    
    # Használat
    async with db_manager.get_session() as session:
        # Adatbázis műveletek...
        pass
    
    # Lezárás
    await db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Globális engine használata

```python
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.config import ConfigManagerFactory

# Konfiguráció betöltése
config_manager = ConfigManagerFactory.get_manager("config.yml")

# Globális engine lekérdezése
engine = DatabaseFactory.get_engine(config_manager)

# Engine használata
async with engine.begin() as conn:
    # Adatbázis műveletek...
    pass
```

## Tervezési Minta

A `DatabaseFactory` a **Factory Method** tervezési mintát valósítja meg, amely:

1. **Egységes interfészt biztosít**: Minden adatbázis komponens ugyanazon a factory-n keresztül érhető el
2. **Konfigurációfüggetlen**: A factory képes kezelni a különböző konfigurációs beállításokat
3. **Lazy loading**: A komponensek csak akkor jönnek létre, amikor először szükség van rájuk
4. **Tesztelhetőség**: Könnyen lehet mock-olni a factory-t tesztelés során

## Kapcsolódó Dokumentáció

- [DatabaseManager](implementations/sqlalchemy_session.md#databasemanager)
- [DB Modul](__init__.md)
- [Config Modul](../config/__init__.md)