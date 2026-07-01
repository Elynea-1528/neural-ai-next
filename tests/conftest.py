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

    KRITIKUS: Az import cache tisztítást NEM végzi, mert az isinstance() check-et elrontja!
    A patch.stopall() ELÉG a teszt izoláció biztosításához.
    """
    # Teszt előtt: mock tisztítás
    _clear_mock_state()

    yield

    # Teszt után: mock tisztítás (import cache MEGMARAD!)
    _clear_mock_state()


@pytest.fixture(autouse=True)
def reset_singletons() -> Generator[None, None, None]:
    """Automatikusan reseteli az összes Singleton példányt minden teszt előtt és után.

    Ez a fixture autouse=True-val fut minden tesztnél, biztosítva a tiszta állapotot.

    KRITIKUS: NEM törli az import cache-t, mert az isinstance() check-et elrontja!
    A reset_mock_state fixture patch.stopall() függvénye helyreállítja a mock-olt
    modulokat, és ez ELÉG a teszt izoláció biztosításához.
    """
    # Teszt előtt: singleton példányok törlése
    _clear_singleton_instances()

    yield

    # Teszt után: singleton példányok törlése (import cache MEGMARAD!)
    _clear_singleton_instances()


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
        if hasattr(_patch, "_active_patches"):
            _patch._active_patches.clear()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
    except Exception:
        pass


def _clear_singleton_instances() -> None:
    """Törli a singleton példányokat."""
    import gc

    # 0.5. neural_ai.core globális _core_components_instance változó resetelése
    try:
        import neural_ai.core

        if hasattr(neural_ai.core, "_core_components_instance"):
            neural_ai.core._core_components_instance = None  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 1. DIContainer (KRITIKUS: Belső állapot törlése ELŐBB, mint a SingletonMeta clear!)
    try:
        from neural_ai.core.base.implementations.di_container import DIContainer
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        # KRITIKUS FIX: Először töröljük a container instance belső állapotát!
        # A SingletonMeta._instances[DIContainer] tartalmazza a DIContainer singleton példányt
        if DIContainer in SingletonMeta._instances:  # pyright: ignore[reportPrivateUsage]
            try:
                container = SingletonMeta._instances[DIContainer]  # pyright: ignore[reportPrivateUsage]
                # Töröljük a container belső dictionary-jeit (ez a KRITIKUS rész!)
                if hasattr(container, "_instances"):
                    container._instances.clear()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
                if hasattr(container, "_factories"):
                    container._factories.clear()  # pyright: ignore[reportPrivateUsage]
                if hasattr(container, "_lazy_components"):
                    container._lazy_components.clear()  # pyright: ignore[reportPrivateUsage]
            except Exception:
                pass
    except (ImportError, AttributeError):
        pass

    # 2. SingletonMeta instances (KRITIKUS: Ez törli a singleton cache-t!)
    try:
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        if hasattr(SingletonMeta, "_instances"):
            SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 3. LoggerFactory (KRITIKUS: _instances cache)
    try:
        from neural_ai.core.logger.factory import LoggerFactory

        if hasattr(LoggerFactory, "_instances"):
            LoggerFactory._instances.clear()  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 4. ConfigManagerFactory (KRITIKUS: _manager_types cache)
    try:
        from neural_ai.core.config.factory import ConfigManagerFactory

        if hasattr(ConfigManagerFactory, "_manager_types"):
            ConfigManagerFactory._manager_types.clear()  # pyright: ignore[reportPrivateUsage]
        if hasattr(ConfigManagerFactory, "_async_manager_types"):
            ConfigManagerFactory._async_manager_types.clear()  # pyright: ignore[reportPrivateUsage]
        if hasattr(ConfigManagerFactory, "_logger"):
            ConfigManagerFactory._logger = None  # pyright: ignore[reportPrivateUsage]
    except (ImportError, AttributeError):
        pass

    # 5. CoreComponentFactory
    try:
        from neural_ai.core.base.factory import CoreComponentFactory

        for attr in ["_instance", "_instances"]:
            if hasattr(CoreComponentFactory, attr):
                setattr(CoreComponentFactory, attr, {} if attr == "_instances" else None)
    except (ImportError, AttributeError):
        pass

    # 6. CoreBridge
    try:
        from neural_ai.ui.core_bridge import CoreBridge

        for attr in ["_instance", "_instances"]:
            if hasattr(CoreBridge, attr):
                setattr(CoreBridge, attr, {} if attr == "_instances" else None)
    except (ImportError, AttributeError):
        pass

    # 7. DatabaseManager + Module-level globals
    try:
        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
        import neural_ai.core.db.implementations.sqlalchemy_session as db_session_module

        # DatabaseManager class attributes
        for attr in ["_instance", "_instances", "_engine", "_session_maker"]:
            if hasattr(DatabaseManager, attr):
                setattr(DatabaseManager, attr, None)
        
        # KRITIKUS: Module-level global változók tisztítása!
        db_session_module._engine = None
        db_session_module._async_session_maker = None
    except (ImportError, AttributeError):
        pass

    # 8. Force garbage collection
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

        # KRITIKUS: Először töröljük a meglévő példány állapotát, UTÁNA a singleton referenciát!
        # Ha fordított sorrendben tennénk, akkor a DIContainer() új példányt hozna létre.

        # 1. Töröljük a meglévő példány állapotát (ha létezik)
        if hasattr(DIContainer, "_instances") and DIContainer in DIContainer._instances:  # pyright: ignore[reportPrivateUsage]
            try:
                container = DIContainer._instances[DIContainer]  # pyright: ignore[reportPrivateUsage]
                if hasattr(container, "_services"):
                    container._services.clear()  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
                if hasattr(container, "_factories"):
                    container._factories.clear()  # pyright: ignore[reportPrivateUsage]
            except Exception:
                pass

        # 2. Most törölhetjük a singleton referenciákat
        if hasattr(DIContainer, "_instance"):
            DIContainer._instance = None  # pyright: ignore[reportPrivateUsage]
        if hasattr(DIContainer, "_instances"):
            DIContainer._instances.clear()  # pyright: ignore[reportPrivateUsage]

    except (ImportError, AttributeError):
        pass


@pytest.fixture(scope="function")
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tiszta környezeti változók minden teszthez.

    Ez a fixture nem autouse, csak explicit használatra.

    """
    # Környezeti változók tisztítása
    env_vars_to_clear = [
        "DATABASE_URL",
        "NEURAL_AI_ENV",
        "NEURAL_AI_CONFIG_PATH",
    ]

    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)
