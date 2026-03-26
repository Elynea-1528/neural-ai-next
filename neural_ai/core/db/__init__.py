"""Adatbázis modul a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kapcsolat kezelést, modelleket és session
factory-t az aszinkron adatbázis műveletekhez.

DDD Szabály:
    Csak Factory + Exceptions exportáltak.
    Az implementációk (Base, models, DatabaseManager, session függvények) NEM exportáltak.
    Ezeket közvetlenül a DatabaseFactory vagy az implementations modulból kell importálni.

Megjegyzés:
    A modul jelenleg nem rendelkezik interfészekkel (interfaces/ üres).
    Ez egy későbbi fázisban kerül kialakításra (DatabaseInterface, SessionInterface).
"""

from neural_ai.core.db.exceptions import (
    DatabaseError,
    DBConnectionError,
    TransactionError,
)
from neural_ai.core.db.factory import DatabaseFactory

__all__ = [
    # Factory
    "DatabaseFactory",
    # Exceptions
    "DatabaseError",
    "DBConnectionError",
    "TransactionError",
]
