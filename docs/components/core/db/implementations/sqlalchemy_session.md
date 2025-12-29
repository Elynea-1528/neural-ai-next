# core/db/implementations/sqlalchemy_session.py

Adatbázis session kezelő a Neural AI Next rendszerhez.

Ez a modul biztosítja az AsyncSession factory-t és a kapcsolódó segédfunkciókat
az adatbázis műveletek aszinkron kezeléséhez.

## Osztályok

### `DatabaseManager`

Adatbázis kezelő osztály a Neural AI Next rendszerhez.

    Ez az osztály magas szintű interfészt biztosít az adatbázis műveletekhez,
    beleértve a session kezelést, inicializálást és lezárást.

    Attributes:
        config_manager: A konfiguráció kezelő példány.


## Függvények

### `get_database_url`

Adatbázis URL lekérdezése a konfigurációból.

    Args:
        config_manager: Opcionális konfiguráció kezelő. Ha nincs megadva,
            létrehoz egy újat a ConfigManagerFactory segítségével.

    Returns:
        Az adatbázis URL string formátumban.

    Raises:
        ValueError: Ha az adatbázis URL nincs konfigurálva.

### `create_engine`

Aszinkron adatbázis engine létrehozása.

    Args:
        db_url: Az adatbázis URL (pl. sqlite+aiosqlite:///neural_ai.db).
        echo: SQL lekérdezések naplózásának engedélyezése.

    Returns:
        Az létrehozott SQLAlchemy async engine.

### `get_engine`

Globális adatbázis engine lekérdezése.

    Ha az engine még nincs létrehozva, létrehozza azt a konfiguráció alapján.

    Args:
        config_manager: Opcionális konfiguráció kezelő.

    Returns:
        A globális SQLAlchemy async engine.

### `get_async_session_maker`

AsyncSession factory lekérdezése.

    Ha a session maker még nincs létrehozva, létrehozza azt.

    Args:
        config_manager: Opcionális konfiguráció kezelő.

    Returns:
        Az async_sessionmaker objektum.

### `get_db_session`

Dependency injection függvény a FastAPI számára.

    Ez a függvény biztosítja az adatbázis session-t a request élettartamára.
    Automatikusan kezeli a session lezárását és a tranzakciók commit/rollback-jét.

    Yields:
        AsyncSession: Az adatbázis session.

    Example:
        ```python
        async def some_operation():
            async with get_db_session() as session:
                result = await session.execute(select(MyModel))
                return result.scalars().all()
        ```

### `get_db_session_direct`

Közvetlen adatbázis session lekérdezése.

    Ez a függvény manuális session kezelést tesz lehetővé.
    A hívó felelőssége a session lezárása.

    Returns:
        AsyncSession: Az adatbázis session.

    Example:
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

### `init_db`

Adatbázis inicializálása.

    Létrehozza az összes táblát az adatbázisban a modellek alapján.
    Ez a függvény az alkalmazás indításakor hívandó.

### `close_db`

Adatbázis kapcsolat lezárása.

    Ez a függvény az alkalmazás leállításakor hívandó.

### `__init__`

Inicializálja az adatbázis kezelőt.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

### `initialize`

Adatbázis inicializálása a kezelővel.

        Létrehozza az engine-t és a session maker-t, majd létrehozza a táblákat.

### `get_session`

Session lekérdezése a kezelőből.

        Yields:
            AsyncSession: Az adatbázis session.

        Raises:
            RuntimeError: Ha a kezelő nincs inicializálva.

### `get_active_configs`

Aktív dinamikus konfigurációk lekérdezése.

        Visszaadja az összes aktív dinamikus konfigurációt kulcs-érték párokként.

        Returns:
            Szótár az aktív konfigurációkulcsokkal és értékeikkel.

        Raises:
            RuntimeError: Ha a kezelő nincs inicializálva.

### `close`

Adatbázis kapcsolat lezárása.

        Felszabadítja az engine erőforrásait.


---

**Forrásfájl:** [`core/db/implementations/sqlalchemy_session.py`](../../../neural_ai/core/db/implementations/sqlalchemy_session.py)
