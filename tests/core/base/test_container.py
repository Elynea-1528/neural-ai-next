"""Dependency injection konténer tesztelése."""

import threading
from typing import Any
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.base.container import DIContainer, LazyComponent
from neural_ai.core.base.exceptions import ComponentNotFoundError, SingletonViolationError


class TestLazyComponent:
    """Lusta komponensek tesztelése."""

    def test_lazy_loading_basic(self) -> None:
        """Alap lusta betöltés tesztelése."""
        # Given
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"
        lazy_component = LazyComponent(mock_factory)

        # When
        result = lazy_component.get()

        # Then
        assert result == "test_instance"
        assert lazy_component.is_loaded is True
        mock_factory.assert_called_once()

    def test_lazy_loading_multiple_calls(self) -> None:
        """Többszöri hívás esetén a factory csak egyszer hívódik."""
        # Given
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"
        lazy_component = LazyComponent(mock_factory)

        # When
        result1 = lazy_component.get()
        result2 = lazy_component.get()

        # Then
        assert result1 == result2 == "test_instance"
        mock_factory.assert_called_once()

    def test_is_loaded_property(self) -> None:
        """A betöltöttségi állapot ellenőrzése."""
        # Given
        mock_factory = Mock()
        lazy_component = LazyComponent(mock_factory)

        # When
        loaded_before = lazy_component.is_loaded
        lazy_component.get()
        loaded_after = lazy_component.is_loaded

        # Then
        assert loaded_before is False
        assert loaded_after is True


