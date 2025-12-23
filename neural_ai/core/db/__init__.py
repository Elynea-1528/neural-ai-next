"""Adatbázis modul a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kapcsolat kezelést, modelleket és session
factory-t az aszinkron adatbázis műveletekhez.
"""

from .base import Base
from .models import DynamicConfig, LogEntry
from .session import (
    DatabaseManager,
    close_db,
    create_engine,
    get_async_session_maker,
    get_database_url,
    get_db_session,
    get_db_session_direct,
    get_engine,
    init_db,
)

__all__ = [
    # Modellek
    "Base",
    "DynamicConfig",
    "LogEntry",
    # Session függvények
    "get_db_session",
    "get_db_session_direct",
    "get_engine",
    "get_async_session_maker",
    "init_db",
    "close_db",
    # Osztályok
    "DatabaseManager",
    # Segédfüggvények
    "get_database_url",
    "create_engine",
]
