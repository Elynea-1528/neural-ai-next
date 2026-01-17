"""Adatbázis factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kezelő komponensek létrehozását a factory
minta segítségével, beleértve a session maker-t és a DatabaseManager-t.
"""

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import (
    DatabaseManager,
    create_engine,
    get_async_session_maker,
    get_engine,
)

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface


# TypedDict a database konfigurációhoz
from typing import TypedDict


class DatabaseConfig(TypedDict):
    """Adatbázis konfigurációs struktúra."""

    url: str


class DatabaseFactory:
    """Factory osztály adatbázis komponensek létrehozásához.

    Ez az osztály felelős az adatbázis kezelő komponensek példányosításáért,
    beleértve a session factory-ket és a DatabaseManager-t.
    """

    def __init__(
        self,
        logger: "LoggerInterface",
        config_manager: ConfigManagerInterface,
    ) -> None:
        """Inicializálja az adatbázis factory-t.

        Args:
            logger: Logger interfész a naplózáshoz.
            config_manager: Konfiguráció kezelő interfész.
        """
        from neural_ai.core.logger.factory import LoggerFactory

        self.logger = LoggerFactory.get_logger("neural_ai.core.db")
        self.config_manager = config_manager

    def get_session_maker(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        """Session maker létrehozása vagy visszaadása.

        Returns:
            Az async_sessionmaker objektum.
        """
        return get_async_session_maker(self.config_manager)

    def get_engine(
        self,
    ) -> AsyncEngine:
        """Adatbázis engine létrehozása vagy visszaadása.

        Returns:
            Az SQLAlchemy async engine.
        """
        return get_engine(self.config_manager)

    def create_engine(self, db_url: str, echo: bool = False) -> AsyncEngine:
        """Egyéni adatbázis engine létrehozása.

        Args:
            db_url: Az adatbázis URL.
            echo: SQL lekérdezések naplózásának engedélyezése.

        Returns:
            Az létrehozott SQLAlchemy async engine.
        """
        return create_engine(db_url, echo=echo)

    def create_manager(
        self,
    ) -> DatabaseManager:
        """DatabaseManager példány létrehozása.

        Returns:
            Az inicializált DatabaseManager példány.
        """
        return DatabaseManager(self.config_manager, self.logger)
