"""Tesztek a neural_ai.core.db.__init__.py modulhoz.

Ez a tesztmodul ellenőrzi a db modul inicializálását és exportált elemeit.
"""

import pytest


class TestDbInit:
    """Tesztek a db __init__ modulhoz."""

    def test_module_import(self) -> None:
        """Teszteli, hogy a modul importálható."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert neural_ai.core.db is not None

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul docstring létezik."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert neural_ai.core.db.__doc__ is not None
        assert "adatbázis" in neural_ai.core.db.__doc__.lower()

    def test_database_factory_exported(self) -> None:
        """Teszteli, hogy a DatabaseFactory exportálva van."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseFactory

        # Assert
        assert DatabaseFactory is not None
        assert hasattr(DatabaseFactory, "create_manager")

    def test_database_error_exported(self) -> None:
        """Teszteli, hogy a DatabaseError exportálva van."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseError

        # Assert
        assert DatabaseError is not None
        assert issubclass(DatabaseError, Exception)

    def test_db_connection_error_exported(self) -> None:
        """Teszteli, hogy a DBConnectionError exportálva van."""
        # Arrange & Act
        from neural_ai.core.db import DBConnectionError

        # Assert
        assert DBConnectionError is not None
        assert issubclass(DBConnectionError, Exception)

    def test_transaction_error_exported(self) -> None:
        """Teszteli, hogy a TransactionError exportálva van."""
        # Arrange & Act
        from neural_ai.core.db import TransactionError

        # Assert
        assert TransactionError is not None
        assert issubclass(TransactionError, Exception)

    def test_all_exports(self) -> None:
        """Teszteli, hogy az __all__ lista tartalmazza az összes exportált elemet."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert hasattr(neural_ai.core.db, "__all__")
        expected_exports = {
            "DatabaseFactory",
            "DatabaseError",
            "DBConnectionError",
            "TransactionError",
        }
        assert set(neural_ai.core.db.__all__) == expected_exports

    def test_factory_in_all(self) -> None:
        """Teszteli, hogy a DatabaseFactory az __all__ listában van."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert "DatabaseFactory" in neural_ai.core.db.__all__

    def test_exceptions_in_all(self) -> None:
        """Teszteli, hogy az összes exception az __all__ listában van."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert "DatabaseError" in neural_ai.core.db.__all__
        assert "DBConnectionError" in neural_ai.core.db.__all__
        assert "TransactionError" in neural_ai.core.db.__all__

    def test_no_implementation_exports(self) -> None:
        """Teszteli, hogy az implementációk NEM exportáltak (DDD szabály)."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert - Implementációk NEM lehetnek az __all__-ban
        forbidden_exports = [
            "DatabaseManager",
            "Base",
            "ModelBase",
            "get_session",
            "async_session_scope",
        ]
        for forbidden in forbidden_exports:
            assert forbidden not in neural_ai.core.db.__all__, (
                f"{forbidden} NEM lehet exportálva (DDD szabály)"
            )

    def test_module_file_attribute(self) -> None:
        """Teszteli, hogy a modul __file__ attribútuma helyes."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert neural_ai.core.db.__file__ is not None
        assert "__init__.py" in neural_ai.core.db.__file__
        assert "neural_ai/core/db" in neural_ai.core.db.__file__

    def test_module_name_attribute(self) -> None:
        """Teszteli, hogy a modul __name__ attribútuma helyes."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert neural_ai.core.db.__name__ == "neural_ai.core.db"

    def test_module_package_attribute(self) -> None:
        """Teszteli, hogy a modul __package__ attribútuma helyes."""
        # Arrange & Act
        import neural_ai.core.db

        # Assert
        assert neural_ai.core.db.__package__ == "neural_ai.core.db"


class TestDbFactoryImport:
    """Tesztek a DatabaseFactory importálására."""

    def test_factory_has_create_manager(self) -> None:
        """Teszteli, hogy a DatabaseFactory rendelkezik create_manager metódussal."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseFactory

        # Assert
        assert hasattr(DatabaseFactory, "create_manager")
        assert callable(DatabaseFactory.create_manager)

    def test_factory_is_class(self) -> None:
        """Teszteli, hogy a DatabaseFactory osztály."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseFactory

        # Assert
        assert isinstance(DatabaseFactory, type)


class TestDbExceptionsImport:
    """Tesztek az exception osztályok importálására."""

    def test_database_error_inheritance(self) -> None:
        """Teszteli, hogy a DatabaseError Exception leszármazott."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseError

        # Assert
        assert issubclass(DatabaseError, Exception)

    def test_db_connection_error_inheritance(self) -> None:
        """Teszteli, hogy a DBConnectionError DatabaseError leszármazott."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseError, DBConnectionError

        # Assert
        assert issubclass(DBConnectionError, DatabaseError)

    def test_transaction_error_inheritance(self) -> None:
        """Teszteli, hogy a TransactionError DatabaseError leszármazott."""
        # Arrange & Act
        from neural_ai.core.db import DatabaseError, TransactionError

        # Assert
        assert issubclass(TransactionError, DatabaseError)

    def test_exceptions_can_be_raised(self) -> None:
        """Teszteli, hogy az exception osztályok dobhatók."""
        # Arrange
        from neural_ai.core.db import DatabaseError, DBConnectionError, TransactionError

        # Act & Assert
        with pytest.raises(DatabaseError):
            raise DatabaseError("Test error")

        with pytest.raises(DBConnectionError):
            raise DBConnectionError("Test connection error")

        with pytest.raises(TransactionError):
            raise TransactionError("Test transaction error")

    def test_exceptions_have_message(self) -> None:
        """Teszteli, hogy az exception osztályok üzenettel rendelkeznek."""
        # Arrange
        from neural_ai.core.db import DatabaseError, DBConnectionError, TransactionError

        # Act
        db_error = DatabaseError("Database error message")
        conn_error = DBConnectionError("Connection error message")
        trans_error = TransactionError("Transaction error message")

        # Assert
        assert str(db_error) == "Database error message"
        assert str(conn_error) == "Connection error message"
        assert str(trans_error) == "Transaction error message"
