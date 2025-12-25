"""Tesztek a DIContainer és LazyComponent osztályokhoz."""

import warnings

import pytest

from neural_ai.core.base.exceptions import ComponentNotFoundError, SingletonViolationError
from neural_ai.core.base.implementations.di_container import DIContainer, LazyComponent


class TestLazyComponent:
    """Lusta komponens tesztelése."""

    def test_lazy_loading_initial_state(self) -> None:
        """Teszteli a lusta betöltés kezdeti állapotát."""
        # Arrange
        def factory() -> str:
            return "test_instance"

        # Act
        component = LazyComponent(factory)

        # Assert
        assert not component.is_loaded
        assert component._instance is None

    def test_lazy_loading_get(self) -> None:
        """Teszteli a lusta betöltésű komponens lekérését."""
        # Arrange
        def factory() -> str:
            return "test_instance"

        component = LazyComponent(factory)

        # Act
        result = component.get()

        # Assert
        assert result == "test_instance"
        assert component.is_loaded
        assert component._instance == "test_instance"

    def test_lazy_loading_thread_safety(self) -> None:
        """Teszteli a szálbiztosságot."""
        # Arrange
        call_count = 0

        def factory() -> int:
            nonlocal call_count
            call_count += 1
            return call_count

        component = LazyComponent(factory)

        # Act
        import threading

        results: list[int] = []
        threads = []

        def get_component() -> None:
            results.append(component.get())

        for _ in range(10):
            thread = threading.Thread(target=get_component)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Assert
        assert len(results) == 10
        assert all(r == 1 for r in results)  # Minden szál ugyanazt az instance-t kapja
        assert call_count == 1  # A factory csak egyszer hívódik meg


