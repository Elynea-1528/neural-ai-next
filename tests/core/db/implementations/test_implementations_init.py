"""Tesztelő modul a neural_ai.core.db.implementations.__init__.py fájlnak.

Ez a modul tartalmazza azokat a teszteket, amelyek ellenőrzik az implementations csomag
__init__.py fájljának helyes működését, különös tekintettel az exportált osztályokra
és függvényekre.
"""

from neural_ai.core.db.implementations import (
    Base,
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


class TestImplementationsInit:
    """Tesztosztály az implementations csomag __init__.py exportjainak ellenőrzésére."""

    def test_base_model_import(self) -> None:
        """Teszteli, hogy a Base model osztály importálható-e."""
        assert Base is not None
        # A Base-nek deklaratív alapnak kell lennie
        assert hasattr(Base, "metadata")

    def test_models_import(self) -> None:
        """Teszteli, hogy a model osztályok importálhatók-e."""
        assert DynamicConfig is not None
        assert LogEntry is not None
        # Ellenőrizzük, hogy a modellek a Base-ből származnak-e
        assert issubclass(DynamicConfig, Base)
        assert issubclass(LogEntry, Base)

    def test_session_functions_import(self) -> None:
        """Teszteli, hogy a session függvények importálhatók-e és hívhatók-e."""
        assert get_db_session is not None
        assert callable(get_db_session)

        assert get_db_session_direct is not None
        assert callable(get_db_session_direct)

        assert get_engine is not None
        assert callable(get_engine)

        assert get_async_session_maker is not None
        assert callable(get_async_session_maker)

        assert init_db is not None
        assert callable(init_db)

        assert close_db is not None
        assert callable(close_db)

    def test_classes_import(self) -> None:
        """Teszteli, hogy az osztályok importálhatók-e."""
        assert DatabaseManager is not None
        # A DatabaseManager-nek rendelkeznie kell a szükséges metódusokkal
        assert hasattr(DatabaseManager, "get_session")
        assert hasattr(DatabaseManager, "close")

    def test_helper_functions_import(self) -> None:
        """Teszteli, hogy a segédfüggvények importálhatók-e és hívhatók-e."""
        assert get_database_url is not None
        assert callable(get_database_url)

        assert create_engine is not None
        assert callable(create_engine)

    def test_all_imports_are_not_none(self) -> None:
        """Teszteli, hogy egyetlen importált objektum sem None."""
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
            get_database_url,
            create_engine,
        ]
        for imported_obj in imports:
            assert imported_obj is not None, f"Az importált objektum None: {imported_obj}"

    def test_all_list_content(self) -> None:
        """Teszteli, hogy a __all__ lista csak a várt exportokat tartalmazza."""
        from neural_ai.core.db.implementations import __all__

        expected_exports = [
            "Base",
            "DynamicConfig",
            "LogEntry",
            "get_db_session",
            "get_db_session_direct",
            "get_engine",
            "get_async_session_maker",
            "init_db",
            "close_db",
            "DatabaseManager",
            "get_database_url",
            "create_engine",
        ]
        assert __all__ == expected_exports

    def test_model_base_relationship(self) -> None:
        """Teszteli, hogy a model osztályok valóban a Base-ből származnak."""
        # Hozzunk létre egy egyszerű táblát a Base-ből
        from sqlalchemy import Column, Integer

        class TestModel(Base):
            __tablename__ = "test_model"
            id = Column(Integer, primary_key=True)

        assert TestModel.__tablename__ == "test_model"
        assert hasattr(TestModel, "metadata")
        assert TestModel in Base.registry._class_registry.values()
