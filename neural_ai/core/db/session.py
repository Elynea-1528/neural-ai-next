"""Adatbázis session kezelő a Neural AI Next rendszerhez.

Ez a modul biztosítja az AsyncSession factory-t és a kapcsolódó segédfunkciókat
az adatbázis műveletek aszinkron kezeléséhez.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory,
)

# Globális változók a session factory-nek
_engine: Any | None = None  # type: ignore
_async_session_maker: Any | None = None  # type: ignore


def get_database_url(config_manager: ConfigManagerInterface | None = None) -> str:
    """Adatbázis URL lekérdezése a konfigurációból.

    Args:
        config_manager: Opcionális konfiguráció kezelő. Ha nincs megadva,
            létrehoz egy újat a ConfigManagerFactory segítségével.

    Returns:
        Az adatbázis URL string formátumban.

    Raises:
        ValueError: Ha az adatbázis URL nincs konfigurálva.
    """
    if config_manager is None:
        config_manager = ConfigManagerFactory.get_manager()

    db_url = config_manager.get("db_url")
    if not db_url:
        raise ValueError(
            "Adatbázis URL nincs konfigurálva. Kérlek állítsd be a DB_URL környezeti változót."
        )

    return db_url


def create_engine(db_url: str, echo: bool = False) -> Any:  # type: ignore
    """Aszinkron adatbázis engine létrehozása.

    Args:
        db_url: Az adatbázis URL (pl. sqlite+aiosqlite:///neural_ai.db).
        echo: SQL lekérdezések naplózásának engedélyezése.

    Returns:
        Az létrehozott SQLAlchemy async engine.
    """
    # SQLite esetén pool tiltása a jobb aszinkron működés érdekében
    if "sqlite" in db_url:
        engine = create_async_engine(
            db_url,
            echo=echo,
            poolclass=NullPool,
            connect_args={"check_same_thread": False},
        )
    else:
        # PostgreSQL és más adatbázisok esetén connection pool használata
        engine = create_async_engine(
            db_url,
            echo=echo,
            pool_size=20,
            max_overflow=0,
        )

    return engine


def get_engine(config_manager: ConfigManagerInterface | None = None) -> Any:  # type: ignore
    """Globális adatbázis engine lekérdezése.

    Ha az engine még nincs létrehozva, létrehozza azt a konfiguráció alapján.

    Args:
        config_manager: Opcionális konfiguráció kezelő.

    Returns:
        A globális SQLAlchemy async engine.
    """
    global _engine

    if _engine is None:
        db_url = get_database_url(config_manager)
        echo = ConfigManagerFactory.get_manager().get("log_level", "INFO") == "DEBUG"
        _engine = create_engine(db_url, echo=echo)

    return _engine


def get_async_session_maker(config_manager: ConfigManagerInterface | None = None) -> Any:  # type: ignore
    """AsyncSession factory lekérdezése.

    Ha a session maker még nincs létrehozva, létrehozza azt.

    Args:
        config_manager: Opcionális konfiguráció kezelő.

    Returns:
        Az async_sessionmaker objektum.
    """
    global _async_session_maker

    if _async_session_maker is None:
        engine = get_engine(config_manager)
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _async_session_maker


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection függvény a FastAPI számára.

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
    """
    session_maker = get_async_session_maker()

    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session_direct() -> AsyncSession:
    """Közvetlen adatbázis session lekérdezése.

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
    """
    session_maker = get_async_session_maker()
    return session_maker()


async def init_db() -> None:
    """Adatbázis inicializálása.

    Létrehozza az összes táblát az adatbázisban a modellek alapján.
    Ez a függvény az alkalmazás indításakor hívandó.
    """
    from .models import Base  # Körkörös import elkerülése

    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Adatbázis inicializálva és táblák létrehozva.")


async def close_db() -> None:
    """Adatbázis kapcsolat lezárása.

    Ez a függvény az alkalmazás leállításakor hívandó.
    """
    global _engine, _async_session_maker

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None

    print("✅ Adatbázis kapcsolat lezárva.")


class DatabaseManager:
    """Adatbázis kezelő osztály a Neural AI Next rendszerhez.

    Ez az osztály magas szintű interfészt biztosít az adatbázis műveletekhez,
    beleértve a session kezelést, inicializálást és lezárást.

    Attributes:
        config_manager: A konfiguráció kezelő példány.
    """

    def __init__(self, config_manager: ConfigManagerInterface | None = None):
        """Inicializálja az adatbázis kezelőt.

        Args:
            config_manager: Opcionális konfiguráció kezelő.
        """
        self.config_manager = config_manager or ConfigManagerFactory.get_manager()
        self._engine: Any | None = None
        self._session_maker: Any | None = None

    async def initialize(self) -> None:
        """Adatbázis inicializálása a kezelővel.

        Létrehozza az engine-t és a session maker-t, majd létrehozza a táblákat.
        """
        db_url = get_database_url(self.config_manager)
        echo = self.config_manager.get("log_level", "INFO") == "DEBUG"

        self._engine = create_engine(db_url, echo=echo)
        self._session_maker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        # Táblák létrehozása
        from .models import Base

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Session lekérdezése a kezelőből.

        Yields:
            AsyncSession: Az adatbázis session.

        Raises:
            RuntimeError: Ha a kezelő nincs inicializálva.
        """
        if self._session_maker is None:
            raise RuntimeError(
                "Adatbázis kezelő nincs inicializálva. Hívd meg először az initialize() metódust."
            )

        async with self._session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """Adatbázis kapcsolat lezárása.

        Felszabadítja az engine erőforrásait.
        """
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None
