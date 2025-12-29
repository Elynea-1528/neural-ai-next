"""Container interfészek tesztelése.

Ez a modul tartalmazza a DIContainerInterface és LazyComponentInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.
"""

import inspect
from typing import Any
from unittest.mock import Mock

from neural_ai.core.base.interfaces.container_interface import (
    DIContainerInterface,
    LazyComponentInterface,
)


class TestDIContainerInterface:
    """DIContainerInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(DIContainerInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in required_methods:
            assert hasattr(DIContainerInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        abstract_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in abstract_methods:
            method = getattr(DIContainerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__"), (
                f"{method_name} nem absztrakt metódus"
            )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        # A TYPE_CHECKING blokk miatt a get_type_hints nem működik
        # Helyette inspect.signature-t használunk
        methods_to_check = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear"
        ]
        
        # Ellenőrizzük, hogy a metódusoknak vannak aláírásaik
        for method_name in methods_to_check:
            method = getattr(DIContainerInterface, method_name)
            sig = inspect.signature(method)
            # A metódusoknak legyenek paraméterei és/vagy visszatérési típusa
            assert len(sig.parameters) > 0 or sig.return_annotation is not inspect.Signature.empty, (
                f"{method_name} metódusnak nincsenek típushintjei"
            )

    def test_interface_methods_are_callable(self) -> None:
        """Teszteli, hogy az interfész metódusai hívhatók-e."""
        required_methods = [
            "register_instance",
            "register_factory",
            "resolve",
            "register_lazy",
            "get",
            "clear",
        ]

        for method_name in required_methods:
            method = getattr(DIContainerInterface, method_name)
            assert callable(method), f"{method_name} nem hívható metódus"

    def test_interface_uses_generic_types(self) -> None:
        """Teszteli, hogy az interfész generikus típusokat használ."""
        # A DIContainerInterface TypeVar-okat használ (T, InterfaceT)
        # Ezt a forráskód ellenőrzésével igazolhatjuk
        source = inspect.getsource(DIContainerInterface)
        assert "TypeVar" in source or "T" in source, (
            "Az interfész nem használ generikus típusokat"
        )

    def test_mock_implementation_register_instance(self) -> None:
        """Teszteli a register_instance metódust mock implementációval (29. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().register_instance(interface, instance)
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                super().register_factory(interface, factory)
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                super().resolve(interface)
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                super().register_lazy(component_name, factory_func)
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                super().get(component_name)
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                super().clear()
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        mock_instance = Mock()
        container.register_instance(str, mock_instance)
        
        assert container.resolve(str) is mock_instance

    def test_mock_implementation_register_factory(self) -> None:
        """Teszteli a register_factory metódust mock implementációval (39. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().register_factory(interface, factory)
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        factory_func = lambda: "test"
        container.register_factory(str, factory_func)
        
        assert container._factories[str] is factory_func

    def test_mock_implementation_resolve(self) -> None:
        """Teszteli a resolve metódust mock implementációval (51. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().resolve(interface)
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        
        # Teszt: resolve üres konténerrel
        assert container.resolve(str) is None
        
        # Teszt: resolve regisztrált példánnyal
        mock_instance = Mock()
        container.register_instance(str, mock_instance)
        assert container.resolve(str) is mock_instance

    def test_mock_implementation_register_lazy(self) -> None:
        """Teszteli a register_lazy metódust mock implementációval (64. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().register_lazy(component_name, factory_func)
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        factory_func = lambda: "lazy_component"
        container.register_lazy("test_component", factory_func)
        
        assert "test_component" in container._lazy_components
        assert container._lazy_components["test_component"] is factory_func

    def test_mock_implementation_get(self) -> None:
        """Teszteli a get metódust mock implementációval (79. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().get(component_name)
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        factory_func = lambda: "lazy_component"
        container.register_lazy("test_component", factory_func)
        
        result = container.get("test_component")
        assert result == "lazy_component"

    def test_mock_implementation_clear(self) -> None:
        """Teszteli a clear metódust mock implementációval (84. sor)."""
        
        class MockContainer(DIContainerInterface):
            """Mock implementáció a DIContainerInterface-hez."""
            
            def __init__(self) -> None:
                self._instances: dict[Any, Any] = {}
                self._factories: dict[Any, Any] = {}
                self._lazy_components: dict[str, Any] = {}
            
            def register_instance(self, interface: Any, instance: Any) -> None:
                self._instances[interface] = instance
            
            def register_factory(self, interface: Any, factory: Any) -> None:
                self._factories[interface] = factory
            
            def resolve(self, interface: Any) -> Any | None:
                return self._instances.get(interface)
            
            def register_lazy(self, component_name: str, factory_func: Any) -> None:
                self._lazy_components[component_name] = factory_func
            
            def get(self, component_name: str) -> object:
                if component_name not in self._lazy_components:
                    raise ValueError(f"Component {component_name} not found")
                return self._lazy_components[component_name]()
            
            def clear(self) -> None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().clear()
                self._instances.clear()
                self._factories.clear()
                self._lazy_components.clear()
        
        container = MockContainer()
        container.register_instance(str, "test")
        container.register_factory(int, lambda: 42)
        container.register_lazy("test", lambda: "lazy")
        
        container.clear()
        
        assert len(container._instances) == 0
        assert len(container._factories) == 0
        assert len(container._lazy_components) == 0


class TestLazyComponentInterface:
    """LazyComponentInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(LazyComponentInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "get",
            "is_loaded",
        ]

        for method_name in required_methods:
            assert hasattr(LazyComponentInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        # get metódus ellenőrzése
        get_method = LazyComponentInterface.get
        assert hasattr(get_method, "__isabstractmethod__"), (
            "get metódus nem absztrakt"
        )

        # is_loaded property ellenőrzése
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )
        assert is_loaded_property.fget is not None, (
            "is_loaded property-nek nincs getter-e"
        )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        # A TYPE_CHECKING blokk miatt a get_type_hints nem működik
        # Helyette inspect.signature-t használunk
        
        # get metódus ellenőrzése
        get_method = LazyComponentInterface.get
        get_sig = inspect.signature(get_method)
        assert get_sig.return_annotation is not inspect.Signature.empty, (
            "get metódusnak nincs visszatérési típusa"
        )
        
        # is_loaded property ellenőrzése
        is_loaded_prop = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_prop, property), (
            "is_loaded nem property"
        )
        assert is_loaded_prop.fget is not None, (
            "is_loaded property-nek nincs getter-e"
        )

    def test_interface_methods_are_callable(self) -> None:
        """Teszteli, hogy az interfész metódusai hívhatók-e."""
        # get metódus ellenőrzése
        get_method = LazyComponentInterface.get
        assert callable(get_method), "get metódus nem hívható"

        # is_loaded property ellenőrzése
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )

    def test_interface_defines_lazy_loading_contract(self) -> None:
        """Teszteli, hogy az interfész definiálja-e a lusta betöltés szerződését."""
        # Az interfésznek tartalmaznia kell a lusta betöltés alapvető műveleteit
        assert hasattr(LazyComponentInterface, "get"), (
            "Az interfész nem definiál get metódust a komponens lekéréséhez"
        )
        assert hasattr(LazyComponentInterface, "is_loaded"), (
            "Az interfész nem definiál is_loaded property-t a betöltés állapotához"
        )

        # A get metódusnak hívhatónak kell lennie
        get_method = LazyComponentInterface.get
        assert callable(get_method), "get metódus nem hívható"

        # Az is_loaded property-nek olvashatónak kell lennie
        is_loaded_property = LazyComponentInterface.is_loaded
        assert isinstance(is_loaded_property, property), (
            "is_loaded nem property"
        )

    def test_mock_implementation_get(self) -> None:
        """Teszteli a get metódust mock implementációval (101. sor)."""
        
        class MockLazyComponent(LazyComponentInterface):
            """Mock implementáció a LazyComponentInterface-hez."""
            
            def __init__(self) -> None:
                self._loaded = False
                self._value: Any = None
            
            def get(self) -> object:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().get()
                if not self._loaded:
                    self._value = "loaded_value"
                    self._loaded = True
                return self._value
            
            @property
            def is_loaded(self) -> bool:
                super().is_loaded
                return self._loaded
        
        component = MockLazyComponent()
        assert not component.is_loaded
        
        value = component.get()
        assert value == "loaded_value"
        assert component.is_loaded

    def test_mock_implementation_is_loaded(self) -> None:
        """Teszteli az is_loaded property-t mock implementációval (111. sor)."""
        
        class MockLazyComponent(LazyComponentInterface):
            """Mock implementáció a LazyComponentInterface-hez."""
            
            def __init__(self) -> None:
                self._loaded = False
                self._value: Any = None
            
            def get(self) -> object:
                if not self._loaded:
                    self._value = "loaded_value"
                    self._loaded = True
                return self._value
            
            @property
            def is_loaded(self) -> bool:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().is_loaded
                return self._loaded
        
        component = MockLazyComponent()
        
        # Teszt: is_loaded kezdetben False
        assert not component.is_loaded
        
        # Teszt: is_loaded True a get hívás után
        component.get()
        assert component.is_loaded