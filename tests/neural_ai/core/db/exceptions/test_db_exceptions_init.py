"""Tesztelő modul a neural_ai.core.db.exceptions.__init__.py fájlnak.

Ez a modul tartalmazza azokat a teszteket, amelyek ellenőrzik az exceptions csomag
__init__.py fájljának helyes működését, különös tekintettel az exportált osztályokra.
"""

from neural_ai.core.db.exceptions import (
    DatabaseError,
    DBConnectionError,
    TransactionError,
)


class TestExceptionsInit:
    """Tesztosztály az exceptions csomag __init__.py exportjainak ellenőrzésére."""

    def test_database_error_import(self) -> None:
        """Teszteli, hogy a DatabaseError osztály importálható-e."""
        assert DatabaseError is not None
        assert issubclass(DatabaseError, Exception)

    def test_db_connection_error_import(self) -> None:
        """Teszteli, hogy a DBConnectionError osztály importálható-e."""
        assert DBConnectionError is not None
        assert issubclass(DBConnectionError, DatabaseError)

    def test_transaction_error_import(self) -> None:
        """Teszteli, hogy a TransactionError osztály importálható-e."""
        assert TransactionError is not None
        assert issubclass(TransactionError, DatabaseError)

    def test_all_list_content(self) -> None:
        """Teszteli, hogy a __all__ lista csak a várt osztályokat tartalmazza."""
        from neural_ai.core.db.exceptions import __all__

        expected_exports = ["DatabaseError", "DBConnectionError", "TransactionError"]
        assert __all__ == expected_exports

    def test_exception_instantiation(self) -> None:
        """Teszteli, hogy az exportált kivétel osztályok példányosíthatók-e."""
        test_message = "Teszt hibaüzenet"

        db_error = DatabaseError(test_message)
        assert str(db_error) == test_message

        conn_error = DBConnectionError(test_message)
        assert str(conn_error) == test_message

        trans_error = TransactionError(test_message)
        assert str(trans_error) == test_message
