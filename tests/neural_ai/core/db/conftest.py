"""Pytest fixtures a neural_ai.core.db tesztek számára.

Ez a modul tartalmazza a közös fixture-öket és setup/teardown logikát
az adatbázis tesztek számára.
"""

import pytest


@pytest.fixture(autouse=True)
async def reset_db_globals():
    """Reset database global state minden teszt előtt és után.
    
    Ez a fixture biztosítja, hogy a globális _engine és _async_session_maker
    változók tiszták legyenek minden teszt előtt és után, elkerülve a
    test isolation problémákat.
    """
    import neural_ai.core.db.implementations.sqlalchemy_session as db_module

    # Reset ELŐTTE
    if db_module._engine is not None:
        try:
            await db_module._engine.dispose()
        except Exception:
            pass

    db_module._engine = None
    db_module._async_session_maker = None

    yield

    # Cleanup UTÁNA
    if db_module._engine is not None:
        try:
            await db_module._engine.dispose()
        except Exception:
            pass

    db_module._engine = None
    db_module._async_session_maker = None


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
        if DatabaseManager in SingletonMeta._instances:
            del SingletonMeta._instances[DatabaseManager]

    yield

    # Cleanup UTÁNA
    if hasattr(SingletonMeta, '_instances'):
        if DatabaseManager in SingletonMeta._instances:
            del SingletonMeta._instances[DatabaseManager]
