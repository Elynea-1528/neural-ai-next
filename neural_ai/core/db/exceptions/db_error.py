"""Adatbázis-specifikus kivételek.

Ez a modul tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.
"""

from neural_ai.core.base.exceptions import NeuralAIException


class DatabaseError(NeuralAIException):
    """Általános adatbázis hiba."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Inicializálja a DatabaseError kivételt.

        Args:
            message: A hibaüzenet.
            details: Opcionális részletes leírás a hibáról.
        """
        super().__init__(message)
        self.details = details


class DBConnectionError(DatabaseError):
    """Adatbázis kapcsolat hiba."""

    def __init__(self, message: str, connection_string: str | None = None) -> None:
        """Inicializálja a DBConnectionError kivételt.

        Args:
            message: A hibaüzenet.
            connection_string: Az adatbázis kapcsolati sztringje.
        """
        super().__init__(message)
        self.connection_string = connection_string


class TransactionError(DatabaseError):
    """Tranzakció hiba."""

    def __init__(self, message: str, transaction_id: str | None = None) -> None:
        """Inicializálja a TransactionError kivételt.

        Args:
            message: A hibaüzenet.
            transaction_id: A tranzakció azonosítója.
        """
        super().__init__(message)
        self.transaction_id = transaction_id
