"""Adatbázis factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kezelő komponensek létrehozását a factory
minta segítségével, beleértve a session maker-t és a DatabaseManager-t.
"""

from typing import Any

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.implementations.sqlalchemy_session import (
    DatabaseManager,
    create_engine,
    get_async_session_maker,
    get_engine,
)


class DatabaseFactory:
    """Factory osztály adatbázis komponensek létrehozásához.

    Ez az osztály felelős az adatbázis kezelő komponensek példányosításáért,
    beleértve a session factory-ket és a DatabaseManager-t.
    """

    @staticmethod
    def get_session_maker(
        config_manager: ConfigManagerInterface | None = None,
    ) -> Any:  # type: ignore
        """Session maker létrehozása vagy visszaadása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az async_sessionmaker objektum.
        """
        return get_async_session_maker(config_manager)

    @staticmethod
    def get_engine(
        config_manager: ConfigManagerInterface | None = None,
    ) -> Any:  # type: ignore
        """Adatbázis engine létrehozása vagy visszaadása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az SQLAlchemy async engine.
        """
        return get_engine(config_manager)

    @staticmethod
    def create_engine(db_url: str, echo: bool = False) -> Any:  # type: ignore
        """Egyéni adatbázis engine létrehozása.

        Args:
            db_url: Az adatbázis URL.
            echo: SQL lekérdezések naplózásának engedélyezése.

        Returns:
            Az létrehozott SQLAlchemy async engine.
        """
        return create_engine(db_url, echo=echo)

    @staticmethod
    def create_manager(
        config_manager: ConfigManagerInterface | None = None,
    ) -> DatabaseManager:
        """DatabaseManager példány létrehozása.

        Args:
            config_manager: Opcionális konfiguráció kezelő.

        Returns:
            Az inicializált DatabaseManager példány.
        """
        return DatabaseManager(config_manager)