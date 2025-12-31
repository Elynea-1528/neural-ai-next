"""Core base implementations modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.implementations.__init__.py fájlban
definiált exportokat és funkcionalitásokat.
"""

from neural_ai.core.base.implementations import (
    DIContainer,
    LazyComponent,
    LazyLoader,
    SingletonMeta,
    lazy_property,
)
from neural_ai.core.base.implementations.component_bundle import CoreComponents


class TestImplementationsInit:
    """Implementations modul __init__.py tesztjei."""

    def test_core_components_import(self) -> None:
        """Teszteli, hogy a CoreComponents importálható-e."""
        assert CoreComponents is not None
        assert hasattr(CoreComponents, "__name__")
        assert CoreComponents.__name__ == "CoreComponents"

    def test_dicontainer_import(self) -> None:
        """Teszteli, hogy a DIContainer importálható-e."""
        assert DIContainer is not None
        assert hasattr(DIContainer, "__name__")
        assert DIContainer.__name__ == "DIContainer"

    def test_lazy_component_import(self) -> None:
        """Teszteli, hogy a LazyComponent importálható-e."""
        assert LazyComponent is not None
        assert hasattr(LazyComponent, "__name__")
        assert LazyComponent.__name__ == "LazyComponent"

    def test_lazy_loader_import(self) -> None:
        """Teszteli, hogy a LazyLoader importálható-e."""
        assert LazyLoader is not None
        assert hasattr(LazyLoader, "__name__")
        assert LazyLoader.__name__ == "LazyLoader"

    def test_lazy_property_import(self) -> None:
        """Teszteli, hogy a lazy_property importálható-e."""
        assert lazy_property is not None
        assert callable(lazy_property)

    def test_singleton_meta_import(self) -> None:
        """Teszteli, hogy a SingletonMeta importálható-e."""
        assert SingletonMeta is not None
        assert hasattr(SingletonMeta, "__name__")
        assert SingletonMeta.__name__ == "SingletonMeta"

    def test_all_exports_available(self) -> None:
        """Teszteli, hogy minden exportált osztály/függvény elérhető-e."""
        from neural_ai.core.base.implementations import __all__

        # CoreComponents nincs az __all__-ban, hogy elkerüljük a körkörös importot
        expected_exports = [
            "DIContainer",
            "LazyComponent",
            "LazyLoader",
            "lazy_property",
            "SingletonMeta",
        ]
        assert __all__ == expected_exports

        # Minden exportált osztály/függvény importálható
        for export_name in __all__:
            module = __import__("neural_ai.core.base.implementations", fromlist=[export_name])
            export_item = getattr(module, export_name)
            assert export_item is not None

    def test_core_components_instantiation(self) -> None:
        """Teszteli, hogy a CoreComponents példányosítható-e."""
        components = CoreComponents()
        assert components is not None
        assert hasattr(components, "config")
        assert hasattr(components, "logger")
        assert hasattr(components, "storage")

    def test_dicontainer_instantiation(self) -> None:
        """Teszteli, hogy a DIContainer példányosítható-e."""
        container = DIContainer()
        assert container is not None
        assert hasattr(container, "register_instance")
        assert hasattr(container, "resolve")

    def test_lazy_component_instantiation(self) -> None:
        """Teszteli, hogy a LazyComponent példányosítható-e."""

        def factory_func() -> str:
            return "test"

        component = LazyComponent(factory_func)
        assert component is not None
        assert hasattr(component, "get")
        assert hasattr(component, "is_loaded")

    def test_lazy_loader_instantiation(self) -> None:
        """Teszteli, hogy a LazyLoader példányosítható-e."""

        def loader_func() -> str:
            return "test"

        loader = LazyLoader(loader_func)
        assert loader is not None
        assert hasattr(loader, "is_loaded")
        assert callable(loader)

    def test_singleton_meta_as_metaclass(self) -> None:
        """Teszteli, hogy a SingletonMeta használható-e metaclass-ként."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj1 = TestClass()
        obj2 = TestClass()

        assert obj1 is obj2
        assert obj1.value == 42

    def test_lazy_property_decorator(self) -> None:
        """Teszteli, hogy a lazy_property dekorátor használható-e."""

        class TestClass:
            def __init__(self) -> None:
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"computed_{self.call_count}"

        obj = TestClass()
        assert obj.call_count == 0

        result1 = obj.expensive_value
        assert result1 == "computed_1"
        assert obj.call_count == 1

        result2 = obj.expensive_value
        assert result2 == "computed_1"
        assert obj.call_count == 1  # Nem nő, mert gyorsítótárazva van
