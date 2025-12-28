"""Adatbázis kivételek tesztek."""
import pytest

from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.db.exceptions.db_error import (
    DBConnectionError,
    DatabaseError,
    TransactionError,
)


class TestDatabaseError:
    """DatabaseError osztály tesztei."""

    def test_database_error_creation(self) -> None:
        """DatabaseError létrehozásának tesztelése."""
        error = DatabaseError("Hibaüzenet")
        assert str(error) == "Hibaüzenet"
        assert error.details is None

    def test_database_error_with_details(self) -> None:
        """DatabaseError létrehozása részletekkel."""
        error = DatabaseError("Hibaüzenet", details="Részletes leírás")
        assert str(error) == "Hibaüzenet"
        assert error.details == "Részletes leírás"

    def test_database_error_is_neural_ai_exception(self) -> None:
        """DatabaseError NeuralAIException-ből származik."""
        error = DatabaseError("Hibaüzenet")
        assert isinstance(error, NeuralAIException)


class TestDBConnectionError:
    """DBConnectionError osztály tesztei."""

    def test_db_connection_error_creation(self) -> None:
        """DBConnectionError létrehozásának tesztelése."""
        error = DBConnectionError("Kapcsolat hiba")
        assert str(error) == "Kapcsolat hiba"
        assert error.connection_string is None

    def test_db_connection_error_with_connection_string(self) -> None:
        """DBConnectionError létrehozása connection stringgel."""
        error = DBConnectionError("Kapcsolat hiba", connection_string="sqlite:///test.db")
        assert str(error) == "Kapcsolat hiba"
        assert error.connection_string == "sqlite:///test.db"

    def test_db_connection_error_inheritance(self) -> None:
        """DBConnectionError DatabaseError-ből származik."""
        error = DBConnectionError("Kapcsolat hiba")
        assert isinstance(error, DatabaseError)


class TestTransactionError:
    """TransactionError osztály tesztei."""

    def test_transaction_error_creation(self) -> None:
        """TransactionError létrehozásának tesztelése (47-48. sorok)."""
        error = TransactionError("Tranzakció hiba")
        assert str(error) == "Tranzakció hiba"
        assert error.transaction_id is None

    def test_transaction_error_with_transaction_id(self) -> None:
        """TransactionError létrehozása transaction ID-vel (47-48. sorok)."""
        error = TransactionError("Tranzakció hiba", transaction_id="txn_12345")
        assert str(error) == "Tranzakció hiba"
        assert error.transaction_id == "txn_12345"

    def test_transaction_error_inheritance(self) -> None:
        """TransactionError DatabaseError-ből származik."""
        error = TransactionError("Tranzakció hiba")
        assert isinstance(error, DatabaseError)