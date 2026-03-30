"""Core base interfaces modul __init__.py tesztelése.

Ez a modul teszteli a neural_ai.core.base.interfaces.__init__.py fájlban
definiált exportokat és funkcionalitásokat.
"""

from neural_ai.core.base.interfaces import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
    DIContainerInterface,
    LazyComponentInterface,
)


class TestInterfacesInit:
    """Interfaces modul __init__.py tesztjei."""

    def test_dicontainer_interface_import(self) -> None:
        """Teszteli, hogy a DIContainerInterface importálható-e."""
        assert DIContainerInterface is not None
        assert hasattr(DIContainerInterface, "__name__")
        assert DIContainerInterface.__name__ == "DIContainerInterface"

    def test_lazy_component_interface_import(self) -> None:
        """Teszteli, hogy a LazyComponentInterface importálható-e."""
        assert LazyComponentInterface is not None
        assert hasattr(LazyComponentInterface, "__name__")
        assert LazyComponentInterface.__name__ == "LazyComponentInterface"

    def test_core_components_interface_import(self) -> None:
        """Teszteli, hogy a CoreComponentsInterface importálható-e."""
        assert CoreComponentsInterface is not None
        assert hasattr(CoreComponentsInterface, "__name__")
        assert CoreComponentsInterface.__name__ == "CoreComponentsInterface"

    def test_core_component_factory_interface_import(self) -> None:
        """Teszteli, hogy a CoreComponentFactoryInterface importálható-e."""
        assert CoreComponentFactoryInterface is not None
        assert hasattr(CoreComponentFactoryInterface, "__name__")
        assert CoreComponentFactoryInterface.__name__ == "CoreComponentFactoryInterface"

    def test_all_exports_available(self) -> None:
        """Teszteli, hogy minden exportált interfész elérhető-e."""
        from neural_ai.core.base.interfaces import __all__

        expected_exports = [
            "DIContainerInterface",
            "LazyComponentInterface",
            "CoreComponentsInterface",
            "CoreComponentFactoryInterface",
        ]
        assert __all__ == expected_exports

        # Minden exportált interfész importálható
        for export_name in __all__:
            module = __import__("neural_ai.core.base.interfaces", fromlist=[export_name])
            export_interface = getattr(module, export_name)
            assert export_interface is not None

    def test_interfaces_are_abstract(self) -> None:
        """Teszteli, hogy az interfészek absztraktak-e."""
        import inspect

        assert inspect.isabstract(DIContainerInterface)
        assert inspect.isabstract(LazyComponentInterface)
        assert inspect.isabstract(CoreComponentsInterface)
        assert inspect.isabstract(CoreComponentFactoryInterface)

    def test_dicontainer_interface_methods(self) -> None:
        """Teszteli, hogy a DIContainerInterface rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in required_methods:
            assert hasattr(DIContainerInterface, method_name), f"Hiányzó metódus: {method_name}"

    def test_lazy_component_interface_methods(self) -> None:
        """Teszteli, hogy a LazyComponentInterface rendelkezik a szükséges metódusokkal."""
        assert hasattr(LazyComponentInterface, "get")
        assert hasattr(LazyComponentInterface, "is_loaded")

    def test_core_components_interface_methods(self) -> None:
        """Teszteli, hogy a CoreComponentsInterface rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "config",
            "logger",
            "storage",
            "has_config",
            "has_logger",
            "has_storage",
            "validate",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentsInterface, method_name), f"Hiányzó metódus: {method_name}"

    def test_core_component_factory_interface_methods(self) -> None:
        """Teszteli, hogy a CoreComponentFactoryInterface rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "create_components",
            "create_with_container",
            "create_minimal",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentFactoryInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interfaces_cannot_be_instantiated(self) -> None:
        """Teszteli, hogy az interfészek nem példányosíthatók."""
        import pytest

        with pytest.raises(TypeError):
            DIContainerInterface()  # type: ignore[abstract]  # pyright: ignore[reportAbstractUsage]

        with pytest.raises(TypeError):
            LazyComponentInterface()  # type: ignore[abstract]  # pyright: ignore[reportAbstractUsage]

        with pytest.raises(TypeError):
            CoreComponentsInterface()  # type: ignore[abstract]  # pyright: ignore[reportAbstractUsage]

        with pytest.raises(TypeError):
            CoreComponentFactoryInterface()  # type: ignore[abstract]  # pyright: ignore[reportAbstractUsage]

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy az interfész metódusok absztraktak-e."""
        # DIContainerInterface metódusai
        for method_name in [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]:
            method = getattr(DIContainerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__"), f"{method_name} nem absztrakt metódus"

        # LazyComponentInterface metódusai
        get_method = LazyComponentInterface.get
        assert hasattr(get_method, "__isabstractmethod__"), "get metódus nem absztrakt"

        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), "is_loaded nem property"

        # CoreComponentsInterface metódusai
        for method_name in ["has_config", "has_logger", "has_storage", "validate"]:
            method = getattr(CoreComponentsInterface, method_name)
            assert hasattr(method, "__isabstractmethod__"), f"{method_name} nem absztrakt metódus"

        # CoreComponentFactoryInterface metódusai
        for method_name in ["create_components", "create_with_container", "create_minimal"]:
            method = getattr(CoreComponentFactoryInterface, method_name)
            assert callable(method), f"{method_name} nem hívható"
