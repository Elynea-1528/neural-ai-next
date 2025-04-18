"""Dependency injection konténer tesztek."""

from abc import ABC, abstractmethod
from unittest.mock import Mock

import pytest

from neural_ai.core.base.container import DIContainer


class DummyInterface(ABC):
    """Teszt interfész."""

    @abstractmethod
    def do_something(self) -> None:
        """Teszt metódus."""
        pass


class DummyImplementation(DummyInterface):
    """Teszt implementáció."""

    def do_something(self) -> None:
        """Teszt metódus implementáció."""
        pass


@pytest.fixture
def container() -> DIContainer:
    """DI konténer fixture."""
    return DIContainer()


def test_register_and_resolve_instance(container: DIContainer) -> None:
    """Teszteli példány regisztrálását és feloldását."""
    instance = DummyImplementation()
    container.register_instance(DummyInterface, instance)

    resolved = container.resolve(DummyInterface)
    assert resolved == instance


def test_register_and_resolve_factory(container: DIContainer) -> None:
    """Teszteli factory függvény regisztrálását és feloldását."""
    instance = DummyImplementation()
    factory = Mock(return_value=instance)
    container.register_factory(DummyInterface, factory)

    resolved = container.resolve(DummyInterface)
    assert resolved == instance
    factory.assert_called_once()


def test_resolve_unknown_interface(container: DIContainer) -> None:
    """Teszteli nem regisztrált interfész feloldását."""
    resolved = container.resolve(DummyInterface)
    assert resolved is None


def test_resolve_caches_factory_result(container: DIContainer) -> None:
    """Teszteli, hogy a factory által létrehozott példány cache-elődik."""
    instance = DummyImplementation()
    factory = Mock(return_value=instance)
    container.register_factory(DummyInterface, factory)

    first = container.resolve(DummyInterface)
    second = container.resolve(DummyInterface)

    assert first == second
    factory.assert_called_once()


def test_clear_container(container: DIContainer) -> None:
    """Teszteli a konténer ürítését."""
    instance = DummyImplementation()
    container.register_instance(DummyInterface, instance)

    container.clear()
    resolved = container.resolve(DummyInterface)
    assert resolved is None


def test_register_instance_overrides_factory(container: DIContainer) -> None:
    """Teszteli, hogy a példány regisztrálás felülírja a factory-t."""
    factory_instance = DummyImplementation()
    instance = DummyImplementation()
    factory = Mock(return_value=factory_instance)

    container.register_factory(DummyInterface, factory)
    container.register_instance(DummyInterface, instance)

    resolved = container.resolve(DummyInterface)
    assert resolved == instance
    factory.assert_not_called()


def test_type_safety(container: DIContainer) -> None:
    """Teszteli a típusbiztonságot."""

    class WrongImplementation:
        """Hibás implementáció, nem származik a DummyInterface-ből."""

        pass

    wrong_instance = WrongImplementation()
    instance = DummyImplementation()

    # A helyes típusú példány regisztrálása működik
    container.register_instance(DummyInterface, instance)
    resolved = container.resolve(DummyInterface)
    assert isinstance(resolved, DummyImplementation)

    # A helytelen típusú példány is működik, mert a Python duck-typing alapú
    container.register_instance(DummyInterface, wrong_instance)
    resolved = container.resolve(DummyInterface)
    assert isinstance(resolved, WrongImplementation)
