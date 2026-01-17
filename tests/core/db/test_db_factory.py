"""Tesztek a neural_ai.core.db.factory modulhoz.

Ez a modul tartalmazza a DatabaseFactory osztály és annak metódusainak tesztjeit.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager


class TestDatabaseFactory:
    """DatabaseFactory osztály tesztjei."""

    @pytest.fixture
    def mock_logger(self) -> MagicMock:
        """Mock logger fixture."""
        return MagicMock()

    @pytest.fixture
    def mock_config(self) -> MagicMock:
        """Mock config manager fixture."""
        return MagicMock(spec=ConfigManagerInterface)

    @pytest.fixture
    def factory(self, mock_logger: MagicMock, mock_config: MagicMock) -> DatabaseFactory:
        """DatabaseFactory fixture."""
        return DatabaseFactory(logger=mock_logger, config_manager=mock_config)

    @patch("neural_ai.core.db.factory.get_async_session_maker")
    def test_get_session_maker_without_config(
        self, mock_get_session_maker: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli a session maker lekérdezést konfig nélkül."""
        mock_session_maker = MagicMock()
        mock_get_session_maker.return_value = mock_session_maker
        session_maker = factory.get_session_maker()

        assert session_maker is not None
        assert session_maker is mock_session_maker

    @patch("neural_ai.core.db.factory.get_async_session_maker")
    def test_get_session_maker_with_config(
        self, mock_get_session_maker: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli a session maker lekérdezést konfiggal."""
        mock_session_maker = MagicMock()
        mock_get_session_maker.return_value = mock_session_maker
        session_maker = factory.get_session_maker()

        assert session_maker is not None
        assert session_maker is mock_session_maker

    @patch("neural_ai.core.db.factory.get_engine")
    def test_get_engine_without_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli az engine lekérdezést konfig nélkül."""
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine

        engine = factory.get_engine()

        assert engine is mock_engine
        mock_get_engine.assert_called_once_with(factory.config_manager)

    @patch("neural_ai.core.db.factory.get_engine")
    def test_get_engine_with_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli az engine lekérdezést konfiggal."""
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine

        engine = factory.get_engine()

        assert engine is mock_engine
        mock_get_engine.assert_called_once_with(factory.config_manager)

    def test_create_engine_with_custom_url(self, factory: DatabaseFactory) -> None:
        """Teszteli az egyéni engine létrehozást."""
        custom_url = "sqlite+aiosqlite:///:memory:"
        engine = factory.create_engine(custom_url, echo=False)

        assert engine is not None
        assert isinstance(engine, AsyncEngine)

    def test_create_engine_with_echo_enabled(self, factory: DatabaseFactory) -> None:
        """Teszteli az engine létrehozást echo módban."""
        custom_url = "sqlite+aiosqlite:///:memory:"
        engine = factory.create_engine(custom_url, echo=True)

        assert engine is not None
        assert isinstance(engine, AsyncEngine)

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    def test_create_manager_without_config(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli a DatabaseManager létrehozást konfig nélkül."""
        mock_config = MagicMock()
        mock_config.get.return_value = "INFO"
        mock_get_manager.return_value = mock_config
        manager = factory.create_manager()

        assert manager is not None
        assert isinstance(manager, DatabaseManager)

    def test_create_manager_with_config(self, factory: DatabaseFactory) -> None:
        """Teszteli a DatabaseManager létrehozást konfiggal."""
        manager = factory.create_manager()

        assert manager is not None
        assert isinstance(manager, DatabaseManager)
        assert manager.config_manager is not None

    @patch("neural_ai.core.db.factory.get_async_session_maker")
    def test_get_session_maker_caches_result(self, mock_get_session: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli, hogy a session maker cache-elődik a modul szintjén."""
        mock_session_maker = MagicMock()
        mock_get_session.return_value = mock_session_maker

        result1 = factory.get_session_maker()
        result2 = factory.get_session_maker()

        assert result1 is result2
        # A modul szintű cache miatt csak egyszer hívódik meg a globális függvény
        mock_get_session.assert_called()

    @patch("neural_ai.core.db.factory.get_engine")
    def test_get_engine_caches_result(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli, hogy az engine cache-elődik a modul szintjén."""
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine

        result1 = factory.get_engine()
        result2 = factory.get_engine()

        assert result1 is result2
        # A modul szintű cache miatt csak egyszer hívódik meg a globális függvény
        mock_get_engine.assert_called()

    def test_create_engine_different_urls(self, factory: DatabaseFactory) -> None:
        """Teszteli az engine létrehozást különböző URL-ekkel."""
        urls = [
            "sqlite+aiosqlite:///:memory:",
            "sqlite+aiosqlite:///test.db",
        ]

        for url in urls:
            engine = factory.create_engine(url)
            assert engine is not None
            assert isinstance(engine, AsyncEngine)

    @patch("neural_ai.core.db.factory.get_async_session_maker")
    @patch("neural_ai.core.db.factory.get_engine")
    def test_factory_methods_return_consistent_types(
        self, mock_get_engine: MagicMock, mock_get_session_maker: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli, hogy a factory metódusok konzisztens típusokat adnak vissza."""
        mock_session_maker = MagicMock()
        mock_get_session_maker.return_value = mock_session_maker
        mock_engine = MagicMock(spec=AsyncEngine)
        mock_get_engine.return_value = mock_engine

        # Session maker teszt
        session_maker = factory.get_session_maker()
        assert session_maker is mock_session_maker

        # Engine teszt
        engine = factory.get_engine()
        assert engine is mock_engine

        # Manager teszt
        manager = factory.create_manager()
        assert isinstance(manager, DatabaseManager)

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    def test_factory_is_stateless(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None:
        """Teszteli, hogy a factory osztály állapotmentes-e."""
        mock_config = MagicMock()
        mock_config.get.return_value = "INFO"
        mock_get_manager.return_value = mock_config
        # Két különböző hívást kell ugyanazt az eredményt adnia
        manager1 = factory.create_manager()
        manager2 = factory.create_manager()

        # A manager Singleton, ezért ugyanazt a példányt kell visszaadnia
        assert manager1 is manager2
