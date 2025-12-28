"""DIContainer és LazyComponent tesztek.

Ez a modul tartalmazza a DIContainer és LazyComponent osztályok
egységtesztjeit, beleértve a regisztrációt, feloldást és lusta betöltést.
"""

from unittest.mock import MagicMock, patch

import pytest
import structlog

from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.implementations.di_container import DIContainer, LazyComponent


class TestLazyComponent:
    """LazyComponent osztály tesztjei."""

    def test_init(self) -> None:
        """Teszteli a LazyComponent inicializálását."""
        factory_func: MagicMock = MagicMock(return_value="test_instance")
        component: LazyComponent[str] = LazyComponent(factory_func)

        assert not component.is_loaded
        # Megjegyzés: A _factory_func protected, de a tesztelés miatt ellenőrizzük
        # A valós használatban csak a get() metódust használjuk

    def test_get_first_access(self) -> None:
        """Teszteli a komponens első hozzáférését (betöltéssel)."""
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)
        component: LazyComponent[MagicMock] = LazyComponent(factory_func)

        result = component.get()

        assert result is mock_instance
        assert component.is_loaded
        factory_func.assert_called_once()

    def test_get_multiple_access(self) -> None:
        """Teszteli, hogy a factory csak egyszer hívódik meg többszöri hozzáféréskor."""
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)
        component: LazyComponent[MagicMock] = LazyComponent(factory_func)

        result1 = component.get()
        result2 = component.get()
        result3 = component.get()

        assert result1 is mock_instance
        assert result2 is mock_instance
        assert result3 is mock_instance
        assert component.is_loaded
        factory_func.assert_called_once()