class TestDIContainer:
    """DI konténer tesztelése."""

    def test_initialization(self) -> None:
        """Teszteli a konténer inicializálását."""
        # Act
        container = DIContainer()

        # Assert
        assert len(container._instances) == 0
        assert len(container._factories) == 0
        assert len(container._lazy_components) == 0

    def test_register_instance(self) -> None:
        """Teszteli a példány regisztrálását."""
        # Arrange
        container = DIContainer()
        instance = "test_string"

        # Act
        container.register_instance(str, instance)

        # Assert
        assert str in container._instances
        assert container._instances[str] == instance

    def test_register_factory(self) -> None:
        """Teszteli a factory regisztrálását."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        # Act
        container.register_factory(str, factory)

        # Assert
        assert str in container._factories
        assert container._factories[str] == factory

    def test_resolve_instance(self) -> None:
        """Teszteli a példány feloldását."""
        # Arrange
        container = DIContainer()
        instance = "test_string"
        container.register_instance(str, instance)

        # Act
        result = container.resolve(str)

        # Assert
        assert result == instance

    def test_resolve_factory(self) -> None:
        """Teszteli a factory feloldását."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        container.register_factory(str, factory)

        # Act
        result = container.resolve(str)

        # Assert
        assert result == "test_string"
        assert str in container._instances  # A factory által létrehozott instance el van mentve

    def test_resolve_not_found(self) -> None:
        """Teszteli a nem található komponens feloldását."""
        # Arrange
        container = DIContainer()

        # Act
        result = container.resolve(str)

        # Assert
        assert result is None

    def test_register_lazy_valid(self) -> None:
        """Teszteli az érvényes lusta komponens regisztrálását."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        # Act
        container.register_lazy("test_component", factory)

        # Assert
        assert "test_component" in container._lazy_components
        assert not container._lazy_components["test_component"].is_loaded

    def test_register_lazy_invalid_name(self) -> None:
        """Teszteli az érvénytelen névvel történő regisztrálást."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        # Act & Assert
        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register_lazy("", factory)

    def test_register_lazy_invalid_factory(self) -> None:
        """Teszteli az érvénytelen factory-val történő regisztrálást."""
        # Arrange
        container = DIContainer()

        # Act & Assert
        with pytest.raises(ValueError, match="Factory function must be callable"):
            container.register_lazy("test_component", "not_callable")  # type: ignore

    def test_get_lazy_component(self) -> None:
        """Teszteli a lusta komponens lekérését."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        container.register_lazy("test_component", factory)

        # Act
        result = container.get("test_component")

        # Assert
        assert result == "test_string"
        assert "test_component" not in container._lazy_components  # Áthelyeződik a regular instances-be
        assert "test_component" in container._instances

    def test_get_component_not_found(self) -> None:
        """Teszteli a nem található komponens lekérését."""
        # Arrange
        container = DIContainer()

        # Act & Assert
        with pytest.raises(ComponentNotFoundError, match="Component 'missing' not found"):
            container.get("missing")

    def test_get_lazy_components_status(self) -> None:
        """Teszteli a lusta komponensek állapotának lekérését."""
        # Arrange
        container = DIContainer()

        def factory1() -> str:
            return "test1"

        def factory2() -> str:
            return "test2"

        container.register_lazy("component1", factory1)
        container.register_lazy("component2", factory2)

        # Act
        status = container.get_lazy_components()

        # Assert
        assert status == {"component1": False, "component2": False}

        # Betöltjük az egyiket
        container.get("component1")
        status = container.get_lazy_components()
        assert status == {"component2": False}

    def test_preload_components(self) -> None:
        """Teszteli a komponensek előtöltését."""
        # Arrange
        container = DIContainer()

        def factory() -> str:
            return "test_string"

        container.register_lazy("test_component", factory)

        # Act
        container.preload_components(["test_component"])

        # Assert
        assert "test_component" not in container._lazy_components
        assert "test_component" in container._instances

    def test_clear(self) -> None:
        """Teszteli a konténer ürítését."""
        # Arrange
        container = DIContainer()
        container.register_instance(str, "test")
        container.register_factory(int, lambda: 42)
        container.register_lazy("lazy", lambda: "lazy_test")

        # Act
        container.clear()

        # Assert
        assert len(container._instances) == 0
        assert len(container._factories) == 0
        assert len(container._lazy_components) == 0

    def test_verify_singleton_warning(self) -> None:
        """Teszteli a singleton ellenőrzés figyelmeztetését."""
        # Arrange
        container = DIContainer()

        class NonSingletonClass:
            pass

        instance = NonSingletonClass()

        # Act & Assert
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            container._verify_singleton(instance, "test_component")

            # Assert
            assert len(w) >= 1
            assert "does not have _initialized flag" in str(w[0].message)

    def test_enforce_singleton_violation(self) -> None:
        """Teszteli a singleton megsértésének észlelését."""
        # Arrange
        container = DIContainer()
        instance1 = object()
        instance2 = object()

        # Act
        container._instances["test_component"] = instance1

        # Assert
        with pytest.raises(SingletonViolationError, match="Singleton pattern violated"):
            container._enforce_singleton("test_component", instance2)

    def test_register_valid(self) -> None:
        """Teszteli az érvényes komponens regisztrálását."""
        # Arrange
        container = DIContainer()
        instance = "test_string"

        # Act
        container.register("test_component", instance)

        # Assert
        assert "test_component" in container._instances
        assert container._instances["test_component"] == instance

    def test_register_invalid_name(self) -> None:
        """Teszteli az érvénytelen névvel történő regisztrálást."""
        # Arrange
        container = DIContainer()

        # Act & Assert
        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register("", "test")

    def test_register_none_instance(self) -> None:
        """Teszteli a None példány regisztrálását."""
        # Arrange
        container = DIContainer()

        # Act & Assert
        with pytest.raises(ValueError, match="Instance cannot be None"):
            container.register("test_component", None)  # type: ignore

    def test_get_memory_usage(self) -> None:
        """Teszteli a memóriahasználat lekérését."""
        # Arrange
        container = DIContainer()
        container.register_instance("str1", "test_string_1")
        container.register_instance("int1", 42)

        # Act
        stats = container.get_memory_usage()

        # Assert
        assert stats["total_instances"] == 2
        assert stats["lazy_components"] == 0
        assert stats["loaded_lazy_components"] == 0
        assert isinstance(stats["instance_sizes"], dict)
        assert "str1" in stats["instance_sizes"]
        assert "int1" in stats["instance_sizes"]


    def test_get_regular_instance(self) -> None:
        """Teszteli a regisztrált példány lekérését a get metódussal."""
        # Arrange
        container = DIContainer()
        test_instance = "test_value"
        container.register("test_component", test_instance)

        # Act
        result = container.get("test_component")

        # Assert
        assert result == test_instance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
