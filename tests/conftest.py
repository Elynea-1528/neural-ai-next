"""
Pytest configuration and fixtures for test isolation.

Ez a fájl biztosítja a Singleton és DI Container állapot tisztítását
minden teszt között, megoldva a test isolation problémát.
"""

import pytest
from typing import Generator


@pytest.fixture(autouse=True)
def reset_singletons() -> Generator[None, None, None]:
    """
    Automatikusan reseteli az összes Singleton példányt minden teszt előtt és után.
    
    Ez a fixture autouse=True-val fut minden tesztnél, biztosítva a tiszta állapotot.
    """
    # Teszt előtt: tisztítás
    _clear_all_singletons()
    
    yield
    
    # Teszt után: tisztítás
    _clear_all_singletons()


def _clear_all_singletons() -> None:
    """Törli az összes Singleton példányt a memóriából."""
    import sys
    import gc
    
    # 1. SingletonMeta instances
    try:
        from neural_ai.core.base.implementations.singleton import SingletonMeta
        if hasattr(SingletonMeta, '_instances'):
            SingletonMeta._instances.clear()  # type: ignore
    except (ImportError, AttributeError):
        pass
    
    # 2. DIContainer
    try:
        from neural_ai.core.base.implementations.di_container import DIContainer
        # Reset class-level singleton
        for attr in ['_instance', '_instances']:
            if hasattr(DIContainer, attr):
                setattr(DIContainer, attr, {} if attr == '_instances' else None)
    except (ImportError, AttributeError):
        pass
    
    # 3. CoreComponentFactory
    try:
        from neural_ai.core.base.factory import CoreComponentFactory
        for attr in ['_instance', '_instances']:
            if hasattr(CoreComponentFactory, attr):
                setattr(CoreComponentFactory, attr, {} if attr == '_instances' else None)
    except (ImportError, AttributeError):
        pass
    
    # 4. CoreBridge
    try:
        from neural_ai.ui.core_bridge import CoreBridge
        for attr in ['_instance', '_instances']:
            if hasattr(CoreBridge, attr):
                setattr(CoreBridge, attr, {} if attr == '_instances' else None)
    except (ImportError, AttributeError):
        pass
    
    # 5. DatabaseManager
    try:
        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
        for attr in ['_instance', '_instances', '_engine', '_session_maker']:
            if hasattr(DatabaseManager, attr):
                setattr(DatabaseManager, attr, None)
    except (ImportError, AttributeError):
        pass
    
    # 6. Force garbage collection
    gc.collect()


@pytest.fixture(autouse=True)
def reset_di_container() -> Generator[None, None, None]:
    """
    Automatikusan reseteli a DI Container-t minden teszt előtt és után.
    
    Ez biztosítja, hogy a dependency injection állapot ne szivárogjon át tesztek között.
    """
    # Teszt előtt: tisztítás
    _clear_di_container()
    
    yield
    
    # Teszt után: tisztítás
    _clear_di_container()


def _clear_di_container() -> None:
    """Törli a DI Container állapotát."""
    try:
        from neural_ai.core.base.implementations.di_container import DIContainer
        
        # Singleton példány törlése
        if hasattr(DIContainer, '_instance'):
            DIContainer._instance = None
        if hasattr(DIContainer, '_instances'):
            DIContainer._instances.clear()
        
        # Ha van aktív példány, annak állapotát is töröljük
        try:
            container = DIContainer()
            if hasattr(container, '_services'):
                container._services.clear()
            if hasattr(container, '_factories'):
                container._factories.clear()
        except Exception:
            pass
            
    except (ImportError, AttributeError):
        pass


@pytest.fixture
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tiszta környezeti változók minden teszthez.
    
    Ez a fixture nem autouse, csak explicit használatra.
    """
    # Környezeti változók tisztítása
    import os
    env_vars_to_clear = [
        'DATABASE_URL',
        'NEURAL_AI_ENV',
        'NEURAL_AI_CONFIG_PATH',
    ]
    
    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)
