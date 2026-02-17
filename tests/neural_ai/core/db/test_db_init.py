"""Tesztek a neural_ai.core.db.__init__ modulhoz.

Ez a modul teszteli, hogy a __init__.py fájlban exportált osztályok és függvények
helyesen importálhatók-e.
"""

from neural_ai.core.db import (
    Base,
    DatabaseFactory,
    DatabaseManager,
    DynamicConfig,
    LogEntry,
    close_db,
    create_engine,
    get_async_session_maker,
    get_database_url,
    get_db_session,
    get_db_session_direct,
    get_engine,
    init_db,
)


class TestDbInit:
    """Teszt osztály a neural_ai.core.db.__init__ modulhoz."""

    def test_base_import(self) -> None:
        """Teszteli, hogy a Base osztály importálható-e."""
        assert Base is not None
        assert hasattr(Base, "__tablename__")

    def test_models_import(self) -> None:
        """Teszteli, hogy a model osztályok importálhatók-e."""
        assert DynamicConfig is not None
        assert LogEntry is not None
        assert hasattr(DynamicConfig, "__tablename__")
        assert hasattr(LogEntry, "__tablename__")

    def test_session_functions_import(self) -> None:
        """Teszteli, hogy a session függvények importálhatók-e."""
        assert get_db_session is not None
        assert get_db_session_direct is not None
        assert get_engine is not None
        assert get_async_session_maker is not None
        assert init_db is not None
        assert close_db is not None

    def test_classes_import(self) -> None:
        """Teszteli, hogy az osztályok importálhatók-e."""
        assert DatabaseManager is not None
        assert DatabaseFactory is not None

    def test_helper_functions_import(self) -> None:
        """Teszteli, hogy a segédfüggvények importálhatók-e."""
        assert get_database_url is not None
        assert create_engine is not None

    def test_all_imports_are_callable(self) -> None:
        """Teszteli, hogy az importált függvények hívhatók-e."""
        # Osztályok, amelyeknek hívhatónak kell lenniük
        assert callable(DatabaseManager)
        assert callable(DatabaseFactory)
        assert callable(create_engine)

    def test_all_imports_are_not_none(self) -> None:
        """Teszteli, hogy az összes importált objektum nem None."""
        imports = [
            Base,
            DynamicConfig,
            LogEntry,
            get_db_session,
            get_db_session_direct,
            get_engine,
            get_async_session_maker,
            init_db,
            close_db,
            DatabaseManager,
            DatabaseFactory,
            get_database_url,
            create_engine,
        ]
        for imported in imports:
            assert imported is not None, f"Import failed for {imported}"

    def test_model_base_relationship(self) -> None:
        """Teszteli, hogy a modellek a Base osztályból származnak-e."""
        assert issubclass(DynamicConfig, Base)
        assert issubclass(LogEntry, Base)