class TestDIContainer:
    """DIContainer osztály tesztjei."""

    def test_init(self) -> None:
        """Teszteli a DIContainer inicializálását."""
        container: DIContainer = DIContainer()

        # A konténer kezdetben üres
        assert container.resolve(object) is None
        assert container.get_lazy_components() == {}

    def test_register_instance(self) -> None:
        """Teszteli a példány regisztrálását."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()

        container.register_instance(str, mock_instance)

        # A regisztrált példány feloldható
        result = container.resolve(str)
        assert result is mock_instance

    def test_register_factory(self) -> None:
        """Teszteli a factory regisztrálását."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)

        container.register_factory(str, factory_func)

        # A factory által létrehozott példány feloldható
        result = container.resolve(str)
        assert result is mock_instance

    def test_resolve_instance(self) -> None:
        """Teszteli a példány feloldását."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        container.register_instance(str, mock_instance)

        result = container.resolve(str)

        assert result is mock_instance

    def test_resolve_factory(self) -> None:
        """Teszteli a factory által létrehozott példány feloldását."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)
        container.register_factory(str, factory_func)

        result = container.resolve(str)

        assert result is mock_instance
        factory_func.assert_called_once()

    def test_resolve_not_found(self) -> None:
        """Teszteli a feloldást nem létező interfész esetén."""
        container: DIContainer = DIContainer()

        result = container.resolve(str)

        assert result is None

    def test_register_lazy_valid(self) -> None:
        """Teszteli a lusta komponens regisztrálását érvényes adatokkal."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)

        container.register_lazy("test_component", factory_func)

        # A lusta komponens lekérhető
        result = container.get("test_component")
        assert result is mock_instance

    def test_register_lazy_empty_name(self) -> None:
        """Teszteli a lusta komponens regisztrálását üres névvel."""
        container: DIContainer = DIContainer()
        factory_func: MagicMock = MagicMock()

        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register_lazy("", factory_func)

    def test_register_lazy_not_callable(self) -> None:
        """Teszteli a lusta komponens regisztrálását nem hívható factory-val."""
        container: DIContainer = DIContainer()

        with pytest.raises(ValueError, match="Factory function must be callable"):
            container.register_lazy("test", "not_callable")  # type: ignore

    def test_get_lazy_component(self) -> None:
        """Teszteli a lusta komponens lekérését."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)
        container.register_lazy("test_component", factory_func)

        result = container.get("test_component")

        assert result is mock_instance
        factory_func.assert_called_once()

    def test_get_lazy_component_not_found(self) -> None:
        """Teszteli a lusta komponens lekérését nem létező névvel."""
        container: DIContainer = DIContainer()

        with pytest.raises(ComponentNotFoundError, match="Component 'test' not found"):
            container.get("test")

    def test_get_lazy_components(self) -> None:
        """Teszteli a lusta komponensek státuszának lekérdezését."""
        container: DIContainer = DIContainer()
        factory_func1: MagicMock = MagicMock()
        factory_func2: MagicMock = MagicMock()
        container.register_lazy("component1", factory_func1)
        container.register_lazy("component2", factory_func2)

        status = container.get_lazy_components()

        assert status == {"component1": False, "component2": False}

    def test_preload_components(self) -> None:
        """Teszteli a komponensek előtöltését."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()
        factory_func: MagicMock = MagicMock(return_value=mock_instance)
        container.register_lazy("test_component", factory_func)

        # Előtöltés előtt még nem töltődött be
        assert container.get_lazy_components() == {"test_component": False}

        container.preload_components(["test_component"])

        # Előtöltés után a komponens betöltődik és áthelyeződik az instances-be
        # Ezért a lazy_components-ből eltűnik
        assert container.get_lazy_components() == {}
        # De lekérhető marad
        result = container.get("test_component")
        assert result is mock_instance

    def test_clear(self) -> None:
        """Teszteli a konténer kiürítését."""
        container: DIContainer = DIContainer()
        container.register_instance(str, "test")
        container.register_factory(int, lambda: 42)
        container.register_lazy("test", lambda: "value")

        container.clear()

        # A konténer üres lesz
        assert container.resolve(str) is None
        assert container.get_lazy_components() == {}

    def test_register_valid(self) -> None:
        """Teszteli a komponens regisztrálását érvényes adatokkal."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()

        container.register("test_component", mock_instance)

        # A regisztrált komponens lekérhető
        result = container.get("test_component")
        assert result is mock_instance

    def test_register_empty_name(self) -> None:
        """Teszteli a komponens regisztrálását üres névvel."""
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()

        with pytest.raises(ValueError, match="Component name must be a non-empty string"):
            container.register("", mock_instance)

    def test_register_none_instance(self) -> None:
        """Teszteli a komponens regisztrálását None példánnyal."""
        container: DIContainer = DIContainer()

        with pytest.raises(ValueError, match="Instance cannot be None"):
            container.register("test", None)  # type: ignore

    def test_get_memory_usage(self) -> None:
        """Teszteli a memóriahasználat lekérdezését."""
        container: DIContainer = DIContainer()
        container.register("test1", "value1")
        container.register("test2", 42)

        stats = container.get_memory_usage()

        assert stats["total_instances"] == 2
        assert stats["lazy_components"] == 0
        assert "instance_sizes" in stats
        assert isinstance(stats["instance_sizes"], dict)

    @patch.object(structlog, "get_logger")
    def test_register_instance_logging(self, mock_get_logger: MagicMock) -> None:
        """Teszteli a naplózást példány regisztrálásakor."""
        mock_logger: MagicMock = MagicMock()
        mock_get_logger.return_value = mock_logger
        container: DIContainer = DIContainer()
        mock_instance: MagicMock = MagicMock()

        container.register_instance(str, mock_instance)

        mock_logger.debug.assert_called()

    def test_verify_singleton_missing_initialized(self) -> None:
        """Teszteli a singleton ellenőrzést hiányzó _initialized flag esetén."""
        container: DIContainer = DIContainer()

        class TestClass:
            pass

        instance = TestClass()

        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            container._verify_singleton(instance, "test_component")
            assert len(w) == 1
            assert "_initialized" in str(w[0].message)
