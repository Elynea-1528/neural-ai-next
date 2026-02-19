"""Dependency injection konténer tesztjei."""

import pytest

from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.implementations.di_container import DIContainer, LazyComponent


class MockComponent:
    """Mock komponens teszteléshez."""

    def __init__(self, value: str = "test") -> None:
        """Inicializálja a mock komponenst."""
        self.value = value
        self._initialized = True


class TestLazyComponent:
    """LazyComponent tesztjei."""

    def test_initialization(self) -> None:
        """Teszteli a lusta komponens inicializálását."""

        def factory() -> MockComponent:
            return MockComponent("lazy")

        lazy = LazyComponent[MockComponent](factory)

        assert not lazy.is_loaded
        assert lazy.get().value == "lazy"
        assert lazy.is_loaded

    def test_get_multiple_times(self) -> None:
        """Teszteli a többszöri get hívást."""
        call_count = 0

        def factory() -> MockComponent:
            nonlocal call_count
            call_count += 1
            return MockComponent(f"call_{call_count}")

        lazy = LazyComponent[MockComponent](factory)

        # Első hívás
        instance1 = lazy.get()
        assert call_count == 1
        assert instance1.value == "call_1"

        # Második hívás - factory-t nem hívja újra
        instance2 = lazy.get()
        assert call_count == 1
        assert instance2 is instance1


    def test_lazy_component_factory_returns_none(self) -> None:
        """LazyComponent factory_func None visszatérése → ComponentNotFoundError"""
        from neural_ai.core.base.implementations.di_container import LazyComponent
        from neural_ai.core.base.exceptions import ComponentNotFoundError
        
        lazy = LazyComponent(lambda: None)
        with pytest.raises(ComponentNotFoundError, match="Lazy component factory returned None"):
            lazy.get()

