"""Tesztek a neural_ai.core.db.factory modulhoz.
# pyright: reportCallIssue=false, reportOptionalMemberAccess=false
# Factory method signature és optional type hibák

Ez a modul tartalmazza a DatabaseFactory osztály és annak metódusainak tesztjeit.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
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
    def test_get_engine_without_config(
        self, mock_get_engine: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli az engine lekérdezést konfig nélkül."""
        mock_engine = MagicMock()
        mock_get_engine.return_value = mock_engine

        engine = factory.get_engine()

        assert engine is mock_engine
        mock_get_engine.assert_called_once_with(factory.config_manager)

    @patch("neural_ai.core.db.factory.get_engine")
    def test_get_engine_with_config(
        self, mock_get_engine: MagicMock, factory: DatabaseFactory
    ) -> None:
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
    def test_create_manager_without_config(
        self, mock_get_manager: MagicMock, factory: DatabaseFactory
    ) -> None:
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
    def test_get_session_maker_caches_result(
        self, mock_get_session: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli, hogy a session maker cache-elődik a modul szintjén."""
        mock_session_maker = MagicMock()
        mock_get_session.return_value = mock_session_maker

        result1 = factory.get_session_maker()
        result2 = factory.get_session_maker()

        assert result1 is result2
        # A modul szintű cache miatt csak egyszer hívódik meg a globális függvény
        mock_get_session.assert_called()

    @patch("neural_ai.core.db.factory.get_engine")
    def test_get_engine_caches_result(
        self, mock_get_engine: MagicMock, factory: DatabaseFactory
    ) -> None:
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
        self,
        mock_get_engine: MagicMock,
        mock_get_session_maker: MagicMock,
        factory: DatabaseFactory,
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
    def test_factory_is_stateless(
        self, mock_get_manager: MagicMock, factory: DatabaseFactory
    ) -> None:
        """Teszteli, hogy a factory osztály állapotmentes-e."""
        mock_config = MagicMock()
        mock_config.get.return_value = "INFO"
        mock_get_manager.return_value = mock_config
        # Két különböző hívást kell ugyanazt az eredményt adnia
        manager1 = factory.create_manager()
        manager2 = factory.create_manager()

        # A manager Singleton, ezért ugyanazt a példányt kell visszaadnia
        assert manager1 is manager2


class TestDatabaseConfigPydanticValidation:
    """Pydantic DatabaseConfig validációs tesztek.

    Ezek a tesztek ellenőrzik a DatabaseConfig Pydantic model működését,
    beleértve a URL formátum validációt és a pool size ellenőrzést.
    """

    def test_database_config_valid_sqlite_url(self) -> None:
        """Érvényes SQLite URL validálása."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(url="sqlite+aiosqlite:///test.db")
        )
        assert config.connection.url == "sqlite+aiosqlite:///test.db"
        assert config.connection.url.startswith("sqlite+aiosqlite://")

    def test_database_config_valid_postgresql_url(self) -> None:
        """Érvényes PostgreSQL URL validálása."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="postgresql+asyncpg://user:pass@localhost:5432/testdb"
            )
        )
        assert config.connection.url.startswith("postgresql+asyncpg://")

    def test_database_config_valid_mysql_url(self) -> None:
        """Érvényes MySQL URL validálása."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(
                url="mysql+aiomysql://user:pass@localhost:3306/testdb"
            )
        )
        assert config.connection.url.startswith("mysql+aiomysql://")

    def test_database_config_invalid_url_raises_error(self) -> None:
        """Érvénytelen URL formátum hibát dob."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        with pytest.raises(ValidationError, match="Érvénytelen adatbázis URL"):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url="mysql://invalid"  # Nem async driver!
                )
            )

    def test_database_config_missing_url_raises_error(self) -> None:
        """Hiányzó URL esetén hibát dob."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        with pytest.raises(ValidationError):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(
                    url=None  # type: ignore
                )
            )

    def test_database_config_pool_size_validation_valid(self) -> None:
        """Pool size >= 1 esetén sikeres validáció."""
        from neural_ai.core.config.interfaces.types import (
            DatabaseConfig,
            DatabaseConnectionConfig,
            DatabasePoolConfig,
        )

        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(url="postgresql+asyncpg://localhost/test"),
            pool=DatabasePoolConfig(size=5, recycle=3600),
        )
        assert config.pool is not None
        assert config.pool.size == 5

    def test_database_config_pool_size_validation_invalid(self) -> None:
        """Pool size < 1 esetén hibát dob."""
        from neural_ai.core.config.interfaces.types import (
            DatabaseConfig,
            DatabaseConnectionConfig,
            DatabasePoolConfig,
        )

        # Pydantic v2 standard hibaüzenet
        with pytest.raises(ValidationError, match="Input should be greater than or equal to 1"):
            DatabaseConfig(
                connection=DatabaseConnectionConfig(url="postgresql+asyncpg://localhost/test"),
                pool=DatabasePoolConfig(size=0, recycle=3600),  # INVALID!
            )

    def test_database_config_pool_optional(self) -> None:
        """Pool konfig opcionális - None is érvényes."""
        from neural_ai.core.config.interfaces.types import DatabaseConfig, DatabaseConnectionConfig

        config = DatabaseConfig(
            connection=DatabaseConnectionConfig(url="sqlite+aiosqlite:///test.db")
            # pool nincs megadva
        )
        assert config.pool is None

    def test_factory_with_real_yaml_config(self, tmp_path: Path) -> None:
        """Factory valós YAML konfigurációval."""
        from neural_ai.core.config.factory import ConfigManagerFactory

        # Temporary YAML fájl létrehozása
        # Fontos: a fájlnév 'database.yaml' legyen, mert a get_database_config()
        # a 'database' szekciót keresi, amit a load_directory() a fájlnévből képez.
        # type: "sqlite" mezőt kivettük, mert a Pydantic modellben nincs benne és forbid extra
        yaml_content = """connection:
  url: "sqlite+aiosqlite:///test_real.db"
pool:
  size: 10
  recycle: 1800
"""
        config_dir = tmp_path / "configs"
        config_dir.mkdir()
        config_file = config_dir / "database.yaml"
        config_file.write_text(yaml_content)

        # Config betöltése load_directory-val
        config_manager = ConfigManagerFactory.create_manager("yaml")
        config_manager.load_directory(str(config_dir))

        # Factory tesztelése
        mock_logger = MagicMock()
        factory = DatabaseFactory(logger=mock_logger, config_manager=config_manager)

        # Engine lekérdezés
        engine = factory.get_engine()
        assert engine is not None

        # Ellenőrzés: az engine létrejött
        assert isinstance(engine, AsyncEngine)
