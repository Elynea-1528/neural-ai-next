"""Pytest fixtures a neural_ai.core.db tesztek számára.

# pyright: reportUnknownArgumentType=false, reportUnknownVariableType=false
# Async fixture type inference hibák.

Ez a modul tartalmazza a közös fixture-öket és setup/teardown logikát
az adatbázis tesztek számára.
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


@pytest.fixture(scope="session", autouse=True)
def mock_config_factory_session():
    """Session scope mock a ConfigManagerFactory számára.

    Ez a fixture biztosítja, hogy a ConfigManagerFactory mock végig él
    az ÖSSZES teszten keresztül, MINDEN pytest-xdist worker-ben.

    FONTOS: Ez a mock NEM autouse, hogy ne zasszunk be minden tesztbe.
    Csak azokat a teszteket érinti, amelyek implicit ConfigManagerFactory-t használnak
    a globális függvényeken keresztül (get_engine, get_async_session_maker, stb.).
    """
    with patch(
        "neural_ai.core.db.implementations.sqlalchemy_session.ConfigManagerFactory"
    ) as mock_factory:
        # Mock config objektum - PYDANTIC COMPATIBLE STRUCTURE
        mock_config = MagicMock(spec=ConfigManagerInterface)

        def config_get_side_effect(key: str, default: object = None) -> object:
            """Mock config.get() with Pydantic-compatible structure."""
            if key == "database":
                return {
                    "connection": {"url": "sqlite+aiosqlite:///:memory:"},
                    "pool": {"size": 20, "recycle": 3600}
                }
            elif key == "config_path":
                return "configs/database.yaml"
            return default

        mock_config.get.side_effect = config_get_side_effect
        mock_factory.get_manager.return_value = mock_config

        yield mock_factory


@pytest.fixture(autouse=True)
async def reset_db_globals():
    """Reset database global state minden teszt előtt és után.

    Ez a fixture biztosítja, hogy a globális _engine és _async_session_maker
    változók tiszták legyenek minden teszt előtt és után, elkerülve a
    test isolation problémákat.

    """
    import neural_ai.core.db.implementations.sqlalchemy_session as db_module

    # Reset ELŐTTE
    if db_module._engine is not None:  # pyright: ignore[reportPrivateUsage]
        try:
            await db_module._engine.dispose()  # pyright: ignore[reportPrivateUsage]
        except Exception:
            pass

    db_module._engine = None  # pyright: ignore[reportPrivateUsage]
    db_module._async_session_maker = None  # pyright: ignore[reportPrivateUsage]

    yield

    # Cleanup UTÁNA
    if db_module._engine is not None:  # pyright: ignore[reportPrivateUsage]
        try:
            await db_module._engine.dispose()  # pyright: ignore[reportGeneralTypeIssues, reportPrivateUsage]
        except Exception:
            pass

    db_module._engine = None  # pyright: ignore[reportPrivateUsage]
    db_module._async_session_maker = None  # pyright: ignore[reportPrivateUsage]


@pytest.fixture(autouse=True)
def reset_db_singleton():
    """Reset DatabaseManager singleton minden teszt előtt és után.

    Ez a fixture biztosítja, hogy a DatabaseManager Singleton példány
    tiszta legyen minden teszt előtt és után.

    """
    from neural_ai.core.base.implementations.singleton import SingletonMeta
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager

    # Clear ELŐTTE
    if hasattr(SingletonMeta, '_instances'):
        if DatabaseManager in SingletonMeta._instances:  # pyright: ignore[reportPrivateUsage]
            del SingletonMeta._instances[DatabaseManager]  # pyright: ignore[reportPrivateUsage]

    yield

    # Cleanup UTÁNA
    if hasattr(SingletonMeta, '_instances'):
        if DatabaseManager in SingletonMeta._instances:  # pyright: ignore[reportPrivateUsage]
            del SingletonMeta._instances[DatabaseManager]  # pyright: ignore[reportPrivateUsage]