class TestDIContainer:
    """DIContainer tesztjei."""

    def test_initialization(self) -> None:
        """Teszteli a konténer inicializálását."""
        container = DIContainer()
        assert container._instances == {}
        assert container._factories == {}
        assert container._lazy_components == {}

    def test_register_instance(self) -> None:
        """Teszteli az instance regisztrálását."""
        container = DIContainer()
        instance = MockComponent("instance")

        container.register_instance(str, instance)

        assert container._instances[str] is instance

    def test_register_factory(self) -> None:
        """Teszteli a factory regisztrálását."""
        container = DIContainer()

        def factory() -> MockComponent:
            return MockComponent("factory")

        container.register_factory(str, factory)

        assert container._factories[str] is factory

    def test_resolve_instance(self) -> None:
        """Teszteli az instance feloldását."""
        container = DIContainer()
        instance = MockComponent("resolve")

        container.register_instance(str, instance)

        resolved = container.resolve(str)
        assert resolved is instance

    def test_resolve_factory(self) -> None:
        """Teszteli a factory feloldását."""
        container = DIContainer()

        def factory() -> MockComponent:
            return MockComponent("factory_resolve")

        container.register_factory(str, factory)

        resolved = container.resolve(str)
        assert isinstance(resolved, MockComponent)
        assert resolved.value == "factory_resolve"

        # Második resolve - ugyanaz az instance
        resolved2 = container.resolve(str)
        assert resolved2 is resolved

    def test_resolve_not_found(self) -> None:
        """Teszteli a nem létező komponens feloldását."""
        container = DIContainer()

        assert container.resolve(str) is None

    def test_register_lazy(self) -> None:
        """Teszteli a lusta komponens regisztrálását."""
        container = DIContainer()

        def factory() -> MockComponent:
            return MockComponent("lazy")

        container.register_lazy("lazy_comp", factory)

        assert "lazy_comp" in container._lazy_components
        assert not container._lazy_components["lazy_comp"].is_loaded

    def test_register_lazy_invalid_name(self) -> None:
        """Teszteli az érvénytelen névvel való regisztrálást."""
        container = DIContainer()

        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register_lazy("", lambda: MockComponent())

    def test_register_lazy_invalid_factory(self) -> None:
        """Teszteli az érvénytelen factory-val való regisztrálást."""
        container = DIContainer()

        with pytest.raises(ValueError, match="Factory function must be callable"):
            container.register_lazy("test", lambda: "not_callable")

    def test_get_regular_instance(self) -> None:
        """Teszteli a reguláris instance lekérését."""
        container = DIContainer()
        instance = MockComponent("regular")

        container._instances["regular_comp"] = instance

        result = container.get("regular_comp")
        assert result is instance

    def test_get_lazy_component(self) -> None:
        """Teszteli a lusta komponens lekérését."""
        container = DIContainer()

        def factory() -> MockComponent:
            return MockComponent("lazy_get")

        container.register_lazy("lazy_get", factory)

        result = container.get("lazy_get")
        assert isinstance(result, MockComponent)
        assert result.value == "lazy_get"

        # Ellenőrizzük, hogy átkerült-e a reguláris instances-be
        assert "lazy_get" in container._instances
        assert "lazy_get" not in container._lazy_components

    def test_get_not_found(self) -> None:
        """Teszteli a nem létező komponens lekérését."""
        container = DIContainer()

        with pytest.raises(ComponentNotFoundError, match="Component 'not_found' not found"):
            container.get("not_found")

    def test_get_lazy_components_status(self) -> None:
        """Teszteli a lusta komponensek státuszának lekérését."""
        container = DIContainer()

        def factory1() -> MockComponent:
            return MockComponent("1")

        def factory2() -> MockComponent:
            return MockComponent("2")

        container.register_lazy("comp1", factory1)
        container.register_lazy("comp2", factory2)

        status = container.get_lazy_components()
        assert status == {"comp1": False, "comp2": False}

        # Betöltjük az egyiket
        container.get("comp1")

        status = container.get_lazy_components()
        assert status == {"comp2": False}  # comp1 már nincs lazy-ben

    def test_preload_components(self) -> None:
        """Teszteli a komponensek előtöltését."""
        container = DIContainer()

        def factory() -> MockComponent:
            return MockComponent("preload")

        container.register_lazy("preload_comp", factory)

        container.preload_components(["preload_comp"])

        assert container.get("preload_comp").value == "preload" # type: ignore

    def test_preload_components_not_found(self) -> None:
        """Teszteli a komponensek előtöltését nem létező komponenssel."""
        container = DIContainer()

        # Nem dob kivételt, csak figyelmen kívül hagyja
        container.preload_components(["not_found_comp"])

        # Üres konténer marad
        assert len(container._lazy_components) == 0

    def test_clear(self) -> None:
        """Teszteli a konténer ürítését."""
        container = DIContainer()

        container._instances["test"] = MockComponent()
        container._factories["test"] = lambda: MockComponent()
        container.register_lazy("lazy", lambda: MockComponent())

        container.clear()

        assert container._instances == {}
        assert container._factories == {}
        assert container._lazy_components == {}

    def test_register_method(self) -> None:
        """Teszteli a register metódust."""
        container = DIContainer()
        instance = MockComponent("register")

        container.register("register_comp", instance)

        assert container._instances["register_comp"] is instance

    def test_register_invalid_name(self) -> None:
        """Teszteli az érvénytelen névvel való regisztrálást."""
        container = DIContainer()

        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register("", MockComponent())

    def test_register_none_instance(self) -> None:
        """Teszteli a None instance regisztrálását."""
        container = DIContainer()

        with pytest.raises(ValueError, match="Instance cannot be None"):
            container.register("test", None)

    def test_enforce_singleton_violation(self) -> None:
        """Teszteli a singleton megsértését."""
        from neural_ai.core.base.exceptions import SingletonViolationError

        container = DIContainer()
        instance1 = MockComponent("1")
        instance2 = MockComponent("2")

        container.register("singleton_comp", instance1)

        # SingletonViolationError várása
        with pytest.raises(SingletonViolationError):
            container.register("singleton_comp", instance2)

    def test_enforce_singleton_no_violation(self) -> None:
        """Teszteli, hogy azonos instance regisztrálása nem okoz problémát."""
        container = DIContainer()
        instance = MockComponent("same")

        # Első regisztráció
        container.register("same_comp", instance)
        # Második regisztráció ugyanazzal az instance-szal - nem dob kivételt
        container.register("same_comp", instance)

    def test_get_memory_usage(self) -> None:
        """Teszteli a memória használat lekérését."""
        container = DIContainer()
        instance = MockComponent()

        container.register("mem_test", instance)
        container.register_lazy("lazy_mem", lambda: MockComponent())

        stats = container.get_memory_usage()

        assert stats["total_instances"] == 1
        assert stats["lazy_components"] == 1
        assert stats["loaded_lazy_components"] == 0
        assert "instance_sizes" in stats
        assert isinstance(stats["instance_sizes"], dict)
