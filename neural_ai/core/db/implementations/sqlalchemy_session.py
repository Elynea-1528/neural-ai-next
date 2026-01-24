"""Adatbázis session kezelő a Neural AI Next rendszerhez.

Ez a modul biztosítja az AsyncSession factory-t és a kapcsolódó segédfunkciókat
az adatbázis műveletek aszinkron kezeléséhez.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.exceptions import DBConnectionError

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface

# TypedDict a database konfigurációhoz
from typing import TypedDict


class DatabaseConfig(TypedDict):
    """Adatbázis konfigurációs struktúra."""

    url: str


if TYPE_CHECKING:
    pass

# Globális változók a session factory-nek
_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


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
        config_manager = ConfigManagerFactory.get_manager("config.yaml")

    # Elsődlegesen a namespaced konfigban keressük
    db_config_raw = config_manager.get("database", "connection")
    if db_config_raw and isinstance(db_config_raw, dict):
        db_config = cast(DatabaseConfig, db_config_raw)
        db_url = db_config["url"]
    else:
        db_url = None

    # Ha nincs, akkor a régi env fallback
    if not db_url:
        db_url = cast(str | None, config_manager.get("db_url"))

    if not db_url:
        raise DBConnectionError(
            message=(
                "Adatbázis URL nincs konfigurálva. "
                "Kérlek állítsd be a database.connection.url-t a configs/database.yaml-ben "
                "vagy a DB_URL környezeti változót."
            )
        )

    return db_url


def create_engine(db_url: str, echo: bool = False) -> AsyncEngine:
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


def get_engine(config_manager: ConfigManagerInterface | None = None) -> AsyncEngine:
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
        echo = ConfigManagerFactory.get_manager("config.yaml").get("log_level", "INFO") == "DEBUG"
        _engine = create_engine(db_url, echo=echo)

    return _engine


def get_async_session_maker(
    config_manager: ConfigManagerInterface | None = None,
) -> async_sessionmaker[AsyncSession]:
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


async def init_db(logger: "LoggerInterface") -> None:
    """Adatbázis inicializálása.

    Létrehozza az összes táblát az adatbázisban a modellek alapján.
    Ez a függvény az alkalmazás indításakor hívandó.

    Args:
        logger: Logger interfész a naplózáshoz.
    """
    from .models import Base  # Körkörös import elkerülése

    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(
        "Adatbázis inicializálva és táblák létrehozva",
        extra={"module": "sqlalchemy_session", "function": "init_db"},
    )


async def close_db(logger: "LoggerInterface") -> None:
    """Adatbázis kapcsolat lezárása.

    Ez a függvény az alkalmazás leállításakor hívandó.

    Args:
        logger: Logger interfész a naplózáshoz.
    """
    global _engine, _async_session_maker

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None

    logger.info(
        "Adatbázis kapcsolat lezárva",
        extra={"module": "sqlalchemy_session", "function": "close_db"},
    )


class DatabaseManager(metaclass=SingletonMeta):
    """Adatbázis kezelő osztály a Neural AI Next rendszerhez.

    Ez az osztály magas szintű interfészt biztosít az adatbázis műveletekhez,
    beleértve a session kezelést, inicializálást és lezárást.

    Attributes:
        config_manager: A konfiguráció kezelő példány.
        logger: A logger interfész.
    """

    def __init__(
        self,
        config_manager: ConfigManagerInterface | None = None,
        logger: "LoggerInterface | None" = None,
    ):
        """Inicializálja az adatbázis kezelőt.

        Args:
            config_manager: Opcionális konfiguráció kezelő.
            logger: Opcionális logger interfész.
        """
        self.config_manager = config_manager or ConfigManagerFactory.get_manager("config.yaml")
        self.logger = logger  # Logger DI
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

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

        if self.logger:
            self.logger.info(
                "DatabaseManager inicializálva",
                extra={"module": "DatabaseManager", "function": "initialize"},
            )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Session lekérdezése a kezelőből.

        Yields:
            AsyncSession: Az adatbázis session.

        Raises:
            RuntimeError: Ha a kezelő nincs inicializálva.
        """
        if self._session_maker is None:
            raise DBConnectionError(
                message=(
                    "Adatbázis kezelő nincs inicializálva. "
                    "Hívd meg először az initialize() metódust."
                )
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

    async def get_active_configs(self) -> dict[str, object]:
        """Aktív dinamikus konfigurációk lekérdezése.

        Visszaadja az összes aktív dinamikus konfigurációt kulcs-érték párokként.

        Returns:
            Szótár az aktív konfigurációkulcsokkal és értékeikkel.

        Raises:
            RuntimeError: Ha a kezelő nincs inicializálva.
        """
        from .models import DynamicConfig  # Körkörös import elkerülése

        if self._session_maker is None:
            raise RuntimeError(
                "Adatbázis kezelő nincs inicializálva. Hívd meg először az initialize() metódust."
            )

        async with self._session_maker() as session:
            stmt = select(DynamicConfig).where(DynamicConfig.is_active)
            result = await session.execute(stmt)
            configs = result.scalars().all()

            return {config.key: config.value for config in configs}

    async def close(self) -> None:
        """Adatbázis kapcsolat lezárása.

        Felszabadítja az engine erőforrásait.
        """
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None

        if self.logger:
            self.logger.info(
                "DatabaseManager lezárva", extra={"module": "DatabaseManager", "function": "close"}
            )