class TestDIContainer:
    """Dependency injection konténer tesztelése."""

    def test_initialization(self) -> None:
        """Konténer inicializálásának tesztelése."""
        # When
        container = DIContainer()

        # Then
        assert len(container._instances) == 0
        assert len(container._factories) == 0
        assert len(container._lazy_components) == 0

    def test_register_instance(self) -> None:
        """Példány regisztrálásának tesztelése."""
        # Given
        container = DIContainer()
        mock_instance = Mock()

        # When
        container.register_instance(str, mock_instance)

        # Then
        assert str in container._instances
        assert container._instances[str] == mock_instance

    def test_register_factory(self) -> None:
        """Factory regisztrálásának tesztelése."""
        # Given
        container = DIContainer()
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"

        # When
        container.register_factory(str, mock_factory)
        result = container.resolve(str)

        # Then
        assert result == "test_instance"  # type: ignore
        mock_factory.assert_called_once()

    def test_resolve_instance(self) -> None:
        """Példány feloldásának tesztelése."""
        # Given
        container = DIContainer()
        mock_instance = Mock()
        container.register_instance(str, mock_instance)

        # When
        result = container.resolve(str)

        # Then
        assert result == mock_instance

    def test_resolve_factory(self) -> None:
        """Factory feloldásának tesztelése."""
        # Given
        container = DIContainer()
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"
        container.register_factory(str, mock_factory)

        # When
        result = container.resolve(str)

        # Then
        assert result == "test_instance"
        mock_factory.assert_called_once()

    def test_resolve_not_found(self) -> None:
        """Nem létező komponens feloldásának tesztelése."""
        # Given
        container = DIContainer()

        # When
        result = container.resolve(str)

        # Then
        assert result is None

    def test_register_lazy_component(self) -> None:
        """Lusta komponens regisztrálásának tesztelése."""
        # Given
        container = DIContainer()
        mock_factory = Mock()

        # When
        container.register_lazy("test_component", mock_factory)

        # Then
        assert "test_component" in container._lazy_components

    def test_register_lazy_invalid_name(self) -> None:
        """Érvénytelen névvel történő regisztráció tesztelése."""
        # Given
        container = DIContainer()

        # When / Then
        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register_lazy("", Mock())

    def test_register_lazy_invalid_factory(self) -> None:
        """Érvénytelen factory függvénnyel történő regisztráció tesztelése."""
        # Given
        container = DIContainer()

        # When / Then
        with pytest.raises(ValueError, match="Factory function must be callable"):
            container.register_lazy("test", "not_callable")  # type: ignore

    def test_get_lazy_component(self) -> None:
        """Lusta komponens lekérésének tesztelése."""
        # Given
        container = DIContainer()
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"
        container.register_lazy("test_component", mock_factory)

        # When
        result = container.get("test_component")

        # Then
        assert result == "test_instance"
        mock_factory.assert_called_once()
        assert "test_component" not in container._lazy_components
        assert "test_component" in container._instances

    def test_get_component_not_found(self) -> None:
        """Nem létező komponens lekérésének tesztelése."""
        # Given
        container = DIContainer()

        # When / Then
        with pytest.raises(ComponentNotFoundError, match="Component 'missing' not found"):
            container.get("missing")

    def test_get_lazy_components_status(self) -> None:
        """Lusta komponensek állapotának lekérdezése."""
        # Given
        container = DIContainer()
        mock_factory1 = Mock(return_value="instance1")
        mock_factory2 = Mock(return_value="instance2")
        container.register_lazy("component1", mock_factory1)
        container.register_lazy("component2", mock_factory2)

        # When
        status = container.get_lazy_components()

        # Then
        assert status["component1"] is False
        assert status["component2"] is False

        # When - betöltés után
        container.get("component1")
        # component1 már nincs a lazy components között, mert átkerült a regular instances-be
        status_after = container.get_lazy_components()

        # Then
        assert "component1" not in status_after  # már nincs lusta komponensként
        assert status_after.get("component2") is False

    def test_preload_components(self) -> None:
        """Komponensek előzetes betöltésének tesztelése."""
        # Given
        container = DIContainer()
        mock_factory = Mock()
        mock_factory.return_value = "test_instance"
        container.register_lazy("test_component", mock_factory)

        # When
        container.preload_components(["test_component"])

        # Then
        assert "test_component" not in container._lazy_components
        assert "test_component" in container._instances

    def test_clear_container(self) -> None:
        """Konténer ürítésének tesztelése."""
        # Given
        container = DIContainer()
        container.register_instance(str, "test")
        container.register_factory(int, lambda: 42)  # type: ignore

        # When
        container.clear()

        # Then
        assert len(container._instances) == 0
        assert len(container._factories) == 0

    def test_register_component(self) -> None:
        """Komponens regisztrálásának tesztelése."""
        # Given
        container = DIContainer()
        mock_instance = Mock()

        # When
        container.register("test_component", mock_instance)

        # Then
        assert "test_component" in container._instances
        assert container._instances["test_component"] == mock_instance

    def test_register_component_invalid_name(self) -> None:
        """Érvénytelen névvel történő komponens regisztráció tesztelése."""
        # Given
        container = DIContainer()

        # When / Then
        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register("", Mock())

    def test_register_component_none_instance(self) -> None:
        """None példánnyal történő regisztráció tesztelése."""
        # Given
        container = DIContainer()

        # When / Then
        with pytest.raises(ValueError, match="Instance cannot be None"):
            container.register("test", None)  # type: ignore

    def test_singleton_violation_detection(self) -> None:
        """Singleton minta megsértésének észlelése."""
        # Given
        container = DIContainer()
        instance1 = Mock()
        instance2 = Mock()

        # When
        container.register("test", instance1)

        # Then
        with pytest.raises(SingletonViolationError):
            container.register("test", instance2)

    def test_get_memory_usage(self) -> None:
        """Memóriahasználat lekérdezésének tesztelése."""
        # Given
        container = DIContainer()
        container.register_instance("test1", "value1")
        container.register_instance("test2", 42)

        # When
        stats = container.get_memory_usage()

        # Then
        assert stats["total_instances"] == 2
        instance_sizes = stats["instance_sizes"]
        assert isinstance(instance_sizes, dict)
        assert "test1" in instance_sizes
        assert "test2" in instance_sizes

    @patch("logging.getLogger")
    def test_logger_integration(self, mock_get_logger: Any) -> None:
        """Logger integráció tesztelése."""
        # Given
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        # When
        container = DIContainer()
        container.register_lazy("test", lambda: "instance")

        # Then
        mock_logger.info.assert_called_once()

    def test_verify_singleton_warning(self) -> None:
        """Singleton ellenőrzés figyelmeztetés tesztelése."""
        # Given
        container = DIContainer()

        class NonSingletonClass:
            pass

        instance = NonSingletonClass()

        # When / Then
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            container.register_instance("test", instance)
            container.get("test")

            # Then
            assert len(w) >= 1
            assert "singleton" in str(w[0].message).lower()

    def test_thread_safety(self) -> None:
        """Szálbiztosság tesztelése."""
        # Given
        container = DIContainer()
        # Előre regisztráljuk a komponenseket, hogy a szálak csak olvassanak
        container.register_lazy("component0", lambda: "instance0")
        container.register_lazy("component1", lambda: "instance1")
        results: list[str] = []
        lock = threading.Lock()

        def worker(thread_id: int) -> None:
            instance = container.get(f"component{thread_id % 2}")
            with lock:
                results.append(f"Thread {thread_id}: {instance}")

        # When
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Then
        assert len(results) == 4
        # Ellenőrizzük, hogy minden szál megkapta a megfelelő instance-t
        assert all("instance0" in r or "instance1" in r for r in results)
