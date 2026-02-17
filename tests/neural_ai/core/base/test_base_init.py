"""Core base modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.__init__.py fájlban
definiált exportokat és funkcionalitásokat.
"""

from neural_ai.core.base import CoreComponentFactory, CoreComponents, DIContainer


class TestBaseInit:
    """Base modul __init__.py tesztjei."""

    def test_dicontainer_import(self) -> None:
        """Teszteli, hogy a DIContainer importálható-e."""
        # A DIContainer osztály elérhető
        assert DIContainer is not None
        assert hasattr(DIContainer, "__name__")
        assert DIContainer.__name__ == "DIContainer"

    def test_core_components_import(self) -> None:
        """Teszteli, hogy a CoreComponents importálható-e."""
        # A CoreComponents osztály elérhető
        assert CoreComponents is not None
        assert hasattr(CoreComponents, "__name__")
        assert CoreComponents.__name__ == "CoreComponents"

    def test_core_component_factory_import(self) -> None:
        """Teszteli, hogy a CoreComponentFactory importálható-e."""
        # A CoreComponentFactory osztály elérhető
        assert CoreComponentFactory is not None
        assert hasattr(CoreComponentFactory, "__name__")
        assert CoreComponentFactory.__name__ == "CoreComponentFactory"

    def test_all_exports_available(self) -> None:
        """Teszteli, hogy minden exportált osztály elérhető-e."""
        # Az __all__ listában definiált osztályok
        from neural_ai.core.base import __all__

        expected_exports = ["DIContainer", "CoreComponents", "CoreComponentFactory"]
        assert __all__ == expected_exports

        # Minden exportált osztály importálható
        for export_name in __all__:
            module = __import__("neural_ai.core.base", fromlist=[export_name])
            export_class = getattr(module, export_name)
            assert export_class is not None
            assert hasattr(export_class, "__name__")

    def test_type_checking_imports(self) -> None:
        """Teszteli, hogy a TYPE_CHECKING blokkban lévő importok nem okoznak hibát."""
        # Ez a teszt ellenőrzi, hogy a TYPE_CHECKING blokkban lévő importok
        # ne okozzanak futási idejű hibát, mivel azokat csak típusellenőrzéshez használják

        # A teszt egyszerűen csak importálja a modult
        # Ha a TYPE_CHECKING blokk hibás lenne, az importálás során hiba keletkezne
        import neural_ai.core.base

        # A modul sikeresen importálódott
        assert neural_ai.core.base is not None

    def test_dicontainer_instantiation(self) -> None:
        """Teszteli, hogy a DIContainer példányosítható-e."""
        container = DIContainer()
        assert container is not None
        assert hasattr(container, "register_instance")
        assert hasattr(container, "resolve")

    def test_core_components_instantiation(self) -> None:
        """Teszteli, hogy a CoreComponents példányosítható-e."""
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
