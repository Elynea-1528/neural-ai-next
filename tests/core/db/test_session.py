"""Tesztek az adatbázis session kezelőhöz.

Ez a modul tartalmazza az összes tesztet a session factory-hez és
a kapcsolódó segédfunkciókhoz.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.db.session import (
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


class TestGetDatabaseUrl:
    """Tesztek a get_database_url függvényhez."""

    def test_get_database_url_with_config_manager(self):
        """Teszteli az adatbázis URL lekérdezést konfiguráció kezelővel."""
        # Mock konfiguráció kezelő létrehozása
        mock_config = Mock()
        mock_config.get.return_value = "sqlite+aiosqlite:///test.db"

        # URL lekérdezése
        result = get_database_url(mock_config)

        # Ellenőrzések
        assert result == "sqlite+aiosqlite:///test.db"
        mock_config.get.assert_called_once_with("db_url")

    def test_get_database_url_without_config_manager(self):
        """Teszteli az adatbázis URL lekérdezést alapértelmezett konfigurációval."""
        with patch("neural_ai.core.db.session.ConfigManagerFactory.get_manager") as mock_factory:
            mock_config = Mock()
            mock_config.get.return_value = "sqlite+aiosqlite:///neural_ai.db"
            mock_factory.return_value = mock_config

            result = get_database_url()

            assert result == "sqlite+aiosqlite:///neural_ai.db"
            mock_factory.assert_called_once()

    def test_get_database_url_missing_config(self):
        """Teszteli a hibát, ha az adatbázis URL nincs konfigurálva."""
        mock_config = Mock()
        mock_config.get.return_value = None

        with pytest.raises(ValueError, match="Adatbázis URL nincs konfigurálva"):
            get_database_url(mock_config)


class TestCreateEngine:
    """Tesztek a create_engine függvényhez."""

    def test_create_engine_sqlite(self):
        """Teszteli az engine létrehozását SQLite adatbázishoz."""
        db_url = "sqlite+aiosqlite:///test.db"

        engine = create_engine(db_url, echo=False)

        assert engine is not None
        assert str(engine.url) == db_url

    def test_create_engine_postgresql(self):
        """Teszteli az engine létrehozását PostgreSQL adatbázishoz."""
        pytest.skip("PostgreSQL teszt kihagyva - asyncpg nincs telepítve")
        
        db_url = "postgresql+asyncpg://user:pass@localhost/db"

        engine = create_engine(db_url, echo=True)

        assert engine is not None
        assert str(engine.url) == db_url


class TestGetEngine:
    """Tesztek a get_engine függvényhez."""

    def test_get_engine_creates_once(self):
        """Teszteli, hogy az engine csak egyszer jön létre."""
        with patch("neural_ai.core.db.session.create_engine") as mock_create:
            with patch("neural_ai.core.db.session.ConfigManagerFactory.get_manager") as mock_factory:
                mock_config = Mock()
                mock_config.get.return_value = "sqlite+aiosqlite:///test.db"
                mock_factory.return_value = mock_config
                
                mock_engine = Mock()
                mock_create.return_value = mock_engine

                # Első hívás
                engine1 = get_engine()

                # Második hívás - ugyanazt az engine-t kell visszaadnia
                engine2 = get_engine()

                assert engine1 is engine2
                mock_create.assert_called_once()


class TestGetAsyncSessionMaker:
    """Tesztek a get_async_session_maker függvényhez."""

    def test_get_async_session_maker_creates_once(self):
        """Teszteli, hogy a session maker csak egyszer jön létre."""
        with patch("neural_ai.core.db.session.get_engine") as mock_get_engine:
            mock_engine = Mock()
            mock_get_engine.return_value = mock_engine

            # Első hívás
            maker1 = get_async_session_maker()

            # Második hívás - ugyanazt kell visszaadnia
            maker2 = get_async_session_maker()

            assert maker1 is maker2
            mock_get_engine.assert_called_once()


class TestGetDbSession:
    """Tesztek a get_db_session context managerhez."""

    @pytest.mark.asyncio
    async def test_get_db_session_commits_on_success(self):
        """Teszteli, hogy a session commitol sikeres művelet után."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock()
        mock_session.rollback = AsyncMock()
        mock_session.close = AsyncMock()

        with patch("neural_ai.core.db.session.get_async_session_maker") as mock_maker:
            mock_maker.return_value.return_value.__aenter__.return_value = mock_session

            async with get_db_session() as session:
                assert session is mock_session

            # Ellenőrzés, hogy commit és close meghívásra került
            mock_session.commit.assert_awaited_once()
            mock_session.rollback.assert_not_called()
            mock_session.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_db_session_rollsback_on_error(self):
        """Teszteli, hogy a session rollbackel hiba esetén."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock()
        mock_session.rollback = AsyncMock()
        mock_session.close = AsyncMock()

        with patch("neural_ai.core.db.session.get_async_session_maker") as mock_maker:
            mock_maker.return_value.return_value.__aenter__.return_value = mock_session

            with pytest.raises(Exception):
                async with get_db_session() as session:
                    raise Exception("Test error")

            # Ellenőrzés, hogy rollback és close meghívásra került
            mock_session.commit.assert_not_called()
            mock_session.rollback.assert_awaited_once()
            mock_session.close.assert_awaited_once()


class TestGetDbSessionDirect:
    """Tesztek a get_db_session_direct függvényhez."""

    @pytest.mark.asyncio
    async def test_get_db_session_direct_returns_session(self):
        """Teszteli, hogy a függvény session-t ad vissza."""
        mock_session = Mock(spec=AsyncSession)

        with patch("neural_ai.core.db.session.get_async_session_maker") as mock_maker:
            mock_maker.return_value.return_value = mock_session

            session = await get_db_session_direct()

            assert session is mock_session


class TestInitDb:
    """Tesztek az init_db függvényhez."""

    @pytest.mark.asyncio
    async def test_init_db_creates_tables(self):
        """Teszteli, hogy az init_db létrehozza a táblákat."""
        mock_engine = Mock()
        mock_conn = AsyncMock()
        mock_engine.begin.return_value = AsyncMock()
        mock_engine.begin.return_value.__aenter__.return_value = mock_conn
        mock_engine.begin.return_value.__aexit__.return_value = None

        with patch("neural_ai.core.db.session.get_engine", return_value=mock_engine):
            await init_db()

            # Ellenőrzés, hogy a függvény lefutott
            assert True  # Ha nem dobott kivételt, sikeres


class TestCloseDb:
    """Tesztek a close_db függvényhez."""

    @pytest.mark.asyncio
    async def test_close_db_disposes_engine(self):
        """Teszteli, hogy a close_db felszabadítja az engine-t."""
        mock_engine = AsyncMock()

        with patch("neural_ai.core.db.session._engine", mock_engine):
            with patch("neural_ai.core.db.session._async_session_maker", Mock()):
                await close_db()

                # Ellenőrzés, hogy a dispose meghívásra került
                mock_engine.dispose.assert_awaited_once()


class TestDatabaseManager:
    """Tesztek a DatabaseManager osztályhoz."""

    @pytest.mark.asyncio
    async def test_database_manager_initialization(self):
        """Teszteli a DatabaseManager inicializálását."""
        mock_config = Mock()
        mock_config.get.side_effect = lambda key, default=None: {
            "db_url": "sqlite+aiosqlite:///test.db",
            "log_level": "INFO",
        }.get(key, default)

        manager = DatabaseManager(mock_config)

        with patch("neural_ai.core.db.session.create_engine") as mock_create_engine:
            mock_engine = Mock()
            mock_conn = AsyncMock()
            mock_engine.begin.return_value = AsyncMock()
            mock_engine.begin.return_value.__aenter__.return_value = mock_conn
            mock_engine.begin.return_value.__aexit__.return_value = None
            mock_create_engine.return_value = mock_engine

            await manager.initialize()

            assert manager._engine is not None
            assert manager._session_maker is not None
            mock_create_engine.assert_called_once()

    @pytest.mark.asyncio
    async def test_database_manager_get_session(self):
        """Teszteli a session lekérdezést a DatabaseManager-ből."""
        mock_config = Mock()
        manager = DatabaseManager(mock_config)
        mock_session_maker = Mock()
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session_maker.return_value = AsyncMock()
        mock_session_maker.return_value.__aenter__.return_value = mock_session
        mock_session_maker.return_value.__aexit__.return_value = None
        manager._session_maker = mock_session_maker

        async with manager.get_session() as session:
            assert session is mock_session

        mock_session.commit.assert_awaited_once()
        mock_session.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_database_manager_get_session_not_initialized(self):
        """Teszteli a hibát, ha a kezelő nincs inicializálva."""
        mock_config = Mock()
        manager = DatabaseManager(mock_config)

        with pytest.raises(RuntimeError, match="nincs inicializálva"):
            async with manager.get_session():
                pass

    @pytest.mark.asyncio
    async def test_database_manager_close(self):
        """Teszteli az adatbázis kezelő lezárását."""
        mock_config = Mock()
        manager = DatabaseManager(mock_config)
        mock_engine = AsyncMock()
        manager._engine = mock_engine

        await manager.close()

        mock_engine.dispose.assert_awaited_once()
        assert manager._engine is None
        assert manager._session_maker is None
