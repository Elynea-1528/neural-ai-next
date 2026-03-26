"""Core base modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.__init__.py fájlban
definiált exportokat és funkcionalitásokat.
"""

from neural_ai.core.base import (
    CoreComponentFactory,
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
    DIContainerInterface,
    LazyComponentInterface,
)
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer


class TestBaseInit:
    """Base modul __init__.py tesztjei."""

    def test_interface_imports(self) -> None:
        """Teszteli, hogy az interfészek importálhatók-e."""
        # Interfészek elérhetők
        assert DIContainerInterface is not None
        assert CoreComponentsInterface is not None
        assert CoreComponentFactoryInterface is not None
        assert LazyComponentInterface is not None

    def test_factory_import(self) -> None:
        """Teszteli, hogy a Factory importálható-e."""
        # A CoreComponentFactory osztály elérhető
        assert CoreComponentFactory is not None
        assert hasattr(CoreComponentFactory, "__name__")
        assert CoreComponentFactory.__name__ == "CoreComponentFactory"

    def test_all_exports_available(self) -> None:
        """Teszteli, hogy minden exportált osztály elérhető-e."""
        # Az __all__ listában definiált osztályok
        from neural_ai.core.base import __all__

        expected_exports = [
            "CoreComponentFactory",
            "CoreComponentFactoryInterface",
            "CoreComponentsInterface",
            "DIContainerInterface",
            "LazyComponentInterface",
        ]
        assert __all__ == expected_exports

        # Minden exportált osztály importálható
        for export_name in __all__:
            module = __import__("neural_ai.core.base", fromlist=[export_name])
            export_class = getattr(module, export_name)
            assert export_class is not None

    def test_implementations_not_exported(self) -> None:
        """Teszteli, hogy az implementációk NEM exportáltak a modul gyökeréből (DDD szabály)."""
        from neural_ai.core.base import __all__

        # Implementációk NEM lehetnek az __all__ listában
        assert "DIContainer" not in __all__
        assert "CoreComponents" not in __all__

    def test_dicontainer_instantiation(self) -> None:
        """Teszteli, hogy a DIContainer példányosítható-e (implementations-ből)."""
        container = DIContainer()
        assert container is not None
        assert hasattr(container, "register_instance")
        assert hasattr(container, "resolve")

    def test_core_components_instantiation(self) -> None:
        """Teszteli, hogy a CoreComponents példányosítható-e (implementations-ből)."""
        components = CoreComponents()
        assert components is not None
        assert hasattr(components, "config")
        assert hasattr(components, "logger")
        assert hasattr(components, "storage")

    def test_core_component_factory_instantiation(self) -> None:
        """Teszteli, hogy a CoreComponentFactory példányosítható-e."""
        container = DIContainer()
        factory = CoreComponentFactory(container)
        assert factory is not None
        assert hasattr(factory, "logger")
        # A config_manager és storage property-k csak akkor érhetők el,
        # ha a konténerben van hozzájuk regisztrálva komponens
        # Ezért csak azt ellenőrizzük, hogy a factory objektum rendelkezik ezekkel a property-kkel
        # A property-k elérésekor DependencyError-t várunk, ha nincs komponens regisztrálva
        assert hasattr(factory, "_config_loader")
        assert hasattr(factory, "_storage_loader")
