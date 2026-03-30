"""Pytest configuration and fixtures for test isolation.

# pyright: reportPrivateUsage=false, reportUnknownMemberType=false
# Pytest fixture és mock private member access hibák.

Ez a fájl biztosítja a Singleton és DI Container állapot tisztítását
minden teszt között, megoldva a test isolation problémát.
"""

import sys
from collections.abc import Generator
from pathlib import Path

import pytest

# Projekt gyökér hozzáadása a sys.path-hoz (pytest discovery fázisához)
# Ez biztosítja, hogy a 'scripts' és más top-level modulok elérhetők legyenek
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture(autouse=True)
def reset_mock_state() -> Generator[None, None, None]:
    """Automatikusan reseteli az összes mock állapotot minden teszt előtt és után.

    Ez megoldja a mock state szennyeződést, ahol a @patch dekorátorok
    állapota átszivárodik tesztek között.

    """
    # Teszt előtt: mock tisztítás
    _clear_mock_state()

    yield

    # Teszt után: mock tisztítás
    _clear_mock_state()


@pytest.fixture(autouse=True)
def reset_singletons() -> Generator[None, None, None]:
    """Automatikusan reseteli az összes Singleton példányt minden teszt előtt és után.

    Ez a fixture autouse=True-val fut minden tesztnél, biztosítva a tiszta állapotot.

    """
    # Teszt előtt: tisztítás
    _clear_all_singletons()

    yield

    # Teszt után: tisztítás
    _clear_all_singletons()


def _clear_mock_state() -> None:
    """Törli az összes mock állapotot, hogy a @patch dekorátorok ne szivárogjon át tesztek között.

    Ez megoldja a mock state szennyeződést, ahol egy teszt mock-ja
    befolyásolja a következő teszteket.

    """
    from unittest.mock import _patch, patch  # pyright: ignore[reportPrivateUsage]

    # 1. Stopoljuk az összes aktív patch-et
    try:
        patch.stopall()
    except Exception:
        pass

    # 2. Töröljük a _patch._active_patches listát
    try:
        if hasattr(_patch, '_active_patches'):
            _patch._active_patches.clear()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    except Exception:
        pass


def _clear_import_cache() -> None:
    """Törli a Python import cache-t.

    A mock-olt vagy elrontott importok ne szivárogjon át tesztek között.

    Ez megoldja a teszt izolációs problémát, ahol egy teszt mock-olja
    a LoggerInterface-t, és az összes utána következő teszt elromlik.

    """
    import sys

    # Modulok listája, amelyeket törölni kell
    modules_to_clear = [
        'neural_ai.core.logger.interfaces.logger_interface',
        'neural_ai.core.config.interfaces.config_manager_interface',
        'neural_ai.data.storage.interfaces.storage_interface',
        'neural_ai.core.base.factory',
        'neural_ai.core.logger.factory',
        'neural_ai.core.config.implementations.yaml_config_manager',
        'neural_ai.core.config.implementations.dynamic_config_manager',
        'neural_ai.core.config.implementations',  # Szülő modul is!
    ]

    for module_name in modules_to_clear:
        if module_name in sys.modules:
            del sys.modules[module_name]


def _clear_all_singletons() -> None:
    """Törli az összes Singleton példányt a memóriából."""
    import gc

    # 0. Import cache tisztítása (KRITIKUS: teszt izolációhoz)
    _clear_import_cache()

    # 0.5. neural_ai.core globális _core_components_instance változó resetelése
    try:
        import neural_ai.core
        if hasattr(neural_ai.core, '_core_components_instance'):
            neural_ai.core._core_components_instance = None  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 1. SingletonMeta instances
    try:
        from neural_ai.core.base.implementations.singleton import SingletonMeta
        if hasattr(SingletonMeta, '_instances'):
            SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]
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

    # 3. LoggerFactory (KRITIKUS: _instances cache)
    try:
        from neural_ai.core.logger.factory import LoggerFactory
        if hasattr(LoggerFactory, '_instances'):
            LoggerFactory._instances.clear()  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 4. CoreComponentFactory
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
    """Automatikusan reseteli a DI Container-t minden teszt előtt és után.

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
            DIContainer._instance = None  # pyright: ignore[reportPrivateUsage]
        if hasattr(DIContainer, '_instances'):
            DIContainer._instances.clear()  # pyright: ignore[reportPrivateUsage]

        # Ha van aktív példány, annak állapotát is töröljük
        try:
            container = DIContainer()
            if hasattr(container, '_services'):
                container._services.clear()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
            if hasattr(container, '_factories'):
                container._factories.clear()  # pyright: ignore[reportPrivateUsage]
        except Exception:
            pass

    except (ImportError, AttributeError):
        pass


@pytest.fixture
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tiszta környezeti változók minden teszthez.

    Ez a fixture nem autouse, csak explicit használatra.

    """
    # Környezeti változók tisztítása
    env_vars_to_clear = [
        'DATABASE_URL',
        'NEURAL_AI_ENV',
        'NEURAL_AI_CONFIG_PATH',
    ]

    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)
