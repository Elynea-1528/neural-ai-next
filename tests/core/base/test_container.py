"""Dependency injection konténer tesztek."""

from abc import ABC, abstractmethod
from unittest.mock import Mock

import pytest

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.exceptions import ComponentNotFoundError, SingletonViolationError


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


def test_register_lazy_component(container: DIContainer) -> None:
    """Teszteli a lusta komponens regisztrálását."""
    instance = DummyImplementation()
    factory_func = Mock(return_value=instance)

    container.register_lazy("test_component", factory_func)

    # A komponens még nem töltődött be
    status = container.get_lazy_components()
    assert "test_component" in status
    assert not status["test_component"]


def test_get_lazy_component(container: DIContainer) -> None:
    """Teszteli a lusta komponens lekérdezését."""
    instance = DummyImplementation()
    factory_func = Mock(return_value=instance)

    container.register_lazy("test_component", factory_func)

    # A komponens most töltődik be
    resolved = container.get("test_component")
    assert resolved == instance
    factory_func.assert_called_once()


def test_get_lazy_component_not_found(container: DIContainer) -> None:
    """Teszteli a nem létező komponens lekérdezését."""
    with pytest.raises(ComponentNotFoundError):
        container.get("nonexistent_component")


def test_get_lazy_components_empty(container: DIContainer) -> None:
    """Teszteli az üres lusta komponens listát."""
    status = container.get_lazy_components()
    assert status == {}


def test_preload_components(container: DIContainer) -> None:
    """Teszteli a komponensek előre betöltését."""
    instance = DummyImplementation()
    factory_func = Mock(return_value=instance)

    container.register_lazy("test_component", factory_func)

    # Előre betöltés
    container.preload_components(["test_component"])

    # A komponens már betöltődött
    status = container.get_lazy_components()
    assert "test_component" not in status  # Már nincs a lusta komponensek között


def test_register_lazy_invalid_name(container: DIContainer) -> None:
    """Teszteli az érvénytelen névvel történő regisztrációt."""
    factory_func = Mock()

    with pytest.raises(ValueError, match="Component name must be a non-empty string"):
        container.register_lazy("", factory_func)


def test_register_lazy_invalid_factory(container: DIContainer) -> None:
    """Teszteli az érvénytelen factory függvénnyel történő regisztrációt."""
    with pytest.raises(ValueError, match="Factory function must be callable"):
        container.register_lazy("test_component", 123)  # type: ignore


def test_register_component(container: DIContainer) -> None:
    """Teszteli a komponens regisztrációt."""
    instance = DummyImplementation()

    container.register("test_component", instance)

    resolved = container.get("test_component")
    assert resolved == instance


def test_register_component_invalid_name(container: DIContainer) -> None:
    """Teszteli az érvénytelen névvel történő regisztrációt."""
    instance = DummyImplementation()

    with pytest.raises(ValueError, match="Component name must be a non-empty string"):
        container.register("", instance)


def test_register_component_none_instance(container: DIContainer) -> None:
    """Teszteli a None példánnyal történő regisztrációt."""
    with pytest.raises(ValueError, match="Instance cannot be None"):
        container.register("test_component", None)


def test_register_component_singleton_violation(container: DIContainer) -> None:
    """Teszteli a singleton szabály megsértését."""
    instance1 = DummyImplementation()
    instance2 = DummyImplementation()

    container.register("test_component", instance1)

    with pytest.raises(SingletonViolationError):
        container.register("test_component", instance2)


def test_get_memory_usage(container: DIContainer) -> None:
    """Teszteli a memóriahasználat lekérdezését."""
    instance = DummyImplementation()
    container.register_instance(DummyInterface, instance)

    stats = container.get_memory_usage()

    assert "total_instances" in stats
    assert "lazy_components" in stats
    assert "loaded_lazy_components" in stats
    assert "instance_sizes" in stats
    assert stats["total_instances"] == 1
    assert stats["lazy_components"] == 0
    assert stats["loaded_lazy_components"] == 0


def test_get_memory_usage_with_lazy(container: DIContainer) -> None:
    """Teszteli a memóriahasználat lekérdezését lusta komponensekkel."""
    instance = DummyImplementation()
    factory_func = Mock(return_value=instance)

    container.register_lazy("test_component", factory_func)

    stats = container.get_memory_usage()

    assert stats["lazy_components"] == 1
    assert stats["loaded_lazy_components"] == 0

    # Betöltjük a komponenst
    container.get("test_component")

    stats = container.get_memory_usage()
    assert stats["loaded_lazy_components"] == 0  # Már nincs lusta komponens
    assert stats["total_instances"] == 1
