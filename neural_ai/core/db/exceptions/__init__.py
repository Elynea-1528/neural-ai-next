"""Adatbázis kivételek modulja.

Ez a csomag tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.
"""

from neural_ai.core.db.exceptions.db_error import (
    DatabaseError,
    DBConnectionError,
    TransactionError,
)

__all__ = [
    "DatabaseError",
    "DBConnectionError",
    "TransactionError",
]
