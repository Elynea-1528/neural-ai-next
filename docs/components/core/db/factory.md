# core/db/factory.py

Adatbázis factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kezelő komponensek létrehozását a factory
minta segítségével, beleértve a session maker-t és a DatabaseManager-t.

## Osztályok

### `DatabaseFactory`

Factory osztály adatbázis komponensek létrehozásához.

    Ez az osztály felelős az adatbázis kezelő komponensek példányosításáért,
    beleértve a session factory-ket és a DatabaseManager-t.


## Függvények

### `get_session_maker`

Session maker létrehozása vagy visszaadása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az async_sessionmaker objektum.

### `get_engine`

Adatbázis engine létrehozása vagy visszaadása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az SQLAlchemy async engine.

### `create_engine`

Egyéni adatbázis engine létrehozása.

        Args:
            db_url: Az adatbázis URL.
            echo: SQL lekérdezések naplózásának engedélyezése.

        Returns:
            Az létrehozott SQLAlchemy async engine.

### `create_manager`

DatabaseManager példány létrehozása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az inicializált DatabaseManager példány.


---

**Forrásfájl:** [`core/db/factory.py`](../../../neural_ai/core/db/factory.py)
